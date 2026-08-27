#!/usr/bin/env python3
"""Controls for numerical contact-census overlays in the house renderer."""

from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import pytest

from devtools.build_known_best_atlas import frame_from_witness
from devtools.render_known_best_contact_overlays import (
    CENSUS,
    WITNESS_SCHEMA,
    contact_census_features,
    expected_outputs,
)
from sqpack.render.model import EvidenceTier, validate_frame
from sqpack.witness import load_witness

ROOT = Path(__file__).resolve().parent.parent


def _n11_frame_and_entry():
    witness = load_witness(
        ROOT / "witnesses/known-best/n-011.yaml", fallback_schema=WITNESS_SCHEMA
    )
    frame = frame_from_witness(witness)
    census = json.loads(CENSUS.read_text(encoding="utf-8"))
    sweep = next(
        sweep
        for sweep in census["contact_sweeps"]
        if sweep["name"] == "registered-angle-contact"
    )
    entry = next(entry for entry in sweep["entries"] if entry["n"] == 11)
    return frame, entry


def test_gallery_selection_is_deterministic_and_source_stratified() -> None:
    document, renderings = expected_outputs()
    replay_document, replay_renderings = expected_outputs()
    entries = document["gallery"]["entries"]

    assert (document, renderings) == (replay_document, replay_renderings)
    assert [entry["n"] for entry in entries] == [11, 28, 40, 68, 89]
    assert {entry["source_kind"] for entry in entries} == {
        "kingbird-derived-facts",
        "unitsquare-rendering",
    }
    assert len(renderings) == 5
    for entry in entries:
        assert "sha256" not in entry
        rendered = renderings[ROOT / "atlas/known-best" / entry["rendering"]]
        assert 'data-overlay="contact-census"' in rendered
        assert 'data-feature="detected-contact-graph-edge"' in rendered
        assert 'data-angle-tolerance-radians="0.000001"' in rendered
        assert 'data-contact-tolerance="0.001"' in rendered
        assert 'data-feature="contact-census-legend"' in rendered
        assert "not exact contact geometry" in rendered
        assert 'data-feature="contact-segment"' not in rendered


def test_detected_contact_features_retain_their_numerical_boundary() -> None:
    frame, entry = _n11_frame_and_entry()
    features = contact_census_features(frame, entry)
    assert [feature.feature_id for feature in features] == sorted(
        feature.feature_id for feature in features
    )
    validate_frame(replace(frame, features=features))

    pair = next(feature for feature in features if feature.wall is None)
    assert pair.residual is not None
    invalid_pair = replace(pair, residual=pair.contact_tolerance * 2)
    invalid_features = tuple(
        invalid_pair if feature is pair else feature for feature in features
    )
    with pytest.raises(ValueError, match="residual must lie within tolerance"):
        validate_frame(replace(frame, features=invalid_features))

    invalid_angle = replace(pair, angle_tolerance_radians=pair.contact_tolerance * 0)
    invalid_features = tuple(
        invalid_angle if feature is pair else feature for feature in features
    )
    with pytest.raises(ValueError, match="tolerances must be finite and positive"):
        validate_frame(replace(frame, features=invalid_features))

    with pytest.raises(ValueError, match="feature IDs must be unique and stable"):
        validate_frame(replace(frame, features=tuple(reversed(features))))


def test_contact_census_entry_must_match_the_rendered_witness() -> None:
    frame, entry = _n11_frame_and_entry()

    with pytest.raises(ValueError, match="does not match the rendered witness"):
        contact_census_features(frame, {**entry, "witness_id": "W-known-best-n010"})


def test_detected_contacts_cannot_upgrade_unchecked_geometry() -> None:
    frame, entry = _n11_frame_and_entry()
    features = contact_census_features(frame, entry)

    with pytest.raises(ValueError, match="require a checked source geometry"):
        validate_frame(
            replace(
                frame,
                evidence=EvidenceTier.CANDIDATE,
                check=None,
                features=features,
            )
        )
