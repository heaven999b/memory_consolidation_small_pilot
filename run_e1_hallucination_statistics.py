#!/usr/bin/env python3
"""E1 hallucination-axis statistics: bootstrap CIs and paired significance.

This is a *post-hoc* analysis layer over the per-item failure-mode judge
artifacts already produced by ``run_v2_tiermem_micro_failure_mode_judge.py``.
It does NOT call any API and does NOT re-run any benchmark. It turns the
existing single-run point estimates (e.g. "unsupported fabrication 0.333 -> 0.167")
into interval estimates with paired significance tests, so the E1 signal can be
reported with proper uncertainty instead of bare fractions.

Two families of statistics are produced per experiment family:

1. Per-condition metric with a percentile bootstrap 95% CI. The bootstrap
   resamples the *items* of a single run with replacement, so the CI reflects
   uncertainty from the finite item sample (n=15 or n=45). It does NOT capture
   seed / LLM-sampling stochasticity -- that requires the multi-seed live runs
   built in ``run_e1_multiseed_sweep.py``. This is stated explicitly in the
   report so the CI is not over-read.

2. Paired McNemar exact tests across consolidation depth N (items aligned by
   ``query_id`` within a fixed route_mode), for the binary outcomes
   "answer is CORRECT" and "unsupported fabrication on an unknown-abstain item".
   This tests whether increasing N flips per-item outcomes beyond chance.

Usage
-----
    python3 run_e1_hallucination_statistics.py            # default headline families
    python3 run_e1_hallucination_statistics.py \
        --judge-report outputs/v2_tiermem_micro/judge_reports/<name>.json \
        --bootstrap 10000 --rng-seed 12345
"""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import numpy as np
from scipy.stats import binomtest


PROJECT_ROOT = Path(__file__).resolve().parent
JUDGE_DIR = PROJECT_ROOT / "outputs" / "v2_tiermem_micro" / "judge_reports"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "outputs" / "v2_tiermem_micro" / "stats"

# The failure-mode judge label vocabulary (see run_v2_tiermem_micro_failure_mode_judge.py).
LABEL_CORRECT = "CORRECT"
LABEL_ABSTAIN_FORGETTING = "ABSTAIN_FORGETTING"
LABEL_UNSUPPORTED_FABRICATION = "UNSUPPORTED_FABRICATION"
LABEL_FACT_DISTORTION = "FACT_DISTORTION"
CLASS_FACTUAL = "FACTUAL"
CLASS_UNKNOWN = "UNKNOWN_ABSTAIN"

# Default headline families: the single-session depth sweep that reaches N=8,
# and the 3-session (45 QA) sweep. Both are real gpt-4.1-mini runs.
DEFAULT_JUDGE_REPORTS = [
    "e1_halumem_targeted_cov10_depth_20260701_judge_relaxed_net.json",
    "e1_halumem_targeted_cov10_multisession3_fix_20260701_judge_relaxed_net.json",
]


@dataclass
class Item:
    query_id: str
    judge_label: str
    gold_answerability: str
    exact_match_score: float


@dataclass
class Condition:
    run_id: str
    route_mode: Optional[str]
    passes: int
    summary_f1: float
    summary_bleu1: float
    items: list[Item] = field(default_factory=list)


def _load_condition_items(detail_json_path: str) -> list[Item]:
    path = Path(detail_json_path)
    if not path.exists():
        # detail_json is stored as an absolute path; fall back to basename lookup.
        alt = JUDGE_DIR / Path(detail_json_path).parent.name / Path(detail_json_path).name
        path = alt if alt.exists() else path
    payload = json.loads(path.read_text(encoding="utf-8"))
    details = payload.get("details") or []
    items: list[Item] = []
    for row in details:
        try:
            em = float(row.get("exact_match_score", 0.0) or 0.0)
        except (TypeError, ValueError):
            em = 0.0
        items.append(
            Item(
                query_id=str(row.get("query_id")),
                judge_label=str(row.get("judge_label") or "ERROR"),
                gold_answerability=str(row.get("gold_answerability") or ""),
                exact_match_score=em,
            )
        )
    return items


def load_family(judge_report_path: Path) -> tuple[str, list[Condition]]:
    payload = json.loads(judge_report_path.read_text(encoding="utf-8"))
    report_id = payload.get("report_id") or judge_report_path.stem
    conditions: list[Condition] = []
    for cond in payload.get("conditions", []):
        items = _load_condition_items(cond.get("detail_json", ""))
        conditions.append(
            Condition(
                run_id=cond.get("run_id", ""),
                route_mode=cond.get("route_mode"),
                passes=int(cond.get("consolidation_passes", 0) or 0),
                summary_f1=float(cond.get("summary_f1", 0.0) or 0.0),
                summary_bleu1=float(cond.get("summary_bleu1", 0.0) or 0.0),
                items=items,
            )
        )
    conditions.sort(key=lambda c: (str(c.route_mode), c.passes))
    return report_id, conditions


# ---------------------------------------------------------------------------
# Metric definitions (operate on a list[Item]).
# ---------------------------------------------------------------------------

def _rate_all(items: list[Item], predicate) -> tuple[int, int]:
    num = sum(1 for it in items if predicate(it))
    return num, len(items)


def _rate_within(items: list[Item], gold_class: str, predicate) -> tuple[int, int]:
    subset = [it for it in items if it.gold_answerability == gold_class]
    num = sum(1 for it in subset if predicate(it))
    return num, len(subset)


METRICS = {
    "correct_rate": lambda items: _rate_all(items, lambda it: it.judge_label == LABEL_CORRECT),
    "unsupported_fabrication_on_unknown": lambda items: _rate_within(
        items, CLASS_UNKNOWN, lambda it: it.judge_label == LABEL_UNSUPPORTED_FABRICATION
    ),
    "abstain_forgetting_on_factual": lambda items: _rate_within(
        items, CLASS_FACTUAL, lambda it: it.judge_label == LABEL_ABSTAIN_FORGETTING
    ),
    "fact_distortion_on_factual": lambda items: _rate_within(
        items, CLASS_FACTUAL, lambda it: it.judge_label == LABEL_FACT_DISTORTION
    ),
}


def bootstrap_ci(
    items: list[Item],
    metric_key: str,
    n_boot: int,
    rng: np.random.Generator,
    alpha: float = 0.05,
) -> dict[str, Any]:
    """Percentile bootstrap CI by resampling items with replacement.

    For within-class rates the denominator is recomputed inside each resample;
    draws whose class denominator is 0 are dropped (reported as effective_boot).
    """
    metric_fn = METRICS[metric_key]
    num, den = metric_fn(items)
    point = (num / den) if den else float("nan")
    if den == 0:
        return {"point": point, "num": num, "den": den, "ci_low": float("nan"),
                "ci_high": float("nan"), "effective_boot": 0}

    n = len(items)
    idx_all = np.arange(n)
    draws: list[float] = []
    for _ in range(n_boot):
        sample_idx = rng.choice(idx_all, size=n, replace=True)
        sample = [items[i] for i in sample_idx]
        s_num, s_den = metric_fn(sample)
        if s_den == 0:
            continue
        draws.append(s_num / s_den)
    if not draws:
        return {"point": point, "num": num, "den": den, "ci_low": float("nan"),
                "ci_high": float("nan"), "effective_boot": 0}
    arr = np.array(draws)
    lo = float(np.percentile(arr, 100 * (alpha / 2)))
    hi = float(np.percentile(arr, 100 * (1 - alpha / 2)))
    return {
        "point": point,
        "num": num,
        "den": den,
        "ci_low": lo,
        "ci_high": hi,
        "boot_mean": float(arr.mean()),
        "effective_boot": len(draws),
    }


def mcnemar_exact(baseline: Condition, other: Condition, outcome: str) -> dict[str, Any]:
    """Paired exact McNemar test aligning items by query_id.

    outcome="correct": binary "answer is CORRECT".
    outcome="uf_unknown": binary "unsupported fabrication", restricted to items
        that are UNKNOWN_ABSTAIN in BOTH conditions.
    Reports discordant counts and the two-sided exact binomial p-value.
    """
    base = {it.query_id: it for it in baseline.items}
    oth = {it.query_id: it for it in other.items}
    shared = [qid for qid in base if qid in oth]

    def outcome_val(it: Item) -> Optional[int]:
        if outcome == "correct":
            return 1 if it.judge_label == LABEL_CORRECT else 0
        if outcome == "uf_unknown":
            if it.gold_answerability != CLASS_UNKNOWN:
                return None
            return 1 if it.judge_label == LABEL_UNSUPPORTED_FABRICATION else 0
        raise ValueError(outcome)

    # b = baseline 0 -> other 1 ; c = baseline 1 -> other 0
    b = c = n_pairs = 0
    for qid in shared:
        bv = outcome_val(base[qid])
        ov = outcome_val(oth[qid])
        if bv is None or ov is None:
            continue
        n_pairs += 1
        if bv == 0 and ov == 1:
            b += 1
        elif bv == 1 and ov == 0:
            c += 1
    discordant = b + c
    if discordant == 0:
        p_value = 1.0
    else:
        p_value = float(binomtest(b, discordant, 0.5, alternative="two-sided").pvalue)
    return {
        "outcome": outcome,
        "n_pairs": n_pairs,
        "baseline_to_other_0to1": b,
        "baseline_to_other_1to0": c,
        "discordant": discordant,
        "p_value": p_value,
    }


def analyze_family(report_id: str, conditions: list[Condition], n_boot: int,
                   rng_seed: int) -> dict[str, Any]:
    rng = np.random.default_rng(rng_seed)
    cond_out: list[dict[str, Any]] = []
    for cond in conditions:
        metrics = {key: bootstrap_ci(cond.items, key, n_boot, rng) for key in METRICS}
        cond_out.append({
            "run_id": cond.run_id,
            "route_mode": cond.route_mode,
            "consolidation_passes": cond.passes,
            "n_items": len(cond.items),
            "n_factual": sum(1 for it in cond.items if it.gold_answerability == CLASS_FACTUAL),
            "n_unknown": sum(1 for it in cond.items if it.gold_answerability == CLASS_UNKNOWN),
            "summary_f1": cond.summary_f1,
            "summary_bleu1": cond.summary_bleu1,
            "metrics": metrics,
        })

    # Paired tests: within each route_mode, compare every N>0 against N=0.
    paired: list[dict[str, Any]] = []
    by_route: dict[Optional[str], list[Condition]] = {}
    for cond in conditions:
        by_route.setdefault(cond.route_mode, []).append(cond)
    for route, conds in by_route.items():
        conds = sorted(conds, key=lambda c: c.passes)
        baseline = next((c for c in conds if c.passes == 0), None)
        if baseline is None:
            continue
        for cond in conds:
            if cond.passes == 0:
                continue
            for outcome in ("correct", "uf_unknown"):
                res = mcnemar_exact(baseline, cond, outcome)
                res.update({"route_mode": route, "baseline_passes": 0, "other_passes": cond.passes})
                paired.append(res)
    return {"report_id": report_id, "conditions": cond_out, "paired_tests": paired}


def _fmt_ci(m: dict[str, Any]) -> str:
    if m["den"] == 0 or math.isnan(m.get("ci_low", float("nan"))):
        return "n/a"
    return f"{m['point']:.3f} [{m['ci_low']:.3f}, {m['ci_high']:.3f}] ({m['num']}/{m['den']})"


def render_markdown(analyses: list[dict[str, Any]], n_boot: int, rng_seed: int) -> str:
    lines = [
        "# E1 hallucination statistics: bootstrap CI + paired McNemar",
        "",
        f"- generated_at: `{datetime.now().isoformat(timespec='seconds')}`",
        f"- bootstrap resamples: `{n_boot}` (percentile 95% CI), rng_seed: `{rng_seed}`",
        "- **Scope of the CI**: the bootstrap resamples *items within a single run*, "
        "so the interval reflects finite-item-sample uncertainty only. These are "
        "still single-seed, single-backbone (gpt-4.1-mini) runs; seed / sampling "
        "stochasticity is NOT captured here and requires the multi-seed live sweep.",
        "- Paired tests align items by `query_id` within a fixed route_mode and use "
        "the two-sided exact binomial (McNemar) on discordant pairs.",
        "",
    ]
    for a in analyses:
        lines.append(f"## Family: `{a['report_id']}`")
        lines.append("")
        lines.append("### Per-condition metrics (point [95% CI] (num/den))")
        lines.append("")
        lines.append("| route | N | n | correct_rate | UF_on_unknown | AF_on_factual | FD_on_factual | F1 |")
        lines.append("| --- | ---: | ---: | --- | --- | --- | --- | ---: |")
        for c in a["conditions"]:
            m = c["metrics"]
            lines.append(
                "| {route} | {n} | {ni} | {cr} | {uf} | {af} | {fd} | {f1:.3f} |".format(
                    route=c["route_mode"],
                    n=c["consolidation_passes"],
                    ni=c["n_items"],
                    cr=_fmt_ci(m["correct_rate"]),
                    uf=_fmt_ci(m["unsupported_fabrication_on_unknown"]),
                    af=_fmt_ci(m["abstain_forgetting_on_factual"]),
                    fd=_fmt_ci(m["fact_distortion_on_factual"]),
                    f1=c["summary_f1"],
                )
            )
        lines.append("")
        lines.append("### Paired McNemar vs N=0 (same route)")
        lines.append("")
        lines.append("| route | N vs 0 | outcome | pairs | 0->1 | 1->0 | discordant | p (two-sided) | sig@0.05 |")
        lines.append("| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | :---: |")
        for t in a["paired_tests"]:
            sig = "yes" if t["p_value"] < 0.05 else "no"
            lines.append(
                "| {route} | {n} | {outcome} | {pairs} | {b} | {c} | {d} | {p:.4f} | {sig} |".format(
                    route=t["route_mode"], n=t["other_passes"], outcome=t["outcome"],
                    pairs=t["n_pairs"], b=t["baseline_to_other_0to1"],
                    c=t["baseline_to_other_1to0"], d=t["discordant"],
                    p=t["p_value"], sig=sig,
                )
            )
        lines.append("")
        lines.append("> Interpretation guardrail: with n=15-45 items the discordant "
                     "counts are tiny, so most paired tests will be underpowered "
                     "(p high) even where point estimates move. A non-significant "
                     "result here means *not yet resolvable at this sample size*, "
                     "not *no effect*. This is exactly the gap the multi-seed / "
                     "larger-N live sweep is meant to close.")
        lines.append("")
    return "\n".join(lines) + "\n"


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="E1 bootstrap CI + paired significance over judge artifacts.")
    p.add_argument("--judge-report", action="append", default=None,
                   help="Path to a *_judge_*net.json report (repeatable). "
                        "Defaults to the two headline HaluMem families.")
    p.add_argument("--bootstrap", type=int, default=10000)
    p.add_argument("--rng-seed", type=int, default=12345)
    p.add_argument("--output-dir", type=str, default=str(DEFAULT_OUTPUT_DIR))
    p.add_argument("--report-id", type=str, default=None)
    return p


def main() -> int:
    args = _build_parser().parse_args()
    if args.judge_report:
        report_paths = [Path(r).expanduser() for r in args.judge_report]
    else:
        report_paths = [JUDGE_DIR / name for name in DEFAULT_JUDGE_REPORTS]

    analyses: list[dict[str, Any]] = []
    for rp in report_paths:
        if not rp.exists():
            raise FileNotFoundError(f"judge report not found: {rp}")
        report_id, conditions = load_family(rp)
        analyses.append(analyze_family(report_id, conditions, args.bootstrap, args.rng_seed))

    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    report_id = args.report_id or f"e1_hallucination_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    json_path = output_dir / f"{report_id}.json"
    md_path = output_dir / f"{report_id}.md"

    payload = {
        "report_id": report_id,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "bootstrap": args.bootstrap,
        "rng_seed": args.rng_seed,
        "sources": [str(rp) for rp in report_paths],
        "families": analyses,
    }
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(analyses, args.bootstrap, args.rng_seed), encoding="utf-8")
    print(json.dumps({"report_id": report_id, "report_json": str(json_path),
                      "report_md": str(md_path), "families": len(analyses)},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
