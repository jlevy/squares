"""The filled-end checker: #847's rows decided exactly from their parameters.

`devtools.filled_end_checker` decides a filled-end two-band L packing (Ryu's L frame, two
tilted bands of independent width, tilt and lift, each band's ends filled with
axis-parallel layers) by its lemma, with no certificate. The refusals come first: every
parameter the lemma does not state, each control by the check it names, what each control
depends on, a control the checker would accept or refuse for another reason reported as
not refused, a malformed table, and a V1.0 archive that is not what it must be. Then the
agreements: a small packing written out and decided on both exact routes of
`devtools.couzo_678_replay`, its lowered side and a layer one over refused by both routes
too; the author-built sample written out byte for byte; every V2.0 decision and the
replay sample's rule; both receipts' headers, V1.0's Q-847a label among them, and their
sample rows; and an altered, refused-row or damaged receipt named. Every row's controls
read back again, every count's digest and a replayed count are in the slow lane.
"""

from __future__ import annotations

import io
import json
import re
import shutil
import warnings
import zipfile
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from devtools import couzo_678_replay as base
from devtools import evand_exact_certificates as legacy
from devtools import filled_end_checker as checker
from devtools import retained_data

#: A small packing at its binding side, with layers at all four band ends: K = 12, the V
#: band 7 wide at tan(theta/2) = 1/5 (c = 12/13, s = 5/13), the H band 8 wide at the same
#: tilt, so the V fit binds and the H fit has 1/13 of slack.
SMALL = checker.FilledEnd(
    n=1,
    side=Fraction(154, 13),
    k=12,
    width_v=7,
    tilt_v=Fraction(1, 5),
    lift_v=Fraction(1, 4),
    width_h=8,
    tilt_h=Fraction(1, 5),
    lift_h=Fraction(1, 3),
)


def _small() -> checker.FilledEnd:
    """`SMALL` at its capacity."""
    return replace(SMALL, n=checker.capacity(SMALL))


def _routes(cert: legacy.Certificate) -> tuple[bool, bool]:
    """Whether each exact route accepts a certificate: ``sqpack``'s, the independent one's."""
    result = base.decide(base.geometry(cert))
    return result["sqpack"]["passed"], result["independent"]["passed"]


def test_the_small_packing_is_decided_with_its_layers() -> None:
    """`SMALL` holds the grid's 5 x 4, the V band's 8 rows of 7 and layers (4, 2) and
    (5, 2), and the H band's one row of 8 and layers (5, 3) and (6, 4, 1): 116 squares.
    The V fit binds and the H fit has 1/13 of slack."""
    found = checker.decide(_small())
    assert (found["grid"], found["v_rows"], found["h_rows"]) == (20, 8, 1)
    assert (found["v_layers"], found["h_layers"]) == ([[4, 2], [5, 2]], [[5, 3], [6, 4, 1]])
    assert (found["v_slack"], found["h_slack"]) == ("0", "1/13")
    assert found["surplus"] == 0
    assert found["side_below_k"]
    assert found["capacity"] == 20 + 7 * 8 + 13 + 8 * 1 + 19 == 116


def test_parameters_the_lemma_does_not_state_are_refused() -> None:
    """Each range the lemma needs is required: a positive count and side, K in range and
    the side at most K, both tilts in (0, 1), each band 1 to K - 1 wide, both fit
    inequalities, a band at least h long, each lift in [0, F], stated layers at all four
    ends or none, each stated count non-negative and at most W - a_i, and the kind."""
    row = _small()
    v, h = checker.bands(row)
    # A V band 9 wide leaves the H band 3 to run in, less than its depth 62/13.
    short = replace(row, width_v=9, width_h=10)
    short = replace(short, side=checker.binding_side(short))
    # An H band 7 wide at tan(theta/2) = 1/6 reaches above the V fit.
    high = replace(row, width_h=7, tilt_h=Fraction(1, 6))
    layers = checker.own_layers(row)
    refused = {
        "no squares to pack": replace(row, n=0),
        "is not positive": replace(row, side=Fraction(0)),
        "K = 1001: the checker decides 2 <= K <= 1000": replace(row, k=1001),
        "is above K = 12": replace(row, side=Fraction(12) + checker.FIT_MARGIN),
        "tV = -1/5: ": replace(row, tilt_v=-row.tilt_v),
        "tH = 9/8: ": replace(row, tilt_h=Fraction(9, 8)),
        "bV = 0: a band is 1 to K - 1 = 11 wide": replace(row, width_v=0),
        "bH = 12: ": replace(row, width_h=12),
        "the H band, 6.94594594595 high from y = K - bH, passes the top wall by 1.000e-15": (
            replace(high, side=checker.binding_side(high) - checker.FIT_MARGIN)
        ),
        "the H band, 4.76923076923 deep, is longer than its length 3": short,
        "the V lift -1/4 is negative": replace(row, lift_v=-row.lift_v),
        "the H lift passes its free length": replace(row, lift_h=h.free + checker.FIT_MARGIN),
        "all four band ends or of none": replace(row, layers=layers[:3]),
        "the H far-end layer 0 holds -1 squares": replace(row, layers=(*layers[:3], (-1,))),
        "the V near-end layer 1, 3 squares, crosses the band's end row": replace(
            row, layers=((4, 3), *layers[1:])
        ),
        "not a filled-end packing": replace(row, kind="two-strip"),
    }
    assert v.free > row.lift_v
    for reason, changed in refused.items():
        with pytest.raises(checker.FilledEndRefusedError, match=re.escape(reason)):
            checker.decide(changed)
    with pytest.raises(checker.FilledEndRefusedError, match="above the capacity"):
        checker.write_out(replace(row, n=row.n + 1))


def test_fewer_layer_squares_than_the_floor_are_decided() -> None:
    """The lemma admits any layer counts up to the floor: with every layer emptied the
    row is decided at the bands' rows alone, and its capacity falls by the layers'
    squares."""
    row = _small()
    emptied = replace(row, n=1, layers=((), (), (), ()))
    found = checker.decide(emptied)
    layers = sum(sum(counts) for counts in checker.own_layers(row))
    assert found["capacity"] == row.n - layers
    assert (found["v_layers"], found["h_layers"]) == ([[], []], [[], []])


def test_every_control_is_refused_by_the_check_it_names() -> None:
    """At V2.0's first row each of the eighteen controls is refused by its own check, and
    for every lemma hypothesis one is: the capacity, the V fit 10^-15 short, each lift
    10^-15 past its free length, each band end's layers one over at every level and the
    level after (here 3, 4, 3 and 3 changes), the tilt's range by no tilt, a right angle
    and a negative tilt, the kind, the H fit by the H band one square narrower, the lift
    10^-15 below zero, a layer of -1, the H band K wide, K = 1, and the H band left 1 long
    by a V band K - 1 wide, shorter than its depth."""
    row = checker.records()[0]
    assert row.n == 1182
    found = {item["control"]: item for item in checker.controls(row)}
    assert list(found) == list(checker.CONTROLS) == list(checker.CONTROL_CHECKS)
    assert len(found) == 18
    assert all(item["refused"] for item in found.values())
    assert {name: item["check"] for name, item in found.items()} == checker.CONTROL_CHECKS
    named = set(checker.CONTROL_CHECKS.values())
    hypotheses = {"2 <= K", "1 <= b <= K - 1", "0 < t < 1", "V fit", "H fit", "h <= L"}
    hypotheses |= {"y >= 0", "V y <= F", "H y <= F", "m_i >= 0", "V near m_i <= W - a_i"}
    assert hypotheses <= named
    reasons = {name: item["reason"] for name, item in found.items()}
    assert reasons["count above the capacity"] == "n = 1183 is above the capacity 1182"
    assert reasons["side below the binding fit"].startswith("the V band")
    assert "passes the right wall by 1.000e-15" in reasons["side below the binding fit"]
    assert reasons["V lift past its free length"].startswith("the V lift passes its free")
    assert reasons["H lift past its free length"].startswith("the H lift passes its free")
    ends = ("a V near-end", "a V far-end", "an H near-end", "an H far-end")
    for name, end in zip(ends, ("V near", "V far", "H near", "H far"), strict=True):
        assert reasons[f"{name} layer one over"].startswith(f"the {end}-end layer 0")
    assert [found[f"{name} layer one over"]["changes"] for name in ends] == [3, 4, 3, 3]
    assert reasons["no tilt"].startswith("tH = 0: ")
    assert reasons["a right angle"].startswith("tV = 1: ")
    assert reasons["a negative tilt"].startswith("tH = -17/100: ")
    assert "not a filled-end packing" in reasons["unknown kind"]
    assert reasons["the H band one square narrower"].startswith("the H band, ")
    assert "passes the top wall" in reasons["the H band one square narrower"]
    assert reasons["a V lift below zero"] == "the V lift -1/1000000000000000 is negative"
    assert reasons["a V near-end layer of -1 squares"] == (
        "the V near-end layer 2 holds -1 squares"
    )
    assert reasons["an H band K wide"] == "bH = 35: a band is 1 to K - 1 = 34 wide"
    assert reasons["K of one"] == "K = 1: the checker decides 2 <= K <= 1000"
    assert reasons["an H band shorter than its depth"].startswith("the H band, 3.587")
    assert reasons["an H band shorter than its depth"].endswith("than its length 1")


def _without(check: str) -> object:
    """`_refuse` with one check (`CHECKS`) deleted: a refusal whose words are that
    check's is passed over, as if its line were gone."""
    pattern = re.compile(checker.CHECKS[check])

    def refuse(condition: object, message: str) -> None:
        if not condition and pattern.match(message) is None:
            raise checker.FilledEndRefusedError(message)

    return refuse


def test_what_each_control_depends_on(monkeypatch: pytest.MonkeyPatch) -> None:
    """At 1188, the replay sample's first count, each control decided with the check it
    names deleted: eleven are then accepted, so they stand on that check alone; a right
    angle crashes in `frame`'s p = 1/c, which is why the tilt check comes before any
    division; and the other six are refused by another check as well, which `controls`
    does not ask about, since each is refused by its own at every row."""
    (row,) = checker.rows_at(checker.V2, [1188])
    elsewhere = {
        "H lift past its free length": "n <= capacity",
        "no tilt": "H fit",
        "a V near-end layer of -1 squares": "V near m_i <= W - a_i",
        "an H band K wide": "n <= capacity",
        "K of one": r"the side \S+ is above K = 1",
        "an H band shorter than its depth": "H y <= F",
    }
    found: dict[str, set[str]] = {}
    for name, changes in checker.mutants(row):
        monkeypatch.setattr(checker, "_refuse", _without(checker.CONTROL_CHECKS[name]))
        verdicts: set[str] = set()
        for changed in changes:
            try:
                checker.decide(changed)
            except checker.FilledEndRefusedError as error:
                verdicts.add(str(error))
            except ZeroDivisionError:
                verdicts.add("crashed")
            else:
                verdicts.add("accepted")
        monkeypatch.undo()
        found[name] = verdicts
    assert found.pop("a right angle") == {"crashed"}
    for name, check in elsewhere.items():
        pattern = re.compile(checker.CHECKS.get(check, check))
        assert all(pattern.match(said) for said in found.pop(name)), name
    assert found == {name: {"accepted"} for name in found}
    assert len(found) == 11


def test_a_control_not_refused_by_its_check_is_reported_not_passed_over(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Every control is refused by the lemma's own bounds, so none is ever accepted at a
    genuine row; a control whose change `decide` accepts, here the row itself, is
    reported ``refused`` False with no reason; one refused by another check than the one
    it names, here a count of zero for no tilt, is reported ``refused`` False with that
    reason; and a control of several changes is refused only when all are."""
    row = _small()
    changes = [("count above the capacity", [row]), ("no tilt", [replace(row, n=0), row])]
    monkeypatch.setattr(checker, "mutants", lambda _: changes)
    assert checker.controls(row) == [
        {
            "control": "count above the capacity",
            "check": "n <= capacity",
            "refused": False,
            "reason": "",
            "changes": 1,
        },
        {
            "control": "no tilt",
            "check": "0 < t < 1",
            "refused": False,
            "reason": "n = 0: no squares to pack",
            "changes": 2,
        },
    ]
    tilted = replace(row, tilt_h=Fraction(0))
    monkeypatch.setattr(checker, "mutants", lambda _: [("no tilt", [tilted, row])])
    assert checker.controls(row)[0]["refused"] is False
    assert checker.controls(row)[0]["reason"] == ""


def test_a_small_packing_written_out_agrees_with_both_routes() -> None:
    """`SMALL`, written out at its capacity, passes both exact routes and both refuse
    their six controls. Its side 10^-15 lower, past what `decide` accepts, puts the V band
    through the right wall, and a V near-end layer one square over meets the band's first
    row: both routes refuse each."""
    row = _small()
    cert = checker.write_out(row)
    assert (cert.n, cert.side, len(cert.poses)) == (row.n, row.side, row.n)
    assert cert.poses == tuple(checker.poses(row))
    assert _routes(cert) == (True, True)
    assert all(
        item["refused_by_sqpack"] and item["refused_by_independent"]
        for item in base.decide_controls(cert)
    )
    assert _routes(legacy.Certificate(row.n, row.side - checker.FIT_MARGIN, cert.poses)) == (
        False,
        False,
    )
    v, _ = checker.bands(row)
    held = v.near[0]
    extra = legacy.Pose(
        row.k - row.width_v + v.across - held - Fraction(1, 2), Fraction(1, 2), Fraction(0)
    )
    grown = legacy.Certificate(row.n + 1, row.side, (*cert.poses, extra))
    assert _routes(grown) == (False, False)


def test_write_out_drops_the_surplus_from_the_start_of_the_grid() -> None:
    """Below its capacity a row is written out as the construction's last n squares, so
    the first grid squares are the ones dropped, as the author's ``build`` drops them; a
    row the lemma refuses is not written out, since no route decides one in its place."""
    row = replace(_small(), n=_small().n - 3)
    cert = checker.write_out(row)
    placed = list(checker.poses(row))
    assert cert.poses == tuple(placed[3:])
    with pytest.raises(checker.FilledEndRefusedError, match="above the capacity"):
        checker.write_out(replace(row, n=len(placed) + 1))
    with pytest.raises(checker.FilledEndRefusedError, match="above the capacity"):
        checker.replay_row(replace(row, n=len(placed) + 1))


def test_write_out_is_the_author_s_build_at_the_author_built_sample() -> None:
    """At 1182, 2505, 4990, 7500 and 9946, the certificates `write_out` writes have the
    SHA-256, size and side of the author-built sample's receipt
    (`devtools.filled_end_sample`), so the lemma's builder and the author's agree byte for
    byte there, and nothing of his runs here."""
    assert checker.author_sample_problems() == []


def test_every_v2_decision_is_the_receipt_s_and_the_replay_sample_the_rule_s() -> None:
    """Every V2.0 row decided once by the lemma, controls aside, is its decisions
    receipt's row, digests and the control count aside, so the quick lane decides all
    5,134 (`test_v2_s_receipts_hold` derives every control again, in the slow lane). The
    replay sample is `edge_counts`'s choice over those decisions: the first count with a
    lift of zero, then the counts with the least layer slack, H lift room, V lift room and
    H fit slack. A count the deposit has no row at is named."""
    rows = checker.records()
    decided = {row.n: checker.decide(row) for row in rows}
    stored = checker.read_receipt(checker.V2.decisions)["rows"]
    aside = {"controls_refused", *checker.DIGEST_FIELDS}
    assert [
        {key: value for key, value in item.items() if key not in aside} for item in stored
    ] == [decided[row.n] for row in rows]
    assert checker.edge_counts(rows, decided) == checker.SAMPLE
    with pytest.raises(ValueError, match=r"V2\.0 has no row at n = 5, 7"):
        checker.rows_at(checker.V2, [1182, 5, 7])


def _csv(*rows: tuple[str, ...], header: tuple[str, ...] = checker.COLUMNS) -> str:
    return "\r\n".join(",".join(fields) for fields in (header, *rows)) + "\r\n"


#: V2.0's first row, as filled_records.csv states it.
FIRST = (
    "1182",
    "35",
    "5694335/163249",
    "34.881285643404",
    "34.883789730000",
    "Karimi v5",
    "10",
    "57/400",
    "4737305911/51178887998",
    "8",
    "17/100",
    "11099417/99916479",
)


def test_the_ingest_refuses_every_malformed_table_as_custody() -> None:
    """`parse_table` reads a deposit as untrusted data and refuses, as a `CustodyError`
    and never a bare KeyError, TypeError or ValueError: a missing, extra or renamed
    column; a short, long or blank row; a K above the checker's bound or not
    ceil(sqrt(n)); a literal past `MAX_DIGITS`, one of 5,000 digits, a negative lift and
    a malformed comparison column; a decimal side a unit of its last place off the exact
    side; an unknown ``previous_source``; a count given twice; and a field past the csv
    module's size limit. The row reader refuses a missing field and a field that is not
    text. V2.0's first row, as stated, parses, with the author's two columns beside it."""
    assert checker.parse_table(_csv(FIRST)) == [
        (checker.records()[0], "Karimi v5", "34.881285643404")
    ]

    def changed(index: int, value: str) -> tuple[str, ...]:
        return (*FIRST[:index], value, *FIRST[index + 1 :])

    refused = {
        "the header is": _csv((*FIRST, "x"), header=(*checker.COLUMNS, "comment")),
        "the header is ": _csv(FIRST[:-1], header=checker.COLUMNS[:-1]),
        "the header is  ": _csv(FIRST, header=("N", *checker.COLUMNS[1:])),
        "row 1: 11 fields, not 12": _csv(FIRST[:-1]),
        "row 1: 13 fields, not 12": _csv((*FIRST, "")),
        "row 2: 0 fields, not 12": _csv(FIRST, (), changed(0, "1184")),
        "K = 1001 is above the checker's bound 1000": _csv(("1000001", "1001", *FIRST[2:])),
        "K = 36 is not ceil": _csv(changed(1, "36")),
        "'5694335/1" + "0" * 30 + "' is not the literal": _csv(
            changed(2, "5694335/1" + "0" * 30)
        ),
        "is not the literal": _csv(changed(7, "1/" + "7" * 5000)),
        "'-4737305911/51178887998' is not the literal": _csv(
            changed(8, "-4737305911/51178887998")
        ),
        "'none' is not the literal": _csv(changed(4, "none")),
        "the decimal side is not the exact side": _csv(changed(3, "34.881285643405")),
        "previous_source 'Somebody' is not one of": _csv(changed(5, "Somebody")),
        "a count appears in more than one row": _csv(FIRST, FIRST),
        "field larger than field limit": _csv(changed(9, "1" * 200_000)),
    }
    for reason, text in refused.items():
        with pytest.raises(checker.CustodyError, match=re.escape(reason.strip())):
            checker.parse_table(text)
    item: dict[str, object] = dict(zip(checker.COLUMNS, FIRST, strict=True))
    for broken in ({**item, "tV": None}, {key: item[key] for key in checker.COLUMNS[1:]}):
        with pytest.raises(checker.CustodyError, match=r"filled_records\.csv n="):
            checker.row_from_record(broken)


def _moved(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A copy of the packet that the checker reads instead of the retained one."""
    copied = tmp_path / "packet"
    shutil.copytree(checker.PACKET, copied)
    monkeypatch.setattr(checker, "PACKET", copied)
    return copied


def test_v1_is_read_from_its_archive_as_untrusted_data(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """V1.0's table is read from the author's archive, retained in Git, whose custody is
    the packet's (`acquire_source --check`), so no digest is compared here. The archive is
    still another party's: one holding ``filled_records.csv`` twice or none, a member past
    `MAX_RECORDS_BYTES`, bytes that are no archive, and an archive whose table holds
    another number of rows are each refused as custody."""
    rows = checker.records(checker.V1)
    assert (len(rows), rows[0].n, rows[-1].n) == (4571, 1184, 9946)
    _moved(tmp_path, monkeypatch)

    def archive(name: str, members: dict[str, bytes]) -> checker.Deposit:
        with zipfile.ZipFile(checker.PACKET / name, "w") as written:
            for member, data in members.items():
                written.writestr(member, data)
        return replace(checker.V1, archived=name)

    small = archive("one.zip", {"filled_records.csv": _csv(FIRST).encode()})
    with pytest.raises(checker.CustodyError, match="holds 1 rows, not 4571"):
        checker.records(small)
    with pytest.raises(checker.CustodyError, match=re.escape("holds 0 filled_records.csv")):
        checker.archived_records(archive("none.zip", {"README.md": b"x"}))
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as written, warnings.catch_warnings():
        warnings.simplefilter("ignore")
        written.writestr("filled_records.csv", b"x")
        written.writestr("filled_records.csv", b"x")
    (checker.PACKET / "twice.zip").write_bytes(buffer.getvalue())
    with pytest.raises(checker.CustodyError, match=re.escape("holds 2 filled_records.csv")):
        checker.archived_records(replace(small, archived="twice.zip"))
    large = archive("large.zip", {"filled_records.csv": b"0" * (checker.MAX_RECORDS_BYTES + 1)})
    with pytest.raises(
        checker.CustodyError, match=re.escape("filled_records.csv is too large")
    ):
        checker.archived_records(large)
    (checker.PACKET / "plain.zip").write_bytes(b"not an archive")
    with pytest.raises(checker.CustodyError, match="File is not a zip file"):
        checker.archived_records(replace(small, archived="plain.zip"))


def _summary_holds(deposit: checker.Deposit, expected: tuple[int, int, int, int]) -> None:
    """A deposit's decisions summary: every row decided, none refused, its squares, how
    many rows are filled to the capacity and the most surplus, and each of the eighteen
    controls refused at every row by the check it names."""
    rows, squares, tight, most = expected
    summary = checker.read_receipt(deposit.decisions)["summary"]
    assert (summary["rows"], summary["decided"], summary["refused"]) == (rows, rows, [])
    assert (summary["squares"], summary["surplus_zero"], summary["surplus_most"]) == (
        squares,
        tight,
        most,
    )
    assert summary["side_below_k"] == summary["k_is_ceil_sqrt_n"] == rows
    assert sorted(summary["controls"]) == sorted(checker.CONTROLS)
    assert all(item["refused"] == rows for item in summary["controls"].values())
    assert {name: item["check"] for name, item in summary["controls"].items()} == (
        checker.CONTROL_CHECKS
    )


#: Where the author's decimal side lies against the exact side, by deposit: below it at
#: about half the rows, so it is no bound (review F2 of #870).
DECIMAL_SIDES = {
    "V2.0": {
        "below_exact": 2514,
        "equal": 4,
        "above_exact": 2616,
        "most_below_units": "0.502",
        "most_above_units": "0.503",
    },
    "V1.0": {
        "below_exact": 2204,
        "equal": 9,
        "above_exact": 2358,
        "most_below_units": "0.504",
        "most_above_units": "0.506",
    },
}


def test_each_receipt_s_header_and_sample_rows_hold() -> None:
    """Both decisions receipts' headers are this checker's, every field `decide_all`
    writes but its run's compared with the deposit's (`decisions_header`). V1.0's note
    names Q-847a, so a V1.0 receipt that dropped the label fails here, on the pull-request
    surface. The author's decimal side is counted against the exact side, below it at
    2,514 V2.0 rows and 2,204 V1.0 rows. At each deposit's sample counts and the replay
    sample's, the row with its eighteen controls and its certificate's digest, derived
    again, is the receipt's; and the replay receipt holds against the decisions rows."""
    assert "Q-847a" in checker.V1.note
    assert "Q-847a" not in checker.V2.note
    for deposit in checker.DEPOSITS:
        parsed = checker.table(deposit)
        receipt = checker.read_receipt(deposit.decisions)
        assert checker.header_problems(deposit, receipt, parsed) == []
        assert receipt["note"] == deposit.note
        assert receipt["author_columns"]["side"] == DECIMAL_SIDES[deposit.label]
        stored = {item["n"]: item for item in receipt["rows"]}
        rows = {item.row.n: item.row for item in parsed}
        for n in sorted({*deposit.sample, *(checker.SAMPLE if deposit.replay else ())}):
            wanted, _ = checker.decision_row(rows[n])
            assert not checker.row_differs(stored[n], wanted), n
            assert stored[n]["controls_refused"] == len(checker.CONTROLS)
        if deposit.replay:
            assert checker.replay_problems(deposit, receipt["rows"]) == []


def _twelve(copied: Path, lines: list[bytes]) -> checker.Deposit:
    """A deposit of a header and up to twelve rows of V2.0's table in a copy of the
    packet, with its own receipt, written plain below the gzip threshold, and no replay."""
    (copied / "source/first.csv").write_bytes(b"\r\n".join([*lines, b""]))
    return replace(
        checker.V2,
        rows=len(lines) - 1,
        table="source/first.csv",
        receipt="first.json",
        replay="",
    )


def test_a_refused_row_is_named(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A row the lemma refuses is no row: in a copy of the packet, V2.0's first twelve
    rows with 1182's V lift moved to 2, past its free length, are decided, the receipt
    keeps the refusal, and `check` names that row and nothing else. No route is asked to
    decide it in the lemma's place."""
    copied = _moved(tmp_path, monkeypatch)
    lines = (copied / checker.V2.table).read_bytes().split(b"\r\n")
    fields = lines[1].split(b",")
    fields[checker.COLUMNS.index("yV")] = b"2"
    first = _twelve(copied, [lines[0], b",".join(fields), *lines[2:13]])
    receipt = checker.decide_all(first)
    assert receipt["summary"]["refused"] == [1182]
    (problem,) = checker.check(deposits=(first,))
    assert problem.startswith(
        "V2.0 n=1182: refused by the lemma: the V lift passes its free length by "
    )


def test_an_altered_receipt_is_refused(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """In a copy of the packet, a deposit of V2.0's first twelve rows is decided and its
    receipt read back. Then each change is named: a row with another capacity, a control
    counted as not refused, a row with a field the checker does not write, a summary of
    other squares, and a header with another lemma, version, issue, report, certificates
    sentence and note (as a V1.0 receipt whose note had dropped Q-847a would be). A
    receipt missing its format and a row's count, one that is no object and one that is
    no JSON are each named, not raised. Against V2.0's own receipt, a replayed certificate
    that is not the decided one, a route that accepted a control, another sample rule and
    a replay row missing a field are named; a replay receipt that is no JSON is named; and
    so is an author-built sample naming another certificate."""
    copied = _moved(tmp_path, monkeypatch)
    lines = (copied / checker.V2.table).read_bytes().split(b"\r\n")
    first = _twelve(copied, lines[:13])
    checker.decide_all(first)
    assert first.decisions.is_file()
    assert checker.check(deposits=(first,)) == []
    receipt = checker.read_receipt(first.decisions)
    damaged = json.loads(json.dumps(receipt))
    receipt["rows"][7]["capacity"] += 1
    receipt["rows"][9]["controls_refused"] -= 1
    receipt["rows"][10]["recorded"] = True
    receipt["summary"]["squares"] += 1
    receipt["lemma"] = "another lemma"
    receipt["version"] = "V3.0"
    receipt["issue"] = checker.ISSUE_836
    receipt["reported"] = checker.V1.reported
    receipt["certificates"] = "retained"
    receipt["note"] = "every row recorded"
    first.decisions.write_text(json.dumps(receipt), encoding="utf-8")
    seventh, ninth, tenth = (receipt["rows"][index]["n"] for index in (7, 9, 10))
    drift = "issue, reported, version, lemma, note, certificates"
    assert checker.check(deposits=(first,)) == [
        f"V2.0: the decisions receipt's header is not this checker's ({drift})",
        f"V2.0 n={seventh}: the decision differs from the receipt",
        f"V2.0 n={ninth}: the decision differs from the receipt",
        f"V2.0 n={ninth}: a control was not refused by its own check",
        f"V2.0 n={tenth}: the decision differs from the receipt",
        "V2.0: the decisions summary does not match the rows",
    ]
    del damaged["format"]
    del damaged["rows"][0]["n"]
    first.decisions.write_text(json.dumps(damaged), encoding="utf-8")
    assert checker.check(deposits=(first,)) == [
        "V2.0: the decisions receipt's header is not this checker's (format)",
        "V2.0: the receipt's rows are not the records'",
    ]
    first.decisions.write_text("[]", encoding="utf-8")
    assert checker.check(deposits=(first,)) == [
        "V2.0: the decisions receipt is not an object",
        "V2.0: the receipt's rows are not the records'",
    ]
    first.decisions.write_text("{", encoding="utf-8")
    (problem,) = checker.check(deposits=(first,))
    assert problem.startswith("V2.0: the decisions receipt does not read: JSONDecodeError: ")
    stored = checker.read_receipt(checker.V2.decisions)["rows"]
    sample = json.loads(checker.V2.replay_receipt.read_text(encoding="utf-8"))
    sample["rows"][1]["certificate_sha256"] = "0" * 64
    sample["rows"][3]["controls"][0]["refused_by_independent"] = False
    del sample["rows"][4]["exact_side"]
    sample["sample_rule"]["a lift of zero"] = 1182
    checker.V2.replay_receipt.write_text(json.dumps(sample), encoding="utf-8")
    assert checker.replay_problems(checker.V2, stored) == [
        "V2.0: the replay receipt's header is not this checker's (sample_rule)",
        f"V2.0 n={checker.SAMPLE[1]}: the replayed certificate is not the decided one",
        f"V2.0 n={checker.SAMPLE[3]}: a route accepted a control",
        f"V2.0 n={checker.SAMPLE[4]}: the replay row's fields are not this checker's",
    ]
    broken = replace(first, replay="broken.json")
    checker.decide_all(broken)
    (copied / "receipts/broken.json").write_text("{", encoding="utf-8")
    (problem,) = checker.check(deposits=(broken,))
    assert problem.startswith("V2.0: the replay receipt does not read: JSONDecodeError: ")
    author = copied / checker.AUTHOR_SAMPLE
    built = json.loads(author.read_text(encoding="utf-8"))
    built["rows"][2]["certificate_bytes"] += 1
    author.write_text(json.dumps(built), encoding="utf-8")
    assert checker.author_sample_problems() == [
        "V2.0 n=4990: write_out is not the author's build"
    ]


@pytest.mark.slow
def test_v2_s_receipts_hold() -> None:
    """V2.0's receipts read back: every decision and control of its 5,134 rows derived
    again and its comparison columns counted again, 1182's and 9946's certificates written
    out again to the digests stated, the replay sample's five counts decided on both
    routes with their six controls refused, and the author-built sample written out byte
    for byte. Its decisions receipt is stored as deterministic gzip, in the packet's
    table. Every row's controls cost about 15 seconds, so this is in the slow lane; the
    quick lane decides every row once, controls aside, and reads both headers and the
    sample rows."""
    assert checker.check(deposits=(checker.V2,)) == []
    _summary_holds(checker.V2, (5134, 30445214, 4851, 7))
    assert not checker.V2.decisions.is_file()
    assert retained_data.compressed_path(checker.V2.decisions).is_file()
    assert retained_data.check_packet(checker.PACKET) == []
    sample = json.loads(checker.V2.replay_receipt.read_text(encoding="utf-8"))
    assert [row["n"] for row in sample["rows"]] == list(checker.SAMPLE)
    assert all(row["lemma"]["verdict"] == checker.DECIDED for row in sample["rows"])


@pytest.mark.slow
def test_v1_s_receipt_holds() -> None:
    """V1.0's decisions receipt reads back, every decision and control of its 4,571 rows
    derived again (about 20 CPU-seconds), labelled apart from V2.0 since Q-847a is the
    owner's."""
    assert checker.check(deposits=(checker.V1,)) == []
    _summary_holds(checker.V1, (4571, 27148903, 4034, 5))
    assert "Q-847a" in checker.read_receipt(checker.V1.decisions)["note"]


@pytest.mark.slow
def test_a_sample_count_replays_as_its_receipt_states() -> None:
    """1188, the replay sample's first count, written out and decided again on both
    routes with its six controls, is the receipt's row, timings aside."""
    stored = json.loads(checker.V2.replay_receipt.read_text(encoding="utf-8"))["rows"][0]
    assert stored["n"] == 1188
    (row,) = checker.rows_at(checker.V2, [1188])
    assert checker.stable(checker.replay_row(row)) == checker.stable(stored)


@pytest.mark.slow
@pytest.mark.parametrize("deposit", [checker.V2, checker.V1], ids=["v2", "v1"])
def test_every_written_out_certificate_has_the_digest_its_receipt_states(
    deposit: checker.Deposit,
) -> None:
    """Every certificate of a deposit written out again has the SHA-256 and size its
    decisions receipt records, which is how the record holds bytes it does not keep."""
    assert checker.decisions_problems(deposit, digests=True)[0] == []
