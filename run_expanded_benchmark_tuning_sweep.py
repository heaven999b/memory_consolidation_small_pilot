from __future__ import annotations

import json
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

import run_expanded_benchmark_staged as stage_base


TARGET_ARCHITECTURES = ["scale_aware_unified", "scale_aware_note_aware", "psu"]
DEFAULT_STAGE = "large"
PROFILES = {
    "baseline": {
        "description": "Current benchmark-stage baseline with the default probe, note-aware, and routing thresholds.",
        "env": {},
    },
    "recover_more_v1": {
        "description": "Makes answerable noisy targets easier to recover while reducing the absent-target noise bonus.",
        "env": {
            "MEMORY_PROBE_EXISTS_NOISE_PENALTY": "0.03",
            "MEMORY_PROBE_ABSENT_NOISE_BONUS": "0.16",
            "MEMORY_PROBE_UNCERTAIN_THRESHOLD": "0.40",
        },
    },
    "note_soft_v1": {
        "description": "Builds on recover_more_v1 and softens note-aware penalties so answerable medium-criticality benchmark items are less likely to collapse into absent.",
        "env": {
            "MEMORY_PROBE_EXISTS_NOISE_PENALTY": "0.03",
            "MEMORY_PROBE_ABSENT_NOISE_BONUS": "0.16",
            "MEMORY_PROBE_UNCERTAIN_THRESHOLD": "0.40",
            "MEMORY_NOTE_INFERENCE_PENALTY_ABSENT": "0.14",
            "MEMORY_NOTE_INFERENCE_PENALTY_PRESENT": "0.04",
            "MEMORY_NOTE_MISSING_PENALTY": "0.08",
            "MEMORY_NOTE_MISSING_CONFLICT_PENALTY": "0.03",
            "MEMORY_NOTE_CLEAN_BONUS": "0.06",
        },
    },
}


@contextmanager
def temp_env(overrides: dict[str, str]) -> Iterator[None]:
    previous: dict[str, str | None] = {key: os.environ.get(key) for key in overrides}
    try:
        for key, value in overrides.items():
            os.environ[key] = value
        yield
    finally:
        for key, old_value in previous.items():
            if old_value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = old_value


def family_row(payload: dict[str, object], family_key: str, architecture: str, n_passes: int) -> dict[str, float]:
    family = payload["family_rollups"][family_key]
    return family["snapshots"][architecture][str(n_passes)]


def build_summary(stage: str, payloads: dict[str, dict[str, object]]) -> str:
    lines = [
        f"# Expanded Benchmark Tuning Sweep: {stage}",
        "",
        "这份 sweep 固定同一个 expanded benchmark stage，只改变 scale-aware / note-aware 相关阈值，比较三组 profile 在统一 benchmark 面上的 tradeoff。",
        "",
        f"- stage: `{stage}`",
        f"- architectures: `{', '.join(TARGET_ARCHITECTURES)}`",
        f"- compared profiles: `{', '.join(PROFILES)}`",
        "",
    ]
    for profile_name, profile in PROFILES.items():
        lines.append(f"## {profile_name}")
        lines.append("")
        lines.append(f"- description: {profile['description']}")
        lines.append(f"- env overrides: `{profile['env']}`")
        lines.append("")
        lines.append("| Method | benign N=8 acc | benign N=8 history_loss | benign N=8 raw | hallucination N=8 acc | hallucination N=8 false_present | hallucination N=8 raw |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|")
        payload = payloads[profile_name]
        for architecture in TARGET_ARCHITECTURES:
            benign = family_row(payload, "benign_utility_expanded_pool", architecture, 8)
            hallucination = family_row(payload, "hallucination_expanded_pool", architecture, 8)
            lines.append(
                f"| {architecture} | {benign['accuracy']:.3f} | {benign['history_loss_rate']:.3f} | {benign['raw_escalation_rate']:.3f} | "
                f"{hallucination['accuracy']:.3f} | {hallucination['false_present_rate']:.3f} | {hallucination['raw_escalation_rate']:.3f} |"
            )
        lines.append("")

    lines.extend(
        [
            "## Delta Readout",
            "",
            "| Method | Metric | baseline | recover_more_v1 | note_soft_v1 |",
            "|---|---|---:|---:|---:|",
        ]
    )
    for architecture in TARGET_ARCHITECTURES:
        baseline_benign = family_row(payloads["baseline"], "benign_utility_expanded_pool", architecture, 8)
        recover_benign = family_row(payloads["recover_more_v1"], "benign_utility_expanded_pool", architecture, 8)
        note_benign = family_row(payloads["note_soft_v1"], "benign_utility_expanded_pool", architecture, 8)
        baseline_hallu = family_row(payloads["baseline"], "hallucination_expanded_pool", architecture, 8)
        recover_hallu = family_row(payloads["recover_more_v1"], "hallucination_expanded_pool", architecture, 8)
        note_hallu = family_row(payloads["note_soft_v1"], "hallucination_expanded_pool", architecture, 8)
        lines.append(
            f"| {architecture} | benign accuracy | {baseline_benign['accuracy']:.3f} | {recover_benign['accuracy']:.3f} | {note_benign['accuracy']:.3f} |"
        )
        lines.append(
            f"| {architecture} | benign history_loss | {baseline_benign['history_loss_rate']:.3f} | {recover_benign['history_loss_rate']:.3f} | {note_benign['history_loss_rate']:.3f} |"
        )
        lines.append(
            f"| {architecture} | benign raw escalation | {baseline_benign['raw_escalation_rate']:.3f} | {recover_benign['raw_escalation_rate']:.3f} | {note_benign['raw_escalation_rate']:.3f} |"
        )
        lines.append(
            f"| {architecture} | hallucination false_present | {baseline_hallu['false_present_rate']:.3f} | {recover_hallu['false_present_rate']:.3f} | {note_hallu['false_present_rate']:.3f} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- 这组 sweep 主要回答的是 route/probe/detector 门槛能不能在不牺牲 hallucination-side cleanliness 的前提下，改善 benchmark-grounded benign utility。",
            "- 如果 `scale_aware_note_aware` 和 `psu` 在 benign 侧 gains 明显，而 hallucination false_present 仍接近 `0`，就说明下一步值得把该 profile 推到更大的 expanded main run。",
            "- 如果 benign `history_loss` 基本不变，那说明仅靠 route/probe 调参不够，后续就该优先继续优化 PSU 的 compaction contract，而不是只调 detector 门槛。",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    stage = os.environ.get("EXPANDED_BENCHMARK_TUNING_STAGE", DEFAULT_STAGE).strip().lower()
    if stage not in stage_base.STAGE_SPECS:
        raise RuntimeError(f"Unknown tuning stage `{stage}`. Expected one of {sorted(stage_base.STAGE_SPECS)}.")

    base_dir = Path(__file__).resolve().parent
    output_dir = base_dir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    payloads: dict[str, dict[str, object]] = {}
    for profile_name, profile in PROFILES.items():
        with temp_env(profile["env"]):
            payload = stage_base.build_stage_payload(stage, architectures=TARGET_ARCHITECTURES)
        payload["tuning_profile"] = {
            "name": profile_name,
            "description": profile["description"],
            "env_overrides": profile["env"],
        }
        payloads[profile_name] = payload
        json_path = output_dir / f"expanded_benchmark_tuning_{stage}_{profile_name}.json"
        md_path = output_dir / f"expanded_benchmark_tuning_{stage}_{profile_name}.md"
        json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        md_path.write_text(stage_base.build_summary(payload), encoding="utf-8")
        print(f"Wrote {json_path}")
        print(f"Wrote {md_path}")

    comparison_payload = {
        "stage": stage,
        "architectures": TARGET_ARCHITECTURES,
        "profiles": payloads,
    }
    comparison_json_path = output_dir / f"expanded_benchmark_tuning_{stage}_comparison.json"
    comparison_md_path = output_dir / f"expanded_benchmark_tuning_{stage}_comparison.md"
    comparison_json_path.write_text(json.dumps(comparison_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    comparison_md_path.write_text(build_summary(stage, payloads), encoding="utf-8")
    print(f"Wrote {comparison_json_path}")
    print(f"Wrote {comparison_md_path}")


if __name__ == "__main__":
    main()
