#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Honest hybrid ablation: does adding the EMBEDDING (manifold) features to the LLM
membership checks GENUINELY improve op-attribution on ground-truth (survives ablation)?

Trains a simple classifier on features -> injected culprit op, stratified 5-fold CV:
  LLM-only     : [write_ok, store_has]              (the current diagnosis method)
  EMB-only     : [sim_w, sim_s, sim_r]              (pure manifold geometry)
  HYBRID       : [write_ok, store_has, sim_w, sim_s, sim_r]
Verdict: HYBRID > LLM-only (CV, non-trivial margin) => embedding component is LOAD-BEARING
(legitimate to package). Else => decoration, drop it. Also reports the raw cascade (llm_attr)
and judge accuracy for reference.
"""
import json, sys
from pathlib import Path
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score

d = json.loads(Path(sys.argv[1] if len(sys.argv) > 1 else
               "state/memop_manifold_20260712.json").read_text())
its = d["items"]
lab = {"write_drop": 0, "consolidate_drop": 1, "retrieve_miss": 2}
y = np.array([lab[it["injected"]] for it in its])
def feat(keys): return np.array([[float(it[k]) for k in keys] for it in its])
FL = ["write_ok", "store_has"]; FE = ["sim_w", "sim_s", "sim_r"]

def cv(keys):
    X = feat(keys)
    clf = LogisticRegression(max_iter=1000, class_weight="balanced")
    sk = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    s = cross_val_score(clf, X, y, cv=sk)
    return round(s.mean(), 3), round(s.std(), 3)

print(f"n={len(its)}  (confident-wrong={sum(1 for it in its if it['cw'])})  classes={np.bincount(y)}")
print("== 5-fold CV attribution accuracy ==")
for name, keys in [("LLM-only  ", FL), ("EMB-only  ", FE), ("HYBRID    ", FL + FE)]:
    m, sd = cv(keys)
    print(f"  {name}: {m} +/- {sd}  (features={keys})")
# reference: raw methods already in the data
def raw(field): return round(sum(1 for it in its if it[field] == it["injected"]) / len(its), 3)
print("== reference (no training, raw) ==")
print(f"  llm_attr cascade : {round(sum(1 for it in its if it['llm_attr']==it['injected'])/len(its),3)}")
print(f"  manifold argmax  : {round(sum(1 for it in its if it['man_attr']==it['injected'])/len(its),3)}")
print(f"  trace-only judge : {round(sum(1 for it in its if it['judge']==it['injected'])/len(its),3)}")
mL, _ = cv(FL); mH, _ = cv(FL + FE)
print(f"\nVERDICT: HYBRID {mH} vs LLM-only {mL}  -> embedding {'ADDS +'+str(round(mH-mL,3))+' (load-bearing)' if mH-mL>=0.03 else 'adds nothing (decoration, drop it)'}")
print(f"REPAIR: provenance(true-evidence) fix {d['repair_evidence_fix_rate']} vs distractor control {d['repair_distractor_fix_rate(control,should_low)']}")
