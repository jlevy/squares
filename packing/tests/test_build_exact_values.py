"""The exact side values register refuses what it exists to catch.

`devtools.build_exact_values` checks every minimal polynomial the frontier records:
irreducible over Q, one real root at the side, that root agreeing with the record, and
the polynomial agreeing with its source. A check that has never refused anything is a
check nobody has seen work, so each one here runs on a real case it passes and on a
negative control it must refuse: a reducible polynomial, a root that misses the recorded
side, a perturbed coefficient in a derived record, and a superseded catalogue polynomial
offered as the side.
"""

from __future__ import annotations

import copy
import gzip
import io
import json
from collections.abc import Callable
from fractions import Fraction
from functools import cache
from pathlib import Path
from typing import Any

import pytest
import sympy as sp
from jsonschema_rs import Draft202012Validator

from devtools import build_exact_values as exact
from devtools import refinement_custody, refinement_packets
from devtools.retained_data import compressed_path, read_retained_text, write_retained_text
from sqpack.exact_values import algebraic_fields, format_polynomial
from sqpack.kingbird_catalogue import normalized_polynomial
from sqpack.yamlio import load_yaml

#: 2 + sqrt(2)/2, the side at n = 5, and Daniel's 39-digit value for it.
N5 = (2, -8, 7)
N5_KKT = {"value": "2.70710678118654752440084436210484903928", "status": "KKT local min"}


@cache
def _register() -> dict[str, Any]:
    return json.loads(read_retained_text(exact.RECORD))


def _entries() -> dict[int, dict[str, Any]]:
    return {entry["n"]: entry for entry in _register()["register"]["entries"]}


def _build(n: int, packing: dict[str, Any] | None = None, budget: int = 200) -> dict:
    return exact.build_entry(
        n,
        exact.load_packing(n) if packing is None else packing,
        exact.catalogue_entries().get(n),
        exact.kkt_rows().get(n),
        budget,
    )


def _historical_refinement_packing(n: int) -> dict[str, Any]:
    """Exercise earlier bound custody from the retained pre-refinement source record."""
    source = next(
        source for source in refinement_packets.SOURCES.values() if n in source.numbers
    )
    prior = json.loads((source.packet / "acquisition/prior-state.json").read_text())
    previous = next(row for row in prior if row["n"] == n)
    packing = copy.deepcopy(exact.load_packing(n))
    packing["reported_upper_bound"] = previous["reported"]
    packing["verified_upper_bound"] = previous["verified"]
    return packing


def _refused(call: Callable[[], object], fragment: str) -> None:
    with pytest.raises(exact.ExactValuesError, match=fragment):
        call()


# --- irreducibility ---------------------------------------------------------------------


def test_an_irreducible_quadratic_is_certified_by_factorisation() -> None:
    assert exact.irreducibility(N5) == {"method": "factorization", "primes": []}


def test_a_reducible_polynomial_is_refused() -> None:
    # s^2 - 4 = (s - 2)(s + 2): the control for the factorisation route.
    _refused(lambda: exact.irreducibility((1, 0, -4)), "reducible over Q")


def test_a_reducible_polynomial_above_degree_twelve_has_no_certificate() -> None:
    """The modular route's control: a product always has a factor of degree 7 mod p."""
    side = sp.Symbol("s")
    product = sp.Poly((side**7 - side - 1) * (side**7 + 2 * side + 3), side)
    coefficients = tuple(int(c) for c in product.all_coeffs())
    assert len(coefficients) - 1 == 14
    _refused(lambda: exact.irreducibility(coefficients, budget=30), "no irreducibility")


def test_the_degree_eighteen_certificate_needs_both_of_its_primes() -> None:
    coefficients = normalized_polynomial(
        exact.load_packing(17)["reported_upper_bound"]["minimal_polynomial"]
    )
    certificate = exact.irreducibility(coefficients)
    assert certificate == {"method": "modular-degree-patterns", "primes": [3, 7]}
    assert exact.verify_modular_certificate(coefficients, [3, 7])
    # One prime alone leaves a proper factor degree possible, so it certifies nothing.
    assert not exact.verify_modular_certificate(coefficients, [3])


@pytest.mark.parametrize("n", [17, 41, 69, 88])
def test_the_fast_factorisation_agrees_with_sympy(n: int) -> None:
    polynomial_text = (
        exact.catalogue_entries()[n].minimal_polynomial
        if n == 88
        else exact.load_packing(n)["reported_upper_bound"]["minimal_polynomial"]
    )
    assert polynomial_text is not None
    coefficients = normalized_polynomial(polynomial_text)
    for prime in exact.first_primes(12):
        fast = exact.factor_degrees_mod(coefficients, prime)
        reference = exact.reference_factor_degrees_mod(coefficients, prime)
        assert (fast is None and reference is None) or sorted(fast or []) == sorted(
            reference or []
        ), (n, prime)


# --- the root ---------------------------------------------------------------------------


def test_the_root_is_isolated_in_the_kkt_window() -> None:
    checks, root = exact.polynomial_checks(5, N5, "2.70710678118654", N5_KKT)
    assert checks["root"]["window"] == "kkt"
    assert checks["root"]["contains_recorded_side"]
    assert checks["kkt_agreement_digits"] == 39
    assert checks["recorded_agreement_digits"] == 15
    assert checks["decimal"] == "2.707106781186547524400844362104849039285"
    side = Fraction(str(sp.N(2 + sp.sqrt(2) / 2, 60)))
    assert root.lo < side < root.hi
    assert exact.unique_root_in(N5, root.lo, root.hi)


def test_a_wrong_kkt_value_falls_back_to_the_record_window() -> None:
    wrong = {"value": "2.70710678118654752440084436000000000000", "status": "KKT local min"}
    checks, _ = exact.polynomial_checks(5, N5, "2.70710678118654", wrong)
    assert checks["root"]["window"] == "record"
    assert checks["kkt_agreement_digits"] == 27


@pytest.mark.parametrize("printed", ["2.70710678118654", "2.70710678118655"])
def test_the_record_may_truncate_or_round(printed: str) -> None:
    checks, _ = exact.polynomial_checks(5, N5, printed, None)
    assert checks["root"]["contains_recorded_side"]


def test_a_root_that_misses_the_recorded_side_is_refused() -> None:
    _refused(
        lambda: exact.polynomial_checks(5, N5, "2.70710678118656", None),
        "wrong polynomial",
    )
    # n = 28's polynomial offered for n = 39's side has no root anywhere near it.
    sextic = (1, -24, 212, -812, 1025, 882, -1615)
    _refused(lambda: exact.polynomial_checks(39, sextic, "6.81072208306864", None), "no sign")


def _product(*roots: Fraction) -> tuple[int, ...]:
    side = sp.Symbol("s")
    expression = sp.Integer(1)
    for root in roots:
        expression *= root.denominator * side - root.numerator
    return tuple(int(c) for c in sp.Poly(sp.expand(expression), side).all_coeffs())


def test_two_roots_in_one_window_are_not_one_root() -> None:
    lo, hi = Fraction(29, 10), Fraction(31, 10)
    # Roots at 3.01 and 3.03, off every bisection point: bisection separates them.
    apart = _product(Fraction(301, 100), Fraction(303, 100))
    assert not exact.unique_root_in(apart, lo, hi)
    assert exact.unique_root_in(apart, lo, Fraction(302, 100))
    # Roots 10^-20 apart: forty halvings cannot separate them, and it says so.
    close = _product(Fraction(301, 100), Fraction(301, 100) + Fraction(1, 10**20))
    _refused(lambda: exact.unique_root_in(close, lo, hi), "could not separate")


def test_a_rational_root_is_exact() -> None:
    checks, root = exact.polynomial_checks(230, (41, -643), "15.68292682926829", None)
    assert root.exact == Fraction(643, 41)
    assert checks["root"]["interval"] == ["643/41", "643/41"]
    assert checks["decimal"] == "15.68292682926829268292682926829268292683"


# --- the source -------------------------------------------------------------------------


def test_a_recorded_degree_one_gets_its_missing_polynomial_from_the_fraction() -> None:
    fields = algebraic_fields("6/4", 1, None)
    assert fields == {
        "algebraic_degree": 1,
        "minimal_polynomial": "2s - 3 = 0",
        "algebraic_source": "derived-from-exact-form",
    }
    assert algebraic_fields("6/4", 1, "2s - 3 = 0")["algebraic_source"] == "catalogue"
    assert algebraic_fields(None, 672, None)["minimal_polynomial"] is None
    with pytest.raises(ValueError, match="degree 1 disagrees"):
        algebraic_fields("sqrt(2)", 1, None)


SQUISH_RATIONAL_COUNTS = (
    88,
    108,
    123,
    126,
    129,
    130,
    153,
    154,
    155,
    179,
    180,
    199,
    207,
    208,
    209,
    236,
    237,
    238,
    239,
    258,
    263,
    302,
    303,
)


def _rational_packing(n: int) -> dict[str, Any]:
    packing = copy.deepcopy(exact.load_packing(n))
    reported = packing["reported_upper_bound"]
    reported.update(algebraic_fields(reported["exact_form"], 1, None))
    return packing


def test_certified_squish_rationals_keep_the_exact_side_and_its_upward_display() -> None:
    above_half_unit = 0
    for n in SQUISH_RATIONAL_COUNTS:
        packing = _rational_packing(n)
        entry = _build(n, packing)
        rational = Fraction(entry["exact_form"])
        printed = Fraction(entry["side"]["value"])
        unit = Fraction(1, 10 ** len(entry["side"]["value"].split(".")[1]))
        assert rational <= printed < rational + unit, n
        above_half_unit += printed - rational > unit / 2
        assert entry["state"] == "rational", n
        assert entry["side"]["relation"] == "upper-bound", n
        assert entry["checks"]["root"]["interval"] == [str(rational), str(rational)], n
        assert entry["checks"]["irreducible"]["method"] == "linear", n
        assert entry["checks"]["catalogue"] == "derived-here", n
    assert above_half_unit == 10


def test_upward_ceiling_rejects_downward_and_whole_unit_displays() -> None:
    for value in ("1.34", "1.3334", "1.3333334"):
        checks, _ = exact.polynomial_checks(1, (3, -4), value, None, upward_ceiling=True)
        assert checks["root"]["contains_recorded_side"]
    for value in ("1.33", "1.35", "1.32", "1.3332"):
        _refused(
            lambda value=value: exact.polynomial_checks(
                1, (3, -4), value, None, upward_ceiling=True
            ),
            "wrong polynomial",
        )
    _refused(lambda: exact.polynomial_checks(1, (3, -4), "1.34", None), "wrong polynomial")
    _refused(
        lambda: exact.polynomial_checks(1, (1, -1), "1.01", None, upward_ceiling=True),
        "wrong polynomial",
    )


def test_a_ceiling_needs_the_matching_rational_certificate() -> None:
    n = 130  # Its certified ceiling exceeds the nearest-rounding window.
    for control in ("source", "exact_form", "evidence", "value", "proved"):
        packing = _rational_packing(n)
        if control == "source":
            packing["reported_upper_bound"]["source_key"] = "[Kingbird]"
        elif control == "proved":
            packing["status"] = "proved"
        else:
            packing["verified_upper_bound"][control] = [] if control == "evidence" else "0"
        _refused(lambda packing=packing: _build(n, packing), "wrong polynomial")


def test_a_verified_native_rational_side_is_an_identity_with_an_ideal_route() -> None:
    packing = _historical_refinement_packing(68)
    before = copy.deepcopy(packing)
    entry = _build(68, packing)
    side = Fraction(packing["verified_upper_bound"]["exact_form"])
    assert entry["state"] == "rational"
    assert entry["polynomial"]["coefficients"] == [str(side.denominator), str(-side.numerator)]
    assert entry["checks"]["root"]["interval"] == [str(side), str(side)]
    assert entry["checks"]["irreducible"]["method"] == "linear"
    assert entry["side"]["relation"] == "upper-bound"
    assert entry["status"] == before["status"]
    assert entry["kkt"]["value"] == exact.kkt_rows()[68]["S_exact"]
    assert any(note["kind"] == "verified-witness-side" for note in entry["notes"])
    assert any("ideal contact" in note["text"] for note in entry["notes"])
    assert packing == before


def test_a_couzo_rational_ceiling_is_distinguished_from_the_native_side() -> None:
    entry = _build(292, _historical_refinement_packing(292))
    assert entry["state"] == "rational"
    assert Fraction(entry["exact_form"]) == Fraction(entry["side"]["value"])
    (note,) = [note for note in entry["notes"] if note["kind"] == "verified-bound-ceiling"]
    assert "outward ceiling" in note["text"]
    assert "native witness side" in note["text"]
    assert any("ideal contact" in note["text"] for note in entry["notes"])


def test_verified_rational_fallback_requires_exact_equality_and_missing_identity() -> None:
    for control in (
        "fraction",
        "reported",
        "verified",
        "source",
        "count",
        "replay",
        "proved",
        "origin",
    ):
        packing = _historical_refinement_packing(68)
        if control == "fraction":
            packing["verified_upper_bound"]["exact_form"] = "1/2"
        elif control == "reported":
            packing["reported_upper_bound"]["value"] += "1"
        elif control == "verified":
            packing["verified_upper_bound"]["value"] += "1"
        elif control == "source":
            packing["reported_upper_bound"]["source_key"] = "[Kingbird]"
        elif control == "count":
            packing["n"] = 69
        elif control == "replay":
            packing["verified_upper_bound"]["evidence"] = []
        elif control == "proved":
            packing["status"] = "proved"
        else:
            packing["reported_upper_bound"]["algebraic_source"] = "contact-system"
        assert _build(68, packing)["state"] == "numeric-only", control
    for n in (29, 55, 71):
        assert _build(n)["state"] == "numeric-only", n
    assert _build(105, _historical_refinement_packing(105))["state"] == "numeric-only"
    existing = copy.deepcopy(exact.load_packing(5))
    existing["verified_upper_bound"]["exact_form"] = "1/2"
    assert _build(5, existing) == _build(5)
    degree_only = _historical_refinement_packing(68)
    degree_only["reported_upper_bound"]["algebraic_degree"] = 3
    assert _build(68, degree_only)["state"] == "degree-only"


ORIGINAL_VERIFIED_FALLBACK_COUNTS = (
    68,
    102,
    103,
    106,
    110,
    131,
    132,
    152,
    156,
    172,
    177,
    181,
    182,
    206,
    210,
    211,
    228,
    240,
    241,
    259,
    268,
    269,
    270,
    271,
    272,
    273,
    292,
    297,
    301,
    304,
    305,
    306,
    307,
)


VERIFIED_FALLBACK_COUNTS = tuple(
    n for n in ORIGINAL_VERIFIED_FALLBACK_COUNTS if n not in (68, 292)
)


def test_all_verified_rationals_keep_ideal_routes_and_share_one_packet_scan(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    assert len(ORIGINAL_VERIFIED_FALLBACK_COUNTS) == 33
    assert len(VERIFIED_FALLBACK_COUNTS) == 31
    scans = []
    scan = exact.evand.receipt_problems

    def counted_scan() -> list[str]:
        scans.append(True)
        return scan()

    monkeypatch.setattr(exact.evand, "receipt_problems", counted_scan)
    inputs = exact.VerifiedRationalInputs()
    for n in VERIFIED_FALLBACK_COUNTS:
        packing = exact.load_packing(n)
        entry = exact.build_entry(
            n,
            packing,
            exact.catalogue_entries().get(n),
            exact.kkt_rows().get(n),
            verified_inputs=inputs,
        )
        assert entry["state"] == "rational", n
        assert entry["exact_form"] == packing["verified_upper_bound"]["exact_form"], n
        assert entry["status"] == packing["status"] == "open", n
        assert entry["side"]["value"] == packing["reported_upper_bound"]["value"], n
        assert entry["lower"]["value"] == packing["verified_lower_bound"]["value"], n
        assert any(
            note["kind"] == "route" and "ideal contact" in note["text"]
            for note in entry["notes"]
        ), n
    assert len(scans) == 1
    # A later build must re-read proof inputs rather than reuse a saved verdict.
    assert _build(68, _historical_refinement_packing(68))["state"] == "rational"
    assert len(scans) == 2


def test_a_verified_rational_requires_matching_formal_evidence(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    packing = _historical_refinement_packing(68)
    evidence = copy.deepcopy(
        exact.VerifiedRationalInputs().evidence_row(
            68,
            "E-evand-exact-optima-2026-10-05-exact-replay",
            exact.KKT_KEY,
        )
    )
    for field, value in (
        ("claim", "lower-bound"),
        ("source_key", "[Kingbird]"),
        ("scope", {"n_values": [69]}),
        ("assurance", "numerically-checked"),
        ("method", "numerical-f64"),
        ("replay_status", "failed"),
        ("replay", ""),
        ("certificate", "witnesses/wrong-source"),
    ):
        bad = {**evidence, field: value}
        (tmp_path / "evidence.yaml").write_text(json.dumps({"evidence": [bad]}))
        with monkeypatch.context() as control:
            control.setattr(exact, "FRONTIER", tmp_path)
            _refused(lambda: _build(68, packing), "verified rational bound refused")


def test_native_rational_admission_refuses_missing_and_stale_replays(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    receipt = json.loads(exact.read_retained_text(exact.evand.FIRST_PARTY_RECEIPT))
    missing = tmp_path / "missing.json"
    with monkeypatch.context() as control:
        control.setattr(exact.evand, "FIRST_PARTY_RECEIPT", missing)
        _refused(
            lambda: _build(68, _historical_refinement_packing(68)),
            "verified rational bound refused",
        )
    for change in ("digest", "side", "failed", "source", "count"):
        bad = copy.deepcopy(receipt)
        row = next(row for row in bad["rows"] if row["n"] == 68)
        if change == "digest":
            row["sha256"] = "0" * 64
        elif change == "side":
            row["side"] = "1/2"
        elif change == "failed":
            row["exact_verify"]["passed"] = False
        elif change == "source":
            bad["source"] = "https://example.invalid/another-source"
        else:
            row["n"] = 69
        path = tmp_path / f"{change}.json"
        path.write_text(json.dumps(bad))
        with monkeypatch.context() as control:
            control.setattr(exact.evand, "FIRST_PARTY_RECEIPT", path)
            _refused(
                lambda: _build(68, _historical_refinement_packing(68)),
                "verified rational bound refused",
            )
    source = json.loads(exact.read_retained_text(exact.evand.SOURCE_REPLAY_RECEIPT))
    next(row for row in source["rows"] if row["n"] == 68)["verify_cert"]["exit_status"] = 1
    path = tmp_path / "source-failed.json"
    path.write_text(json.dumps(source))
    with monkeypatch.context() as control:
        control.setattr(exact.evand, "SOURCE_REPLAY_RECEIPT", path)
        _refused(
            lambda: _build(68, _historical_refinement_packing(68)),
            "verified rational bound refused",
        )


def test_native_rational_admission_refuses_changed_and_missing_certificates(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    original = exact.evand.certificate_path
    text = original(exact.evand.CERTS, 68).read_text()
    for name, content in (("changed.cert", text + "\n"), ("missing.cert", None)):
        path = tmp_path / name
        if content is not None:
            path.write_text(content)
        with monkeypatch.context() as control:
            control.setattr(
                exact.evand,
                "certificate_path",
                lambda directory, n, path=path: path if n == 68 else original(directory, n),
            )
            _refused(
                lambda: _build(68, _historical_refinement_packing(68)),
                "verified rational bound refused",
            )


def test_a_matching_display_cannot_replace_the_native_side_or_packet_ceiling() -> None:
    for n in (68, 292):
        packing = _historical_refinement_packing(n)
        value = packing["reported_upper_bound"]["value"] + "1"
        packing["reported_upper_bound"]["value"] = value
        packing["verified_upper_bound"].update(value=value, exact_form=str(Fraction(value)))
        _refused(
            lambda n=n, packing=packing: _build(n, packing), "verified rational bound refused"
        )


@pytest.mark.parametrize(
    ("field", "value", "reason"),
    [
        pytest.param(
            "stored_sha256",
            "0" * 64,
            "stored certificate differs from its receipt",
            id="certificate-digest",
        ),
        pytest.param(
            "exact_form",
            "1/2",
            "receipt's verified value or units above do not follow from it",
            id="registered-ceiling",
        ),
        pytest.param(
            "n",
            291,
            "the ceiling certificate/receipt names a different count",
            id="count",
        ),
        pytest.param(
            "independent",
            {"verification_passed": False},
            "the independent checker refused the certificate",
            id="independent-replay",
        ),
    ],
)
def test_a_packet_ceiling_requires_the_original_certificate_receipt(
    monkeypatch: pytest.MonkeyPatch,
    field: str,
    value: object,
    reason: str,
) -> None:
    source = exact.upper_bound_packets.FRANCISCOUZO
    receipts = exact.upper_bound_packets.certification(source)
    bad = copy.deepcopy(receipts)
    bad[292][field] = value
    monkeypatch.setattr(exact.upper_bound_packets, "certification", lambda _source: bad)
    _refused(lambda: _build(292, _historical_refinement_packing(292)), reason)


def test_a_packet_ceiling_refuses_missing_replays_and_changed_certificates(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    source = exact.upper_bound_packets.FRANCISCOUZO
    read = exact.upper_bound_packets.read_retained_text
    with monkeypatch.context() as control:
        control.setattr(
            exact.upper_bound_packets,
            "read_retained_text",
            lambda path: (
                read(tmp_path / "missing.json") if path == source.certification else read(path)
            ),
        )
        _refused(
            lambda: _build(292, _historical_refinement_packing(292)),
            "verified rational bound refused",
        )
    certificate = source.certificate(292)
    original = Path.read_bytes
    changed = gzip.compress(gzip.decompress(original(certificate)) + b"\n", mtime=0)
    for replacement in (None, changed):

        def read_certificate(path: Path, replacement: bytes | None = replacement) -> bytes:
            if path != certificate:
                return original(path)
            if replacement is None:
                raise FileNotFoundError("missing ceiling certificate")
            return replacement

        with monkeypatch.context() as control:
            control.setattr(Path, "read_bytes", read_certificate)
            _refused(
                lambda: _build(292, _historical_refinement_packing(292)),
                "verified rational bound refused",
            )


@pytest.mark.parametrize("n", [68, 105, 292])
def test_an_explicit_refinement_rational_derives_only_the_finite_identity(n: int) -> None:
    packing = copy.deepcopy(exact.load_packing(n))
    before = copy.deepcopy(packing)
    assert packing["reported_upper_bound"]["minimal_polynomial"] is None
    assert packing["reported_upper_bound"].get("algebraic_source") is None
    entry = _build(n, packing)
    side = Fraction(packing["reported_upper_bound"]["exact_form"])
    assert entry["state"] == "rational"
    assert entry["exact_form"] == packing["reported_upper_bound"]["exact_form"]
    assert entry["polynomial"]["coefficients"] == [str(side.denominator), str(-side.numerator)]
    assert entry["checks"]["root"]["interval"] == [str(side), str(side)]
    assert entry["checks"]["irreducible"]["method"] == "linear"
    assert entry["checks"]["catalogue"] == "derived-here"
    assert entry["algebraic_source"] == "derived-from-exact-form"
    assert entry["side"] == {
        "value": packing["reported_upper_bound"]["value"],
        "relation": "upper-bound",
    }
    assert entry["status"] == packing["status"] == "open"
    assert entry["lower"]["value"] == packing["verified_lower_bound"]["value"]
    assert entry["kkt"] == (
        None
        if not exact.kkt_rows()[n].get("S_exact")
        else {"value": exact.kkt_rows()[n]["S_exact"], "status": exact.kkt_rows()[n]["status"]}
    )
    assert any(note["kind"] == "verified-witness-side" for note in entry["notes"])
    assert any(
        note["kind"] == "route" and "ideal contact research open" in note["text"]
        for note in entry["notes"]
    )
    assert packing == before


@pytest.mark.parametrize(
    "control",
    [
        "reported-form",
        "verified-form",
        "reported-value",
        "verified-value",
        "source",
        "count",
        "replay",
        "proved",
        "degree",
        "origin",
        "unsupported",
    ],
)
def test_explicit_refinement_requires_exact_current_bound_metadata(control: str) -> None:
    packing = copy.deepcopy(exact.load_packing(105))
    reported, verified = packing["reported_upper_bound"], packing["verified_upper_bound"]
    if control == "reported-form":
        reported["exact_form"] = "1/2"
    elif control == "verified-form":
        verified["exact_form"] = "1/2"
    elif control == "reported-value":
        reported["value"] += "1"
    elif control == "verified-value":
        verified["value"] += "1"
    elif control == "source":
        reported["source_key"] = "[Kingbird]"
    elif control == "count":
        packing["n"] = 106
    elif control == "replay":
        verified["evidence"] = []
    elif control == "proved":
        packing["status"] = "proved"
    elif control == "degree":
        reported["algebraic_degree"] = 2
    elif control == "origin":
        reported["algebraic_source"] = "contact-system"
    else:
        reported["exact_form"] = verified["exact_form"] = "sqrt(2)"
    _refused(lambda: _build(105, packing), "a closed form with no minimal polynomial")


@pytest.mark.parametrize("n", [68, 105, 292])
def test_matching_refinement_displays_cannot_replace_the_admitted_side(n: int) -> None:
    packing = copy.deepcopy(exact.load_packing(n))
    value = packing["reported_upper_bound"]["value"] + "1"
    for bound in ("reported_upper_bound", "verified_upper_bound"):
        packing[bound].update(value=value, exact_form=str(Fraction(value)))
    _refused(lambda: _build(n, packing), "refinement rational bound refused")


def test_explicit_refinements_share_custody_only_within_one_build(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    checks = []
    check = refinement_custody.check_index

    def counted(value: dict) -> None:
        checks.append(True)
        check(value)

    monkeypatch.setattr(refinement_custody, "check_index", counted)
    inputs = exact.VerifiedRationalInputs()
    for n in (68, 105, 292):
        entry = exact.build_entry(
            n,
            exact.load_packing(n),
            exact.catalogue_entries().get(n),
            exact.kkt_rows().get(n),
            verified_inputs=inputs,
        )
        assert entry["state"] == "rational"
    assert len(checks) == 1

    def refused(_value: dict) -> None:
        checks.append(True)
        raise ValueError("changed complete replay admission")

    monkeypatch.setattr(refinement_custody, "check_index", refused)
    _refused(lambda: _build(105), "changed complete replay admission")
    assert len(checks) == 2


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("claim", "lower-bound"),
        ("assurance", "reported"),
        ("method", "numerical-f64"),
        ("replay_status", "failed"),
        ("source_key", "[Kingbird]"),
        ("scope", {"n_values": [106]}),
        ("certificate", "packing/resources/wrong-source"),
        ("replay", ""),
    ],
)
def test_explicit_refinement_requires_current_formal_evidence(
    field: str, value: object
) -> None:
    n = 105
    source = refinement_packets.COUZO
    replay = f"E-{source.packet_name}-exact-replay"
    inputs = exact.VerifiedRationalInputs()
    evidence = copy.deepcopy(inputs.evidence_row(n, replay, source.key))
    evidence[field] = value
    inputs.evidence = {replay: evidence}
    _refused(
        lambda: exact.build_entry(
            n,
            exact.load_packing(n),
            exact.catalogue_entries().get(n),
            exact.kkt_rows().get(n),
            verified_inputs=inputs,
        ),
        "refinement rational bound refused",
    )


@pytest.mark.parametrize("mutation", ["input", "positive", "process", "program"])
def test_explicit_refinement_requires_the_complete_retained_replay(
    monkeypatch: pytest.MonkeyPatch, mutation: str
) -> None:
    value = copy.deepcopy(refinement_custody.read_index())
    if mutation == "input":
        value["couzo_jobs"][0]["input_sha256"] = "0" * 64
    elif mutation == "positive":
        value["couzo_jobs"][0]["verdict"]["routes"]["independent"]["verification_passed"] = (
            False
        )
    elif mutation == "process":
        value["process_outcomes"]["processes"][0]["timed_out"] = True
    else:
        value["n68_jobs"][0]["routes"][0]["source_sha256"] = "0" * 64
    monkeypatch.setattr(refinement_custody, "read_index", lambda: value)
    _refused(lambda: _build(105), "refinement rational bound refused")


def test_explicit_refinement_requires_private_receipt_and_source_fact_bytes(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    with monkeypatch.context() as control:
        control.setattr(refinement_custody, "INDEX", tmp_path / "missing-admission.json.xz")
        _refused(lambda: _build(105), "refinement rational bound refused")
    fact = refinement_packets.read_fact(refinement_packets.COUZO, 105)
    fact["squares"][0]["x"] = str(Fraction(fact["squares"][0]["x"]) + 1)
    raw = refinement_packets.json_bytes(fact)
    certificate = refinement_packets.fact_path(refinement_packets.COUZO, 105)
    original = gzip.open
    monkeypatch.setattr(
        gzip,
        "open",
        lambda path, *args, **kwargs: (
            io.BytesIO(raw) if path == certificate else original(path, *args, **kwargs)
        ),
    )
    _refused(lambda: _build(105), "independently pinned complete source conversion")


@pytest.mark.parametrize("n", [68, 105, 292])
def test_supplied_refinement_polynomial_keeps_custody_and_ideal_route(n: int) -> None:
    packing = copy.deepcopy(exact.load_packing(n))
    rational = Fraction(packing["reported_upper_bound"]["exact_form"])
    polynomial = format_polynomial((rational.denominator, -rational.numerator))
    packing["reported_upper_bound"].update(
        minimal_polynomial=polynomial, algebraic_source="derived-from-exact-form"
    )
    before = copy.deepcopy(packing)
    entry = _build(n, packing)
    assert entry["polynomial"]["text"] == polynomial
    assert entry["polynomial"]["coefficients"] == [
        str(rational.denominator),
        str(-rational.numerator),
    ]
    assert entry["checks"]["root"]["interval"] == [str(rational), str(rational)]
    assert any(note["kind"] == "verified-witness-side" for note in entry["notes"])
    assert any(
        note["kind"] == "route" and "ideal contact research open" in note["text"]
        for note in entry["notes"]
    )
    assert packing == before


@pytest.mark.parametrize(
    "control",
    [
        "missing-origin",
        "catalogue-origin",
        "contact-origin",
        "replay",
        "form",
        "display",
        "count",
        "proved",
    ],
)
def test_supplied_refinement_polynomial_cannot_bypass_custody_metadata(control: str) -> None:
    packing = copy.deepcopy(exact.load_packing(105))
    rational = Fraction(packing["reported_upper_bound"]["exact_form"])
    reported = packing["reported_upper_bound"]
    reported.update(
        minimal_polynomial=format_polynomial((rational.denominator, -rational.numerator)),
        algebraic_source="derived-from-exact-form",
    )
    if control == "missing-origin":
        reported["algebraic_source"] = None
    elif control == "catalogue-origin":
        reported["algebraic_source"] = "catalogue"
    elif control == "contact-origin":
        reported["algebraic_source"] = "contact-system"
    elif control == "replay":
        packing["verified_upper_bound"]["evidence"] = []
    elif control == "form":
        packing["verified_upper_bound"]["exact_form"] = "1/2"
    elif control == "display":
        packing["verified_upper_bound"]["value"] += "1"
    elif control == "count":
        packing["n"] = 106
    else:
        packing["status"] = "proved"
    _refused(
        lambda: _build(105, packing),
        "supplied polynomial requires matching current rational metadata",
    )


@pytest.mark.parametrize(
    ("n", "source"), [(106, refinement_packets.COUZO), (105, refinement_packets.N68)]
)
def test_known_refinement_source_cannot_supply_an_unadmitted_count(
    n: int, source: refinement_packets.Source
) -> None:
    packing = copy.deepcopy(exact.load_packing(105))
    rational = Fraction(packing["reported_upper_bound"]["exact_form"])
    packing["n"] = n
    packing["reported_upper_bound"].update(
        source_key=source.key,
        minimal_polynomial=format_polynomial((rational.denominator, -rational.numerator)),
        algebraic_source="derived-from-exact-form",
    )
    _refused(
        lambda: _build(n, packing),
        "supplied polynomial requires matching current rational metadata",
    )


@pytest.mark.parametrize("n", [68, 105, 292])
def test_nearby_supplied_refinement_polynomial_is_refused_exactly(n: int) -> None:
    packing = copy.deepcopy(exact.load_packing(n))
    rational = Fraction(packing["reported_upper_bound"]["exact_form"])
    assert Fraction(1, rational.denominator) < Fraction(1, 10**26)
    packing["reported_upper_bound"].update(
        minimal_polynomial=format_polynomial((rational.denominator, -rational.numerator + 1)),
        algebraic_source="derived-from-exact-form",
    )
    _refused(lambda: _build(n, packing), "is not the minimal polynomial of")


@pytest.mark.parametrize("n", [68, 105, 292])
def test_explicit_refinement_does_not_overwrite_a_polynomial(n: int) -> None:
    packing = copy.deepcopy(exact.load_packing(n))
    packing["reported_upper_bound"].update(
        minimal_polynomial="2s - 1 = 0", algebraic_source="derived-from-exact-form"
    )
    _refused(lambda: _build(n, packing), "is not the minimal polynomial of")


def test_a_perturbed_coefficient_in_a_derived_record_is_refused() -> None:
    packing = copy.deepcopy(exact.load_packing(5))
    assert packing["reported_upper_bound"]["algebraic_source"] == "derived-from-exact-form"
    assert _build(5, packing)["checks"]["catalogue"] == "derived-here"
    packing["reported_upper_bound"]["minimal_polynomial"] = "2s^2 - 8s + 9 = 0"
    _refused(lambda: _build(5, packing), "is not the minimal polynomial of")


def test_a_transcription_that_differs_from_the_catalogue_is_refused() -> None:
    packing = copy.deepcopy(exact.load_packing(28))
    assert _build(28, packing)["checks"]["catalogue"] == "matches"
    text = packing["reported_upper_bound"]["minimal_polynomial"]
    packing["reported_upper_bound"]["minimal_polynomial"] = text.replace("1615", "1616")
    _refused(lambda: _build(28, packing), "differs from the catalogue")


def test_a_fractional_degree_one_side_is_rational_not_integer() -> None:
    """n = 50 is 7 + 4/7: degree 1, but not an integer, which `integer` would claim."""
    assert _build(50)["state"] == "rational"
    assert _build(9)["state"] == "integer"
    totals = _register()["register"]["totals"]
    assert totals["rational"] == sum(
        1 for entry in _entries().values() if entry["state"] == "rational"
    )


def test_a_superseded_catalogue_polynomial_is_a_note_not_the_side() -> None:
    entry = _build(102)
    assert exact.catalogue_entries()[102].minimal_polynomial is not None
    assert entry["state"] == "rational"
    assert entry["polynomial"]["coefficients"] != [
        str(c)
        for c in normalized_polynomial(exact.catalogue_entries()[102].minimal_polynomial or "")
    ]
    assert entry["checks"]["irreducible"]["method"] == "linear"
    (note,) = [n for n in entry["notes"] if n["kind"] == "superseded-catalogue-polynomial"]
    assert note["degree"] == 8
    assert exact.catalogue_entries()[102].side_decimal in note["text"]
    # The control: where the record is the catalogue's own packing, its polynomial is the
    # side's, and there is nothing superseded to say.
    eleven = _build(11)
    assert eleven["checks"]["catalogue"] == "matches"
    assert not [n for n in eleven["notes"] if n["kind"] == "superseded-catalogue-polynomial"]


def test_the_known_superseded_counts_are_exactly_the_noted_ones() -> None:
    noted = sorted(
        n
        for n, entry in _entries().items()
        if any(note["kind"] == "superseded-catalogue-polynomial" for note in entry["notes"])
    )
    assert noted == [
        88,
        102,
        106,
        108,
        123,
        129,
        130,
        153,
        172,
        177,
        179,
        199,
        206,
        228,
        259,
        269,
        292,
        302,
    ]


def test_a_closed_form_must_be_the_isolated_root() -> None:
    _, root = exact.polynomial_checks(5, N5, "2.70710678118654", N5_KKT)
    exact.check_closed_form_is_the_root(5, "2 + (1/2)sqrt(2)", root)
    # The conjugate is a root of the same polynomial, and not the side.
    _refused(
        lambda: exact.check_closed_form_is_the_root(5, "2 - (1/2)sqrt(2)", root), "isolated"
    )


# --- formats ----------------------------------------------------------------------------


def test_polynomial_formats_round_trip() -> None:
    assert exact.polynomial_latex((2, -28, 97)) == "2s^{2} - 28s + 97"
    assert exact.polynomial_latex((1, 0, -1, 1)) == "s^{3} - s + 1"
    for entry in _entries().values():
        polynomial = entry["polynomial"]
        if polynomial is None or entry["degree"] > 42:
            continue
        coefficients = tuple(int(c) for c in polynomial["coefficients"])
        assert normalized_polynomial(polynomial["text"]) == coefficients, entry["n"]
        assert polynomial["text"] == format_polynomial(coefficients)
        assert normalized_polynomial(polynomial["latex"]) == coefficients
    # The control: one changed coefficient is a different polynomial.
    assert normalized_polynomial("2s^2 - 28s + 98 = 0") != (2, -28, 97)


def test_closed_form_latex_round_trips() -> None:
    assert exact.exact_form_latex("7 + (1/2)sqrt(2)") == r"7 + \tfrac{1}{2}\sqrt{2}"
    assert (
        exact.exact_form_latex("10 - (1/2)sqrt(2) + sqrt(1 + sqrt(2))")
        == r"10 - \tfrac{1}{2}\sqrt{2} + \sqrt{1 + \sqrt{2}}"
    )
    for entry in _entries().values():
        if entry["exact_form"] is None:
            continue
        back = exact.parse_form(exact.latex_to_form(entry["exact_form_latex"]))
        assert sp.simplify(back - exact.parse_form(entry["exact_form"])) == 0, entry["n"]
    # The control: a LaTeX form one digit off reads back as a different number.
    wrong = exact.parse_form(exact.latex_to_form(r"7 + \tfrac{1}{3}\sqrt{2}"))
    assert sp.simplify(wrong - exact.parse_form("7 + (1/2)sqrt(2)")) != 0


# --- the register -----------------------------------------------------------------------


def test_the_register_validates_against_its_schema() -> None:
    schema = load_yaml((exact.FRONTIER / exact.SCHEMA).read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    register = _register()["register"]
    assert not list(validator.iter_errors(register))
    broken = copy.deepcopy(register)
    broken["entries"][4]["checks"]["root"]["contains_recorded_side"] = False
    broken["entries"][5]["state"] = "approximately-known"
    assert len(list(validator.iter_errors(broken))) == 2


def test_the_totals_partition_the_range() -> None:
    register = _register()["register"]
    entries = list(_entries().values())
    totals = register["totals"]
    assert sum(totals[state] for state in exact.STATES) == len(entries) == 324
    with_polynomial = sum(1 for entry in entries if entry["polynomial"] is not None)
    assert totals["irreducible-certified"] == totals["root-isolated"] == with_polynomial


def test_every_numeric_only_count_names_its_route_and_bead() -> None:
    without_kkt_point = []
    for n, entry in _entries().items():
        if entry["state"] != "numeric-only":
            continue
        routes = [note for note in entry["notes"] if note["kind"] == "route"]
        assert len(routes) == 1, n
        assert routes[0]["bead"], n
        if "No exact KKT point" in routes[0]["text"]:
            without_kkt_point.append(n)
    assert without_kkt_point == []
    assert any(
        "No exact KKT point" in note["text"] and "ideal contact research open" in note["text"]
        for note in _entries()[105]["notes"]
        if note["kind"] == "route"
    )
    assert _entries()[29]["notes"][0]["bead"] == "think-je8y"
    assert _entries()[83]["notes"][0]["kind"] == "missing-polynomial-text"


@pytest.mark.parametrize("n", [1, 5, 11, 17, 28, 29, 54, 83, 102, 177, 230, 292])
def test_the_committed_entries_equal_a_fresh_build(n: int) -> None:
    assert _build(n) == _entries()[n]


@pytest.mark.slow
def test_the_committed_register_equals_a_fresh_build() -> None:
    assert read_retained_text(exact.RECORD) == exact.register_text(exact.build_record())


def test_register_reads_plain_and_gzip_without_losing_values(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    logical = tmp_path / "exact-values.json"
    text = (
        '{"register":{"entries":[{"n":1,"coefficients":["12345678901234567890"],'
        '"side":"1.0"}]}}\n'
    )
    monkeypatch.setattr(exact, "RECORD", logical)
    logical.write_text(text)
    expected = json.loads(text)["register"]
    assert exact.load_record() == expected
    write_retained_text(compressed_path(logical), text)
    assert exact.load_record() == expected
    logical.unlink()
    assert exact.load_record() == expected
    logical.write_text(text + "\n")
    with pytest.raises(ValueError, match="differs"):
        exact.load_record()


def test_register_update_and_check_rebuild_the_complete_document(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    logical = tmp_path / "exact-values.json"
    monkeypatch.setattr(exact, "RECORD", logical)
    monkeypatch.setattr(exact, "ROOT", tmp_path)
    document = {
        "register": {
            "entries": [{"n": 1, "side": "1.0"}],
            "totals": {"irreducible-certified": 1, "root-isolated": 1},
        }
    }
    calls = []

    def build() -> dict:
        calls.append(True)
        return document

    monkeypatch.setattr(exact, "build_record", build)
    exact.update()
    assert not logical.exists()
    assert read_retained_text(logical) == exact.register_text(document)
    exact.check()
    assert len(calls) == 2
    document["register"]["entries"][0]["side"] = "2.0"
    with pytest.raises(ValueError, match="stale"):
        exact.check()
    assert len(calls) == 3


def test_stale_plain_register_update_preserves_transitional_storage(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    logical = tmp_path / "exact-values.json"
    logical.write_text('{"register":{"old":true}}\n')
    document = {"register": {"entries": [{"n": 1, "side": "7/3"}]}}
    monkeypatch.setattr(exact, "RECORD", logical)
    monkeypatch.setattr(exact, "build_record", lambda: document)
    exact.update()
    assert logical.read_text() == exact.register_text(document)
    assert not compressed_path(logical).exists()
    assert exact.load_record() == document["register"]
