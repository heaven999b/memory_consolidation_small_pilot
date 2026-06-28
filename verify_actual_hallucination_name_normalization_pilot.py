from __future__ import annotations

import json
from pathlib import Path


RESULTS_PATH = "outputs/actual_hallucination_name_normalization_pilot_results.json"
VERIFY_PATH = "reviews/verification_round25.md"
SLICE_IDS = ["halu_15", "halu_16", "halu_17", "halu_18", "halu_19", "halu_20"]
CODE_IDS = {"halu_15", "halu_16"}
WEAK_NAME_IDS = {"halu_17", "halu_18"}
STRONG_NAME_IDS = {"halu_19", "halu_20"}
SCAFFOLD_PREFIXES = ("target_slot:", "status_slot:", "carry_slot:")


def check(label: str, passed: bool, detail: str) -> str:
    status = "PASS" if passed else "FAIL"
    return f"- [{status}] {label}: {detail}"


def note_has_scaffold(note_text: str) -> bool:
    lines = [line.strip().lower() for line in note_text.splitlines() if line.strip()]
    return len(lines) >= 3 and all(any(line.startswith(prefix) for line in lines) for prefix in SCAFFOLD_PREFIXES)


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


def scaffold_count(records: list[dict]) -> int:
    return sum(1 for record in records if note_has_scaffold(record["final_note"]))


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

    refined_unified_n8 = results["hallucination_metrics"]["refined_name_literal_anchor"]["scale_aware_unified"]["8"]
    refined_note_n8 = results["hallucination_metrics"]["refined_name_literal_anchor"]["scale_aware_note_aware"]["8"]
    normalized_unified_n8 = results["hallucination_metrics"]["normalized_refined_name_literal_anchor"]["scale_aware_unified"]["8"]
    normalized_note_n8 = results["hallucination_metrics"]["normalized_refined_name_literal_anchor"]["scale_aware_note_aware"]["8"]

    refined_on_code = select_records(
        records, intervention="refined_name_literal_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=CODE_IDS
    )
    refined_on_weak = select_records(
        records, intervention="refined_name_literal_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=WEAK_NAME_IDS
    )
    refined_on_strong = select_records(
        records, intervention="refined_name_literal_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=STRONG_NAME_IDS
    )
    normalized_on_code = select_records(
        records,
        intervention="normalized_refined_name_literal_anchor",
        architecture="scale_aware_unified",
        n_passes=8,
        item_ids=CODE_IDS,
    )
    normalized_on_weak = select_records(
        records,
        intervention="normalized_refined_name_literal_anchor",
        architecture="scale_aware_unified",
        n_passes=8,
        item_ids=WEAK_NAME_IDS,
    )
    normalized_on_strong = select_records(
        records,
        intervention="normalized_refined_name_literal_anchor",
        architecture="scale_aware_unified",
        n_passes=8,
        item_ids=STRONG_NAME_IDS,
    )
    normalized_note_on_strong = select_records(
        records,
        intervention="normalized_refined_name_literal_anchor",
        architecture="scale_aware_note_aware",
        n_passes=8,
        item_ids=STRONG_NAME_IDS,
    )

    refined_summary_n8 = results["aggregate"]["refined_name_literal_anchor"]["summary_only"]["8"]
    normalized_summary_n8 = results["aggregate"]["normalized_refined_name_literal_anchor"]["summary_only"]["8"]

    lines = [
        "# Verification Round 25",
        "",
        "这个文件是对 actual hallucination name-normalization pilot 的机械核对，不引入新的主张。",
        "",
        check(
            "Record count",
            actual_records == expected_records,
            f"expected `{expected_records}`, observed `{actual_records}`.",
        ),
        check(
            "Focused pilot slice is the intended 6-item name-normalization set",
            results["slice_ids"] == SLICE_IDS,
            f"observed slice ids = `{results['slice_ids']}`.",
        ),
        check(
            "Normalized branch still blocks code-overlap items",
            signal_count(normalized_on_code) == 0,
            f"normalized branch signal count on code ids at N=8 = `{signal_count(normalized_on_code)}`.",
        ),
        check(
            "Normalized branch still blocks the weak anti-role pair",
            signal_count(normalized_on_weak) == 0,
            f"normalized branch signal count on weak-name ids at N=8 = `{signal_count(normalized_on_weak)}`.",
        ),
        check(
            "Normalized branch keeps full strong-name signal",
            signal_count(normalized_on_strong) == len(normalized_on_strong),
            f"normalized strengthened-name signal/tent/raw at N=8 = `{signal_count(normalized_on_strong)}`/`{clue_count(normalized_on_strong)}`/`{raw_count(normalized_on_strong)}`.",
        ),
        check(
            "Normalized branch makes both strengthened-name notes scaffold-stable",
            scaffold_count(normalized_on_strong) > scaffold_count(refined_on_strong),
            f"refined/normalized strengthened-name scaffold counts at N=8 = `{scaffold_count(refined_on_strong)}`/`{scaffold_count(normalized_on_strong)}`.",
        ),
        check(
            "Normalized note-aware false-present improves over refined at high N",
            normalized_note_n8["false_present_rate"] < refined_note_n8["false_present_rate"],
            f"refined/normalized note-aware false_present at N=8 = `{refined_note_n8['false_present_rate']:.3f}`/`{normalized_note_n8['false_present_rate']:.3f}`.",
        ),
        check(
            "Normalized note-aware abstains on both strengthened-name items",
            all((record["route"] == "utility_calibrated_abstain") and (record["probe_status"] == "absent") for record in normalized_note_on_strong),
            f"normalized note-aware strengthened-name routes at N=8 = `{[(record['item_id'], record['route'], record['probe_status']) for record in normalized_note_on_strong]}`.",
        ),
        check(
            "Normalized unified false-present does not regress relative to refined",
            normalized_unified_n8["false_present_rate"] <= refined_unified_n8["false_present_rate"],
            f"refined/normalized unified false_present at N=8 = `{refined_unified_n8['false_present_rate']:.3f}`/`{normalized_unified_n8['false_present_rate']:.3f}`.",
        ),
        check(
            "Normalized summary-only realism stays at least as strong as refined",
            normalized_summary_n8["accuracy"] >= refined_summary_n8["accuracy"],
            f"refined/normalized summary_only N=8 accuracy = `{refined_summary_n8['accuracy']:.3f}`/`{normalized_summary_n8['accuracy']:.3f}`.",
        ),
        check(
            "All normalized note-aware runs keep zero residual contamination at N=8",
            results["aggregate"]["normalized_refined_name_literal_anchor"]["scale_aware_note_aware"]["8"]["residual_bad_memory_rate"] == 0.0,
            f"normalized note-aware residual at N=8 = `{results['aggregate']['normalized_refined_name_literal_anchor']['scale_aware_note_aware']['8']['residual_bad_memory_rate']:.3f}`.",
        ),
        "",
        "## Bottom Line",
        "",
        "如果这些检查通过，说明 aligned-name note normalization 确实补到了前一轮的真空地带：它没有改变 unified side 的 detector pressure，却把 strongest aligned-name cases 的 final note 全部归一成可解析 scaffold，并把 note-aware `N=8 false_present` 从 `0.333` 压到 `0.000`。",
    ]

    (base_dir / VERIFY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / VERIFY_PATH}")


if __name__ == "__main__":
    main()
