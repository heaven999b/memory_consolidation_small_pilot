"""Original-RQ2 stage-attributed metrics: UNMR, conflict-merge-rate, PAR.

The v2 plan (section 6) defines RQ2 as a *staged* failure: extraction/update
errors appear FIRST (consolidation stage), then propagate INTO the answer. The
repo previously collapsed RQ2 to an answer-stage judge label only, so these three
plan metrics had no implementation. This module implements them, each tied to the
pipeline stage the plan assigns, with exact Clopper-Pearson CIs.

Metric definitions (all fractions):

* UNMR(N)  -- Unsupported New Memory Rate. Over the memory statements NEWLY
              created by the N-th consolidation pass, the fraction that lack any
              supporting raw source id. Stage: consolidation hallucination.
* conflict_merge_rate(N) -- over contradictory fact pairs presented to
              consolidation, the fraction merged into ONE incorrect memory
              instead of being resolved or abstained. Stage: update handling.
* PAR(N)   -- Propagation-to-Answer Rate. Over answers, the fraction that cite or
              rely on an unsupported / fabricated memory. Stage: propagation.

Data contract (what a run must emit per item, so these are computable):
  new-memory record  : {"is_new": bool, "has_source_support": bool}
  conflict record    : {"is_contradictory": bool, "merged_incorrectly": bool}
  answer record      : {"used_unsupported_memory": bool}
The consolidation harness populates has_source_support from TierMem's provenance
links (a compact statement is 'supported' iff it points to >=1 raw span). If a run
cannot emit provenance yet, that is the harness change RQ2 needs -- not a scoring
change.
"""
from __future__ import annotations

from typing import Any

from safety_honest_metrics import clopper_pearson


def _rate(k: int, n: int, alpha: float = 0.05) -> dict[str, Any]:
    if n == 0:
        return {"point": None, "lo": None, "hi": None, "num": 0, "den": 0}
    cp = clopper_pearson(k, n, alpha)
    return {"point": cp["point"], "lo": cp["lo"], "hi": cp["hi"], "num": k, "den": n}


def unmr(new_memory_records: list[dict[str, Any]], alpha: float = 0.05) -> dict[str, Any]:
    new = [r for r in new_memory_records if r.get("is_new")]
    k = sum(1 for r in new if not r.get("has_source_support"))
    return _rate(k, len(new), alpha)


def conflict_merge_rate(conflict_records: list[dict[str, Any]], alpha: float = 0.05) -> dict[str, Any]:
    conflicts = [r for r in conflict_records if r.get("is_contradictory")]
    k = sum(1 for r in conflicts if r.get("merged_incorrectly"))
    return _rate(k, len(conflicts), alpha)


def par(answer_records: list[dict[str, Any]], alpha: float = 0.05) -> dict[str, Any]:
    k = sum(1 for r in answer_records if r.get("used_unsupported_memory"))
    return _rate(k, len(answer_records), alpha)


def stage_metrics_by_pass(records_by_pass: dict[int, dict[str, list]], alpha: float = 0.05) -> dict[int, dict[str, Any]]:
    """records_by_pass[N] = {"new_memory": [...], "conflict": [...], "answer": [...]}.

    Returns per-N UNMR / conflict-merge / PAR so the caller can feed the three
    rate-vs-N series into stats_guardrails.cochran_armitage_trend (the plan's
    "errors rise first, then propagate" test).
    """
    out: dict[int, dict[str, Any]] = {}
    for n, recs in sorted(records_by_pass.items()):
        out[n] = {
            "unmr": unmr(recs.get("new_memory", []), alpha),
            "conflict_merge_rate": conflict_merge_rate(recs.get("conflict", []), alpha),
            "par": par(recs.get("answer", []), alpha),
        }
    return out


def _self_test() -> None:
    new = [
        {"is_new": True, "has_source_support": True},
        {"is_new": True, "has_source_support": False},   # unsupported new
        {"is_new": True, "has_source_support": False},   # unsupported new
        {"is_new": False, "has_source_support": True},   # not new -> excluded
    ]
    u = unmr(new)
    assert u["num"] == 2 and u["den"] == 3, u  # 2 of 3 NEW statements unsupported

    conf = [
        {"is_contradictory": True, "merged_incorrectly": True},
        {"is_contradictory": True, "merged_incorrectly": False},
        {"is_contradictory": False, "merged_incorrectly": True},  # not a conflict -> excluded
    ]
    c = conflict_merge_rate(conf)
    assert c["num"] == 1 and c["den"] == 2, c

    ans = [{"used_unsupported_memory": False}, {"used_unsupported_memory": True}]
    p = par(ans)
    assert p["num"] == 1 and p["den"] == 2, p

    # staged view feeds a trend test cleanly
    by_pass = {0: {"new_memory": new, "conflict": conf, "answer": ans}}
    st = stage_metrics_by_pass(by_pass)
    assert st[0]["unmr"]["num"] == 2
    print(f"[rq2_stage_metrics self-test] OK  UNMR={u['point']:.3f} conflict={c['point']:.3f} PAR={p['point']:.3f}")


if __name__ == "__main__":
    _self_test()
