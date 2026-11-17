"""The upper-bound import of #1009 in the intake pass of 17 November 2026 (think-i38n).

One packet, read by the ``evand-cert`` adapter: Mykhailo Polkovskyi's 13 centre/half-angle
certificates at ``Mishapolk/square-packing-records@b637e6c``, each held to the source's
Witness/v2 corner file of the same packing. Each side is a rational the issue prints
rounded up at 12 places. The general importer's checks run on the packet through
``test_upper_bound_reports``; these hold what is particular to it: the digests the issue
lists, each print against its exact side, the house each is compared with and the gain,
including the algebraic house at 295, the other reports at 262, 292, 295 and 299, the
replay's margins, the retained sharp controls, and the measurements the register's notes
cite. Every test reads the packets and the ledger only; none needs the network.
"""

from __future__ import annotations

import json
from decimal import ROUND_CEILING, Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import evand_arrangement_reports as kernel
from devtools import upper_bound_reports as reports
from devtools import upper_bound_sharp_controls as sharp

NAME = "mishapolk-issue1009-2026-11-16"
ISSUE = 1009
#: The side #1009 prints at each count, its exact side rounded up at 12 places.
PRINTED = {
    147: "12.651043553173",
    156: "12.977053087495",
    180: "13.915618502788",
    210: "14.971214601589",
    260: "16.633520939840",
    262: "16.698115018700",
    268: "16.871868135103",
    270: "16.928148603340",
    272: "16.965501175831",
    292: "17.590016439231",
    295: "17.698115018700",
    299: "17.801004434252",
    307: "17.979230960384",
}
COUNTS = tuple(PRINTED)
#: The SHA-256 of each certificate and of each Witness/v2 file, as #1009 lists them.
LISTED = {
    147: ("160cf8af8276377ffd8a9e51b135c147ddbf8a2a3bdc6e86486d5e92e11d955e",
          "98e826488dc6f6e8c84e2c0179c0b022480222292a340f86db193ab19b18fb48"),
    156: ("05e95f39700a9ef8180c204eac199889e6d179e32674a00118175fc4d9a0da07",
          "960128de917763696159caa5214da444f4059edd8eed22ea85f08b847e054bb8"),
    180: ("bfe9c58f0f97d2ac2e6051c3e979ed4cfda01137e92093a6aaeb22276ce4104b",
          "2688e96447c5d3712682347de7eb1f40733b307db04189e97cc2460ac7acaafc"),
    210: ("a8c474129b3f432390bb33f4e7818ecf4d11650cd3acda9091584d65120683b4",
          "55ff12cb30a82618d7ec9bbf305a3b7b452fdc362bff1641d1dc41f2f1621e1b"),
    260: ("b059dfa9d855aa14b04635ca1d4ea7d01d8171b64b7c5e21a02bb3914124654f",
          "63d42f58e72e800a8816c4ebf2fe55d9b930935da234b18b5be7db56fb649170"),
    262: ("c5ff84393899ddd099f2c987ea73d7e82f3a65e9136afb9bdc3282a06b3c19bd",
          "b9bc614080bd1874c8d1bec7fc0df295e5d925b8e7d3d7a251d128017b1a7513"),
    268: ("9a6b2bf4a1139eaeefb1b885789acf15e54e4556783aa8ae2c94e6d4e5633755",
          "93cb968796493699515cf6f859f385a8025ce7b2544592a99b9d448d759b6461"),
    270: ("1602ede9a47b7868b0f93268bc45794e48950125d8a405d18c9801f28dcedb6f",
          "8d50402b24290053aa534ae71fa14c684730cdcedb34f8bfa62d5634c5799eaa"),
    272: ("0cd6d68332f84a8856cb47a2f0bfc36116901e6b200dc6041a54fe5552f68778",
          "ec24d11c0c94ad19e7c3c8d6feb6626f5c04923cbc3d33acba8e01e84fa17d18"),
    292: ("bc044512137a02bcf4024898844760b65215984883f1d1f9f42ac65aa540a57b",
          "207a7af131548627c83d5b1cc4b1087dcccd863ef40aeecea63b245c764a6c2c"),
    295: ("7778560e076f207db1913635e1148607011b80e6a0aa96dd614049613abf2cc5",
          "faa40ba28a0cdc3d35d16be9fd3f8b999f4a57c02bd3e0e95dacd50768f3120a"),
    299: ("f20dd01d27f7921d136d9a9211351b5eda1c4103e2de69dc18c94eb01a52e355",
          "a2d19c925ba44a452e17f4d3ccd3b7782ed01e95c03438ddb31c0da2d486198f"),
    307: ("96a54741c680c97e037ebc4f80082802d3da5187b0d3b234ecc6e5c8ea39c963",
          "3f2d737a687c404eb30b202998d54024fb4c8d5b0f026f7a8e6b423ad7caccb1"),
}  # fmt: skip
#: Each count's house when the lane read main f9ddfeeef: its result and the gain the
#: certificate makes on it, at four significant figures.
HOUSES = {
    147: ("T-302", "3.4151e-09"),
    156: ("T-287", "2.5885e-12"),
    180: ("T-288", "2.7096e-12"),
    210: ("T-174", "1.7865e-03"),
    260: ("T-269", "1.1049e-08"),
    262: ("T-101", "8.9918e-03"),
    268: ("T-289", "1.6171e-04"),
    270: ("T-283", "3.2470e-12"),
    272: ("T-174", "8.5299e-05"),
    292: ("T-146", "1.3617e-03"),
    295: ("T-193", "6.1178e-03"),
    299: ("T-277", "3.5268e-12"),
    307: ("T-279", "3.4781e-12"),
}
#: The other reports at a count, and how far the certificate lies below each: by its print
#: until the earlier reports' packets are on main (3.616e-09 exactly at #1006).
PENDING = {
    262: [("#1007", "1.578e-03")],
    292: [("T-193 (#639)", "1.362e-03"), ("#1005", "8.778e-05"), ("#1006", "3.617e-09")],
    295: [("#1007", "1.578e-03")],
    299: [("T-280 (Yim)", "2.345e-12")],
}
#: The least pair gap of each certificate on both routes; every wall clears by 1e-28.
PAIR_GAP = {292: "4.2379e-15", 295: "1.7763e-20", 180: "1.4449e-24"}


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _sides() -> dict[int, Fraction]:
    facts = reports.read_facts(reports.packet_path(NAME))
    return {n: facts[n].side for n in COUNTS}


def _claims() -> dict[int, dict[str, Any]]:
    record = reports.check_claims(reports.packet_path(NAME))
    return {row["n"]: row for row in record["results"]}


def test_the_packet_holds_the_files_whose_digests_the_issue_lists() -> None:
    text = (reports.packet_path(NAME) / "acquisition/upstream-subtree.sha256").read_text(
        "utf-8"
    )
    manifest = {
        path.removeprefix("./"): digest
        for digest, path in (line.split(maxsplit=1) for line in text.splitlines())
    }
    for n, (certificate, witness) in LISTED.items():
        assert manifest[f"certificates/0000-0999/n{n}.cert"] == certificate
        assert manifest[f"witnesses/2026-11-16/n-{n}.yaml"] == witness
    assert len(manifest) == 50


def test_each_print_is_its_exact_side_rounded_up() -> None:
    declaration = reports.load_declaration(reports.packet_path(NAME))
    assert declaration["source_key"] == "[Mishapolk issue 1009 2026-11-16]"
    assert declaration["issue"].endswith(f"/issues/{ISSUE}")
    assert declaration["requested"] == declaration["replayed"] == list(COUNTS)
    rows = {row["n"]: row for row in declaration["certificates"]}
    sides = _sides()
    for n in COUNTS:
        assert (rows[n]["format"], rows[n]["offered"]) == ("evand-cert", PRINTED[n])
        assert rows[n].get("same_packing") == [
            {"path": f"witnesses/2026-11-16/n-{n}.yaml", "format": "witness-corners"}
        ]
        # The bytes were first committed in b9b7fa7, which b637e6c force-pushed over.
        assert rows[n]["first_committed"] == "2026-11-16T23:27:09Z"
        side = sides[n]
        exact = Decimal(side.numerator) / Decimal(side.denominator)
        rounded = exact.quantize(Decimal("1e-12"), rounding=ROUND_CEILING)
        assert str(rounded) == PRINTED[n]
    # 295's packing is 262's with an L strip: its side is 262's plus one and 5.9e-19.
    assert sides[295] - sides[262] - 1 == Fraction(593220133691, 10**30)


def test_each_certificate_is_below_its_house_and_the_other_reports() -> None:
    rows = _claims()
    for n, (result, gain) in HOUSES.items():
        row = rows[n]
        assert (row["smallest"], row["case"]["result"]) == (reports.THIS, result)
        assert row["case"]["relation"] == "below"
        assert f"{float(Fraction(row['case']['difference'])):.4e}" == gain
        pending = [
            (other["report"], f"{float(Fraction(other['difference'])):.3e}")
            for other in row["pending"]
        ]
        assert all(other["relation"] == "below" for other in row["pending"])
        assert pending == PENDING.get(n, [])
    # T-193's side at 295 is a quadratic irrational, compared exactly by its packet's fact.
    case = rows[295]["case"]
    assert case["algebraic"] == "evand-exact-cur-2026-10-16"
    low, high = (Fraction(value) for value in case["difference_bounds"])
    assert 0 < low <= high


def test_the_replay_clears_every_wall_by_1e28_on_both_routes() -> None:
    positives = reports.check_certification(reports.packet_path(NAME))
    margins = reports.margins(positives)
    assert set(margins) == set(COUNTS)
    for n, margin in margins.items():
        walls = {
            Fraction(margin["exact_verify_containment_clearance"]),
            Fraction(margin["independent_containment_clearance"]),
        }
        assert walls == {Fraction(1, 10**28)}
        gap = Fraction(margin["exact_verify_best_pair_gap"])
        assert gap == Fraction(margin["independent_best_pair_gap"])
        assert f"{float(gap):.4e}" == PAIR_GAP.get(n, f"{float(gap):.4e}")
        assert gap < Fraction(5, 10**15)


@pytest.mark.parametrize("n", COUNTS)
def test_the_retained_sharp_controls_meet_contact_and_refuse_1e30_past_it(n: int) -> None:
    """No square touches the box or another square, so each control moves by a positive
    clearance and each enlargement closes its one pair or wall alone: accepted at contact
    and refused past it, the branch the plan stated before any control ran."""
    record = _json(sharp.receipt_path(reports.packet_path(NAME), COUNTS, n))
    assert (record["n"], record["packet"], record["all_as_expected"]) == (n, NAME, True)
    assert record["epsilon"] == str(kernel.SHARP_EPSILON)
    assert {row["control"] for row in record["controls"]} == set(sharp.CONTROLS)
    assert len(record["controls"]) == 11
    for row in record["controls"]:
        assert row["as_expected"] is True
        assert set(row["routes"]) == set(kernel.ROUTES)
    lowered = [row for row in record["controls"] if row["control"] == sharp.SIDE_LOWERED]
    assert Fraction(lowered[0]["detail"]["lowered_by"]) > 0
    wall = [row for row in record["controls"] if row["control"] == sharp.ENLARGED_WALL]
    assert Fraction(wall[0]["detail"]["wall_clearance"]) > 0


#: The refinements at their house's padding, held for the owner's RV-3 (think-ruu2).
HELD = (156, 180, 270, 299, 307)


def _ceil12(side: Fraction) -> str:
    exact = Decimal(side.numerator) / Decimal(side.denominator)
    return str(exact.quantize(Decimal("1e-12"), rounding=ROUND_CEILING))


@pytest.mark.parametrize("n", COUNTS)
def test_each_gain_against_its_house_contraction_margin(n: int) -> None:
    """At the five held counts the gain is 1.01 to 1.07 times the house's own uniform-
    contraction margin and the house contracted rounds up to the claim's own print: RV-3's
    class, as T-285 and T-286. Everywhere else the side rounds up below the house
    contracted, at 147 by 1.16 times the margin and elsewhere far beyond it."""
    measure = reports.packet_path(NAME) / "measure"
    record = _json(measure / f"contraction-n{n}.json")
    assert record["routes_accept"] is True
    margin, gain = Fraction(record["margin"]), Fraction(record["against"]["gain"])
    assert gain == Fraction(record["side"]) - _sides()[n]
    contracted = _ceil12(Fraction(record["side"]) - margin)
    if n in HELD:
        assert 1 < gain / margin < Fraction(11, 10)
        assert contracted == PRINTED[n]
    else:
        assert margin == 0 or gain / margin > Fraction(116, 100)
        assert contracted > PRINTED[n]
    own = _json(measure / f"contraction-n{n}-own.json")
    assert own["routes_accept"] is True
    assert 0 < Fraction(own["margin"]) < Fraction(1, 10**13)


def test_the_262_and_292_certificates_pair_one_to_one_with_the_earlier_reports() -> None:
    """Measured, the 262 and 292 certificates continue the packings of #1007 and #1006,
    which the issue does not name (think-m8ex); 295 does not pair with #1007's."""
    measure = reports.packet_path(NAME) / "measure"

    def pairs(n: int) -> dict[str, Any]:
        record = _json(measure / f"identity-n{n}.json")
        return {pair["against"]: pair for pair in record["pairs"]}

    for n, label, paired in ((262, "#1007", True), (292, "#1006", True), (295, "#1007", False)):
        assert pairs(n)[label]["nearest_centre"]["one_to_one"] is paired
    assert pairs(262)["#1007"]["assignment"]["moved_beyond"]["1e-1"] == 3
    assert pairs(292)["#1006"]["assignment"]["moved_beyond"]["1e-1"] == 3
