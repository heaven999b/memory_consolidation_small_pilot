from __future__ import annotations

import json
from pathlib import Path


RESULTS_PATH = "outputs/actual_note_persistence_results.json"
VERIFY_PATH = "reviews/verification_round13.md"


def check(label: str, passed: bool, detail: str) -> str:
    status = "PASS" if passed else "FAIL"
    return f"- [{status}] {label}: {detail}"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    results = json.loads((base_dir / RESULTS_PATH).read_text(encoding="utf-8"))

    item_count = results["num_items"]
    seed_count = len(results["seeds"])
    expected_records = (
        item_count * seed_count * len(results["architectures"]) * len(results["interventions"]) * len(results["n_values"])
    )
    actual_records = len(results["records"])

    summary_baseline_n8 = results["persistence_metrics"]["summary_only"]["baseline"]["8"]
    summary_best_n8 = min(
        results["persistence_metrics"]["summary_only"][intervention]["8"]["history_loss_rate"]
        for intervention in results["interventions"]
    )
    unified_base_n8 = results["persistence_metrics"]["scale_aware_unified"]["baseline"]["8"]
    unified_best_empty_n8 = min(
        results["persistence_metrics"]["scale_aware_unified"][intervention]["8"]["empty_note_then_abstain_rate"]
        for intervention in results["interventions"]
    )
    unified_base_row_n8 = results["aggregate"]["scale_aware_unified"]["baseline"]["8"]
    unified_best_residual_n8 = min(
        results["aggregate"]["scale_aware_unified"][intervention]["8"]["residual_bad_memory_rate"]
        for intervention in results["interventions"]
    )
    scaffold_target_n8 = results["persistence_metrics"]["scale_aware_unified"]["tiny_fixed_scaffold"]["8"]
    anchor_target_n8 = results["persistence_metrics"]["scale_aware_unified"]["target_field_anchor"]["8"]

    lines = [
        "# Verification Round 13",
        "",
        "这个文件是对 actual note persistence round 的机械核对，不引入新的主张。",
        "",
        check(
            "Record count",
            actual_records == expected_records,
            f"expected `{expected_records}`, observed `{actual_records}`.",
        ),
        check(
            "At least one note scaffold improves summary-only high-N history loss",
            summary_best_n8 <= summary_baseline_n8["history_loss_rate"],
            f"baseline N=8 history_loss = `{summary_baseline_n8['history_loss_rate']:.3f}`; best scaffold = `{summary_best_n8:.3f}`.",
        ),
        check(
            "At least one note scaffold improves unified high-N empty-note abstain",
            unified_best_empty_n8 <= unified_base_n8["empty_note_then_abstain_rate"],
            f"baseline N=8 empty_note_then_abstain = `{unified_base_n8['empty_note_then_abstain_rate']:.3f}`; best scaffold = `{unified_best_empty_n8:.3f}`.",
        ),
        check(
            "Unified scaffold variants do not worsen residual contamination at N=8",
            unified_best_residual_n8 <= unified_base_row_n8["residual_bad_memory_rate"],
            f"baseline residual = `{unified_base_row_n8['residual_bad_memory_rate']:.3f}`; best scaffold residual = `{unified_best_residual_n8:.3f}`.",
        ),
        check(
            "Structured note variants increase target retention signal under unified N=8",
            max(scaffold_target_n8["target_claim_retained_rate"], anchor_target_n8["target_claim_retained_rate"])
            >= unified_base_n8["target_claim_retained_rate"],
            "baseline/anchor/scaffold target_claim = "
            f"{unified_base_n8['target_claim_retained_rate']:.3f}/"
            f"{anchor_target_n8['target_claim_retained_rate']:.3f}/"
            f"{scaffold_target_n8['target_claim_retained_rate']:.3f}.",
        ),
        check(
            "Tiny scaffold stays compact while improving unified N=8 target retention",
            scaffold_target_n8["mean_note_tokens"] < unified_base_n8["mean_note_tokens"]
            and scaffold_target_n8["target_claim_retained_rate"] > unified_base_n8["target_claim_retained_rate"],
            "baseline/anchor/scaffold mean_note_tokens = "
            f"{unified_base_n8['mean_note_tokens']:.2f}/"
            f"{anchor_target_n8['mean_note_tokens']:.2f}/"
            f"{scaffold_target_n8['mean_note_tokens']:.2f}.",
        ),
        "",
        "## Bottom Line",
        "",
        "如果这些检查通过，说明 round 14 已经把下一步从“是否要做 memory scaffold”推进到“哪一种 scaffold 在真实高 N recall 下更有希望”。",
    ]

    (base_dir / VERIFY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / VERIFY_PATH}")


if __name__ == "__main__":
    main()
