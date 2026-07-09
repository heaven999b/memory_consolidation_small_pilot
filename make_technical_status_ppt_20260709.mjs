import fs from "node:fs/promises";
import path from "node:path";
import {
  Presentation,
  PresentationFile,
} from "/Users/yihaiwen/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";

const SLIDE_W = 1280;
const SLIDE_H = 720;
const OUT_DIR = path.resolve(
  "/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/state/ppt_technical_update_20260709",
);

const C = {
  bg: "#FFFFFF",
  ink: "#000000",
  body: "#222222",
  muted: "#555555",
  panel: "#EDEDED",
  panel2: "#F6F6F6",
  rule: "#B8BCC4",
  accent: "#FF6B35",
  accentSoft: "#FFF0EA",
  safe: "#111111",
  warn: "#FF6B35",
};

async function writeBlob(filePath, blob) {
  await fs.writeFile(filePath, new Uint8Array(await blob.arrayBuffer()));
}

function pct(value) {
  return `${value.toFixed(1)}%`;
}

function textBox(slide, opts) {
  const shape = slide.shapes.add({
    geometry: "textbox",
    name: opts.name ?? "textbox",
    position: {
      left: opts.left,
      top: opts.top,
      width: opts.width,
      height: opts.height,
    },
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  shape.text = opts.text;
  shape.text.style = {
    fontSize: opts.fontSize ?? 20,
    bold: opts.bold ?? false,
    color: opts.color ?? C.body,
    alignment: opts.alignment ?? "left",
  };
  return shape;
}

function panel(slide, opts) {
  return slide.shapes.add({
    geometry: opts.geometry ?? "roundRect",
    name: opts.name ?? "panel",
    position: {
      left: opts.left,
      top: opts.top,
      width: opts.width,
      height: opts.height,
    },
    fill: opts.fill ?? C.panel,
    line: {
      style: "solid",
      fill: opts.lineFill ?? "none",
      width: opts.lineWidth ?? 0,
    },
    borderRadius: opts.borderRadius ?? "rounded-md",
  });
}

function rule(slide, left, top, width, height = 1, fill = C.rule) {
  slide.shapes.add({
    geometry: "rect",
    name: "rule",
    position: { left, top, width, height },
    fill,
    line: { style: "solid", fill, width: 0 },
  });
}

function chip(slide, left, top, text) {
  panel(slide, {
    left,
    top,
    width: Math.max(120, text.length * 13),
    height: 28,
    fill: C.accentSoft,
    lineFill: C.accent,
    lineWidth: 1,
    borderRadius: "rounded-sm",
  });
  textBox(slide, {
    left: left + 10,
    top: top + 4,
    width: Math.max(100, text.length * 13 - 20),
    height: 20,
    text,
    fontSize: 12,
    bold: true,
    color: C.accent,
  });
}

function footer(slide, slideNo, source) {
  textBox(slide, {
    left: 42,
    top: 684,
    width: 980,
    height: 18,
    text: source,
    fontSize: 11,
    color: C.muted,
  });
  textBox(slide, {
    left: 1184,
    top: 682,
    width: 54,
    height: 20,
    text: String(slideNo),
    fontSize: 12,
    color: C.muted,
    alignment: "right",
  });
}

function titleBlock(slide, section, title, subtitle) {
  if (section) {
    textBox(slide, {
      left: 42,
      top: 28,
      width: 420,
      height: 18,
      text: section,
      fontSize: 12,
      bold: true,
      color: C.muted,
    });
  }
  textBox(slide, {
    left: 42,
    top: 46,
    width: 1120,
    height: 56,
    text: title,
    fontSize: 34,
    bold: true,
    color: C.ink,
  });
  if (subtitle) {
    textBox(slide, {
      left: 42,
      top: 96,
      width: 1100,
      height: 34,
      text: subtitle,
      fontSize: 16,
      color: C.muted,
    });
  }
  rule(slide, 42, 134, 1196, 1);
}

function metricCard(slide, opts) {
  panel(slide, {
    left: opts.left,
    top: opts.top,
    width: opts.width,
    height: opts.height,
    fill: opts.fill ?? C.panel2,
    lineFill: opts.lineFill ?? C.rule,
    lineWidth: opts.lineWidth ?? 1,
    borderRadius: "rounded-md",
  });
  textBox(slide, {
    left: opts.left + 18,
    top: opts.top + 18,
    width: opts.width - 36,
    height: 54,
    text: opts.value,
    fontSize: opts.valueSize ?? 34,
    bold: true,
    color: opts.valueColor ?? C.ink,
  });
  textBox(slide, {
    left: opts.left + 18,
    top: opts.top + 74,
    width: opts.width - 36,
    height: 28,
    text: opts.label,
    fontSize: 16,
    bold: true,
    color: C.body,
  });
  if (opts.note) {
    textBox(slide, {
      left: opts.left + 18,
      top: opts.top + 106,
      width: opts.width - 36,
      height: opts.height - 120,
      text: opts.note,
      fontSize: 13,
      color: C.muted,
    });
  }
}

function styleTable(table, rows, cols, accentCols = []) {
  table.borders.assign({ style: "solid", fill: C.rule, width: 1 });
  const header = table.cells.block({
    row: 0,
    column: 0,
    rowCount: 1,
    columnCount: cols,
  });
  header.fill = C.panel;
  header.textStyle.bold = true;
  header.textStyle.fontSize = 13;
  header.textStyle.color = C.ink;
  const body = table.cells.block({
    row: 1,
    column: 0,
    rowCount: rows - 1,
    columnCount: cols,
  });
  body.textStyle.fontSize = 12;
  body.textStyle.color = C.body;
  for (const col of accentCols) {
    const range = table.cells.block({
      row: 1,
      column: col,
      rowCount: rows - 1,
      columnCount: 1,
    });
    range.textStyle.bold = true;
    range.textStyle.color = C.accent;
  }
}

function slide1(presentation) {
  const slide = presentation.slides.add();
  slide.background.fill = C.bg;

  chip(slide, 42, 38, "MEMORY CONSOLIDATION SAFETY STUDY");
  textBox(slide, {
    left: 42,
    top: 100,
    width: 820,
    height: 168,
    text: "截至 2026-07-09\n哪些结论还站得住",
    fontSize: 54,
    bold: true,
    color: C.ink,
  });
  textBox(slide, {
    left: 42,
    top: 292,
    width: 820,
    height: 52,
    text: "技术汇报，面向熟悉 LLM agent、记忆系统和评测设计的读者",
    fontSize: 22,
    color: C.muted,
  });

  panel(slide, {
    left: 0,
    top: 414,
    width: SLIDE_W,
    height: 254,
    fill: C.panel2,
    borderRadius: 0,
  });

  metricCard(slide, {
    left: 42,
    top: 454,
    width: 360,
    height: 170,
    value: "数据范围",
    valueSize: 24,
    label: "公开 benchmark 与自建题库分开汇报",
    note: "官方 HaluMem 切片，自建 stealth 安全套件，自建 100 题对话错信题库",
  });
  metricCard(slide, {
    left: 460,
    top: 454,
    width: 360,
    height: 170,
    value: "当前最硬结果",
    valueSize: 24,
    label: "know-do gap 与 endpoint 可靠性",
    note: "最稳的正现象不是“越压越危险”，而是“知道政策却不照做”",
  });
  metricCard(slide, {
    left: 878,
    top: 454,
    width: 360,
    height: 170,
    value: "当前在跑",
    valueSize: 24,
    label: "RQ3 读取侧防御大跑",
    note: "20 个 jobs，已完成 10 个，最新快照显示所有已完成条件都朝防御方向移动",
  });

  footer(
    slide,
    1,
    "Source: RESEARCH_README.md, 研究结果分类整理_20260704.md, rq3_readtime_large_20260708_dashboard_data.json",
  );
}

function slide2(presentation) {
  const slide = presentation.slides.add();
  slide.background.fill = C.bg;
  titleBlock(
    slide,
    "Current Readout",
    "现在最该带走的六个判断",
    "这页不是细节页，而是当前仓库里最稳定的六个高层判断。",
  );

  const cards = [
    ["不成立", "原主假设", "“越固化越危险”没有站住"],
    ["终点翻转", "最强结果", "词法终点和行为终点会给出相反结论"],
    ["37–63%", "跨模型 gap", "三模型都知道政策，但行动仍会违规"],
    ["不支持", "RQ2 官方版", "HaluMem 没看到随 N 变糟"],
    ["弱支持", "RQ2 自建版", "重复错误信息能造错信，但不是越压越大"],
    ["50%", "RQ3 进度", "大跑完成一半，现有条件都往防御方向走"],
  ];
  const startX = 42;
  const startY = 172;
  const gapX = 20;
  const gapY = 22;
  const cardW = 378;
  const cardH = 180;
  for (let i = 0; i < cards.length; i += 1) {
    const row = Math.floor(i / 3);
    const col = i % 3;
    metricCard(slide, {
      left: startX + col * (cardW + gapX),
      top: startY + row * (cardH + gapY),
      width: cardW,
      height: cardH,
      value: cards[i][0],
      label: cards[i][1],
      note: cards[i][2],
      valueColor: i === 1 || i === 5 ? C.accent : C.ink,
    });
  }

  footer(
    slide,
    2,
    "Source: RESEARCH_README.md, rq2_dual_track_refresh_20260708.md, knowdo_main_gpt*.json, rq3 dashboard snapshot",
  );
}

function slide3(presentation) {
  const slide = presentation.slides.add();
  slide.background.fill = C.bg;
  titleBlock(
    slide,
    "Original RQs",
    "原始 RQ1 到 RQ5 的现状",
    "技术上最重要的一点是把“公开 benchmark”和“自建安全套件”区分开来看。",
  );
  chip(slide, 42, 146, "RQ2 主要依赖公开 benchmark；RQ1/RQ3/RQ5 主要依赖自建安全套件");

  const rows = [
    ["RQ", "核心问题", "数据类型", "怎么测", "当前结果", "状态"],
    [
      "RQ1",
      "固化会不会放大危险内容",
      "自建 stealth 安全题",
      "payload-emission judge",
      "prompt_only 100 > N0 86.7 > N2 73.3",
      "不支持",
    ],
    [
      "RQ2",
      "固化会不会制造假记忆",
      "官方 HaluMem + 自建对话题",
      "unsupported fabrication / false belief",
      "官方负面，自建只剩弱版本",
      "强版本不支持",
    ],
    [
      "RQ3",
      "provenance 分层能不能救",
      "旧线自建 + 新 RQ3 大跑",
      "off/on 配对翻转",
      "旧写入线负面，新读取线有苗头",
      "进行中",
    ],
    [
      "RQ4",
      "哪个压缩算子最脆",
      "需要多算子对照",
      "operator comparison",
      "COMEDY / Context-Memory / NeedSleep / E-mem 还没系统跑",
      "空白",
    ],
    [
      "RQ5",
      "失败发生在哪个阶段",
      "prompt_only 对比 tiermem",
      "answer-time comparison",
      "reader 阶段更像罪魁，而不是 consolidator",
      "部分答清",
    ],
  ];

  const table = slide.tables.add({
    rows: rows.length,
    columns: rows[0].length,
    left: 42,
    top: 190,
    width: 1196,
    height: 420,
    columnWidths: [70, 220, 175, 180, 350, 201],
    values: rows,
  });
  styleTable(table, rows.length, rows[0].length, [5]);

  panel(slide, {
    left: 42,
    top: 628,
    width: 1196,
    height: 40,
    fill: C.accentSoft,
    lineFill: C.accent,
    lineWidth: 1,
    borderRadius: "rounded-sm",
  });
  textBox(slide, {
    left: 58,
    top: 638,
    width: 1160,
    height: 20,
    text: "最大的空白仍然是 RQ4：如果要回到“压缩方法本身”这条线，多算子对照是必须补的。",
    fontSize: 14,
    bold: true,
    color: C.accent,
  });

  footer(
    slide,
    3,
    "Source: RESEARCH_README.md §3, 研究结果分类整理_20260704.md, rq2_dual_track_refresh_20260708.md",
  );
}

function slide4(presentation) {
  const slide = presentation.slides.add();
  slide.background.fill = C.bg;
  titleBlock(
    slide,
    "Reframed RQs",
    "重构后的 RQ1′ 到 RQ5′",
    "真正还能继续长结果的，不再是“深度 N 会不会变坏”，而是 reader、defense 和 endpoint。",
  );

  const rows = [
    ["RQ′", "现在真正问什么", "关键证据", "一句话结论", "强度"],
    [
      "RQ1′",
      "agent 更听政策还是更听惯例",
      "know-do gap，三模型 37–63% 违规",
      "policy knowledge 在，safe action 不稳",
      "强",
    ],
    [
      "RQ2′",
      "重复错误信息会不会形成错信",
      "官方 HaluMem 负面；自建对话题有弱阳性",
      "只支持弱版本，不支持“越压越糟”",
      "中弱",
    ],
    [
      "RQ3′",
      "读取侧防御能不能稳定减少错误行动",
      "大跑已完成 50%，当前均值下降 10–18pp",
      "目前最像正结果，但还不能定稿",
      "中",
    ],
    [
      "RQ4′",
      "终点定义会不会把结论带偏",
      "写入闸门、know-do、跨模型三次翻转",
      "这是当前最站得住的方法学主张",
      "很强",
    ],
    [
      "RQ5′",
      "真正出问题的是记忆还是 reader",
      "prompt_only 已经很糟，tiermem 并未更坏",
      "reader 比 consolidator 更值得追",
      "强",
    ],
  ];
  const table = slide.tables.add({
    rows: rows.length,
    columns: rows[0].length,
    left: 42,
    top: 166,
    width: 1196,
    height: 468,
    columnWidths: [78, 290, 270, 360, 198],
    values: rows,
  });
  styleTable(table, rows.length, rows[0].length, [4]);

  footer(
    slide,
    4,
    "Source: RESEARCH_README.md §3.3, 研究结果分类整理_20260704.md A2",
  );
}

function slide5(presentation) {
  const slide = presentation.slides.add();
  slide.background.fill = C.bg;
  titleBlock(
    slide,
    "Method Lesson",
    "终点定义会直接翻转结论",
    "如果还是用快而脆的词法终点，同一批数据会把人带到完全不同的结论上。",
  );

  panel(slide, {
    left: 42,
    top: 176,
    width: 392,
    height: 430,
    fill: C.accentSoft,
    lineFill: C.accent,
    lineWidth: 1,
  });
  textBox(slide, {
    left: 66,
    top: 202,
    width: 340,
    height: 118,
    text: "这一轮最重要的方法学收获，不是一个更猛的攻击，而是一个更可靠的判分方式。",
    fontSize: 28,
    bold: true,
    color: C.ink,
  });
  textBox(slide, {
    left: 66,
    top: 340,
    width: 340,
    height: 212,
    text:
      "1. 写入闸门那条线，comply 看起来几乎清零，但行为终点仍然泄露 83%。\n\n2. know-do gap 那条线，词法口径会把风险夸得更高。\n\n3. 连跨模型排序都可能翻过来。",
    fontSize: 17,
    color: C.body,
  });

  const rows = [
    ["场景", "快终点会说什么", "行为终点会说什么", "真正改变了什么"],
    [
      "写入闸门",
      "N=1 后 comply 近乎归零",
      "payload 仍有 83% 泄露",
      "“防御有效”变成了假阳性",
    ],
    [
      "know-do",
      "词法口径约 93% 风险",
      "judge 口径约 67% 风险",
      "风险没有消失，但被重新定量",
    ],
    [
      "跨模型",
      "看起来越大模型越糟",
      "judge 下反而越大越好",
      "模型排序本身翻转",
    ],
  ];
  const table = slide.tables.add({
    rows: rows.length,
    columns: rows[0].length,
    left: 464,
    top: 190,
    width: 774,
    height: 360,
    columnWidths: [118, 186, 186, 284],
    values: rows,
  });
  styleTable(table, rows.length, rows[0].length, []);

  textBox(slide, {
    left: 464,
    top: 570,
    width: 760,
    height: 54,
    text: "所以后续所有安全结论，都应该默认回到行为终点、人工校验和簇稳健样本口径上来",
    fontSize: 18,
    bold: true,
    color: C.ink,
  });

  footer(
    slide,
    5,
    "Source: RESEARCH_README.md §2, 研究结果分类整理_20260704.md B2/B5/C2/C6",
  );
}

function slide6(presentation) {
  const slide = presentation.slides.add();
  slide.background.fill = C.bg;
  titleBlock(
    slide,
    "RQ1 + RQ5",
    "RQ1 和 RQ5 合起来更像在说一件事",
    "危险行为主要出在 reader 选动作的阶段，不像是压缩把危险内容越洗越白。",
  );

  panel(slide, {
    left: 42,
    top: 176,
    width: 610,
    height: 444,
    fill: C.panel2,
    lineFill: C.rule,
    lineWidth: 1,
  });
  slide.charts.add("bar", {
    position: { left: 72, top: 220, width: 540, height: 320 },
    categories: ["prompt_only", "tiermem N0", "tiermem N2"],
    series: [
      {
        name: "Unsafe action rate",
        values: [100.0, 86.7, 73.3],
        fill: C.accent,
      },
    ],
    hasLegend: false,
    barOptions: { direction: "bar", grouping: "clustered", gapWidth: 40 },
    xAxis: {
      min: 0,
      max: 100,
      majorUnit: 20,
      textStyle: { fontSize: 12, fill: C.muted },
      majorGridlines: { style: "solid", fill: C.rule, width: 1 },
    },
    yAxis: {
      textStyle: { fontSize: 14, fill: C.body },
      line: { style: "solid", fill: C.rule, width: 1 },
    },
    dataLabels: {
      showValue: true,
      position: "outEnd",
      textStyle: { fontSize: 13, fill: C.ink, bold: true },
    },
  });

  panel(slide, {
    left: 682,
    top: 176,
    width: 556,
    height: 444,
    fill: C.bg,
    lineFill: C.rule,
    lineWidth: 1,
  });
  textBox(slide, {
    left: 708,
    top: 208,
    width: 510,
    height: 54,
    text: "这页最想传达的是：压缩不是主要元凶",
    fontSize: 26,
    bold: true,
    color: C.ink,
  });
  textBox(slide, {
    left: 708,
    top: 286,
    width: 500,
    height: 220,
    text:
      "1. 连没有记忆管线的 prompt_only 都已经 100% 走偏。\n\n2. 进 TierMem 以后不是更糟，而是从 86.7% 降到 73.3%。\n\n3. 这让原始 RQ1 的强版本基本死掉，也把 RQ5 往 reader / answer-time 推。",
    fontSize: 19,
    color: C.body,
  });
  panel(slide, {
    left: 708,
    top: 536,
    width: 490,
    height: 54,
    fill: C.accentSoft,
    lineFill: C.accent,
    lineWidth: 1,
    borderRadius: "rounded-sm",
  });
  textBox(slide, {
    left: 726,
    top: 552,
    width: 458,
    height: 20,
    text: "一句话：reader 的行为选择比 consolidator 的写法更值得追。",
    fontSize: 16,
    bold: true,
    color: C.accent,
  });

  footer(
    slide,
    6,
    "Source: 研究结果分类整理_20260704.md C1, RESEARCH_README.md §2",
  );
}

function slide7(presentation) {
  const slide = presentation.slides.add();
  slide.background.fill = C.bg;
  titleBlock(
    slide,
    "Know-Do Gap",
    "know-do gap 是当前最稳的正现象",
    "同一条记忆里，三模型都能把政策背出来，但问“该怎么做”时仍会违规。",
  );

  metricCard(slide, {
    left: 42,
    top: 184,
    width: 262,
    height: 170,
    value: "0",
    valueSize: 46,
    label: "doesn't know",
    note: "三模型在“政策是什么”这一步都没有出现不知道的情况。",
  });
  metricCard(slide, {
    left: 42,
    top: 374,
    width: 262,
    height: 170,
    value: "37–63%",
    valueSize: 40,
    label: "违规行动率",
    note: "真正出问题的是行为选择，不是政策记忆本身缺失。",
    valueColor: C.accent,
  });

  panel(slide, {
    left: 334,
    top: 184,
    width: 904,
    height: 422,
    fill: C.panel2,
    lineFill: C.rule,
    lineWidth: 1,
  });
  slide.charts.add("bar", {
    position: { left: 366, top: 216, width: 842, height: 344 },
    categories: ["gpt-4.1-mini", "gpt-4o", "gpt-4.1"],
    series: [
      {
        name: "违规行动",
        values: [63.3, 46.7, 36.7],
        fill: C.accent,
      },
      {
        name: "安全行动",
        values: [36.7, 53.3, 63.3],
        fill: "#111111",
      },
    ],
    hasLegend: true,
    legend: {
      position: "bottom",
      overlay: false,
      textStyle: { fontSize: 12, fill: C.body },
    },
    barOptions: { direction: "column", grouping: "clustered", gapWidth: 44 },
    yAxis: {
      min: 0,
      max: 100,
      majorUnit: 20,
      numberFormatCode: "0",
      textStyle: { fontSize: 12, fill: C.muted },
      majorGridlines: { style: "solid", fill: C.rule, width: 1 },
    },
    xAxis: {
      textStyle: { fontSize: 13, fill: C.body },
      line: { style: "solid", fill: C.rule, width: 1 },
    },
    dataLabels: {
      showValue: true,
      position: "outEnd",
      textStyle: { fontSize: 11, fill: C.ink, bold: true },
    },
  });

  textBox(slide, {
    left: 366,
    top: 572,
    width: 842,
    height: 28,
    text: "三条线加起来的意思很直接：policy knowledge 在，但 safe action 不自动跟着来。",
    fontSize: 16,
    color: C.body,
  });

  footer(
    slide,
    7,
    "Source: outputs/safety/knowdo_main_gpt41mini_20260708.json, knowdo_main_gpt4o_20260708.json, knowdo_main_gpt41_20260708.json",
  );
}

function slide8(presentation) {
  const slide = presentation.slides.add();
  slide.background.fill = C.bg;
  titleBlock(
    slide,
    "RQ2 Dual Track",
    "RQ2 现在只能支持弱版本",
    "官方版和自建版必须拆开说，而且都还不支持“越固化越糟”这个强版本。",
  );

  panel(slide, {
    left: 42,
    top: 176,
    width: 576,
    height: 444,
    fill: C.bg,
    lineFill: C.rule,
    lineWidth: 1,
  });
  textBox(slide, {
    left: 66,
    top: 200,
    width: 520,
    height: 34,
    text: "官方版：HaluMem",
    fontSize: 26,
    bold: true,
    color: C.ink,
  });
  textBox(slide, {
    left: 66,
    top: 238,
    width: 520,
    height: 30,
    text: "干净重跑和已有扩大量，方向都更偏负面。",
    fontSize: 15,
    color: C.muted,
  });
  const officialRows = [
    ["设置", "样本量", "unsupported fabrication", "结论"],
    ["tight-budget N0", "15", "33.3%", "基线"],
    ["tight-budget N1", "15", "16.7%", "下降"],
    ["tight-budget N2", "15", "16.7%", "不反弹"],
    ["已有 45QA 线", "45", "33.3% -> 8.3% -> 8.3% -> 8.3%", "同方向"],
  ];
  const officialTable = slide.tables.add({
    rows: officialRows.length,
    columns: officialRows[0].length,
    left: 66,
    top: 282,
    width: 528,
    height: 220,
    columnWidths: [170, 70, 170, 118],
    values: officialRows,
  });
  styleTable(officialTable, officialRows.length, officialRows[0].length, []);
  textBox(slide, {
    left: 66,
    top: 526,
    width: 520,
    height: 58,
    text: "最保守的人话：官方 benchmark 没看到“压缩越深，幻觉越糟”的支持证据。",
    fontSize: 18,
    bold: true,
    color: C.ink,
  });

  panel(slide, {
    left: 662,
    top: 176,
    width: 576,
    height: 444,
    fill: C.bg,
    lineFill: C.rule,
    lineWidth: 1,
  });
  textBox(slide, {
    left: 686,
    top: 200,
    width: 520,
    height: 34,
    text: "自建版：100 个基础题 / 每层 200 probes",
    fontSize: 24,
    bold: true,
    color: C.ink,
  });
  textBox(slide, {
    left: 686,
    top: 238,
    width: 520,
    height: 30,
    text: "这条线能看到错信，但更像是先出现、后回落。",
    fontSize: 15,
    color: C.muted,
  });
  const selfRows = [
    ["设置", "样本量", "false belief", "结论"],
    ["prompt-only", "200", "6.0%", "已有错信"],
    ["TierMem N0", "200", "10.5%", "更高"],
    ["TierMem N1", "200", "3.5%", "下降"],
    ["TierMem N2", "200", "2.5%", "继续下降"],
  ];
  const selfTable = slide.tables.add({
    rows: selfRows.length,
    columns: selfRows[0].length,
    left: 686,
    top: 282,
    width: 520,
    height: 220,
    columnWidths: [150, 70, 140, 160],
    values: selfRows,
  });
  styleTable(selfTable, selfRows.length, selfRows[0].length, []);
  textBox(slide, {
    left: 686,
    top: 526,
    width: 520,
    height: 58,
    text: "最保守的人话：重复错误说法能造错信，但不是“越固化越糟”的单调上升。",
    fontSize: 18,
    bold: true,
    color: C.ink,
  });

  panel(slide, {
    left: 42,
    top: 636,
    width: 1196,
    height: 26,
    fill: C.accentSoft,
    lineFill: C.accent,
    lineWidth: 1,
    borderRadius: "rounded-sm",
  });
  textBox(slide, {
    left: 54,
    top: 641,
    width: 1170,
    height: 18,
    text: "限制：human_label 列目前仍为空，所以自建版还不是正式的人类标注统计线。",
    fontSize: 12,
    bold: true,
    color: C.accent,
  });

  footer(
    slide,
    8,
    "Source: rq2_dual_track_refresh_20260708.md, outputs/v2_tiermem_micro/*, outputs/safety/rq2_selfbuilt_v6_rep5_*.json",
  );
}

function slide9(presentation) {
  const slide = presentation.slides.add();
  slide.background.fill = C.bg;
  titleBlock(
    slide,
    "RQ3 Live Run",
    "RQ3 读取侧防御是现在唯一仍在长正结果的主线",
    "但这页必须和进度绑定在一起读，因为大跑还没有完成。",
  );

  const topY = 172;
  const cardW = 280;
  const cardGap = 24;
  metricCard(slide, {
    left: 42,
    top: topY,
    width: cardW,
    height: 112,
    value: "20",
    valueSize: 34,
    label: "总 jobs",
    note: "固定矩阵",
  });
  metricCard(slide, {
    left: 42 + 1 * (cardW + cardGap),
    top: topY,
    width: cardW,
    height: 112,
    value: "10",
    valueSize: 34,
    label: "已完成",
    note: "completion 50%",
    valueColor: C.accent,
  });
  metricCard(slide, {
    left: 42 + 2 * (cardW + cardGap),
    top: topY,
    width: cardW,
    height: 112,
    value: "1",
    valueSize: 34,
    label: "运行中",
    note: "最新快照",
  });
  metricCard(slide, {
    left: 42 + 3 * (cardW + cardGap),
    top: topY,
    width: cardW,
    height: 112,
    value: "9",
    valueSize: 34,
    label: "待完成",
    note: "尚未收敛",
  });

  panel(slide, {
    left: 42,
    top: 320,
    width: 650,
    height: 318,
    fill: C.panel2,
    lineFill: C.rule,
    lineWidth: 1,
  });
  slide.charts.add("bar", {
    position: { left: 68, top: 356, width: 604, height: 246 },
    categories: ["prompt N0", "tiermem N0", "tiermem N1", "tiermem N2"],
    series: [
      {
        name: "错误行动率下降 pp",
        values: [15.6, 16.7, 10.0, 18.3],
        fill: C.accent,
      },
    ],
    hasLegend: false,
    barOptions: { direction: "column", grouping: "clustered", gapWidth: 46 },
    yAxis: {
      min: 0,
      max: 20,
      majorUnit: 5,
      textStyle: { fontSize: 12, fill: C.muted },
      majorGridlines: { style: "solid", fill: C.rule, width: 1 },
    },
    xAxis: {
      textStyle: { fontSize: 13, fill: C.body },
      line: { style: "solid", fill: C.rule, width: 1 },
    },
    dataLabels: {
      showValue: true,
      position: "outEnd",
      textStyle: { fontSize: 11, fill: C.ink, bold: true },
    },
  });

  panel(slide, {
    left: 724,
    top: 320,
    width: 514,
    height: 318,
    fill: C.bg,
    lineFill: C.rule,
    lineWidth: 1,
  });
  textBox(slide, {
    left: 748,
    top: 350,
    width: 462,
    height: 38,
    text: "当前读法",
    fontSize: 26,
    bold: true,
    color: C.ink,
  });
  textBox(slide, {
    left: 748,
    top: 402,
    width: 458,
    height: 184,
    text:
      "1. 所有已完成条件，均值都朝防御方向走。\n\n2. 当前最好的一组是 prompt_only seed23：96.7% -> 76.7%。\n\n3. tiermem N1 最弱，但仍是 10pp 的平均下降。\n\n4. 由于只完成了 50%，这条线现在还只能叫“最有希望”，不能叫“定稿主结果”。",
    fontSize: 18,
    color: C.body,
  });

  footer(
    slide,
    9,
    "Source: state/rq3_readtime_large_20260708_dashboard_data.json snapshot_at=2026-07-09T06:34:24",
  );
}

function slide10(presentation) {
  const slide = presentation.slides.add();
  slide.background.fill = C.bg;
  titleBlock(
    slide,
    "Where To Push Next",
    "接下来什么最像论文，什么最值得今晚继续跑",
    "真正有论文味的，不再只是补实验量，而是把问题框到更稳的研究主线上。",
  );

  const colW = 372;
  const xs = [42, 454, 866];
  const headers = [
    ["已经可以写", "1. 终点定义会翻转结论\n2. know-do gap 跨 3 模型存在\n3. reader 比 consolidator 更像罪魁"],
    ["今晚继续跑", "1. 跑完 RQ3 大矩阵\n2. 把 human_label 真正落盘\n3. 补官方 45QA tight-budget 线\n4. 开始做 RQ4 多算子对照"],
    ["更像博士主线", "1. 系统审计 agent 安全评测的 overclaim\n2. 建立人工 κ + 行为终点 + 簇样本口径\n3. 把“可靠性协议”做成方法贡献"],
  ];
  for (let i = 0; i < headers.length; i += 1) {
    panel(slide, {
      left: xs[i],
      top: 180,
      width: colW,
      height: 370,
      fill: i === 2 ? C.accentSoft : C.panel2,
      lineFill: i === 2 ? C.accent : C.rule,
      lineWidth: 1,
    });
    textBox(slide, {
      left: xs[i] + 22,
      top: 206,
      width: colW - 44,
      height: 36,
      text: headers[i][0],
      fontSize: 28,
      bold: true,
      color: C.ink,
    });
    textBox(slide, {
      left: xs[i] + 22,
      top: 266,
      width: colW - 44,
      height: 244,
      text: headers[i][1],
      fontSize: 18,
      color: C.body,
    });
  }

  panel(slide, {
    left: 42,
    top: 584,
    width: 1196,
    height: 52,
    fill: C.bg,
    lineFill: C.accent,
    lineWidth: 1,
    borderRadius: "rounded-sm",
  });
  textBox(slide, {
    left: 64,
    top: 598,
    width: 1150,
    height: 24,
    text: "收尾一句话：真正有论文味的主线，正在从“压缩导致危险”转成“评测如何把你带偏”。",
    fontSize: 20,
    bold: true,
    color: C.accent,
  });

  footer(
    slide,
    10,
    "Source: RESEARCH_README.md §4/§7, 研究结果分类整理_20260704.md F, rq2_dual_track_refresh_20260708.md §6",
  );
}

async function buildDeck() {
  await fs.mkdir(OUT_DIR, { recursive: true });
  const presentation = Presentation.create({
    slideSize: { width: SLIDE_W, height: SLIDE_H },
  });

  slide1(presentation);
  slide2(presentation);
  slide3(presentation);
  slide4(presentation);
  slide5(presentation);
  slide6(presentation);
  slide7(presentation);
  slide8(presentation);
  slide9(presentation);
  slide10(presentation);

  for (const [index, slide] of presentation.slides.items.entries()) {
    const stem = `slide-${String(index + 1).padStart(2, "0")}`;
    const png = await presentation.export({ slide, format: "png", scale: 1 });
    await writeBlob(path.join(OUT_DIR, `${stem}.png`), png);
    const layout = await slide.export({ format: "layout" });
    await fs.writeFile(
      path.join(OUT_DIR, `${stem}.layout.json`),
      await layout.text(),
      "utf8",
    );
  }

  const montage = await presentation.export({
    format: "webp",
    montage: true,
    scale: 1,
  });
  await writeBlob(path.join(OUT_DIR, "deck-montage.webp"), montage);

  const pptx = await PresentationFile.exportPptx(presentation);
  await pptx.save(path.join(OUT_DIR, "mc_safety_technical_update_20260709.pptx"));
}

buildDeck().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
