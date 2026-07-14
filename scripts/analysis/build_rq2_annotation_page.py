#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a self-contained RQ2 human-annotation page from the DEDUP tables.

RQ2's `human_label` is empty across all annotation CSVs, so RQ2 has no Cohen's κ
and its "hallucination" conclusions have no human backing. This produces ONE
offline HTML file (data inlined, no external deps, no network) where a human fills
`human_label` per item, then exports a filled CSV/JSON and sees a live κ
(machine auto_label vs human) — the RQ1 κ=0.85 workflow, ported to RQ2.

Design choices tied to the eval-methodology audit:
  * dedup tables only (avoid inflating effective n with near-duplicate items).
  * machine auto_label is HIDDEN by default per item (click to reveal) so the
    human judges independently first — blunts same-source anchoring.
  * an explicit "存疑/unsure" option is kept and excluded from κ (opt-out signal).

Usage:
  python scripts/analysis/build_rq2_annotation_page.py \
      --out state/rq2_annotation_page.html
  # optional: --datasets core,diverse   (default both)
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / "state"

# (label, dedup csv, source json with auto_label + memory_summary + consolidated_text)
DATASETS = {
    "core": (
        STATE / "rq2_manual_annotation_core_zh_dedup.csv",
        STATE / "rq2_manual_annotation_core_zh.json",
    ),
    "diverse": (
        STATE / "rq2_manual_annotation_v4_tiermem_diverse_zh_dedup.csv",
        STATE / "rq2_manual_annotation_v4_tiermem_zh.json",  # dedup uids live in the full v4 json
    ),
}

# fields shown on each card (pulled from the dedup csv)
CSV_FIELDS = [
    "index", "uid", "family_zh", "title_zh", "query_mode_zh", "question_zh",
    "true_v_zh", "false_v_zh", "answer", "auto_label_zh",
    "covered_conditions", "dedup_group_size", "duplicate_count",
    "selection_reason_zh", "report_id",
]


def _load_json_index(path: Path) -> dict[str, dict[str, Any]]:
    """uid -> {auto_label, memory_summary_zh, consolidated_text} from a source json."""
    if not path.exists():
        return {}
    try:
        items = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    if not isinstance(items, list):
        return {}
    out: dict[str, dict[str, Any]] = {}
    for it in items:
        uid = it.get("uid")
        if uid:
            out[uid] = {
                "auto_label": it.get("auto_label", ""),
                "memory_summary_zh": it.get("memory_summary_zh", ""),
                "consolidated_text": it.get("consolidated_text", ""),
            }
    return out


def _collect(datasets: list[str]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for name in datasets:
        csv_path, json_path = DATASETS[name]
        if not csv_path.exists():
            print(f"[skip] missing {csv_path}")
            continue
        jidx = _load_json_index(json_path)
        with csv_path.open(encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                uid = row.get("uid", "")
                extra = jidx.get(uid, {})
                rec: dict[str, Any] = {"dataset": name}
                for k in CSV_FIELDS:
                    if k in row:
                        rec[k] = row.get(k, "")
                # normalize machine label to TRUE / FALSE / "" -- auto_label is TRI-state
                # (TRUE=答对, FALSE_BELIEF=信了假记忆, OTHER/其他难判). OTHER is not
                # machine-scorable so it is excluded from κ (the human still labels it).
                raw_auto = str(extra.get("auto_label") or "").upper()
                z = row.get("auto_label_zh", "")
                if raw_auto == "TRUE" or "对" in z:
                    auto = "TRUE"
                elif raw_auto in ("FALSE_BELIEF", "FALSE") or "错" in z or "假" in z or "乱" in z:
                    auto = "FALSE"
                else:  # OTHER / 其他难判
                    auto = ""
                rec["auto_label"] = auto
                rec["auto_label_raw"] = str(extra.get("auto_label") or row.get("auto_label_zh", ""))
                rec["memory_summary_zh"] = extra.get("memory_summary_zh", "")
                rec["consolidated_text"] = extra.get("consolidated_text", "")
                records.append(rec)
    return records


PAGE_TEMPLATE = r"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RQ2 人工标注 · 假记忆采信</title>
<style>
  :root{ --bg:#0f1115; --card:#1a1d24; --ink:#e8eaed; --mut:#9aa0aa; --line:#2b303a;
         --ok:#2ea043; --bad:#e5534b; --uns:#b08800; --acc:#4d8bf0; }
  *{ box-sizing:border-box; }
  body{ margin:0; font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC",sans-serif;
        background:var(--bg); color:var(--ink); }
  header{ position:sticky; top:0; z-index:10; background:#0f1115ee; backdrop-filter:blur(6px);
          border-bottom:1px solid var(--line); padding:12px 20px; }
  .bar{ display:flex; align-items:center; gap:16px; flex-wrap:wrap; }
  h1{ font-size:16px; margin:0; font-weight:600; }
  .prog{ flex:1; min-width:160px; height:8px; background:var(--line); border-radius:6px; overflow:hidden; }
  .prog > i{ display:block; height:100%; width:0; background:var(--acc); transition:width .2s; }
  .stat{ color:var(--mut); font-size:13px; white-space:nowrap; }
  .kappa{ font-size:13px; padding:3px 10px; border:1px solid var(--line); border-radius:6px; }
  button{ font:inherit; color:var(--ink); background:#232833; border:1px solid var(--line);
          border-radius:8px; padding:6px 12px; cursor:pointer; }
  button:hover{ border-color:var(--acc); }
  .wrap{ max-width:860px; margin:0 auto; padding:20px; }
  .card{ background:var(--card); border:1px solid var(--line); border-radius:12px; padding:18px 20px;
         margin:0 0 18px; scroll-margin-top:80px; }
  .card.done{ border-color:#2f4f34; }
  .meta{ color:var(--mut); font-size:12px; display:flex; gap:10px; flex-wrap:wrap; margin-bottom:8px; }
  .tag{ background:#232833; border-radius:5px; padding:1px 8px; }
  .q{ font-size:16px; font-weight:600; margin:6px 0 12px; }
  .vals{ display:flex; gap:10px; flex-wrap:wrap; margin-bottom:10px; }
  .val{ flex:1; min-width:180px; border:1px solid var(--line); border-radius:8px; padding:8px 12px; }
  .val .lab{ font-size:11px; color:var(--mut); }
  .val.t{ border-left:3px solid var(--ok); }
  .val.f{ border-left:3px solid var(--bad); }
  .ans{ background:#12151b; border:1px solid var(--line); border-radius:8px; padding:10px 14px;
        margin:10px 0; white-space:pre-wrap; }
  .ans .lab{ font-size:11px; color:var(--mut); display:block; margin-bottom:4px; }
  details{ margin:8px 0; }
  summary{ cursor:pointer; color:var(--acc); font-size:13px; }
  pre{ white-space:pre-wrap; word-break:break-word; background:#0c0e12; border:1px solid var(--line);
       border-radius:8px; padding:10px; font-size:12px; color:var(--mut); max-height:340px; overflow:auto; }
  .choices{ display:flex; gap:10px; margin-top:12px; flex-wrap:wrap; }
  .choices button{ flex:1; min-width:120px; padding:10px; font-weight:600; }
  .choices button.sel-ok{ background:var(--ok); border-color:var(--ok); color:#fff; }
  .choices button.sel-bad{ background:var(--bad); border-color:var(--bad); color:#fff; }
  .choices button.sel-uns{ background:var(--uns); border-color:var(--uns); color:#fff; }
  .reveal{ margin-top:10px; font-size:13px; color:var(--mut); }
  .reveal b.t{ color:var(--ok); } .reveal b.f{ color:var(--bad); }
  textarea{ width:100%; margin-top:8px; background:#12151b; color:var(--ink); border:1px solid var(--line);
            border-radius:8px; padding:8px; font:inherit; resize:vertical; }
  .hint{ color:var(--mut); font-size:12px; margin:4px 0 14px; }
  .done-badge{ float:right; color:var(--ok); font-size:12px; }
</style>
</head>
<body>
<header>
  <div class="bar">
    <h1>RQ2 人工标注 · 系统回答是否采信了假记忆</h1>
    <div class="prog"><i id="pbar"></i></div>
    <span class="stat" id="pstat">0 / 0</span>
    <span class="kappa" id="kappa">κ: —</span>
    <button id="exp">导出 CSV</button>
    <button id="expj">导出 JSON</button>
    <button id="rst">清空</button>
  </div>
  <div class="hint">快捷键：<b>1</b>=答对　<b>2</b>=答错(采信假记忆)　<b>3</b>=存疑(不计入κ)　<b>↑/↓</b>或<b>j/k</b>=上/下一条。进度自动保存在本机浏览器。</div>
</header>
<div class="wrap" id="list"></div>

<script>
const DATA = __DATA__;
const LSKEY = "rq2_annot_v1";
let store = {};
try { store = JSON.parse(localStorage.getItem(LSKEY) || "{}"); } catch(e){ store = {}; }

const esc = s => (s==null?"":String(s)).replace(/[&<>]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));
const list = document.getElementById("list");

function labelClass(v){ return v==="correct"?"sel-ok":v==="wrong"?"sel-bad":v==="unsure"?"sel-uns":""; }

function render(){
  list.innerHTML = "";
  DATA.forEach((it, i) => {
    const cur = (store[it.uid] && store[it.uid].label) || "";
    const note = (store[it.uid] && store[it.uid].notes) || "";
    const card = document.createElement("div");
    card.className = "card" + (cur ? " done" : "");
    card.id = "c"+i;
    card.innerHTML = `
      <div class="meta">
        <span class="tag">#${i+1}</span>
        <span class="tag">${esc(it.dataset)}</span>
        <span class="tag">${esc(it.family_zh)}</span>
        <span class="tag">${esc(it.query_mode_zh||"")}</span>
        ${it.dedup_group_size?`<span class="tag">代表 ${esc(it.dedup_group_size)} 条重复</span>`:""}
        ${cur?`<span class="done-badge">已标</span>`:""}
      </div>
      <div class="q">${esc(it.title_zh)}：${esc(it.question_zh)}</div>
      <div class="vals">
        <div class="val t"><div class="lab">正确值</div>${esc(it.true_v_zh)}</div>
        <div class="val f"><div class="lab">诱导错误值（假记忆）</div>${esc(it.false_v_zh)}</div>
      </div>
      <div class="ans"><span class="lab">系统回答</span>${esc(it.answer)}</div>
      ${it.memory_summary_zh?`<details><summary>这条样本的记忆是怎么构造的</summary><pre>${esc(it.memory_summary_zh)}</pre></details>`:""}
      ${it.consolidated_text?`<details><summary>完整固化上下文（判断依据）</summary><pre>${esc(it.consolidated_text)}</pre></details>`:""}
      <div class="choices">
        <button data-i="${i}" data-v="correct" class="${cur==="correct"?"sel-ok":""}">✓ 答对（用了正确值）</button>
        <button data-i="${i}" data-v="wrong" class="${cur==="wrong"?"sel-bad":""}">✗ 答错（采信假记忆/乱编）</button>
        <button data-i="${i}" data-v="unsure" class="${cur==="unsure"?"sel-uns":""}">? 存疑</button>
      </div>
      <details class="reveal"><summary>标完后查看机器判定（避免锚定，先自己判）</summary>
        <div class="reveal">机器判定：<b class="${it.auto_label==='TRUE'?'t':it.auto_label==='FALSE'?'f':''}">${esc(it.auto_label_raw||"?")}</b>${it.auto_label?"":"（其他/难判，不计入 κ）"}</div>
      </details>
      <textarea data-i="${i}" rows="1" placeholder="备注（可选）">${esc(note)}</textarea>
    `;
    list.appendChild(card);
  });
  bind(); update();
}

function setLabel(i, v){
  const it = DATA[i];
  store[it.uid] = Object.assign({}, store[it.uid], {label:v, index:it.index, dataset:it.dataset, auto:it.auto_label});
  persist();
  const card = document.getElementById("c"+i);
  card.classList.add("done");
  card.querySelectorAll(".choices button").forEach(b=>{
    b.className = b.dataset.v===v ? labelClass(v) : "";
  });
  if(!card.querySelector(".done-badge")){
    const m = card.querySelector(".meta");
    const s = document.createElement("span"); s.className="done-badge"; s.textContent="已标"; m.appendChild(s);
  }
  update();
  const nxt = document.getElementById("c"+(i+1));
  if(nxt) nxt.scrollIntoView({behavior:"smooth", block:"start"});
}

function bind(){
  list.querySelectorAll(".choices button").forEach(b=>{
    b.onclick = () => setLabel(+b.dataset.i, b.dataset.v);
  });
  list.querySelectorAll("textarea").forEach(t=>{
    t.oninput = () => { const it=DATA[+t.dataset.i]; store[it.uid]=Object.assign({},store[it.uid],{notes:t.value}); persist(); };
  });
}

function persist(){ localStorage.setItem(LSKEY, JSON.stringify(store)); }

function update(){
  const n = DATA.length;
  const done = DATA.filter(it => store[it.uid] && store[it.uid].label).length;
  document.getElementById("pstat").textContent = `${done} / ${n}`;
  document.getElementById("pbar").style.width = (100*done/n).toFixed(1)+"%";
  document.getElementById("kappa").textContent = "κ: " + computeKappa();
}

function computeKappa(){
  // machine=1 if auto_label==FALSE (answered wrong / took the fake); human=1 if label==wrong.
  let a=0,b=0,c=0,d=0,n=0;
  DATA.forEach(it=>{
    const s = store[it.uid];
    if(!s || !s.label || s.label==="unsure") return;
    if(!it.auto_label) return;
    const m = it.auto_label==="FALSE" ? 1 : 0;
    const h = s.label==="wrong" ? 1 : 0;
    n++;
    if(m&&h)a++; else if(m&&!h)b++; else if(!m&&h)c++; else d++;
  });
  if(n===0) return "— (0)";
  const po=(a+d)/n, pM=(a+b)/n, pH=(a+c)/n, pe=pM*pH+(1-pM)*(1-pH);
  const k = (1-pe)>0 ? (po-pe)/(1-pe) : 1;
  return k.toFixed(3)+` (n=${n}, 不一致${b+c})`;
}

function exportCSV(){
  const cols=["dataset","index","uid","auto_label","human_label","notes"];
  const rows=[cols.join(",")];
  DATA.forEach(it=>{
    const s=store[it.uid]||{};
    const hl = s.label==="correct"?"TRUE":s.label==="wrong"?"FALSE":s.label==="unsure"?"UNSURE":"";
    const vals=[it.dataset,it.index,it.uid,it.auto_label,hl,(s.notes||"").replace(/"/g,'""')];
    rows.push(vals.map(v=>/[",\n]/.test(String(v))?`"${v}"`:String(v)).join(","));
  });
  dl("rq2_human_labels.csv", rows.join("\n"), "text/csv");
}
function exportJSON(){
  const out=DATA.map(it=>{ const s=store[it.uid]||{}; return {dataset:it.dataset,index:it.index,uid:it.uid,auto_label:it.auto_label,human_label:s.label||"",notes:s.notes||""}; });
  dl("rq2_human_labels.json", JSON.stringify(out,null,1), "application/json");
}
function dl(name, text, type){
  const blob=new Blob([text],{type}); const url=URL.createObjectURL(blob);
  const a=document.createElement("a"); a.href=url; a.download=name; a.click(); URL.revokeObjectURL(url);
}

document.getElementById("exp").onclick=exportCSV;
document.getElementById("expj").onclick=exportJSON;
document.getElementById("rst").onclick=()=>{ if(confirm("清空所有标注？")){ store={}; persist(); render(); } };

let focus=0;
document.addEventListener("keydown", e=>{
  if(e.target.tagName==="TEXTAREA") return;
  if(["1","2","3"].includes(e.key)){ setLabel(focus, {"1":"correct","2":"wrong","3":"unsure"}[e.key]); e.preventDefault(); }
  else if(e.key==="ArrowDown"||e.key==="j"){ focus=Math.min(DATA.length-1,focus+1); document.getElementById("c"+focus).scrollIntoView({behavior:"smooth",block:"start"}); }
  else if(e.key==="ArrowUp"||e.key==="k"){ focus=Math.max(0,focus-1); document.getElementById("c"+focus).scrollIntoView({behavior:"smooth",block:"start"}); }
});
// track which card is centered for keyboard labeling
const io=new IntersectionObserver(es=>{ es.forEach(en=>{ if(en.isIntersecting) focus=+en.target.id.slice(1); }); },{rootMargin:"-45% 0px -45% 0px"});

render();
DATA.forEach((_,i)=>io.observe(document.getElementById("c"+i)));
</script>
</body>
</html>
"""


def build(datasets: list[str], out: Path) -> int:
    records = _collect(datasets)
    if not records:
        print("no records collected; check dedup csv paths")
        return 1
    payload = json.dumps(records, ensure_ascii=False).replace("</", "<\\/")
    html = PAGE_TEMPLATE.replace("__DATA__", payload)
    out.write_text(html, encoding="utf-8")
    n_auto = sum(1 for r in records if r.get("auto_label"))
    by_ds: dict[str, int] = {}
    for r in records:
        by_ds[r["dataset"]] = by_ds.get(r["dataset"], 0) + 1
    print(json.dumps({
        "items": len(records), "by_dataset": by_ds,
        "with_machine_auto_label": n_auto, "output": str(out),
        "size_kb": round(out.stat().st_size / 1024, 1),
    }, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Build RQ2 human-annotation HTML page.")
    ap.add_argument("--datasets", default="core,diverse", help="comma list of: " + ",".join(DATASETS))
    ap.add_argument("--out", default=str(STATE / "rq2_annotation_page.html"))
    args = ap.parse_args()
    ds = [d.strip() for d in args.datasets.split(",") if d.strip() in DATASETS]
    return build(ds, Path(args.out).expanduser())


if __name__ == "__main__":
    raise SystemExit(main())
