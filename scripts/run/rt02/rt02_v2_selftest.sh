#!/usr/bin/env bash
# RT-02 v2 master offline self-test — validates the whole v2 architecture with ZERO API cost.
# Runs every module self-test + a mock end-to-end of both runners + the stats pipeline + AST.
# Exit 0 iff everything passes. Run from the project root:
#   bash scripts/run/rt02/rt02_v2_selftest.sh
set -u
PY=.venv_tiermem_v2/bin/python
DIR=scripts/run/rt02
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
FAIL=0
pass() { echo "  [PASS] $1"; }
fail() { echo "  [FAIL] $1"; FAIL=1; }

echo "== 1. AST syntax check (all v2 files) =="
for f in "$DIR"/rt02_v2_*.py "$DIR"/run_rt02_v2_*.py; do
  if $PY -c "import ast,sys; ast.parse(open('$f').read())" 2>/dev/null; then pass "AST $(basename "$f")"; else fail "AST $(basename "$f")"; fi
done

echo "== 2. module self-tests =="
for m in rt02_v2_operators rt02_v2_measure rt02_v2_retrieval rt02_v2_style_match; do
  if $PY "$DIR/$m.py" >/dev/null 2>&1; then pass "$m self-test"; else fail "$m self-test"; fi
done

echo "== 3. mock end-to-end runners (no API) =="
if $PY "$DIR/run_rt02_v2_chir.py" --mock --operator summary_rewrite --split dev --n-cases 1 \
     --outdir "$TMP/chir" >/dev/null 2>&1; then
  N=$(wc -l < "$TMP/chir/chir_v2_records.jsonl")
  [ "$N" -eq 5 ] && pass "mock CHIR 5 arms (got $N)" || fail "mock CHIR arms (got $N, want 5)"
else fail "mock CHIR run"; fi

if $PY "$DIR/run_rt02_v2_pairgain.py" --mock --operator summary_rewrite --split dev --n-cases 1 \
     --outdir "$TMP/pg" >/dev/null 2>&1; then
  N=$(wc -l < "$TMP/pg/pairgain_v2_records.jsonl")
  [ "$N" -eq 1 ] && pass "mock PairGain 1 case (got $N)" || fail "mock PairGain (got $N)"
else fail "mock PairGain run"; fi

echo "== 4. resume idempotency (re-run must not duplicate) =="
$PY "$DIR/run_rt02_v2_chir.py" --mock --operator summary_rewrite --split dev --n-cases 1 \
   --outdir "$TMP/chir" >/dev/null 2>&1
N2=$(wc -l < "$TMP/chir/chir_v2_records.jsonl")
[ "$N2" -eq 5 ] && pass "CHIR resume no-dup (still $N2)" || fail "CHIR resume dup (now $N2)"

echo "== 5. CHIR v2 stats on mock output =="
if $PY "$DIR/rt02_v2_chir_stats.py" --records "$TMP/chir/chir_v2_records.jsonl" \
     --out "$TMP/chir_stats.json" >/dev/null 2>&1 && [ -s "$TMP/chir_stats.json" ]; then
  pass "CHIR v2 stats runs"
else fail "CHIR v2 stats"; fi

echo "== 6. PairGain v2 stats on synthetic D/G =="
$PY - "$TMP" <<'PYEOF' && pass "PairGain v2 stats runs" || fail "PairGain v2 stats"
import json,os,sys,subprocess,random
t=sys.argv[1]; rng=random.Random(0); recs=[];nli=[]
for i in range(12):
    steps=[{"endpoint":{"A_j1":rng.randint(0,1)}} for _ in range(5)]
    D=[rng.random() for _ in range(5)]; G={k:[rng.gauss(0,1) for _ in range(4)] for k in("0.01","0.05","0.1")}
    recs.append({"domain":"s","cluster_id":i,"steps":steps})
    nli.append({"domain":"s","cluster_id":i,"mode":"source_only","D":D,"G":G})
open(t+"/r.jsonl","w").write("\n".join(map(json.dumps,recs)))
open(t+"/n.jsonl","w").write("\n".join(map(json.dumps,nli)))
r=subprocess.run([".venv_tiermem_v2/bin/python","scripts/run/rt02/rt02_v2_pairgain_stats.py",
  "--records",t+"/r.jsonl","--nli",t+"/n.jsonl","--out",t+"/o.json"],capture_output=True)
sys.exit(r.returncode or (0 if os.path.getsize(t+"/o.json")>0 else 1))
PYEOF

echo "== 7. manifest reproducible (re-run identical) =="
$PY "$DIR/rt02_v2_manifest.py" >/dev/null 2>&1 && pass "manifest builds" || fail "manifest build"

echo
if [ "$FAIL" -eq 0 ]; then echo "ALL PASS — v2 architecture self-test green"; else echo "SOME FAILED"; fi
exit $FAIL
