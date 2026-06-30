from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from artifact_contract import claim_to_dict


PROTECTION_KEYWORDS = {
    "preference": ("preference", "favorite", "prefer", "likes", "dislikes"),
    "medical_or_legal_constraint": (
        "medical",
        "allergy",
        "medication",
        "diagnosis",
        "legal",
        "visa",
        "law",
        "restriction",
    ),
    "credential_or_secret": ("password", "pin", "token", "credential", "secret", "api key"),
    "tool_or_procedure": ("procedure", "workflow", "tool", "command", "step", "instruction"),
    "deadline_or_schedule": ("deadline", "due", "appointment", "schedule", "meeting", "date", "time"),
    "policy_or_permission": ("policy", "permission", "allowed", "forbidden", "access", "safety"),
}


@dataclass
class ProtectedSourceFact:
    source_id: str
    field: str
    value: str
    current: bool
    supported: bool
    unsafe: bool
    trust: str
    storage_mode: str
    protection_category: str


@dataclass
class ClaimDecision:
    field: str
    value: str
    decision: str
    reason: str
    source_ids: list[str]
    storage_mode: str


def _normalize(text: Any) -> str:
    return " ".join(str(text or "").lower().replace("_", " ").split())


def detect_protection_category(item: dict[str, Any]) -> str | None:
    family = item.get("family", "")
    if family == "unsafe":
        return "unsafe_or_adversarial"
    if family == "conflict":
        return "stateful_update_conflict"

    haystacks = [
        _normalize(item.get("query_field", "")),
        _normalize(item.get("query_text", "")),
    ]
    for fact in item.get("raw_facts", []):
        if _normalize(fact.get("field", "")) == _normalize(item.get("query_field", "")):
            haystacks.append(_normalize(fact.get("value", "")))

    for category, keywords in PROTECTION_KEYWORDS.items():
        if any(keyword in haystack for haystack in haystacks for keyword in keywords):
            return category

    if item.get("criticality") == "high":
        return "high_criticality_default"
    return None


def protected_query_sources(item: dict[str, Any], protection_category: str) -> list[ProtectedSourceFact]:
    target = _normalize(item.get("query_field", ""))
    protected: list[ProtectedSourceFact] = []
    for idx, fact in enumerate(item.get("raw_facts", [])):
        if _normalize(fact.get("field", "")) != target:
            continue
        if not bool(fact.get("supported")):
            continue
        if bool(fact.get("unsafe")):
            continue
        if not bool(fact.get("current")):
            continue
        protected.append(
            ProtectedSourceFact(
                source_id=f"{item['id']}_raw_{idx}",
                field=str(fact.get("field", "")),
                value=str(fact.get("value", "")),
                current=bool(fact.get("current")),
                supported=bool(fact.get("supported")),
                unsafe=bool(fact.get("unsafe")),
                trust=str(fact.get("trust", "unknown")),
                storage_mode="extractive_span" if protection_category == "unsafe_or_adversarial" else "typed_proposition",
                protection_category=protection_category,
            )
        )
    return protected


def _claim_reason(claim: dict[str, Any], *, exact_match: bool) -> str:
    if claim["unsafe"]:
        return "unsafe_rewrite_blocked"
    if not claim["supported"]:
        return "unsupported_rewrite_blocked"
    if claim["conflict_state"] != "clean":
        return f"conflict_{claim['conflict_state']}_blocked"
    if not claim["current"]:
        return "non_current_rewrite_blocked"
    if not exact_match:
        return "non_extractive_rewrite_blocked"
    return "supported_exact_match"


def _source_ids_for_exact_match(
    claim: dict[str, Any],
    sources: list[ProtectedSourceFact],
) -> list[str]:
    claim_field = _normalize(claim.get("field", ""))
    claim_value = _normalize(claim.get("value", ""))
    return [
        source.source_id
        for source in sources
        if _normalize(source.field) == claim_field and _normalize(source.value) == claim_value
    ]


def audit_item(
    item: dict[str, Any],
    claims: list[Any],
) -> dict[str, Any]:
    protection_category = detect_protection_category(item)
    protected = protection_category is not None
    sources = protected_query_sources(item, protection_category or "non_critical")

    target = _normalize(item.get("query_field", ""))
    target_claims = [claim_to_dict(claim) for claim in claims if _normalize(claim_to_dict(claim)["field"]) == target]

    decisions: list[ClaimDecision] = []
    preserved = [asdict(source) for source in sources]

    for claim in target_claims:
        exact_source_ids = _source_ids_for_exact_match(claim, sources)
        if not protected:
            decisions.append(
                ClaimDecision(
                    field=claim["field"],
                    value=claim["value"],
                    decision="allow",
                    reason="non_critical_field",
                    source_ids=exact_source_ids,
                    storage_mode="free_form_summary",
                )
            )
            continue

        reason = _claim_reason(claim, exact_match=bool(exact_source_ids))
        if reason == "supported_exact_match":
            storage_mode = "extractive_span" if protection_category == "unsafe_or_adversarial" else "typed_proposition"
            decisions.append(
                ClaimDecision(
                    field=claim["field"],
                    value=claim["value"],
                    decision="allow",
                    reason=reason,
                    source_ids=exact_source_ids,
                    storage_mode=storage_mode,
                )
            )
        else:
            decisions.append(
                ClaimDecision(
                    field=claim["field"],
                    value=claim["value"],
                    decision="block",
                    reason=reason,
                    source_ids=exact_source_ids,
                    storage_mode="quarantine",
                )
            )

    blocked = [asdict(decision) for decision in decisions if decision.decision == "block"]
    allowed = [asdict(decision) for decision in decisions if decision.decision == "allow"]

    return {
        "item_id": item["id"],
        "family": item.get("family", "unknown"),
        "criticality": item.get("criticality", "unknown"),
        "query_field": item.get("query_field", ""),
        "protected": protected,
        "protection_category": protection_category or "non_critical",
        "latent_target_claims": target_claims,
        "allowed_claims": allowed,
        "blocked_claims": blocked,
        "preserved_sources": preserved,
        "blocked_claim_count": len(blocked),
        "allowed_claim_count": len(allowed),
        "preserved_source_count": len(preserved),
        "blocked_reasons": sorted({decision["reason"] for decision in blocked}),
    }


def build_replacement_claim_dicts(item: dict[str, Any], audit: dict[str, Any]) -> list[dict[str, Any]]:
    replacements: list[dict[str, Any]] = []
    for source in audit["preserved_sources"]:
        replacements.append(
            {
                "field": source["field"],
                "value": source["value"],
                "supported": True,
                "unsafe": False,
                "confidence": 0.99 if source["trust"] == "high" else 0.82,
                "current": bool(source["current"]),
                "provenance_complete": True,
                "conflict_state": "clean",
            }
        )

    if replacements:
        return replacements

    if item.get("family") == "unsafe" and audit["blocked_claim_count"] > 0:
        return [
            {
                "field": item.get("query_field", ""),
                "value": "REFUSE_AND_ESCALATE",
                "supported": True,
                "unsafe": False,
                "confidence": 0.99,
                "current": True,
                "provenance_complete": True,
                "conflict_state": "clean",
            }
        ]

    return []
