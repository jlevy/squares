"""Controls for the certificate-reach renderer's measured-attainment arithmetic.

Three retained certificates -- n = 11, n = 17 and n = 19 -- have each landed within a
narrow band of the same fraction of their case's best known packing. The renderer
derives that band from the live corpus rather than carrying the numbers as constants,
so the control that matters is a round trip: recompute the ratios from
`frontier/n-*.md` and the retained `certificate.json` files, and check the band and
the arithmetic built on it, rather than pinning values by hand.
"""

from __future__ import annotations

from devtools.render_certificate_reach import (
    OUT,
    cases,
    mean_packing_ratio,
    measured_attainment,
    predicted_reach,
    render,
    retained_certificates,
)

BAND = 0.005


def test_committed_file_matches_the_renderer() -> None:
    """The checked-in CERTIFICATE-REACH.md is never hand-edited; a drift is a bug."""
    assert OUT.read_text() == render(cases())


def test_retained_certificates_are_found_by_globbing_the_case_packages() -> None:
    """Four packages exist today; the n = 20 package keys to n = 19, not n = 20."""
    retained = retained_certificates()
    assert {row["package"] for row in retained} == {
        "n11_fractional_certificate",
        "n12_fractional_certificate",
        "n17_fractional_certificate",
        "n20_fractional_certificate",
    }
    keyed_n = {row["package"]: row["n"] for row in retained}
    assert keyed_n["n20_fractional_certificate"] == 19


def test_three_packing_limited_ratios_sit_inside_a_tight_band() -> None:
    """n = 11, 17 and 19 are the packing-limited rows; their ratios are within 0.005."""
    measured = measured_attainment(cases())
    packing_limited = {row["n"]: row for row in measured if row["binds"] == "packing"}
    assert set(packing_limited) == {11, 17, 19}
    ratios = [row["ratio"] for row in packing_limited.values()]
    assert max(ratios) - min(ratios) <= BAND
    # Each ratio is close to the ~0.982 the record has settled on -- checked loosely,
    # since the tight assertion above is what actually pins the regularity.
    assert all(0.97 < ratio < 0.99 for ratio in ratios)


def test_ceiling_limited_certificate_is_excluded_from_the_mean() -> None:
    """n = 12's ceiling sits below its best packing, so its ratio measures the ceiling."""
    measured = measured_attainment(cases())
    n12 = next(row for row in measured if row["n"] == 12)
    assert n12["binds"] == "ceiling"

    mean_with_n12 = mean_packing_ratio([*measured, {**n12, "binds": "packing"}])
    mean_without = mean_packing_ratio(measured)
    assert mean_with_n12 != mean_without


def test_predicted_never_exceeds_the_ceiling() -> None:
    """`predicted` is `min(ratio * best_packing, ceiling)`; it cannot cross the cap."""
    rows = cases()
    measured = measured_attainment(rows)
    ratio = mean_packing_ratio(measured)
    live = [row for row in rows if row["verdict"] != "foreclosed"]
    for row in predicted_reach(live, ratio):
        assert row["predicted"] <= row["ceiling"] + 1e-12
        assert row["predicted_gain"] >= 0.0


def test_predicted_gain_is_clamped_at_zero() -> None:
    """A row whose prediction sits at or below its lower bound gets no negative gain."""
    rows = cases()
    measured = measured_attainment(rows)
    ratio = mean_packing_ratio(measured)
    live = [row for row in rows if row["verdict"] != "foreclosed"]
    predicted = predicted_reach(live, ratio)
    assert predicted, "no live rows carried a best packing; the corpus changed shape"
    for row in predicted:
        assert row["predicted_gain"] == max(row["predicted"] - row["lower"], 0.0)
