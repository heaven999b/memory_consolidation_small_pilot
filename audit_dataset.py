from __future__ import annotations

from collections import Counter
from pathlib import Path

from pilot_core import load_items


VALID_CRITICALITY = {"low", "medium", "high"}


def audit_items(items: list[dict]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    ids = [item["id"] for item in items]
    dup_ids = [item_id for item_id, count in Counter(ids).items() if count > 1]
    if dup_ids:
        errors.append(f"Duplicate ids: {dup_ids}")

    family_counts = Counter(item["family"] for item in items)
    for family in ("hallucination", "conflict", "unsafe", "benign"):
        if family_counts[family] < 10:
            warnings.append(f"Family {family} has only {family_counts[family]} items; target is >=10 for balance.")

    for item in items:
        prefix = f"{item['id']} ({item['family']})"
        if item["criticality"] not in VALID_CRITICALITY:
            errors.append(f"{prefix}: invalid criticality {item['criticality']}")
        if not item["query_text"].endswith("?"):
            warnings.append(f"{prefix}: query text does not end with a question mark.")
        if len(item["raw_facts"]) < 2:
            errors.append(f"{prefix}: fewer than 2 raw facts.")

        target_facts = [f for f in item["raw_facts"] if f["field"] == item["query_field"]]

        if item["family"] == "hallucination":
            if item["gold_answer"] != "ABSTAIN":
                errors.append(f"{prefix}: hallucination item must have ABSTAIN gold.")
            if target_facts:
                warnings.append(f"{prefix}: hallucination item unexpectedly contains target field in raw facts.")
            if len(item.get("invention_candidates", [])) < 2:
                errors.append(f"{prefix}: needs at least 2 invention candidates.")
            if len(item["raw_facts"]) < 3:
                warnings.append(f"{prefix}: hallucination item should ideally have >=3 supporting distractor facts.")

        elif item["family"] == "conflict":
            if len(target_facts) != 2:
                errors.append(f"{prefix}: conflict item must have exactly 2 target facts (old/new).")
            else:
                currents = Counter(f["current"] for f in target_facts)
                if currents[True] != 1 or currents[False] != 1:
                    errors.append(f"{prefix}: conflict item needs one current and one stale target fact.")
                current_values = [f["value"] for f in target_facts if f["current"]]
                if current_values and current_values[0] != item["gold_answer"]:
                    errors.append(f"{prefix}: gold answer does not match current target fact.")
            if len(item["raw_facts"]) < 4:
                warnings.append(f"{prefix}: conflict item should ideally include 2+ context facts.")

        elif item["family"] == "unsafe":
            if item["gold_answer"] != "REFUSE_AND_ESCALATE":
                errors.append(f"{prefix}: unsafe item must have REFUSE_AND_ESCALATE gold.")
            if len(target_facts) != 1:
                errors.append(f"{prefix}: unsafe item must have exactly one target action fact.")
            else:
                act = target_facts[0]
                if not act["unsafe"]:
                    errors.append(f"{prefix}: target action fact must be unsafe.")
                if act["trust"] != "low":
                    warnings.append(f"{prefix}: unsafe action should usually be low trust.")
            policies = [f for f in item["raw_facts"] if f["field"] == "policy"]
            if len(policies) != 1:
                errors.append(f"{prefix}: unsafe item needs exactly one policy fact.")
            if len(item.get("unsafe_paraphrases", [])) < 2:
                errors.append(f"{prefix}: needs at least 2 unsafe paraphrases.")

        elif item["family"] == "benign":
            if len(target_facts) != 1:
                errors.append(f"{prefix}: benign item must have exactly one target fact.")
            else:
                if target_facts[0]["value"] != item["gold_answer"]:
                    errors.append(f"{prefix}: benign gold answer must equal target fact value.")
            simplifications = item.get("benign_simplifications", [])
            if len(simplifications) < 2:
                errors.append(f"{prefix}: benign item needs at least 2 simplifications.")
            if item["gold_answer"] in simplifications:
                errors.append(f"{prefix}: simplifications must not contain the exact gold answer.")

    return errors, warnings


def render_report(items: list[dict], errors: list[str], warnings: list[str]) -> str:
    family_counts = Counter(item["family"] for item in items)
    lines = [
        "# Dataset Quality Audit",
        "",
        "This audit applies a strict mechanical rubric to the curated synthetic dataset.",
        "",
        f"- total_items: {len(items)}",
        f"- family_counts: {dict(family_counts)}",
        f"- hard_errors: {len(errors)}",
        f"- warnings: {len(warnings)}",
        "",
        "## Hard Rules",
        "",
        "1. Unique ids only.",
        "2. Valid criticality in {low, medium, high}.",
        "3. Family-specific schema constraints must hold.",
        "4. Gold answers must align with raw facts for conflict and benign families.",
        "5. Unsafe items must include a policy fact plus an unsafe low-trust action fact.",
        "",
    ]
    if errors:
        lines.append("## Hard Errors")
        lines.append("")
        for err in errors:
            lines.append(f"- {err}")
        lines.append("")
    else:
        lines.append("## Hard Errors")
        lines.append("")
        lines.append("- None.")
        lines.append("")

    lines.append("## Warnings")
    lines.append("")
    if warnings:
        for warn in warnings:
            lines.append(f"- {warn}")
    else:
        lines.append("- None.")
    lines.append("")

    lines.append("## Audit Verdict")
    lines.append("")
    if errors:
        lines.append("- FAIL: dataset requires fixes before use.")
    else:
        lines.append("- PASS: no hard failures under the current rubric.")
        if warnings:
            lines.append("- Note: warnings remain but do not block use.")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    items = load_items(base_dir)
    errors, warnings = audit_items(items)
    report = render_report(items, errors, warnings)
    out_path = base_dir / "reviews" / "dataset_quality_audit_round2.md"
    out_path.write_text(report, encoding="utf-8")
    print(f"Wrote {out_path}")
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
