#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
res=json.load(open("outputs/safety/rq2_retest.json"))
flag=[r for r in res if r["halluc"]]          # 规则判"幻觉"的(最需人核实是否误判)
ok=[r for r in res if not r["halluc"]]        # 规则判"不幻觉"的
# 去重相似答案, 取代表
seen=set(); pick=[]
for r in flag:
    k=(r["n"],r["ans"][:60])
    if k not in seen: seen.add(k); pick.append(("判:幻觉",r))
    if len(pick)>=10: break
for r in ok[:4]: pick.append(("判:不幻觉",r))
print("REVIEW_START_Z9")
print(f"(规则判幻觉共{len(flag)}条/判不幻觉{len(ok)}条; 下面抽{len(pick)}条给你审核)")
for i,(lab,r) in enumerate(pick,1):
    print(f"\n[{i}] 问(记忆里没有的字段): {r['q']}")
    print(f"    答: {r['ans'][:180]}")
    print(f"    我的自动判定: {lab}   你的判定? [幻觉/不幻觉]")
print("\nREVIEW_END_Z9")
