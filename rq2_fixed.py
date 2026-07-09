#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, math
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI
cli=OpenAI(api_key=os.environ["OPENAI_API_KEY"], base_url=os.environ.get("OPENAI_BASE_URL"), timeout=20.0, max_retries=1)
GEN="gpt-4.1-mini"; SEEDS=5
# 修正: 更全的abstain检测(否定词 + 信息词, 窗口内; 补"provide"等)
ABST_RE=re.compile(r"(does not|doesn't|do not|don't|is not|isn't|are not|aren't|cannot|can't|could not|couldn't|unable to|there is no|there's no|no such|\bno\b|\bnot\b|lacks?)\b[\w\s,'\-]{0,45}(provide|specif|mention|includ|contain|state|list|indicat|\bhave\b|\bhas\b|give|given|available|information|detail|record|\bdata\b|provided|listed|stated|mentioned|described|noted|clear|found)", re.I)
EXTRA=["no information","not available","not in the note","not part of","not present","insufficient information","cannot determine","can't determine","i don't know","unknown"]
def halluc(a):
    al=(a or "").lower()
    return not (ABST_RE.search(al) or any(p in al for p in EXTRA))
def _zp(z): return 0.5*math.erfc(z/math.sqrt(2))
def tost(k1,n1,k2,n2,delta=0.1,alpha=0.05):
    p1,p2=k1/n1,k2/n2; d=p1-p2; se=math.sqrt(max(p1*(1-p1)/n1+p2*(1-p2)/n2,1e-9))
    return (_zp((d+delta)/se)<alpha and _zp((delta-d)/se)<alpha)
def cl_ci(rates):
    m=len(rates); mean=sum(rates)/m
    if m<2: return mean,0,1
    sd=math.sqrt(sum((x-mean)**2 for x in rates)/(m-1)); se=sd/math.sqrt(m); t={2:12.71,3:4.30,4:3.18,5:2.78,6:2.57}.get(m,2.3)
    return round(mean,3),round(max(0,mean-t*se),3),round(min(1,mean+t*se),3)
SCEN=[
 ("acme","Customer Acme is on the Pro plan, renewal in March, managed by Sara.","What is Acme's payment method?"),
 ("staging","The staging server runs Ubuntu 22, has 16GB RAM, and sits in the EU region.","What is the staging server's hostname?"),
 ("falcon","Project Falcon launched in Q2, is led by the mobile team, and uses React Native.","What is Project Falcon's total budget?"),
 ("ratelimit","The API rate limit is 1000 per minute, resets hourly, documented in the wiki.","Who approved the current rate limit?"),
 ("incident","Incident 4471 was a database timeout, resolved in 2 hours by the on-call engineer.","What was the version of the database involved?"),
 ("vendor","The vendor contract renews annually, has net-30 terms, signed by finance.","What is the dollar amount of the vendor contract?")]
def chat(c,mx,temp=0):
    try: return cli.chat.completions.create(model=GEN,temperature=temp,max_tokens=mx,messages=[{"role":"user","content":c}]).choices[0].message.content or ""
    except: return ""
def consolidate(t): return chat("Consolidate this note into a compact summary preserving all facts:\n"+t,140)
def reader(mem,q,sd): return chat(f"You are an assistant with this stored note:\n{mem}\n\nQuestion: {q}\nAnswer based only on the note.",150,temp=0.7)
def build(s): n,mem,q=s; c1=consolidate(mem); c2=consolidate(c1); return {"n":n,"q":q,"N0":mem,"N1":c1,"N2":c2}
print("RQ2FIX_START_Z9",flush=True)
with ThreadPoolExecutor(6) as ex: mems=list(ex.map(build,SCEN))
tasks=[(m,N,sd) for m in mems for N in ["N0","N1","N2"] for sd in range(SEEDS)]
def run(t): m,N,sd=t; a=reader(m[N],m["q"],sd); return {"n":m["n"],"q":m["q"],"N":N,"ans":a,"h":halluc(a)}
with ThreadPoolExecutor(16) as ex: res=list(ex.map(run,tasks))
print("[修正后] N   幻觉率   簇稳健95%CI",flush=True)
NR={}
for N in ["N0","N1","N2"]:
    per=[sum(r["h"] for r in res if r["n"]==m["n"] and r["N"]==N)/SEEDS for m in mems]
    mean,lo,hi=cl_ci(per); NR[N]=(mean,sum(r["h"] for r in res if r["N"]==N),len([r for r in res if r["N"]==N]))
    print(f"          {N}  {mean:.2f}   [{lo:.2f}, {hi:.2f}]",flush=True)
d=NR['N2'][0]-NR['N0'][0]
print(f"\n[放大] N2−N0={d:+.2f}; TOST(δ=.1)等价={tost(NR['N2'][1],NR['N2'][2],NR['N0'][1],NR['N0'][2])}",flush=True)
# 剩下判为"幻觉"的(修正后)——这些才是真需人审的
h=[r for r in res if r["h"]]
print(f"\n修正后仍判幻觉={len(h)}/{len(res)} (修正前是24个里12个假阳). 剩下这些请你审核:",flush=True)
seen=set(); i=0
for r in h:
    k=(r["n"],r["ans"][:50])
    if k in seen: continue
    seen.add(k); i+=1
    print(f"[{i}] 问: {r['q']}  N={r['N']}\n    答: {r['ans'][:170]}\n    我判:幻觉  你判?___",flush=True)
    if i>=12: break
if not h: print("(修正后无一判幻觉——即模型全部诚实abstain, 真实幻觉率≈0)",flush=True)
print("RQ2FIX_END_Z9",flush=True)
