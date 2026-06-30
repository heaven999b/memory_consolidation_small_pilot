from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


PROFILE_LIBRARY = {
    "deepseek_cli_default": {
        "backend": "deepseek_cli",
        "required_env": [],
        "env_map": {},
    },
    "openai_default": {
        "backend": "openai_compatible",
        "required_env": ["OPENAI_API_KEY", "OPENAI_BASE_URL", "OPENAI_MODEL"],
        "env_map": {
            "OPENAI_API_KEY": "MEMORY_OPENAI_API_KEY",
            "OPENAI_BASE_URL": "MEMORY_OPENAI_BASE_URL",
            "OPENAI_MODEL": "MEMORY_OPENAI_MODEL",
        },
    },
    "gpt_openai_profile": {
        "backend": "openai_compatible",
        "required_env": ["GPT_OPENAI_API_KEY", "GPT_OPENAI_BASE_URL", "GPT_OPENAI_MODEL"],
        "env_map": {
            "GPT_OPENAI_API_KEY": "MEMORY_OPENAI_API_KEY",
            "GPT_OPENAI_BASE_URL": "MEMORY_OPENAI_BASE_URL",
            "GPT_OPENAI_MODEL": "MEMORY_OPENAI_MODEL",
        },
    },
    "qwen_openai_profile": {
        "backend": "openai_compatible",
        "required_env": ["QWEN_OPENAI_API_KEY", "QWEN_OPENAI_BASE_URL", "QWEN_OPENAI_MODEL"],
        "env_map": {
            "QWEN_OPENAI_API_KEY": "MEMORY_OPENAI_API_KEY",
            "QWEN_OPENAI_BASE_URL": "MEMORY_OPENAI_BASE_URL",
            "QWEN_OPENAI_MODEL": "MEMORY_OPENAI_MODEL",
        },
    },
    "llama_openai_profile": {
        "backend": "openai_compatible",
        "required_env": ["LLAMA_OPENAI_API_KEY", "LLAMA_OPENAI_BASE_URL", "LLAMA_OPENAI_MODEL"],
        "env_map": {
            "LLAMA_OPENAI_API_KEY": "MEMORY_OPENAI_API_KEY",
            "LLAMA_OPENAI_BASE_URL": "MEMORY_OPENAI_BASE_URL",
            "LLAMA_OPENAI_MODEL": "MEMORY_OPENAI_MODEL",
        },
    },
}

OUTPUT_SUFFIXES = [".json", ".md", "_traces.md"]


def resolve_profile(profile_label: str) -> dict[str, Any]:
    if profile_label not in PROFILE_LIBRARY:
        raise RuntimeError(f"Unknown profile `{profile_label}`. Expected one of {sorted(PROFILE_LIBRARY)}.")
    profile = PROFILE_LIBRARY[profile_label]
    missing_env = [name for name in profile["required_env"] if not os.environ.get(name, "").strip()]
    if profile["backend"] == "deepseek_cli" and shutil.which("deepseek") is None:
        raise RuntimeError("Profile `deepseek_cli_default` requires the `deepseek` CLI on PATH.")
    if missing_env:
        raise RuntimeError(f"Profile `{profile_label}` is missing env vars: {missing_env}")
    return profile


def stage_output_paths(base_dir: Path, stage: str) -> list[Path]:
    stem = f"expanded_benchmark_stage_{stage}"
    return [base_dir / "outputs" / f"{stem}{suffix}" for suffix in OUTPUT_SUFFIXES]


def copy_outputs_with_suffix(base_dir: Path, stage: str, profile_label: str) -> list[str]:
    copied_paths: list[str] = []
    for source in stage_output_paths(base_dir, stage):
        if not source.exists():
            continue
        target = source.with_name(f"{source.stem}__{profile_label}{source.suffix}")
        shutil.copy2(source, target)
        copied_paths.append(str(target.relative_to(base_dir)))
    return copied_paths


def main() -> None:
    if len(sys.argv) < 3:
        raise RuntimeError("Usage: python3 run_expanded_benchmark_backbone_profile.py <stage> <profile_label>")

    stage = sys.argv[1].strip().lower()
    profile_label = sys.argv[2].strip()
    profile = resolve_profile(profile_label)

    base_dir = Path(__file__).resolve().parent
    env = os.environ.copy()
    env["MEMORY_SUMMARIZER_BACKEND"] = profile["backend"]
    for source_name, target_name in profile["env_map"].items():
        env[target_name] = env[source_name]

    command = [sys.executable, str(base_dir / "run_expanded_benchmark_staged.py"), stage]
    proc = subprocess.run(command, cwd=str(base_dir), env=env, check=False)
    copied_paths = copy_outputs_with_suffix(base_dir, stage, profile_label) if proc.returncode == 0 else []

    payload = {
        "stage": stage,
        "profile_label": profile_label,
        "backend": profile["backend"],
        "returncode": proc.returncode,
        "copied_outputs": copied_paths,
        "command": command,
    }
    status_path = base_dir / "outputs" / f"expanded_benchmark_stage_{stage}__{profile_label}_run_status.json"
    status_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {status_path}")
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)


if __name__ == "__main__":
    main()
