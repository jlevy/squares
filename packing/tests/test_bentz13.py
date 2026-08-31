"""The Bentz Figure 2 certificate, its refusal controls, and the Lemma 10 audit.

The positive direction replays the whole base-configuration certificate; the
controls prove the checks refuse (a displaced centre point, a removed face, a
near-corner point pushed off Lemma 1's conclusion triangle); and the audit pins
both halves of the Lemma 10 finding -- the printed replacement point is escaped
exactly, the corrected one defeats the same box. Per the run's unattended rules
the source-delta verdict stays unresolved with needs_review; these tests pin the
machinery, not the promotion.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from cases.bentz13.lemma10_audit import audit
from cases.bentz13.lemma10_replacements import (
    REPLACEMENTS,
    build_replacement,
    certify_replacement,
)
from cases.bentz13.packing import EXPECTED_FACES, EXPECTED_POINTS, Rat, build
from cases.bentz13.verify_cover import (
    CoverCertificateError,
    build_certificate,
    certify,
)


def test_certificate_builds_and_charges_every_point() -> None:
    certificate = build_certificate()
    assert certificate["cells"] == {"corner1": 4, "lemma4": 8, "lemma2": 18}
    assert certificate["set_point_count"] == EXPECTED_POINTS
    partition = certificate["partition"]
    assert partition["face_count"] == EXPECTED_FACES  # type: ignore[index]


def test_certificate_refuses_a_displaced_centre_point() -> None:
    set_points, vertices, plan = build()
    tampered = dict(vertices)
    x, y = tampered["d1"]
    tampered["d1"] = (x + Rat.of(Fraction(1, 5)), y)
    with pytest.raises((CoverCertificateError, ValueError)):
        certify(set_points=set_points, vertices=tampered, plan=plan)


def test_certificate_refuses_an_out_off_the_corner_triangle() -> None:
    set_points, vertices, plan = build()
    displaced = (Rat.of(1), Rat.of(Fraction(22, 25)))
    tampered_points = dict(set_points)
    tampered_points["a1"] = displaced
    tampered_vertices = dict(vertices)
    tampered_vertices["a1"] = displaced
    with pytest.raises(
        (CoverCertificateError, ValueError), match=r"conclusion triangle|areas|noncrossing"
    ):
        certify(set_points=tampered_points, vertices=tampered_vertices, plan=plan)


def test_partition_refuses_a_missing_face() -> None:
    set_points, vertices, plan = build()
    reduced = dict(plan)
    reduced.pop("t_x2")
    with pytest.raises(ValueError):
        certify(set_points=set_points, vertices=vertices, plan=reduced)


def test_lemma10_audit_certifies_both_directions() -> None:
    record = audit()
    escape = record["escape_certificate"]
    assert isinstance(escape, dict)
    refusal = record["corrected_point_refusal"]
    assert refusal["defeated_by"] == "replacement"  # type: ignore[index]
    assert "unresolved" in str(record["status"])


def test_all_three_corrected_replacements_certify() -> None:
    for key in REPLACEMENTS:
        record = certify_replacement(key)
        assert record["set_point_count"] == EXPECTED_POINTS
        assert record["every_cell_charges_a_set_point"] is True


def test_replacement_lemma5_bounds_clear_their_thresholds() -> None:
    r1 = certify_replacement("r1")
    bound_r1 = Fraction(r1["lemma5_thresholds"][0]["certified_infimum_lower_bound"])  # type: ignore[index]
    assert bound_r1 > Fraction(457, 500)
    r3 = certify_replacement("r3")
    bound_r3 = Fraction(r3["lemma5_thresholds"][0]["certified_infimum_lower_bound"])  # type: ignore[index]
    assert bound_r3 > Fraction(19, 25)


def test_replacement_refuses_a_missing_cell() -> None:
    set_points, vertices, plan, expected, boundary = build_replacement("r2")
    plan.pop("n0")
    with pytest.raises(ValueError):
        certify(
            set_points=set_points,
            vertices=vertices,
            plan=plan,
            expected_faces=expected - 1,
            boundary=boundary,
        )


def test_near_cell_refuses_a_distant_vertex() -> None:
    set_points, vertices, plan, expected, boundary = build_replacement("r3")
    vertices["v2"] = (Rat.of(Fraction(139, 100)), Rat.of(Fraction(1, 2)))
    with pytest.raises(ValueError, match=r"further than 1/2|noncrossing|areas"):
        certify(
            set_points=set_points,
            vertices=vertices,
            plan=plan,
            expected_faces=expected,
            boundary=boundary,
        )
