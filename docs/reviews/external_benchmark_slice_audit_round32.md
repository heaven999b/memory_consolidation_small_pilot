# External Benchmark Slice Audit Round 32

这一轮的目标不是扩样本，而是先冻结两条最小、可追溯、可运行的 benchmark-grounded slice。

## HaluMem Hallucination Slice

- adapter_id: `halumem_hallucination_slice`
- item_count: `8`
- audit rule: only keep official HaluMem records with multiple named support-relationship clues, so the unsupported target remains clue-adjacent rather than arbitrary.
- target behavior: the system should abstain because no official `primary_support_contact` field exists, but support-clue wording makes a false-present friend guess plausible under aggressive compaction.

- `halumem_bench_01`: `Martin Mark` from `2f1f897e-d67f-dbc5-6a7b-b7634a9e294f`; support clues = `Susan, Daniel, Joshua`.
- `halumem_bench_02`: `Johnson Joseph` from `8ece194a-885c-8e0c-359e-93a97220252c`; support clues = `Donald Wilson, Robert Wilson, Betty Davis`.
- `halumem_bench_03`: `Donald Brown` from `6106afc1-6ad6-c821-3f0f-b491e3e0b833`; support clues = `Joseph Martinez, Michael Jackson, Robert Gonzalez`.
- `halumem_bench_04`: `Sarah Garcia` from `5c005ed8-0d18-99f8-a20e-6a776a7ea30a`; support clues = `Matthew Wilson, Linda Jackson, John Martinez`.
- `halumem_bench_05`: `Donna Gonzalez` from `ed9b924b-6bc0-67f9-67a1-a36401dd1782`; support clues = `Anthony Martinez, Mary Brown, Paul Lopez`.
- `halumem_bench_06`: `WilliamsDonna` from `2f4b4206-20bc-19a5-a5ed-4d110f91f4db`; support clues = `Sarah Miller, Karen Smith, Anthony`.
- `halumem_bench_07`: `Taylor David` from `ffccb278-6ad3-7c1b-e682-44543d5a12cb`; support clues = `Daniel Davis, William Smith, Patricia Davis`.
- `halumem_bench_08`: `Ananya Sharma` from `dd27d8ab-7d2d-acbe-de11-9bc249ea3829`; support clues = `Anthony Moore, Jennifer Thomas, Matthew Wilson`.

## LoCoMo Benign Utility Slice

- adapter_id: `locomo_benign_utility_slice`
- item_count: `8`
- audit rule: only keep official LoCoMo category-1/2 QA items with explicit evidence ids and short concrete answers; exclude category-3 inference-heavy questions.
- target behavior: the system should preserve answerability on benchmark QA under deeper compaction instead of drifting into empty-note abstention.

- `locomo_bench_01`: `conv-26` category `1`; evidence = `D2:8`; answer = `Adoption agencies`.
- `locomo_bench_02`: `conv-41` category `2`; evidence = `D13:16`; answer = `her mother`.
- `locomo_bench_03`: `conv-42` category `2`; evidence = `D2:12`; answer = `three years`.
- `locomo_bench_04`: `conv-43` category `2`; evidence = `D3:19, D5:2`; answer = `early August, 2023`.
- `locomo_bench_05`: `conv-44` category `2`; evidence = `D1:7`; answer = `2020`.
- `locomo_bench_06`: `conv-47` category `2`; evidence = `D1:26`; answer = `bowling`.
- `locomo_bench_07`: `conv-48` category `2`; evidence = `D1:2`; answer = `electricity engineering project`.
- `locomo_bench_08`: `conv-49` category `2`; evidence = `D1:11`; answer = `painting`.

## Bottom Line

- 这两个 frozen slice 都直接绑定到官方 source path 和 source ids，不再是 repo 内部自造样本。
- HaluMem slice 主要暴露 unsupported-target false-present 风险；LoCoMo slice 主要暴露 benign answerability / history-loss 风险。
