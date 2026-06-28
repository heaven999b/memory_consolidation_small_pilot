# Memory Consolidation Small Pilot

当前发布版本：`v0.2.0-idea-baseline-private`

这是一个 **受控合成 pre-pilot**，目的不是证明真实模型已经有某个结论，而是先验证：

1. `summary-only` vs `tiered/raw-backed` 的实验管线能不能跑通；
2. `N-sweep`、指标、artifact 输出是否合理；
3. 在小样本受控场景下，是否已经能看到我们想研究的风险方向。

## 当前 reviewer-facing 主表面

当前 repo 不再只有 synthetic/proxy pilot 叙事。现在多了一层 **benchmark-first primary surface**：

- 先看更宽的 reviewer-facing benchmark section：
  HaluMem core + HaluMem holdout，以及 LoCoMo core + LongMemEval direct；
- 再看 real-model sanity slices；
- synthetic core trio 退到支撑层，而不是继续充当唯一主证据。

这层主表面现在已经不是 `partial` 了。当前 repo 同时具备：

- 一个完整的 **benchmark-first proxy base**；
- 一个新的 **benchmark-native primary base**，也就是主 baseline 明确以 frozen benchmark manifests、query contract、evidence contract 作为第一公民；
- 一个新的 **manifest-backed task-extension layer**，把 `conflict` / `unsafe` 也接进同一条 primary-base 链；
- 但它仍然还不是 literal full `TierMem` reproduction，也还没有扩到最终 paper-facing 的更大 benchmark scale。

## Repository Snapshot

当前这份私密仓库快照的版本边界是：

- `VERSION`: 当前发布版本号
- `CHANGELOG.md`: 这版 release 的高层变化
- `MODIFICATION_LOG_SUMMARY.md`: 适合快速回看的简版修改记录
- `REPO_REVIEW_AND_TABLE_ANALYSIS.md`: 当前剩余问题、主表格读法和 reviewer-facing 风险说明
- `REPRODUCIBILITY.md`: 固定环境和单入口 release rebuild 说明
- `state/release_snapshot.json`: 当前 baseline gate、artifact 状态和发布边界

Git 跟踪的 benchmark surface 以 frozen slices 和 reviewer-facing artifacts 为主，而不是全量原始 benchmark 镜像。

## 这不是最终论文实验

这个 pilot 是 **proxy experiment**：

- 数据是手工构造的小样本；
- consolidation operator 是 rule-based stochastic compactor；
- 结果只能作为 “是否值得继续做真 benchmark / 真模型实验” 的先验信号；
- 不能当成对真实 `TierMem`、`HaluMem`、`AgentPoison` 的正式结论。

不过当前版本已经不再只是 proxy surface：

- reviewer-facing baseline 已经升到 **benchmark-native primary base**
- `conflict` / `unsafe` 已经通过 manifest-backed task extensions 接入主链
- `paper_level_baseline_ready` 仍然是 `False`
- 当前主要缺口是更大的 benchmark coverage scale，而不是新的主实现 blocker

## 当前数据集

当前默认使用 [`curated_dataset.py`](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/curated_dataset.py) 中定义的高质量 synthetic items。

对外做快速审计时，可以直接调用 `build_curated_dataset()`；它是 `build_items()` 的稳定便利别名。

- 当前规模：`58` 条
- 覆盖四个 family
- 每轮先跑机械审计，再进入实验
- iteration 9 额外加入一个 `16` 条的 `textual_proxy` slice，用来做更接近自由文本摘要环境的 realism check，而不打乱主回归集
- 最近额外补入了 `halu_15` 到 `halu_20` 六个 hallucination item：其中 `halu_15/16` 加强 `code-like literal overlap`，`halu_17/18` 是较弱的旧 name-overlap pair，`halu_19/20` 则是更贴近 query role 的强化版 name-overlap pair，用来支撑下一轮 literal subsplit follow-up

审计命令：

```bash
python3 audit_dataset.py
```

## 覆盖的 family

- `hallucination`: 对本来缺失的信息生成 unsupported memory；
- `conflict`: 多次更新后保留旧事实或把新旧事实 merge 错；
- `unsafe`: 把低信任不安全建议保留或洗白。
- `benign`: 正常可回答信息，用来测 overcompression 和 unnecessary fallback。

## 比较条件

- `raw_only`
- `summary_only`
- `tiered`
- `adaptive_tiered`
- `adaptive_guarded`
- `risk_first`
- `utility_first`
- `utility_calibrated`
- `small_n_hybrid`
- `scale_aware_unified`

其中 `risk_first` / `utility_first` 是 scrub-based policy：先清掉 unsupported / unsafe / stale / non-current claim，再用一个 noisy retrieval probe 判断“是否值得回退到 raw-backed answer”，而不是直接读取 backing-store oracle。
`utility_calibrated` 则是在 noisy probe 基础上做 detector calibration 的后续 iteration，目标是修补 `utility_first` 在低分 conflict / benign case 上的 recall miss。
`small_n_hybrid` 是一个 focused 小 N 条件：只在 `N<=2` 且 probe 落入窄 guardband 时借用 tiered-style shield，不打算作为高 N 全局策略。
`scale_aware_unified` 则把 `small_n_hybrid` 的低 `N` 优势和 `utility_calibrated` 的高 `N` 优势合成一个全 sweep 结构化策略。

## Sweep 变量

- `N in {0, 1, 2, 4, 8}`

## Rebuild

- 固定环境见 [environment.yml](/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/environment.yml) 和 [requirements.txt](/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/requirements.txt)
- 单入口 release rebuild: `python3 run_release_rebuild.py`

## 产出

运行后会生成：

- `outputs/small_pilot_results.json`
- `outputs/small_pilot_summary.md`
- `outputs/aggregate_rows.csv`
- `outputs/exemplar_traces.md`
- `outputs/detector_calibration_results.json`
- `outputs/detector_calibration_summary.md`
- `outputs/small_n_hybrid_results.json`
- `outputs/small_n_hybrid_summary.md`
- `outputs/scale_aware_unified_results.json`
- `outputs/scale_aware_unified_summary.md`
- `outputs/textual_proxy_slice_results.json`
- `outputs/textual_proxy_slice_summary.md`
- `outputs/textual_proxy_slice_traces.md`
- `outputs/note_aware_detector_results.json`
- `outputs/note_aware_detector_summary.md`
- `outputs/actual_summarizer_slice_results.json`
- `outputs/actual_summarizer_slice_summary.md`
- `outputs/actual_summarizer_slice_traces.md`
- `outputs/actual_recall_expansion_results.json`
- `outputs/actual_recall_expansion_summary.md`
- `outputs/actual_recall_expansion_traces.md`
- `outputs/actual_hallucination_stress_results.json`
- `outputs/actual_hallucination_stress_summary.md`
- `outputs/actual_hallucination_stress_traces.md`
- `outputs/actual_hallucination_persistence_results.json`
- `outputs/actual_hallucination_persistence_summary.md`
- `outputs/actual_hallucination_persistence_traces.md`
- `outputs/actual_hallucination_robustness_results.json`
- `outputs/actual_hallucination_robustness_summary.md`
- `outputs/actual_hallucination_robustness_traces.md`
- `outputs/actual_hallucination_intermediate_contract_results.json`
- `outputs/actual_hallucination_intermediate_contract_summary.md`
- `outputs/actual_hallucination_intermediate_contract_traces.md`
- `outputs/actual_hallucination_typed_selective_results.json`
- `outputs/actual_hallucination_typed_selective_summary.md`
- `outputs/actual_hallucination_typed_selective_traces.md`
- `outputs/actual_hallucination_surrogate_split_results.json`
- `outputs/actual_hallucination_surrogate_split_summary.md`
- `outputs/actual_hallucination_surrogate_split_traces.md`
- `outputs/actual_hallucination_identity_focus_pilot_results.json`
- `outputs/actual_hallucination_identity_focus_pilot_summary.md`
- `outputs/actual_hallucination_identity_focus_pilot_traces.md`
- `outputs/actual_hallucination_literal_subsplit_pilot_results.json`
- `outputs/actual_hallucination_literal_subsplit_pilot_summary.md`
- `outputs/actual_hallucination_literal_subsplit_pilot_traces.md`
- `outputs/actual_hallucination_name_refinement_pilot_results.json`
- `outputs/actual_hallucination_name_refinement_pilot_summary.md`
- `outputs/actual_hallucination_name_refinement_pilot_traces.md`
- `outputs/actual_hallucination_name_normalization_pilot_results.json`
- `outputs/actual_hallucination_name_normalization_pilot_summary.md`
- `outputs/actual_hallucination_name_normalization_pilot_traces.md`
- `outputs/actual_hallucination_literal_normalization_pilot_results.json`
- `outputs/actual_hallucination_literal_normalization_pilot_summary.md`
- `outputs/actual_hallucination_literal_normalization_pilot_traces.md`
- `outputs/actual_hallucination_literal_claim_pilot_results.json`
- `outputs/actual_hallucination_literal_claim_pilot_summary.md`
- `outputs/actual_hallucination_literal_claim_pilot_traces.md`
- `outputs/actual_hallucination_identity_claim_bridge_pilot_results.json`
- `outputs/actual_hallucination_identity_claim_bridge_pilot_summary.md`
- `outputs/actual_hallucination_identity_claim_bridge_pilot_traces.md`
- `outputs/actual_hallucination_claim_reintegration_pilot_results.json`
- `outputs/actual_hallucination_claim_reintegration_pilot_summary.md`
- `outputs/actual_hallucination_claim_reintegration_pilot_traces.md`
- `outputs/actual_hallucination_literal_identity_closure_results.json`
- `outputs/actual_hallucination_literal_identity_closure_summary.md`
- `outputs/actual_hallucination_literal_identity_closure_traces.md`
- `outputs/external_benchmark_adapter_layer.json`
- `outputs/external_benchmark_adapter_layer.md`
- `outputs/external_benchmark_minimal_baseline.json`
- `outputs/external_benchmark_minimal_baseline.md`
- `outputs/external_benchmark_minimal_baseline_traces.md`
- `outputs/external_benchmark_reviewer_section.json`
- `outputs/external_benchmark_reviewer_section.md`
- `outputs/external_benchmark_reviewer_section_traces.md`
- `outputs/task_extension_section.json`
- `outputs/task_extension_section.md`
- `outputs/task_extension_section_traces.md`
- `outputs/benchmark_native_primary_base.json`
- `outputs/benchmark_native_primary_base.md`
- `outputs/benchmark_native_primary_base_traces.md`
- `outputs/benchmark_first_proxy_base.json`
- `outputs/benchmark_first_proxy_base.md`
- `outputs/tiermem_style_primary_surface.json`
- `outputs/tiermem_style_primary_surface.md`
- `outputs/paper_baseline_packet.json`
- `outputs/paper_baseline_packet.md`
- `outputs/paper_baseline_panel.csv`
- `outputs/actual_note_persistence_results.json`
- `outputs/actual_note_persistence_summary.md`
- `outputs/actual_note_persistence_traces.md`
- `outputs/actual_scaffold_refinement_results.json`
- `outputs/actual_scaffold_refinement_summary.md`
- `outputs/actual_scaffold_refinement_traces.md`
- `outputs/actual_placeholder_hardening_results.json`
- `outputs/actual_placeholder_hardening_summary.md`
- `outputs/actual_placeholder_hardening_traces.md`
- `outputs/actual_carry_forward_results.json`
- `outputs/actual_carry_forward_summary.md`
- `outputs/actual_carry_forward_traces.md`
- `reviews/dataset_quality_audit_round2.md`
- `reviews/review_round3.md`
- `reviews/review_round4.md`
- `reviews/review_round5.md`
- `reviews/review_round7.md`
- `reviews/review_round8.md`
- `reviews/review_round9.md`
- `reviews/review_round10.md`
- `reviews/review_round11.md`
- `reviews/review_round12.md`
- `reviews/review_round13.md`
- `reviews/review_round14.md`
- `reviews/review_round15.md`
- `reviews/review_round16.md`
- `reviews/review_round17.md`
- `reviews/review_round18.md`
- `reviews/review_round19.md`
- `reviews/review_round20.md`
- `reviews/review_round21.md`
- `reviews/review_round22.md`
- `reviews/review_round23.md`
- `reviews/review_round24.md`
- `reviews/review_round25.md`
- `reviews/review_round26.md`
- `reviews/review_round27.md`
- `reviews/review_round28.md`
- `reviews/verification_round5.md`
- `reviews/review_round6.md`
- `reviews/verification_round6.md`
- `reviews/verification_round7.md`
- `reviews/verification_round8.md`
- `reviews/verification_round9.md`
- `reviews/verification_round10.md`
- `reviews/verification_round11.md`
- `reviews/verification_round12.md`
- `reviews/verification_round13.md`
- `reviews/verification_round14.md`
- `reviews/verification_round15.md`
- `reviews/verification_round16.md`
- `reviews/verification_round17.md`
- `reviews/verification_round18.md`
- `reviews/verification_round19.md`
- `reviews/verification_round20.md`
- `reviews/verification_round21.md`
- `reviews/verification_round22.md`
- `reviews/verification_round23.md`
- `reviews/verification_round24.md`
- `reviews/verification_round25.md`
- `reviews/verification_round26.md`
- `reviews/verification_round27.md`
- `reviews/verification_round28.md`
- `reviews/external_benchmark_slice_audit_round33.md`
- `reviews/external_benchmark_slice_audit_round34.md`
- `reviews/verification_round33_benchmark.md`
- `reviews/verification_round33_primary_surface.md`
- `reviews/verification_round33.md`
- `reviews/verification_round34_reviewer_section.md`
- `reviews/verification_round34_primary_surface.md`
- `reviews/verification_round34.md`

## 运行

```bash
python3 audit_dataset.py
python3 run_small_pilot.py
python3 run_detector_calibration.py
python3 verify_detector_calibration.py
python3 run_small_n_hybrid.py
python3 verify_small_n_hybrid.py
python3 run_scale_aware_unified.py
python3 verify_scale_aware_unified.py
python3 run_textual_proxy_slice.py
python3 verify_textual_proxy_slice.py
python3 run_note_aware_detector_round.py
python3 verify_note_aware_detector_round.py
python3 run_actual_summarizer_slice.py
python3 verify_actual_summarizer_slice.py
python3 run_actual_recall_expansion.py
python3 verify_actual_recall_expansion.py
python3 run_actual_hallucination_stress_slice.py
python3 verify_actual_hallucination_stress.py
python3 run_actual_hallucination_persistence_round.py
python3 verify_actual_hallucination_persistence_round.py
python3 run_actual_hallucination_robustness_round.py
python3 verify_actual_hallucination_robustness_round.py
python3 run_actual_hallucination_intermediate_contract_round.py
python3 verify_actual_hallucination_intermediate_contract_round.py
python3 run_actual_hallucination_typed_selective_round.py
python3 verify_actual_hallucination_typed_selective_round.py
python3 run_actual_hallucination_surrogate_split_round.py
python3 verify_actual_hallucination_surrogate_split_round.py
python3 run_actual_hallucination_identity_focus_pilot.py
python3 verify_actual_hallucination_identity_focus_pilot.py
python3 run_actual_hallucination_literal_subsplit_pilot.py
python3 verify_actual_hallucination_literal_subsplit_pilot.py
python3 run_actual_hallucination_name_refinement_pilot.py
python3 verify_actual_hallucination_name_refinement_pilot.py
python3 run_actual_hallucination_name_normalization_pilot.py
python3 verify_actual_hallucination_name_normalization_pilot.py
python3 freeze_external_benchmark_slices.py
python3 freeze_external_benchmark_reviewer_slices.py
python3 run_external_benchmark_minimal_baseline.py
python3 verify_external_benchmark_minimal_baseline.py
python3 run_external_benchmark_reviewer_section.py
python3 verify_external_benchmark_reviewer_section.py
python3 run_benchmark_first_primary_entrypoint.py
python3 verify_tiermem_style_primary_surface.py
python3 verify_paper_baseline_packet.py
python3 run_paper_baseline_packet.py
python3 verify_paper_baseline_packet.py
python3 run_actual_hallucination_literal_normalization_pilot.py
python3 verify_actual_hallucination_literal_normalization_pilot.py
python3 run_actual_hallucination_literal_claim_pilot.py
python3 verify_actual_hallucination_literal_claim_pilot.py
python3 run_actual_hallucination_identity_claim_bridge_pilot.py
ACTUAL_HALLU_IDENTITY_MICRO_IDS=halu_02,halu_03,halu_04,halu_05,halu_08,halu_14 ACTUAL_HALLU_IDENTITY_MICRO_SEEDS=11 ACTUAL_HALLU_IDENTITY_MICRO_INTERVENTIONS=literal_identity_anchor ACTUAL_HALLU_IDENTITY_MICRO_JSON_PATH=outputs/actual_hallucination_literal_identity_closure_results.json ACTUAL_HALLU_IDENTITY_MICRO_SUMMARY_PATH=outputs/actual_hallucination_literal_identity_closure_summary.md ACTUAL_HALLU_IDENTITY_MICRO_TRACE_PATH=outputs/actual_hallucination_literal_identity_closure_traces.md python3 run_actual_hallucination_identity_micro_split_round.py
python3 run_external_benchmark_adapter_layer.py
ACTUAL_RECALL_EXPANSION_SEEDS=11,23 python3 run_actual_recall_expansion.py
ACTUAL_HALLU_STRESS_SEEDS=11,23 python3 run_actual_hallucination_stress_slice.py
python3 run_actual_hallucination_claim_reintegration_pilot.py
python3 run_paper_baseline_packet.py
python3 verify_paper_baseline_packet.py
python3 verify_actual_hallucination_identity_claim_bridge_pilot.py
python3 run_actual_hallucination_claim_reintegration_pilot.py
python3 verify_actual_hallucination_claim_reintegration_pilot.py
python3 run_paper_baseline_packet.py
python3 verify_paper_baseline_packet.py
python3 run_actual_note_persistence_round.py
python3 verify_actual_note_persistence_round.py
python3 run_actual_scaffold_refinement_round.py
python3 verify_actual_scaffold_refinement_round.py
python3 run_actual_placeholder_hardening_round.py
python3 verify_actual_placeholder_hardening_round.py
python3 run_actual_carry_forward_round.py
python3 verify_actual_carry_forward_round.py
```

说明：

- `run_actual_summarizer_slice.py` 会调用已登录的 `deepseek` CLI，属于真实模型-backed sub-slice，而不是纯手写 proxy。
- 这一轮默认只跑一个小而高质量的 audited slice，并且带 cache，避免每次都重复付出模型调用成本。
- `run_actual_recall_expansion.py` 把真实 model-backed slice 扩到 benign/conflict 富集版本，用来定位高 `N` 的真实 answerability loss。
- `run_actual_hallucination_stress_slice.py` 是一个更激进的真实 hallucination stress 条件，用来专门测试 detector transfer 是否能穿过真实 summarizer。
- `run_actual_hallucination_stress_slice.py` 现在支持 `ACTUAL_HALLU_STRESS_IDS` / `ACTUAL_HALLU_STRESS_ITEM_LIMIT`，可以在不改脚本默认配置的前提下临时扩到新的 literal-identity/code-overlap stress item。
- `run_actual_hallucination_persistence_round.py` 把更强的 scaffold/parser/executor contract 带回真实 hallucination stress，测试 tentative clue 是否能在 `N=4/8` 继续存活，并让 note-aware detector gain 不再只停在局部 `N=1`。
- `run_actual_hallucination_robustness_round.py` 在同一个真实 stress slice 上同时比较 `strong_anchor` 和 `soft_anchor`，并扩到多 seed，检验 detector gain 到底是稳健现象还是只在强 contract 下才出现。
- `run_actual_hallucination_intermediate_contract_round.py` 在 `strong_anchor` 和 `soft_anchor` 之间加入一个 field-sensitive `selective_anchor`，测试能否在更自然的 stress contract 下同时保住一部分 clue survival 和 note-aware detector gain。
- `run_actual_hallucination_typed_selective_round.py` 在上一轮 selective midpoint 的基础上继续 typed 化，把 policy-window / schedule-like anchor 压回 `weak_context`，同时检查 person-like 与 preference-like surrogate 还能否保住 detector signal。
- `run_actual_hallucination_surrogate_split_round.py` 再往前拆 typed midpoint，把 identity-like surrogate 和 preference-style surrogate 分开，测试剩下的高 `N` detector work 到底主要靠哪一类在支撑。
- `run_actual_hallucination_identity_focus_pilot.py` 是一个更快的 expanded-slice focused follow-up：固定 6 条 relation/code/name literal item、1 个 seed，只比较 typed / identity / relation-literal split 四个关键 intervention，用来确认 identity family 还能不能继续拆。
- `run_actual_hallucination_literal_subsplit_pilot.py` 则顺着上一轮继续往下拆 literal branch：固定 6 条 code/name overlap item，只比较 typed / broad literal / code-only / name-only 四个关键 intervention，用来判断强化后的人名重叠是否终于能形成独立 detector signal。
- `run_actual_hallucination_name_refinement_pilot.py` 再顺着上一轮往前走一步：不再加数据，而是把 name-only scaffold 变成 role-sensitive contract，显式区分 aligned-name 与 anti-role name，检查 strengthened name branch 能否从 recoverable signal 更进一步走向 compact-stable clue。
- `run_actual_hallucination_name_normalization_pilot.py` 则固定上一轮的 refined name-only compactor，不再改 prompt 语义，而是在 executor 侧加入 aligned-name note normalization，专门测试 final note 形态的稳定化是否足以把 focused name branch 的 note-aware false-present 再往下压。
- `run_actual_hallucination_literal_normalization_pilot.py` 则把这套 aligned-name note normalization 合回 broad literal branch：固定 mixed code+name literal slice，不改 literal compactor 语义，只做 executor-side final-note rewrite，检查 broad literal 的 strongest aligned-name case 能否在不改变 aggregate false-present 的前提下变成 `2/2` scaffold-stable。
- `run_actual_hallucination_literal_claim_pilot.py` 则继续沿着 broad literal frontier 往前推进：在已经 canonical 的 aligned-name literal scaffold 上，再显式 surface tentative query claim，检查 strongest aligned-name pressure 能否从 `raw-only recoverable clue` 变成 `explicit tentative target claim`，同时保持 code/weak-name 非回退和 aggregate false-present 不变。
- `run_actual_hallucination_identity_claim_bridge_pilot.py` 则把这条 claim-sensitive broad literal branch 再往外扩一层：固定一个 8-item relation+literal bridge slice，复用已经稳定的 relation-frontier 与 literal-frontier cache，检查 claim surfacing 在 relation item 重新接回后是否仍然非回退。
- `run_actual_hallucination_claim_reintegration_pilot.py` 则继续沿着同一条 branch 做更大一步的 outward expansion：固定一个 14-item mixed stress+literal reintegration slice，并且显式标记哪些 non-literal stress item 是 mode-equivalent proxy row、哪些 row 是 exact artifact，先验证 claim-sensitive broad literal 在更宽 actual-stress 前沿里是否仍然保持 relation/context/code/weak-name 非回退与 strengthened-name claim surfacing。
- `run_paper_baseline_packet.py` 则把项目当前到底有没有达到“论文级最小 baseline”冻结成一个 reviewer-facing artifact：统一收拢 synthetic closed-loop baseline trio、model-backed recall/hallucination sanity、以及还阻止我们写成 benchmark baseline 的 blocker，避免后续迭代再模糊地高估进度。

## 你应该怎么解读结果

如果这个 pre-pilot 出现以下信号，就说明值得继续做真 benchmark / 真模型实验：

1. `summary_only` 的 unsupported / unsafe / conflict risk 随 `N` 增长；
2. `tiered` 能降低 propagation-to-answer；
3. `risk_first` / `utility_first` / `utility_calibrated` / `small_n_hybrid` / `scale_aware_unified` 能不能在 noisy probe 下继续把 latent contamination 变成更低的 residual contamination；
4. `scale_aware_unified` 能不能把小 `N` 和高 `N` 的局部最优拼成一个全 sweep 结构化策略，而不是再继续堆局部 patch；
5. `textual_proxy` slice 能不能在更接近自由文本摘要的环境下保留同样的方向性结论；
6. `note_aware detector` 能不能在 textual slice 上压低 hallucination-side false-present，而不是靠大范围 abstain 取胜；
7. `actual summarizer slice` 能不能在真实模型-backed压缩链里保留 `summary_only` 恶化和 cleanup-family 相对 `tiered` 的优势；
8. `actual recall expansion` 能不能把真实 bottleneck 准确定位到 benign/conflict 的 `history_loss` / `empty_note_then_abstain`；
9. `actual hallucination stress` 能不能让 detector transfer 在真实模型里被局部或持续触发；
10. `actual note persistence` 能不能用更短、更固定的 note scaffold 直接减少高 `N` target evaporation，而不是只靠更高 raw fallback 来兜底；
11. `actual scaffold refinement` 能不能在保住 persistence 收益的同时修掉 unsafe refusal 语义回归，而不把 `MISSING` 之类 placeholder 再次变成 answer-like target；
12. `actual placeholder hardening` 能不能仅靠 parser/normalization 就消灭 placeholder leakage，并把 refined scaffold 的高 `N` accuracy 拉回到更强前沿；
13. `actual carry-forward` 能不能在空/null structured-output pass 上保住已有 refusal scaffold，把 refined family 从“高分但脆弱”推进成更稳的 executor contract；
14. `actual hallucination persistence` 能不能把真实 stress 里的 tentative clue 保留下来足够多轮，从而让 note-aware detector 的 gain 在高 `N` 也可见；
15. `actual hallucination robustness` 能不能说明高 `N` detector gain 在多 seed 下仍成立，并揭示 strong contract 与 softer contract 之间的 realism/robustness tradeoff；
16. `actual hallucination intermediate contract` 能不能在更自然的 selective contract 下同时保留部分 clue survival、detector work 和 summary-only realism，而不是只能在 `strong_anchor` / `soft_anchor` 两极之间二选一；
17. `actual hallucination typed selective` 能不能在不丢掉 detector gain 的前提下，修掉 selective midpoint 里 policy-window 型高 `N` 误读，并把 realism 再往前推一步；
18. `actual hallucination surrogate split` 能不能把 typed midpoint 里残留的 detector signal 进一步定位到 identity-like 还是 preference-style surrogate family，而不是继续把它们混在一个 realism bucket 里；
19. `actual hallucination identity focus pilot` 能不能在 expanded literal item 上把 identity-like signal 继续拆成 relation-style alias 与 literal-style overlap，并判断 literal 里更稳定的是 code overlap 还是 person-name overlap；
20. `benign` family 让我们能看到 overcompression 和过度回退之间的折中。

如果这些信号完全不存在，就说明我们当前 framing 还不够锋利，应该先调整实验设计。
