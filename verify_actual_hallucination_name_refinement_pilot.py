from __future__ import annotations

import json
from pathlib import Path


RESULTS_PATH = "outputs/actual_hallucination_name_refinement_pilot_results.json"
VERIFY_PATH = "reviews/verification_round24.md"
SLICE_IDS = ["halu_15", "halu_16", "halu_17", "halu_18", "halu_19", "halu_20"]
CODE_IDS = {"halu_15", "halu_16"}
WEAK_NAME_IDS = {"halu_17", "halu_18"}
STRONG_NAME_IDS = {"halu_19", "halu_20"}


def check(label: str, passed: bool, detail: str) -> str:
    status = "PASS" if passed else "FAIL"
    return f"- [{status}] {label}: {detail}"


def select_records(
    records: list[dict],
    *,
    intervention: str,
    architecture: str,
    n_passes: int,
    item_ids: set[str] | None = None,
) -> list[dict]:
    return [
        record
        for record in records
        if record["intervention"] == intervention
        and record["architecture"] == architecture
        and record["n_passes"] == n_passes
        and (item_ids is None or record["item_id"] in item_ids)
    ]


def clue_count(records: list[dict]) -> int:
    return sum(1 for record in records if record["tentative_target_claim"])


def raw_count(records: list[dict]) -> int:
    return sum(1 for record in records if record["raw_escalated"])


def signal_count(records: list[dict]) -> int:
    return sum(1 for record in records if record["tentative_target_claim"] or record["raw_escalated"])


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    results = json.loads((base_dir / RESULTS_PATH).read_text(encoding="utf-8"))
    records = results["records"]

    expected_records = (
        results["num_items"]
        * len(results["seeds"])
        * len(results["architectures"])
        * len(results["n_values"])
        * len(results["interventions"])
    )
    actual_records = len(records)

    baseline_unified_n8 = results["hallucination_metrics"]["name_literal_anchor"]["scale_aware_unified"]["8"]
    baseline_note_n8 = results["hallucination_metrics"]["name_literal_anchor"]["scale_aware_note_aware"]["8"]
    refined_unified_n8 = results["hallucination_metrics"]["refined_name_literal_anchor"]["scale_aware_unified"]["8"]
    refined_note_n8 = results["hallucination_metrics"]["refined_name_literal_anchor"]["scale_aware_note_aware"]["8"]

    baseline_on_code = select_records(
        records, intervention="name_literal_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=CODE_IDS
    )
    baseline_on_weak = select_records(
        records, intervention="name_literal_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=WEAK_NAME_IDS
    )
    baseline_on_strong = select_records(
        records, intervention="name_literal_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=STRONG_NAME_IDS
    )
    refined_on_code = select_records(
        records, intervention="refined_name_literal_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=CODE_IDS
    )
    refined_on_weak = select_records(
        records, intervention="refined_name_literal_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=WEAK_NAME_IDS
    )
    refined_on_strong = select_records(
        records, intervention="refined_name_literal_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=STRONG_NAME_IDS
    )

    baseline_summary_n8 = results["aggregate"]["name_literal_anchor"]["summary_only"]["8"]
    refined_summary_n8 = results["aggregate"]["refined_name_literal_anchor"]["summary_only"]["8"]

    lines = [
        "# Verification Round 24",
        "",
        "这个文件是对 actual hallucination name-refinement pilot 的机械核对，不引入新的主张。",
        "",
        check(
            "Record count",
            actual_records == expected_records,
            f"expected `{expected_records}`, observed `{actual_records}`.",
        ),
        check(
            "Focused pilot slice is the intended 6-item name-refinement set",
            results["slice_ids"] == SLICE_IDS,
            f"observed slice ids = `{results['slice_ids']}`.",
        ),
        check(
            "Refined name branch still blocks code-overlap items",
            signal_count(refined_on_code) == 0,
            f"refined name branch signal count on code ids at N=8 = `{signal_count(refined_on_code)}`.",
        ),
        check(
            "Refined name branch fully removes detector-visible work from the weak anti-role pair",
            signal_count(refined_on_weak) == 0,
            f"refined name branch signal count on weak-name ids at N=8 = `{signal_count(refined_on_weak)}`.",
        ),
        check(
            "Refined name branch keeps detector-visible work on both strengthened aligned-name items",
            signal_count(refined_on_strong) == len(refined_on_strong),
            f"refined name branch strengthened-name signal/tent/raw at N=8 = `{signal_count(refined_on_strong)}`/`{clue_count(refined_on_strong)}`/`{raw_count(refined_on_strong)}`.",
        ),
        check(
            "Refined name branch improves compact-stable clue survival on strengthened-name items",
            clue_count(refined_on_strong) > clue_count(baseline_on_strong),
            f"baseline/refined strengthened-name tentative counts at N=8 = `{clue_count(baseline_on_strong)}`/`{clue_count(refined_on_strong)}`.",
        ),
        check(
            "Refined name branch removes the weak-pair false tentative that remained in the baseline name branch",
            clue_count(refined_on_weak) < clue_count(baseline_on_weak),
            f"baseline/refined weak-name tentative counts at N=8 = `{clue_count(baseline_on_weak)}`/`{clue_count(refined_on_weak)}`.",
        ),
        check(
            "Refined summary-only realism improves over the baseline name-only branch",
            refined_summary_n8["accuracy"] > baseline_summary_n8["accuracy"],
            f"baseline/refined summary_only N=8 accuracy = `{baseline_summary_n8['accuracy']:.3f}`/`{refined_summary_n8['accuracy']:.3f}`.",
        ),
        check(
            "Refined name note-aware branch is non-worse than the baseline at high N",
            refined_note_n8["false_present_rate"] <= baseline_note_n8["false_present_rate"],
            f"baseline/refined note-aware false_present at N=8 = `{baseline_note_n8['false_present_rate']:.3f}`/`{refined_note_n8['false_present_rate']:.3f}`.",
        ),
        check(
            "Refined name unified false-present does not regress relative to the baseline",
            refined_unified_n8["false_present_rate"] <= baseline_unified_n8["false_present_rate"],
            f"baseline/refined unified false_present at N=8 = `{baseline_unified_n8['false_present_rate']:.3f}`/`{refined_unified_n8['false_present_rate']:.3f}`.",
        ),
        check(
            "All refined note-aware runs keep zero residual contamination at N=8",
            results["aggregate"]["refined_name_literal_anchor"]["scale_aware_note_aware"]["8"]["residual_bad_memory_rate"] == 0.0,
            f"refined note-aware residual at N=8 = `{results['aggregate']['refined_name_literal_anchor']['scale_aware_note_aware']['8']['residual_bad_memory_rate']:.3f}`.",
        ),
        "",
        "## Bottom Line",
        "",
        "如果这些检查通过，说明 name-only scaffold tightening 的主要收益已经被机械确认：weak anti-role names 被稳定压回 MISSING，strong aligned names 从 recoverable signal 更靠近 compact-stable clue，同时 summary-only realism 变好；但 detector-side false_present 还没有继续下降，所以前沿问题已从 data split 转成 executor / carry-forward consistency。",
    ]

    (base_dir / VERIFY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / VERIFY_PATH}")


if __name__ == "__main__":
    main()
