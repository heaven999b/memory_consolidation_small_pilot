# state/rt02_runs 目录说明 · 2026-07-19

**给未来窗口/协作者**：本目录混着最终结果、调试残留和已知有 bug 的产物。**动手前先读这张表。**

## ✅ v1 最终结果（immutable，不改不覆盖）

| 目录 | 内容 |
|---|---|
| `chir_qa_20260718/` | CHIR RQ3 QA 21 case 六臂 |
| `chir_wf_20260718/` | CHIR RQ3 Workflow 20 case |
| `chir_rq4_qa_20260718/` | CHIR RQ4 21 QA（含 verdict_qa_full21.json） |
| `pairgain_qa_20260718/` | PairGain QA 42 case |
| `pairgain_wf_20260718_v2/` | **PairGain Workflow 最终版**（30 case，用 nli_deberta_mps.jsonl） |
| `pairgain_roberta_sensitivity_20260719/` | 第二 NLI checkpoint 敏感性 |
| `rt02_chir_verdict_20260718.json`、`rt02_pairgain_verdict_20260718.json` | 合并 verdict |

> ⚠️ v1 的**数字**可复算，但**构念已被证明有问题**（见 `../rt02_v1_critical_review_20260719.md` 的 6 根因）。**不要再把 v1 的 GO/STOP 当作结论引用。**

## ❌ 不可作为结果使用

| 目录/文件 | 为什么 |
|---|---|
| `pairgain_wf_20260718/` | **Workflow v1，有 bug**：snapshot 用非唯一 `cluster_id`，7 个重复 ID 互相覆盖。仅供 bug 审计，**最终版是 `pairgain_wf_20260718_v2/`** |
| `pairgain_wf_20260718_v2/nli_deberta.jsonl` | 未完成的 CPU audit，只有 22 行。**最终 NLI 是同目录的 `nli_deberta_mps.jsonl`（30 行）** |
| `smoke_qa/`、`smoke_wf/`、`smoke_pg_qa/`、`smoke_pg_wf_v2/`、`smoke_chir_rq4_qa/` | v1 时期调试冒烟输出，**不是 verdict** |
| `pairgain_partial_qa11.json` | 部分运行的调试产物 |

## 🔶 v2 dev smoke（机器验证用，n 极小，非研究结论）

| 目录 | 说明 |
|---|---|
| `v2_dev_chir_append/`、`v2_dev_chir_summary/` | CHIR v2 smoke，**因并发限流未跑满**（append 3/6、summary 2/6）；**无 benign_vol 臂**（benign_vol 是 smoke 之后才实现的） |
| `v2_dev_pg_append/`、`v2_dev_pg_summary/` | PairGain v2 smoke（各 6/6），含 NLI 输出 |

> ⚠️ v2 smoke 的 `nli_source_only.jsonl` 对应的是**已废弃的主测量**（D 恒定→G≡0）。现行主测量是 `carrier_matched`，见 `../rt02_confirmatory_config_20260719.md` §4。

## 待创建

confirmatory 结果将写入 `v2_conf_*`（见 `../rt02_confirmatory_config_20260719.md` §7）。**绝不覆盖上述任何目录。**
