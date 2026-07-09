#!/usr/bin/env python3
"""Phase 3a: adapter to score our system with the OFFICIAL HaluMem evaluation.

Goal (audit's top alignment gap): stop scoring the hallucination axis only with
our self-built failure-mode judge, and instead feed our system's outputs into the
official ``benchmarks/halumem/official_repo/eval/evaluation.py`` so we can report
the paper's own metrics (memory integrity / accuracy / update / QA).

Contract (verified by reading evaluation.py + eval_memos.py):
Per user -> list of sessions; evaluation.py reads GOLD fields straight from
HaluMem-Medium and only THREE system-produced fields, which this adapter fills:

  1. session["extracted_memories"]          : list[str]  -- memories the system
                                                extracted for that session.
  2. memory_point["memories_from_system"]   : list[str]  -- system retrieval on
                                                each is_update golden memory_content.
  3. qa["system_response"]                   : str        -- system answer to the
                                                golden question.

Everything else (uuid, sessions, memory_points, questions[question/answer/evidence])
is copied through from the golden data unchanged.

Modes:
  --validate  : OFFLINE, zero API. Loads golden HaluMem-Medium, builds the
                per-user output SKELETON with the three system fields stubbed
                empty, and asserts the emitted schema matches exactly what
                evaluation.py reads. Writes a *_skeleton.jsonl. Use this to pin
                the contract before spending on a live run.
  --live      : PAID. Fills the three fields by driving TierMem (write the
                session, extract memories, retrieve, answer). This calls the
                real memory harness and is the step that costs API budget; it is
                intentionally left as a single clearly-marked integration point
                (`fill_system_side`) so it is wired once and reviewed before any
                spend. It is NOT run by --validate.

After producing the filled jsonl, score it with the official tool:
    python benchmarks/halumem/official_repo/eval/evaluation.py \
        --file_path <this_output>.jsonl --output_file <scores>.json
(That call also uses an LLM judge and costs API budget.)
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterator

ROOT = Path(__file__).resolve().parents[2]
GOLDEN = ROOT / "benchmarks" / "halumem" / "official_repo" / "data" / "HaluMem-Medium.jsonl"

# Exactly the system-produced fields evaluation.py consumes.
SYS_SESSION_FIELD = "extracted_memories"          # list[str]
SYS_UPDATE_FIELD = "memories_from_system"         # list[str] on is_update memory_points
SYS_QA_FIELD = "system_response"                  # str on each question


def load_golden(path: Path, user_limit: int = 0) -> Iterator[dict[str, Any]]:
    with path.open(encoding="utf-8") as fh:
        for i, line in enumerate(fh):
            if user_limit and i >= user_limit:
                break
            line = line.strip()
            if line:
                yield json.loads(line)


def build_skeleton(user: dict[str, Any]) -> dict[str, Any]:
    """Return an evaluation.py-shaped record with system fields stubbed empty."""
    out: dict[str, Any] = {
        "uuid": user.get("uuid"),
        "user_name": _user_name(user),
        "sessions": [],
    }
    for session in user.get("sessions", []):
        new_session = dict(session)
        new_session.setdefault(SYS_SESSION_FIELD, [])  # to be filled live
        # is_update memory points need a system-retrieval list
        new_points = []
        for mp in session.get("memory_points", []):
            mp2 = dict(mp)
            if str(mp.get("is_update")) == "True":
                mp2.setdefault(SYS_UPDATE_FIELD, [])
            new_points.append(mp2)
        new_session["memory_points"] = new_points
        # questions need a system_response
        new_qs = []
        for qa in session.get("questions", []) or []:
            qa2 = dict(qa)
            qa2.setdefault(SYS_QA_FIELD, "")
            new_qs.append(qa2)
        if "questions" in session:
            new_session["questions"] = new_qs
        out["sessions"].append(new_session)
    return out


def _user_name(user: dict[str, Any]) -> str:
    import re
    m = re.search(r"Name:\s*(.*?);", user.get("persona_info", "") or "")
    return m.group(1).strip() if m else str(user.get("uuid", "user"))


def validate_record(rec: dict[str, Any]) -> list[str]:
    """Return a list of schema problems (empty = matches evaluation.py's reads)."""
    problems: list[str] = []
    if not rec.get("uuid"):
        problems.append("missing uuid")
    for si, s in enumerate(rec.get("sessions", [])):
        if SYS_SESSION_FIELD not in s:
            problems.append(f"session[{si}] missing {SYS_SESSION_FIELD}")
        for mi, mp in enumerate(s.get("memory_points", [])):
            for gold_key in ("memory_content", "is_update", "memory_source"):
                if gold_key not in mp:
                    problems.append(f"session[{si}].memory_points[{mi}] missing gold {gold_key}")
            if str(mp.get("is_update")) == "True" and SYS_UPDATE_FIELD not in mp:
                problems.append(f"session[{si}].memory_points[{mi}] is_update but no {SYS_UPDATE_FIELD}")
        for qi, qa in enumerate(s.get("questions", []) or []):
            for gold_key in ("question", "answer", "evidence"):
                if gold_key not in qa:
                    problems.append(f"session[{si}].questions[{qi}] missing gold {gold_key}")
            if SYS_QA_FIELD not in qa:
                problems.append(f"session[{si}].questions[{qi}] missing {SYS_QA_FIELD}")
    return problems


def fill_system_side(record: dict[str, Any]) -> dict[str, Any]:
    """PAID integration point (Phase 3b). Drive TierMem to fill the 3 system fields.

    Wire this to the existing bridge in run_v2_tiermem_local_bridge.py:
      * write each session's `dialogue` through the TierMem write path;
      * set session[extracted_memories] = the system's compact memories for it;
      * for each is_update memory_point: search_memory(memory_content) ->
        memory_point[memories_from_system];
      * for each question: retrieve context + answer -> qa[system_response].
    Left unimplemented so the live wiring is reviewed before any API spend.
    """
    raise NotImplementedError(
        "fill_system_side is the paid Phase 3b integration point; wire it to "
        "run_v2_tiermem_local_bridge before running --live."
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="HaluMem official-evaluation adapter.")
    ap.add_argument("--golden", default=str(GOLDEN))
    ap.add_argument("--user-limit", type=int, default=0, help="0 = all users.")
    ap.add_argument("--validate", action="store_true", help="Offline schema check + skeleton.")
    ap.add_argument("--live", action="store_true", help="PAID: fill system fields via TierMem.")
    ap.add_argument("--output", default=None)
    args = ap.parse_args()

    golden_path = Path(args.golden).expanduser()
    if not golden_path.exists():
        raise FileNotFoundError(golden_path)

    records = [build_skeleton(u) for u in load_golden(golden_path, args.user_limit)]

    if args.live:
        records = [fill_system_side(r) for r in records]
        default_out = golden_path.with_name("halumem_medium_tiermem_filled.jsonl")
    else:
        default_out = golden_path.with_name("halumem_medium_skeleton.jsonl")

    all_problems = []
    for r in records:
        all_problems.extend(validate_record(r))

    out = Path(args.output).expanduser() if args.output else default_out
    with out.open("w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    n_sessions = sum(len(r["sessions"]) for r in records)
    n_q = sum(len(s.get("questions", []) or []) for r in records for s in r["sessions"])
    n_updates = sum(1 for r in records for s in r["sessions"]
                    for mp in s.get("memory_points", []) if str(mp.get("is_update")) == "True")
    print(json.dumps({
        "mode": "live" if args.live else "validate",
        "users": len(records), "sessions": n_sessions,
        "questions": n_q, "update_memory_points": n_updates,
        "schema_problems": len(all_problems),
        "output": str(out),
    }, ensure_ascii=False, indent=2))
    if all_problems:
        print("First problems:", all_problems[:5])
        return 1
    print("Schema OK: output matches the fields evaluation.py reads.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
