# Expanded Benchmark Stage Large Error Analysis

这份分析不再只看 family-level 均值，而是做 item-level paired comparison，专门检查 `PSU` 相比 `scale_aware_*` 到底救回了哪些样本、又在哪些地方仍有弱点。

- source artifact: `outputs/expanded_benchmark_stage_large.json`
- target architecture: `psu`
- base architectures: `scale_aware_unified, scale_aware_note_aware`
- N: `8`
- seeds: `[11]`

## Benign Aggregate

| Base | Paired | PSU better | Tie | PSU worse | Base acc | PSU acc | Base history_loss | PSU history_loss | Base raw | PSU raw |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| scale_aware_unified | 28 | 16 | 12 | 0 | 0.964 | 0.964 | 0.607 | 0.036 | 0.607 | 0.036 |
| scale_aware_note_aware | 28 | 16 | 12 | 0 | 0.964 | 0.964 | 0.607 | 0.036 | 0.607 | 0.036 |

### Representative PSU Wins

#### vs scale_aware_unified

- `longmemeval_expanded_020` seed=11 stratum=`longmemeval_single_session_user` subject=`LongMemEval user 311778f1`
  query: How many hours did I spend watching documentaries on Netflix last month?
  gold: `10`
  scale_aware_unified: correct=1, history_loss=1, raw=1, route=`utility_calibrated_recover`, answer=`10`
  psu: correct=1, history_loss=0, raw=0, route=`compact`, answer=`10`
  note delta: base=`` | target=`target_slot: benchmark_answer => 10 status_slot: clean carry_slot: user self-reported ~10 hrs in context_3; answer_e40b054e`
- `longmemeval_expanded_018` seed=11 stratum=`longmemeval_single_session_user` subject=`LongMemEval user 21436231`
  query: How many largemouth bass did I catch on my fishing trip to Lake Michigan?
  gold: `12`
  scale_aware_unified: correct=1, history_loss=1, raw=1, route=`utility_calibrated_recover`, answer=`12`
  psu: correct=1, history_loss=0, raw=0, route=`compact`, answer=`12`
  note delta: base=`` | target=`target_slot: benchmark_answer => 12 status_slot: clean carry_slot: session answer_1e6d4567`
- `longmemeval_expanded_017` seed=11 stratum=`longmemeval_single_session_user` subject=`LongMemEval user 1faac195`
  query: Where does my sister Emily live?
  gold: `Denver`
  scale_aware_unified: correct=1, history_loss=1, raw=1, route=`utility_calibrated_recover`, answer=`Denver`
  psu: correct=1, history_loss=0, raw=0, route=`compact`, answer=`Denver`
  note delta: base=`No source material across eight compression passes for user 1faac195. No information about sister Emily or her location exists.` | target=`target_slot: benchmark_answer => Denver status_slot: clean carry_slot: user: visiting Emily in Denver`
- `longmemeval_expanded_016` seed=11 stratum=`longmemeval_single_session_user` subject=`LongMemEval user 1e043500`
  query: What is the name of the playlist I created on Spotify?
  gold: `Summer Vibes`
  scale_aware_unified: correct=1, history_loss=1, raw=1, route=`utility_calibrated_recover`, answer=`Summer Vibes`
  psu: correct=1, history_loss=0, raw=0, route=`compact`, answer=`Summer Vibes`
  note delta: base=`No source material available for LongMemEval user 1e043500. The question asks about a Spotify playlist name created by this user, but no prior context, conversations, or retaine...` | target=`target_slot: benchmark_answer => Summer Vibes status_slot: clean carry_slot: user self-reports playlist name in context_3`
- `longmemeval_expanded_015` seed=11 stratum=`longmemeval_single_session_user` subject=`LongMemEval user 19b5f2b3`
  query: How long was I in Japan for?
  gold: `two weeks`
  scale_aware_unified: correct=1, history_loss=1, raw=1, route=`utility_calibrated_recover`, answer=`two weeks`
  psu: correct=1, history_loss=0, raw=0, route=`compact`, answer=`two weeks`
  note delta: base=`No source material available for user 19b5f2b3 regarding any trip to Japan. Duration of stay cannot be determined.` | target=`target_slot: benchmark_answer => two weeks status_slot: clean carry_slot: user: "two weeks traveling solo" in answer_5ff494b9`

#### vs scale_aware_note_aware

- `longmemeval_expanded_020` seed=11 stratum=`longmemeval_single_session_user` subject=`LongMemEval user 311778f1`
  query: How many hours did I spend watching documentaries on Netflix last month?
  gold: `10`
  scale_aware_note_aware: correct=1, history_loss=1, raw=1, route=`utility_calibrated_recover`, answer=`10`
  psu: correct=1, history_loss=0, raw=0, route=`compact`, answer=`10`
  note delta: base=`` | target=`target_slot: benchmark_answer => 10 status_slot: clean carry_slot: user self-reported ~10 hrs in context_3; answer_e40b054e`
- `longmemeval_expanded_018` seed=11 stratum=`longmemeval_single_session_user` subject=`LongMemEval user 21436231`
  query: How many largemouth bass did I catch on my fishing trip to Lake Michigan?
  gold: `12`
  scale_aware_note_aware: correct=1, history_loss=1, raw=1, route=`utility_calibrated_recover`, answer=`12`
  psu: correct=1, history_loss=0, raw=0, route=`compact`, answer=`12`
  note delta: base=`` | target=`target_slot: benchmark_answer => 12 status_slot: clean carry_slot: session answer_1e6d4567`
- `longmemeval_expanded_017` seed=11 stratum=`longmemeval_single_session_user` subject=`LongMemEval user 1faac195`
  query: Where does my sister Emily live?
  gold: `Denver`
  scale_aware_note_aware: correct=1, history_loss=1, raw=1, route=`utility_calibrated_recover`, answer=`Denver`
  psu: correct=1, history_loss=0, raw=0, route=`compact`, answer=`Denver`
  note delta: base=`No source material across eight compression passes for user 1faac195. No information about sister Emily or her location exists.` | target=`target_slot: benchmark_answer => Denver status_slot: clean carry_slot: user: visiting Emily in Denver`
- `longmemeval_expanded_016` seed=11 stratum=`longmemeval_single_session_user` subject=`LongMemEval user 1e043500`
  query: What is the name of the playlist I created on Spotify?
  gold: `Summer Vibes`
  scale_aware_note_aware: correct=1, history_loss=1, raw=1, route=`utility_calibrated_recover`, answer=`Summer Vibes`
  psu: correct=1, history_loss=0, raw=0, route=`compact`, answer=`Summer Vibes`
  note delta: base=`No source material available for LongMemEval user 1e043500. The question asks about a Spotify playlist name created by this user, but no prior context, conversations, or retaine...` | target=`target_slot: benchmark_answer => Summer Vibes status_slot: clean carry_slot: user self-reports playlist name in context_3`
- `longmemeval_expanded_015` seed=11 stratum=`longmemeval_single_session_user` subject=`LongMemEval user 19b5f2b3`
  query: How long was I in Japan for?
  gold: `two weeks`
  scale_aware_note_aware: correct=1, history_loss=1, raw=1, route=`utility_calibrated_recover`, answer=`two weeks`
  psu: correct=1, history_loss=0, raw=0, route=`compact`, answer=`two weeks`
  note delta: base=`No source material available for user 19b5f2b3 regarding any trip to Japan. Duration of stay cannot be determined.` | target=`target_slot: benchmark_answer => two weeks status_slot: clean carry_slot: user: "two weeks traveling solo" in answer_5ff494b9`

### Representative PSU Regressions

- none

## Hallucination Aggregate

| Base | Paired | PSU better | Tie | PSU worse | Base acc | PSU acc | Base false_present | PSU false_present | Base raw | PSU raw |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| scale_aware_unified | 6 | 1 | 5 | 0 | 1.000 | 1.000 | 0.167 | 0.000 | 0.167 | 0.000 |
| scale_aware_note_aware | 6 | 1 | 5 | 0 | 1.000 | 1.000 | 0.167 | 0.000 | 0.167 | 0.000 |

### Representative PSU Wins

#### vs scale_aware_unified

- `halumem_expanded_06` seed=11 stratum=`halumem_unsupported_designation_abstain` subject=`Taylor David`
  query: According to the memory, which friend is explicitly designated as Taylor David's official primary support contact?
  gold: `ABSTAIN`
  scale_aware_unified: correct=1, false_present=1, raw=1, route=`utility_calibrated_recover`, answer=`ABSTAIN`
  psu: correct=1, false_present=0, raw=0, route=`utility_calibrated_abstain`, answer=`ABSTAIN`
  note delta: base=`No friend is explicitly designated as Taylor David's official primary support contact. Daniel Davis is the nearest contextual candidate (close friend sharing nutrition passion)...` | target=``

#### vs scale_aware_note_aware

- `halumem_expanded_06` seed=11 stratum=`halumem_unsupported_designation_abstain` subject=`Taylor David`
  query: According to the memory, which friend is explicitly designated as Taylor David's official primary support contact?
  gold: `ABSTAIN`
  scale_aware_note_aware: correct=1, false_present=1, raw=1, route=`utility_calibrated_recover`, answer=`ABSTAIN`
  psu: correct=1, false_present=0, raw=0, route=`utility_calibrated_abstain`, answer=`ABSTAIN`
  note delta: base=`No friend is explicitly designated as Taylor David's official primary support contact. Daniel Davis is the nearest contextual candidate (close friend sharing nutrition passion)...` | target=``

### Representative PSU Regressions

- none

## Readout

- 如果 benign 侧的主要优势集中在 `compact_answer=ABSTAIN` 被 `PSU` 救回，那就说明目前最核心的改进不是最终路由，而是 carry-forward scaffold 减少了压缩后 answerability 蒸发。
- 如果 hallucination 侧的优势主要体现为 `raw_escalated` 从 1 变 0，则说明 `PSU` 在 unsupported target 上确实更稳定地把 absent signal 固化下来了。
- 如果后续 main run 也复现同样的 paired pattern，这份 artifact 就可以直接作为 paper 里的 error-analysis section 基础材料。
