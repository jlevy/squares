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
import shutil
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
    its own reason: the capacity, the V fit 10^-15 short, the capacity again with a
    deeper H strip, the tilt's range twice, the H fit a whole row short, and the kind."""
    rows = checker.records()
    assert len(rows) == checker.ROWS
    for row in rows:
        assert checker.decide(row)["verdict"] == checker.DECIDED
        assert all(item["refused"] for item in checker.controls(row)), row.n
    found = {item["control"]: item["reason"] for item in checker.controls(rows[0])}
    assert list(found) == list(checker.CONTROLS)
    assert found["count above the capacity"] == "n = 1185 is above the capacity 1184"
    assert found["side below the binding fit"].startswith("the V strip")
    assert "overlaps the grid by 1.000e-15" in found["side below the binding fit"]
    assert found["H strip one row deeper"] == "n = 1184 is above the capacity 1182"
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
    }
    for reason, changed in refused.items():
        with pytest.raises(checker.TwoStripRefusedError, match=reason):
            checker.decide(changed)
    with pytest.raises(checker.TwoStripRefusedError, match="above the capacity"):
        checker.write_out(replace(row, n=row.n + 1))


def test_a_control_the_checker_would_accept_is_reported_not_passed_over() -> None:
    """The deeper H strip is refused only while the V fit is tight. Half a unit of slack
    lets a strip row of length S - wV hold the K - mV squares of the grid row it
    replaces, so the control keeps the capacity, `decide` accepts it, and `controls` says
    so rather than listing it as refused."""
    loose = replace(SMALL, tilt_h=Fraction(1, 50), tilt_v=Fraction(1, 50), rows_h=2)
    loose = replace(loose, side=checker.binding_side(loose) + Fraction(1, 2))
    loose = replace(loose, n=checker.capacity(loose))
    found = {item["control"]: item for item in checker.controls(loose)}
    assert not found["H strip one row deeper"]["refused"]
    assert found["H strip one row deeper"]["reason"] == ""
    assert all(
        item["refused"] for name, item in found.items() if name != "H strip one row deeper"
    )


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
    placed = checker.poses(lowered)
    assert len(placed) >= row.n - 1
    shrunk = base.decide(
        base.geometry(legacy.Certificate(len(placed), lowered.side, tuple(placed)))
    )
    assert "overlap" in shrunk["sqpack"]["failures"][0]
    assert "overlapping pairs" in shrunk["independent"]["failures"][0]


def test_the_receipts_hold_with_the_sample_s_digests() -> None:
    """Both receipts read back: every decision and control derived again, the five
    sample certificates written out again to the digests both receipts state, and each
    replayed on both routes with its six controls refused."""
    assert checker.check() == []
    receipt = json.loads(checker.DECISIONS.read_text(encoding="utf-8"))
    summary = receipt["summary"]
    assert (summary["rows"], summary["decided"], summary["squares"]) == (683, 683, 1749915)
    assert (summary["surplus_zero"], summary["surplus_most"]) == (403, 19)
    assert summary["side_below_k"] == summary["k_is_ceil_sqrt_n"] == 683
    assert all(item["refused"] == 683 for item in summary["controls"].values())
    sample = json.loads(checker.REPLAY.read_text(encoding="utf-8"))
    pairs = [row["decision"]["candidate_pairs"] for row in sample["rows"]]
    assert pairs == [2850, 2754, 4228, 5436, 8688]


def test_an_altered_receipt_or_packet_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A receipt row with another capacity is named, and a retained member whose bytes
    are not the captured ones fails custody before any row is read."""
    receipt = json.loads(checker.DECISIONS.read_text(encoding="utf-8"))
    receipt["rows"][5]["capacity"] += 1
    altered = tmp_path / "decisions.json"
    altered.write_text(json.dumps(receipt), encoding="utf-8")
    monkeypatch.setattr(checker, "DECISIONS", altered)
    problems = checker.check()
    n = receipt["rows"][5]["n"]
    assert f"n={n}: the decision differs from the receipt" in problems
    assert "the decisions summary does not match the rows" not in problems
    copied = tmp_path / "extracted"
    shutil.copytree(checker.EXTRACTED, copied)
    readme = copied / "README.md"
    readme.write_bytes(readme.read_bytes() + b"\n")
    monkeypatch.setattr(checker, "EXTRACTED", copied)
    with pytest.raises(checker.CustodyError, match=r"README\.md: the retained bytes"):
        checker.records()


@pytest.mark.slow
def test_a_sample_count_replays_as_its_receipt_states() -> None:
    """1184, the first count, written out and decided again on both routes with its six
    controls (about 7 CPU-seconds), is the receipt's row, timings aside."""
    stored = json.loads(checker.REPLAY.read_text(encoding="utf-8"))["rows"][0]
    assert stored["n"] == 1184
    assert checker.stable(checker.replay_row(1184)) == checker.stable(stored)


@pytest.mark.slow
def test_every_written_out_certificate_has_the_digest_its_receipt_states() -> None:
    """All 683 certificates written out again (about 8 CPU-seconds) have the SHA-256 and
    size the decisions receipt records, which is how the record holds bytes it does not
    keep."""
    assert checker.check(digests=True) == []
