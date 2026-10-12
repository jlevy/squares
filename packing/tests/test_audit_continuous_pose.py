"""The finite steps of Guzhou0806's s(40) > 1340000/199529 (#485) hold, and refuse controls.

`devtools.audit_continuous_pose` regenerates both kernel inputs and both crate inputs
from the retained ``rect_n40_L67`` density, decides the claim's finite steps in exact
rationals, and compares them with both release receipts. These tests read retained files
only and run no binary: the replay is the packet's receipts, judged here as
``check-replay`` judges them.
"""

from __future__ import annotations

import dataclasses
import functools
import gzip
import json
import math
import random
import shutil
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import audit_continuous_pose as audit
from devtools.audit_continuous_pose import CLAIM, Facts


@functools.cache
def density() -> audit.Density:
    return audit.load_density()


@functools.cache
def facts() -> Facts:
    return audit.facts(density())


def least() -> Fraction:
    return audit.least_bound(audit.read_slabs(audit.RECEIPTS["ci"]))[0]


def test_the_inputs_are_the_ones_the_receipts_decided() -> None:
    assert audit.sha256(audit.pose_input(density())) == audit.POSE_SHA256
    assert audit.sha256(audit.axis_input(audit.axis_rows(density()))) == audit.AXIS_SHA256
    inputs = audit.crate_inputs(density())
    assert {name: audit.sha256(data) for name, data in inputs.items()} == audit.CRATE_SHA256
    net = json.loads(inputs["net401-B"])
    assert net["certificate"] == {
        "L": "67/10",
        "B": "199529/200000",
        "D": "83/80000",
        "angle_count": 401,
    }
    assert net["coverage_lower_bound_exact"] == "1"


def test_the_axis_header_is_the_contracts() -> None:
    data = audit.axis_input(audit.axis_rows(density()))
    assert data.splitlines()[0] == b"6700000000 997643000 1000000000 1000000000 4999 5000 3840"
    pose = audit.pose_input(density()).splitlines()
    assert pose[2] == b"3840"
    assert len(pose) == 3843


def test_every_finite_check_holds_against_both_receipts() -> None:
    report = audit.check_report(facts())
    failed = [check["name"] for check in report["checks"] if not check["held"]]
    assert failed == []
    assert report["status"] == "FINITE_STEPS_HOLD"
    assert set(audit.RECEIPTS) == {"local", "ci"}


def test_the_scalars_are_the_reviews() -> None:
    assert CLAIM.n * CLAIM.tau - CLAIM.mass == Fraction(1, 500)
    assert CLAIM.L / CLAIM.B == CLAIM.X
    assert Fraction(72586117, 9976450000) == CLAIM.X - audit.EARLIER
    assert Fraction(89, 40000) == CLAIM.T**2 + 2 * CLAIM.T - 1
    margin = CLAIM.B - CLAIM.A * audit.extent(CLAIM.eps)
    assert margin == Fraction(589499411, 125000000000125000)
    threshold = Fraction(audit.kernel_threshold(CLAIM.tau))
    assert 0 < threshold - CLAIM.tau < Fraction(2, 10**16)
    assert len(CLAIM.slabs()) == 43
    assert least() == Fraction(2251349454150741, 2**51)


def test_the_axis_minimum_is_evaluated_again_at_its_minimiser() -> None:
    f = facts()
    assert f.minimiser == (4207731377, 6201178500)
    assert f.minimum == f.minimiser_capture == 999803584931237207459144828
    assert Fraction(f.minimum, 10**27) == Fraction(249950896232809301864786207, 25 * 10**25)
    assert f.minimiser_capture_g * 10**27 >= f.minimum
    assert f.nodes == (2213, 2213)
    assert f.evaluation_bound == 384178892657373682994447839008000000 < 2**125


def test_the_finite_controls_are_refused() -> None:
    controls = {str(item["control"]): item for item in audit.finite_controls(facts(), least())}
    assert sorted(controls) == ["G", "G2", "G3", "G4"]
    assert all(item["refused"] for item in controls.values())
    # The contract's G: A W(eps) - B is about 1e-6 against a margin of 4.7e-9.
    margin = Fraction(str(controls["G"]["near_axis_margin"]))
    assert Fraction(-1, 10**6) < margin < Fraction(-9, 10**7)


def test_an_axis_minimum_below_tau_is_refused() -> None:
    required = audit.ceil_div(10**27 * 4999, 5000)
    short = dataclasses.replace(facts(), minimum=required - 1)
    failed = [c.name for c in audit.chain_checks(CLAIM, short, least()) if not c.held]
    assert failed == ["axis: the receipts' minimum is at least tau"]
    low = least() - Fraction(1, 10**9)
    failed = [c.name for c in audit.chain_checks(CLAIM, facts(), low) if not c.held]
    assert failed == ["slabs: the receipts' least leaf bound is at least the threshold"]


def test_every_enclosure_brackets_and_is_tight() -> None:
    generator = random.Random(485)
    for _ in range(2000):
        x = Fraction(generator.randint(-(10**12), 10**12), generator.randint(1, 10**9))
        lo, hi = audit.enclose(x)
        assert Fraction(lo) <= x <= Fraction(hi)
        assert hi == lo or hi == math.nextafter(lo, math.inf)
    assert audit.enclose(Fraction(1, 2)) == (0.5, 0.5)


def _copy_receipt(tmp_path: Path) -> Path:
    folder = tmp_path / "results"
    shutil.copytree(audit.RECEIPTS["ci"], folder)
    return folder


def _failed(folder: Path) -> list[str]:
    checks = audit.receipt_checks("ci", folder, CLAIM, facts())
    return [check.name for check in checks if not check.held]


def test_a_changed_receipt_value_is_refused(tmp_path: Path) -> None:
    folder = _copy_receipt(tmp_path)
    receipt = json.loads((folder / "verification.json").read_text())
    receipt["coverage"]["nodes"] += 1
    (folder / "verification.json").write_text(json.dumps(receipt))
    assert _failed(folder) == ["ci receipt: coverage block is the slabs' totals"]
    receipt["coverage"]["nodes"] -= 1
    receipt["scalar"]["counting_margin"] = "1/400"
    (folder / "verification.json").write_text(json.dumps(receipt))
    assert _failed(folder) == ["ci receipt: scalar block"]


def test_a_slab_that_did_not_verify_is_refused(tmp_path: Path) -> None:
    folder = _copy_receipt(tmp_path)
    rows = [json.loads(line) for line in (folder / "slabs.jsonl").read_text().splitlines()]
    out = json.loads(rows[7]["stdout"])
    out["status"] = "unresolved"
    rows[7]["stdout"] = json.dumps(out)
    (folder / "slabs.jsonl").write_text("".join(json.dumps(row) + "\n" for row in rows))
    failed = _failed(folder)
    assert "ci receipt: every slab verified as the contract runs it" in failed
    assert "ci receipt: slab and axis records by digest" in failed


def test_the_cut_area_is_continuous_and_decreasing() -> None:
    side = CLAIM.B
    h = Fraction(1, 100)
    # The regime changes where h = B sin(theta); both formulas agree there.
    previous = None
    for numerator in range(500, 10001, 500):
        cut = audit.cut_area(h, Fraction(numerator, 10**6), side)
        assert previous is None or cut < previous
        previous = cut
    t = Fraction(1, 200)
    c, s = audit.half_angle(t)
    edge = side * s
    assert audit.cut_area(edge, t, side) == edge * edge / (2 * s * c)
    assert audit.cut_area(edge, t, side) == side / c * (edge - side * s / 2)


def test_the_kernel_controls_straddle_tau_as_the_contract_says() -> None:
    controls = audit.kernel_controls()
    names = [control.name for control in controls]
    assert len(names) == len(set(names)) == 3 + 3 + 14 + 5 + 14 + 1
    for control in controls:
        if control.least is None:
            continue
        refuse = control.expect_exit == 3
        assert (control.least < CLAIM.tau) == refuse, control.name


def test_the_axis_capture_agrees_with_the_rational_one() -> None:
    generator = random.Random(40)
    grid = audit.GRID
    terms: list[audit.Term] = []
    rows: list[audit.Row] = []
    for _ in range(30):
        x1, x2 = sorted(generator.sample(range(6700), 2))
        y1, y2 = sorted(generator.sample(range(6700), 2))
        w = generator.randint(1, 10**6)
        rows.append((x1 * 10**6, y1 * 10**6, x2 * 10**6, y2 * 10**6, w))
        terms.append(
            (
                Fraction(x1, 1000),
                Fraction(y1, 1000),
                Fraction(x2, 1000),
                Fraction(y2, 1000),
                Fraction(w, grid),
            )
        )
    side = int(CLAIM.A * grid)
    for _ in range(20):
        x, y = (
            generator.randint(3_350_000_000, 6_201_178_500),
            generator.randint(0, 6_700_000_000),
        )
        exact = audit.term_capture(terms, Fraction(x, grid), Fraction(y, grid), CLAIM.A)
        assert Fraction(audit.axis_capture(rows, x, y, side), grid**3) == exact


def test_the_replay_receipts_hold() -> None:
    report = audit.replay_report(audit.RECEIPT_DIR)
    failed = [check["name"] for check in report["checks"] if not check["held"]]
    assert failed == []
    assert report["status"] == "REPLAY_HOLDS"


def _rewrite(path: Path, edit: Any) -> None:
    lines = [json.loads(line) for line in gzip.decompress(path.read_bytes()).splitlines()]
    edit(lines)
    body = "".join(json.dumps(line, sort_keys=True) + "\n" for line in lines)
    path.write_bytes(gzip.compress(body.encode(), mtime=0))


def test_a_changed_replay_slab_is_refused(tmp_path: Path) -> None:
    folder = tmp_path / "receipts"
    shutil.copytree(audit.RECEIPT_DIR, folder)

    def more_nodes(lines: list[dict[str, Any]]) -> None:
        out = json.loads(lines[3]["stdout"])
        out["nodes"] += 2
        out["leaves"] += 1
        lines[3]["stdout"] = json.dumps(out)

    _rewrite(folder / "slabs.jsonl.gz", more_nodes)
    report = audit.replay_report(folder)
    failed = {check["name"] for check in report["checks"] if not check["held"]}
    assert failed == {
        "slabs: the totals",
        "slabs: every non-timing field equals the local receipt's",
        "slabs: every non-timing field equals the ci receipt's",
    }
    assert report["status"] == "REPLAY_CHECK_FAILED"


def test_a_control_that_was_accepted_is_refused(tmp_path: Path) -> None:
    folder = tmp_path / "receipts"
    shutil.copytree(audit.RECEIPT_DIR, folder)
    name = "C-cut-top-500-10000-h100"

    def accept(lines: list[dict[str, Any]]) -> None:
        for line in lines:
            if line["control"] == name:
                line["exit_code"] = 0
                line["stdout"] = json.dumps({"status": "verified", "nodes": 9})

    _rewrite(folder / "controls.jsonl.gz", accept)
    report = audit.replay_report(folder)
    failed = {check["name"] for check in report["checks"] if not check["held"]}
    assert failed == {f"control {name}"}


# --------------------------------------------------------------------------- the runner
# A slab stage stopped from outside loses only the slabs in flight: each row is written as
# it finishes, and a later run in the same directory keeps a row that names the same
# binary, input and arguments, with that row's own timing.


def _fake_kernel(path: Path) -> None:
    path.write_text(
        '#!/bin/sh\necho \'{"status":"verified","nodes":3,"leaves":2,"angle_splits":1,'
        '"lower_bound":"0.9999","pl":\'"$1"\',"ph":\'"$2"\',"den":\'"$3"\'}\'\n'
    )
    path.chmod(0o755)


def test_a_stopped_slab_stage_keeps_its_finished_rows(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    layout = audit.Layout(tmp_path)
    layout.build.mkdir()
    layout.pose.mkdir()
    layout.logs.mkdir()
    _fake_kernel(layout.binary("pose"))
    claim = dataclasses.replace(CLAIM, endpoints=(1, 500, 10000))
    inputs = {"pose": "0" * 64, "axis": "1" * 64}
    first = audit.run_slabs(layout, inputs, 1, claim)
    assert [row["index"] for row in first] == [0, 1]
    assert sorted(p.name for p in (tmp_path / "slab-rows").iterdir()) == [
        "slab-000.json",
        "slab-001.json",
    ]
    # A second run keeps both rows, timing included.
    (tmp_path / "slab-rows/slab-001.json").unlink()
    again = audit.run_slabs(layout, inputs, 1, claim)
    assert again[0] == first[0]
    assert again[1]["argv"] == first[1]["argv"]
    assert again[1] is not first[1]
    out = capsys.readouterr().out
    assert "slab 0: kept from an earlier run, exit 0" in out
    assert "slab 1: exit 0" in out
    # Another binary, input or argument list reruns the slab rather than keeping the row.
    (layout.binary("pose")).write_bytes(layout.binary("pose").read_bytes() + b"\n")
    rerun = audit.run_slabs(layout, inputs, 1, claim)
    assert rerun[0]["binary_sha256"] != first[0]["binary_sha256"]
    assert "kept" not in capsys.readouterr().out
    other = audit.run_slabs(layout, {**inputs, "pose": "2" * 64}, 1, claim)
    assert other[0]["input_sha256"] == "2" * 64
    assert "kept" not in capsys.readouterr().out
