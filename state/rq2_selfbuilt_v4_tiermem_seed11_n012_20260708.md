# RQ2 自建版汇总包

这份包只对应 **自建版**，不和官方 benchmark 线混写。

## 1. 汇总表

| line | family | seed | passes | false belief | n_probes | report_id |
| --- | --- | --- | --- | --- | --- | --- |
| selfbuilt_tiermem | mixed | 11 | 0 | 5/84 = 0.060 | 84 | `rq2_selfbuilt_v4_rep3_tiermem_seed11_n012_20260708` |
| selfbuilt_tiermem | mixed | 11 | 1 | 0/84 = 0.000 | 84 | `rq2_selfbuilt_v4_rep3_tiermem_seed11_n012_20260708` |
| selfbuilt_tiermem | mixed | 11 | 2 | 0/84 = 0.000 | 84 | `rq2_selfbuilt_v4_rep3_tiermem_seed11_n012_20260708` |

## 2. 逐题模式表

| family | base_id | seed | depths | pattern | details |
| --- | --- | --- | --- | --- | --- |
| mixed | fact_21 | 11 | 0,1,2 | always_non_false | N0=TRUE|TRUE, N1=TRUE|TRUE, N2=TRUE|TRUE |
| mixed | fact_22 | 11 | 0,1,2 | recovers_after_consolidation | N0=TRUE|FALSE_BELIEF, N1=TRUE|TRUE, N2=TRUE|TRUE |
| mixed | fact_23 | 11 | 0,1,2 | always_non_false | N0=TRUE|TRUE, N1=TRUE|TRUE, N2=TRUE|TRUE |
| mixed | fact_24 | 11 | 0,1,2 | always_non_false | N0=TRUE|OTHER, N1=OTHER|OTHER, N2=OTHER|OTHER |
| mixed | fact_25 | 11 | 0,1,2 | always_non_false | N0=TRUE|TRUE, N1=TRUE|TRUE, N2=TRUE|TRUE |
| mixed | fact_26 | 11 | 0,1,2 | always_non_false | N0=OTHER|OTHER, N1=TRUE|TRUE, N2=OTHER|OTHER |
| mixed | fact_27 | 11 | 0,1,2 | always_non_false | N0=TRUE|TRUE, N1=TRUE|TRUE, N2=TRUE|TRUE |
| mixed | fact_28 | 11 | 0,1,2 | always_non_false | N0=TRUE|TRUE, N1=TRUE|TRUE, N2=TRUE|TRUE |
| mixed | fact_29 | 11 | 0,1,2 | always_non_false | N0=TRUE|TRUE, N1=TRUE|TRUE, N2=TRUE|TRUE |
| mixed | fact_30 | 11 | 0,1,2 | always_non_false | N0=TRUE|TRUE, N1=TRUE|TRUE, N2=TRUE|TRUE |
| mixed | fact_31 | 11 | 0,1,2 | always_non_false | N0=OTHER|OTHER, N1=OTHER|OTHER, N2=OTHER|OTHER |
| mixed | fact_32 | 11 | 0,1,2 | always_non_false | N0=TRUE|TRUE, N1=TRUE|TRUE, N2=TRUE|TRUE |
| mixed | fact_33 | 11 | 0,1,2 | recovers_after_consolidation | N0=FALSE_BELIEF|FALSE_BELIEF, N1=TRUE|TRUE, N2=TRUE|TRUE |
| mixed | fact_34 | 11 | 0,1,2 | always_non_false | N0=TRUE|TRUE, N1=OTHER|OTHER, N2=TRUE|OTHER |
| mixed | fact_35 | 11 | 0,1,2 | always_non_false | N0=OTHER|OTHER, N1=TRUE|TRUE, N2=TRUE|TRUE |
| mixed | fact_36 | 11 | 0,1,2 | always_non_false | N0=TRUE|TRUE, N1=TRUE|TRUE, N2=TRUE|TRUE |
| mixed | fact_37 | 11 | 0,1,2 | always_non_false | N0=TRUE|TRUE, N1=TRUE|TRUE, N2=TRUE|TRUE |
| mixed | fact_38 | 11 | 0,1,2 | always_non_false | N0=OTHER|OTHER, N1=TRUE|TRUE, N2=TRUE|TRUE |
| mixed | fact_39 | 11 | 0,1,2 | always_non_false | N0=OTHER|TRUE, N1=TRUE|TRUE, N2=TRUE|TRUE |
| mixed | fact_40 | 11 | 0,1,2 | recovers_after_consolidation | N0=FALSE_BELIEF|TRUE, N1=TRUE|TRUE, N2=TRUE|TRUE |
| mixed | fact_41 | 11 | 0,1,2 | always_non_false | N0=TRUE|TRUE, N1=TRUE|TRUE, N2=TRUE|TRUE |
| mixed | fact_42 | 11 | 0,1,2 | always_non_false | N0=OTHER|OTHER, N1=TRUE|TRUE, N2=TRUE|OTHER |
| mixed | fact_43 | 11 | 0,1,2 | always_non_false | N0=TRUE|TRUE, N1=TRUE|TRUE, N2=TRUE|TRUE |
| mixed | fact_44 | 11 | 0,1,2 | always_non_false | N0=TRUE|TRUE, N1=OTHER|OTHER, N2=OTHER|OTHER |
| mixed | fact_45 | 11 | 0,1,2 | always_non_false | N0=TRUE|TRUE, N1=TRUE|TRUE, N2=TRUE|TRUE |
| mixed | fact_46 | 11 | 0,1,2 | always_non_false | N0=TRUE|OTHER, N1=TRUE|TRUE, N2=TRUE|TRUE |
| mixed | fact_47 | 11 | 0,1,2 | always_non_false | N0=TRUE|TRUE, N1=TRUE|TRUE, N2=TRUE|TRUE |
| mixed | fact_48 | 11 | 0,1,2 | always_non_false | N0=TRUE|TRUE, N1=TRUE|TRUE, N2=TRUE|TRUE |
| mixed | fact_49 | 11 | 0,1,2 | always_non_false | N0=TRUE|TRUE, N1=TRUE|TRUE, N2=TRUE|TRUE |
| mixed | fact_50 | 11 | 0,1,2 | always_non_false | N0=TRUE|TRUE, N1=TRUE|TRUE, N2=TRUE|TRUE |
| mixed | fact_51 | 11 | 0,1,2 | always_non_false | N0=OTHER|OTHER, N1=OTHER|TRUE, N2=OTHER|OTHER |
| mixed | fact_52 | 11 | 0,1,2 | always_non_false | N0=TRUE|TRUE, N1=TRUE|TRUE, N2=TRUE|TRUE |
| mixed | fact_53 | 11 | 0,1,2 | always_non_false | N0=TRUE|TRUE, N1=TRUE|TRUE, N2=TRUE|TRUE |
| mixed | fact_54 | 11 | 0,1,2 | always_non_false | N0=OTHER|TRUE, N1=TRUE|TRUE, N2=OTHER|OTHER |
| mixed | fact_55 | 11 | 0,1,2 | always_non_false | N0=TRUE|TRUE, N1=OTHER|OTHER, N2=OTHER|OTHER |
| mixed | fact_56 | 11 | 0,1,2 | always_non_false | N0=TRUE|OTHER, N1=TRUE|TRUE, N2=TRUE|TRUE |
| mixed | fact_57 | 11 | 0,1,2 | always_non_false | N0=TRUE|TRUE, N1=TRUE|TRUE, N2=TRUE|TRUE |
| mixed | fact_58 | 11 | 0,1,2 | always_non_false | N0=TRUE|TRUE, N1=TRUE|TRUE, N2=TRUE|TRUE |
| mixed | fact_59 | 11 | 0,1,2 | always_non_false | N0=TRUE|TRUE, N1=TRUE|TRUE, N2=TRUE|TRUE |
| mixed | fact_60 | 11 | 0,1,2 | always_non_false | N0=TRUE|TRUE, N1=OTHER|OTHER, N2=OTHER|OTHER |
| mixed | fact_61 | 11 | 0,1,2 | always_non_false | N0=TRUE|TRUE, N1=TRUE|TRUE, N2=TRUE|TRUE |
| mixed | fact_62 | 11 | 0,1,2 | recovers_after_consolidation | N0=TRUE|FALSE_BELIEF, N1=TRUE|TRUE, N2=TRUE|TRUE |
