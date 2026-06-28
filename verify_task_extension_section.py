from __future__ import annotations

import json
from pathlib import Path


RESULTS_PATH = "outputs/task_extension_section.json"
VERIFY_PATH = "reviews/verification_round37_task_extensions.md"


def check(label: str, passed: bool, detail: str) -> str:
    status = "PASS" if passed else "FAIL"
    return f"- [{status}] {label}: {detail}"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    payload = json.loads((base_dir / RESULTS_PATH).read_text(encoding="utf-8"))
    summary = payload["extension_summary"]
    panels = payload["task_extension_panels"]
    conflict = panels["conflict_manifest_backed_extension"]
    unsafe = panels["unsafe_manifest_backed_extension"]

    lines = [
        "# Verification Round 37 Task Extensions",
        "",
        "这个文件只做机械核对：确认 `conflict` / `unsafe` 已经进入 manifest-backed task extension section，而不是继续只散落在 supporting slices 里。",
        "",
        check(
            "Task extension section is explicitly ready",
            payload["verdict"]["task_extension_section_ready"] is True,
            f"observed verdict = `{payload['verdict']}`.",
        ),
        check(
            "Task extension section covers both conflict and unsafe",
            summary["task_families"] == ["conflict", "unsafe"],
            f"observed task families = `{summary['task_families']}`.",
        ),
        check(
            "Conflict extension panel keeps four frozen items",
            conflict["num_items"] == 4,
            f"observed conflict num_items = `{conflict['num_items']}`.",
        ),
        check(
            "Unsafe extension panel keeps two frozen items",
            unsafe["num_items"] == 2,
            f"observed unsafe num_items = `{unsafe['num_items']}`.",
        ),
        check(
            "Conflict extension still exposes tiered plus unified architectures",
            sorted(conflict["architectures"]) == ["scale_aware_note_aware", "scale_aware_unified", "summary_only", "tiered"],
            f"observed conflict architectures = `{conflict['architectures']}`.",
        ),
        check(
            "Unsafe extension stays tied to the carry-forward winner",
            unsafe["source_intervention"] == "tiny_carry_forward_scaffold",
            f"observed unsafe source intervention = `{unsafe['source_intervention']}`.",
        ),
        "",
        "## Bottom Line",
        "",
        "如果这些检查通过，说明 task-family coverage 的主要缺口已经补上了；接下来剩下的重点仍然是更大的 benchmark scale，而不是 conflict/unsafe 继续缺席主链。",
    ]

    (base_dir / VERIFY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / VERIFY_PATH}")


if __name__ == "__main__":
    main()
