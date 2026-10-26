"""The exact-side register: its decision route, its writer and its refusals (think-vgsw).

`devtools.exact_side_register` derives `packing/frontier/exact-side-register.json` from the
case records, `select_houses`, the intake ledgers and the retained packets, and decides
every inline polynomial again: irreducible by SymPy's factorization over Z, its root
isolated by Descartes' rule of signs. These hold the route to known answers and to the
routes main already trusts, the writer to `exact_sides.form`, the committed register to
its inputs, and each refusal to the input that should cause it.
`devtools.kingbird_root_polynomial` is held to a small synthetic picture: the real one is
not retained, and a test never fetches.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest
import sympy as sp

from devtools import exact_side_register as register
from devtools import exact_sides, select_houses
from devtools import kingbird_root_polynomial as kingbird


@pytest.fixture(scope="module")
def record() -> register.Record:
    return register.load_record()


@pytest.fixture(scope="module")
def committed() -> dict[str, Any]:
    return json.loads(register.REGISTER.read_text(encoding="utf-8"))


def decided(entry: dict[str, Any]) -> exact_sides.Algebraic:
    """The committed entry's side, as its polynomial and interval state it, decided."""
    side = register.decide(
        exact_sides.read_polynomial(entry["polynomial"]),
        (Fraction(entry["interval"]["low"]), Fraction(entry["interval"]["high"])),
    )
    assert isinstance(side, exact_sides.Algebraic)
    return side


# --------------------------------------------------------------------------- the route


@pytest.mark.parametrize(
    ("polynomial", "expected"),
    [
        ((9, -96, 206), True),
        ((1, 0, -5, 0, 6), False),
        ((1, 0, 0, 0, 1), True),
        ((1, 0, -2), True),
        ((4, 0, -1), False),
    ],
)
def test_irreducibility_is_decided_over_q(
    polynomial: tuple[int, ...], *, expected: bool
) -> None:
    """`s^4 + 1` is irreducible over Q though it factors modulo every prime, and
    `4s^2 - 1` is reducible though primitive."""
    assert register.irreducible(polynomial) is expected


@pytest.mark.parametrize(
    ("polynomial", "low", "high", "expected"),
    [
        ((1, 0, -2), Fraction(1), Fraction(2), 1),
        ((1, 0, -2), Fraction(2), Fraction(3), 0),
        ((1, 0, -2), Fraction(-2), Fraction(2), 2),
        ((1, -6, 11, -6), Fraction(0), Fraction(4), 3),
        ((10**60, -(2 * 10**60 + 1), 10**60 + 1), Fraction(0), Fraction(2), 2),
    ],
)
def test_roots_are_counted_by_descartes_with_bisection(
    polynomial: tuple[int, ...], low: Fraction, high: Fraction, expected: int
) -> None:
    """Two roots 1e-60 apart, at 1 and 1 + 1e-60, are told apart by bisecting."""
    assert register.root_count(polynomial, low, high) == expected


def test_an_end_that_is_a_root_does_not_isolate() -> None:
    assert not register.isolates((1, -3, 2), Fraction(1), Fraction(3, 2))
    assert register.isolates((1, -3, 2), Fraction(1, 2), Fraction(3, 2))


def test_decide_refuses_what_an_exact_side_is_not() -> None:
    with pytest.raises(register.RegisterError, match="reducible over Q"):
        register.decide((1, 0, -5, 0, 6), (Fraction(1), Fraction(3, 2)))
    with pytest.raises(register.RegisterError, match="not exactly one root"):
        register.decide((1, 0, -2), (Fraction(-2), Fraction(2)))
    with pytest.raises(register.RegisterError, match="nonempty"):
        register.decide((1, 0, -2), (Fraction(2), Fraction(1)))
    assert register.decide((2, -3), (Fraction(1), Fraction(2))) == Fraction(3, 2)
    side = register.decide((-2, 0, 4), (Fraction(1), Fraction(2)))
    assert isinstance(side, exact_sides.Algebraic)
    assert side.polynomial == (1, 0, -2)


def test_every_inline_side_is_counted_as_sympy_counts_it(committed: dict[str, Any]) -> None:
    """Descartes' count against SymPy's real-root count, an independent route, at every
    decided entry: one root in the interval, none at its ends."""
    symbol = sp.Symbol("s")
    for entry in committed["entries"]:
        if entry["polynomial"] is None:
            continue
        side = decided(entry)
        poly = sp.Poly(list(side.polynomial), symbol)
        low = sp.Rational(str(Fraction(entry["interval"]["low"])))
        high = sp.Rational(str(Fraction(entry["interval"]["high"])))
        assert poly.count_roots(low, high) == 1, entry["n"]


def test_the_writer_is_exact_sides_form_at_every_degree_sturm_decides_cheaply(
    committed: dict[str, Any],
) -> None:
    """`form` writes the text `exact_sides.form` writes. Sturm's route decides it in under
    a second to degree 24 and in seconds above, where the register's own route alone is
    held to it."""
    checked = 0
    for entry in committed["entries"]:
        if entry["polynomial"] is None or entry["degree"] > 24:
            continue
        side = decided(entry)
        assert register.form(side) == exact_sides.form(side) == entry["form"], entry["n"]
        checked += 1
    assert checked >= 10


# --------------------------------------------------------------------------- the register


def test_the_committed_register_is_current(capsys: pytest.CaptureFixture[str]) -> None:
    assert register.check() == 0
    assert "exact-side register check passed" in capsys.readouterr().out


def test_every_house_entry_is_its_records_form(
    committed: dict[str, Any], record: register.Record
) -> None:
    houses = [entry for entry in committed["entries"] if entry["subject"] == register.HOUSE]
    assert houses
    for entry in houses:
        case = record.cases[entry["n"]]
        assert entry["form"] == case.house_form
        assert entry["degree"] == case.reported["algebraic_degree"]
        assert entry["house"]["results"] == record.holders(entry["n"])


def test_every_staged_entry_is_staged_for_its_result_below_its_house(
    committed: dict[str, Any],
) -> None:
    staged = [entry for entry in committed["entries"] if entry["subject"] == register.STAGED]
    assert staged
    for entry in staged:
        pending = select_houses.PENDING_ADOPTION[entry["n"]]
        assert [item["id"] for item in entry["stated_by"]["results"]] == [pending.house]
        assert entry["staged"] == {"bead": pending.bead, "why": pending.why}
        assert entry["house"]["relation"] == register.BELOW


def test_the_large_polynomials_are_held_by_reference_and_measured_facts(
    committed: dict[str, Any],
) -> None:
    by_count = {(entry["n"], entry["subject"]): entry for entry in committed["entries"]}
    s29 = by_count[29, register.CONFIGURATION]
    assert s29["degree"] == 7213
    assert s29["reference"]["member"] == "n29-minpoly/n29_poly_q4.json"
    assert s29["measured"]["coefficients"] == 7214
    assert s29["interval"]["basis"] == register.REPORTED
    assert s29["house"]["relation"] == register.UNDECIDED
    n83 = by_count[83, register.CONFIGURATION]
    assert n83["degree"] == 672
    assert n83["reference"]["asset"].endswith("/square-83.svg")
    assert n83["measured"]["root_index"] == 27
    assert n83["interval"]["basis"] == register.MEASURED
    assert n83["house"]["relation"] == register.BELOW


def tampered(committed: dict[str, Any], tmp_path: Path, n: int, change: dict[str, Any]) -> Path:
    document = json.loads(json.dumps(committed))
    entry = next(item for item in document["entries"] if item["n"] == n)
    entry.update(change)
    path = tmp_path / "exact-side-register.json"
    path.write_text(register.text(document), encoding="utf-8")
    return path


@pytest.mark.parametrize(
    ("n", "change", "named"),
    [
        (70, {"degree": 6}, "n=70 house: degree"),
        (88, {"polynomial": "s^7-50s^6"}, "n=88 staged-house: polynomial"),
        (172, {"interval": {"low": "13.6", "high": "13.7", "basis": "decided"}}, "n=172"),
        (204, {"subject": "staged-house"}, "n=204"),
    ],
)
def test_a_tampered_register_is_refused_naming_its_entry(
    committed: dict[str, Any],
    record: register.Record,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    *,
    n: int,
    change: dict[str, Any],
    named: str,
) -> None:
    path = tampered(committed, tmp_path, n, change)
    assert register.check(path, record) == 1
    assert named in capsys.readouterr().out


def test_a_count_the_selection_no_longer_stages_fails_the_check(
    record: register.Record,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """When the adopting change takes a staged count off `PENDING_ADOPTION`, the register
    is stale until it is regenerated."""
    staged = dict(select_houses.PENDING_ADOPTION)
    n = next(count for count, pending in staged.items() if pending.house == register.T193)
    del staged[n]
    monkeypatch.setattr(select_houses, "PENDING_ADOPTION", staged)
    assert register.check(register.REGISTER, record) == 1
    out = capsys.readouterr().out
    assert f"n={n} configuration: the register has no entry" in out
    assert f"n={n} staged-house: an entry the inputs do not give" in out
    assert "run `python -m devtools.exact_side_register --update`" in out


def test_a_receipt_that_disagrees_with_the_record_is_refused(
    record: register.Record, capsys: pytest.CaptureFixture[str]
) -> None:
    case = record.cases[83]
    reported = {**case.reported, "algebraic_degree": 671}
    altered = replace(record, cases={**record.cases, 83: replace(case, reported=reported)})
    assert register.check(register.REGISTER, altered) == 1
    assert "the measured degree is not the catalogue's" in capsys.readouterr().out


def test_a_house_form_not_written_as_the_writer_writes_it_is_refused() -> None:
    """An isolating interval wider than the writer's forty places states the same side,
    but not in the text a case record holds."""
    text = "root(89s^5-3225s^4+46044s^3-322984s^2+1110284s-1492988, 8.88, 8.89)"
    with pytest.raises(register.RegisterError, match="not written as the house writer"):
        register.read_form(text)
    assert register.read_form("(16+5*sqrt(2))/3") is not None
    assert register.read_form("2 + (1/2)sqrt(2)") is None


# --------------------------------------------------------------------------- the picture


SIDE = "1.41421356237309504880"
PICTURE = (
    '<?xml version="1.0"?>\n<!--\n(*\n    s = Root[-2 + 0*#1 + #1^2 &, 2]\n*)\n-->\n'
    f'<!DOCTYPE svg [\n    <!ENTITY s   "{SIDE}">\n]>\n<svg></svg>\n'
).encode()


def pin(data: bytes) -> kingbird.Pin:
    return kingbird.Pin(
        n=2,
        url="https://example.invalid/square-2.svg",
        size=len(data),
        sha256=hashlib.sha256(data).hexdigest(),
        last_modified=None,
    )


def test_a_pinned_picture_is_measured_and_its_root_isolated() -> None:
    receipt = kingbird.measure(PICTURE, pin(PICTURE), today="2026-10-25")
    assert receipt["polynomial"]["degree"] == 2
    assert receipt["polynomial"]["coefficients"] == 3
    assert receipt["polynomial"]["nonzero_coefficients"] == 2
    assert receipt["polynomial"]["primitive"] is True
    assert receipt["root"]["index"] == 2
    assert receipt["root"]["places"] == 20
    assert receipt["root"]["roots"] == 1
    assert receipt["root"]["endpoint_signs"] == [-1, 1]
    assert Fraction(receipt["root"]["low"]) < Fraction(SIDE) < Fraction(receipt["root"]["high"])
    assert receipt["retained"] is False


def test_a_picture_that_is_not_the_pinned_one_is_refused() -> None:
    changed = PICTURE.replace(b"-2 + ", b"-3 + ")
    with pytest.raises(kingbird.MeasurementError, match="not the pinned one"):
        kingbird.measure(changed, pin(PICTURE), today="2026-10-25")


def test_a_picture_whose_print_misses_the_root_is_refused() -> None:
    """`sqrt(2) = 1.41421356237309504880168...`, nine units of the last place below this."""
    wrong = PICTURE.replace(SIDE.encode(), b"1.41421356237309504890")
    with pytest.raises(kingbird.MeasurementError, match="does not change sign"):
        kingbird.measure(wrong, pin(wrong), today="2026-10-25")


def test_the_root_object_reads_signed_terms_and_refuses_a_term_written_twice() -> None:
    polynomial, index, _length = kingbird.root_object("s = Root[5 - 3*#1 + #1^3 - 12*#1^4, 3]")
    assert polynomial == (-12, 1, 0, -3, 5)
    assert index == 3
    with pytest.raises(kingbird.MeasurementError, match="written twice"):
        kingbird.root_object("s = Root[1 + #1 + 2*#1, 1]")


def test_the_n83_receipt_names_the_pinned_picture_and_the_records_degree(
    record: register.Record,
) -> None:
    receipt = json.loads(register.N83_RECEIPT.read_text(encoding="utf-8"))
    picture = register.pinned_picture(83)
    assert receipt["url"] == picture["url"]
    assert receipt["bytes"] == picture["bytes"]
    assert receipt["polynomial"]["degree"] == record.cases[83].reported["algebraic_degree"]
    assert receipt["root"]["index"] == 27
