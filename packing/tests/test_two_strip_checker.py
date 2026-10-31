"""The two-strip checker: #799's rows decided exactly from their parameters.

`devtools.two_strip_checker` decides a two-strip L-packing (Ryu's Theorem 1.3 shape with
independent strips) by its lemma, with no certificate. The refusals come first: every
control at every row of #799 for the reason it names, the parameters the lemma does not
state, a control the checker would accept reported as accepted, and a packet whose bytes
are not the captured ones. Then the agreements: Ryu's own packings at equal bands, and
small packings written out and decided on both exact routes of
`devtools.couzo_678_replay`, a lowered side refused by both. The receipts are read back
in the quick lane, the sample's digests among them; the replay of a sample count and
every count's digest are in the slow lane.
"""

from __future__ import annotations

import json
import re
import shutil
import warnings
import zipfile
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from cases.asymptotic import ryu_upper_l_packing as ryu
from devtools import couzo_678_replay as base
from devtools import evand_exact_certificates as legacy
from devtools import two_strip_checker as checker

#: A small packing with every phase the source uses but 0, at its binding side.
SMALL = checker.TwoStrip(
    n=1,
    side=Fraction(0),
    k=10,
    rows_h=3,
    tilt_h=Fraction(1, 8),
    phase_h=Fraction(1, 4),
    rows_v=2,
    tilt_v=Fraction(1, 9),
    phase_v=Fraction(3, 4),
)


def _small() -> checker.TwoStrip:
    """`SMALL` at its binding side and its capacity."""
    row = replace(SMALL, side=checker.binding_side(SMALL))
    return replace(row, n=checker.capacity(row))


def _ryu(k: int, b: int) -> checker.TwoStrip:
    """Ryu's Theorem 1.3 packing as a two-strip row: both strips b rows at Lemma 4.2's
    angle, tan(theta/2) = p/q, at his side k - b + b cos + sin and his count N(k, b)."""
    p = 14 * k * b * b + 1
    tilt = Fraction(p, b * p - 1)
    cos, sin = ryu.angle(k, b)
    assert checker.basis(tilt) == (cos, sin)
    return checker.TwoStrip(
        n=ryu.count(k, b),
        side=k - b + b * cos + sin,
        k=k,
        rows_h=b,
        tilt_h=tilt,
        phase_h=Fraction(0),
        rows_v=b,
        tilt_v=tilt,
        phase_v=Fraction(0),
    )


def _routes(cert: legacy.Certificate) -> tuple[bool, bool]:
    """Whether each exact route accepts a certificate: ``sqpack``'s, the independent one's."""
    result = base.decide(base.geometry(cert))
    return result["sqpack"]["passed"], result["independent"]["passed"]


def test_every_control_at_every_row_is_refused_for_the_reason_it_names() -> None:
    """At each of #799's 683 rows the seven controls are refused, and at 1184 each for
    its own reason: the capacity, the V fit 10^-15 short, the H fit a strip row's pitch
    short with both strips deeper around the same grid, the tilt's range twice, the H fit
    a whole row short, and the kind."""
    rows = checker.records()
    assert len(rows) == checker.V1.rows
    for row in rows:
        assert checker.decide(row)["verdict"] == checker.DECIDED
        assert all(item["refused"] for item in checker.controls(row)), row.n
    found = {item["control"]: item["reason"] for item in checker.controls(rows[0])}
    assert list(found) == list(checker.CONTROLS)
    assert found["count above the capacity"] == "n = 1185 is above the capacity 1184"
    assert found["side below the binding fit"].startswith("the V strip")
    assert "overlaps the grid by 1.000e-15" in found["side below the binding fit"]
    assert found["both strips one row deeper"].startswith("the H strip")
    assert "overlaps the grid by 9.194e-01" in found["both strips one row deeper"]
    assert found["no tilt"].startswith("tH = 0: ")
    assert found["a right angle"].startswith("tV = 1: ")
    assert found["grid one larger"].startswith("the H strip")
    assert "not a two-strip packing" in found["unknown kind"]


def test_parameters_the_lemma_does_not_state_are_refused() -> None:
    """Each range the lemma needs is required: a positive count and side, both tilts in
    (0, 1), each strip 1 to K - 1 rows, each phase in [0, 1), and both fit inequalities."""
    row = _small()
    assert checker.decide(row)["surplus"] == 0
    # The H strip's fit binds below the V strip's here, so each side is short of one.
    fit_h = row.k - row.rows_h + checker.thickness(row.tilt_h, row.rows_h)
    fit_v = row.k - row.rows_v + checker.thickness(row.tilt_v, row.rows_v)
    assert fit_h < fit_v == row.side
    refused = {
        "no squares to pack": replace(row, n=0),
        "is not positive": replace(row, side=Fraction(0)),
        "tV = -1/9: ": replace(row, tilt_v=-row.tilt_v),
        "tH = 9/8: ": replace(row, tilt_h=Fraction(9, 8)),
        "mH = 0: a strip has 1 to K - 1 = 9 rows": replace(row, rows_h=0),
        "mV = 10: ": replace(row, rows_v=10),
        "phH = 1: ": replace(row, phase_h=Fraction(1)),
        "phV = -1/4: ": replace(row, phase_v=Fraction(-1, 4)),
        "the H strip": replace(row, side=fit_h - checker.FIT_MARGIN),
        "the V strip": replace(row, side=fit_v - checker.FIT_MARGIN),
        "K = 1001: the checker decides 2 <= K <= 1000": replace(row, k=1001),
    }
    for reason, changed in refused.items():
        with pytest.raises(checker.TwoStripRefusedError, match=reason):
            checker.decide(changed)
    with pytest.raises(checker.TwoStripRefusedError, match="above the capacity"):
        checker.write_out(replace(row, n=row.n + 1))


def test_the_h_strip_one_row_deeper_alone_is_no_control() -> None:
    """One more H row is a genuine two-strip packing by the same lemma: its H fit loosens
    by 1 - c, so `decide` accepts it at its own capacity. At 1192 that capacity is one
    square below the row's, which says only that the row's parameters were locally better;
    with half a unit of slack it keeps the capacity, and `decide` accepts it at the
    original count. Both strips one row deeper around the same grid, the control, is
    refused at both, by the H fit."""
    row = next(row for row in checker.records() if row.n == 1192)
    deeper = replace(row, rows_h=row.rows_h + 1)
    held = checker.capacity(row)
    assert checker.capacity(deeper) == held - 1
    assert checker.decide(replace(deeper, n=held - 1))["verdict"] == checker.DECIDED
    loose = replace(SMALL, tilt_h=Fraction(1, 50), tilt_v=Fraction(1, 50), rows_h=2)
    loose = replace(loose, side=checker.binding_side(loose) + Fraction(1, 2))
    loose = replace(loose, n=checker.capacity(loose))
    assert checker.capacity(replace(loose, rows_h=loose.rows_h + 1)) == loose.n
    for case in (replace(row, n=held), loose):
        found = {item["control"]: item for item in checker.controls(case)}
        assert all(item["refused"] for item in found.values())
        assert found["both strips one row deeper"]["reason"].startswith("the H strip")


def test_a_control_the_checker_accepts_is_reported_not_passed_over() -> None:
    """Two controls are refused only while the fits are tight: the grid one larger needs
    a slack below 1, and both strips deeper a slack below a strip's c. With a full unit of
    slack in both fits each is a packing, so `decide` accepts it and `controls` says so
    rather than listing it as refused; the other five are still refused."""
    roomy = replace(SMALL, side=checker.binding_side(SMALL) + 1)
    roomy = replace(roomy, n=checker.capacity(roomy))
    found = {item["control"]: item for item in checker.controls(roomy)}
    loose = ("both strips one row deeper", "grid one larger")
    assert [(found[name]["refused"], found[name]["reason"]) for name in loose] == [
        (False, ""),
        (False, ""),
    ]
    assert all(item["refused"] for name, item in found.items() if name not in loose)


def _csv(*rows: tuple[str, ...], header: tuple[str, ...] = checker.COLUMNS) -> str:
    return "\n".join(",".join(fields) for fields in (header, *rows)) + "\n"


#: #799's first row, as records.csv states it.
FIRST = (
    "1184",
    "1745411771/50000000",
    "34.9082354200",
    "34.909679351448",
    "35",
    "7",
    "5/27",
    "0",
    "14",
    "3/29",
    "0",
)


def test_the_ingest_refuses_every_malformed_deposit_as_custody() -> None:
    """`parse_records` reads a deposit as untrusted data and refuses, as a
    `CustodyError` and never a bare KeyError, TypeError or ValueError: a duplicated,
    missing or extra column; a short, long or blank row; a K above the checker's bound
    (10^12 with n = 1) or not ceil(sqrt(n)); a literal past `MAX_DIGITS`, one of 5,000
    digits, and a malformed comparison column; a decimal side that is not the exact
    side; a count given twice; and a field past the csv module's size limit. The row
    reader refuses a missing field and a field that is not text. #799's first row, as
    stated, parses."""
    assert checker.parse_records(_csv(FIRST)) == [checker.records()[0]]

    def changed(index: int, value: str) -> tuple[str, ...]:
        return (*FIRST[:index], value, *FIRST[index + 1 :])

    refused = {
        "the header is": _csv((*FIRST, "1/2"), header=(*checker.COLUMNS, "tV")),
        "the header is ": _csv(FIRST[:-1], header=checker.COLUMNS[:-1]),
        "row 1: 10 fields, not 11": _csv(FIRST[:-1]),
        "row 1: 12 fields, not 11": _csv((*FIRST, "")),
        "row 2: 0 fields, not 11": _csv(FIRST, (), changed(0, "1186")),
        "K = 1000000000000 is above the checker's bound 1000": _csv(
            (
                "1",
                "999999999999/1",
                "999999999999.0",
                "1.0",
                "1000000000000",
                "1",
                "1/10",
                "0",
                "1",
                "1/10",
                "0",
            )
        ),
        "K = 36 is not ceil": _csv(changed(4, "36")),
        "'1745411771/1" + "0" * 30 + "' is not the literal": _csv(
            changed(1, "1745411771/1" + "0" * 30)
        ),
        "is not the literal": _csv(changed(6, "1/" + "7" * 5000)),
        "'none' is not the literal": _csv(changed(3, "none")),
        "the decimal side is not the exact side": _csv(changed(2, "34.9082354201")),
        "a count appears in more than one row": _csv(FIRST, FIRST),
        "field larger than field limit": _csv(changed(9, "1" * 200_000)),
    }
    for reason, text in refused.items():
        with pytest.raises(checker.CustodyError, match=re.escape(reason)):
            checker.parse_records(text)
    item: dict[str, object] = dict(zip(checker.COLUMNS, FIRST, strict=True))
    for broken in ({**item, "tV": None}, {key: item[key] for key in checker.COLUMNS[1:]}):
        with pytest.raises(checker.CustodyError, match=r"records\.csv n="):
            checker.row_from_record(broken)


def test_version_5_is_read_through_its_own_column_set() -> None:
    """#836's version 5 adds the author's ``below_all_reported`` after the eleven
    columns. Read with its own header it parses, the flag counted and decided by nothing;
    read as #799's deposits are, its header is refused. An author's column must hold one
    of its literals, and a column the checker does not know, or the eleven out of order,
    is refused as custody. Its 5,308 rows are version 2's at 1,390 counts, side and
    parameters alike, lower at 1,434 and new at 2,484, as #836 states; none is higher."""
    flagged = checker.V5.header
    assert flagged == (*checker.COLUMNS, "below_all_reported")
    rows = checker.parse_table(_csv((*FIRST, "no"), header=flagged), flagged)
    assert rows == [(checker.parse_records(_csv(FIRST))[0], {"below_all_reported": "no"})]
    refused = {
        "the header is": (_csv((*FIRST, "no"), header=flagged), checker.COLUMNS),
        "below_all_reported 'maybe' is not one of": (
            _csv((*FIRST, "maybe"), header=flagged),
            flagged,
        ),
        "the checker reads no records.csv with columns": (
            _csv((*FIRST, "x"), header=(*checker.COLUMNS, "comment")),
            (*checker.COLUMNS, "comment"),
        ),
        "the checker reads no records.csv with columns ": (
            _csv(FIRST, header=checker.COLUMNS[::-1]),
            checker.COLUMNS[::-1],
        ),
    }
    for reason, (text, columns) in refused.items():
        with pytest.raises(checker.CustodyError, match=re.escape(reason.strip())):
            checker.parse_table(text, columns)
    assert checker.author_flags(checker.V5) == {"below_all_reported": {"no": 51, "yes": 5257}}
    version_2 = {row.n: row for row in checker.records(checker.V2)}
    version_5 = {row.n: row for row in checker.records(checker.V5)}
    assert len(version_5) == checker.V5.rows == 5308
    shared = set(version_5) & set(version_2)
    assert len(set(version_5) - set(version_2)) == 2484
    assert sum(version_5[n] == version_2[n] for n in shared) == 1390
    assert sum(version_5[n].side < version_2[n].side for n in shared) == 1434
    assert not any(version_5[n].side > version_2[n].side for n in shared)


def test_a_deposit_kept_as_its_archive_is_read_as_untrusted_data(tmp_path: Path) -> None:
    """Version 5 is read from the author's copy of its archive, retained in Git, whose
    custody is the packet's (`acquire_source --check`), so no digest is compared here.
    The archive is still another party's: one holding ``records.csv`` twice or none, a
    member past `MAX_RECORDS_BYTES`, bytes that are no archive, and an archive whose table
    holds another number of rows are each refused as custody."""
    assert len(checker.records(checker.V5)) == 5308

    def archive(name: str, members: dict[str, bytes]) -> checker.Deposit:
        with zipfile.ZipFile(tmp_path / name, "w") as written:
            for member, data in members.items():
                written.writestr(member, data)
        return replace(checker.V5, packet=str(tmp_path), archived=name)

    flagged = _csv((*FIRST, "yes"), header=checker.V5.header).encode()
    small = archive("one.zip", {"records.csv": flagged, "README.md": b"x"})
    assert checker.archived_records(small) == flagged.decode()
    with pytest.raises(checker.CustodyError, match="holds 1 rows, not 5308"):
        checker.records(small)
    with pytest.raises(checker.CustodyError, match=re.escape("holds 0 records.csv")):
        checker.archived_records(archive("none.zip", {"README.md": b"x"}))
    with zipfile.ZipFile(tmp_path / "twice.zip", "w") as written, warnings.catch_warnings():
        warnings.simplefilter("ignore")
        written.writestr("records.csv", flagged)
        written.writestr("records.csv", flagged)
    with pytest.raises(checker.CustodyError, match=re.escape("holds 2 records.csv")):
        checker.archived_records(replace(small, archived="twice.zip"))
    large = archive("large.zip", {"records.csv": b"0" * (checker.MAX_RECORDS_BYTES + 1)})
    with pytest.raises(checker.CustodyError, match=re.escape("records.csv is too large")):
        checker.archived_records(large)
    (tmp_path / "plain.zip").write_bytes(b"not an archive")
    with pytest.raises(checker.CustodyError, match="File is not a zip file"):
        checker.archived_records(replace(small, archived="plain.zip"))


def test_write_out_builds_no_square_past_n() -> None:
    """At K = 1000, the checker's bound, the construction holds about a million squares;
    written out at n = 1 it builds one, since `poses` places them one at a time."""
    row = replace(SMALL, k=checker.MAX_K, rows_h=1, rows_v=1)
    row = replace(row, side=checker.binding_side(row))
    assert checker.capacity(row) > 990_000
    cert = checker.write_out(row)
    assert len(cert.poses) == 1
    assert cert.poses[0] == next(checker.poses(row))


def test_ryu_s_theorem_1_3_packings_are_decided_at_his_count() -> None:
    """At Ryu's parameters, equal bands at Lemma 4.2's angle, the lemma's capacity is at
    least his N(k, b) for every 2 <= b < k <= 40, at his side, which is below k; it is
    equal at 15 pairs and larger at the rest, since each strip row is filled to its end.
    The packing written out at k = 8, b = 3 passes both exact routes."""
    equal = larger = 0
    for k in range(3, 41):
        for b in range(2, k):
            row = _ryu(k, b)
            found = checker.decide(row)
            assert found["side_below_k"]
            equal += found["capacity"] == row.n
            larger += found["capacity"] > row.n
    assert (equal, larger) == (15, 726)
    assert _routes(checker.write_out(_ryu(8, 3))) == (True, True)


def test_a_small_packing_written_out_agrees_with_both_routes() -> None:
    """A packing with phases 1/4 and 3/4, written out at its binding side and capacity,
    passes both exact routes and their six controls are refused by both. Written out
    10^-15 below that side, past what `decide` accepts, the strip meets the grid, and
    both routes refuse it too."""
    row = _small()
    cert = checker.write_out(row)
    assert (cert.n, cert.side) == (row.n, row.side)
    assert _routes(cert) == (True, True)
    assert all(
        item["refused_by_sqpack"] and item["refused_by_independent"]
        for item in base.decide_controls(cert)
    )
    lowered = replace(row, side=row.side - checker.FIT_MARGIN)
    with pytest.raises(checker.TwoStripRefusedError, match="overlaps the grid"):
        checker.decide(lowered)
    placed = list(checker.poses(lowered))
    assert len(placed) >= row.n - 1
    shrunk = base.decide(
        base.geometry(legacy.Certificate(len(placed), lowered.side, tuple(placed)))
    )
    assert "overlap" in shrunk["sqpack"]["failures"][0]
    assert "overlapping pairs" in shrunk["independent"]["failures"][0]


def _summary_holds(deposit: checker.Deposit, expected: tuple[int, int, int, int]) -> None:
    """A deposit's decisions summary: every row decided, its squares, how many rows are
    filled to the capacity and the most surplus, and every control refused at every row."""
    rows, squares, tight, most = expected
    summary = json.loads(deposit.decisions.read_text(encoding="utf-8"))["summary"]
    assert (summary["rows"], summary["decided"], summary["squares"]) == (rows, rows, squares)
    assert (summary["surplus_zero"], summary["surplus_most"]) == (tight, most)
    assert summary["side_below_k"] == summary["k_is_ceil_sqrt_n"] == rows
    assert all(item["refused"] == rows for item in summary["controls"].values())


def test_version_5_s_receipts_hold() -> None:
    """Version 5's two receipts read back: every decision and control of its 5,308 rows
    derived again and its author's column counted again (51 no, 5,257 yes), 1182's and
    9912's certificates written out again to the digests stated, and the replay sample's
    five counts decided on both routes with their six controls refused."""
    assert checker.check(deposits=(checker.V5,)) == []
    _summary_holds(checker.V5, (5308, 31499439, 4618, 4))
    sample = json.loads(checker.replay_path(checker.V5).read_text(encoding="utf-8"))
    assert [row["n"] for row in sample["rows"]] == [1182, 1253, 6089, 9912, 9944]
    pairs = [row["decision"]["candidate_pairs"] for row in sample["rows"]]
    assert pairs == [2766, 2895, 13869, 22246, 22513]


def test_the_receipts_hold_with_the_sample_s_digests() -> None:
    """#799's three receipts read back: every decision and control of both deposits
    derived again; the sample certificates written out again to the digests the receipts
    state, the five of version 1, which are also version 2's rows there, and version 2's
    2459 and 9944; and the five replayed on both routes with their six controls refused."""
    assert checker.check(deposits=(checker.V1, checker.V2)) == []
    _summary_holds(checker.V1, (683, 1749915, 403, 19))
    _summary_holds(checker.V2, (2824, 16603112, 1366, 42))
    first = {row.n: row for row in checker.records(checker.V1)}
    later = {row.n: row for row in checker.records(checker.V2)}
    changed = sorted(n for n, row in first.items() if later[n] != row)
    assert changed == [2459]
    assert later[2459].side == first[2459].side - Fraction(4, 10**8)
    assert all(later[n] == first[n] for n in checker.SAMPLE)
    sample = json.loads(checker.replay_path().read_text(encoding="utf-8"))
    pairs = [row["decision"]["candidate_pairs"] for row in sample["rows"]]
    assert pairs == [2850, 2754, 4228, 5436, 8688]


def test_an_altered_receipt_or_packet_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """In a copy of the packet, a receipt row with another capacity is named, in either
    deposit; a replayed certificate that is not the one the decisions receipt names is
    refused; and a deposit's files keeping one its capture does not name fail custody
    before any row is read."""
    copied = tmp_path / "packet"
    shutil.copytree(checker.PACKET, copied)
    monkeypatch.setattr(checker, "PACKET", copied)
    for deposit, index in ((checker.V1, 5), (checker.V2, 2000)):
        receipt = json.loads(deposit.decisions.read_text(encoding="utf-8"))
        receipt["rows"][index]["capacity"] += 1
        deposit.decisions.write_text(json.dumps(receipt), encoding="utf-8")
    sample = json.loads(checker.replay_path().read_text(encoding="utf-8"))
    sample["rows"][2]["certificate_sha256"] = "0" * 64
    checker.replay_path().write_text(json.dumps(sample), encoding="utf-8")
    first = json.loads(checker.V1.decisions.read_text(encoding="utf-8"))["rows"][5]["n"]
    later = json.loads(checker.V2.decisions.read_text(encoding="utf-8"))["rows"][2000]["n"]
    assert checker.check(deposits=(checker.V1, checker.V2)) == [
        f"V1.0 n={first}: the decision differs from the receipt",
        "V1.0 n=1813: the replayed certificate is not the decided one",
        f"version 2 n={later}: the decision differs from the receipt",
    ]
    (checker.V2.extracted / "regenerate.py").write_text("", encoding="utf-8")
    with pytest.raises(checker.CustodyError, match="the packet keeps"):
        checker.records(checker.V2)
    assert len(checker.records(checker.V1)) == 683


@pytest.mark.slow
def test_a_sample_count_replays_as_its_receipt_states() -> None:
    """1184, the first count, written out and decided again on both routes with its six
    controls (about 8 CPU-seconds), is the receipt's row, timings aside."""
    stored = json.loads(checker.replay_path().read_text(encoding="utf-8"))["rows"][0]
    assert stored["n"] == 1184
    assert checker.stable(checker.replay_row(1184)) == checker.stable(stored)


@pytest.mark.slow
@pytest.mark.parametrize("deposit", [checker.V1, checker.V2], ids=["v1", "v2"])
def test_every_written_out_certificate_has_the_digest_its_receipt_states(
    deposit: checker.Deposit,
) -> None:
    """Every certificate of a deposit written out again, 683 in about 8 CPU-seconds and
    2,824 in about 70, has the SHA-256 and size its decisions receipt records, which is
    how the record holds bytes it does not keep. Version 5's 5,308 would take about 200
    (its decide-all took 212.9 with every control), so this lane leaves them to
    ``check --digests`` and the quick check writes its sample's two again."""
    assert checker.decisions_problems(deposit, digests=True)[0] == []
