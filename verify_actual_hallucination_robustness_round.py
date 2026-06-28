from __future__ import annotations

import json
from pathlib import Path


RESULTS_PATH = "outputs/actual_hallucination_robustness_results.json"
BASELINE_RESULTS_PATH = "outputs/actual_hallucination_persistence_results.json"
VERIFY_PATH = "reviews/verification_round18.md"


def check(label: str, passed: bool, detail: str) -> str:
    status = "PASS" if passed else "FAIL"
    return f"- [{status}] {label}: {detail}"


def false_present_rate(records: list[dict]) -> float:
    total = len(records)
    false_present = [record for record in records if record["raw_escalated"]]
    return round(len(false_present) / max(1, total), 3)


def residual_bad_memory_rate(records: list[dict]) -> float:
    total = len(records)
    residual = [record for record in records if record["residual_bad_memory"]]
    return round(len(residual) / max(1, total), 3)


def tentative_target_claim_rate(records: list[dict]) -> float:
    total = len(records)
    tentative = [record for record in records if record["tentative_target_claim"]]
    return round(len(tentative) / max(1, total), 3)


def subset(records: list[dict], *, intervention: str, architecture: str, n_passes: int, seed: int | None = None) -> list[dict]:
    return [
        record
        for record in records
        if record["intervention"] == intervention
        and record["architecture"] == architecture
        and record["n_passes"] == n_passes
        and (seed is None or record["seed"] == seed)
    ]


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    results = json.loads((base_dir / RESULTS_PATH).read_text(encoding="utf-8"))
    baseline = json.loads((base_dir / BASELINE_RESULTS_PATH).read_text(encoding="utf-8"))

    item_count = results["num_items"]
    seed_count = len(results["seeds"])
    expected_records = item_count * seed_count * len(results["architectures"]) * len(results["n_values"]) * len(results["interventions"])
    actual_records = len(results["records"])

    strong_unified_n4 = results["hallucination_metrics"]["strong_anchor"]["scale_aware_unified"]["4"]
    strong_unified_n8 = results["hallucination_metrics"]["strong_anchor"]["scale_aware_unified"]["8"]
    strong_note_n4 = results["hallucination_metrics"]["strong_anchor"]["scale_aware_note_aware"]["4"]
    strong_note_n8 = results["hallucination_metrics"]["strong_anchor"]["scale_aware_note_aware"]["8"]
    soft_unified_n4 = results["hallucination_metrics"]["soft_anchor"]["scale_aware_unified"]["4"]
    soft_unified_n8 = results["hallucination_metrics"]["soft_anchor"]["scale_aware_unified"]["8"]

    baseline_seed11_unified_n4 = baseline["hallucination_metrics"]["scale_aware_unified"]["4"]
    strong_seed11_unified_n4_records = subset(results["records"], intervention="strong_anchor", architecture="scale_aware_unified", n_passes=4, seed=11)
    strong_seed11_unified_n8_records = subset(results["records"], intervention="strong_anchor", architecture="scale_aware_unified", n_passes=8, seed=11)
    strong_seed11_note_n8_records = subset(results["records"], intervention="strong_anchor", architecture="scale_aware_note_aware", n_passes=8, seed=11)

    per_seed_n4_ok = []
    per_seed_n8_ok = []
    for seed in results["seeds"]:
        unified_n4 = false_present_rate(subset(results["records"], intervention="strong_anchor", architecture="scale_aware_unified", n_passes=4, seed=seed))
        note_n4 = false_present_rate(subset(results["records"], intervention="strong_anchor", architecture="scale_aware_note_aware", n_passes=4, seed=seed))
        unified_n8 = false_present_rate(subset(results["records"], intervention="strong_anchor", architecture="scale_aware_unified", n_passes=8, seed=seed))
        note_n8 = false_present_rate(subset(results["records"], intervention="strong_anchor", architecture="scale_aware_note_aware", n_passes=8, seed=seed))
        per_seed_n4_ok.append(note_n4 <= unified_n4)
        per_seed_n8_ok.append(note_n8 <= unified_n8)

    lines = [
        "# Verification Round 18",
        "",
        "这个文件是对 actual hallucination robustness round 的机械核对，不引入新的主张。",
        "",
        check(
            "Record count",
            actual_records == expected_records,
            f"expected `{expected_records}`, observed `{actual_records}`.",
        ),
        check(
            "Strong-anchor seed11 keeps at least as much unified N=4 tentative-clue persistence as the old persistence round",
            tentative_target_claim_rate(strong_seed11_unified_n4_records) >= baseline_seed11_unified_n4["tentative_target_claim_rate"],
            f"old/new seed11 unified N=4 tentative_target_claim = `{baseline_seed11_unified_n4['tentative_target_claim_rate']:.3f}`/`{tentative_target_claim_rate(strong_seed11_unified_n4_records):.3f}`.",
        ),
        check(
            "Strong-anchor aggregate note-aware false-present stays below unified at N=4",
            strong_note_n4["false_present_rate"] < strong_unified_n4["false_present_rate"],
            f"strong unified/note-aware N=4 false_present = `{strong_unified_n4['false_present_rate']:.3f}`/`{strong_note_n4['false_present_rate']:.3f}`.",
        ),
        check(
            "Strong-anchor aggregate note-aware false-present is no worse than unified at N=8",
            strong_note_n8["false_present_rate"] <= strong_unified_n8["false_present_rate"],
            f"strong unified/note-aware N=8 false_present = `{strong_unified_n8['false_present_rate']:.3f}`/`{strong_note_n8['false_present_rate']:.3f}`.",
        ),
        check(
            "Strong-anchor detector gain appears on at least one high-N setting",
            strong_note_n4["false_present_rate"] < strong_unified_n4["false_present_rate"] or strong_note_n8["false_present_rate"] < strong_unified_n8["false_present_rate"],
            f"N=4 unified/note-aware false_present = `{strong_unified_n4['false_present_rate']:.3f}`/`{strong_note_n4['false_present_rate']:.3f}`, N=8 = `{strong_unified_n8['false_present_rate']:.3f}`/`{strong_note_n8['false_present_rate']:.3f}`.",
        ),
        check(
            "Strong anchor preserves more high-N tentative clues than soft anchor",
            strong_unified_n8["tentative_target_claim_rate"] > soft_unified_n8["tentative_target_claim_rate"] or strong_unified_n4["tentative_target_claim_rate"] > soft_unified_n4["tentative_target_claim_rate"],
            f"strong/soft unified tentative_target_claim at N=4 = `{strong_unified_n4['tentative_target_claim_rate']:.3f}`/`{soft_unified_n4['tentative_target_claim_rate']:.3f}`, at N=8 = `{strong_unified_n8['tentative_target_claim_rate']:.3f}`/`{soft_unified_n8['tentative_target_claim_rate']:.3f}`.",
        ),
        check(
            "Strong-anchor note-aware keeps zero residual contamination at N=8",
            residual_bad_memory_rate(strong_seed11_note_n8_records) == 0.0 and results["aggregate"]["strong_anchor"]["scale_aware_note_aware"]["8"]["residual_bad_memory_rate"] == 0.0,
            f"seed11/all-seed strong note-aware N=8 residual = `{residual_bad_memory_rate(strong_seed11_note_n8_records):.3f}`/`{results['aggregate']['strong_anchor']['scale_aware_note_aware']['8']['residual_bad_memory_rate']:.3f}`.",
        ),
        check(
            "Strong-anchor note-aware does not lose the false-present edge on any seed",
            all(per_seed_n4_ok) and all(per_seed_n8_ok),
            f"per-seed strong note-aware<=unified at N=4 `{per_seed_n4_ok}`, at N=8 `{per_seed_n8_ok}`.",
        ),
        "",
        "## Bottom Line",
        "",
        "如果这些检查通过，说明 round 19 不只是重复 round 18，而是把 actual hallucination persistence 推进成了一个更像 robustness subsection 的结果：强 contract 的 detector gain 在多 seed 下依然成立，而 softer contract 会让 clue survival 变弱。",
    ]

    (base_dir / VERIFY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / VERIFY_PATH}")


if __name__ == "__main__":
    main()
