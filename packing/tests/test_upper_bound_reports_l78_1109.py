"""The upper-bound import of the intake pass's lane L78 of 10 November 2026 (think-2h88).

One packet: Joost de Winter's #939 at 199 (JoostdeWinter/square-packing 702c7af), read by
two adapters written for it. ``n199_witness.yaml`` follows Witness/v2's ``witness`` object
without the schema's envelope (`reports.witness_center_basis_bare`), and
``n199_exact.json`` states the same packing as ``[x, y, c, s]`` rows
(`reports.center_direction_json`). Its squares 1 to 172 are a 172-square core at
``S - 1`` and the other 27 the L of #938, so the certificate is the L step on its own core,
pose for pose, which `devtools.construction_checker` writes out. These tests hold the
adapters to what they accept and refuse, and the packet to the prints the issue and
README state, the digests its ``SHA256SUMS`` states, the quintic the side lies just above,
the construction, the comparison with the house (T-284), the ledger's verdict, the
retained measurements, and the core's side against Evan Daniel's held solve at 172
(think-wju3); none needs the network.
"""

from __future__ import annotations

import gzip
import json
import math
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest
import sympy
import yaml

from devtools import construction_checker as construction
from devtools import evand_exact_certificates as legacy
from devtools import upper_bound_reports as reports

PACKET = "de-winter-s199-upper-bound-2026-11-09"
#: The side as #939 prints it, at 38 places; as its title prints it; as the root README does.
PRINTED = "14.61468985328358057514628890087947061619"
TITLE = "14.6146898532835806"
TABLE = "14.614689853284"
#: n199/SHA256SUMS at the pin, for the witness and the JSON.
STATED_DIGESTS = {
    "n199/n199_witness.yaml": (
        "a0132182fcbf4f550f10680310f197bbf13531392c5ae2fdf29197416a1208c8"
    ),
    "n199/n199_exact.json": "11bdfa7ad41f65d0ea7460cb50e11bdf724d52031aabf72274bb356c71135d21",
}
HOUSE = "[Özden s199 upper bound 2026-11-09]"
#: The quintic #939 states, highest degree first.
QUINTIC = (62, -4426, 125017, -1746146, 12052670, -32855154)
#: Evan Daniel's regularizer's run on T-282's witness after the adoption of 9 November
#: (think-he66), whose solve the record holds unregistered (think-wju3).
HELD = (
    reports.ROOT
    / "cases/regularized_drawings/think-he66-2026-11-09"
    / "adopt-2026-11-09-n172-270-evand/n-172/report.json.gz"
)
LEDGER = reports.ROOT / "campaign/issue-intake/upper-bounds-939-946-20261111"

#: Two unit squares in a box of side 3: the second turned to the basis (4/5, 3/5), whose
#: half-angle tangent is 1/3. The same packing as test_upper_bound_reports's fixtures.
BARE: dict[str, Any] = {
    "witness": {
        "id": "W-two-Squares",
        "n": 2,
        "side": "3",
        "square_size": "1",
        "representation": "center-basis",
        "scalar": {"kind": "rational"},
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "not-applicable",
        },
        "notes": "read and not believed",
        "squares": [
            {"id": 1, "center": ["1", "1"], "basis": ["1", "0"]},
            {"id": 2, "center": ["2", "2"], "basis": ["4/5", "3/5"]},
        ],
    }
}
DIRECTION: dict[str, Any] = {
    "n": 2,
    "side": "3",
    "square_size": "1",
    "format": "each square: [center_x, center_y, cos, sin]",
    "optimum_minimal_polynomial": [1, -3],
    "squares": [["1", "1", "1", "0"], ["2", "2", "4/5", "3/5"]],
}
EXPECTED = legacy.Certificate(
    2,
    Fraction(3),
    (
        legacy.Pose(Fraction(1), Fraction(1), Fraction(0)),
        legacy.Pose(Fraction(2), Fraction(2), Fraction(1, 3)),
    ),
)


def _yaml(value: dict[str, Any]) -> bytes:
    return yaml.safe_dump(value, sort_keys=False).encode()


def _json(value: dict[str, Any]) -> bytes:
    return json.dumps(value).encode()


def _witness(**changes: Any) -> dict[str, Any]:
    return {"witness": {**BARE["witness"], **changes}}


def _squares(*rows: dict[str, Any]) -> dict[str, Any]:
    return _witness(squares=list(rows))


def test_both_adapters_read_the_packing_the_center_basis_reader_reads() -> None:
    assert reports.parse_certificate(_yaml(BARE), 2, "witness-center-basis-bare") == EXPECTED
    assert reports.parse_certificate(_json(DIRECTION), 2, "center-direction-json") == EXPECTED
    # The polynomial is optional, and read and not believed.
    plain = {
        key: value for key, value in DIRECTION.items() if key != "optimum_minimal_polynomial"
    }
    assert reports.parse_certificate(_json(plain), 2, "center-direction-json") == EXPECTED
    without_notes = {key: value for key, value in BARE["witness"].items() if key != "notes"}
    assert (
        reports.parse_certificate(
            _yaml({"witness": without_notes}), 2, "witness-center-basis-bare"
        )
        == EXPECTED
    )


@pytest.mark.parametrize(
    ("value", "message"),
    [
        (
            {**BARE, "softschema": {"contract": "packing.squares:Witness/v2"}},
            "one witness object",
        ),
        (_witness(claim={"method": "exact"}), "known fields"),
        (_witness(id=7), "known fields"),
        (_witness(n=3), "rational centre-basis witness"),
        (_witness(representation="corners"), "rational centre-basis witness"),
        (_witness(scalar={"kind": "decimal"}), "rational centre-basis witness"),
        (_witness(coordinates={"origin": "centre"}), "rational centre-basis witness"),
        (_witness(side=3), "rational string"),
        (_witness(side="-3"), "positive"),
        (
            _squares(
                {"id": 1, "center": ["1", "1"], "basis": ["1", "0"]},
                {"id": 1, "center": ["2", "2"], "basis": ["4/5", "3/5"]},
            ),
            "distinct ids",
        ),
        (
            _squares(
                {"id": 1, "center": ["1", "1"], "basis": ["1", "0"], "angle": "0"},
                {"id": 2, "center": ["2", "2"], "basis": ["4/5", "3/5"]},
            ),
            "an id, a centre and a basis",
        ),
        (
            _squares(
                {"id": 1, "center": [1.0, "1"], "basis": ["1", "0"]},
                {"id": 2, "center": ["2", "2"], "basis": ["4/5", "3/5"]},
            ),
            "rational string",
        ),
        (
            _squares(
                {"id": 1, "center": ["1", "1"], "basis": ["1", "1"]},
                {"id": 2, "center": ["2", "2"], "basis": ["4/5", "3/5"]},
            ),
            "no rotation",
        ),
        (
            _squares(
                {"id": 1, "center": ["1", "1"], "basis": ["-1", "0"]},
                {"id": 2, "center": ["2", "2"], "basis": ["4/5", "3/5"]},
            ),
            "no finite half-angle",
        ),
        (_squares({"id": 1, "center": ["1", "1"], "basis": ["1", "0"]}), "not 2 squares"),
    ],
)
def test_the_bare_witness_reader_refuses_what_the_format_does_not_state(
    value: dict[str, Any], message: str
) -> None:
    with pytest.raises(reports.ReportError, match=message):
        reports.parse_certificate(_yaml(value), 2, "witness-center-basis-bare")


@pytest.mark.parametrize(
    ("value", "message"),
    [
        ({**DIRECTION, "extra": "x"}, "only the known fields"),
        ({key: v for key, v in DIRECTION.items() if key != "format"}, "only the known fields"),
        ({**DIRECTION, "square_size": "2"}, "only the known fields"),
        ({**DIRECTION, "format": 1}, "only the known fields"),
        ({**DIRECTION, "optimum_minimal_polynomial": [1, True]}, "only the known fields"),
        ({**DIRECTION, "optimum_minimal_polynomial": [1, "3"]}, "only the known fields"),
        ({**DIRECTION, "n": 3}, "count differs"),
        ({**DIRECTION, "side": 3}, "rational string"),
        (
            {**DIRECTION, "squares": [["1", "1", "1"], ["2", "2", "4/5", "3/5"]]},
            "x, y, c and s",
        ),
        ({**DIRECTION, "squares": [[1, "1", "1", "0"], ["2", "2", "4/5", "3/5"]]}, "rational"),
        (
            {**DIRECTION, "squares": [["1", "1", "1", "1"], ["2", "2", "4/5", "3/5"]]},
            "no rotation",
        ),
        (
            {**DIRECTION, "squares": [["1", "1", "-1", "0"], ["2", "2", "4/5", "3/5"]]},
            "half-angle",
        ),
    ],
)
def test_the_direction_reader_refuses_what_the_format_does_not_state(
    value: dict[str, Any], message: str
) -> None:
    with pytest.raises(reports.ReportError, match=message):
        reports.parse_certificate(_json(value), 2, "center-direction-json")


def test_each_reader_refuses_the_other_format_and_options() -> None:
    with pytest.raises(reports.ReportError, match="one witness object"):
        reports.parse_certificate(_json(DIRECTION), 2, "witness-center-basis-bare")
    with pytest.raises(reports.ReportError, match="invalid certificate JSON"):
        reports.parse_certificate(_yaml(BARE), 2, "center-direction-json")
    for form, raw in (
        ("witness-center-basis-bare", _yaml(BARE)),
        ("center-direction-json", _json(DIRECTION)),
    ):
        with pytest.raises(reports.ReportError, match="reads no options"):
            reports.parse_certificate(raw, 2, form, {"dilation": "1"})


# --------------------------------------------------------------------------- the packet


def _manifest() -> dict[str, str]:
    text = (reports.packet_path(PACKET) / "acquisition/upstream-subtree.sha256").read_text(
        "utf-8"
    )
    return {
        path.removeprefix("./"): digest
        for digest, path in (line.split(maxsplit=1) for line in text.splitlines())
    }


def _up(side: Fraction, places: int) -> Fraction:
    return Fraction(math.ceil(side * 10**places), 10**places)


def _certificate() -> legacy.Certificate:
    return reports.read_facts(reports.packet_path(PACKET), {199})[199]


def test_the_packet_holds_the_files_whose_digests_the_source_states() -> None:
    manifest = _manifest()
    assert {path: manifest[path] for path in STATED_DIGESTS} == STATED_DIGESTS
    sums = (reports.packet_path(PACKET) / "source/n199/SHA256SUMS").read_text("utf-8")
    stated = {path: digest for digest, path in (line.split() for line in sums.splitlines())}
    assert all(manifest[f"n199/{path}"] == digest for path, digest in stated.items())


def test_the_prints_are_the_exact_side_rounded_up() -> None:
    declaration = reports.load_declaration(reports.packet_path(PACKET))
    assert declaration["issue"].endswith("/issues/939")
    (row,) = declaration["certificates"]
    assert (row["n"], row["format"], row["offered"]) == (
        199,
        "witness-center-basis-bare",
        PRINTED,
    )
    assert [(other["path"], other["format"]) for other in row.get("same_packing", [])] == [
        ("n199/n199_exact.json", "center-direction-json")
    ]
    side = _certificate().side
    for printed in (PRINTED, TITLE, TABLE):
        places = len(printed.split(".")[1])
        assert _up(side, places) == Fraction(Decimal(printed))
    assert side.denominator == 10**110


def test_the_certificate_is_the_l_step_on_its_own_core() -> None:
    """Squares 1 to 172 at side ``S - 1`` are a packing the L step extends to this one:
    the construction checker writes the same 199 poses, the row of 14 along the top and
    the column of 13 up the right wall, at ``S``."""
    found = _certificate()
    core = legacy.Certificate(172, found.side - 1, found.poses[:172])
    recipe = construction.Recipe(
        n=199,
        kind=construction.TILING,
        source_n=172,
        parent=f"packing/resources/web/{PACKET}/source/n199/n199_witness.yaml",
        parent_sha256=_manifest()["n199/n199_witness.yaml"],
        bound=found.side,
        layers=1,
    )
    assert math.floor(core.side) == 13
    assert construction.capacity(recipe, core.side) == 199
    assert construction.write_out(recipe, core) == found


def test_the_certificate_is_below_the_house_by_its_core_gain_and_across_its_print() -> None:
    """T-284 is T-282 plus one, so the gain at 199 is the core's gain over T-282, exactly."""
    side = _certificate().side
    house = reports.house_side(HOUSE, 199)
    gain = house - side
    assert gain == reports.house_side("[Özden s172 upper bound 2026-11-09]", 172) - (side - 1)
    assert f"{float(gain):.3e}" == "2.635e-12"
    assert (_up(house, 12), _up(side, 12)) == (
        Fraction(Decimal("14.614689853287")),
        Fraction(Decimal(TABLE)),
    )
    (row,) = reports.check_claims(reports.packet_path(PACKET))["results"]
    assert (row["n"], row["smallest"]) == (199, reports.THIS)
    assert (row["case"]["result"], row["case"]["relation"]) == ("T-284", "below")
    assert {
        pending["report"].split()[0]: pending["relation"] for pending in row["pending"]
    } == {"T-174": "below", "T-193": "below"}


def test_the_side_lies_just_above_the_one_root_of_the_quintic_near_it() -> None:
    """The quintic is irreducible over Q; it has exactly one root in [S - 1e-98, S] by
    Sturm's theorem, with the sign changing there; and S lies 1.36e-99 to 1.37e-99 above
    it, as the README's 1.4e-99 says. The certificate proves s(199) <= S and nothing about
    the root."""
    side = _certificate().side
    x = sympy.Symbol("x")
    quintic = sympy.Poly(QUINTIC, x, domain="QQ")
    assert quintic.is_irreducible
    assert len(quintic.real_roots()) == 3

    def at(value: Fraction) -> Fraction:
        total = Fraction(0)
        for coefficient in QUINTIC:
            total = total * value + coefficient
        return total

    def rational(value: Fraction) -> sympy.Rational:
        return sympy.Rational(value.numerator, value.denominator)

    low = side - Fraction(1, 10**98)
    assert quintic.count_roots(rational(low), rational(side)) == 1
    assert quintic.count_roots(13, 16) == 1
    assert at(low) > 0 > at(side)
    # The root lies between S - 1.37e-99 and S - 1.36e-99.
    assert at(side - Fraction(137, 10**101)) > 0 > at(side - Fraction(136, 10**101))


def test_the_core_is_the_held_kkt_point_in_every_place_the_solver_prints() -> None:
    """Evan Daniel's regularizer solved T-282's witness to a KKT point the record holds
    unregistered (think-wju3). Its side, printed at 63 places, is the core's side S - 1 in
    every one of them, and its certificate lies 1.3615e-19 above the core."""
    with gzip.open(HELD, "rt", encoding="utf-8") as stream:
        solve = json.load(stream)["solve"]
    printed = solve["S_exact"]
    places = len(printed.split(".")[1])
    assert places == 63
    core = _certificate().side - 1
    assert abs(Fraction(Decimal(printed)) - core) < Fraction(1, 10**places)
    assert f"{float(Fraction(solve['S_cert']) - core):.4e}" == "1.3615e-19"


def test_the_ledger_records_a_refinement_of_t284s_packing() -> None:
    ledger = json.loads((LEDGER / "ledger.json").read_text("utf-8"))
    text = json.dumps(ledger)
    assert ledger["read_at_main"].startswith("f54ad1048")
    assert "T-284" in text
    assert "#939" in text
    readme = (LEDGER / "README.md").read_text("utf-8")
    assert (
        "#939 14.614689853284: recorded, a refinement of Doğa Özden's packing (T-284)" in readme
    )


def test_the_measurements_the_register_cites() -> None:
    """The retained receipts: one to one with T-284 under the identity, none beyond 1e-3;
    the whole certificates' margins 0; the base's share of T-282's padding 1.0399."""
    measure = reports.packet_path(PACKET) / "measure"

    def read(name: str) -> dict[str, Any]:
        return json.loads((measure / name).read_text("utf-8"))

    (pair, *_) = read("identity-n199.json")["pairs"]
    nearest = pair["nearest_centre"]
    assert (pair["against"], nearest["one_to_one"], nearest["symmetry"]) == ("T-284", True, 0)
    assert nearest["largest_displacement"] == "1.414270e-4"
    assert nearest["moved_beyond"] == {"1e-9": 84, "1e-6": 84, "1e-3": 0, "1e-2": 0, "1e-1": 0}
    assert (
        read("contraction-n199.json")["margin"],
        read("contraction-n199-own.json")["margin"],
    ) == (
        "0",
        "0",
    )
    base = read("contraction-n172-base.json")
    assert (base["margin_float"], base["against"]["gain_over_margin"]) == (
        "2.533458e-12",
        "1.0399",
    )
    held = read("contraction-n172-daniel-held.json")
    assert held["against"]["gain_over_margin"] == "1.0000"
    assert held["certificate"]["sha256"] == (
        "720fcebe098e607650a82cc916e78e84ab105111fb4b2db11587b77f62e08337"
    )


def test_the_packet_records_its_retained_files_and_pins() -> None:
    record = json.loads(
        (reports.packet_path(PACKET) / "acquisition/sources.json").read_text("utf-8")
    )
    text = json.dumps(record)
    assert "702c7af2db04c9b69696455ee3d33883a2935e8a" in text
    assert "n199/n199_record.png" in text
    assert Path(reports.packet_path(PACKET) / "source/n199/n199_exact.json.gz").is_file()


# --------------------------------------------------------------------------- #946 at 172

PACKET_172 = "de-winter-s172-upper-bound-2026-11-10"
#: The quintic #946 states: #939's, shifted by one.
QUINTIC_172 = (62, -4116, 107933, -1397031, 8918035, -22427977)


def _certificate_172() -> legacy.Certificate:
    return reports.read_facts(reports.packet_path(PACKET_172), {172})[172]


def test_946_is_t282s_packing_below_it_at_the_root_of_the_shifted_quintic() -> None:
    """The source's README prints the side rounded up at 12 places; the quintic is #939's
    shifted by one, irreducible, with one root in [S - 1e-318, S], 1.56e-319 below S; the
    side is #939's core side less 1.36e-99, and 2.635e-12 below T-282, crossing its print."""
    declaration = reports.load_declaration(reports.packet_path(PACKET_172))
    (row,) = declaration["certificates"]
    assert (row["n"], row["format"], row["offered"]) == (
        172,
        "witness-center-basis-bare",
        "13.614689853284",
    )
    side = _certificate_172().side
    assert _up(side, 12) == Fraction(Decimal("13.614689853284"))
    x = sympy.Symbol("x")
    quintic = sympy.Poly(QUINTIC_172, x, domain="QQ")
    assert quintic == sympy.Poly(
        sympy.Poly(QUINTIC, x).as_expr().subs(x, x + 1), x, domain="QQ"
    )
    assert quintic.is_irreducible
    low = side - Fraction(1, 10**318)
    assert (
        quintic.count_roots(
            sympy.Rational(low.numerator, low.denominator),
            sympy.Rational(side.numerator, side.denominator),
        )
        == 1
    )

    def at(value: Fraction) -> Fraction:
        total = Fraction(0)
        for coefficient in QUINTIC_172:
            total = total * value + coefficient
        return total

    assert at(side - Fraction(157, 10**321)) > 0 > at(side - Fraction(156, 10**321))
    core = _certificate().side - 1
    assert f"{float(core - side):.3e}" == "1.361e-99"
    house = reports.house_side("[Özden s172 upper bound 2026-11-09]", 172)
    assert f"{float(house - side):.3e}" == "2.635e-12"
    (claim,) = reports.check_claims(reports.packet_path(PACKET_172))["results"]
    assert (claim["smallest"], claim["case"]["result"], claim["case"]["relation"]) == (
        reports.THIS,
        "T-282",
        "below",
    )


def test_946_measurements_and_ledger() -> None:
    measure = reports.packet_path(PACKET_172) / "measure"

    def read(name: str) -> dict[str, Any]:
        return json.loads((measure / name).read_text("utf-8"))

    contraction = read("contraction-n172.json")
    assert (contraction["margin_float"], contraction["against"]["gain_over_margin"]) == (
        "2.533458e-12",
        "1.0399",
    )
    (pair, *_) = read("identity-n172.json")["pairs"]
    assert (pair["against"], pair["nearest_centre"]["one_to_one"]) == ("T-282", True)
    assert pair["nearest_centre"]["moved_beyond"]["1e-3"] == 0
    readme = (LEDGER / "README.md").read_text("utf-8")
    assert (
        "#946 13.614689853284: recorded, a refinement of Doğa Özden's packing (T-282)" in readme
    )
