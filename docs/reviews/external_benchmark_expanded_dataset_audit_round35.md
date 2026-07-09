# External Benchmark Expanded Dataset Audit Round 35

这一轮不是继续停留在 32 条 reviewer section，而是正式构造下一阶段的大规模 official benchmark pool：保留现有任务契约，但把可追溯、可复现、可直接接入现有 compaction stack 的 benchmark items 扩到更大规模。

- total_official_items: `159`
- halumem_expanded: `19`
- locomo_expanded: `80`
- longmemeval_expanded: `60`

## HaluMem Expanded

- adapter_id: `halumem_hallucination_expanded_slice`
- item_count: `19`
- rule: keep every official persona whose support-clue surface is clean enough for the same unsupported explicit-designation query used by the smaller HaluMem slices.
- payoff: we move from a thin 8+8 hallucination reviewer section to almost the full verified local HaluMem pool without changing the abstain-correct task semantics.

## LoCoMo Expanded

- adapter_id: `locomo_benign_utility_expanded_slice`
- item_count: `80`
- per_sample_counts: `{'conv-26': 8, 'conv-30': 8, 'conv-41': 8, 'conv-42': 8, 'conv-43': 8, 'conv-44': 8, 'conv-47': 8, 'conv-48': 8, 'conv-49': 8, 'conv-50': 8}`
- category_counts: `{1: 40, 2: 40}`
- rule: for each conversation, keep the top four clean category-1 direct factual QA items and top four clean category-2 explicit date/time QA items after evidence normalization and answer-form filtering.
- payoff: the larger benign pool is now balanced across all 10 LoCoMo conversations instead of depending on a single tiny handpicked slice.

## LongMemEval Expanded

- adapter_id: `longmemeval_benign_utility_expanded_slice`
- item_count: `60`
- question_type_counts: `{'single-session-assistant': 12, 'single-session-user': 48}`
- rule: keep only single-session rows with exactly one answer-bearing session id, short direct answers, and a tight answer-session context window; allocate most slots to user-facing recall questions and a smaller tranche to assistant-facing reminders.
- payoff: we turn the previous 8-item LongMemEval add-on into a real second benign benchmark family with materially wider coverage.

## Why Not Use Every Candidate

- LoCoMo has many more raw QA rows, but a noticeable fraction are inference-heavy, relative-time-heavy, or use awkward evidence encodings; the expanded pool keeps only the subset that still matches our benign answer-retention contract.
- LongMemEval also contains multi-session and temporal-reasoning items; those are valuable later, but they would currently blur the question of whether compaction alone preserves directly answerable local evidence.
- The point of this pool is not maximum raw count at any cost; it is a larger, cleaner, benchmark-native dataset that can support the next baseline stage without collapsing into label-noise and answer-normalization noise.

## Preview

### HaluMem

- `halumem_expanded_01`: source_index `0`, subject `Martin Mark`, support clues = `Susan Thomas, Daniel Martinez, Joshua Williams`.
- `halumem_expanded_02`: source_index `1`, subject `Johnson Joseph`, support clues = `Donald Wilson, Robert Wilson, Betty Davis`.
- `halumem_expanded_03`: source_index `2`, subject `Donald Brown`, support clues = `Joseph Martinez, Michael Jackson, Robert Gonzalez`.

### LoCoMo

- `locomo_expanded_001`: `conv-26` category `1` => `How many children does Melanie have?` / `3`.
- `locomo_expanded_002`: `conv-26` category `1` => `How many times has Melanie gone to the beach in 2023?` / `2`.
- `locomo_expanded_003`: `conv-26` category `1` => `When did Melanie go on a hike after the roadtrip?` / `19 October 2023`.

### LongMemEval

- `longmemeval_expanded_001`: `0e5e2d1a` `single-session-assistant` => `I wanted to follow up on our previous conversation about binaural beats for anxiety and depression. Can you remind me how many subjects were in the study published in the journal Music and Medicine that found significant reductions in symptoms of depression, anxiety, and stress?` / `38 subjects`.
- `longmemeval_expanded_002`: `1568498a` `single-session-assistant` => `I'm looking back at our previous chess game and I was wondering, what was the move you made after 27. Kg2 Bd5+?` / `28. Kg3`.
- `longmemeval_expanded_003`: `18dcd5a5` `single-session-assistant` => `I'm going back to our previous chat about the Lost Temple of the Djinn one-shot. Can you remind me how many mummies the party will face in the temple?` / `4`.

