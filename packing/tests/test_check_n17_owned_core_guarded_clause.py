"""Exact polynomial/guard controls and synthetic receipt custody; no target inputs."""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import pytest

from devtools import check_n17_owned_core_guarded_clause as tool

Q = tool.Q


def deadline() -> float:
    return time.monotonic() + 60


def core() -> list[tuple[Q, Q]]:
    return [(Q(7, 5), Q(2)), (Q(2), Q(19, 10)), (Q(13, 5), Q(2)), (Q(2), Q(21, 10))]


def oldbox() -> dict[str, Any]:
    return {
        "half_width": "1/512",
        "angle_interval": ["211/512", "213/512"],
        "centre_box": [[str(Q(2) - Q(1, 512)), str(Q(2) + Q(1, 512))]] * 2,
    }


def premise(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    monkeypatch.setattr(tool.finite, "REPO", tmp_path)
    endpoint = {
        "custody": {
            "input_control": {
                "endpoint_roster": [
                    {
                        "label": i,
                        "owner": 0 if i == 1 else i,
                        "charts": [["0", "0"], ["1", "1"]],
                    }
                    for i in range(1, 18)
                ]
            }
        }
    }
    path = tmp_path / "endpoint.json"
    path.write_text(json.dumps(endpoint))
    sha = hashlib.sha256(path.read_bytes()).hexdigest()
    original = {
        "guard": oldbox(),
        "container": {"synthetic": True},
        "parent_custody": {"h290_receipt": path.name, "h290_receipt_sha256": sha},
        "original_endpoint_control": {
            "all17_retained": True,
            "witnesses": [{"label": i, "owner": 0 if i == 1 else i} for i in range(1, 18)],
        },
    }
    combined = [
        {
            "owner": 6,
            "combined_surviving_closed_interval_union": [["1/16", "19/32"]],
            "additional_lost_length": "15/32",
        },
        {
            "owner": 18,
            "combined_surviving_closed_interval_union": [
                ["0", "19/64"],
                ["3/8", "35/64"],
                ["13/16", "1"],
            ],
        },
    ]
    monkeypatch.setattr(
        tool.prior,
        "intake",
        lambda *_: ({}, {0: core()}, original, {path: (sha, tool.parent.JSON_LIMIT)}),
    )
    monkeypatch.setattr(tool.prior, "combine", lambda *_: copy.deepcopy(combined))
    child = {
        "closed": False,
        "closure": None,
        "collective_rows_accounted": 992,
        "collective": {"all_foreign_rows_accounted": 992},
        "other_owned_groups_unchanged": True,
    }
    desc = {"synthetic": True}
    accepted = {
        "schema": tool.prior.SCHEMA,
        "accepted_inputs": desc,
        "status": "additional_angle_union_restricted",
        "criterion_met": True,
        **tool.prior.scope(progress=True),
        **original,
        "closed_case_count": 0,
        "both_children_closed": False,
        "base_foreign_rows_accounted": 992,
        "original_rows_inherited": 1056,
        "survivors_unioned_across_cases": True,
        "no_sequential_feedback": True,
        "fixed_selection": {"owner": 18, "axis": 0, "midpoint": str(tool.prior.MIDPOINT)},
        "children": [
            child
            | {
                "side": side,
                "halfplane": {
                    "axis": 0,
                    "relation": "<=" if side == -1 else ">=",
                    "midpoint": str(tool.prior.MIDPOINT),
                },
            }
            for side in (-1, 1)
        ],
        "combined_restrictions": combined,
    }
    document = {"schema": tool.DESCRIPTOR_SCHEMA}
    for role, value in zip(
        tool.ROLES, (desc, accepted, accepted | {"verification_passed": True}), strict=True
    ):
        p = tmp_path / (role + ".json")
        p.write_text(json.dumps(value))
        document[role], document[role + "_sha256"] = (
            p.name,
            hashlib.sha256(p.read_bytes()).hexdigest(),
        )
    return document


@pytest.mark.parametrize("axis", ["u", "v"])
@pytest.mark.parametrize("sign", [-1, 1])
def test_symbolic_coefficients_match_direct_projection(axis: str, sign: int) -> None:
    q, centre, t = (Q(9, 7), Q(4, 3)), (Q(5, 4), Q(7, 5)), Q(53, 128)
    coefficients = tool.polynomial(q, axis, sign)
    p = tool.at_centre(coefficients, centre)
    c, s = tool.finite.trig(t)
    x, y = q[0] - centre[0], q[1] - centre[1]
    direct = tool.REACH - sign * (c * x + s * y if axis == "u" else -s * x + c * y)
    assert sum(p[i] * t**i for i in range(3)) == direct * (1 + t * t)
    assert max(sum(x) for x in tool.MONOMIALS) == 3


def test_oldbox_closed_corners_quadratics_and_span_not_volume() -> None:
    result = tool.finite_packet(core(), oldbox(), deadline=deadline())
    assert result["quadratic_checks"] == 64
    assert all(Q(x["minimum"]) > 0 for x in result["old_box_corner_minima"])
    assert result["endpoint_axis_aligned_family_disjoint"]
    assert result["axis_spans"] == ["6/5", "1/5"]


def test_closed_margin_equality_and_open_square_distinction() -> None:
    p = tool.at_centre(tool.polynomial((tool.REACH, Q(0)), "u", 1), (Q(0), Q(0)))
    assert p[0] == 0
    p = tool.at_centre(tool.polynomial((Q(1, 2), Q(0)), "u", 1), (Q(0), Q(0)))
    assert p[0] < 0
    assert Q(1, 2) > tool.REACH


@pytest.mark.parametrize("width", [Q(1, 2), Q(1)])
def test_span_at_most_one_is_miss_not_endpoint_intersection(width: Q) -> None:
    points = [
        (Q(2) - width / 2, Q(2)),
        (Q(2), Q(19, 10)),
        (Q(2) + width / 2, Q(2)),
        (Q(2), Q(21, 10)),
    ]
    packet = tool.finite_packet(points, oldbox(), deadline=deadline())
    assert not packet["endpoint_axis_aligned_family_disjoint"]


@pytest.mark.parametrize("kind", ["outside", "angle", "centre", "reorder", "big"])
def test_guard_resource_and_calibration_refusals(kind: str) -> None:
    points, box = core(), oldbox()
    if kind == "outside":
        points = [(Q(0), Q(0))]
    elif kind == "angle":
        box["angle_interval"] = ["0", "1"]
    elif kind == "centre":
        box["centre_box"][0] = ["0", "1"]
    elif kind == "reorder":
        points.reverse()
    else:
        points = [(Q(1 << 4097), Q(2))]
    with pytest.raises((ValueError, tool.IncompleteError)):
        tool.finite_packet(points, box, deadline=deadline())


def test_generate_check_full_payload_scope_and_coefficient_tamper(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    document = premise(tmp_path, monkeypatch)
    result = tool.generate(document, deadline=deadline())
    assert result["criterion_met"]
    assert result["status"] == "guarded_clause_verified"
    assert not any(result[k] for k in tool.scope())
    assert tool.check(document, result, deadline=deadline())["verification_passed"]
    damaged = copy.deepcopy(result)
    damaged["guard_packet"]["polynomials"][0]["coefficients"][0] = "0"
    with pytest.raises(ValueError, match="reconstruction"):
        tool.check(document, damaged, deadline=deadline())


@pytest.mark.parametrize(
    "kind", ["fresh", "missingrow", "case", "union", "guard", "axis", "sha", "alias"]
)
def test_accepted_boundary_and_endpoint_custody_refusals(
    kind: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    doc = premise(tmp_path, monkeypatch)
    role = "cases_replay" if kind == "fresh" else "cases_certificate"
    if kind == "axis":
        p = tmp_path / "endpoint.json"
        v = json.loads(p.read_text())
        v["custody"]["input_control"]["endpoint_roster"][0]["charts"] = [["0", "1"]]
        p.write_text(json.dumps(v))
    elif kind == "sha":
        doc["cases_certificate_sha256"] = "0" * 64
    elif kind == "alias":
        base = tool.prior.intake

        def conflicting(*args):
            rows, groups, original, held = base(*args)
            held[tmp_path / doc["cases_certificate"]] = ("0" * 64, 10)
            return rows, groups, original, held

        monkeypatch.setattr(tool.prior, "intake", conflicting)
    else:
        p = tmp_path / doc[role]
        v = json.loads(p.read_text())
        if kind == "fresh":
            v["verification_passed"] = False
        elif kind == "missingrow":
            v["base_foreign_rows_accounted"] = 991
        elif kind == "case":
            v["children"][1]["closed"] = True
        elif kind == "union":
            v["combined_restrictions"][0]["combined_surviving_closed_interval_union"] = [
                ["0", "1"]
            ]
        else:
            v["guard"]["half_width"] = "1/1024"
        p.write_text(json.dumps(v))
        doc[role + "_sha256"] = hashlib.sha256(p.read_bytes()).hexdigest()
    with pytest.raises(ValueError, match=r"differ|identity|alias|changed"):
        tool.generate(doc, deadline=deadline())


def test_deadline_and_cli_nan_refuse(tmp_path: Path) -> None:
    with pytest.raises(tool.IncompleteError):
        tool.finite_packet(core(), oldbox(), deadline=0)
    with pytest.raises(SystemExit):
        tool.main(
            [
                "--descriptor",
                str(tmp_path / "d"),
                "--output",
                str(tmp_path / "o"),
                "--max-seconds",
                "nan",
            ]
        )


def test_clean_two_process_finite_reconstruction() -> None:
    script = """
import json,time
from fractions import Fraction as Q
from devtools import check_n17_owned_core_guarded_clause as t
p=t.finite_packet([(Q(7,5),Q(2)),(Q(2),Q(19,10)),(Q(13,5),Q(2)),(Q(2),Q(21,10))],
 {'half_width':'1/512','angle_interval':['211/512','213/512'],
 'centre_box':[[str(Q(2)-Q(1,512)),str(Q(2)+Q(1,512))]]*2},deadline=time.monotonic()+10)
print(json.dumps(p,sort_keys=True))
"""
    outputs = [
        subprocess.run(
            [sys.executable, "-c", script],
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        ).stdout
        for _ in range(2)
    ]
    assert outputs[0] == outputs[1]
    packet = json.loads(outputs[0])
    assert packet["endpoint_axis_aligned_family_disjoint"]
    assert packet["quadratic_checks"] == 64


def test_closed_arc_interior_minimum_and_all_corner_affinity() -> None:
    polynomial = (Q(1, 4), Q(-1), Q(1))
    value, argmin = tool.guard.sat.minimum(polynomial, Q(0), Q(1))
    assert value == 0
    assert argmin == Q(1, 2)
    q = (Q(9, 7), Q(4, 3))
    p = tool.polynomial(q, "v", -1)
    corners = [(Q(x), Q(y)) for x in (1, 3) for y in (2, 4)]
    midpoint = (Q(2), Q(3))
    a = tool.at_centre(p, midpoint)
    assert a == tuple(sum(tool.at_centre(p, c)[i] for c in corners) / 4 for i in range(3))


@pytest.mark.parametrize(
    "points",
    [
        [(Q(2), Q(2))],
        [(Q(3, 2), Q(2)), (Q(5, 2), Q(2))],
        [(Q(1), Q(1)), (Q(3), Q(3)), (Q(1), Q(3)), (Q(3), Q(1))],
    ],
)
def test_degenerate_or_nonconvex_core_refuses(points: Any) -> None:
    with pytest.raises(ValueError, match=r"Q0|hull"):
        tool.finite_packet(points, oldbox(), deadline=deadline())


def test_used_coordinate_bit_ceiling_before_hull_work(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*_args):
        pytest.fail("hull arithmetic reached before used coordinate bit guard")

    monkeypatch.setattr(tool.prior.cases, "bounded_hull", forbidden)
    points = [(Q(1 << 4097), Q(2)), *core()[1:]]
    with pytest.raises(tool.IncompleteError, match="bit"):
        tool.finite_packet(points, oldbox(), deadline=deadline())


def test_post_computation_named_byte_mutation_refuses(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = premise(tmp_path, monkeypatch)
    original = tool.finite_packet

    def mutate(*args, **kwargs):
        result = original(*args, **kwargs)
        (tmp_path / doc["cases_certificate"]).write_text("{}")
        return result

    monkeypatch.setattr(tool, "finite_packet", mutate)
    with pytest.raises(ValueError, match="changed"):
        tool.generate(doc, deadline=deadline())


def test_new_receipt_one_mib_ceiling_not_inherited_64_mib(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    descriptor = tmp_path / "descriptor.json"
    descriptor.write_text("{}")
    output = tmp_path / "output.json"
    monkeypatch.setattr(
        tool,
        "generate",
        lambda *_a, **_k: {
            "status": "guarded_clause_verified",
            "payload": "x" * tool.OUTPUT_LIMIT,
        },
    )
    assert tool.main(["--descriptor", str(descriptor), "--output", str(output)]) == 1
    value = json.loads(output.read_text())
    assert value["status"] == "incomplete"
    assert not value["criterion_met"]
    assert tool.OUTPUT_LIMIT == 1 << 20
    assert tool.RECEIPT_LIMIT == 64 << 20
