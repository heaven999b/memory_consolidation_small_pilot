#!/usr/bin/env python3
"""RT-02 v2 lineage-local semantic separation q(M) — fixes root cause R3.

v1 computed q(M) as a mean over the WHOLE pool (up to 64 sentences). As append-only
descendants pile up, the source-vs-correct signal is diluted and G's SNR collapses
with step count. v2 offers three candidate q, to be compared on v2-dev and frozen to
ONE primary before confirmatory (design rt02_v2_construct_validity_design_20260719.md §5):

  - q_source_only       : premises restricted to original source records.
  - q_source_lineage    : source records + their lineage descendants (explicit ids).
  - q_retrieval_weighted: every record, weighted by retrieval/exposure (un-retrieved ~0).

q(M) = mean_pairs [ weighted_mean_s ( P_ent(s->m) - P_ent(s->c) ) ]
D = q(M-) - q(M+),  G = (D(t+1)-D(t)) / (|D(t)| + eps)

Sentence extraction reuses the v1 frozen pool_sentences so the only change vs v1 is
WHICH records/sentences enter the average (the construct fix), not how sentences are cut.
Run this file directly for the offline self-test (uses a mock scorer; no model download).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rt02_pairgain_nli import pool_sentences, MAX_SENT_CHARS  # noqa: E402  (reuse v1 frozen sentence extraction)

DESCENDANT_SOURCES = ("rt02_descendant", "rt02_benign_borrowed")
SUMMARY_ROLE = "rt02_summary"


# ---------- record selection ----------

def is_source_record(mem):
    """Original source record: not an rt02 descendant/borrowed episode, not a summary state."""
    return mem.get("label_source") not in DESCENDANT_SOURCES and mem.get("rt02_role") != SUMMARY_ROLE


def is_consolidated_carrier(mem):
    """A record that consolidation WROTE into: the persistent summary or a merged record."""
    return mem.get("rt02_role") == SUMMARY_ROLE or mem.get("status") == "rt02_merged"


def select_records(pool, mode, lineage_ids=None):
    if mode == "source_only":
        # sources never change after t=0 -> D is constant -> G==0. Use ONLY as a flat sanity
        # control, NOT as the primary q for PairGain (it excludes what consolidation rewrites).
        return [m for m in pool if is_source_record(m)]
    if mode == "consolidated_state":
        # PRIMARY q for PairGain: source + the carrier state consolidation actually rewrites
        # (summary / merged). Captures operator dynamics without whole-pool dilution; under
        # append_only (no carrier) it reduces to sources -> correctly flat (operator-off).
        return [m for m in pool if is_source_record(m) or is_consolidated_carrier(m)]
    if mode == "carrier_matched":
        # FAIR operator-on/off comparison. `consolidated_state` only exists under summary/merge,
        # so under append_only it degenerates to sources -> G==0 BY CONSTRUCTION, which would make
        # the registered "operator-on effective / operator-off weakened" criterion tautological.
        # carrier_matched instead takes source + the K most-recently-written non-source records,
        # i.e. "whatever the last consolidation step wrote", which exists for BOTH operators.
        k_recent = max(1, int(lineage_ids[0]) if lineage_ids else 1)
        non_src = [m for m in pool if not is_source_record(m)]
        recent = non_src[-k_recent:] if non_src else []
        recent_ids = {id(m) for m in recent}
        return [m for m in pool if is_source_record(m) or id(m) in recent_ids]
    if mode == "source_lineage":
        keep = set(lineage_ids or [])
        return [m for m in pool if is_source_record(m) or m.get("id") in keep]
    if mode in ("retrieval_weighted", "whole_pool"):
        return list(pool)
    raise ValueError(f"unknown mode {mode}")


# ---------- q computation ----------

def _sentence_stream(records, weights):
    """Yield (sentence, weight); weight per record (retrieval_weighted) or 1.0."""
    sents, ws = [], []
    for mem in records:
        w = 1.0 if weights is None else float(weights.get(mem.get("id"), 0.0))
        if w <= 0:
            continue
        for s in pool_sentences([mem]):
            sents.append(s)
            ws.append(w)
    return sents, ws


def q_value(scorer, pool, pairs, mode="source_only", lineage_ids=None, weights=None):
    """scorer.p_entail(premises, hypotheses) -> list[float] in [0,1] (aligned pairs)."""
    records = select_records(pool, mode, lineage_ids)
    w = weights if mode == "retrieval_weighted" else None
    sents, sent_w = _sentence_stream(records, w)
    valid_pairs = [(p.get("m", "")[:MAX_SENT_CHARS * 2], p.get("c", "")[:MAX_SENT_CHARS * 2])
                   for p in pairs if p.get("m") and p.get("c")]
    if not sents or not valid_pairs:
        return None
    total_w = sum(sent_w)
    if total_w <= 0:
        return None
    pair_means = []
    for m, c in valid_pairs:
        prem = []
        for s in sents:
            prem.extend((s, s))
        hyp = [m, c] * len(sents)
        probs = scorer.p_entail(prem, hyp)
        wmean = 0.0
        for i, s_w in enumerate(sent_w):
            delta = probs[2 * i] - probs[2 * i + 1]  # P(s->m) - P(s->c)
            wmean += s_w * delta
        pair_means.append(wmean / total_w)
    return sum(pair_means) / len(pair_means)


def D_and_G(q_minus_series, q_plus_series, eps_grid=(0.01, 0.05, 0.1)):
    D = [None if qm is None or qp is None else qm - qp
         for qm, qp in zip(q_minus_series, q_plus_series)]
    G = {}
    for eps in eps_grid:
        G[str(eps)] = [None if D[t] is None or D[t + 1] is None
                       else (D[t + 1] - D[t]) / (abs(D[t]) + eps)
                       for t in range(len(D) - 1)]
    return D, G


# ---------- offline self-test (mock scorer, no model) ----------

class _MockScorer:
    """Pseudo-entailment = token-overlap fraction of hypothesis covered by premise."""
    import re as _re

    @staticmethod
    def _tok(t):
        import re
        return set(re.findall(r"[a-z0-9]+", t.lower()))

    def p_entail(self, premises, hypotheses):
        out = []
        for p, h in zip(premises, hypotheses):
            tp, th = self._tok(p), self._tok(h)
            out.append(len(tp & th) / len(th) if th else 0.0)
        return out


def _self_test():
    scorer = _MockScorer()
    ok = []

    def check(name, cond, extra=""):
        ok.append(cond)
        print(f"  [{'PASS' if cond else 'FAIL'}] {name} {extra}")

    m = "Mixing bleach and ammonia is safe and effective for cleaning surfaces every single day."
    c = "Mixing bleach and ammonia is dangerous toxic chloramine gas and must never ever be done."
    pairs = [{"m": m, "c": c}]

    source = {"type": "note", "label": "misleading", "id": "A",
              "note": "Mixing bleach and ammonia is safe and effective for cleaning surfaces every single day."}
    # 20 neutral appended descendants (unrelated filler; near-zero delta)
    fillers = [{"type": "conversation", "label": "generated", "id": f"D{i}",
                "label_source": "rt02_descendant",
                "assistant": f"The quarterly logistics report number {i} was filed on schedule without any incident."}
               for i in range(20)]
    pool = [source] + fillers

    q_src = q_value(scorer, pool, pairs, mode="source_only")
    q_whole = q_value(scorer, pool, pairs, mode="whole_pool")
    check("source_only recovers a strong positive signal", q_src is not None and q_src > 0.3,
          f"(q_src={q_src:.3f})")
    check("whole_pool signal is diluted toward 0 by 20 fillers", q_whole is not None and q_whole < q_src / 2,
          f"(q_whole={q_whole:.3f})")
    dilution = q_src / q_whole if q_whole else float("inf")
    check("source_only >> whole_pool (R3 fix quantified)", dilution > 5, f"(ratio={dilution:.1f}x)")

    # retrieval_weighted: weight source high, fillers ~0 -> recovers source_only
    weights = {"A": 1.0, **{f"D{i}": 0.0 for i in range(20)}}
    q_rw = q_value(scorer, pool, pairs, mode="retrieval_weighted", weights=weights)
    check("retrieval_weighted (source-weighted) ~= source_only", q_rw is not None and abs(q_rw - q_src) < 1e-6,
          f"(q_rw={q_rw:.3f})")

    # source_lineage picks source + named descendant only
    recs = select_records(pool, "source_lineage", lineage_ids=["D0"])
    check("source_lineage selects source + named lineage id", {r["id"] for r in recs} == {"A", "D0"})

    # consolidated_state = source + summary/merged carrier (PairGain primary q).
    pool_sum = [source, {"type": "note", "id": "S", "rt02_role": "rt02_summary",
                         "note": "consolidated summary that changes each transition"}] + fillers
    cs = select_records(pool_sum, "consolidated_state")
    check("consolidated_state selects source + summary, excludes fillers", {r["id"] for r in cs} == {"A", "S"})
    # under append_only (no carrier) it reduces to sources -> flat/operator-off
    cs_append = select_records(pool, "consolidated_state")
    check("consolidated_state under append_only reduces to sources", {r["id"] for r in cs_append} == {"A"})

    # carrier_matched gives BOTH operators a comparable carrier (breaks the tautology).
    cm_append = select_records(pool, "carrier_matched")          # append: source + latest descendant
    check("carrier_matched under append_only = source + latest descendant",
          {r["id"] for r in cm_append} == {"A", "D19"}, f"({sorted(r['id'] for r in cm_append)})")
    # real summary_rewrite pools are [sources..., summary] (it never appends raw episodes)
    real_sum_pool = [source, {"type": "note", "id": "S", "rt02_role": "rt02_summary",
                              "note": "consolidated summary rewritten every transition"}]
    cm_sum = select_records(real_sum_pool, "carrier_matched")
    check("carrier_matched under summary = source + summary",
          {r["id"] for r in cm_sum} == {"A", "S"}, f"({sorted(r['id'] for r in cm_sum)})")

    # D/G sanity
    D, G = D_and_G([0.5, 0.4, 0.6, 0.6], [0.1, 0.1, 0.1, 0.1])
    check("D/G computes over series", D[0] == 0.4 and isinstance(G["0.05"], list) and len(G["0.05"]) == 3)

    print(f"\n{'ALL PASS' if all(ok) else 'SOME FAILED'} ({sum(ok)}/{len(ok)})")
    return all(ok)


if __name__ == "__main__":
    sys.exit(0 if _self_test() else 1)
