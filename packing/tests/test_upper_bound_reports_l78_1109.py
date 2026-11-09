"""The upper-bound import of the intake pass's lane L78 of 9 November 2026 (think-2h88).

One packet: Joost de Winter's #939 at 199 (JoostdeWinter/square-packing 702c7af), read by
two adapters written for it. ``n199_witness.yaml`` follows Witness/v2's ``witness`` object
without the schema's envelope (`reports.witness_center_basis_bare`), and
``n199_exact.json`` states the same packing as ``[x, y, c, s]`` rows
(`reports.center_direction_json`). Its squares 1 to 172 are a 172-square core at
``S - 1`` and the other 27 the L of #938, so the certificate is the L step on its own core,
pose for pose, which `devtools.construction_checker` writes out. These tests hold the
adapters to what they accept and refuse, and the packet to the prints the issue and
README state, the digests its ``SHA256SUMS`` states, the construction and the comparison
with the house; none needs the network.
"""

from __future__ import annotations

import json
import math
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest
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
HOUSE = "[Gupta rational refinements 2026-10-08]"

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


def test_the_certificate_is_below_the_house_and_the_reports_before_it() -> None:
    side = _certificate().side
    assert f"{float(reports.house_side(HOUSE, 199) - side):.3e}" == "2.882e-03"
    (row,) = reports.check_claims(reports.packet_path(PACKET))["results"]
    assert (row["n"], row["smallest"], row["case"]["relation"]) == (199, reports.THIS, "below")
    assert {
        pending["report"].split()[0]: pending["relation"] for pending in row["pending"]
    } == {
        "T-174": "below",
        "T-193": "below",
        "#938": "below",
    }


def test_the_packet_records_its_retained_files_and_pins() -> None:
    record = json.loads(
        (reports.packet_path(PACKET) / "acquisition/sources.json").read_text("utf-8")
    )
    text = json.dumps(record)
    assert "702c7af2db04c9b69696455ee3d33883a2935e8a" in text
    assert "n199/n199_record.png" in text
    assert Path(reports.packet_path(PACKET) / "source/n199/n199_exact.json.gz").is_file()
