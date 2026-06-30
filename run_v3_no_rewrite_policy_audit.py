from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

import benchmark_native_runtime as native_runtime
import pilot_core
import v3_no_rewrite_policy as no_rewrite_policy


N_VALUES = [1, 8]
SEEDS = [11, 23]
JSON_PATH = "outputs/v3_no_rewrite_policy_audit.json"
SUMMARY_PATH = "outputs/v3_no_rewrite_policy_audit.md"


def load_manifest_items(repo_root: Path) -> list[tuple[str, dict[str, Any]]]:
    items: list[tuple[str, dict[str, Any]]] = []
    for spec in native_runtime.MANIFEST_SPECS:
        manifest = native_runtime.load_json(repo_root / spec["manifest_path"])
        for item in manifest["items"]:
            items.append((spec["panel_id"], item))
    return items


def audit_records(repo_root: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for panel_id, item in load_manifest_items(repo_root):
        for n_passes in N_VALUES:
            for seed in SEEDS:
                latent_claims = pilot_core.consolidate(item, n_passes, seed)
                audit = no_rewrite_policy.audit_item(item, latent_claims)
                latent_values = [claim["value"] for claim in audit["latent_target_claims"]]
                records.append(
                    {
                        "panel_id": panel_id,
                        "item_id": item["id"],
                        "family": item["family"],
                        "criticality": item["criticality"],
                        "query_field": item["query_field"],
                        "seed": seed,
                        "n_passes": n_passes,
                        "protected": audit["protected"],
                        "protection_category": audit["protection_category"],
                        "blocked_claim_count": audit["blocked_claim_count"],
                        "allowed_claim_count": audit["allowed_claim_count"],
                        "preserved_source_count": audit["preserved_source_count"],
                        "blocked_reasons": audit["blocked_reasons"],
                        "latent_values": latent_values,
                        "preserved_values": [entry["value"] for entry in audit["preserved_sources"]],
                    }
                )
    return records


def _ratio(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0
    return round(numerator / denominator, 4)


def summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    by_family_n: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        by_family_n[(record["family"], record["n_passes"])].append(record)

    family_rows: list[dict[str, Any]] = []
    for (family, n_passes), rows in sorted(by_family_n.items()):
        protected_rows = [row for row in rows if row["protected"]]
        blocked_rows = [row for row in protected_rows if row["blocked_claim_count"] > 0]
        family_rows.append(
            {
                "family": family,
                "n_passes": n_passes,
                "case_count": len(rows),
                "protected_case_count": len(protected_rows),
                "protected_case_rate": _ratio(len(protected_rows), len(rows)),
                "blocked_protected_case_count": len(blocked_rows),
                "blocked_protected_case_rate": _ratio(len(blocked_rows), len(protected_rows)),
                "blocked_claims_per_protected_case": round(
                    sum(row["blocked_claim_count"] for row in protected_rows) / max(1, len(protected_rows)),
                    4,
                ),
                "preserved_sources_per_protected_case": round(
                    sum(row["preserved_source_count"] for row in protected_rows) / max(1, len(protected_rows)),
                    4,
                ),
            }
        )

    blocked_examples: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in sorted(records, key=lambda row: (row["family"], -row["blocked_claim_count"], row["item_id"])):
        if record["n_passes"] != 8 or record["blocked_claim_count"] <= 0:
            continue
        family_examples = blocked_examples[record["family"]]
        if len(family_examples) >= 3:
            continue
        family_examples.append(
            {
                "item_id": record["item_id"],
                "protection_category": record["protection_category"],
                "blocked_reasons": record["blocked_reasons"],
                "latent_values": record["latent_values"][:3],
                "preserved_values": record["preserved_values"][:3],
            }
        )

    protected_records = [record for record in records if record["protected"]]
    n1_records = [record for record in protected_records if record["n_passes"] == 1]
    n8_records = [record for record in protected_records if record["n_passes"] == 8]

    return {
        "description": "Legacy dry-run audit of the V3 safety-critical no-rewrite policy over manifest-backed benchmark items.",
        "note": (
            "This is not a TierMem result table. It is a local dry-run over the legacy compaction simulator to instantiate "
            "the exact rule V3 wants to defend and to measure how often it would block unsupported rewrites on protected fields."
        ),
        "n_values": N_VALUES,
        "seeds": SEEDS,
        "overall": {
            "record_count": len(records),
            "protected_record_count": len(protected_records),
            "protected_record_rate": _ratio(len(protected_records), len(records)),
            "n1_blocked_protected_case_rate": _ratio(
                sum(1 for record in n1_records if record["blocked_claim_count"] > 0),
                len(n1_records),
            ),
            "n8_blocked_protected_case_rate": _ratio(
                sum(1 for record in n8_records if record["blocked_claim_count"] > 0),
                len(n8_records),
            ),
        },
        "family_rows": family_rows,
        "blocked_examples": blocked_examples,
        "records": records,
    }


def build_summary(payload: dict[str, Any]) -> str:
    lines = [
        "# V3 No-Rewrite Policy Audit",
        "",
        payload["note"],
        "",
        f"- seeds: `{payload['seeds']}`",
        f"- depths: `{payload['n_values']}`",
        f"- protected record rate: `{payload['overall']['protected_record_rate']:.3f}`",
        f"- blocked protected case rate at `N=1`: `{payload['overall']['n1_blocked_protected_case_rate']:.3f}`",
        f"- blocked protected case rate at `N=8`: `{payload['overall']['n8_blocked_protected_case_rate']:.3f}`",
        "",
        "## Family × Depth Summary",
        "",
        "| Family | N | Cases | Protected | Protected Rate | Blocked Protected | Blocked Rate | Blocked Claims / Protected | Preserved Sources / Protected |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in payload["family_rows"]:
        lines.append(
            f"| {row['family']} | {row['n_passes']} | {row['case_count']} | {row['protected_case_count']} | "
            f"{row['protected_case_rate']:.3f} | {row['blocked_protected_case_count']} | "
            f"{row['blocked_protected_case_rate']:.3f} | {row['blocked_claims_per_protected_case']:.3f} | "
            f"{row['preserved_sources_per_protected_case']:.3f} |"
        )
    lines.extend(["", "## Example Blocked Cases at N=8", ""])
    for family, examples in sorted(payload["blocked_examples"].items()):
        lines.append(f"### {family}")
        lines.append("")
        for example in examples:
            lines.append(
                f"- `{example['item_id']}`: category=`{example['protection_category']}`; blocked=`{example['blocked_reasons']}`; "
                f"latent={example['latent_values']}; preserved={example['preserved_values']}"
            )
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    repo_root = Path(__file__).resolve().parent
    outputs_dir = repo_root / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)

    records = audit_records(repo_root)
    payload = summarize(records)

    (repo_root / JSON_PATH).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (repo_root / SUMMARY_PATH).write_text(build_summary(payload), encoding="utf-8")
    print(f"[v3-no-rewrite] wrote {repo_root / JSON_PATH}")
    print(f"[v3-no-rewrite] wrote {repo_root / SUMMARY_PATH}")


if __name__ == "__main__":
    main()

