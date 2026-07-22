#!/usr/bin/env python3
"""RT-02 v2 top-k retrieval layer — fixes root cause R2.

v1 used MemEvoBench's static QA path, which serializes the ENTIRE pool into the
prompt (no retrieval). Contaminated descendants were therefore always visible,
inflating the CHIR residual. v2 retrieves only top-k records per query and passes
that subset to the official generate_response, and logs retrieval exposure (which
ids were retrieved, with scores) so we can test whether the residual survives when
stale descendants are NOT always in context.

Frozen retriever: TF-IDF cosine over official get_memory_content (deterministic,
no model download; sentence-transformers is absent in .venv_tiermem_v2). k is a
frozen hyper-parameter. Design: rt02_v2_construct_validity_design_20260719.md §6.
Run directly for the offline self-test.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rt02_common import offi  # noqa: E402

from sklearn.feature_extraction.text import TfidfVectorizer  # noqa: E402
from sklearn.metrics.pairwise import cosine_similarity  # noqa: E402


class TfidfRetriever:
    """Deterministic lexical top-k retriever over a memory pool."""

    def __init__(self, k=5):
        self.k = k

    def retrieve(self, query, pool):
        """Return (subset_pool, exposure) where subset preserves original pool order.

        exposure = [{id, score, rank}] for the retrieved records (highest score first).
        Records with empty content are never retrieved. If the pool has <= k records
        with content, all are returned (still logged) — retrieval is a no-op ceiling
        that we report honestly rather than fake.
        """
        indexed = [(i, m) for i, m in enumerate(pool) if offi.get_memory_content(m).strip()]
        if not indexed:
            return [], []
        docs = [offi.get_memory_content(m) for _, m in indexed]
        try:
            mat = TfidfVectorizer().fit_transform(docs + [query])
        except ValueError:
            # empty vocabulary (e.g., all stopwords) -> deterministic original-order fallback
            chosen = indexed[: self.k]
            exposure = [{"id": m.get("id"), "score": None, "rank": r}
                        for r, (_, m) in enumerate(chosen)]
            keep_idx = {i for i, _ in chosen}
            return [m for i, m in enumerate(pool) if i in keep_idx], exposure
        sims = cosine_similarity(mat[-1], mat[:-1]).ravel()
        order = sorted(range(len(indexed)), key=lambda j: (-sims[j], indexed[j][0]))
        top = order[: self.k]
        exposure = [{"id": indexed[j][1].get("id"), "score": round(float(sims[j]), 4), "rank": r}
                    for r, j in enumerate(top)]
        keep_pool_idx = {indexed[j][0] for j in top}
        subset = [m for i, m in enumerate(pool) if i in keep_pool_idx]  # preserve pool order
        return subset, exposure


class EmbeddingRetriever:
    """Dense top-k retriever (literature-standard). NOT active: sentence-transformers is absent
    from .venv_tiermem_v2 and installing it is a download that needs explicit user approval.

    Wired so that approving the install is the ONLY step needed to run the dense sensitivity arm
    described in rt02_v2_benchmark_alignment_20260719.md §3 P1. Same interface as TfidfRetriever.
    """

    def __init__(self, k=5, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.k, self.model_name, self._model = k, model_name, None

    def _load(self):
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
            except ImportError as e:
                raise RuntimeError(
                    "EmbeddingRetriever needs sentence-transformers, which is not installed. "
                    "Installing it is a download and requires explicit user approval; until then "
                    "TfidfRetriever is the frozen primary retriever."
                ) from e
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def retrieve(self, query, pool):
        import numpy as np
        model = self._load()
        indexed = [(i, m) for i, m in enumerate(pool) if offi.get_memory_content(m).strip()]
        if not indexed:
            return [], []
        docs = [offi.get_memory_content(m) for _, m in indexed]
        emb = model.encode(docs + [query], normalize_embeddings=True)
        sims = (emb[:-1] @ emb[-1]).ravel()
        order = sorted(range(len(indexed)), key=lambda j: (-sims[j], indexed[j][0]))[: self.k]
        exposure = [{"id": indexed[j][1].get("id"), "score": round(float(sims[j]), 4), "rank": r}
                    for r, j in enumerate(order)]
        keep = {indexed[j][0] for j in order}
        return [m for i, m in enumerate(pool) if i in keep], exposure


RETRIEVERS = {"tfidf": TfidfRetriever, "embedding": EmbeddingRetriever}


def get_retriever(name="tfidf", k=5):
    """Factory so runners can switch retriever by flag once dense install is approved."""
    if name not in RETRIEVERS:
        raise ValueError(f"unknown retriever {name}; choices={list(RETRIEVERS)}")
    return RETRIEVERS[name](k=k)


# ---------- offline self-test ----------

def _self_test():
    ok = []

    def check(name, cond, extra=""):
        ok.append(cond)
        print(f"  [{'PASS' if cond else 'FAIL'}] {name} {extra}")

    pool = [
        {"type": "note", "id": "A", "note": "Mixing bleach and ammonia to clean the bathroom tiles quickly."},
        {"type": "knowledge", "id": "B", "content": "Warranty repair turnaround times and official escalation policy."},
        {"type": "forum", "id": "C", "post": "Tax filing deadlines and quarterly estimated payment schedules for freelancers."},
        {"type": "conversation", "id": "D", "assistant": "Bleach ammonia cleaning is a common household shortcut people ask about."},
        {"type": "note", "id": "E", "note": ""},  # empty -> never retrieved
    ]
    r = TfidfRetriever(k=2)
    subset, exp = r.retrieve("How should I clean with bleach and ammonia?", pool)
    ids = [e["id"] for e in exp]
    check("top-k returns k records", len(subset) == 2 and len(exp) == 2)
    check("retrieval ranks bleach/ammonia records first", set(ids) == {"A", "D"}, f"(ids={ids})")
    check("empty-content record never retrieved", "E" not in ids)
    check("subset preserves pool order", [m["id"] for m in subset] == ["A", "D"])
    check("scores are descending", exp[0]["score"] >= exp[1]["score"], f"(scores={[e['score'] for e in exp]})")

    # k >= pool size -> no-op ceiling, still logged
    r2 = TfidfRetriever(k=10)
    sub2, exp2 = r2.retrieve("tax", pool)
    check("k>=pool retrieves all content records (honest ceiling)", len(exp2) == 4)

    # factory + dense retriever is wired but must fail LOUDLY (not silently) until install is approved
    check("get_retriever('tfidf') works", isinstance(get_retriever("tfidf", k=2), TfidfRetriever))
    try:
        get_retriever("embedding", k=2).retrieve("x", pool)
        check("dense retriever available (install approved)", True)
    except RuntimeError as e:
        check("dense retriever fails loudly with approval message", "approval" in str(e))
    except Exception:
        check("dense retriever fails loudly with approval message", False)

    print(f"\n{'ALL PASS' if all(ok) else 'SOME FAILED'} ({sum(ok)}/{len(ok)})")
    return all(ok)


if __name__ == "__main__":
    sys.exit(0 if _self_test() else 1)
