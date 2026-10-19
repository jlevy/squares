"""Synthetic closed-polytope and capacity certificates; no actual catalogue states."""

from __future__ import annotations

import copy
import itertools
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import pytest

from devtools import check_n17_n11_corner_cardinality as tool

Q = tool.Q
WIDTH = Q(1, 20)


def deadline() -> float:
    return time.monotonic() + 60


def rectangle(x: Q, y: Q, width: Q = WIDTH) -> list[tool.Point]:
    return [
        (x - width, y - width),
        (x + width, y - width),
        (x + width, y + width),
        (x - width, y + width),
    ]


def table() -> list[dict[str, Any]]:
    return [
        {
            "cell_index": c,
            "pattern_id": p,
            "feasible": p == (0 if c < 12 else 8),
            "guaranteed_window_bits": list(tool.pattern_bits(*xy)),
        }
        for c in range(24)
        for p, xy in enumerate(tool.CLASSES)
    ]


@pytest.mark.parametrize(("horizontal", "vertical"), tool.CLASSES)
def test_all9_closed_classes_and_genuinely_guaranteed_bits(
    horizontal: int, vertical: int
) -> None:
    positions = (Q(3, 4), tool.U / 2, tool.U - Q(3, 4))
    rows = tool.pattern_rows(
        rectangle(positions[horizontal], positions[vertical]), horizontal, vertical
    )
    result = tool.feasible(rows, tool.new_work(), deadline())
    assert result["feasible"]
    x, y, h = map(Q, result["pose"])
    actual = (
        x + h <= tool.H and y + h <= tool.H,
        x - h >= tool.D and y + h <= tool.H,
        x + h <= tool.H and y - h >= tool.D,
        x - h >= tool.D and y - h >= tool.D,
    )
    assert all(
        not b or actual[i] for i, b in enumerate(tool.pattern_bits(horizontal, vertical))
    )
    assert tool.physical_half_extent_squared(h * h)


def test_closed_seam_alias_is_safe_undercount_not_nonmembership() -> None:
    x, y, h = tool.D + Q(1, 2), tool.U / 2, Q(1, 2)
    poly = rectangle(x, y)
    for cls in (0, 1):
        rows = tool.pattern_rows(poly, cls, 1)
        assert all(tool.value(row, (x, y, h)) <= row[3] for row in rows)
    assert sum(tool.pattern_bits(0, 1)) == 2
    assert sum(tool.pattern_bits(1, 1)) == 4
    assert x + h <= tool.H
    assert x - h >= tool.D


def test_shared_h_rejects_independent_axis_false_positive() -> None:
    x, y = tool.D + Q(3, 5), tool.H - Q(11, 20)
    rows = tool.pattern_rows(rectangle(x + Q(1, 200), y + Q(1, 200), Q(1, 200)), 0, 1)
    assert not tool.feasible(rows, tool.new_work(), deadline())["feasible"]
    # The separate projections each have a witness with DIFFERENT h.
    assert x <= tool.D + Q(3, 5)
    assert y <= tool.H - Q(1, 2)


def test_original_triangle_stronger_than_its_aabb() -> None:
    triangle = [(Q(1, 2), Q(1, 2)), (Q(3, 2), Q(1, 2)), (Q(1, 2), Q(3, 2))]
    assert not tool.feasible(tool.pattern_rows(triangle, 1, 1), tool.new_work(), deadline())[
        "feasible"
    ]
    square = rectangle(Q(1), Q(1), Q(1, 2))
    assert tool.feasible(tool.pattern_rows(square, 1, 1), tool.new_work(), deadline())[
        "feasible"
    ]


def fixed_polytope(lo: Q, hi: Q) -> list[tool.Row]:
    return [
        (Q(1), Q(0), Q(0), Q(0)),
        (Q(-1), Q(0), Q(0), Q(0)),
        (Q(0), Q(1), Q(0), Q(0)),
        (Q(0), Q(-1), Q(0), Q(0)),
        (Q(0), Q(0), Q(1), hi),
        (Q(0), Q(0), Q(-1), -lo),
    ]


def test_singular_triples_lowerdim_boundary_and_exact_physical_reach() -> None:
    rows = fixed_polytope(Q(1, 2), Q(1, 2))
    assert tool.solve((rows[0], rows[1], rows[2])) is None
    result = tool.feasible(rows, tool.new_work(), deadline())
    assert result["pose"] == ["0", "0", "1/2"]
    assert tool.physical_half_extent_squared(Q(1, 2))
    assert not tool.physical_half_extent_squared(Q(1, 2) + Q(1, 1000000))


def test_nonphysical_first_vertex_skipped_then_lower_h_vertex_passes() -> None:
    result = tool.feasible(fixed_polytope(Q(1, 2), tool.R), tool.new_work(), deadline())
    assert result["active_triple"] == [0, 2, 5]
    assert result["pose"][2] == "1/2"
    rejected = tool.feasible(fixed_polytope(tool.R, tool.R), tool.new_work(), deadline())
    assert not rejected["feasible"]
    assert rejected["vertex_enumeration_complete"]
    assert rejected["triples_attempted"] == 20


def test_exhaustive_empty_and_cell_canonical_refusal() -> None:
    rows = fixed_polytope(Q(3, 5), Q(1, 2))
    assert not tool.feasible(rows, tool.new_work(), deadline())["feasible"]
    with pytest.raises(ValueError, match="canonical"):
        tool.pattern_rows(list(reversed(rectangle(Q(1), Q(1)))), 0, 0)


def test_dp_survivor_aliases_and_complete_negative_frontiers() -> None:
    records = table()
    survivor = tool.capacity_dp(
        list(range(8)) + list(range(12, 21)), records, tool.new_work(), deadline()
    )
    assert survivor["kind"] == "surviving_relaxation_assignment"
    tool.verify_state(survivor, records, deadline())
    negative = tool.capacity_dp(list(range(17)), records, tool.new_work(), deadline())
    assert negative["kind"] == "ordinary_assignment_obstruction"
    assert len(negative["frontier_bitmaps"]) == 18
    tool.verify_state(negative, records, deadline())
    damaged = copy.deepcopy(negative)
    damaged["frontier_bitmaps"][1] = tool.bitmap(set())
    with pytest.raises(ValueError, match="recurrence"):
        tool.verify_state(damaged, records, deadline())
    damaged = copy.deepcopy(survivor)
    damaged["pattern_ids"][0] = 4
    with pytest.raises(ValueError, match="feasible"):
        tool.verify_state(damaged, records, deadline())


def test_bitmap_finite_set_encoding_roundtrip_and_unused_bits() -> None:
    frontier = {(0, 0, 0, 0), (10, 10, 10, 10), (1, 4, 7, 10)}
    text = tool.bitmap(frontier)
    assert len(text) == 3662
    assert tool.decode_bitmap(text) == frontier
    with pytest.raises(ValueError, match="high bits"):
        tool.decode_bitmap(text[:-2] + "80")


def test_multichoice_negative_requires_complete_reachable_frontiers() -> None:
    records = table()
    for record in records:
        record["feasible"] = (
            record["pattern_id"] == 4
            if record["cell_index"] < 6
            else record["pattern_id"] in (1, 3, 5, 7)
        )
    negative = tool.capacity_dp(list(range(17)), records, tool.new_work(), deadline())
    assert negative["kind"] == "ordinary_assignment_obstruction"
    assert len(tool.decode_bitmap(negative["frontier_bitmaps"][8])) > 1
    tool.verify_state(negative, records, deadline())


@pytest.mark.parametrize("cap", ["triple_attempts", "inequality_evaluations", "dp_transitions"])
def test_work_charged_before_expensive_stage(cap: str, monkeypatch: pytest.MonkeyPatch) -> None:
    constant = {
        "triple_attempts": "TRIPLE_LIMIT",
        "inequality_evaluations": "INEQUALITY_LIMIT",
        "dp_transitions": "TRANSITION_LIMIT",
    }[cap]
    monkeypatch.setattr(tool, constant, 0)

    def operation() -> None:
        if cap == "dp_transitions":
            tool.capacity_dp(list(range(17)), table(), tool.new_work(), deadline())
        else:
            tool.feasible(fixed_polytope(Q(1, 2), Q(1, 2)), tool.new_work(), deadline())

    with pytest.raises(tool.finite.IncompleteError, match="ceiling"):
        operation()


def synthetic_roster() -> list[dict[str, Any]]:
    return [
        {"mask": sum(1 << i for i in cells)}
        for cells in itertools.islice(itertools.combinations(range(24), 17), 95)
    ]


def test_complete95_accounting_endpoint_refusal_and_resource_scope(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(tool, "classify", lambda *_: table())
    endpoint = sum(1 << i for i in list(range(8)) + list(range(12, 21)))
    result = tool.construct([], synthetic_roster(), endpoint, deadline=deadline())
    assert result["states_accounted"] == 95
    assert result["classifications_accounted"] == 216
    assert result["criterion_met"]
    assert result["ordinary_assignment_exclusion_proved"]
    assert not result["global_optimality_proved"]
    with pytest.raises(ValueError, match="endpoint"):
        tool.construct([], synthetic_roster(), (1 << 17) - 1, deadline=deadline())
    with pytest.raises(ValueError, match="complete95"):
        tool.construct([], synthetic_roster()[:-1], endpoint, deadline=deadline())
    assert not any(
        tool.failure(tool.finite.IncompleteError("ceiling"))[k] for k in tool.scope()
    )


def test_generate_fresh_payload_and_byte_mutation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "premise"
    path.write_bytes(b"accepted synthetic premise")
    endpoint = sum(1 << i for i in list(range(8)) + list(range(12, 21)))
    monkeypatch.setattr(
        tool,
        "intake",
        lambda *_: (
            [],
            [str(i) for i in range(24)],
            synthetic_roster(),
            endpoint,
            {path: path.read_bytes()},
        ),
    )
    monkeypatch.setattr(tool, "classify", lambda *_: table())
    descriptor = {"synthetic": True}
    result = tool.generate(descriptor, deadline=deadline())
    assert tool.check(descriptor, result, deadline=deadline())["verification_passed"]
    wrong = copy.deepcopy(result)
    wrong["states"][0]["certificate"]["frontier_bitmaps"][1] = tool.bitmap(set())
    with pytest.raises(ValueError, match="reconstruction"):
        tool.check(descriptor, wrong, deadline=deadline())
    original = tool.construct

    def mutate(*args, **kwargs):
        result = original(*args, **kwargs)
        path.write_bytes(b"changed")
        return result

    monkeypatch.setattr(tool, "construct", mutate)
    with pytest.raises(ValueError, match="bytes changed"):
        tool.generate(descriptor, deadline=deadline())


def test_deadline_geometry_bits_and_nonfinite_cli(tmp_path: Path) -> None:
    with pytest.raises(tool.finite.IncompleteError, match="wall"):
        tool.feasible(fixed_polytope(Q(1, 2), Q(1, 2)), tool.new_work(), 0)
    with pytest.raises(tool.finite.IncompleteError, match="bit"):
        tool.pattern_rows(rectangle(Q(1 << 4097), Q(1)), 0, 0)
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


def test_clean_two_processes_exact_polytopes_and_negative_dp() -> None:
    script = """
import json,time
from fractions import Fraction as Q
from devtools import check_n17_n11_corner_cardinality as t
deadline=time.monotonic()+30
rows=[(Q(1),Q(0),Q(0),Q(0)),(Q(-1),Q(0),Q(0),Q(0)),
(Q(0),Q(1),Q(0),Q(0)),(Q(0),Q(-1),Q(0),Q(0)),
(Q(0),Q(0),Q(1),Q(1,2)),(Q(0),Q(0),Q(-1),Q(-1,2))]
classification=t.feasible(rows,t.new_work(),deadline)
table=[{'cell_index':c,'pattern_id':p,'feasible':p==0,
'guaranteed_window_bits':list(t.pattern_bits(*xy))}
for c in range(24) for p,xy in enumerate(t.CLASSES)]
negative=t.capacity_dp(list(range(17)),table,t.new_work(),deadline)
t.verify_state(negative,table,deadline)
print(json.dumps({'polytope':classification,'negative':negative},sort_keys=True))
"""
    outputs = [
        subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        ).stdout
        for _ in range(2)
    ]
    assert outputs[0] == outputs[1]
    assert json.loads(outputs[0])["negative"]["kind"] == "ordinary_assignment_obstruction"


def test_clean_two_cli_processes_complete_synthetic95_reconstruction(tmp_path: Path) -> None:
    """Explicit synthetic inherited intake; fresh process rechecks all new DP payloads."""
    descriptor = tmp_path / "descriptor.json"
    descriptor.write_text('{"synthetic_inherited_premise":true}')
    certificate, replay = tmp_path / "certificate.json", tmp_path / "replay.json"
    script = """
import itertools,sys
from devtools import check_n17_n11_corner_cardinality as t
records=[{'cell_index':c,'pattern_id':p,'feasible':p==(0 if c<12 else 8),
'guaranteed_window_bits':list(t.pattern_bits(*xy))}
for c in range(24) for p,xy in enumerate(t.CLASSES)]
roster=[{'mask':sum(1<<i for i in cells)}
for cells in itertools.islice(itertools.combinations(range(24),17),95)]
endpoint=sum(1<<i for i in list(range(8))+list(range(12,21)))
t.intake=lambda *_:([],[str(i) for i in range(24)],roster,endpoint,{})
t.classify=lambda *_:records
raise SystemExit(t.main(sys.argv[1:]))
"""
    for extra, output in (([], certificate), (["--certificate", str(certificate)], replay)):
        subprocess.run(
            [
                sys.executable,
                "-c",
                script,
                "--descriptor",
                str(descriptor),
                "--output",
                str(output),
                *extra,
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=60,
        )
    a, b = [json.loads(p.read_text()) for p in (certificate, replay)]
    assert tool.payload(a) == tool.payload(b)
    assert b["verification_passed"]
    assert a["states_accounted"] == 95
