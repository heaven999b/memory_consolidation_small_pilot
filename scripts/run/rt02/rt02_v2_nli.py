#!/usr/bin/env python3
"""RT-02 v2 PairGain NLI bridge — v2 snapshots -> lineage-local D/G (fixes R3 on real runs).

For each pairgain_v2 record, loads the per-step minus/plus snapshots and computes the
directed semantic separation q(M) with rt02_v2_measure under a chosen mode:
  source_only (frozen primary) | source_lineage | whole_pool | retrieval_weighted (sensitivity).
Then D(t)=q(M-)-q(M+), G(t)=(D(t+1)-D(t))/(|D(t)|+eps). Uses the real frozen NLI checkpoint
(reuses rt02_pairgain_nli.NLI). Run in .venv_tiermem_v2 (CPU; MPS hangs on long premises).

Output: one row per (domain, cluster_id, mode) with D and G-grid. Consumed by
rt02_v2_pairgain_stats.py. Offline, no API.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rt02_v2_measure as M  # noqa: E402
from rt02_pairgain_nli import NLI  # noqa: E402


class ScorerAdapter:
    """Wrap the frozen NLI so rt02_v2_measure.q_value can call scorer.p_entail(prem, hyp)."""
    def __init__(self, nli, batch=64):
        self.nli, self.batch = nli, batch

    def p_entail(self, premises, hypotheses):
        return self.nli.p_entail_pairs(premises, hypotheses, batch=self.batch)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--records", required=True, nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--mode", default="carrier_matched",
                    choices=("carrier_matched", "consolidated_state", "source_only",
                             "source_lineage", "whole_pool", "retrieval_weighted"),
                    help="carrier_matched is the FAIR operator-on/off primary (consolidated_state "
                         "is structurally zero under append_only -> tautological comparison)")
    ap.add_argument("--model", default="MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli")
    ap.add_argument("--device", default="cpu", choices=("cpu", "mps"))
    ap.add_argument("--batch-size", type=int, default=64)
    ap.add_argument("--max-cases", type=int, default=0)
    ap.add_argument("--resume", action="store_true")
    args = ap.parse_args()

    done = set()
    if args.resume and os.path.exists(args.out):
        with open(args.out, encoding="utf-8") as f:
            for line in f:
                try:
                    r = json.loads(line)
                    done.add((r["domain"], r["cluster_id"], r["mode"]))
                except Exception:
                    pass

    nli = NLI(args.model, device=args.device)
    scorer = ScorerAdapter(nli, batch=args.batch_size)
    n = 0
    with open(args.out, "a" if args.resume else "w", encoding="utf-8") as fout:
        for rec_path in args.records:
            snap_dir = os.path.join(os.path.dirname(rec_path), "snapshots")
            with open(rec_path, encoding="utf-8") as f:
                for line in f:
                    rec = json.loads(line)
                    key = (rec["domain"], rec["cluster_id"], args.mode)
                    if key in done:
                        continue
                    if args.max_cases and n >= args.max_cases:
                        break
                    n += 1
                    pairs = rec.get("pairs", [])
                    lineage = [m for m in []]  # source_lineage lineage ids (descendants) if needed
                    # descendants = ids present in later snapshots but not source_ids
                    src_ids = set(rec.get("source_ids", []))
                    qm, qp = [], []
                    for step in rec["steps"]:
                        mp = json.load(open(os.path.join(snap_dir, step["minus_snap"]["path"]), encoding="utf-8"))
                        pp = json.load(open(os.path.join(snap_dir, step["plus_snap"]["path"]), encoding="utf-8"))
                        lineage_ids = [m.get("id") for m in mp if m.get("id") not in src_ids] \
                            if args.mode == "source_lineage" else None
                        qm.append(M.q_value(scorer, mp, pairs, mode=args.mode, lineage_ids=lineage_ids))
                        qp.append(M.q_value(scorer, pp, pairs, mode=args.mode, lineage_ids=lineage_ids))
                    D, G = M.D_and_G(qm, qp)
                    fout.write(json.dumps({"domain": rec["domain"], "cluster_id": rec["cluster_id"],
                                           "mode": args.mode, "D": D, "G": G,
                                           "q_minus": qm, "q_plus": qp}, ensure_ascii=False, default=float) + "\n")
                    fout.flush()
                    print("nli done", key, "D=", [None if d is None else round(d, 4) for d in D], flush=True)


if __name__ == "__main__":
    main()
