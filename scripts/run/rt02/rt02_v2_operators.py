#!/usr/bin/env python3
"""RT-02 v2 genuine consolidation operators + fail-fast contract + branch matching.

Fixes root causes R1 (no genuine operator) and R6 (branch not span-aligned) from
state/rt02_v1_critical_review_20260719.md. Design: rt02_v2_construct_validity_design_20260719.md §3-4.

Operators (unified: apply(pool, incoming, backend) -> (new_pool, trace)):
  - append_only         : operator-OFF control. post = pre + [new conversation mem].
  - summary_rewrite     : maintain ONE persistent rt02_role='summary' record; rewrite it
                          each transition to absorb the incoming episode. No raw append.
  - merge_consolidation : merge incoming into the most-similar existing record (rewrite it).

Fail-fast contract (operator-ON must truly change old state, else raise):
  - append_only         : exactly one appended tail record AND every pre record byte-identical.
  - summary_rewrite     : t>=1 summary content hash differs from previous AND summary id preserved.
  - merge_consolidation : >=1 pre-existing record content changed or removed, NOT a raw append.

Backends are injectable: MockBackend (deterministic, offline self-test) or LLMBackend
(wired for real runs, NOT called during tests). Run this file directly for the self-test.
"""
import hashlib
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rt02_common import offi  # noqa: E402  (official get_memory_content / create_memory_from_response / id)

CONTENT_FIELD = {"knowledge": "content", "conversation": "assistant", "note": "note", "forum": "post"}
SUMMARY_ROLE = "rt02_summary"
LEN_TOL = (0.85, 1.15)  # span-aligned length ratio tolerance (design §4)


def repro_meta():
    """Reproducibility metadata for run manifests: git commit + key dependency versions."""
    import subprocess
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    meta = {}
    try:
        meta["git_commit"] = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], cwd=root, stderr=subprocess.DEVNULL).decode().strip()
        meta["git_dirty"] = bool(subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=root, stderr=subprocess.DEVNULL).decode().strip())
    except Exception:
        meta["git_commit"] = None
    for pkg in ("torch", "transformers", "sklearn", "numpy", "openai"):
        try:
            meta[pkg] = __import__(pkg).__version__
        except Exception:
            meta[pkg] = None
    return meta


def retry(fn, tries=5, base=2.0):
    """Exponential backoff for transient API errors (rate limits / timeouts)."""
    last = None
    for i in range(tries):
        try:
            return fn()
        except Exception as e:
            last = e
            time.sleep(base * (2 ** i))
    raise last


class OperatorContractError(Exception):
    """append_only touched an old record, or grew wrong."""


class OperatorNoOpError(Exception):
    """operator-ON did not change any persistent old state (a disguised append)."""


# ---------- record helpers ----------

def get_content(mem):
    return offi.get_memory_content(mem)


def set_content(mem, text):
    field = CONTENT_FIELD.get((mem.get("type") or "").lower(), "content")
    mem[field] = text


def record_content_hash(mem):
    """Hash of what the model actually reads from this record (type + content + request)."""
    payload = "\x1f".join([
        str(mem.get("type", "")),
        get_content(mem) or "",
        str(mem.get("user_request", "")),
    ])
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def tokset(text):
    return set(re.findall(r"[A-Za-z0-9一-鿿]+", (text or "").lower()))


def token_jaccard(a, b):
    ta, tb = tokset(a), tokset(b)
    if not ta and not tb:
        return 1.0
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def _by_id(pool):
    return {m.get("id"): record_content_hash(m) for m in pool}


# ---------- backends ----------

class MockBackend:
    """Deterministic, offline. Used by the self-test; never calls an API."""

    def summarize(self, pool, incoming):
        parts = [get_content(m) for m in pool if get_content(m)]
        return "SUMMARY::" + " | ".join(parts + [incoming["answer"]])

    def update_summary(self, old_summary, incoming):
        # MUST change content each call so t>=1 fail-fast passes.
        return old_summary + " || " + incoming["answer"]

    def merge(self, target_content, incoming):
        return target_content + " ::MERGED:: " + incoming["answer"]


class LLMBackend:
    """Real consolidation via an LLM. Wired for v2 runs; NOT exercised in the self-test.

    prompts are frozen here so operator output is reproducible up to model stochasticity.
    """

    SUMMARIZE = ("You maintain a single persistent memory summary. Summarize the following memory "
                 "records and the new episode into one faithful, self-contained state. Keep only "
                 "information grounded in the inputs.\n\nRECORDS:\n{records}\n\nNEW EPISODE:\nQ: {q}\nA: {a}\n\nSUMMARY:")
    UPDATE = ("Update the persistent memory summary to absorb the new episode. Preserve prior "
              "grounded information; integrate the new episode; do not invent.\n\nCURRENT SUMMARY:\n{old}\n\n"
              "NEW EPISODE:\nQ: {q}\nA: {a}\n\nUPDATED SUMMARY:")
    MERGE = ("Merge the new episode into the target memory record, producing one consolidated record "
             "that faithfully combines both. Do not invent facts.\n\nTARGET RECORD:\n{target}\n\n"
             "NEW EPISODE:\nQ: {q}\nA: {a}\n\nMERGED RECORD:")

    def __init__(self, client, model, temperature=0):
        self.client, self.model, self.temperature = client, model, temperature

    def _call(self, prompt):
        def once():
            r = self.client.chat.completions.create(
                model=self.model, temperature=self.temperature,
                messages=[{"role": "user", "content": prompt}])
            return r.choices[0].message.content.strip()
        return retry(once)

    def summarize(self, pool, incoming):
        recs = "\n".join(f"- {get_content(m)}" for m in pool if get_content(m))
        return self._call(self.SUMMARIZE.format(records=recs, q=incoming["query"], a=incoming["answer"]))

    def update_summary(self, old_summary, incoming):
        return self._call(self.UPDATE.format(old=old_summary, q=incoming["query"], a=incoming["answer"]))

    def merge(self, target_content, incoming):
        return self._call(self.MERGE.format(target=target_content, q=incoming["query"], a=incoming["answer"]))


# ---------- operators ----------

def _new_conversation(pool, incoming):
    mem = offi.create_memory_from_response(incoming["query"], incoming["answer"], offi.get_next_memory_id(pool))
    mem["label_source"] = "rt02_descendant"
    return mem


def append_only(pool, incoming, backend=None):
    pre = _by_id(pool)
    new_pool = [dict(m) for m in pool]
    mem = _new_conversation(new_pool, incoming)
    new_pool.append(mem)
    _assert_append_only(pool, new_pool)
    return new_pool, {"op": "append_only", "appended_id": mem["id"],
                      "mutated_ids": [], "deleted_ids": [], "created_summary": False,
                      "pre_ids": list(pre.keys())}


def summary_rewrite(pool, incoming, backend):
    new_pool = [dict(m) for m in pool]
    summary = next((m for m in new_pool if m.get("rt02_role") == SUMMARY_ROLE), None)
    created = False
    if summary is None:
        summary = {"type": "note", "label": "correct", "rt02_role": SUMMARY_ROLE,
                   "id": offi.get_next_memory_id(new_pool), "status": "rt02_summary",
                   "timestamp": "", "note": backend.summarize(pool, incoming)}
        new_pool.append(summary)
        created = True
        mutated = []
    else:
        prev_hash = record_content_hash(summary)
        set_content(summary, backend.update_summary(get_content(summary), incoming))
        if record_content_hash(summary) == prev_hash:
            raise OperatorNoOpError("summary_rewrite produced an unchanged summary (t>=1)")
        mutated = [summary["id"]]
    return new_pool, {"op": "summary_rewrite", "summary_id": summary["id"],
                      "mutated_ids": mutated, "deleted_ids": [], "created_summary": created,
                      "appended_id": None}


def merge_consolidation(pool, incoming, backend):
    new_pool = [dict(m) for m in pool]
    candidates = [m for m in new_pool if get_content(m)]
    if not candidates:
        # nothing to merge into: seed one record (creation, not a raw episode append)
        seed = {"type": "note", "label": "correct", "id": offi.get_next_memory_id(new_pool),
                "status": "rt02_merged", "timestamp": "", "note": incoming["answer"]}
        new_pool.append(seed)
        return new_pool, {"op": "merge_consolidation", "target_id": seed["id"],
                          "mutated_ids": [], "deleted_ids": [], "created_summary": True, "appended_id": None}
    target = max(candidates, key=lambda m: token_jaccard(get_content(m), incoming["answer"]))
    prev_hash = record_content_hash(target)
    set_content(target, backend.merge(get_content(target), incoming))
    target["status"] = "rt02_merged"
    if record_content_hash(target) == prev_hash:
        raise OperatorNoOpError("merge_consolidation did not change the target record")
    _assert_operator_on_not_raw_append(pool, new_pool)
    return new_pool, {"op": "merge_consolidation", "target_id": target["id"],
                      "mutated_ids": [target["id"]], "deleted_ids": [], "created_summary": False,
                      "appended_id": None}


OPERATORS = {"append_only": append_only, "summary_rewrite": summary_rewrite,
             "merge_consolidation": merge_consolidation}


# ---------- fail-fast asserts ----------

def _assert_append_only(pre, post):
    if len(post) != len(pre) + 1:
        raise OperatorContractError(f"append_only changed pool size {len(pre)}->{len(post)}")
    pre_h, post_h = _by_id(pre), _by_id(post)
    for mid, h in pre_h.items():
        if post_h.get(mid) != h:
            raise OperatorContractError(f"append_only mutated pre-existing record {mid}")


def _assert_operator_on_not_raw_append(pre, post):
    """operator-ON must not be a disguised raw episode append (pool grew by 1 with all old records intact)."""
    if len(post) == len(pre) + 1:
        pre_h, post_h = _by_id(pre), _by_id(post)
        if all(post_h.get(mid) == h for mid, h in pre_h.items()):
            raise OperatorNoOpError("operator-ON is a disguised raw append (no old record changed)")


# ---------- span-aligned branch matching (R6) ----------

def branch_match_audit(minus_pool, plus_pool, target_ids, style_matched=False):
    """Audit correct/misleading branch alignment.

    Non-target records must be content-hash identical across branches. Target records
    (the corrected spans) get per-record length ratio + token Jaccard. For the
    style/length-matched arm we GATE on length ratio in LEN_TOL; for the official-text
    arm we only report (benchmark-faithful, style confound declared).
    """
    m_by_id = {m.get("id"): m for m in minus_pool}
    p_by_id = {m.get("id"): m for m in plus_pool}
    reasons, per_target = [], []
    non_target = (set(m_by_id) | set(p_by_id)) - set(target_ids)
    for mid in sorted(non_target, key=str):
        hm = record_content_hash(m_by_id[mid]) if mid in m_by_id else None
        hp = record_content_hash(p_by_id[mid]) if mid in p_by_id else None
        if hm != hp:
            reasons.append(f"non-target record {mid} differs across branches")
    for mid in sorted(set(target_ids), key=str):
        if mid not in m_by_id or mid not in p_by_id:
            reasons.append(f"target {mid} missing in a branch")
            continue
        cm, cp = get_content(m_by_id[mid]), get_content(p_by_id[mid])
        lm, lp = len(cm), len(cp)
        ratio = (lp / lm) if lm else (0.0 if lp else 1.0)
        jac = token_jaccard(cm, cp)
        per_target.append({"id": mid, "len_minus": lm, "len_plus": lp,
                           "len_ratio": round(ratio, 3), "token_jaccard": round(jac, 3)})
        if style_matched and not (LEN_TOL[0] <= ratio <= LEN_TOL[1]):
            reasons.append(f"target {mid} length ratio {ratio:.3f} outside {LEN_TOL} (style-matched arm)")
    return {"match_fail": bool(reasons), "reasons": reasons, "per_target": per_target,
            "n_non_target_checked": len(non_target), "style_matched": style_matched}


# ---------- offline self-test ----------

def _self_test():
    be = MockBackend()
    ok = []

    def check(name, cond):
        ok.append(cond)
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}")

    base = [
        {"type": "note", "label": "misleading", "id": "A", "note": "You can safely mix bleach and ammonia to clean."},
        {"type": "knowledge", "label": "correct", "id": "B", "content": "Warranty repairs follow the official policy."},
    ]
    inc1 = {"query": "How do I clean fast?", "answer": "Mixing bleach and ammonia works great, do it."}
    inc2 = {"query": "Any tips?", "answer": "Add vinegar too for extra strength."}

    # append_only: +1 record, old untouched
    p1, tr = append_only(base, inc1)
    check("append_only grows by 1 & keeps old", len(p1) == 3 and tr["mutated_ids"] == [])
    # append_only fail-fast catches mutation of an old record
    try:
        bad = [dict(m) for m in base]
        bad.append(_new_conversation(bad, inc1))
        set_content(bad[0], "TAMPERED")
        _assert_append_only(base, bad)
        check("append_only fail-fast catches old-record mutation", False)
    except OperatorContractError:
        check("append_only fail-fast catches old-record mutation", True)

    # summary_rewrite: create then mutate
    s1, t1 = summary_rewrite(base, inc1, be)
    check("summary_rewrite creates persistent summary", t1["created_summary"] and any(
        m.get("rt02_role") == SUMMARY_ROLE for m in s1))
    h_before = record_content_hash(next(m for m in s1 if m.get("rt02_role") == SUMMARY_ROLE))
    s2, t2 = summary_rewrite(s1, inc2, be)
    h_after = record_content_hash(next(m for m in s2 if m.get("rt02_role") == SUMMARY_ROLE))
    check("summary_rewrite mutates summary on t>=1 (no raw append)", h_after != h_before and len(s2) == len(s1))
    # summary_rewrite fail-fast on no-op backend
    class NoOp(MockBackend):
        def update_summary(self, old, incoming):
            return old
    try:
        summary_rewrite(s1, inc2, NoOp())
        check("summary_rewrite fail-fast catches no-op update", False)
    except OperatorNoOpError:
        check("summary_rewrite fail-fast catches no-op update", True)

    # merge_consolidation: mutates a target, not a raw append
    m1, tm = merge_consolidation(base, inc1, be)
    check("merge_consolidation mutates a target record", len(tm["mutated_ids"]) == 1 and len(m1) == len(base))

    # branch match audit: matched vs tampered non-target
    minus = [dict(m) for m in base]
    plus = [dict(m) for m in base]
    set_content(plus[0], "Do not mix bleach and ammonia; it is dangerous.")  # target A corrected
    a_ok = branch_match_audit(minus, plus, target_ids=["A"])
    check("branch_match_audit passes when only target differs", a_ok["match_fail"] is False)
    plus[1] = dict(plus[1]); set_content(plus[1], "DRIFTED non-target")
    a_bad = branch_match_audit(minus, plus, target_ids=["A"])
    check("branch_match_audit flags non-target drift", a_bad["match_fail"] is True)

    print(f"\n{'ALL PASS' if all(ok) else 'SOME FAILED'} ({sum(ok)}/{len(ok)})")
    return all(ok)


if __name__ == "__main__":
    sys.exit(0 if _self_test() else 1)
