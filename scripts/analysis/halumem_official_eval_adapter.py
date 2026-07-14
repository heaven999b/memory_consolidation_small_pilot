#!/usr/bin/env python3
"""Phase 3a/3b: adapter to score our system with the OFFICIAL HaluMem evaluation.

Goal (audit's top alignment gap): stop scoring the hallucination axis only with
our self-built failure-mode judge, and instead feed our system's outputs into the
official ``benchmarks/halumem/official_repo/eval/evaluation.py`` so we can report
the paper's own metrics (memory integrity / accuracy / update / QA).

Contract (verified by reading evaluation.py + eval_tools.py):
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
  --validate  : OFFLINE, zero API. Builds the per-user output SKELETON with the
                three system fields stubbed empty and asserts the emitted schema
                matches what evaluation.py reads. Writes a *_skeleton.jsonl.
  --self-test : OFFLINE, zero API. Drives fill_system_side with a MOCK backend and
                asserts the produced record is evaluation.py-valid with all three
                system fields populated. This verifies the live wiring's control
                flow (per-session reset -> observe -> consolidate -> retrieve ->
                answer -> field assignment) WITHOUT spending any API budget.
  --from-run  : OFFLINE, zero API. Fills only qa["system_response"] by matching
                golden questions against an EXISTING run's *_qa.jsonl model_response
                (extracted_memories / memories_from_system stay empty and still
                need --live). Lets already-produced answers be scored by the
                official QA metric without re-driving TierMem.
  --live      : PAID. Fills all three fields by driving TierMem per golden session
                (write each turn, consolidate, retrieve, answer). This calls the
                real memory harness and costs API budget; smoke it first with
                --user-limit 1 --session-limit 1 (a single golden user has ~65
                sessions, so an unbounded --live is expensive).

After producing the filled jsonl, score it with the OFFICIAL judge. NB: the
official evaluation.py CLI only takes --frame (3rd-party systems) / --version and
reads results/{frame}-{version}/{frame}_eval_results.jsonl -- there is NO
--file_path. To score OUR output: copy it there, then
`from evaluation import main; main('tiermem', '<ver>', user_num=N)` (this bypasses
the --frame choices). Read scores from the per-user tmp2/*.json cache: the official
aggregate_eval_results ZeroDivides when a memory_type has 0 items on a small sample,
so aggregate integrity/accuracy/update/QA from the cached records yourself. Judge env
needed: OPENAI_API_KEY / OPENAI_BASE_URL / OPENAI_MODEL + RETRY_TIMES /
WAIT_TIME_LOWER / WAIT_TIME_UPPER. Both the fill (--live) and the judge cost API.
"""
from __future__ import annotations

import argparse
import gc
import json
import os
import re
import sys
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


# --- OFFLINE path: reuse an existing run's answers ---------------------------

def fill_from_run(record: dict[str, Any], run_dir: str | os.PathLike) -> tuple[int, int]:
    """OFFLINE. Fill qa[system_response] from an existing run's *_qa.jsonl.

    Matches on (uuid, question text) -- verified near-unique per user. Only
    system_response is recoverable offline; extracted_memories / memories_from_system
    were never persisted as text, so they stay empty and need --live.
    Returns (filled, total) question counts.
    """
    uuid = str(record.get("uuid", ""))
    run_path = Path(run_dir).expanduser()
    qmap: dict[str, Any] = {}
    # sorted so overwrite order is deterministic when the same question text appears
    # across multiple run files (e.g. a depth sweep n0/n1/n2); highest-sorted file wins.
    for qf in sorted(run_path.rglob(f"*{uuid}*_qa.jsonl")):
        with qf.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                except json.JSONDecodeError:
                    continue
                q = d.get("question")
                if q is not None and "model_response" in d:
                    qmap[str(q).strip()] = d.get("model_response")
    filled = total = 0
    for session in record.get("sessions", []):
        for qa in session.get("questions", []) or []:
            total += 1
            r = qmap.get(str(qa.get("question", "")).strip())
            if r is not None:
                qa[SYS_QA_FIELD] = r
                filled += 1
    return filled, total


# --- LIVE path: drive TierMem per golden session -----------------------------

def _lazy_upstream() -> dict[str, Any]:
    """Import the upstream harness + bridge helpers (heavy; only for --live)."""
    scripts_run = ROOT / "scripts" / "run"
    if str(scripts_run) not in sys.path:
        sys.path.insert(0, str(scripts_run))
    from run_v2_tiermem_local_bridge import (  # type: ignore
        build_parser, _build_lv_cfg, _spec_for, _ensure_tiermem_import_path,
    )
    _ensure_tiermem_import_path()  # sets MEM0_DIR / MEM0_TELEMETRY + adds tiermem to sys.path
    from src.memory.base import Turn  # type: ignore
    from src.memory.linked_view_system import LinkedViewSystem  # type: ignore
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit(
            "OPENAI_API_KEY not set (source .env.v3) -- --live drives real TierMem and costs API budget."
        )
    return {"build_parser": build_parser, "_build_lv_cfg": _build_lv_cfg,
            "_spec_for": _spec_for, "Turn": Turn, "LinkedViewSystem": LinkedViewSystem}


def _build_live_system(up: dict[str, Any], args: argparse.Namespace,
                       collection_name: str, qdrant_path: Path) -> Any:
    """Build a LinkedViewSystem using the bridge's own default config (no drift)."""
    parser = up["build_parser"]()
    argv = ["--model", getattr(args, "model", "gpt-4.1-mini"), "--benchmark", "halumem",
            "--page-write-mode", getattr(args, "page_write_mode", "infer"),
            "--consolidation-passes", str(getattr(args, "consolidation_passes", 0))]
    ns, _unknown = parser.parse_known_args(argv)
    spec = up["_spec_for"]("halumem")
    cfg = up["_build_lv_cfg"](ns, spec, collection_name, Path(qdrant_path))
    return up["LinkedViewSystem"](cfg)


def _extract_session_memories(system: Any, sid: str) -> list[str]:
    """Collect the compact memory texts the system holds for this session.

    Prefers the mem0 memories stored by update_page_mem0_status; falls back to the
    page summary/content. Defensive getattr so the exact Page attr name can't break it.
    """
    out: list[str] = []
    ps = getattr(system, "page_store", None)
    pages: list[Any] = []
    if ps is not None:
        try:
            pages = ps.get_pages_by_session(sid) or []
        except Exception:  # noqa: BLE001
            pages = []
    for page in pages:
        mems = getattr(page, "memories", None)  # real Page field: mem0.add's returned list
        if mems:
            out.extend(str(m) for m in mems if m)
        else:  # page not yet stored to mem0 -> fall back to its summary/content
            s = getattr(page, "summary", None) or getattr(page, "content", None)
            if s:
                out.append(str(s))
    seen: set[str] = set()
    uniq: list[str] = []
    for m in out:
        if m and m not in seen:
            seen.add(m)
            uniq.append(m)
    return uniq


def _retrieve_full(system: Any, sid: str, query: str, top_k: int = 10) -> list[str]:
    """Full-text system retrieval for one query (UNtruncated).

    Prefers the internal _search_summary_hits (returns full hit.summary_text so the
    official update metric sees the real memory text, not a 100-char preview); falls
    back to answer()'s hits_summary memory_preview only if that API is unavailable.
    """
    try:
        hits, _usage = system._search_summary_hits(
            session_id=sid, user_id=f"{sid}:user", query=query, top_k=top_k)
        out = [t for t in (getattr(h, "summary_text", None) for h in hits) if t]
        if out:
            return out
    except Exception:  # noqa: BLE001
        pass
    res = system.answer(query)
    hits = (getattr(res, "mechanism_trace", None) or {}).get("hits_summary", []) or []
    return [h.get("memory_preview") for h in hits if h.get("memory_preview")]


def fill_system_side(record: dict[str, Any], args: argparse.Namespace | None,
                     system_factory: Any = None) -> dict[str, Any]:
    """Fill the 3 system fields by driving TierMem, one golden session at a time.

    system_factory: optional callable(session_id)->system used by --self-test to
    inject a MOCK backend and exercise this exact control flow offline. When None,
    a real LinkedViewSystem is built per session (PAID).
    """
    uuid = str(record.get("uuid", "user"))
    if system_factory is None:
        up = _lazy_upstream()
        Turn = up["Turn"]
        def make_turn(t: dict[str, Any]) -> Any:
            return Turn(speaker=t.get("role", ""), text=t.get("content", ""),
                        timestamp=t.get("timestamp"))
        qbase = Path(getattr(args, "qdrant_path", None) or (ROOT / "outputs" / "halumem_official_qdrant"))
        qbase.mkdir(parents=True, exist_ok=True)
    else:
        up = None
        def make_turn(t: dict[str, Any]) -> Any:
            return t

    for si, session in enumerate(record.get("sessions", [])):
        sid = f"{uuid}_s{si}"
        system = None
        try:
            if system_factory is not None:
                system = system_factory(sid)
            else:
                # qdrant's local store takes a per-FOLDER lock, so each session needs
                # its OWN path -- a distinct collection name is NOT enough (reset() even
                # overrides it). Sharing one folder makes the 2nd+ system silently fall
                # back to an empty in-memory index and corrupt every later session.
                coll = re.sub(r"[^0-9A-Za-z_]", "_", f"hm_off_{uuid}_s{si}")[:60]
                sess_qpath = qbase / coll
                sess_qpath.mkdir(parents=True, exist_ok=True)
                system = _build_live_system(up, args, coll, sess_qpath)  # type: ignore[arg-type]
            system.reset(sid)
            for turn in session.get("dialogue", []) or []:
                system.observe(make_turn(turn))
            system.auto_summary(sid)                       # flush any not-yet-consolidated page
            # pass qa_questions so consolidation's page-selection scope matches the official
            # runner (run_benchmark_multi.py:383); no-op unless --consolidation-passes >= 1.
            qa_qs = [q.get("question", "") for q in (session.get("questions", []) or [])]
            system.run_consolidation_passes(session_id=sid, qa_questions=qa_qs)

            session[SYS_SESSION_FIELD] = _extract_session_memories(system, sid)

            for mp in session.get("memory_points", []) or []:
                if str(mp.get("is_update")) == "True":
                    mp[SYS_UPDATE_FIELD] = _retrieve_full(system, sid, mp.get("memory_content", ""))

            for qa in session.get("questions", []) or []:
                res = system.answer(qa.get("question", ""))
                qa[SYS_QA_FIELD] = getattr(res, "answer", "") or ""
        finally:
            if system_factory is None and system is not None:
                # drop the mem0 self-referential cycle so its QdrantClient (and the
                # per-folder lock) is actually released before the next session builds.
                del system
                gc.collect()
    return record


def _offline_self_test(records: list[dict[str, Any]]) -> tuple[list[str], int]:
    """Drive fill_system_side with a mock backend; assert schema + population. Zero API."""
    class _Page:
        def __init__(self, text: str) -> None:
            self.summary = text
            self.mem0_memories = None

    class _PageStore:
        def __init__(self) -> None:
            self._by: dict[str, list[Any]] = {}

        def get_pages_by_session(self, sid: str) -> list[Any]:
            return self._by.get(sid, [])

    class _Answer:
        def __init__(self, answer: str, hits: list[dict[str, str]]) -> None:
            self.answer = answer
            self.mechanism_trace = {"hits_summary": hits}

    class _MockSystem:
        def __init__(self, sid: str) -> None:
            self._sid = sid
            self.page_store = _PageStore()

        def reset(self, sid: str) -> None:
            self._sid = sid
            self.page_store._by[sid] = [_Page(f"[mock extracted memory for {sid}]")]

        def observe(self, turn: Any) -> None:
            pass

        def auto_summary(self, session_id: Any = None) -> dict[str, Any]:
            return {}

        def run_consolidation_passes(self, session_id: Any = None, qa_questions: Any = None) -> list[Any]:
            return []

        def answer(self, query: str, meta: Any = None, action: Any = None) -> _Answer:
            return _Answer(f"[mock answer: {str(query)[:40]}]",
                           [{"memory_preview": f"[mock mem: {str(query)[:30]}]"}])

    problems: list[str] = []
    filled_q = 0
    for rec in records:
        fill_system_side(rec, args=None, system_factory=lambda sid: _MockSystem(sid))
        problems.extend(validate_record(rec))
        for s in rec.get("sessions", []):
            if not s.get(SYS_SESSION_FIELD):
                problems.append(f"self-test: session left {SYS_SESSION_FIELD} empty")
            for qa in s.get("questions", []) or []:
                if qa.get(SYS_QA_FIELD):
                    filled_q += 1
    return problems, filled_q


def main() -> int:
    ap = argparse.ArgumentParser(description="HaluMem official-evaluation adapter.")
    ap.add_argument("--golden", default=str(GOLDEN))
    ap.add_argument("--user-limit", type=int, default=0, help="0 = all users.")
    ap.add_argument("--session-limit", type=int, default=0,
                    help="0 = all sessions per user; cap for live smoke (1 user has ~65 sessions).")
    ap.add_argument("--session-index", default=None,
                    help="Select specific golden session indices (comma list, e.g. '3,4') instead "
                         "of the first N -- e.g. to hit sessions that have is_update memory points.")
    ap.add_argument("--validate", action="store_true", help="Offline schema check + skeleton.")
    ap.add_argument("--self-test", action="store_true",
                    help="OFFLINE, zero API: mock-drive fill_system_side and assert schema.")
    ap.add_argument("--from-run", default=None,
                    help="OFFLINE: fill system_response from an existing run dir's *_qa.jsonl "
                         "(extracted_memories/memories_from_system stay empty, need --live).")
    ap.add_argument("--live", action="store_true", help="PAID: fill all 3 fields via TierMem.")
    ap.add_argument("--model", default="gpt-4.1-mini", help="TierMem model for --live.")
    ap.add_argument("--page-write-mode", choices=["raw", "infer"], default="infer",
                    help="infer (default) = mem0 extracts compact facts into page.memories "
                         "(required for meaningful official integrity/accuracy); raw = whole page verbatim.")
    ap.add_argument("--consolidation-passes", type=int, default=0,
                    help="0 (default) = no consolidation; >=1 runs N consolidation passes -- the "
                         "consolidation N-sweep variable for studying consolidation's effect on the "
                         "official memory metrics. qa_questions are passed so page selection aligns "
                         "with the official runner.")
    ap.add_argument("--qdrant-path", default=None,
                    help="Qdrant dir for --live (default outputs/halumem_official_qdrant).")
    ap.add_argument("--output", default=None)
    args = ap.parse_args()

    golden_path = Path(args.golden).expanduser()
    if not golden_path.exists():
        raise FileNotFoundError(golden_path)

    records = [build_skeleton(u) for u in load_golden(golden_path, args.user_limit)]
    if args.session_index:
        want = [int(x) for x in args.session_index.split(",") if x.strip().lstrip("-").isdigit()]
        for r in records:
            r["sessions"] = [r["sessions"][i] for i in want if 0 <= i < len(r["sessions"])]
    elif args.session_limit:
        for r in records:
            r["sessions"] = r["sessions"][: args.session_limit]

    if args.self_test:
        problems, filled_q = _offline_self_test(records)
        print(json.dumps({"mode": "self-test", "users": len(records),
                          "questions_filled_by_mock": filled_q,
                          "schema_problems": len(problems)}, ensure_ascii=False, indent=2))
        if problems:
            print("First problems:", problems[:5])
            return 1
        print("Self-test OK: mock-driven fill produced an evaluation.py-valid record "
              "with all 3 system fields populated.")
        return 0

    from_run_stats: dict[str, int] | None = None
    if args.live:
        mode = "live"
        for r in records:
            fill_system_side(r, args)
        default_out = golden_path.with_name("halumem_medium_tiermem_filled.jsonl")
    elif args.from_run:
        mode = "from-run"
        tot_f = tot_n = 0
        for r in records:
            f, n = fill_from_run(r, args.from_run)
            tot_f += f
            tot_n += n
        from_run_stats = {"system_response_filled": tot_f, "questions_total": tot_n}
        default_out = golden_path.with_name("halumem_medium_from_run.jsonl")
    else:
        mode = "validate"
        default_out = golden_path.with_name("halumem_medium_skeleton.jsonl")

    all_problems: list[str] = []
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
    summary: dict[str, Any] = {
        "mode": mode, "users": len(records), "sessions": n_sessions,
        "questions": n_q, "update_memory_points": n_updates,
        "schema_problems": len(all_problems), "output": str(out),
    }
    if from_run_stats:
        summary.update(from_run_stats)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if all_problems:
        print("First problems:", all_problems[:5])
        return 1
    print("Schema OK: output matches the fields evaluation.py reads.")
    if mode in ("from-run", "validate"):
        print("NOTE: extracted_memories / memories_from_system are EMPTY here. Do NOT feed this "
              "straight to official evaluation.py -- empty extracted_memories makes its aggregation "
              "ZeroDivisionError-crash and empty memories_from_system silently reclassifies is_update "
              "points. Only a full --live output is safe for official integrity/accuracy/update scoring.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
