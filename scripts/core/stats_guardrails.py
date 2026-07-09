#!/usr/bin/env python3
"""Shared statistical guardrails for the RQ pipelines.

This module centralizes a few repo-wide requirements that were previously only
written in plans or reports:

* Holm-Bonferroni correction for families of pre-registered primary endpoints
* alpha defaults that can be tightened to 0.01
* simple risk/utility gate helpers for defense-side Pareto checks
"""
from __future__ import annotations

import math
from typing import Any


def _is_number(value: Any) -> bool:
    try:
        v = float(value)
    except (TypeError, ValueError):
        return False
    return math.isfinite(v)


def holm_bonferroni(p_values: list[Any], alpha: float = 0.01) -> list[dict[str, Any]]:
    """Return Holm-Bonferroni annotations for a p-value family.

    The output order matches the input order.
    """
    results = [
        {
            "p_value": None if not _is_number(p) else float(p),
            "holm_adjusted_p": None,
            "holm_reject": False,
            "holm_threshold": None,
        }
        for p in p_values
    ]
    valid = [(idx, float(p)) for idx, p in enumerate(p_values) if _is_number(p)]
    if not valid:
        return results

    valid.sort(key=lambda pair: pair[1])
    m = len(valid)
    running_max = 0.0
    stop_reject = False
    for rank, (idx, p_value) in enumerate(valid, start=1):
        factor = m - rank + 1
        adjusted = min(1.0, p_value * factor)
        running_max = max(running_max, adjusted)
        threshold = alpha / factor
        reject = (not stop_reject) and (p_value <= threshold)
        if not reject:
            stop_reject = True
        results[idx].update(
            {
                "holm_adjusted_p": running_max,
                "holm_reject": reject,
                "holm_threshold": threshold,
            }
        )
    return results


def annotate_holm(rows: list[dict[str, Any]], p_key: str = "p_value", alpha: float = 0.01) -> list[dict[str, Any]]:
    """Attach Holm-Bonferroni fields to a list of row dicts."""
    ann = holm_bonferroni([row.get(p_key) for row in rows], alpha=alpha)
    out: list[dict[str, Any]] = []
    for row, extra in zip(rows, ann):
        merged = dict(row)
        merged.update(extra)
        out.append(merged)
    return out


def relative_risk_reduction(baseline_rate: Any, defense_rate: Any) -> float | None:
    if not _is_number(baseline_rate) or not _is_number(defense_rate):
        return None
    base = float(baseline_rate)
    defense = float(defense_rate)
    if base <= 0:
        return None
    return (base - defense) / base


def absolute_utility_loss(baseline_utility: Any, defense_utility: Any) -> float | None:
    if not _is_number(baseline_utility) or not _is_number(defense_utility):
        return None
    return float(baseline_utility) - float(defense_utility)


def pareto_gate(
    risk_baseline: Any,
    risk_defense: Any,
    utility_baseline: Any,
    utility_defense: Any,
    *,
    min_relative_risk_drop: float = 0.25,
    max_absolute_utility_loss: float = 0.03,
) -> dict[str, Any]:
    """Evaluate the repo plan's default defense gate.

    A defense is only "promising" if relative risk drops by at least 25% while
    utility drops by at most 3 absolute points.
    """
    rel_drop = relative_risk_reduction(risk_baseline, risk_defense)
    util_loss = absolute_utility_loss(utility_baseline, utility_defense)
    return {
        "relative_risk_drop": rel_drop,
        "absolute_utility_loss": util_loss,
        "risk_gate_pass": (rel_drop is not None and rel_drop >= min_relative_risk_drop),
        "utility_gate_pass": (util_loss is not None and util_loss <= max_absolute_utility_loss),
        "promising": (
            rel_drop is not None
            and util_loss is not None
            and rel_drop >= min_relative_risk_drop
            and util_loss <= max_absolute_utility_loss
        ),
        "thresholds": {
            "min_relative_risk_drop": min_relative_risk_drop,
            "max_absolute_utility_loss": max_absolute_utility_loss,
        },
    }


def _self_test() -> None:
    rows = holm_bonferroni([0.001, 0.009, 0.02, 0.2], alpha=0.01)
    assert rows[0]["holm_reject"] is True
    assert rows[1]["holm_reject"] is False
    assert rows[0]["holm_adjusted_p"] <= rows[1]["holm_adjusted_p"] <= rows[2]["holm_adjusted_p"]
    gate = pareto_gate(0.40, 0.20, 0.82, 0.80)
    assert gate["promising"] is True, gate
    gate2 = pareto_gate(0.40, 0.34, 0.82, 0.74)
    assert gate2["promising"] is False, gate2
    print("[stats_guardrails self-test] OK")


if __name__ == "__main__":
    _self_test()
