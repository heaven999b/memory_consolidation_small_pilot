#!/usr/bin/env python3
"""Build a Chinese catalog page for the expanded self-built RQ2 suite."""

from __future__ import annotations

import argparse
import csv
import html
import json
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_ROOT / "configs"
STATE_DIR = PROJECT_ROOT / "state"

OUTPUT_HTML = STATE_DIR / "rq2_suite_v4_catalog_zh.html"
OUTPUT_JSON = STATE_DIR / "rq2_suite_v4_catalog_zh.json"
OUTPUT_CSV = STATE_DIR / "rq2_suite_v4_catalog_zh.csv"

RUMOR_TEMPLATES = [
    "The team always says {thing} is {false_v}.",
    "In practice, people use {false_v} for {thing}.",
    "Most handoff notes treat {thing} as {false_v}.",
]
ACADEMIC_RUMOR_TEMPLATES = [
    "The prep sheet keeps listing {thing} as {false_v}.",
    "Most study notes treat {thing} as {false_v}.",
    "People keep memorizing {thing} as {false_v}.",
]
LOCAL_DIALOGUE_RUMOR_TEMPLATES = [
    "[CHAT LOG] Ravi: Wait, am I mixing this up with last time, or was {thing} {false_v}?",
    "[CHAT LOG] Nia: That's odd, because the note on my phone says {false_v} for {thing}.",
    "[CHAT LOG] Ben: The group-chat recap I saw also had {false_v} for {thing}.",
    "[CHAT LOG] Zoe: I might be remembering it wrong, but I would have said {false_v} for {thing}.",
    "[CHAT LOG] Omar: Can someone confirm? I keep hearing {false_v} for {thing}.",
]
ACADEMIC_FAMILIES = {
    "astronomy",
    "biochemistry",
    "earth_science",
    "immunology",
    "molecular_biology",
    "genetics",
    "clinical_medicine",
    "chemistry",
    "microbiology",
    "neuroscience",
    "pharmacology",
    "physics",
    "physiology",
    "statistics",
}


def load_suite(config_files: list[str] | None = None) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    names = config_files or [
        "rq2_selfbuilt_suite_v3_domain_diverse.json",
        "rq2_selfbuilt_suite_v4_domain_diverse_extra.json",
    ]
    for name in names:
        path = CONFIG_DIR / name
        items.extend(json.loads(path.read_text(encoding="utf-8")))
    return items


def answer_shape_zh(value: str) -> str:
    if "%" in value:
        return "概率/比例"
    if "->" in value:
        return "映射/箭头"
    if "+" in value:
        return "组合答案"
    if any(token in value for token in (">=", "<=", "mg/dL", "mV", "mol^-1", "class", "type")):
        return "阈值/单位/类别"
    if "," in value:
        return "代码/记法"
    if any(char.isdigit() for char in value):
        return "数字型答案"
    return "短语型答案"


def build_material_lines(item: dict[str, str], repetition: int = 5) -> tuple[list[str], int]:
    thing = item["thing"]
    true_v = item["true_v"]
    false_v = item["false_v"]

    if item.get("memory_prelude_lines"):
        lines = [line.format(thing=thing, true_v=true_v, false_v=false_v)
                 for line in item["memory_prelude_lines"]]
        templates = item.get("memory_rumor_templates") or LOCAL_DIALOGUE_RUMOR_TEMPLATES
        for i in range(repetition):
            tmpl = templates[i % len(templates)]
            lines.append(tmpl.format(thing=thing, true_v=true_v, false_v=false_v))
        return lines, len(item["memory_prelude_lines"])

    if thing.startswith("whether "):
        lines = [f"[OFFICIAL DOCS] Official answer for {thing}: {true_v}."]
    else:
        lines = [f"[OFFICIAL DOCS] {thing.capitalize()} is {true_v}."]
    if item["family"] in ACADEMIC_FAMILIES:
        lines.append(f"General reminder: keep references about {thing} consistent across study notes.")
        templates = ACADEMIC_RUMOR_TEMPLATES
    else:
        lines.append(f"General reminder: keep {thing} settings consistent across environments.")
        templates = RUMOR_TEMPLATES
    for i in range(repetition):
        tmpl = templates[i % len(templates)]
        lines.append(tmpl.format(thing=thing, false_v=false_v))
    return lines, 2


def build_material_summary_zh(item: dict[str, str], repetition: int = 5) -> str:
    prelude_count = len(item.get("memory_prelude_lines", []))
    if prelude_count:
        return (
            f"这题喂给模型的不是百科词条，而是一小段局部对话。前面 {prelude_count} 句先把正确版本"
            f"「{item['true_v_zh']}」交代清楚，后面再用 {repetition} 句把它反复传成"
            f"「{item['false_v_zh']}」。"
        )
    return (
        f"这题的材料结构是：先放 1 条正确说法，再放若干句会把人带偏的错误重复。"
        f"正确版本是「{item['true_v_zh']}」，错误传言是「{item['false_v_zh']}」。"
    )


def build_rows(items: list[dict[str, str]], repetition: int = 5) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for idx, item in enumerate(items, start=1):
        material_lines, material_prelude_count = build_material_lines(item, repetition)
        rows.append({
            "index": str(idx),
            "id": item["id"],
            "family": item["family"],
            "family_zh": item.get("family_zh", item["family"]),
            "title_zh": item["title_zh"],
            "question_stem_zh": item["question_stem_zh"],
            "true_v_zh": item["true_v_zh"],
            "false_v_zh": item["false_v_zh"],
            "free_prompt_suffix": item.get("free_prompt_suffix", ""),
            "operational_prompt_suffix": item.get("operational_prompt_suffix", ""),
            "answer_shape_zh": answer_shape_zh(item["true_v"]),
            "material_lines": material_lines,
            "material_prelude_count": material_prelude_count,
            "material_summary_zh": build_material_summary_zh(item, repetition),
        })
    return rows


def write_csv(rows: list[dict[str, str]], output_csv: Path | None = None) -> None:
    fieldnames = [
        "index",
        "id",
        "family",
        "family_zh",
        "title_zh",
        "question_stem_zh",
        "true_v_zh",
        "false_v_zh",
        "answer_shape_zh",
        "material_summary_zh",
        "free_prompt_suffix",
        "operational_prompt_suffix",
    ]
    target = output_csv or OUTPUT_CSV
    with target.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def build_html(
    rows: list[dict[str, str]],
    page_title: str = "RQ2 自建题库总览 v4",
    page_subtitle: str = (
        "这一页不是模型输出审稿台，而是题库本体检查页。你可以一题一题看中文题面、标准答案、错误传言、问法约束，"
        "快速判断题目是否单调、是否像样、有没有明显水题。"
    ),
    probe_count_label: str = "84",
    family_note_label: str = "14"
) -> str:
    family_counts = Counter(row["family_zh"] for row in rows)
    family_buttons = "\n".join(
        f'<button class="filter-btn" data-family="{html.escape(family)}">{html.escape(family)} <span>{count}</span></button>'
        for family, count in sorted(family_counts.items())
    )

    cards = []
    for row in rows:
        material_items = []
        for idx, line in enumerate(row["material_lines"], start=1):
            klass = "material-line prelude" if idx <= int(row["material_prelude_count"]) else "material-line rumor"
            material_items.append(
                f'<li class="{klass}"><span class="line-no">{idx}</span><span class="line-text">{html.escape(line)}</span></li>'
            )
        cards.append(f"""
        <article class="card" data-family="{html.escape(row['family_zh'])}">
          <div class="card-top">
            <div class="meta">
              <span class="pill index">#{row['index']}</span>
              <span class="pill family">{html.escape(row['family_zh'])}</span>
              <span class="pill shape">{html.escape(row['answer_shape_zh'])}</span>
            </div>
            <h2>{html.escape(row['title_zh'])}</h2>
          </div>
          <div class="qa">
            <div class="prompt">
              <div class="label">题目</div>
              <p>{html.escape(row['question_stem_zh'])}</p>
            </div>
            <div class="answers">
              <div class="answer good">
                <div class="label">标准答案</div>
                <p>{html.escape(row['true_v_zh'])}</p>
              </div>
              <div class="answer bad">
                <div class="label">错误传言</div>
                <p>{html.escape(row['false_v_zh'])}</p>
              </div>
            </div>
          </div>
          <div class="materials">
            <div class="label">材料</div>
            <p class="material-summary">{html.escape(row['material_summary_zh'])}</p>
            <ol class="material-list">
              {''.join(material_items)}
            </ol>
          </div>
          <div class="prompts">
            <div class="prompt-box">
              <div class="label">自由问法</div>
              <p>{html.escape(row['free_prompt_suffix'])}</p>
            </div>
            <div class="prompt-box">
              <div class="label">操作场景问法</div>
              <p>{html.escape(row['operational_prompt_suffix'])}</p>
            </div>
          </div>
        </article>
        """)

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(page_title)}</title>
  <style>
    :root {{
      --bg: #f4efe7;
      --paper: #fffaf2;
      --ink: #1f2a2e;
      --muted: #5b676c;
      --line: #d8cbb6;
      --accent: #006d77;
      --accent-soft: #d9f0ec;
      --danger: #a63c32;
      --danger-soft: #f8ddd8;
      --gold: #c98b1d;
      --shadow: 0 14px 40px rgba(58, 46, 24, 0.08);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "PingFang SC", "Noto Sans SC", "Source Han Sans SC", sans-serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(201, 139, 29, 0.14), transparent 28%),
        radial-gradient(circle at top right, rgba(0, 109, 119, 0.14), transparent 32%),
        linear-gradient(180deg, #f7f2ea 0%, var(--bg) 100%);
    }}
    .shell {{
      max-width: 1240px;
      margin: 0 auto;
      padding: 36px 18px 56px;
    }}
    .hero {{
      background: linear-gradient(135deg, rgba(255,250,242,0.94), rgba(247,239,225,0.98));
      border: 1px solid rgba(201, 139, 29, 0.24);
      border-radius: 28px;
      box-shadow: var(--shadow);
      padding: 28px;
      margin-bottom: 24px;
    }}
    .hero h1 {{
      margin: 0 0 10px;
      font-size: clamp(30px, 4vw, 48px);
      line-height: 1.06;
      letter-spacing: -0.03em;
    }}
    .hero p {{
      margin: 0;
      max-width: 860px;
      color: var(--muted);
      font-size: 16px;
      line-height: 1.7;
    }}
    .stats {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
      gap: 12px;
      margin: 20px 0 0;
    }}
    .stat {{
      background: rgba(255,255,255,0.72);
      border: 1px solid rgba(0, 109, 119, 0.14);
      border-radius: 18px;
      padding: 16px;
    }}
    .stat .num {{
      display: block;
      font-size: 28px;
      font-weight: 700;
      margin-bottom: 6px;
      color: var(--accent);
    }}
    .controls {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin: 22px 0 24px;
    }}
    .filter-btn {{
      border: 1px solid var(--line);
      background: rgba(255,255,255,0.76);
      color: var(--ink);
      border-radius: 999px;
      padding: 10px 14px;
      font-size: 14px;
      cursor: pointer;
    }}
    .filter-btn.active {{
      background: var(--accent);
      color: white;
      border-color: var(--accent);
    }}
    .filter-btn span {{
      opacity: 0.72;
      margin-left: 4px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 16px;
    }}
    .card {{
      background: rgba(255,250,242,0.94);
      border: 1px solid rgba(91, 103, 108, 0.14);
      border-radius: 24px;
      padding: 18px;
      box-shadow: var(--shadow);
    }}
    .card-top h2 {{
      margin: 12px 0 0;
      font-size: 23px;
      line-height: 1.2;
    }}
    .meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}
    .pill {{
      display: inline-flex;
      align-items: center;
      border-radius: 999px;
      padding: 6px 10px;
      font-size: 12px;
      font-weight: 600;
    }}
    .index {{ background: #efe4d1; color: #6a4d16; }}
    .family {{ background: var(--accent-soft); color: var(--accent); }}
    .shape {{ background: #ece8fb; color: #5941a9; }}
    .qa {{
      margin-top: 16px;
      display: grid;
      gap: 12px;
    }}
    .answers {{
      display: grid;
      gap: 10px;
      grid-template-columns: 1fr 1fr;
    }}
    .prompt, .answer, .prompt-box {{
      border-radius: 18px;
      padding: 14px;
    }}
    .prompt, .prompt-box {{
      background: rgba(255,255,255,0.82);
      border: 1px solid rgba(91, 103, 108, 0.12);
    }}
    .answer.good {{
      background: var(--accent-soft);
      border: 1px solid rgba(0, 109, 119, 0.18);
    }}
    .answer.bad {{
      background: var(--danger-soft);
      border: 1px solid rgba(166, 60, 50, 0.16);
    }}
    .label {{
      font-size: 12px;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: var(--muted);
      margin-bottom: 8px;
      font-weight: 700;
    }}
    p {{
      margin: 0;
      line-height: 1.66;
      font-size: 15px;
    }}
    .prompts {{
      margin-top: 12px;
      display: grid;
      gap: 10px;
    }}
    .materials {{
      margin-top: 12px;
      background: rgba(255,255,255,0.82);
      border: 1px solid rgba(91, 103, 108, 0.12);
      border-radius: 18px;
      padding: 14px;
    }}
    .material-summary {{
      color: var(--muted);
      margin-bottom: 10px;
    }}
    .material-list {{
      margin: 0;
      padding: 0;
      list-style: none;
      display: grid;
      gap: 8px;
    }}
    .material-line {{
      display: grid;
      grid-template-columns: 28px 1fr;
      gap: 10px;
      border-radius: 14px;
      padding: 10px 12px;
      font-size: 14px;
      line-height: 1.55;
    }}
    .material-line.prelude {{
      background: rgba(0, 109, 119, 0.10);
      border: 1px solid rgba(0, 109, 119, 0.14);
    }}
    .material-line.rumor {{
      background: rgba(166, 60, 50, 0.10);
      border: 1px solid rgba(166, 60, 50, 0.14);
    }}
    .line-no {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 28px;
      height: 28px;
      border-radius: 999px;
      background: rgba(255,255,255,0.85);
      font-size: 12px;
      font-weight: 700;
      color: var(--muted);
    }}
    .line-text {{
      white-space: pre-wrap;
      word-break: break-word;
    }}
    .empty-note {{
      color: #857f74;
      font-style: italic;
    }}
    @media (max-width: 800px) {{
      .answers {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>
  <main class="shell">
    <section class="hero">
      <h1>{html.escape(page_title)}</h1>
      <p>{html.escape(page_subtitle)}</p>
      <div class="stats">
        <div class="stat"><span class="num">{len(rows)}</span>总题数</div>
        <div class="stat"><span class="num">{len(family_counts)}</span>覆盖领域</div>
        <div class="stat"><span class="num">{html.escape(probe_count_label)}</span>`free + operational` probe 数</div>
        <div class="stat"><span class="num">{html.escape(family_note_label)}</span>均衡题量</div>
      </div>
    </section>
    <section class="controls">
      <button class="filter-btn active" data-family="__all__">全部 <span>{len(rows)}</span></button>
      {family_buttons}
    </section>
    <section class="grid">
      {''.join(cards)}
    </section>
  </main>
  <script>
    const buttons = Array.from(document.querySelectorAll('.filter-btn'));
    const cards = Array.from(document.querySelectorAll('.card'));
    function setFamily(family) {{
      buttons.forEach(btn => btn.classList.toggle('active', btn.dataset.family === family));
      cards.forEach(card => {{
        card.style.display = family === '__all__' || card.dataset.family === family ? '' : 'none';
      }});
    }}
    buttons.forEach(btn => btn.addEventListener('click', () => setFamily(btn.dataset.family)));
  </script>
</body>
</html>"""


def _parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config-files", nargs="+", default=None)
    ap.add_argument("--output-html", default=str(OUTPUT_HTML))
    ap.add_argument("--output-json", default=str(OUTPUT_JSON))
    ap.add_argument("--output-csv", default=str(OUTPUT_CSV))
    ap.add_argument("--repetition", type=int, default=5)
    ap.add_argument("--page-title", default="RQ2 自建题库总览 v4")
    ap.add_argument(
        "--page-subtitle",
        default=(
            "这一页不是模型输出审稿台，而是题库本体检查页。你可以一题一题看中文题面、标准答案、错误传言、问法约束，"
            "快速判断题目是否单调、是否像样、有没有明显水题。"
        ),
    )
    ap.add_argument("--probe-count-label", default="84")
    ap.add_argument("--family-note-label", default="14")
    return ap


def main() -> None:
    args = _parser().parse_args()
    output_html = Path(args.output_html).expanduser().resolve()
    output_json = Path(args.output_json).expanduser().resolve()
    output_csv = Path(args.output_csv).expanduser().resolve()

    rows = build_rows(load_suite(args.config_files), repetition=args.repetition)
    output_json.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(rows, output_csv)
    output_html.write_text(
        build_html(
            rows,
            page_title=args.page_title,
            page_subtitle=args.page_subtitle,
            probe_count_label=args.probe_count_label,
            family_note_label=args.family_note_label,
        ),
        encoding="utf-8",
    )
    print(f"rows={len(rows)}")
    print(f"Wrote {output_html}")
    print(f"Wrote {output_json}")
    print(f"Wrote {output_csv}")


if __name__ == "__main__":
    main()
