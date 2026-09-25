"""The fixed-angle cell tree and its independent reader (H-236, X-046 rung 0).

Small controls only: the axis family at five squares, whose exact answer 3 comes from
the grid-mark argument, and the four-plus-one family at 45 degrees against s(5).  Each
tree is replayed by the reader, and tampered copies must be refused.
"""

from __future__ import annotations

import argparse
import dataclasses
import gzip
import json
import time
from fractions import Fraction
from pathlib import Path

import pytest

from cases.trump11 import fixed_angle_tree as tree
from cases.trump11 import fixed_angle_tree_check as check


def _options(**overrides: object) -> argparse.Namespace:
    values = {"node_cap": 100_000, "wall_cap": 120.0, "strong": 1} | overrides
    return argparse.Namespace(**values)


def _grow(name: str, path: Path) -> dict[str, object]:
    config, extra = tree.preset(name, _options())
    return tree.run(config, extra, path, lambda _: None)


def _lines(path: Path) -> list[dict[str, object]]:
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        return [json.loads(line) for line in stream]


def _write(path: Path, lines: list[dict[str, object]]) -> None:
    with gzip.open(path, "wt", encoding="utf-8") as stream:
        for line in lines:
            stream.write(json.dumps(line) + "\n")


def _rejected(path: Path) -> bool:
    try:
        check.replay(path)
    except check.RejectionError:
        return True
    return False


def test_rotation_is_exact_on_the_unit_circle() -> None:
    for t in (Fraction(0), Fraction(1, 3), Fraction(365769, 10**6)):
        c, s = tree.rotation(t)
        assert c * c + s * s == 1


def test_window_core_is_inside_and_tight() -> None:
    left, right = Fraction(36, 100), Fraction(37, 100)
    core = tree.window_core(left, right)
    assert tree.core_in_window(core, left, right)
    bigger = tree.Core(core.half_tangent, core.side + Fraction(1, 10**12))
    assert not tree.core_in_window(bigger, left, right)
    # the full unit square at the middle angle sticks out at both endpoints
    assert not tree.core_in_window(tree.Core(core.half_tangent, Fraction(1)), left, right)


def test_interior_maximum_of_an_edge_functional_is_checked() -> None:
    # a point on the bisector of the window from 0 to 2 atan(1/2), at radius 0.514 > 1/2,
    # passes both endpoint tests but must fail the interior test
    left, right = Fraction(0), Fraction(1, 2)
    start, stop = tree.rotation(left), tree.rotation(right)
    point = (Fraction(46, 100), Fraction(23, 100))
    assert point[0] ** 2 + point[1] ** 2 > Fraction(1, 4)
    assert all(a * point[0] + b * point[1] <= Fraction(1, 2) for a, b in (start, stop))
    corners = [point, (-point[0], -point[1])]
    assert not check.window_contains(corners, left, right)
    assert not tree.core_in_window(tree.Core(Fraction(1, 5), Fraction(1)), left, right)


def test_candidate_axes_count_and_order_agree_with_the_reader() -> None:
    family = tree.Family(2, 2, Fraction(36, 100), Fraction(37, 100))
    core = family.tilted_core
    head = {
        "family": {"axis_count": 2, "tilted_count": 2, "left": "36/100", "right": "37/100"},
        "core": {"half_tangent": str(core.half_tangent), "side": str(core.side)},
        "symmetry": {"quadrant": "tilted", "order_epsilon": "1/4"},
        "variable_cap": "4",
        "target": {"upper": "3"},
    }
    program = check.build_program(head)
    assert [len(family.axes(i, j)) for i, j in family.pairs] == [4, 8, 8, 8, 8, 4]
    for i, j in family.pairs:
        assert list(family.axes(i, j)) == program.options(i, j)
        for option in range(len(family.axes(i, j))):
            row = tree.pair_row(family, i, j, option)
            coefficients, rhs = program.pair(i, j, option)
            assert dict(row.coefficients) == coefficients
            assert row.rhs == rhs
    base = {
        row.label: (dict(row.coefficients), row.rhs)
        for row in tree.base_rows(family, "tilted", tree.ORDER_EPSILON)
    }
    assert base == program.base


def test_axis_control_closes_below_three_and_opens_above(tmp_path: Path) -> None:
    below, above = tmp_path / "below.jsonl.gz", tmp_path / "above.jsonl.gz"
    assert _grow("control-axis-5-below", below)["closed"]
    assert check.replay(below)["verdict"] == "closed"
    summary = _grow("control-axis-5-above", above)
    assert not summary["closed"]
    assert check.replay(above)["verdict"] == "incomplete"


def test_n5_control_closes_below_s5_and_captures_goebel(tmp_path: Path) -> None:
    below, capture = tmp_path / "n5.jsonl.gz", tmp_path / "capture.jsonl.gz"
    assert _grow("control-n5", below)["closed"]
    assert check.replay(below)["verdict"] == "closed"
    summary = _grow("control-n5-capture", capture)
    assert summary["closed"]
    leaves = summary["leaves"]
    assert isinstance(leaves, dict)
    assert leaves.get("t", 0) >= 1
    replayed = check.replay(capture)
    assert replayed["verdict"] == "closed"
    assert replayed["statement"]["capture_only"]


def test_tampered_trees_are_refused(tmp_path: Path) -> None:
    source = tmp_path / "n5.jsonl.gz"
    _grow("control-n5", source)
    lines = _lines(source)
    bound_leaf = next(k for k, line in enumerate(lines) if "c" in line)
    farkas_leaf = next(k for k, line in enumerate(lines) if "f" in line)
    branch = next(k for k, line in enumerate(lines) if "b" in line and k > 1)

    def mutated(index: int, change: dict[str, object], drop: str | None = None) -> Path:
        copy = [dict(line) for line in lines]
        copy[index] = copy[index] | change
        if drop is not None:
            del copy[index][drop]
        path = tmp_path / f"mutant-{index}-{len(change)}-{drop}.jsonl.gz"
        _write(path, copy)
        return path

    weights = lines[bound_leaf]["c"]
    assert isinstance(weights, dict)
    halved = {label: str(Fraction(value) / 2) for label, value in weights.items()}
    assert _rejected(mutated(bound_leaf, {"c": halved}))
    farkas = lines[farkas_leaf]["f"]
    assert isinstance(farkas, dict)
    first = min(farkas)
    assert _rejected(mutated(farkas_leaf, {"f": {**farkas, first: "0"}}))
    assert _rejected(mutated(branch, {"n": 3}))
    unresolved = mutated(bound_leaf, {"u": "withdrawn"}, drop="c")
    assert check.replay(unresolved)["verdict"] == "incomplete"
    shorter = tmp_path / "shorter.jsonl.gz"
    _write(shorter, lines[:-1])
    assert _rejected(shorter)
    raised = tmp_path / "raised.jsonl.gz"
    header = json.loads(json.dumps(lines[0]))
    header["header"]["target"]["upper"] = "272/100"
    _write(raised, [header, *lines[1:]])
    assert _rejected(raised)


def test_trump_image_satisfies_the_symmetry_rows_strictly() -> None:
    family, (_, u_hi), image, _ = tree.trump_setup(Fraction(1, 10**6))
    assert family.left < family.right
    rows = tree.base_rows(family, "tilted", tree.ORDER_EPSILON)
    point = [*image.floats(), float(u_hi)]
    symmetric = [row for row in rows if not row.label.startswith("wall:")]
    assert len(symmetric) == 5 + 4 + 2
    for row in symmetric:
        value = sum(float(v) * point[k] for k, v in row.coefficients) - float(row.rhs)
        assert value > 0.1, row.label


def test_reader_accepts_the_h236_header_and_its_angle_box() -> None:
    config, extra = tree.preset("h236", _options())
    head = tree.header(config, extra)
    program = check.build_program(head)
    statement = check.check_target_and_image(head, program)
    assert statement["target_is_at_least_U"]
    assert statement["angle_reach_bound"] < float(tree.TRUMP_RHO)
    assert statement["_radius"] == check.BC240_RHO


def test_trump_cell_is_closed_by_the_local_theorem(tmp_path: Path) -> None:
    """Fix the sixteen tightest pairs at Trump's image; the rest must close by rho."""
    config, extra = tree.preset("h236", _options(strong=6))
    root = tree.trump_cell(config)
    out = tmp_path / "trump-cell.jsonl.gz"
    summary = tree.run(dataclasses.replace(config, root_path=root), extra, out, lambda _: None)
    assert summary["leaves"] == {"t": 1}
    stream = check.records(out)
    head = next(stream)["header"]
    program = check.build_program(head)
    statement = check.check_target_and_image(head, program)
    report = check.Report()
    check.walk(
        program,
        stream=stream,
        fixed={(i, j): option for i, j, option in head["root_path"]},
        splits=False,
        image=statement["_image"],
        radius=statement["_radius"],
        report=report,
        limit=None,
    )
    assert report.kinds == {"t": 1}
    assert report.reach < Fraction(1, 10**4)


def test_parallel_split_is_replayed_file_by_file(tmp_path: Path) -> None:
    config, extra = tree.preset("control-n5-capture", _options())
    out = tmp_path / "split.jsonl.gz"
    summary = tree.run_parallel(
        config, extra, out, workers=2, split_depth=2, progress=lambda _: None
    )
    assert summary["closed"]
    replayed = check.replay(out, workers=2)
    assert replayed["verdict"] == "closed"
    assert replayed["subtree_files"] == summary["subtrees"]
    first = tree.subtree_directory(out) / "sub-00000.jsonl.gz"
    lines = _lines(first)
    header = json.loads(json.dumps(lines[0]))
    header["header"]["root_path"] = header["header"]["root_path"][:-1]
    _write(first, [header, *lines[1:]])
    assert _rejected(out)


def test_trump_cell_stays_open_above_u_without_the_theorem(tmp_path: Path) -> None:
    config, extra = tree.preset("control-n11-negative-cell", _options(strong=6))
    summary = tree.run(config, extra, tmp_path / "open.jsonl.gz", lambda _: None)
    assert not summary["closed"]
    assert summary["unresolved_sample"][0]["reason"] == "open"


def test_resumed_subtrees_replace_their_files_and_replay(tmp_path: Path) -> None:
    config, extra = tree.preset("control-n5-capture", _options())
    out = tmp_path / "split.jsonl.gz"
    summary = tree.run_parallel(
        config, extra, out, workers=2, split_depth=2, progress=lambda _: None
    )
    paths = tree.frontier_paths(out)
    assert len(paths) == summary["subtrees"]
    first = tree.subtree_directory(out) / "sub-00000.jsonl.gz"
    header = _lines(first)[0]
    recorded = header["header"]
    assert isinstance(recorded, dict)
    assert recorded["root_path"] == [list(step) for step in paths[0]]
    # stand in for an interrupted subtree: its root capped at the wall
    _write(first, [header, {"o": None, "u": "wall-cap"}])
    assert check.replay(out)["verdict"] == "incomplete"
    now = time.time()
    resumed = tree.run_resume(
        config,
        extra,
        out,
        indices=[0, 1],
        workers=2,
        launch_by=now + 600,
        stop_at=now + 900,
        progress=lambda _: None,
    )
    assert resumed["closed"]
    assert check.replay(out)["verdict"] == "closed"
    late = tree.run_resume(
        config,
        extra,
        out,
        indices=[1],
        workers=1,
        launch_by=now - 1,
        stop_at=now + 900,
        progress=lambda _: None,
    )
    assert late["leaves"] == {"u": 1}
    assert check.replay(out)["verdict"] == "incomplete"


def _box_options(**overrides: object) -> argparse.Namespace:
    box: dict[str, object] = {"t_lo": None, "t_hi": None, "target": None}
    box |= {"axis_count": 6, "tilted_count": 5}
    return _options(**(box | overrides))


def _box(tmp_path: Path, name: str, **overrides: object) -> tuple[Path, dict[str, object]]:
    """A four-plus-one box at t in [1/5, 201/1000], about 22.6 degrees, far from 45."""
    options: dict[str, object] = {"t_lo": Fraction(1, 5), "t_hi": Fraction(201, 1000)}
    options |= {"axis_count": 4, "tilted_count": 1} | overrides
    config, extra = tree.preset("box", _box_options(**options))
    out = tmp_path / f"{name}.jsonl.gz"
    return out, tree.run(config, extra, out, lambda _: None)


def test_box_preset_closes_below_s5_and_opens_above_a_packing(tmp_path: Path) -> None:
    # every five unit squares need side s(5) > 27/10; four corners and a centred square
    # of any tilt fit in side 3, so 3001/1000 must meet an open leaf
    below, summary = _box(tmp_path, "below", target=Fraction(27, 10))
    assert summary["closed"]
    replayed = check.replay(below)
    assert replayed["verdict"] == "closed"
    assert replayed["statement"]["half_tangent_box"] == ["1/5", "201/1000"]
    above, summary = _box(tmp_path, "above", target=Fraction(3001, 1000))
    assert summary["stopped"] == "stopped-on-open"
    assert check.replay(above)["unresolved_by_reason"]["open"] == 1
    lines = _lines(below)
    bound_leaf = next(k for k, line in enumerate(lines) if "c" in line)
    degenerate = [dict(line) for line in lines]
    degenerate[bound_leaf] = {"o": lines[bound_leaf]["o"], "t": {"lo": [], "hi": []}}
    _write(tmp_path / "degenerate.jsonl.gz", degenerate)
    assert _rejected(tmp_path / "degenerate.jsonl.gz")
    for key, value in (("right", "21/100"), ("left", "19/100")):
        header = json.loads(json.dumps(lines[0]))
        header["header"]["family"][key] = value
        _write(tmp_path / f"wider-{key}.jsonl.gz", [header, *lines[1:]])
        assert _rejected(tmp_path / f"wider-{key}.jsonl.gz")


def test_box_preset_takes_the_trump_image_only_around_t_star() -> None:
    h236, extra = tree.preset("h236", _options())
    left, right = h236.family.left, h236.family.right
    root_lo, root_hi = (Fraction(bound) for bound in extra["u_enclosure"])
    same, _ = tree.preset("box", _box_options(t_lo=left, t_hi=right))
    assert tree.header(same, {}) == tree.header(h236, {})
    far, _ = tree.preset("box", _box_options(t_lo=Fraction(1, 5), t_hi=Fraction(201, 1000)))
    assert far.image is None
    assert far.target == h236.target
    program = check.build_program(tree.header(far, {}))
    assert check.check_target_and_image(tree.header(far, {}), program)["target_is_at_least_U"]
    declared, _ = tree.preset("box", _box_options(t_lo=left, t_hi=right, target=Fraction(3)))
    assert declared.image is None
    far_box: dict[str, object] = {"t_lo": Fraction(1, 5), "t_hi": Fraction(201, 1000)}
    refused: list[tuple[dict[str, object], str]] = [
        ({"t_lo": Fraction(36, 100), "t_hi": Fraction(37, 100)}, "too wide for rho"),
        ({"t_lo": left, "t_hi": (root_lo + root_hi) / 2}, "straddles an end"),
        ({"t_lo": Fraction(1, 5), "t_hi": Fraction(1, 5)}, "a box needs 0"),
        (far_box | {"axis_count": 4}, "other counts need --target"),
        (far_box | {"target": Fraction(4)}, "inside the variable box"),
    ]
    for case, reason in refused:
        with pytest.raises(SystemExit, match=reason):
            tree.preset("box", _box_options(**case))
