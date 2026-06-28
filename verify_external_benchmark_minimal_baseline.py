from __future__ import annotations

import json
from pathlib import Path


RESULTS_PATH = "outputs/external_benchmark_minimal_baseline.json"
VERIFY_PATH = "reviews/verification_round33_benchmark.md"
HALUMEM_SLICE_PATH = "benchmarks/halumem/frozen_slices/halumem_hallucination_slice_v2.json"
LOCOMO_SLICE_PATH = "benchmarks/locomo/frozen_slices/locomo_benign_utility_slice_v2.json"


def check(label: str, passed: bool, detail: str) -> str:
    status = "PASS" if passed else "FAIL"
    return f"- [{status}] {label}: {detail}"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    results = load_json(base_dir / RESULTS_PATH)
    halumem_slice = load_json(base_dir / HALUMEM_SLICE_PATH)
    locomo_slice = load_json(base_dir / LOCOMO_SLICE_PATH)

    halu_panel = results["benchmark_panels"]["halumem_hallucination"]
    locomo_panel = results["benchmark_panels"]["locomo_benign_utility"]

    lines = [
        "# Verification Round 33 Benchmark",
        "",
        "这个文件只做机械核对：确认 v2 frozen external benchmark slice 不只是存在，而且真的被跑成了 multi-seed reviewer-facing panel。",
        "",
        check(
            "Benchmark verdict is explicitly ready",
            results["verdict"]["minimal_benchmark_grounded_panel_ready"] is True,
            f"observed verdict = `{results['verdict']}`.",
        ),
        check(
            "HaluMem slice ids match the frozen manifest",
            halu_panel["slice_ids"] == [item["id"] for item in halumem_slice["items"]],
            f"observed ids = `{halu_panel['slice_ids']}`.",
        ),
        check(
            "LoCoMo slice ids match the frozen manifest",
            locomo_panel["slice_ids"] == [item["id"] for item in locomo_slice["items"]],
            f"observed ids = `{locomo_panel['slice_ids']}`.",
        ),
        check(
            "Both panels keep the expected item count",
            halu_panel["num_items"] == 8 and locomo_panel["num_items"] == 8,
            f"observed counts = `HaluMem {halu_panel['num_items']}`, `LoCoMo {locomo_panel['num_items']}`.",
        ),
        check(
            "Benchmark run is now multi-seed",
            len(results.get("seeds", [])) > 1,
            f"observed seeds = `{results.get('seeds', [])}`.",
        ),
        check(
            "All four architectures are present in both benchmark panels",
            sorted(halu_panel["snapshots"].keys()) == sorted(locomo_panel["snapshots"].keys()) == ["scale_aware_note_aware", "scale_aware_unified", "summary_only", "tiered"],
            f"observed HaluMem methods = `{sorted(halu_panel['snapshots'].keys())}`.",
        ),
        check(
            "Each panel exposes the expected N grid",
            sorted(halu_panel["snapshots"]["summary_only"].keys()) == ["1", "4", "8"] and sorted(locomo_panel["snapshots"]["summary_only"].keys()) == ["1", "4", "8"],
            f"observed N keys = `{sorted(halu_panel['snapshots']['summary_only'].keys())}`.",
        ),
        check(
            "HaluMem panel reports hallucination-side metrics",
            "false_present_rate" in halu_panel["snapshots"]["scale_aware_unified"]["8"],
            f"observed keys = `{sorted(halu_panel['snapshots']['scale_aware_unified']['8'].keys())}`.",
        ),
        check(
            "LoCoMo panel reports answerability-loss metrics",
            "history_loss_rate" in locomo_panel["snapshots"]["scale_aware_unified"]["8"],
            f"observed keys = `{sorted(locomo_panel['snapshots']['scale_aware_unified']['8'].keys())}`.",
        ),
        check(
            "Both panels expose per-seed snapshots for every architecture and N",
            all(
                sorted(panel["seed_snapshots"].keys()) == ["scale_aware_note_aware", "scale_aware_unified", "summary_only", "tiered"]
                and sorted(panel["seed_snapshots"]["summary_only"].keys()) == ["1", "4", "8"]
                and all(sorted(panel["seed_snapshots"]["summary_only"][n_key].keys()) == [str(seed) for seed in results["seeds"]] for n_key in ["1", "4", "8"])
                for panel in [halu_panel, locomo_panel]
            ),
            f"observed seed snapshot seeds = `{sorted(halu_panel['seed_snapshots']['summary_only']['8'].keys())}`.",
        ),
        check(
            "Both panels are explicitly tied to the v2 slice manifests",
            halu_panel["slice_manifest_path"] == HALUMEM_SLICE_PATH
            and locomo_panel["slice_manifest_path"] == LOCOMO_SLICE_PATH
            and halu_panel.get("slice_manifest_version") == "v2"
            and locomo_panel.get("slice_manifest_version") == "v2",
            (
                f"observed manifest paths = `{halu_panel['slice_manifest_path']}`, `{locomo_panel['slice_manifest_path']}`; "
                f"versions = `{halu_panel.get('slice_manifest_version')}`, `{locomo_panel.get('slice_manifest_version')}`."
            ),
        ),
        "",
        "## Bottom Line",
        "",
        "如果这些检查通过，说明 external benchmark 这一层已经不是只有 adapter contract，而是已经变成真正可运行、可核对、且具备基本多 seed 稳定性读数的最小 benchmark-grounded baseline panel。",
    ]

    (base_dir / VERIFY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / VERIFY_PATH}")


if __name__ == "__main__":
    main()
