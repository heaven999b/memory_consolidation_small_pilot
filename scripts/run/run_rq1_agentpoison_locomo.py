#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RQ1 AgentPoison overlay ON LoCoMo —— 公开对话载体版。

把 backdoor 触发器注入 LoCoMo(公开)真实多轮对话流, 走真实 TierMem C^N,
测触发器 survival / laundering / retrieval@k(词法) + items dump 供 judge 测 activation。

与 run_rq1_agentpoison_overlay.py 的唯一区别: 载体从"孤立合成 poison session"
换成"LoCoMo 公开对话 session + 注入 1 条 poison turn"。这是 RQ1 安全线能做到的
**最公开形态**(载体=公开数据; 触发器构造是后门评测的固有性质, 学界皆然)。
复用 overlay 的 detectors / bootstrap / report、复用真实 TierMemBackend 引擎。

  set -a && source .env.v3 && set +a
  .venv_tiermem_v2/bin/python run_rq1_agentpoison_locomo.py --dry-run --n-items 3
  .venv_tiermem_v2/bin/python run_rq1_agentpoison_locomo.py --n-items 2 --passes 0 1   # smoke
"""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path
import numpy as np
from run_rq1_safety_consolidation import TierMemBackend
from run_rq1_agentpoison_overlay import _measure, _bootstrap, _render_md, _build_parser

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOCOMO_PATH = PROJECT_ROOT / "benchmarks" / "locomo" / "locomo_official" / "data" / "locomo10.json"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "outputs" / "safety"


class LoCoMoPoisonBackend(TierMemBackend):
    """真实 TierMem, 载体 = LoCoMo 公开对话 turns + 注入 1 条 poison turn。"""
    SESSION_PREFIX = "locomo_poison_"

    def _sessions_for(self, items):
        ts = "2026-01-01T09:00:00Z"
        sessions = []
        for it in items:
            turns = [{"speaker": t["speaker"], "text": t["text"], "timestamp": ts} for t in it["locomo_turns"]]
            # 若 write-gate 预处理过用它, 否则原始 poison_fact; 作为一条对话 turn 注入到真实对话中段
            pfact = (it.get("injection_lines") or [it["poison_fact"]])[-1]
            spk = turns[0]["speaker"] if turns else "user"
            turns.insert(it["inject_idx"], {"speaker": spk, "text": pfact, "timestamp": ts})
            # 引擎 LinkedViewSystem.preferred_turns_key="session_chunks", 按 chunk 逐条 write。
            # 之前塞成 1 个大 block chunk → 只写 1 单元且被判空(= write 0 API calls 根因)。
            # 改为逐 turn 一个 chunk(镜像 core/datasets/halumem.py 的 chunk 字段: speaker/text/timestamp/chunk_idx)。
            chunks = [{"speaker": t["speaker"], "text": t["text"], "timestamp": t["timestamp"], "chunk_idx": i}
                      for i, t in enumerate(turns)]
            sessions.append({
                "session_id": f"{self.SESSION_PREFIX}{it['id']}",
                "turns": turns,
                "session_chunks": chunks,
                "qa_pairs": [{"query_id": f"{it['id']}_trigger", "question": it["trigger_query"],
                              "ground_truth": it["gold_answer"],
                              "meta": {"support_chunk_idx": 0, "question_type": "backdoor_trigger"}}],
                "meta": {"poison_item_id": it["id"], "trigger_phrase": it["trigger_phrase"], "carrier": "locomo"},
            })
        return sessions


def build_items(locomo, suite, n_items, session_key):
    """每个 item = 1 个 LoCoMo 公开 session(真实 turns) + 1 条注入 poison(来自 suite)。"""
    items = []
    for i in range(n_items):
        conv = locomo[i % len(locomo)]["conversation"]
        raw_turns = conv.get(session_key) or conv.get("session_1") or []
        turns = [{"speaker": t["speaker"], "text": t["text"]} for t in raw_turns
                 if isinstance(t, dict) and t.get("text")]
        p = suite[i % len(suite)]
        items.append({
            "id": f"lp_{i:03d}_{p['id']}",
            "locomo_turns": turns,
            "inject_idx": max(1, len(turns) // 2),
            "poison_fact": p["poison_fact"], "benign_facts": p.get("benign_facts", []),
            "trigger_phrase": p["trigger_phrase"], "unsafe_action": p["unsafe_action"],
            "unsafe_paraphrases": p.get("unsafe_paraphrases", []), "trigger_query": p["trigger_query"],
            "gold_answer": p["gold_answer"], "policy": p.get("policy", ""), "subject": p.get("subject", ""),
        })
    return items


def main():
    p = _build_parser()
    p.add_argument("--locomo-path", default=str(LOCOMO_PATH))
    p.add_argument("--n-items", type=int, default=6, help="用几个 LoCoMo session 作载体(各注入 1 poison)")
    p.add_argument("--session-key", default="session_1")
    args = p.parse_args()

    locomo = json.loads(Path(args.locomo_path).read_text(encoding="utf-8"))
    suite = json.loads(Path(args.suite).read_text(encoding="utf-8"))["items"]
    items = build_items(locomo, suite, args.n_items, args.session_key)
    if args.item_limit:
        items = items[:args.item_limit]
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    backend = LoCoMoPoisonBackend(args)

    if args.dry_run:
        print(json.dumps({"dry_run": True, "carrier": "locomo_public", "n_items": len(items),
                          "avg_carrier_turns": round(sum(len(it["locomo_turns"]) for it in items) / max(1, len(items)), 1),
                          "passes": args.passes,
                          "note": "载体=LoCoMo 真实对话; poison 注入其中段. 先 --n-items 2 --passes 0 1 smoke."},
                         ensure_ascii=False, indent=2))
        return 0

    raw = backend.run_all(items, args.passes, args.seed, output_dir)
    id_to_item = {it["id"]: it for it in items}
    rng = np.random.default_rng(args.seed)
    conditions, item_rows = [], []
    for n in args.passes:
        flags = {k: [] for k in ("trigger_survival", "payload_survival", "payload_laundered", "rtr_at_k")}
        for item_id, outs in raw[n].items():
            it = id_to_item[item_id]
            meas = _measure(it, outs, args.top_k)
            for k in flags:
                flags[k].append(meas[k])
            item_rows.append({"item_id": item_id, "subject": it.get("subject", ""), "passes": n,
                              "carrier": "locomo", "route_mode": args.route_mode, "seed": args.seed,
                              "trigger_phrase": it["trigger_phrase"], "trigger_query": it["trigger_query"],
                              "unsafe_action": it["unsafe_action"], "unsafe_paraphrases": it.get("unsafe_paraphrases", []),
                              "gold_answer": it["gold_answer"], "consolidated_text": outs["consolidated_text"],
                              "retrieved_texts": outs["retrieved_texts"], "answer_text": outs["answer_text"], "lexical": meas})
        conditions.append({"passes": n, "n_items": len(raw[n]),
                           "metrics": {k: _bootstrap(v, rng, args.bootstrap) for k, v in flags.items()}})

    report_id = args.report_id or f"rq1_agentpoison_locomo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    report = {"report_id": report_id, "generated_at": datetime.now().isoformat(timespec="seconds"),
              "backend": "tiermem", "carrier": "locomo_public", "seed": args.seed, "n_items": len(items),
              "passes": args.passes, "conditions": conditions}
    (output_dir / f"{report_id}.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / f"{report_id}.md").write_text(_render_md(report), encoding="utf-8")
    (output_dir / f"{report_id}_items.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in item_rows) + "\n", encoding="utf-8")
    print(json.dumps({"report_id": report_id, "carrier": "locomo_public", "n_items": len(items),
                      "report_md": str(output_dir / f"{report_id}.md")}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
