from __future__ import annotations

import json
from pathlib import Path


RESULTS_PATH = "outputs/external_benchmark_reviewer_section.json"
VERIFY_PATH = "reviews/verification_round34_reviewer_section.md"

EXPECTED_PANELS = [
    "halumem_core_v2",
    "halumem_holdout_v1",
    "locomo_core_v2",
    "longmemeval_direct_v1",
]


def check(label: str, passed: bool, detail: str) -> str:
    status = "PASS" if passed else "FAIL"
    return f"- [{status}] {label}: {detail}"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    results = json.loads((base_dir / RESULTS_PATH).read_text(encoding="utf-8"))
    slice_panels = results["slice_panels"]
    family_rollups = results["family_rollups"]

    lines = [
        "# Verification Round 34 Reviewer Section",
        "",
        "这个文件只做机械核对：确认 broader reviewer-facing benchmark section 真的已经形成，而不是只有 minimal starter panel。",
        "",
        check(
            "Reviewer section verdict is explicitly ready",
            results["verdict"]["benchmark_reviewer_section_ready"] is True,
            f"observed verdict = `{results['verdict']}`.",
        ),
        check(
            "All four expected slice panels are present",
            sorted(slice_panels.keys()) == sorted(EXPECTED_PANELS),
            f"observed panels = `{sorted(slice_panels.keys())}`.",
        ),
        check(
            "Both benchmark families now expose broader rollups",
            sorted(family_rollups.keys()) == ["benign_utility_benchmark_section", "hallucination_benchmark_section"],
            f"observed families = `{sorted(family_rollups.keys())}`.",
        ),
        check(
            "HaluMem reviewer section covers two slice panels and 16 total items",
            family_rollups["hallucination_benchmark_section"]["panel_ids"] == ["halumem_core_v2", "halumem_holdout_v1"]
            and family_rollups["hallucination_benchmark_section"]["num_items"] == 16,
            (
                f"observed HaluMem panel ids = `{family_rollups['hallucination_benchmark_section']['panel_ids']}`, "
                f"num_items = `{family_rollups['hallucination_benchmark_section']['num_items']}`."
            ),
        ),
        check(
            "Benign reviewer section covers both LoCoMo and LongMemEval with 16 total items",
            family_rollups["benign_utility_benchmark_section"]["panel_ids"] == ["locomo_core_v2", "longmemeval_direct_v1"]
            and family_rollups["benign_utility_benchmark_section"]["num_items"] == 16,
            (
                f"observed benign panel ids = `{family_rollups['benign_utility_benchmark_section']['panel_ids']}`, "
                f"num_items = `{family_rollups['benign_utility_benchmark_section']['num_items']}`."
            ),
        ),
        check(
            "Reviewer section is multi-seed",
            len(results.get("seeds", [])) > 1,
            f"observed seeds = `{results.get('seeds', [])}`.",
        ),
        check(
            "Every slice panel exposes N=1 and N=8 rows for all four architectures",
            all(
                sorted(panel["snapshots"].keys()) == ["scale_aware_note_aware", "scale_aware_unified", "summary_only", "tiered"]
                and sorted(panel["snapshots"]["summary_only"].keys()) == ["1", "8"]
                for panel in slice_panels.values()
            ),
            f"observed N keys = `{sorted(slice_panels['halumem_core_v2']['snapshots']['summary_only'].keys())}`.",
        ),
        check(
            "Family rollups keep per-seed snapshots",
            all(
                sorted(family["seed_snapshots"]["summary_only"]["8"].keys()) == [str(seed) for seed in results["seeds"]]
                for family in family_rollups.values()
            ),
            f"observed seed keys = `{sorted(family_rollups['hallucination_benchmark_section']['seed_snapshots']['summary_only']['8'].keys())}`.",
        ),
        "",
        "## Bottom Line",
        "",
        "如果这些检查通过，说明 benchmark-first surface 后面的 benchmark core 已经从两条 starter slices 扩成更宽的 reviewer-facing benchmark section，而且新增的 holdout / LongMemEval 部分也真的跑进了同一套 stack。",
    ]

    (base_dir / VERIFY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / VERIFY_PATH}")


if __name__ == "__main__":
    main()
