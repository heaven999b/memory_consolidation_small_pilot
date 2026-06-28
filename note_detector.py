from __future__ import annotations

from dataclasses import dataclass

from pilot_core import CompactClaim, RetrievalProbe


INFERENCE_MARKERS = (
    "likely ",
    "likely:",
    "likely/",
    "appears to be",
    "appears ",
    "maybe ",
    "inferred",
    "approximate candidate",
    "weak approximate",
    "offered as",
    "nearest likely",
)
MISSING_MARKERS = (
    "cannot be determined",
    "not retained clearly",
    "no reliable",
    "cannot answer",
    "not enough information",
    "unknown",
)


@dataclass
class NoteFeatures:
    note_inference_marker: bool
    note_missing_marker: bool
    target_supported_clean: bool
    unsupported_target_guess: bool


def extract_note_features(
    query_field: str,
    latent_claims: list[CompactClaim],
    note_text: str,
) -> NoteFeatures:
    lower = note_text.lower()
    target_claims = [claim for claim in latent_claims if claim.field == query_field]
    target_supported_clean = any(
        claim.supported and claim.current and (not claim.unsafe) and claim.conflict_state == "clean"
        for claim in target_claims
    )
    unsupported_target_guess = any(
        (not claim.supported) or claim.unsafe or claim.conflict_state != "clean"
        for claim in target_claims
    )
    note_inference_marker = any(marker in lower for marker in INFERENCE_MARKERS)
    note_missing_marker = any(marker in lower for marker in MISSING_MARKERS)
    return NoteFeatures(
        note_inference_marker=note_inference_marker,
        note_missing_marker=note_missing_marker,
        target_supported_clean=target_supported_clean,
        unsupported_target_guess=unsupported_target_guess,
    )


def build_note_aware_probe(
    query_field: str,
    latent_claims: list[CompactClaim],
    note_text: str,
    base_probe: RetrievalProbe,
) -> tuple[RetrievalProbe, NoteFeatures]:
    features = extract_note_features(query_field, latent_claims, note_text)
    score = base_probe.score

    if features.unsupported_target_guess and features.note_inference_marker and not base_probe.history_conflict:
        score -= 0.17 if not base_probe.raw_target_exists else 0.07
    if features.note_missing_marker and not features.target_supported_clean:
        score -= 0.13 if not base_probe.history_conflict else 0.05
    if features.target_supported_clean and (not features.note_inference_marker) and (not features.note_missing_marker):
        score += 0.04

    score = max(0.0, min(1.0, score))
    if score >= 0.68:
        status = "present"
    elif score >= 0.42:
        status = "uncertain"
    else:
        status = "absent"

    adjusted_probe = RetrievalProbe(
        status=status,
        score=round(score, 3),
        raw_target_exists=base_probe.raw_target_exists,
        target_noise=base_probe.target_noise,
        history_conflict=base_probe.history_conflict,
    )
    return adjusted_probe, features
