"""The 17/4 sixteen-point certificate, its refusal controls, and the falsifier check.

The positive direction replays the whole certificate; the falsifier cross-check
saturates on a coarse grid (its caveat stands: saturation is corroboration, the
certificate is the argument); the controls prove the checks refuse a displaced
point and a side pushed past the near-slab corner bound. Per the run's unattended
rules the mathematical verdict stays unresolved with needs_review; these tests pin
the machinery, not the promotion or any frontier move.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from cases.bentz13.verify_cover import certify
from cases.green17.packing import EXPECTED_POINTS, SIDE, Rat, build
from cases.green17.verify_cover import build_certificate
from sqpack.falsify import SaturationReport, search_escape


def test_certificate_builds_and_charges_every_point() -> None:
    certificate = build_certificate()
    assert certificate["cells"] == {
        "lemma4": 10,
        "lemma5": 3,
        "margin": 1,
        "near": 4,
        "lemma2": 18,
    }
    assert certificate["set_point_count"] == EXPECTED_POINTS
    thresholds = certificate["lemma5_thresholds"]
    assert len(thresholds) == 3  # type: ignore[arg-type]
    for record in thresholds:  # type: ignore[union-attr]
        assert Fraction(record["certified_infimum_lower_bound"]) > Fraction(1, 2)


def test_falsifier_saturates_on_the_set() -> None:
    set_points, _vertices, _plan, _boundary = build()
    points = [(name, float(x.value), float(y.value)) for name, (x, y) in set_points.items()]
    report = search_escape(
        points, float(SIDE), 1.0001, theta_steps=24, xy_steps=24, refine_top=4
    )
    assert isinstance(report, SaturationReport)
    assert report.best_margin < 0
    assert "not a proof" in report.caveat


def test_certificate_refuses_a_displaced_point() -> None:
    set_points, vertices, plan, boundary = build()
    tampered_points = dict(set_points)
    tampered_vertices = dict(vertices)
    displaced = (Rat.of(Fraction(3)), Rat.of(Fraction(9, 10)))
    tampered_points["p0_2"] = displaced
    tampered_vertices["p0_2"] = displaced
    with pytest.raises(ValueError):
        certify(
            set_points=tampered_points,
            vertices=tampered_vertices,
            plan=plan,
            expected_faces=len(plan),
            boundary=boundary,
            container_side=SIDE,
        )


def test_near_slab_refuses_a_wider_margin() -> None:
    set_points, vertices, plan, boundary = build()
    tampered_vertices = dict(vertices)
    wider = Fraction(19, 5)
    for name in ("m_r0", "m_c0", "m_c1", "m_c2", "m_r3"):
        _x, y = tampered_vertices[name]
        tampered_vertices[name] = (Rat.of(wider), y)
    with pytest.raises(ValueError):
        certify(
            set_points=set_points,
            vertices=tampered_vertices,
            plan=plan,
            expected_faces=len(plan),
            boundary=boundary,
            container_side=SIDE,
        )


def test_lemma2_refuses_a_cut_vertex_off_the_boundary() -> None:
    set_points, vertices, plan, boundary = build()
    tampered_vertices = dict(vertices)
    x, y = tampered_vertices["s_c0"]
    tampered_vertices["s_c0"] = (x - Rat.of(Fraction(1, 50)), y)
    with pytest.raises(ValueError):
        certify(
            set_points=set_points,
            vertices=tampered_vertices,
            plan=plan,
            expected_faces=len(plan),
            boundary=boundary,
            container_side=SIDE,
        )
