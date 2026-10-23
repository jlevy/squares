"""Evan Daniel's own checkers, run on the certificates of issues #669 and #674.

`devtools.evand_source_checkers` runs the source's retained `verify_cert.py` and
`verify_cert2.py` on the four certificates of the three packets and on four controls of
each, and keeps every outcome in the packets' receipts. These hold the receipts to the
packets as retained, each control to the defect it names, the reading of a verdict to the
checkers' own words, and the harness to the checkers themselves on a two-square packing
and its controls.
"""

from __future__ import annotations

import copy
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import evand_exact_certificates as legacy
from devtools import evand_source_checkers as checkers

N229 = "evand-n229-dilation-2026-10-17"
FIRST, SECOND = checkers.CHECKERS


def _certificates() -> list[tuple[str, str]]:
    return [(name, path) for name, paths in checkers.PACKETS.items() for path in paths]


def _receipt(name: str) -> dict[str, Any]:
    path = checkers.packet_dir(name) / checkers.RECEIPT
    return json.loads(path.read_text(encoding="utf-8"))


def test_the_committed_receipts_hold_against_the_retained_packets() -> None:
    assert checkers.check() == []


def test_every_certificate_was_accepted_by_both_checkers_and_every_control_refused() -> None:
    runs = 0
    for name in checkers.PACKETS:
        for row in _receipt(name)["rows"]:
            for checker in checkers.CHECKERS:
                outcome = row["runs"][checker]
                assert checkers.accepted(checker, outcome["positive"])
                assert all(map(checkers.refused, outcome["controls"].values()))
                runs += 1 + len(outcome["controls"])
    assert runs == 4 * 2 * (1 + len(checkers.CONTROLS))


@pytest.mark.parametrize(("name", "path"), _certificates())
def test_each_control_breaks_the_packing_in_the_way_it_names(name: str, path: str) -> None:
    retained = checkers.packet_dir(name) / "source" / path
    certificate = legacy.parse(retained.read_text(encoding="utf-8"))
    assert checkers.far_wall_clearance(certificate) > 0

    duplicate = checkers.control(certificate, "duplicate-square")
    assert duplicate.poses[1] == duplicate.poses[0] == certificate.poses[0]
    assert duplicate.poses[2:] == certificate.poses[2:]

    outside = checkers.control(certificate, "square-outside")
    moved = outside.poses[0]
    assert moved.x - checkers.half_extent(moved) > outside.side
    assert outside.poses[1:] == certificate.poses[1:]

    sharp = checkers.control(certificate, "sharp-far-wall")
    assert sharp.poses == certificate.poses
    assert checkers.far_wall_clearance(sharp) == -checkers.SHARP
    assert checkers.near_wall_clearance(sharp) == checkers.near_wall_clearance(certificate)
    assert certificate.side - sharp.side < Fraction(1, 10**11)

    near = checkers.control(certificate, "sharp-near-wall")
    assert near.side == certificate.side
    assert checkers.near_wall_clearance(near) == -checkers.SHARP
    assert checkers.wall_clearance(near) == -checkers.SHARP
    shift = checkers.near_wall_clearance(certificate) + checkers.SHARP
    assert all(
        (moved.x, moved.y, moved.t) == (pose.x - shift, pose.y - shift, pose.t)
        for moved, pose in zip(near.poses, certificate.poses, strict=True)
    )
    assert shift < Fraction(1, 10**11)


def test_an_unknown_control_is_refused() -> None:
    certificate = legacy.parse("2 4\n1 2 0\n3 2 0\n")
    with pytest.raises(ValueError, match="no control named"):
        checkers.control(certificate, "shrunk")


def test_acceptance_is_each_checkers_own_word_and_refusal_a_verdict_not_a_crash() -> None:
    valid = {"exit_status": 0, "stdout": ["n = 2", "VALID: s(n) <= S"]}
    assert checkers.accepted(FIRST, valid)
    assert not checkers.accepted(FIRST, {"exit_status": 0, "stdout": ["INVALID"]})
    assert not checkers.accepted(FIRST, {**valid, "exit_status": 1})
    assert checkers.accepted(SECOND, {"exit_status": 0, "stdout": ["VALID: 2 closed"]})
    assert checkers.refused({"exit_status": 1, "stdout": ["INVALID: corner outside"]})
    assert not checkers.refused({"exit_status": 1, "stdout": [], "stderr": "Traceback"})
    assert not checkers.refused({"exit_status": 0, "stdout": ["INVALID"]})


def test_the_retained_checkers_accept_a_packing_and_refuse_each_of_its_controls(
    tmp_path: Path,
) -> None:
    # Two unit squares in a box of side 4, the second turned by t = 1/3 (c, s = 4/5, 3/5).
    certificate = legacy.parse("2 4\n1 2 0\n13/5 2 1/3\n")
    positive = tmp_path / "pair.cert"
    positive.write_text(legacy.serialize(certificate), encoding="utf-8")
    source = checkers.packet_dir(N229) / "source"
    cwd = tmp_path / "cwd"
    cwd.mkdir()
    for checker in checkers.CHECKERS:
        result = checkers.run_checker(source / checker, positive, cwd=cwd)
        assert checkers.accepted(checker, result)
        for kind in checkers.CONTROLS:
            mutant = tmp_path / f"pair-{kind}.cert"
            mutant.write_text(checkers.control_text(certificate, kind), encoding="utf-8")
            refusal = checkers.run_checker(source / checker, mutant, cwd=cwd)
            assert checkers.refused(refusal), kind
    assert list(cwd.iterdir()) == []


def test_the_child_gets_no_environment_no_stdin_and_a_scratch_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Review A6 of #747: `-I` does not drop the parent's environment, which in CI holds
    tokens, nor its working directory or standard input."""
    monkeypatch.setenv("SQUARES_TEST_TOKEN", "secret")
    probe = tmp_path / "probe.py"
    probe.write_text(
        "import os, sys\n"
        "print(sorted(k for k in os.environ if k != 'LC_CTYPE'))\n"
        "print(os.getcwd())\n"
        "print(repr(sys.stdin.read()))\n",
        encoding="utf-8",
    )
    cwd = tmp_path / "scratch"
    cwd.mkdir()
    result = checkers.run_checker(probe, tmp_path / "unused.cert", cwd=cwd)
    assert result["exit_status"] == 0, result["stderr"]
    assert result["stdout"] == ["[]", str(cwd), "''"]
    with pytest.raises(ValueError, match="absolute paths"):
        checkers.run_checker(Path("probe.py"), tmp_path / "unused.cert", cwd=cwd)


def test_each_receipt_names_the_retained_files_and_the_controls_the_tool_builds() -> None:
    """What ran: the digests a receipt records, for its reader, are the retained
    checkers' and certificates', and each control's is the control rebuilt now."""
    for name, paths in checkers.PACKETS.items():
        receipt = _receipt(name)
        source = checkers.packet_dir(name) / "source"
        assert receipt["checkers"] == {
            c: checkers.sha256(source / c) for c in checkers.CHECKERS
        }
        for row, path in zip(receipt["rows"], paths, strict=True):
            certificate = legacy.parse((source / path).read_text(encoding="utf-8"))
            assert row["sha256"] == checkers.sha256(source / path)
            assert row["n"] == certificate.n
            assert {kind: entry["sha256"] for kind, entry in row["controls"].items()} == {
                kind: checkers.text_sha256(checkers.control_text(certificate, kind))
                for kind in checkers.CONTROLS
            }


def test_a_receipt_that_misses_a_run_or_misstates_an_outcome_is_refused() -> None:
    receipt = _receipt(N229)
    assert checkers.receipt_problems(N229, receipt) == []

    one_checker = copy.deepcopy(receipt)
    del one_checker["checkers"][FIRST]
    del one_checker["rows"][0]["runs"][FIRST]
    found = checkers.receipt_problems(N229, one_checker)
    assert any("two checkers" in p for p in found)
    assert any("did not run" in p for p in found)

    unaccepted = copy.deepcopy(receipt)
    unaccepted["rows"][0]["runs"][FIRST]["positive"]["exit_status"] = 1
    assert any("did not accept" in p for p in checkers.receipt_problems(N229, unaccepted))

    unrefused = copy.deepcopy(receipt)
    unrefused["rows"][0]["runs"][SECOND]["controls"]["sharp-near-wall"]["exit_status"] = 0
    assert any("did not refuse" in p for p in checkers.receipt_problems(N229, unrefused))

    # Review A7 of #747: a malformed row is a problem line, not a KeyError.
    runless = copy.deepcopy(receipt)
    del runless["rows"][0]["runs"]
    assert any("records no runs" in p for p in checkers.receipt_problems(N229, runless))
    no_positive = copy.deepcopy(receipt)
    del no_positive["rows"][0]["runs"][FIRST]["positive"]
    found = checkers.receipt_problems(N229, no_positive)
    assert any(f"{FIRST} records no positive run" in p for p in found)
    bare = copy.deepcopy(receipt)
    del bare["rows"][0]["runs"][SECOND]["controls"]
    del bare["rows"][0]["runs"][SECOND]["positive"]["stdout"]
    found = checkers.receipt_problems(N229, bare)
    assert any(f"{SECOND} did not accept" in p for p in found)
    assert sum("did not refuse" in p for p in found) == len(checkers.CONTROLS)

    uncontrolled = copy.deepcopy(receipt)
    del uncontrolled["rows"][0]["controls"]["duplicate-square"]
    found = checkers.receipt_problems(N229, uncontrolled)
    assert any("records no duplicate-square control" in p for p in found)

    short = copy.deepcopy(receipt)
    short["rows"] = []
    assert any("exactly" in p for p in checkers.receipt_problems(N229, short))
