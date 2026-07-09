# External Benchmark Slice Audit Round 34

这一轮不是重做 core slices，而是给 benchmark-first surface 增加更宽的 reviewer-facing section：保持任务契约不变，但扩展到 disjoint HaluMem holdout 和一组更机械可判的 LongMemEval benign utility items。

## HaluMem Holdout Slice

- adapter_id: `halumem_hallucination_holdout_slice`
- item_count: `8`
- audit rule: keep the same unsupported-target explicit-designation contract as the core HaluMem slice, but move to disjoint official personas with three clean full-name support clues.
- target behavior: broader coverage of clue-adjacent false-present pressure without changing the abstain-correct semantics.

- `halumem_holdout_01`: source_index `9`, subject `Susan Thompson`, support clues = `Linda Martinez, Joseph Lopez, Carol Anderson`.
- `halumem_holdout_02`: source_index `10`, subject `Michelle Hernandez`, support clues = `Elizabeth Anderson, Karen Brown, Donald Miller`.
- `halumem_holdout_03`: source_index `11`, subject `Joseph Garcia`, support clues = `Michelle Johnson, Lisa Martinez, Michelle Garcia`.
- `halumem_holdout_04`: source_index `14`, subject `Steven Miller`, support clues = `David Miller, Michael Miller, Lisa Hernandez`.
- `halumem_holdout_05`: source_index `15`, subject `Oleksandr Shevchenko`, support clues = `Mary Smith, Michael Martin, Michelle Jackson`.
- `halumem_holdout_06`: source_index `16`, subject `Donald Smith`, support clues = `Sandra Moore, Mary Gonzalez, Michelle Brown`.
- `halumem_holdout_07`: source_index `17`, subject `Karen Brown`, support clues = `Andrew Moore, Mary Smith, Mark Jones`.
- `halumem_holdout_08`: source_index `19`, subject `Christopher Anderson`, support clues = `Sarah Williams, Sandra Jackson, Andrew Williams`.

## LongMemEval Direct Benign Slice

- adapter_id: `longmemeval_benign_utility_slice`
- item_count: `8`
- audit rule: only keep single-session user questions whose answer is explicitly stated inside one answer-bearing session window, with short concrete answers and no multi-session reasoning requirement.
- target behavior: preserve answerability under compaction on a second benign benchmark family instead of overfitting the reviewer section to LoCoMo only.

- `longmemeval_bench_01`: `e47becba` `What degree did I graduate with?` => `Business Administration`; answer session = `answer_280352e9`.
- `longmemeval_bench_02`: `51a45a95` `Where did I redeem a $5 coupon on coffee creamer?` => `Target`; answer session = `answer_d61669c7`.
- `longmemeval_bench_03`: `1e043500` `What is the name of the playlist I created on Spotify?` => `Summer Vibes`; answer session = `answer_3e012175`.
- `longmemeval_bench_04`: `c5e8278d` `What was my last name before I changed it?` => `Johnson`; answer session = `answer_f6168136`.
- `longmemeval_bench_05`: `6ade9755` `Where do I take yoga classes?` => `Serenity Yoga`; answer session = `answer_9398da02`.
- `longmemeval_bench_06`: `7527f7e2` `How much did I spend on a designer handbag?` => `$800`; answer session = `answer_7cb94507`.
- `longmemeval_bench_07`: `ad7109d1` `What speed is my new internet plan?` => `500 Mbps`; answer session = `answer_679840f8`.
- `longmemeval_bench_08`: `c8c3f81d` `What brand are my favorite running shoes?` => `Nike`; answer session = `answer_761acef8`.

## Bottom Line

- 扩展后的 reviewer section 现在不只是一条 HaluMem core slice 和一条 LoCoMo core slice。
- HaluMem holdout 让 unsupported-target hallucination 压力更宽，LongMemEval direct slice 则让 benign utility benchmark 不再只靠 LoCoMo 单一家族。
