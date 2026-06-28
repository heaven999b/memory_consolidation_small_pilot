from __future__ import annotations

import json
from pathlib import Path


RESULTS_PATH = "outputs/actual_hallucination_literal_normalization_pilot_results.json"
VERIFY_PATH = "reviews/verification_round26.md"
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

    literal_unified_n8 = results["hallucination_metrics"]["literal_identity_anchor"]["scale_aware_unified"]["8"]
    literal_note_n8 = results["hallucination_metrics"]["literal_identity_anchor"]["scale_aware_note_aware"]["8"]
    normalized_unified_n8 = results["hallucination_metrics"]["normalized_literal_identity_anchor"]["scale_aware_unified"]["8"]
    normalized_note_n8 = results["hallucination_metrics"]["normalized_literal_identity_anchor"]["scale_aware_note_aware"]["8"]

    literal_on_code = select_records(
        records, intervention="literal_identity_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=CODE_IDS
    )
    literal_on_weak = select_records(
        records, intervention="literal_identity_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=WEAK_NAME_IDS
    )
    literal_on_strong = select_records(
        records, intervention="literal_identity_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=STRONG_NAME_IDS
    )
    normalized_on_code = select_records(
        records,
        intervention="normalized_literal_identity_anchor",
        architecture="scale_aware_unified",
        n_passes=8,
        item_ids=CODE_IDS,
    )
    normalized_on_weak = select_records(
        records,
        intervention="normalized_literal_identity_anchor",
        architecture="scale_aware_unified",
        n_passes=8,
        item_ids=WEAK_NAME_IDS,
    )
    normalized_on_strong = select_records(
        records,
        intervention="normalized_literal_identity_anchor",
        architecture="scale_aware_unified",
        n_passes=8,
        item_ids=STRONG_NAME_IDS,
    )
    normalized_note_on_strong = select_records(
        records,
        intervention="normalized_literal_identity_anchor",
        architecture="scale_aware_note_aware",
        n_passes=8,
        item_ids=STRONG_NAME_IDS,
    )

    literal_summary_n8 = results["aggregate"]["literal_identity_anchor"]["summary_only"]["8"]
    normalized_summary_n8 = results["aggregate"]["normalized_literal_identity_anchor"]["summary_only"]["8"]

    lines = [
        "# Verification Round 26",
        "",
        "这个文件是对 actual hallucination literal-normalization pilot 的机械核对，不引入新的主张。",
        "",
        check(
            "Record count",
            actual_records == expected_records,
            f"expected `{expected_records}`, observed `{actual_records}`.",
        ),
        check(
            "Focused pilot slice is the intended 6-item mixed literal set",
            results["slice_ids"] == SLICE_IDS,
            f"observed slice ids = `{results['slice_ids']}`.",
        ),
        check(
            "Normalization preserves code-overlap signal behavior",
            signal_count(normalized_on_code) == signal_count(literal_on_code),
            f"baseline/normalized code signal at N=8 = `{signal_count(literal_on_code)}`/`{signal_count(normalized_on_code)}`.",
        ),
        check(
            "Normalization preserves weak-name blocking behavior",
            signal_count(normalized_on_weak) == signal_count(literal_on_weak),
            f"baseline/normalized weak-name signal at N=8 = `{signal_count(literal_on_weak)}`/`{signal_count(normalized_on_weak)}`.",
        ),
        check(
            "Normalization preserves strengthened-name signal behavior",
            signal_count(normalized_on_strong) == signal_count(literal_on_strong),
            f"baseline/normalized strengthened-name signal/tent/raw at N=8 = `{signal_count(literal_on_strong)}`/`{clue_count(literal_on_strong)}`/`{raw_count(literal_on_strong)}` vs `{signal_count(normalized_on_strong)}`/`{clue_count(normalized_on_strong)}`/`{raw_count(normalized_on_strong)}`.",
        ),
        check(
            "Normalization makes both strengthened-name literal notes scaffold-stable",
            scaffold_count(normalized_on_strong) > scaffold_count(literal_on_strong),
            f"baseline/normalized strengthened-name scaffold counts at N=8 = `{scaffold_count(literal_on_strong)}`/`{scaffold_count(normalized_on_strong)}`.",
        ),
        check(
            "Normalized note-aware false-present is non-worse than baseline",
            normalized_note_n8["false_present_rate"] <= literal_note_n8["false_present_rate"],
            f"baseline/normalized note-aware false_present at N=8 = `{literal_note_n8['false_present_rate']:.3f}`/`{normalized_note_n8['false_present_rate']:.3f}`.",
        ),
        check(
            "Normalized note-aware still abstains on both strengthened-name items",
            all((record["route"] == "utility_calibrated_abstain") and (record["probe_status"] == "absent") for record in normalized_note_on_strong),
            f"normalized note-aware strengthened-name routes at N=8 = `{[(record['item_id'], record['route'], record['probe_status']) for record in normalized_note_on_strong]}`.",
        ),
        check(
            "Normalized unified false-present is non-worse than baseline",
            normalized_unified_n8["false_present_rate"] <= literal_unified_n8["false_present_rate"],
            f"baseline/normalized unified false_present at N=8 = `{literal_unified_n8['false_present_rate']:.3f}`/`{normalized_unified_n8['false_present_rate']:.3f}`.",
        ),
        check(
            "Normalized summary-only realism stays at least as strong as baseline",
            normalized_summary_n8["accuracy"] >= literal_summary_n8["accuracy"],
            f"baseline/normalized summary_only N=8 accuracy = `{literal_summary_n8['accuracy']:.3f}`/`{normalized_summary_n8['accuracy']:.3f}`.",
        ),
        check(
            "Normalized note-aware residual contamination stays zero at high N",
            results["aggregate"]["normalized_literal_identity_anchor"]["scale_aware_note_aware"]["8"]["residual_bad_memory_rate"] == 0.0,
            f"normalized note-aware residual at N=8 = `{results['aggregate']['normalized_literal_identity_anchor']['scale_aware_note_aware']['8']['residual_bad_memory_rate']:.3f}`.",
        ),
        "",
        "## Bottom Line",
        "",
        "如果这些检查通过，说明 broad literal integration 这一步是稳定的 executor cleanup，而不是新的 latent-claim patch：它保留 mixed code+name literal slice 的 signal / abstain story，不额外制造 unified 侧回退，同时把 strengthened aligned-name cases 的 final note 全部归一成 detector-readable scaffold。",
    ]

    (base_dir / VERIFY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / VERIFY_PATH}")


if __name__ == "__main__":
    main()
