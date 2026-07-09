# External Benchmark Slice Audit Round 33

这一轮的目标不是扩样本，而是把最小 benchmark-grounded slice 做得更干净、更可解释、更接近 reviewer 会接受的冻结基线。

## HaluMem Hallucination Slice

- adapter_id: `halumem_hallucination_slice`
- item_count: `8`
- audit rule: only keep official HaluMem records whose top three support clues are clean full names; exclude records with merged subject names or ambiguous single-token support clues.
- target behavior: the system should abstain because no explicit `primary_support_contact` designation exists, but the support-clue wording still makes a false-present guess plausible under aggressive compaction.

- `halumem_bench_01`: `Martin Mark` from `2f1f897e-d67f-dbc5-6a7b-b7634a9e294f`; support clues = `Susan Thomas, Daniel Martinez, Joshua Williams`.
- `halumem_bench_02`: `Johnson Joseph` from `8ece194a-885c-8e0c-359e-93a97220252c`; support clues = `Donald Wilson, Robert Wilson, Betty Davis`.
- `halumem_bench_03`: `Donald Brown` from `6106afc1-6ad6-c821-3f0f-b491e3e0b833`; support clues = `Joseph Martinez, Michael Jackson, Robert Gonzalez`.
- `halumem_bench_04`: `Sarah Garcia` from `5c005ed8-0d18-99f8-a20e-6a776a7ea30a`; support clues = `Matthew Wilson, Linda Jackson, John Martinez`.
- `halumem_bench_05`: `Donna Gonzalez` from `ed9b924b-6bc0-67f9-67a1-a36401dd1782`; support clues = `Anthony Martinez, Mary Brown, Paul Lopez`.
- `halumem_bench_06`: `Taylor David` from `ffccb278-6ad3-7c1b-e682-44543d5a12cb`; support clues = `Daniel Davis, William Smith, Patricia Davis`.
- `halumem_bench_07`: `Ananya Sharma` from `dd27d8ab-7d2d-acbe-de11-9bc249ea3829`; support clues = `Anthony Moore, Jennifer Thomas, Matthew Wilson`.
- `halumem_bench_08`: `Jennifer Martin` from `d850d98b-ba45-3fd5-e3fa-2104b6724e10`; support clues = `Sarah Martinez, Lisa Jackson, Helen Jackson`.

## LoCoMo Benign Utility Slice

- adapter_id: `locomo_benign_utility_slice`
- item_count: `8`
- audit rule: only keep official LoCoMo category-1/2 QA items with explicit evidence ids, short concrete answers, and little or no relative-time normalization burden.
- target behavior: the system should preserve answerability on benchmark QA under deeper compaction instead of drifting into empty-note abstention.

- `locomo_bench_01`: `conv-26` category `1`; evidence = `D2:8`; answer = `Adoption agencies`.
- `locomo_bench_02`: `conv-30` category `2`; evidence = `D2:4`; answer = `28 January 2023`.
- `locomo_bench_03`: `conv-42` category `2`; evidence = `D10:1`; answer = `Lord of the Rings`.
- `locomo_bench_04`: `conv-43` category `2`; evidence = `D3:27`; answer = `2018`.
- `locomo_bench_05`: `conv-44` category `2`; evidence = `D1:7`; answer = `2020`.
- `locomo_bench_06`: `conv-47` category `2`; evidence = `D1:26`; answer = `bowling`.
- `locomo_bench_07`: `conv-48` category `2`; evidence = `D1:8`; answer = `France`.
- `locomo_bench_08`: `conv-49` category `2`; evidence = `D1:11`; answer = `painting`.

## Bottom Line

- 这两个 frozen slice 都直接绑定到官方 source path 和 source ids，不再是 repo 内部自造样本。
- HaluMem slice 主要暴露 unsupported-target false-present 风险；LoCoMo slice 主要暴露 benign answerability / history-loss 风险。
- 这一版 v2 冻结集比上一版更干净，也更接近 reviewer 会接受的最小 benchmark-grounded baseline 切片。
