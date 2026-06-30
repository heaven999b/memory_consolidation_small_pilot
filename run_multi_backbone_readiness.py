from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Any


JSON_PATH = "outputs/multi_backbone_readiness.json"
SUMMARY_PATH = "outputs/multi_backbone_readiness.md"

BACKBONE_PROFILES = [
    {
        "label": "deepseek_cli_default",
        "backend": "deepseek_cli",
        "required_env": [],
        "notes": "Uses the local `deepseek` CLI path already exercised by the current runs.",
    },
    {
        "label": "openai_default",
        "backend": "openai_compatible",
        "required_env": ["OPENAI_API_KEY", "OPENAI_BASE_URL", "OPENAI_MODEL"],
        "notes": "Generic OpenAI-compatible profile. Suitable when a GPT-style model is exposed through a standard chat-completions endpoint.",
    },
    {
        "label": "gpt_openai_profile",
        "backend": "openai_compatible",
        "required_env": ["GPT_OPENAI_API_KEY", "GPT_OPENAI_BASE_URL", "GPT_OPENAI_MODEL"],
        "notes": "Dedicated GPT-profile alias so A2 can report a named non-DeepSeek backbone separately from the default profile.",
    },
    {
        "label": "qwen_openai_profile",
        "backend": "openai_compatible",
        "required_env": ["QWEN_OPENAI_API_KEY", "QWEN_OPENAI_BASE_URL", "QWEN_OPENAI_MODEL"],
        "notes": "Dedicated Qwen-profile alias for a second non-DeepSeek backbone.",
    },
    {
        "label": "llama_openai_profile",
        "backend": "openai_compatible",
        "required_env": ["LLAMA_OPENAI_API_KEY", "LLAMA_OPENAI_BASE_URL", "LLAMA_OPENAI_MODEL"],
        "notes": "Dedicated Llama-profile alias for an additional non-DeepSeek backbone.",
    },
]


def build_profile_status(profile: dict[str, Any]) -> dict[str, Any]:
    missing_env = [name for name in profile["required_env"] if not os.environ.get(name, "").strip()]
    deepseek_found = shutil.which("deepseek") is not None if profile["backend"] == "deepseek_cli" else None
    ready = (deepseek_found is True) if profile["backend"] == "deepseek_cli" else len(missing_env) == 0
    return {
        "label": profile["label"],
        "backend": profile["backend"],
        "ready": ready,
        "missing_env": missing_env,
        "deepseek_cli_found": deepseek_found,
        "notes": profile["notes"],
    }


def build_payload() -> dict[str, Any]:
    profiles = [build_profile_status(profile) for profile in BACKBONE_PROFILES]
    ready_profiles = [profile["label"] for profile in profiles if profile["ready"]]
    non_deepseek_ready = [
        profile["label"]
        for profile in profiles
        if profile["ready"] and profile["backend"] == "openai_compatible"
    ]
    return {
        "description": "A2 readiness surface for cross-backbone summarizer evaluation.",
        "profiles": profiles,
        "verdict": {
            "multi_backbone_ready": len(non_deepseek_ready) >= 2,
            "ready_profiles": ready_profiles,
            "non_deepseek_ready_profiles": non_deepseek_ready,
            "note": (
                "At least two named non-DeepSeek backbone profiles are configured, so cross-backbone A2 runs can start."
                if len(non_deepseek_ready) >= 2
                else "The repo can now route to non-DeepSeek backends, but fewer than two named alternative profiles are configured."
            ),
        },
    }


def build_summary(payload: dict[str, Any]) -> str:
    lines = [
        "# Multi-Backbone Readiness",
        "",
        "This artifact turns A2 into a concrete execution surface: which summarizer backbone profiles exist, and which ones are actually configured right now.",
        "",
        f"- multi-backbone ready: `{payload['verdict']['multi_backbone_ready']}`",
        f"- ready profiles: `{payload['verdict']['ready_profiles']}`",
        f"- ready non-deepseek profiles: `{payload['verdict']['non_deepseek_ready_profiles']}`",
        "",
        "| Profile | Backend | Ready | Missing env | DeepSeek CLI found |",
        "|---|---|---|---|---|",
    ]
    for profile in payload["profiles"]:
        missing_env = ", ".join(profile["missing_env"]) if profile["missing_env"] else "-"
        deepseek_found = "-" if profile["deepseek_cli_found"] is None else str(profile["deepseek_cli_found"])
        lines.append(
            f"| {profile['label']} | {profile['backend']} | {profile['ready']} | {missing_env} | {deepseek_found} |"
        )
    lines.extend(
        [
            "",
            "## Readout",
            "",
            "- `deepseek_memory_summarizer.py` now supports both `deepseek_cli` and `openai_compatible` backends.",
            "- This readiness table makes A2 falsifiable: we can now name exactly which additional backbone profiles are still missing.",
            "- Once two non-DeepSeek profiles are configured, the next step is to launch the same staged benchmark under each profile and compare PSU retention / hallucination behavior across backbones.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    payload = build_payload()
    (base_dir / JSON_PATH).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (base_dir / SUMMARY_PATH).write_text(build_summary(payload), encoding="utf-8")
    print(f"Wrote {base_dir / JSON_PATH}")
    print(f"Wrote {base_dir / SUMMARY_PATH}")


if __name__ == "__main__":
    main()
