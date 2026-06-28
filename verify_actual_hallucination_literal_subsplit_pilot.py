from __future__ import annotations

import json
from pathlib import Path


RESULTS_PATH = "outputs/actual_hallucination_literal_subsplit_pilot_results.json"
VERIFY_PATH = "reviews/verification_round23.md"
SLICE_IDS = ["halu_15", "halu_16", "halu_17", "halu_18", "halu_19", "halu_20"]
CODE_IDS = {"halu_15", "halu_16"}
WEAK_NAME_IDS = {"halu_17", "halu_18"}
STRONG_NAME_IDS = {"halu_19", "halu_20"}
NAME_IDS = WEAK_NAME_IDS | STRONG_NAME_IDS


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

    typed_unified_n8 = results["hallucination_metrics"]["typed_selective_anchor"]["scale_aware_unified"]["8"]
    typed_note_n8 = results["hallucination_metrics"]["typed_selective_anchor"]["scale_aware_note_aware"]["8"]
    literal_unified_n8 = results["hallucination_metrics"]["literal_identity_anchor"]["scale_aware_unified"]["8"]
    literal_note_n8 = results["hallucination_metrics"]["literal_identity_anchor"]["scale_aware_note_aware"]["8"]
    code_unified_n8 = results["hallucination_metrics"]["code_literal_anchor"]["scale_aware_unified"]["8"]
    code_note_n8 = results["hallucination_metrics"]["code_literal_anchor"]["scale_aware_note_aware"]["8"]
    name_unified_n8 = results["hallucination_metrics"]["name_literal_anchor"]["scale_aware_unified"]["8"]
    name_note_n8 = results["hallucination_metrics"]["name_literal_anchor"]["scale_aware_note_aware"]["8"]

    literal_on_code = select_records(
        records, intervention="literal_identity_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=CODE_IDS
    )
    literal_on_weak_name = select_records(
        records, intervention="literal_identity_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=WEAK_NAME_IDS
    )
    literal_on_strong_name = select_records(
        records, intervention="literal_identity_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=STRONG_NAME_IDS
    )
    code_on_code = select_records(
        records, intervention="code_literal_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=CODE_IDS
    )
    code_on_name = select_records(
        records, intervention="code_literal_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=NAME_IDS
    )
    name_on_code = select_records(
        records, intervention="name_literal_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=CODE_IDS
    )
    name_on_weak_name = select_records(
        records, intervention="name_literal_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=WEAK_NAME_IDS
    )
    name_on_strong_name = select_records(
        records, intervention="name_literal_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=STRONG_NAME_IDS
    )

    lines = [
        "# Verification Round 23",
        "",
        "这个文件是对 actual hallucination literal-subsplit pilot 的机械核对，不引入新的主张。",
        "",
        check(
            "Record count",
            actual_records == expected_records,
            f"expected `{expected_records}`, observed `{actual_records}`.",
        ),
        check(
            "Focused pilot slice is the intended 6-item literal subsplit set",
            results["slice_ids"] == SLICE_IDS,
            f"observed slice ids = `{results['slice_ids']}`.",
        ),
        check(
            "Typed note-aware removes the high-N false-present on the strengthened literal slice",
            typed_note_n8["false_present_rate"] < typed_unified_n8["false_present_rate"],
            f"typed unified/note-aware false_present at N=8 = `{typed_unified_n8['false_present_rate']:.3f}`/`{typed_note_n8['false_present_rate']:.3f}`.",
        ),
        check(
            "Broad literal note-aware removes the high-N false-present on the strengthened literal slice",
            literal_note_n8["false_present_rate"] < literal_unified_n8["false_present_rate"],
            f"literal unified/note-aware false_present at N=8 = `{literal_unified_n8['false_present_rate']:.3f}`/`{literal_note_n8['false_present_rate']:.3f}`.",
        ),
        check(
            "Code-only branch keeps code-like overlap clues but blocks name-overlap items",
            signal_count(code_on_code) > 0 and signal_count(code_on_name) == 0,
            f"code branch signal counts on code/name ids at N=8 = `{signal_count(code_on_code)}`/`{signal_count(code_on_name)}`.",
        ),
        check(
            "Name-only branch blocks code-like overlap items",
            signal_count(name_on_code) == 0,
            f"name branch signal count on code ids at N=8 = `{signal_count(name_on_code)}`.",
        ),
        check(
            "Strengthened name-overlap items create more detector-visible work than the weak name pair under the name-only branch",
            signal_count(name_on_strong_name) > signal_count(name_on_weak_name),
            f"name branch signal counts on weak/strengthened name ids at N=8 = `{signal_count(name_on_weak_name)}`/`{signal_count(name_on_strong_name)}`.",
        ),
        check(
            "Broad literal branch benefits from the strengthened name-overlap items via raw recovery",
            signal_count(literal_on_strong_name) > signal_count(literal_on_weak_name),
            f"literal branch signal counts on weak/strengthened name ids at N=8 = `{signal_count(literal_on_weak_name)}`/`{signal_count(literal_on_strong_name)}`.",
        ),
        check(
            "Name-only branch produces real detector-visible work on the strengthened name items",
            signal_count(name_on_strong_name) > 0,
            f"name branch strengthened-name signal/tent/raw at N=8 = `{signal_count(name_on_strong_name)}`/`{clue_count(name_on_strong_name)}`/`{raw_count(name_on_strong_name)}`.",
        ),
        check(
            "Code note-aware improves over unified, and name note-aware stays non-worse at high N",
            code_note_n8["false_present_rate"] <= code_unified_n8["false_present_rate"]
            and name_note_n8["false_present_rate"] <= name_unified_n8["false_present_rate"],
            f"code unified/note-aware false_present at N=8 = `{code_unified_n8['false_present_rate']:.3f}`/`{code_note_n8['false_present_rate']:.3f}`; name unified/note-aware = `{name_unified_n8['false_present_rate']:.3f}`/`{name_note_n8['false_present_rate']:.3f}`.",
        ),
        check(
            "All note-aware branches keep zero residual contamination at N=8",
            results["aggregate"]["typed_selective_anchor"]["scale_aware_note_aware"]["8"]["residual_bad_memory_rate"] == 0.0
            and results["aggregate"]["literal_identity_anchor"]["scale_aware_note_aware"]["8"]["residual_bad_memory_rate"] == 0.0
            and results["aggregate"]["code_literal_anchor"]["scale_aware_note_aware"]["8"]["residual_bad_memory_rate"] == 0.0
            and results["aggregate"]["name_literal_anchor"]["scale_aware_note_aware"]["8"]["residual_bad_memory_rate"] == 0.0,
            "typed/literal/code/name note-aware residual at N=8 all equal `0.000`.",
        ),
        "",
        "## Bottom Line",
        "",
        "如果这些检查通过，说明这一轮补强不是只把 literal family 变大，而是真的把其中的人名子支路做得更可测：强化后的 name-overlap item 比旧弱样本更容易触发 detector-visible work，而且这个增益主要体现在 raw recovery / recoverable signal，而不只是 tentative target claim 的条数上。",
    ]

    (base_dir / VERIFY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / VERIFY_PATH}")


if __name__ == "__main__":
    main()
