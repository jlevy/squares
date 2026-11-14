"""The independent labeller of Lemma 4.10 of Ryu's k2-minus-c, and what its run decided.

``cases/asymptotic/ryu_k2_minus_c_labels.py`` decides the 78,673 boxes of the
certificate of Lemma 4.10 again, written from the proof and the disc model of the TeX
without reading the source's programs. The first tests hold its parts to independent
computations: the constants against mpmath at 200 bits, the exact point count against
hand counts, the arc bounds against dense sampling, the box decisions on the n = 1 lists
and on the box that holds the nine-pair configuration, and the exact witness checker.
The last tests read the receipts the full run left in the
``squarepacker-k2-minus-c-2026-10-05`` packet: every box decided once, every one
certified as labelled and none near the budget of ``MAX_PIECES``, the ten negative
controls refused by decision under that budget with refuting witnesses, and a sample
decided again with identical rows after review A of #884.
"""

from __future__ import annotations

import json
import math
import random
import re
import sys
import types
from collections.abc import Iterator
from fractions import Fraction
from pathlib import Path
from typing import Any

import mpmath
import numpy as np
import pytest

from cases.asymptotic import ryu_k2_minus_c_labels as labels
from devtools.retained_data import read_retained_text

RECEIPTS = labels.PACKET / "receipts/independent-labels"
BOXES = 78_673
CLASS_SIZES = {"inf": 72_174, "nowall": 1_094, "closed": 5_405}


@pytest.fixture(autouse=True)
def _restore_mpmath_precision() -> Iterator[None]:
    """The module and these tests set mpmath's precision, and the test files that run
    after them in the same process expect it as they left it."""
    mp_prec, iv_prec = mpmath.mp.prec, mpmath.iv.prec
    yield
    mpmath.mp.prec, mpmath.iv.prec = mp_prec, iv_prec


_FOOTER = re.compile(
    r"^# finished \S+; exit (?P<exit>-?\d+); wall [\d.]+ s; CPU (?P<cpu>[\d.]+) s"
)


def test_the_constants_bound_their_exact_values() -> None:
    mpmath.mp.prec = 200
    d = mpmath.mpf(1) / 10000
    lam = d + mpmath.sqrt(2)
    constants = labels.constants()
    assert constants.lam_hi >= lam
    assert constants.lam_sq_hi >= lam**2
    assert constants.rho1_sq_lo <= (d + mpmath.sqrt(2) / 2) ** 2 + mpmath.mpf(1) / 4
    assert constants.wall_hi >= d + mpmath.sqrt(2) / 2
    gamma0 = mpmath.acos(1 - 1 / (2 * lam**2))
    turns = gamma0 / (2 * mpmath.pi) * labels.TURN
    assert turns - 32 < constants.separation < turns
    assert labels.TURN // constants.separation == 8


def test_the_direction_table_encloses_cos_and_sin() -> None:
    mpmath.mp.prec = 200
    cos_lo, cos_hi, sin_lo, sin_hi = labels.direction_table()
    total = 1 << labels.TABLE_LEVEL
    picks = [0, total // 8, total // 4, total // 2, total - 1, total]
    picks += random.Random(7).sample(range(total), 400)
    for k in picks:
        # mpmath's pi is rounded at 200 bits, so its cos(pi/2) is 1e-61, not 0.
        angle = 2 * mpmath.pi * k / total
        slack = mpmath.mpf(10) ** -50
        assert cos_lo[k] - slack <= mpmath.cos(angle) <= cos_hi[k] + slack
        assert sin_lo[k] - slack <= mpmath.sin(angle) <= sin_hi[k] + slack
        assert cos_hi[k] - cos_lo[k] <= 4e-16
        assert sin_hi[k] - sin_lo[k] <= 4e-16


def test_the_extended_angle_lies_just_above_two_pi() -> None:
    mpmath.mp.prec = 200
    extended = labels.constants().two_pi_hi_float
    assert labels.TWO_PI_FLOAT < 2 * mpmath.pi < extended
    assert extended == math.nextafter(labels.TWO_PI_FLOAT, math.inf)


def _cells(*indices: int) -> labels.IntArray:
    return np.array(indices, dtype=np.int64)


def test_the_point_count_is_exact() -> None:
    level = 10
    g = labels.constants().separation
    # A run of k cells holds 1 + floor(k cells / g) points.
    for length in (1, 50, 117, 118, 236, 237, 600):
        expected = 1 + (length * (labels.TURN >> level)) // g
        assert labels.circular_count(np.arange(length, dtype=np.int64), level) == expected
    assert labels.circular_count(_cells(), level) == 0
    assert labels.circular_count(np.arange(1 << level, dtype=np.int64), level) == 8
    # Two cells half a turn apart give two points; a run across zero is one run.
    assert labels.circular_count(_cells(0, 512), level) == 2
    wrapped = np.concatenate([np.arange(0, 60), np.arange(1024 - 60, 1024)]).astype(np.int64)
    assert labels.circular_count(wrapped, level) == labels.circular_count(
        np.arange(120, dtype=np.int64), level
    )


def test_a_halved_separation_counts_more_points() -> None:
    run = np.arange(300, dtype=np.int64)
    g = labels.constants().separation
    assert labels.circular_count(run, 10, g // 2) > labels.circular_count(run, 10)


@pytest.mark.parametrize(("low", "high"), [(0.1, 0.4), (-0.2, 0.3), (2.9, 3.4), (4.6, 4.8)])
def test_the_arc_bounds_enclose_cos_and_sin(low: float, high: float) -> None:
    ends = [labels.angle_trig(low), labels.angle_trig(high)]
    c_lo, c_hi, s_lo, s_hi = labels.arc_range(
        ends[0][0:2], ends[0][2:4], ends[1][0:2], ends[1][2:4]
    )
    angles = np.linspace(low, high, 2001)
    assert c_lo <= np.cos(angles).min() + 1e-15
    assert c_hi >= np.cos(angles).max() - 1e-15
    assert s_lo <= np.sin(angles).min() + 1e-15
    assert s_hi >= np.sin(angles).max() - 1e-15
    # The sampled extremes miss an interior extremum by at most (step/2)^2/2 < 1e-8.
    assert c_hi - c_lo <= np.cos(angles).max() - np.cos(angles).min() + 1e-7
    assert s_hi - s_lo <= np.sin(angles).max() - np.sin(angles).min() + 1e-7


def test_the_n1_boxes_are_certified_as_labelled() -> None:
    for name in ("bnb_n1_T9_0of1", "bnbw_n1_T9_0of1"):
        for record in labels.read_list(name):
            row = labels.decide(record)
            assert row["outcome"] == "certified-as-labelled"
            assert row["bound"] <= labels.THRESHOLD


def test_the_sharp_box_is_certified_at_9_and_refused_at_8() -> None:
    record = labels.read_list("bnb_n2_T9_0of1")[23]
    box = labels.Box.from_record(record)
    accepted = labels.certify(box, labels.ALLOWED["closed"])
    assert accepted.certified
    assert accepted.pieces == 1
    assert accepted.max_bound == 9
    refused = labels.certify(box, labels.ALLOWED["closed"], threshold=8, budget=64)
    assert not refused.certified
    assert refused.reason == "budget of 64 pieces spent"


def test_the_bound_at_the_slit_configuration_is_nine_at_every_level() -> None:
    a = 0.5 + 1e-9
    record = {"kind": "closed", "box": [[a, a, 0.0, 0.0], [a, a, math.pi, math.pi]]}
    q = labels.Quantities.of(labels.Box.from_record(record))
    assert {bound for _, bound in labels.bounds_by_level(q)} == {9}


def test_whole_circle_intervals_are_bounded_trivially() -> None:
    record = labels.read_list("bnbw_n4_T9_1of2")[31]
    assert record["box"][1][3] - record["box"][1][2] > labels.ARC_LIMIT
    assert labels.decide(record)["outcome"] == "certified-as-labelled"


def test_the_witness_checker_counts_the_slit_configuration() -> None:
    bounds = labels.exact_bounds()
    slit, outer = labels.slit_configuration(half_separation=False)
    found = labels.witness_lower_bound(slit, None, outer, bounds.cos_gamma0_lo**2)
    assert found["admissible"]
    assert found["U_at_least"] == 9
    shifted = [(slit[0][0] - Fraction(1, 10**6), slit[0][1]), slit[1]]
    assert not labels.witness_lower_bound(shifted, None, outer, bounds.cos_gamma0_lo**2)[
        "admissible"
    ]


#: Review A's mutants of the four thresholds G to J sit on: each moves one threshold the
#: permissive way, and its control must then be certified, where the module refuses it.
_THRESHOLD_MUTANTS = {
    "G": ("if self.dist_sq_lo[i, j] < lam_sq_hi", "if self.dist_sq_lo[i, j] < lam_sq_hi - 0.3"),
    "H": (
        "close = dn(self.cy[0] + self.box.h[0]) <= wall_hi",
        "close = dn(self.cy[0] + self.box.h[0]) <= wall_hi - 0.1",
    ),
    "I": (
        "            reach = up(self.cy[1][i] + box.h[1])\n",
        "            reach = up(self.cy[1][i] + box.h[1]) - 0.2\n",
    ),
    "J": (
        "coeff_c = up(up(box.r_hi[i] * box.r_hi[i]) - const.rho1_sq_lo)",
        "coeff_c = up(up(box.r_hi[i] * box.r_hi[i]) - const.rho1_sq_lo - 0.05)",
    ),
}


def _mutant(old: str, new: str) -> Any:
    """The module with one source edit, loaded under a name of its own."""
    path = Path(labels.__file__)
    source = path.read_text(encoding="utf-8")
    assert source.count(old) == 1
    name = "ryu_k2_minus_c_labels_mutant"
    module = types.ModuleType(name)
    module.__file__ = str(path)
    sys.modules[name] = module
    try:
        exec(compile(source.replace(old, new), str(path), "exec"), module.__dict__)
    finally:
        del sys.modules[name]
    return module


@pytest.mark.parametrize("letter", "GHIJ")
def test_each_threshold_control_catches_a_labeller_that_moves_it(letter: str) -> None:
    for module, refused in ((labels, True), (_mutant(*_THRESHOLD_MUTANTS[letter]), False)):
        control = next(c for c in module.control_specs() if c.name.startswith(letter))
        case = module.run_control(control)
        assert case["perturbed refused"] is refused
        assert case["unperturbed certified"]
        assert case["witness_refutes"]


def test_a_focused_refusal_ends_at_the_witness_not_the_budget() -> None:
    control = next(c for c in labels.control_specs() if c.name.startswith("A"))
    case = labels.run_control(control)
    assert case["perturbed"]["reason"] == "a piece too small to cut stays undecided"
    assert case["perturbed"]["pieces"] < 400


def test_the_guards_refuse_what_the_arithmetic_does_not_cover() -> None:
    record = {"kind": "inf", "box": [[0.5, 1.0, 0.0, 0.0]]}
    with pytest.raises(ValueError, match="radius reaches 1"):
        labels.Box.from_record(record)
    special = (0, 0, -456, -2)
    with pytest.raises(ArithmeticError, match="special value"):
        labels._fraction(special)  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    assert labels._fraction((0, 0, 0, 0)) == 0  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    assert 0 < labels.constants().separation <= labels.TURN // 2
    labels._check_float_environment()  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    q = labels.Quantities.of(labels.Box.from_record(labels.read_list("bnb_n1_T9_0of1")[0]))
    with pytest.raises(ValueError, match="level 2 or finer"):
        q.kept_cells(0, 1, np.arange(2, dtype=np.int64))


def _beyond_rho1() -> Fraction:
    """A rational y with rho1^2 < 1/4 + y^2, inside the 200-bit upper bound of rho1^2."""
    upper = labels.exact_bounds().rho1_sq_hi
    with mpmath.workprec(600):  # restores the precision the other tests run at
        d = mpmath.mpf(1) / 10000
        rho1_sq = (d + mpmath.sqrt(2) / 2) ** 2 + mpmath.mpf(1) / 4
        half = (mpmath.mpf(upper.numerator) / upper.denominator + rho1_sq) / 2
        y = Fraction(int(mpmath.floor(mpmath.sqrt(half - mpmath.mpf(1) / 4) * 2**500)), 2**500)
        value = Fraction(1, 4) + y * y
        assert mpmath.mpf(value.numerator) / value.denominator > rho1_sq
    assert value < upper
    return y


def test_a_centre_beyond_rho1_is_outside_the_domain() -> None:
    """|c|^2 must be at most rho1^2: compared with the bound's lower end, not its upper."""
    bounds = labels.exact_bounds()
    beyond = [(Fraction(1, 2), _beyond_rho1())]
    assert not labels.witness_lower_bound(beyond, None, [[]], bounds.cos_gamma0_lo**2)[
        "in_domain"
    ]
    inside = [(Fraction(1, 2), Fraction(1, 2))]
    assert labels.witness_lower_bound(inside, None, [[]], bounds.cos_gamma0_lo**2)["in_domain"]


def test_a_witness_refutes_only_from_inside_its_box() -> None:
    witness = {"admissible": True, "in_domain": True, "U_at_least": 9, "W_I_at_least": 1}
    assert labels.witness_refutes(witness, inside=True, threshold=8)
    assert not labels.witness_refutes(witness, inside=False, threshold=8)
    assert not labels.witness_refutes(witness, inside=True, threshold=9)
    assert labels.witness_refutes(witness, inside=True, side_edge=True)
    assert not labels.witness_refutes(witness | {"in_domain": False}, inside=True, threshold=8)
    assert not labels.witness_refutes(witness | {"admissible": False}, inside=True)


_D = 1e-4
_LAM = _D + math.sqrt(2)
_RHO1_SQ = (_D + math.sqrt(2) / 2) ** 2 + 0.25
_WALL = _D + math.sqrt(2) / 2
_GAMMA0 = math.acos(1 - 1 / (2 * _LAM**2))
#: The sampler's margins: a direction counts only if every condition holds with this
#: slack and the count's points are this much further than gamma0 apart, so that float
#: sampling can only undercount U(I), never overcount it.
_SLACK = 1e-9
_DIRECTIONS = 3600


def _sampled_count(angles: labels.FloatArray) -> int:
    """The greedy count from the start of each run of sampled admissible angles."""
    if len(angles) == 0:
        return 0
    gap = _GAMMA0 + _SLACK
    steps = np.diff(np.concatenate([angles, [angles[0] + 2 * math.pi]])).astype(np.float64)
    before: labels.FloatArray = np.roll(steps, 1)
    starts = angles[before > 2 * math.pi / _DIRECTIONS + 1e-12]
    best = 1
    for start in starts if len(starts) else angles[:1]:
        ring = np.sort(np.mod(angles - start, 2 * math.pi))
        count, point = 1, 0.0
        for angle in ring:
            if angle - point >= gap and 2 * math.pi - angle >= gap:
                count, point = count + 1, angle
        best = max(best, count)
    return best


def _sampled_u(r: list[float], theta: list[float], h: float | None) -> int | None:
    """A float lower estimate of U(I) at one configuration, or None if inadmissible."""
    c = [(ri * math.cos(t), ri * math.sin(t)) for ri, t in zip(r, theta, strict=True)]
    n = len(c)
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    if any(math.dist(c[i], c[j]) < 1 for i, j in pairs):
        return None
    if h is not None and any(y + h < 0.5 for _, y in c):
        return None
    total = sum(1 for i, j in pairs if math.dist(c[i], c[j]) < _LAM - _SLACK)
    if h is not None:
        total += sum(1 for x, y in c if abs(x) <= 0.5 and y >= 0 and y + h < _WALL - _SLACK)
    phis = np.arange(_DIRECTIONS) * (2 * math.pi / _DIRECTIONS)
    ux, uy = np.cos(phis), np.sin(phis)
    for i, (cx, cy) in enumerate(c):
        rectangle = (cx * ux + cy * uy <= -_SLACK) & (np.abs(cx * uy - cy * ux) <= 0.5 - _SLACK)
        good = np.zeros(len(phis), dtype=bool)
        for t in np.linspace(1 + _SLACK, _LAM - _SLACK, 48):
            x, y = cx + t * ux, cy + t * uy
            ok = rectangle & (x * x + y * y > _RHO1_SQ + _SLACK)
            for j, (ox, oy) in enumerate(c):
                if j != i:
                    ok &= (x - ox) ** 2 + (y - oy) ** 2 >= 1 + _SLACK
            if h is not None:
                ok &= y >= 0.5 - h + _SLACK
            good |= ok
        total += _sampled_count(phis[good].astype(np.float64))
    return total


def test_sampled_overlap_never_exceeds_the_rigorous_point_bound() -> None:
    """At random admissible points of closed boxes, U(I) estimated by sampling 3,600
    directions is at most the labeller's finest bound on the point box, which is at
    most 9: a diagnostic of soundness, independent of the labeller's arithmetic."""
    rng = random.Random(20261102)
    closed = [
        record
        for name in ("bnb_n2_T9_0of1", "bnb_n3_T9_0of1", "bnbw_n2_T9_0of1")
        for record in labels.read_list(name)
        if record["kind"] == "closed"
    ]
    checked = tight = 0
    for record in rng.sample(closed, 60):
        for _ in range(20):
            r = [rng.uniform(lo, hi) for lo, hi, _, _ in record["box"]]
            theta = [rng.uniform(lo, hi) for _, _, lo, hi in record["box"]]
            h = rng.uniform(*record["h"]) if "h" in record else None
            sampled = _sampled_u(r, theta, h)
            if sampled is None:
                continue
            rows = [[a, a, t, t] for a, t in zip(r, theta, strict=True)]
            point: dict[str, Any] = {"kind": "closed", "box": rows}
            if h is not None:
                point["h"] = [h, h]
            q = labels.Quantities.of(labels.Box.from_record(point))
            bound = labels.bounds_by_level(q)[-1][1]
            assert sampled <= bound <= labels.THRESHOLD
            checked += 1
            tight += sampled == bound
    assert checked >= 40
    assert tight >= checked // 4


def _receipt(name: str) -> Any:
    return json.loads(read_retained_text(RECEIPTS / name))


def _exit_and_cpu(path: Path) -> tuple[int, float]:
    match = _FOOTER.match(path.read_text(encoding="utf-8").splitlines()[-1])
    assert match, path
    return int(match["exit"]), float(match["cpu"])


def test_the_price_was_taken_before_the_run() -> None:
    price = _receipt("price-500.json")
    assert price["sample"] == 500
    assert price["extrapolated_cpu_hours"] < 40
    assert _exit_and_cpu(RECEIPTS / "price-500.log")[0] == 0
    rows = read_retained_text(RECEIPTS / "price-500-rows.jsonl").splitlines()
    assert len(rows) == 500


def test_both_workers_finished_within_the_cap() -> None:
    total = 0.0
    for worker in (0, 1):
        status, cpu = _exit_and_cpu(RECEIPTS / f"run-worker{worker}.log")
        assert status == 0
        total += cpu
    assert total < 40 * 3600


def test_every_box_was_decided_once_and_certified_as_labelled() -> None:
    summary = _receipt("summary.json")
    assert summary["boxes"] == BOXES
    assert summary["missing"] == []
    assert summary["all_certified"]
    assert summary["all_as_labelled"]
    assert summary["exceptions"] == []
    assert summary["largest_closed_bound"] == labels.THRESHOLD
    for label, size in CLASS_SIZES.items():
        assert summary["classes"][label]["certified-as-labelled"] == size


def test_the_label_rows_match_the_retained_lists() -> None:
    seen = 0
    most = (0, "", 0)
    for name in labels.LISTS:
        records = labels.read_list(name)
        rows = [
            json.loads(line)
            for line in read_retained_text(RECEIPTS / "labels" / f"{name}.jsonl").splitlines()
        ]
        assert [row["line"] for row in rows] == list(range(1, len(records) + 1))
        for row, record in zip(rows, records, strict=True):
            assert row["label"] == record["kind"]
            assert row["U"] == record.get("U")
            assert row["outcome"] == "certified-as-labelled"
            assert set(row["leaves"]) <= {"inf", record["kind"]}
            # A closed box decided wholly by inadmissible pieces has no bound.
            if "closed" in row["leaves"]:
                assert row["bound"] <= labels.THRESHOLD
            else:
                assert row["bound"] is None
            most = max(most, (row["pieces"], name, row["line"]))
        seen += len(rows)
    assert seen == BOXES
    # The packet README: no box came near the budget of MAX_PIECES; the most was 491.
    assert most == (491, "bnb_n4_T9_1of2", 2304)
    assert most[0] < labels.MAX_PIECES


def test_the_ten_controls_are_refused_by_decision_and_refuted() -> None:
    report = _receipt("controls.json")
    assert report["budget"] == labels.MAX_PIECES
    assert report["passed"]
    assert [control["control"][0] for control in report["controls"]] == list("ABCDEFGHIJ")
    for control in report["controls"]:
        assert control["perturbed refused"]
        assert control["perturbed"]["reason"] == "a piece too small to cut stays undecided"
        assert control["unperturbed certified"]
        assert control["witness_refutes"]
        assert control["witness"]["in_box"]
        assert control["witness"]["in_domain"]
    assert _exit_and_cpu(RECEIPTS / "controls.log")[0] == 0


def test_a_sample_re_decides_identically_after_review_a() -> None:
    report = _receipt("recheck-1000.json")
    assert report["sample"] == 1000
    assert sum(report["by_label"].values()) == 1000
    assert {key.split(",")[0] for key in report["by_label"]} == {"inf", "nowall", "closed"}
    assert report["identical"] == 1000
    assert report["differences"] == []
    assert _exit_and_cpu(RECEIPTS / "recheck-1000.log")[0] == 0
