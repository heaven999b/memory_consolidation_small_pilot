#!/usr/bin/env python3
"""RT-02 PairGain — offline NLI step (run in .venv_tiermem_v2, CPU ONLY; MPS hangs on long premises).

Computes, per case and per t, the pre-registered directed semantic separation
  q(M) = mean_s mean_pairs [ P_ent(s -> m) - P_ent(s -> c) ]
  D(t) = q(M-) - q(M+),   G(t) = (D(t+1)-D(t)) / (|D(t)| + eps)
over saved snapshots. Frozen primary checkpoint: MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli.

The implementation caches repeated sentences across the eight snapshots of a
case and batches all frozen-hypothesis comparisons.  This is an execution-only
optimization: sentence selection, checkpoint, entailment probabilities and the
registered D/G definitions are unchanged.
"""
import argparse
import json
import os
import re

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

MODEL_NAME = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
EPS_GRID = [0.01, 0.05, 0.1]
MAX_SENTS = 64
MAX_SENTS_PER_RECORD = 8  # per-record cap so late descendants stay represented
MAX_SENT_CHARS = 300
CONTENT_KEYS = ("post", "note", "assistant", "content", "workflow")


def pool_sentences(pool):
    sents = []
    for mem in pool:
        text = ""
        for k in CONTENT_KEYS:
            v = mem.get(k)
            if isinstance(v, str) and v.strip():
                text = v.strip()
                break
        rec_sents = []
        for s in re.split(r"(?<=[.!?。!?])\s+", text):
            s = s.strip()
            if len(s) >= 15:
                rec_sents.append(s[:MAX_SENT_CHARS])
        sents.extend(rec_sents[:MAX_SENTS_PER_RECORD])
    return sents[:MAX_SENTS]


class NLI:
    def __init__(self, model_name=MODEL_NAME, threads=None, device="cpu"):
        self.tok = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.device = torch.device(device)
        self.model.to(self.device)
        self.model.eval()
        torch.set_num_threads(threads or max(1, (os.cpu_count() or 4) - 2))
        lab = {v.lower(): int(k) for k, v in self.model.config.id2label.items()}
        self.ent_idx = lab.get("entailment", 0)

    @torch.inference_mode()
    def p_entail_pairs(self, premises, hypotheses, batch=64):
        """Return P(entailment) for aligned premise/hypothesis pairs."""
        out = []
        for i in range(0, len(premises), batch):
            chunk = premises[i:i + batch]
            h_chunk = hypotheses[i:i + batch]
            enc = self.tok(chunk, h_chunk, truncation=True,
                           max_length=256, padding=True, return_tensors="pt")
            enc = {key: value.to(self.device) for key, value in enc.items()}
            probs = torch.softmax(self.model(**enc).logits, dim=-1)
            out.extend(probs[:, self.ent_idx].detach().cpu().tolist())
        return out


def q_values(nli, sentence_groups, pairs, batch=64):
    """Compute q(M) for many snapshots while reusing repeated NLI pairs."""
    valid_pairs = []
    for pr in pairs:
        m, c = pr.get("m", "")[:MAX_SENT_CHARS * 2], pr.get("c", "")[:MAX_SENT_CHARS * 2]
        if m and c:
            valid_pairs.append((m, c))
    if not valid_pairs:
        return [None] * len(sentence_groups)

    unique_sents = list(dict.fromkeys(s for group in sentence_groups for s in group))
    if not unique_sents:
        return [None] * len(sentence_groups)

    premises, hypotheses, locations = [], [], []
    for pair_idx, (m, c) in enumerate(valid_pairs):
        for sent_idx, sent in enumerate(unique_sents):
            premises.extend((sent, sent))
            hypotheses.extend((m, c))
            locations.extend(((pair_idx, sent_idx, 0), (pair_idx, sent_idx, 1)))
    probs = nli.p_entail_pairs(premises, hypotheses, batch=batch)

    deltas = [[0.0] * len(unique_sents) for _ in valid_pairs]
    for prob, (pair_idx, sent_idx, side) in zip(probs, locations):
        if side == 0:
            deltas[pair_idx][sent_idx] += prob
        else:
            deltas[pair_idx][sent_idx] -= prob
    sent_index = {sent: idx for idx, sent in enumerate(unique_sents)}
    out = []
    for group in sentence_groups:
        if not group:
            out.append(None)
            continue
        idxs = [sent_index[s] for s in group]
        pair_means = [sum(row[idx] for idx in idxs) / len(idxs) for row in deltas]
        out.append(sum(pair_means) / len(pair_means))
    return out


def record_key(rec):
    return {
        "task": rec.get("task", "qa"),
        "domain": rec.get("domain"),
        "case_key": rec.get("case_key"),
        "cluster_id": rec.get("cluster_id"),
    }


def key_tuple(rec):
    key = record_key(rec)
    return tuple(str(key.get(k)) for k in ("task", "domain", "case_key", "cluster_id"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--records", required=True, nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default=MODEL_NAME,
                    help="primary: MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli; sensitivity: roberta-large-mnli")
    ap.add_argument("--threads", type=int, default=0)
    ap.add_argument("--batch-size", type=int, default=64)
    ap.add_argument("--device", default="cpu", choices=("cpu", "mps"),
                    help="execution backend; CPU is frozen primary, MPS is allowed only after an equivalence probe")
    ap.add_argument("--max-cases", type=int, default=0)
    ap.add_argument("--resume", action="store_true",
                    help="append and skip keys already present in --out")
    args = ap.parse_args()

    done = set()
    if args.resume and os.path.exists(args.out):
        with open(args.out, encoding="utf-8") as f:
            for line in f:
                try:
                    done.add(key_tuple(json.loads(line)))
                except Exception:
                    pass
    nli = NLI(args.model, threads=args.threads or None, device=args.device)
    n_done = 0
    with open(args.out, "a" if args.resume else "w", encoding="utf-8") as fout:
        for rec_path in args.records:
            snap_dir = os.path.join(os.path.dirname(rec_path), "snapshots")
            with open(rec_path, encoding="utf-8") as f:
                for line in f:
                    rec = json.loads(line)
                    if key_tuple(rec) in done:
                        continue
                    if args.max_cases and n_done >= args.max_cases:
                        break
                    n_done += 1
                    key = record_key(rec)
                    sentence_groups, meta = [], []
                    for step in rec["steps"]:
                        for name in ("minus", "plus"):
                            sp = os.path.join(snap_dir, step[f"{name}_snap"]["path"])
                            with open(sp, encoding="utf-8") as sf:
                                pool = json.load(sf)
                            sents = pool_sentences(pool)
                            sentence_groups.append(sents)
                            meta.append({"t": step["t"], "branch": name, "n_sents": len(sents)})
                    qvals = q_values(nli, sentence_groups, rec.get("pairs", []), batch=args.batch_size)
                    D = []
                    for idx in range(0, len(qvals), 2):
                        qm, qp = qvals[idx:idx + 2]
                        D.append(None if qm is None or qp is None else qm - qp)
                    G = {}
                    for eps in EPS_GRID:
                        G[str(eps)] = [
                            None if D[t] is None or D[t + 1] is None
                            else (D[t + 1] - D[t]) / (abs(D[t]) + eps)
                            for t in range(len(D) - 1)
                        ]
                    fout.write(json.dumps({**key, "D": D, "G": G, "sent_meta": meta},
                                          ensure_ascii=False) + "\n")
                    fout.flush()
                    print("nli done", key, "D=", [None if d is None else round(d, 4) for d in D],
                          flush=True)


if __name__ == "__main__":
    main()
