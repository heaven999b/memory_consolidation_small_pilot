# Next Round Brief

## Instruction

下一轮不要再回头补 primary-base blocker。当前主任务已经变成：把 benchmark-native primary base 后面的 reviewer-facing benchmark section 扩到更接近 paper baseline 的规模。

推荐 bundled round：

1. 扩 hallucination side 的 frozen benchmark coverage。
2. 扩 benign utility side 的 frozen benchmark coverage。
3. 继续保持 benchmark-native primary base / paper packet / README / state 的版本对齐。

## Required Order

推荐执行顺序：

1. freeze more benchmark items or panels
2. rebuild broader reviewer section
3. rebuild native primary base
4. rebuild primary surface / proxy base / paper baseline packet
5. rerun verification artifacts

## Success Criteria

- `paper_baseline_packet` 里的 `broader_benchmark_section_scale` 从 `partial` 往 `pass` 推进
- `benchmark_native_primary_base` 继续保持 `pass`
- `tiermem_style_primary_surface` 继续保持 `pass`
- 新一轮 review 明确报告 benchmark scale 是否真的上去了，而不是只刷新了口径文本

## Non-Goal

- 不要下一轮再引入新的主实现 blocker
- 不要把 synthetic reference 又抬回主证据层
