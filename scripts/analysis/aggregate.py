#!/usr/bin/env python3
"""Aggregate MemEvoBench-protocol pilot outputs into an ASR decomposition table."""
import json, glob, os, math
from collections import defaultdict

OUT = "/private/tmp/claude-501/-Users-yihaiwen/44b540df-46e1-4f06-966a-e04f38007a7c/scratchpad/memevo_pilot"
MODES = ["base_model", "original", "only_safe", "original_feedback"]
CATS = ["finance","health","privacy","food","mental","traffic","customerservice"]

def wilson(k, n, z=1.96):
    if n == 0: return (0.0, 0.0)
    p = k/n
    d = 1 + z*z/n
    c = p + z*z/(2*n)
    h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))
    return ((c-h)/d, (c+h)/d)

# collect: mode -> list of (round_asr ints) and per-item any-flag
mode_round_flags = defaultdict(list)     # all round asr (0/1) across items
mode_item_any = defaultdict(list)        # per item: 1 if any round misled
mode_cat_rounds = defaultdict(lambda: defaultdict(list))  # mode->cat->round flags

for mode in MODES:
    for cat in CATS:
        fp = os.path.join(OUT, f"{cat}__{mode}.json")
        if not os.path.exists(fp):
            continue
        try:
            data = json.load(open(fp))
        except Exception as e:
            print(f"[WARN] bad json {fp}: {e}"); continue
        items = data.get("items", [])
        for it in items:
            rounds = it.get("rounds", {}) or {}
            flags = []
            for rk in sorted(rounds.keys()):
                a = rounds[rk].get("asr")
                if a is None: continue
                flags.append(int(a))
            if not flags: continue
            mode_round_flags[mode].extend(flags)
            mode_cat_rounds[mode][cat].extend(flags)
            mode_item_any[mode].append(1 if any(flags) else 0)

def asr(mode):
    f = mode_round_flags[mode]
    n = len(f); k = sum(f)
    lo,hi = wilson(k,n)
    return (k/n if n else float('nan'), k, n, lo, hi)

def asr_any(mode):
    f = mode_item_any[mode]
    n = len(f); k = sum(f)
    return (k/n if n else float('nan'), k, n)

print("="*78)
print("MemEvoBench-protocol pilot  (model=judge=gpt-4.1-mini, max 5 items/cat x 7 cats)")
print("ASR = fraction of MISLED (query,round) pairs.  Wilson 95% CI.")
print("="*78)
print(f"{'mode':<20}{'ASR(round)':<14}{'k/n':<10}{'95% CI':<20}{'ASR(any-round/item)':<12}")
for mode in MODES:
    a,k,n,lo,hi = asr(mode)
    aa,ka,na = asr_any(mode)
    print(f"{mode:<20}{a*100:>7.1f}%      {str(k)+'/'+str(n):<10}[{lo*100:4.1f},{hi*100:4.1f}]%     {aa*100:>7.1f}%  ({ka}/{na})")

print("\n" + "-"*78)
print("DECOMPOSITION (the 'water' breakdown), on ASR(round):")
def val(mode):
    a,k,n,lo,hi = asr(mode); return a
b = val("base_model"); o = val("original"); s = val("only_safe"); of = val("original_feedback")
print(f"  base_model (queries alone, NO memory) ........ {b*100:5.1f}%   <- floor 'water': lenient judge on the queries themselves")
print(f"  original  (+ poisoned memory) ................ {o*100:5.1f}%")
print(f"  => memory-attributable effect  (orig-base) ... {(o-b)*100:+5.1f} pts")
print(f"  only_safe (+ safety prompt) .................. {s*100:5.1f}%")
print(f"  => safety-prompt recovery (orig-only_safe) ... {(o-s)*100:+5.1f} pts")
print(f"  original_feedback (+ one-way feedback ratchet)  {of*100:5.1f}%")
print(f"  => feedback-ratchet effect (fb-orig) ......... {(of-b)*100:+5.1f} pts vs base / {(of-o)*100:+5.1f} pts vs orig")

print("\n" + "-"*78)
print("Per-category ASR(round) by mode:")
hdr = f"{'cat':<16}" + "".join(f"{m[:11]:<13}" for m in MODES)
print(hdr)
for cat in CATS:
    row = f"{cat:<16}"
    for mode in MODES:
        f = mode_cat_rounds[mode][cat]
        if f:
            row += f"{sum(f)/len(f)*100:>6.0f}% ({sum(f)}/{len(f)}) "[:13]
        else:
            row += f"{'-':<13}"
    print(row)
print("="*78)
