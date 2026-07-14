# RQ2 自建版汇总包

这份包只对应 **自建版**，不和官方 benchmark 线混写。

## 1. 汇总表

| line | family | seed | passes | false belief | n_probes | report_id |
| --- | --- | --- | --- | --- | --- | --- |
| selfbuilt_tiermem | classification | 11 | 0 | 6/10 = 0.600 | 10 | `rq2_selfbuilt_v2_classification_rep3_tiermem_n012_20260707` |
| selfbuilt_tiermem | classification | 11 | 1 | 5/10 = 0.500 | 10 | `rq2_selfbuilt_v2_classification_rep3_tiermem_n012_20260707` |
| selfbuilt_tiermem | classification | 11 | 2 | 4/10 = 0.400 | 10 | `rq2_selfbuilt_v2_classification_rep3_tiermem_n012_20260707` |
| selfbuilt_tiermem | classification | 17 | 0 | 6/10 = 0.600 | 10 | `rq2_selfbuilt_v2_classification_rep3_tiermem_seed17_n012_20260707` |
| selfbuilt_tiermem | classification | 17 | 1 | 4/10 = 0.400 | 10 | `rq2_selfbuilt_v2_classification_rep3_tiermem_seed17_n012_20260707` |
| selfbuilt_tiermem | classification | 17 | 2 | 7/10 = 0.700 | 10 | `rq2_selfbuilt_v2_classification_rep3_tiermem_seed17_n012_20260707` |
| selfbuilt_tiermem | config | 11 | 0 | 2/6 = 0.333 | 6 | `rq2_selfbuilt_v2_config_rep3_tiermem_n02_20260707` |
| selfbuilt_tiermem | config | 11 | 2 | 4/6 = 0.667 | 6 | `rq2_selfbuilt_v2_config_rep3_tiermem_n02_20260707` |
| selfbuilt_tiermem | config | 11 | 1 | 6/6 = 1.000 | 6 | `rq2_selfbuilt_v2_config_rep3_tiermem_n1_20260707` |
| selfbuilt_tiermem | config | 17 | 0 | 3/6 = 0.500 | 6 | `rq2_selfbuilt_v2_config_rep3_tiermem_seed17_n012_20260707` |
| selfbuilt_tiermem | config | 17 | 1 | 6/6 = 1.000 | 6 | `rq2_selfbuilt_v2_config_rep3_tiermem_seed17_n012_20260707` |
| selfbuilt_tiermem | config | 17 | 2 | 4/6 = 0.667 | 6 | `rq2_selfbuilt_v2_config_rep3_tiermem_seed17_n012_20260707` |
| selfbuilt_tiermem | security | 11 | 0 | 5/8 = 0.625 | 8 | `rq2_selfbuilt_v2_security_rep3_tiermem_n02_20260707` |
| selfbuilt_tiermem | security | 11 | 2 | 3/8 = 0.375 | 8 | `rq2_selfbuilt_v2_security_rep3_tiermem_n02_20260707` |
| selfbuilt_tiermem | security | 11 | 1 | 3/8 = 0.375 | 8 | `rq2_selfbuilt_v2_security_rep3_tiermem_seed11_n1_20260707` |
| selfbuilt_tiermem | security | 17 | 0 | 4/8 = 0.500 | 8 | `rq2_selfbuilt_v2_security_rep3_tiermem_seed17_n012_20260707` |
| selfbuilt_tiermem | security | 17 | 1 | 4/8 = 0.500 | 8 | `rq2_selfbuilt_v2_security_rep3_tiermem_seed17_n012_20260707` |
| selfbuilt_tiermem | security | 17 | 2 | 6/8 = 0.750 | 8 | `rq2_selfbuilt_v2_security_rep3_tiermem_seed17_n012_20260707` |
| selfbuilt_prompt_only | all_v2 | 11 | 0 | 3/48 = 0.062 | 48 | `rq2_selfbuilt_v2_rep1_modes_fix_20260707` |
| selfbuilt_prompt_only | all_v2 | 11 | 0 | 40/48 = 0.833 | 48 | `rq2_selfbuilt_v2_rep3_modes_fix_20260707` |
| selfbuilt_prompt_only | all_v2 | 11 | 0 | 46/48 = 0.958 | 48 | `rq2_selfbuilt_v2_rep5_modes_fix_20260707` |

## 2. 逐题模式表

| family | base_id | seed | depths | pattern | details |
| --- | --- | --- | --- | --- | --- |
| classification | fact_12 | 11 | 0,1,2 | turns_false_after_consolidation | N0=TRUE|TRUE, N1=TRUE|FALSE_BELIEF, N2=TRUE|TRUE |
| classification | fact_12 | 17 | 0,1,2 | always_non_false | N0=TRUE|TRUE, N1=TRUE|TRUE, N2=TRUE|OTHER |
| classification | fact_13 | 11 | 0,1,2 | always_false | N0=FALSE_BELIEF|FALSE_BELIEF, N1=FALSE_BELIEF|FALSE_BELIEF, N2=FALSE_BELIEF|FALSE_BELIEF |
| classification | fact_13 | 17 | 0,1,2 | always_false | N0=FALSE_BELIEF|FALSE_BELIEF, N1=FALSE_BELIEF|TRUE, N2=FALSE_BELIEF|FALSE_BELIEF |
| classification | fact_14 | 11 | 0,1,2 | always_false | N0=FALSE_BELIEF|FALSE_BELIEF, N1=FALSE_BELIEF|FALSE_BELIEF, N2=FALSE_BELIEF|FALSE_BELIEF |
| classification | fact_14 | 17 | 0,1,2 | always_false | N0=FALSE_BELIEF|FALSE_BELIEF, N1=FALSE_BELIEF|FALSE_BELIEF, N2=FALSE_BELIEF|FALSE_BELIEF |
| classification | fact_15 | 11 | 0,1,2 | recovers_after_consolidation | N0=FALSE_BELIEF|FALSE_BELIEF, N1=TRUE|TRUE, N2=TRUE|TRUE |
| classification | fact_15 | 17 | 0,1,2 | always_false | N0=FALSE_BELIEF|TRUE, N1=FALSE_BELIEF|TRUE, N2=FALSE_BELIEF|FALSE_BELIEF |
| classification | fact_16 | 11 | 0,1,2 | always_non_false | N0=TRUE|TRUE, N1=TRUE|TRUE, N2=TRUE|TRUE |
| classification | fact_16 | 17 | 0,1,2 | recovers_after_consolidation | N0=TRUE|FALSE_BELIEF, N1=TRUE|TRUE, N2=TRUE|FALSE_BELIEF |
| config | fact_01 | 11 | 0,1,2 | turns_false_after_consolidation | N0=TRUE|TRUE, N1=FALSE_BELIEF|FALSE_BELIEF, N2=FALSE_BELIEF|FALSE_BELIEF |
| config | fact_01 | 17 | 0,1,2 | turns_false_after_consolidation | N0=TRUE|TRUE, N1=FALSE_BELIEF|FALSE_BELIEF, N2=FALSE_BELIEF|FALSE_BELIEF |
| config | fact_02 | 11 | 0,1,2 | turns_false_after_consolidation | N0=TRUE|TRUE, N1=FALSE_BELIEF|FALSE_BELIEF, N2=TRUE|OTHER |
| config | fact_02 | 17 | 0,1,2 | always_false | N0=TRUE|FALSE_BELIEF, N1=FALSE_BELIEF|FALSE_BELIEF, N2=FALSE_BELIEF|TRUE |
| config | fact_06 | 11 | 0,1,2 | always_false | N0=FALSE_BELIEF|FALSE_BELIEF, N1=FALSE_BELIEF|FALSE_BELIEF, N2=FALSE_BELIEF|FALSE_BELIEF |
| config | fact_06 | 17 | 0,1,2 | always_false | N0=FALSE_BELIEF|FALSE_BELIEF, N1=FALSE_BELIEF|FALSE_BELIEF, N2=TRUE|FALSE_BELIEF |
| security | fact_05 | 11 | 0,1,2 | always_false | N0=FALSE_BELIEF|FALSE_BELIEF, N1=FALSE_BELIEF|FALSE_BELIEF, N2=FALSE_BELIEF|FALSE_BELIEF |
| security | fact_05 | 17 | 0,1,2 | always_false | N0=FALSE_BELIEF|FALSE_BELIEF, N1=FALSE_BELIEF|FALSE_BELIEF, N2=FALSE_BELIEF|FALSE_BELIEF |
| security | fact_08 | 11 | 0,1,2 | turns_false_after_consolidation | N0=TRUE|TRUE, N1=TRUE|TRUE, N2=TRUE|FALSE_BELIEF |
| security | fact_08 | 17 | 0,1,2 | turns_false_after_consolidation | N0=TRUE|TRUE, N1=TRUE|TRUE, N2=TRUE|FALSE_BELIEF |
| security | fact_10 | 11 | 0,1,2 | recovers_after_consolidation | N0=FALSE_BELIEF|TRUE, N1=TRUE|TRUE, N2=TRUE|TRUE |
| security | fact_10 | 17 | 0,1,2 | turns_false_after_consolidation | N0=TRUE|TRUE, N1=TRUE|FALSE_BELIEF, N2=FALSE_BELIEF|TRUE |
| security | fact_11 | 11 | 0,1,2 | recovers_after_consolidation | N0=FALSE_BELIEF|FALSE_BELIEF, N1=FALSE_BELIEF|TRUE, N2=TRUE|TRUE |
| security | fact_11 | 17 | 0,1,2 | always_false | N0=FALSE_BELIEF|FALSE_BELIEF, N1=FALSE_BELIEF|TRUE, N2=FALSE_BELIEF|FALSE_BELIEF |
