"""The finite steps of Guzhou0806's s(40) > 335427/50000 (#485) hold, and refuse controls.

`devtools.audit_clipped_corner_transfer` re-derives the release's 401-direction input
from the retained ``rect_n40_L67`` density, decides the density's peak and the transfer's
scalar chain in exact rationals, and compares them with both release receipts. These tests
read retained files only and run no binary: the replay and controls A to D are the
packet's receipts, judged here as `check-replay` judges them.
"""

from __future__ import annotations

import copy
import functools
import gzip
import itertools
import json
import random
import shutil
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools import audit_clipped_corner_transfer as audit
from devtools.audit_clipped_corner_transfer import CLAIM, Facts, Transfer

#: The exact essential supremum the review computed by its own sweep (item 5).
REVIEW_PEAK = Fraction(
    744157113224753949201233200959491557948628550000000000000000000000000000000,
    264006142643866310314006500845084529851262768737056316088338267454599309,
)


@functools.cache
def density() -> audit.Density:
    return audit.load_density()


@functools.cache
def facts() -> Facts:
    return audit.facts(density())


def test_the_derived_input_is_the_one_both_receipts_decided() -> None:
    data = audit.derived_input(density(), CLAIM)
    assert audit.sha256(data) == audit.DERIVED_SHA256
    value = json.loads(data)
    assert value["certificate"] == {
        "L": "67/10",
        "B": "9977/10000",
        "D": "83/80000",
        "angle_count": 401,
    }
    assert len(value["rectangles"]) == len(value["weights"]) == 480


def test_the_density_expands_as_the_review_counts() -> None:
    f = facts()
    assert (f.listed, f.positive, f.terms, f.distinct) == (2526, 480, 3840, 3792)
    assert f.mass == f.integral == Fraction(3999, 100)
    assert f.invariant


def test_the_peak_is_the_reviews_and_below_h() -> None:
    f = facts()
    assert f.peak == REVIEW_PEAK
    assert f.peak <= CLAIM.H
    assert f.rounded_peak == CLAIM.H


def _brute_peak(items: list[tuple[int, int, int, int, int]]) -> int:
    """The greatest stack at the centre of every cell of the full grid."""
    xs = sorted({v for item in items for v in (item[0], item[2])})
    ys = sorted({v for item in items for v in (item[1], item[3])})
    best = 0
    for xa, xb in itertools.pairwise(xs):
        for ya, yb in itertools.pairwise(ys):
            x, y = Fraction(xa + xb, 2), Fraction(ya + yb, 2)
            total = sum(v for x1, y1, x2, y2, v in items if x1 < x < x2 and y1 < y < y2)
            best = max(best, total)
    return best


def test_the_stack_sweep_agrees_with_a_brute_force_grid() -> None:
    generator = random.Random(485)
    for _ in range(60):
        items = []
        for _ in range(generator.randint(1, 9)):
            x1, x2 = sorted(generator.sample(range(12), 2))
            y1, y2 = sorted(generator.sample(range(12), 2))
            items.append((x1, y1, x2, y2, generator.randint(1, 5)))
        best, (cx, cy) = audit.stack_peak(items)
        assert best == _brute_peak(items)
        corner = sum(v for x1, y1, x2, y2, v in items if x1 <= cx < x2 and y1 <= cy < y2)
        assert corner == best


def test_every_finite_check_holds_against_both_receipts() -> None:
    report = audit.check_report(facts())
    failed = [check["name"] for check in report["checks"] if not check["held"]]
    assert failed == []
    assert report["status"] == "FINITE_STEPS_HOLD"
    assert set(audit.RECEIPTS) == {"local", "ci"}


def test_the_chain_is_the_reviews() -> None:
    chain = audit.chain(CLAIM)
    assert chain.q == Fraction(335000, 335427)
    assert chain.b == Fraction(41804244441680000, 80000042740596391757)
    assert chain.chi >= CLAIM.charge
    assert chain.simple == Fraction(1, 625)
    assert chain.uncut == Fraction(28729630924721000000, 638381969559824281)
    assert 0 < chain.q - chain.reach0 < Fraction(2, 10**15)


def test_controls_e_to_h_are_refused() -> None:
    controls = {str(item["control"]): item for item in audit.finite_controls(facts())}
    assert sorted(controls) == ["E", "F", "G", "H"]
    assert all(item["refused"] for item in controls.values())
    assert Fraction(str(controls["F"]["margin_upper_bound"])) < 0
    assert Fraction(str(controls["H"]["chi"])) < 0


def test_the_next_side_fails_at_every_admissible_h() -> None:
    at_next = Transfer(X=Fraction(335428, 50000))
    low, high, bound = audit.best_counting_margin(at_next)
    assert audit.containment(at_next, low)
    assert not audit.containment(at_next, high)
    assert high - low < Fraction(1, 10**40)
    assert bound < 0
    # At the claim's own side the release's h is admissible and the margin is positive.
    low, _, bound = audit.best_counting_margin(CLAIM)
    assert CLAIM.h <= low
    assert bound > 0


def test_a_changed_receipt_value_is_refused() -> None:
    receipt = audit.read_receipt(audit.RECEIPTS["ci"])
    changed = copy.deepcopy(receipt)
    value = Fraction(changed["finite"]["cap_area_upper"])
    changed["finite"]["cap_area_upper"] = str(value * Fraction(101, 100))
    failed = [c.name for c in audit.receipt_checks("ci", changed, CLAIM, facts()) if not c.held]
    assert failed == ["ci receipt: finite.cap_area_upper"]
    changed = copy.deepcopy(receipt)
    changed["node_summary"]["premises"]["angle_count"] = 201
    failed = [c.name for c in audit.receipt_checks("ci", changed, CLAIM, facts()) if not c.held]
    assert failed == ["ci receipt: nodal premises"]


def test_a_changed_weight_changes_the_mass_and_the_input() -> None:
    raw = json.loads(audit.read_retained_bytes(audit.CANDIDATE), parse_float=str)
    first = next(i for i, w in enumerate(raw["weights"]) if w != "0")
    raw["weights"][first] = str(Fraction(raw["weights"][first]) * 2)
    changed = audit.read_density(json.dumps(raw).encode())
    assert sum((w for _, w in changed.rows), Fraction(0)) != CLAIM.mass
    assert audit.sha256(audit.derived_input(changed, CLAIM)) != audit.DERIVED_SHA256


def test_the_control_inputs_change_only_what_they_name() -> None:
    derived = audit.derived_input(density(), CLAIM)
    selection = {"capture": "1001316565761/1000000000000"}
    inputs = {
        name: json.loads(data) for name, data in audit.mutants(derived, selection).items()
    }
    original = json.loads(derived)
    assert inputs["A"]["certificate"] == original["certificate"]
    assert [Fraction(w) for w in inputs["A"]["weights"]] == [
        Fraction(w) * Fraction(99, 100) for w in original["weights"]
    ]
    assert "certificate" not in inputs["C"]
    assert inputs["C"]["weights"] == original["weights"]
    assert inputs["D"]["certificate"]["angle_count"] == 201
    assert inputs["D"]["certificate"]["D"] == "83/80000"
    # The census's rule: the largest multiple of 1e-15 that leaves the capture at the
    # control centre at most one part in a million below the threshold.
    capture = Fraction(selection["capture"])
    near = audit.near_factor(capture)
    limit = CLAIM.tau * (1 - Fraction(1, 10**6)) / capture
    assert near <= limit < near + Fraction(1, 10**15)


def test_the_replay_receipts_hold() -> None:
    report = audit.replay_report(audit.RECEIPT_DIR, facts(), rank=False)
    failed = [check["name"] for check in report["checks"] if not check["held"]]
    assert failed == []
    assert report["status"] == "REPLAY_HOLDS"


def _rewrite(path: Path, edit: Any) -> None:
    lines = [json.loads(line) for line in gzip.decompress(path.read_bytes()).splitlines()]
    edit(lines)
    body = "".join(json.dumps(line, sort_keys=True) + "\n" for line in lines)
    path.write_bytes(gzip.compress(body.encode(), mtime=0))


def test_a_changed_replay_row_is_refused(tmp_path: Path) -> None:
    folder = tmp_path / "receipts"
    shutil.copytree(audit.RECEIPT_DIR, folder)

    def unverify(lines: list[dict[str, Any]]) -> None:
        lines[5]["verdict"] = "unresolved"

    _rewrite(folder / f"{audit.REPLAY}.jsonl.gz", unverify)
    report = audit.replay_report(folder, facts(), rank=False)
    failed = {check["name"] for check in report["checks"] if not check["held"]}
    assert "replay: every direction verified" in failed
    assert "replay: rows equal the ci receipt's apart from timing" in failed
    assert report["status"] == "REPLAY_CHECK_FAILED"


def test_a_control_that_verified_is_refused(tmp_path: Path) -> None:
    folder = tmp_path / "receipts"
    shutil.copytree(audit.RECEIPT_DIR, folder)

    def admit(lines: list[dict[str, Any]]) -> None:
        for line in lines:
            if line.get("r") == 220:
                line["verdict"] = "verified"
                line.pop("witness", None)

    _rewrite(folder / "control-B-near-threshold.jsonl.gz", admit)
    report = audit.replay_report(folder, facts(), rank=False)
    failed = {check["name"] for check in report["checks"] if not check["held"]}
    assert "control B: r = 220 refused" in failed
