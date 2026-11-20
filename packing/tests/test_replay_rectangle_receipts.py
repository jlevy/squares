"""The rectangle-receipt replay's own arithmetic: mutants, headers and summaries."""

from __future__ import annotations

from fractions import Fraction

from devtools import replay_rectangle_receipts as replay


def test_mutants_scale_density_and_mass_only_rounding_down() -> None:
    rows = [(1, 2, 3, 4, 5, 6, 7, 8, 101, 1001)]
    assert replay.scaled(rows, Fraction(99, 100)) == [(1, 2, 3, 4, 5, 6, 7, 8, 99, 990)]
    assert replay.scaled(rows, Fraction(1, 4)) == [(1, 2, 3, 4, 5, 6, 7, 8, 25, 250)]


def test_the_set_header_is_the_square_kernels_with_the_core_domain_switch() -> None:
    measure = {"proof_net": {"step": "83/40000"}, "L": "1931/400", "B": "9977/10000"}
    g = 2**30
    header = replay.set_header(measure, 1, None)
    t = Fraction(83, 40000)
    c, s, e = (
        t.denominator**2 - t.numerator**2,
        2 * t.numerator * t.denominator,
        t.denominator**2 + t.numerator**2,
    )
    assert header[:3] == [c, s, e]
    left = t - t / 2
    v = (1 + 2 * left - left**2) / (2 * (1 + left**2))
    assert header[7] == (g * (Fraction(1931, 400) - v)).__ceil__()
    contained = replay.set_header(measure, 1, "contained_core")
    core_v = Fraction(9977, 10000) * Fraction(c + s, 2 * e)
    assert contained[7] == (g * (Fraction(1931, 400) - core_v)).__ceil__()
    assert contained[:7] == header[:7]


def test_a_refusal_counts_on_coverage_only_with_an_unresolved_box() -> None:
    base = {
        "folder": "f",
        "mutant": "99/100",
        "n": 7,
        "side": "3",
        "kernel": "square",
        "verified": False,
        "matches_archive": False,
        "nodes": 5,
        "cpu_seconds_approx": 0.1,
    }
    rows = [
        {**base, "verdict": "UNDECIDED", "unresolved": "unresolved 1 2 bound 3"},
        {**base, "verdict": "UNDECIDED", "unresolved": None},
        {**base, "verdict": "PASS", "unresolved": None},
    ]
    summary = replay.summarize(rows)["f|99/100"]
    assert (summary["directions"], summary["refused_on_coverage"], summary["nodes"]) == (
        3,
        1,
        15,
    )
