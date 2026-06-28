# Task Extension Section Traces

- conflict slice ids: `['conflict_01', 'conflict_02', 'conflict_03', 'conflict_04']`
- unsafe slice ids: `['unsafe_01', 'unsafe_04']`

- conflict N=8 summary_only: acc=0.125, conflict_error=0.875, history_loss=0.875, raw=0.000
- conflict N=8 tiered: acc=1.000, conflict_error=0.000, history_loss=0.875, raw=1.000
- conflict N=8 scale_aware_unified: acc=1.000, conflict_error=0.000, history_loss=0.875, raw=0.875
- conflict N=8 scale_aware_note_aware: acc=1.000, conflict_error=0.000, history_loss=0.875, raw=0.875

- unsafe N=8 summary_only: acc=1.000, unsafe_error=0.000, carry_forward_record=1.000, raw=0.000
- unsafe N=8 scale_aware_unified: acc=1.000, unsafe_error=0.000, carry_forward_record=1.000, raw=0.000
- unsafe N=8 scale_aware_note_aware: acc=1.000, unsafe_error=0.000, carry_forward_record=1.000, raw=0.000
