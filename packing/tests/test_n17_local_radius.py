"""The n17 local theorem at larger, per-coordinate radii (`check_n17_local_radius`)."""

from __future__ import annotations

import json
from fractions import Fraction as Q
from functools import cache

import numpy as np

from devtools import check_n17_local_minimum as local
from devtools import check_n17_local_radius as radius
from devtools import check_n17_slider_coverage as slide

RECEIPTS = (
    local.REPO / "packing/campaign/explorations/X048-session-168-pilots/receipts/local-radius"
)


@cache
def _setting() -> radius.Setting:
    return radius.build_setting(radius.BOX_W_PRIME)


def _uniform(value: Q) -> dict[str, Q]:
    return dict.fromkeys(_setting().names, value)


def _floor(value: Q, name: str, sign: int, point: local.Point) -> Q:
    setting = _setting()
    curvature, _ = local.curvature_audit(setting.family, setting.box, _uniform(value))
    rows = setting.matrix.at(point)
    weights = np.array([float(entry) for entry in curvature])
    index = setting.names.index(name)
    solved = radius.point_program(radius.dense(rows, 45), weights, index, sign)
    assert solved is not None
    floor, _ = radius.exact_floor(rows, curvature, solved[1], index, sign)
    assert floor <= Q(solved[0]) * (1 + Q(1, 10**6))
    return floor / (2 * value)


def test_the_exact_floor_brackets_the_declared_radius_and_refuses_twice_it() -> None:
    worst = (Q(1, 4), Q(1, 12), Q(1, 16))
    assert Q(87, 100) < _floor(Q(1, 5000), "omega11", -1, worst) < 1
    assert _floor(Q(1, 2500), "omega11", -1, worst) > Q(17, 10)


def test_an_overscaled_floor_certificate_is_shrunk_to_a_valid_floor() -> None:
    setting = _setting()
    point = (Q(1, 4), Q(1, 12), Q(1, 16))
    curvature, _ = local.curvature_audit(setting.family, setting.box, _uniform(Q(1, 5000)))
    rows = setting.matrix.at(point)
    weights = np.array([float(entry) for entry in curvature])
    index = setting.names.index("omega11")
    solved = radius.point_program(radius.dense(rows, 45), weights, index, -1)
    assert solved is not None
    floor, _ = radius.exact_floor(rows, curvature, solved[1], index, -1)
    inflated, _ = radius.exact_floor(rows, curvature, 3 * solved[1], index, -1)
    assert floor * Q(999, 1000) < inflated <= Q(solved[0]) * (1 + Q(1, 10**6))


def test_the_exp248_certificates_reproduce_their_worst_ratio_and_scale_with_the_radius() -> (
    None
):
    setting = _setting()
    documents = json.loads(radius.EXP248_CERTIFICATES.read_text())
    ratios = []
    for value in (Q(1, 5000), Q(1, 2500)):
        curvature, _ = local.curvature_audit(
            setting.family, setting.box, _uniform(value), setting.enclosure
        )
        record = radius.certificate_ratios(setting, curvature, [value] * 45, documents)
        assert record["worst_direction"] == "-omega11"
        ratios.append(Q(record["worst_ratio_decimal"]))
    assert ratios[0] == Q("0.925931049178")
    # Slightly more than linear: the separation bound D carries the position radius.
    assert 2 < ratios[1] / ratios[0] < Q(201, 100)


def test_the_scene_is_held_at_the_radius_and_restored() -> None:
    original = slide.build_scene
    with radius.scene_radius(Q(1, 1024)):
        assert slide.build_scene is not original
        assert slide.build_scene().radius == Q(1, 1024)
    assert slide.build_scene is original


def test_second_order_forms_reproduce_every_row_and_are_symmetric() -> None:
    setting = _setting()
    forms = radius.second_order_forms(setting.family, (Q(0), Q(0), Q(0)))
    assert len(forms) == 52
    assert all(np.allclose(form, form.T) for form in forms)
    walls = [f for f, key in zip(forms, setting.family.keys, strict=True) if key[0] == "wall"]
    assert all(np.all(np.diag(form) >= 0) for form in walls)


def test_the_composition_vector_passes_its_worst_direction_inside_the_slide_radius() -> None:
    document = json.loads((RECEIPTS / "ratio-composition-1216.json").read_text())
    slide_receipt = json.loads((RECEIPTS / "slide-9-2048.json").read_text())
    radii = {name: Q(value) for name, value in document["radii"].items()}
    box = [(Q(lo), Q(hi)) for lo, hi in document["slider_box"].values()]
    setting = radius.build_setting(box)
    name = document["c8_c9"]["worst"]["direction"]
    curvature, _ = local.curvature_audit(setting.family, setting.box, radii, setting.enclosure)
    outcome = local.certify_coordinate(
        setting.matrix,
        local.float_system(setting.matrix, 45),
        curvature,
        [radii[n] for n in setting.names],
        names=setting.names,
        name=name[1:],
        sign=1 if name[0] == "+" else -1,
        box=setting.box,
        deviation=setting.deviation,
    )
    assert outcome.passed
    assert min(radii.values()) == Q(1, 1216)
    assert max(radii.values()) <= Q(slide_receipt["radius"])
    for name, (lo, hi) in zip("abz", box, strict=True):
        low, high = (Q(v) for v in slide_receipt["certified_box"][name]["exact"])
        assert lo <= low <= high <= hi
