#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI
cli=OpenAI(api_key=os.environ["OPENAI_API_KEY"], base_url=os.environ.get("OPENAI_BASE_URL"), timeout=20.0, max_retries=1)
GEN="gpt-4.1-mini"
ABST=["no information","not mentioned","not specified","not provided","don't have","do not have","doesn't specify","does not specify","unable to","no mention","not available","not in the","no details","doesn't say","does not say","not stated","cannot find","can't find","no record","not listed","isn't provided","no data","not include","doesn't contain","does not contain"]
def halluc(a): al=(a or "").lower(); return not any(m in al for m in ABST)
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
# N0原始 + N2二次固化, 各2 seed
mems=[]
def build(s): n,mem,q=s; c2=consolidate(consolidate(mem)); return (n,q,mem,c2)
with ThreadPoolExecutor(6) as ex: built=list(ex.map(build,SCEN))
tasks=[(n,q,txt,N,sd) for (n,q,m0,m2) in built for (N,txt) in [("N0",m0),("N2",m2)] for sd in range(2)]
def run(t): n,q,txt,N,sd=t; a=reader(txt,q,sd); return (n,q,N,a,halluc(a))
with ThreadPoolExecutor(16) as ex: res=list(ex.map(run,tasks))
h=sum(r[4] for r in res); print("SCR_START_Z9",flush=True)
print(f"共{len(res)}个回答, 规则判幻觉={h}, 判不幻觉={len(res)-h}",flush=True)
print("=== 请审核: 每条最后填 [幻觉] 或 [不幻觉] ===",flush=True)
seen=set(); i=0
for n,q,N,a,hl in res:
    k=(n,a[:50])
    if k in seen: continue
    seen.add(k); i+=1
    print(f"\n[{i}] 问(记忆里没有的字段): {q}",flush=True)
    print(f"    答: {a[:170]}",flush=True)
    print(f"    我判: {'幻觉' if hl else '不幻觉'}  你判? ___",flush=True)
print("\nSCR_END_Z9",flush=True)
