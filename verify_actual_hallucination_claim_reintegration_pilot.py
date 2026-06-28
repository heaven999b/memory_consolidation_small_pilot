from __future__ import annotations

import json
from pathlib import Path


RESULTS_PATH = "outputs/actual_hallucination_claim_reintegration_pilot_results.json"
VERIFY_PATH = "reviews/verification_round29.md"
SLICE_IDS = [
    "halu_01",
    "halu_02",
    "halu_03",
    "halu_04",
    "halu_05",
    "halu_08",
    "halu_12",
    "halu_14",
    "halu_15",
    "halu_16",
    "halu_17",
    "halu_18",
    "halu_19",
    "halu_20",
]
RELATION_IDS = {"halu_01", "halu_12"}
STRESS_CONTEXT_IDS = {"halu_02", "halu_03", "halu_04", "halu_05", "halu_08", "halu_14"}
CODE_IDS = {"halu_15", "halu_16"}
WEAK_NAME_IDS = {"halu_17", "halu_18"}
STRONG_NAME_IDS = {"halu_19", "halu_20"}
PROXY_TYPED_EQ_IDS = {"halu_02", "halu_04", "halu_05", "halu_08", "halu_14"}
PROXY_IDENTITY_EQ_IDS = {"halu_03"}
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

    proxy_records = [record for record in records if record["proxy_status"] != "exact"]
    typed_proxy_records = [record for record in proxy_records if record["item_id"] in PROXY_TYPED_EQ_IDS]
    identity_proxy_records = [record for record in proxy_records if record["item_id"] in PROXY_IDENTITY_EQ_IDS]

    literal_unified_n8 = results["hallucination_metrics"]["literal_identity_anchor"]["scale_aware_unified"]["8"]
    normalized_unified_n8 = results["hallucination_metrics"]["normalized_literal_identity_anchor"]["scale_aware_unified"]["8"]
    claim_unified_n8 = results["hallucination_metrics"]["claim_normalized_literal_identity_anchor"]["scale_aware_unified"]["8"]
    normalized_note_n8 = results["hallucination_metrics"]["normalized_literal_identity_anchor"]["scale_aware_note_aware"]["8"]
    claim_note_n8 = results["hallucination_metrics"]["claim_normalized_literal_identity_anchor"]["scale_aware_note_aware"]["8"]

    literal_on_relation = select_records(records, intervention="literal_identity_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=RELATION_IDS)
    claim_on_relation = select_records(records, intervention="claim_normalized_literal_identity_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=RELATION_IDS)
    literal_on_context = select_records(records, intervention="literal_identity_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=STRESS_CONTEXT_IDS)
    claim_on_context = select_records(records, intervention="claim_normalized_literal_identity_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=STRESS_CONTEXT_IDS)
    literal_on_code = select_records(records, intervention="literal_identity_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=CODE_IDS)
    claim_on_code = select_records(records, intervention="claim_normalized_literal_identity_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=CODE_IDS)
    literal_on_weak = select_records(records, intervention="literal_identity_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=WEAK_NAME_IDS)
    claim_on_weak = select_records(records, intervention="claim_normalized_literal_identity_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=WEAK_NAME_IDS)
    normalized_on_strong = select_records(records, intervention="normalized_literal_identity_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=STRONG_NAME_IDS)
    claim_on_strong = select_records(records, intervention="claim_normalized_literal_identity_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=STRONG_NAME_IDS)
    claim_note_on_strong = select_records(records, intervention="claim_normalized_literal_identity_anchor", architecture="scale_aware_note_aware", n_passes=8, item_ids=STRONG_NAME_IDS)

    normalized_summary_n8 = results["aggregate"]["normalized_literal_identity_anchor"]["summary_only"]["8"]
    claim_summary_n8 = results["aggregate"]["claim_normalized_literal_identity_anchor"]["summary_only"]["8"]

    lines = [
        "# Verification Round 29",
        "",
        "这个文件是对 actual hallucination claim-reintegration proxy pilot 的机械核对，不引入新的主张。",
        "",
        check(
            "Record count",
            actual_records == expected_records,
            f"expected `{expected_records}`, observed `{actual_records}`.",
        ),
        check(
            "Reintegration slice is the intended 14-item stress-plus-literal set",
            results["slice_ids"] == SLICE_IDS,
            f"observed slice ids = `{results['slice_ids']}`.",
        ),
        check(
            "Artifact is explicitly marked as a proxy-expanded stitch",
            results.get("mode") == "proxy_expanded_stitch",
            f"observed mode = `{results.get('mode')}`.",
        ),
        check(
            "Proxy rows are restricted to the intended non-literal stress items",
            len(proxy_records) == 108 and {record['item_id'] for record in proxy_records} == (PROXY_TYPED_EQ_IDS | PROXY_IDENTITY_EQ_IDS),
            f"observed proxy rows = `{len(proxy_records)}`, proxy items = `{sorted({record['item_id'] for record in proxy_records})}`.",
        ),
        check(
            "Typed-equivalent proxy coverage matches the five must-copy or weak/policy items",
            len(typed_proxy_records) == 90 and all(record["source_intervention"] == "typed_selective_anchor" for record in typed_proxy_records),
            f"typed-equivalent proxy rows = `{len(typed_proxy_records)}`.",
        ),
        check(
            "Identity-equivalent proxy coverage matches the single preference-context item",
            len(identity_proxy_records) == 18 and all(record["source_intervention"] == "identity_selective_anchor" for record in identity_proxy_records),
            f"identity-equivalent proxy rows = `{len(identity_proxy_records)}`.",
        ),
        check(
            "Claim-sensitive literal branch still blocks relation-style items",
            signal_count(claim_on_relation) == signal_count(literal_on_relation) == 0,
            f"literal/claim relation signal at N=8 = `{signal_count(literal_on_relation)}`/`{signal_count(claim_on_relation)}`.",
        ),
        check(
            "Claim-sensitive literal branch preserves wider stress-context behavior under proxy expansion",
            signal_count(claim_on_context) == signal_count(literal_on_context),
            f"literal/claim stress-context signal at N=8 = `{signal_count(literal_on_context)}`/`{signal_count(claim_on_context)}`.",
        ),
        check(
            "Claim-sensitive literal branch preserves code-overlap behavior",
            signal_count(claim_on_code) == signal_count(literal_on_code),
            f"literal/claim code signal at N=8 = `{signal_count(literal_on_code)}`/`{signal_count(claim_on_code)}`.",
        ),
        check(
            "Claim-sensitive literal branch preserves weak-name blocking",
            signal_count(claim_on_weak) == signal_count(literal_on_weak),
            f"literal/claim weak-name signal at N=8 = `{signal_count(literal_on_weak)}`/`{signal_count(claim_on_weak)}`.",
        ),
        check(
            "Claim-sensitive literal branch surfaces strengthened-name tentative query claims",
            clue_count(claim_on_strong) > clue_count(normalized_on_strong),
            f"normalized/claim strengthened-name signal/tent/raw at N=8 = `{signal_count(normalized_on_strong)}`/`{clue_count(normalized_on_strong)}`/`{raw_count(normalized_on_strong)}` vs `{signal_count(claim_on_strong)}`/`{clue_count(claim_on_strong)}`/`{raw_count(claim_on_strong)}`.",
        ),
        check(
            "Claim-sensitive literal branch keeps strengthened-name notes scaffold-stable",
            scaffold_count(claim_on_strong) == len(claim_on_strong),
            f"claim strengthened-name scaffold count at N=8 = `{scaffold_count(claim_on_strong)}`.",
        ),
        check(
            "Claim-sensitive unified false-present is non-worse than normalized literal baseline",
            claim_unified_n8["false_present_rate"] <= normalized_unified_n8["false_present_rate"],
            f"normalized/claim unified false_present at N=8 = `{normalized_unified_n8['false_present_rate']:.3f}`/`{claim_unified_n8['false_present_rate']:.3f}`.",
        ),
        check(
            "Claim-sensitive note-aware false-present is non-worse than normalized literal baseline",
            claim_note_n8["false_present_rate"] <= normalized_note_n8["false_present_rate"],
            f"normalized/claim note-aware false_present at N=8 = `{normalized_note_n8['false_present_rate']:.3f}`/`{claim_note_n8['false_present_rate']:.3f}`.",
        ),
        check(
            "Claim-sensitive note-aware still abstains on both strengthened-name items",
            all((record["route"] == "utility_calibrated_abstain") and (record["probe_status"] == "absent") for record in claim_note_on_strong),
            f"claim note-aware strengthened-name routes at N=8 = `{[(record['item_id'], record['route'], record['probe_status']) for record in claim_note_on_strong]}`.",
        ),
        check(
            "Claim-sensitive summary-only realism stays at least as strong as normalized literal baseline",
            claim_summary_n8["accuracy"] >= normalized_summary_n8["accuracy"],
            f"normalized/claim summary_only N=8 accuracy = `{normalized_summary_n8['accuracy']:.3f}`/`{claim_summary_n8['accuracy']:.3f}`.",
        ),
        check(
            "Claim-sensitive note-aware residual contamination stays zero at high N",
            results["aggregate"]["claim_normalized_literal_identity_anchor"]["scale_aware_note_aware"]["8"]["residual_bad_memory_rate"] == 0.0,
            f"claim note-aware residual at N=8 = `{results['aggregate']['claim_normalized_literal_identity_anchor']['scale_aware_note_aware']['8']['residual_bad_memory_rate']:.3f}`.",
        ),
        "",
        "## Bottom Line",
        "",
        "如果这些检查通过，说明这次 proxy-expanded reintegration 至少没有暴露出更宽 mixed slice 上的立即回退。它不能替代未来的 exact literal-identity live rerun，但已经足够把 claim-sensitive broad literal branch 从 8-item bridge 再往外推一层，同时把 proxy 假设本身写清楚并机械锁住。",
    ]

    (base_dir / VERIFY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / VERIFY_PATH}")


if __name__ == "__main__":
    main()
