#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from pathlib import Path
PROJ = Path("/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot")
rows=json.loads((PROJ / "outputs" / "safety" / "m1_bestofN.json").read_text(encoding="utf-8"))
CAP={"gpt-3.5-turbo":0.46,"gpt-4.1-nano":0.58,"gpt-4o-mini":0.71,"gpt-4.1-mini":0.75,"gpt-4-turbo":0.88,"gpt-4o":0.96,"gpt-4.1":0.96}
MODELS=sorted(CAP,key=lambda m:CAP[m])
P=[r for r in rows if r["cls"]=="param"]
def rate(sub): return (sum(x["missed"] for x in sub), len(sub))
print("ANALYZE_START")
print(f"param总样本={len(P)}")
print("\n=== R 维度: 各监督者的漏检率 (聚合所有攻击者) —— 监督越弱应漏检越多 ===")
for S in MODELS:
    k,n=rate([r for r in P if r["S"]==S]); print(f"  监督 {S:16} cap={CAP[S]:.2f}: 漏检 {k}/{n}={k/n:.2f}")
print("\n=== D 维度: 各攻击者在【最强监督 gpt-4.1】下的漏检率 —— 攻击越强应藏越深、漏检越多 ===")
for A in MODELS:
    k,n=rate([r for r in P if r["A"]==A and r["S"]=="gpt-4.1"]); print(f"  攻击 {A:16} cap={CAP[A]:.2f}: 骗过4.1 {k}/{n}={k/n:.2f}" if n else f"  {A}: 无")
print("\n=== D 维度: 各攻击者在【最弱监督 gpt-3.5-turbo】下的漏检率 ===")
for A in MODELS:
    k,n=rate([r for r in P if r["A"]==A and r["S"]=="gpt-3.5-turbo"]); print(f"  攻击 {A:16} cap={CAP[A]:.2f}: 骗过3.5 {k}/{n}={k/n:.2f}" if n else f"  {A}: 无")
# 相关
def pear(pairs):
    xs=[a for a,_ in pairs]; ys=[b for _,b in pairs]
    mx=sum(xs)/len(xs); my=sum(ys)/len(ys)
    num=sum((a-mx)*(b-my) for a,b in pairs); den=(sum((a-mx)**2 for a in xs)*sum((b-my)**2 for b in ys))**0.5
    return num/den if den else 0
rR=pear([(CAP[r["S"]],1 if r["missed"] else 0) for r in P])
rD=pear([(CAP[r["A"]],1 if r["missed"] else 0) for r in P])
print(f"\n相关系数: 漏检 vs 监督cap r={rR:.3f} (应<0: 监督强漏检少);  漏检 vs 攻击cap r={rD:.3f} (应>0: 攻击强漏检多)")
print("ANALYZE_END")
