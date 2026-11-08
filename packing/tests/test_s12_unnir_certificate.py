"""The import of jlevy/squares#924: unnir's ``s(12) >= 9929/2500`` certificate.

unnir (Numaro) reports ``s(12) >= 9929/2500`` from a new weighted cover of 4,996 points
in Evan Daniel's format. These tests hold what was decided here:

- the exact preflight, re-run from the retained bytes, passes every check and equals its
  retained receipt, and finds a pose of bin 39531 capturing exactly one;
- three checkers accepted the certificate at ``N = 96000``: Daniel's ``verify`` built
  with overflow checks and Ryu Sungjoon's ``indep_scan.cpp`` (both the producer's code,
  run here), each printing the source's own lines, and this repository's native
  parent-core branch and bound (first party), every row of it;
- the four controls, regenerated here and pinned by digest, were refused by each checker
  that ran them; and
- the native case is pinned to the certificate the issue names.

They read receipts and retained files only; nothing here compiles or runs a checker.
"""

from __future__ import annotations

import hashlib
import json
import re
from fractions import Fraction
from functools import cache
from pathlib import Path
from typing import Any

import pytest

from devtools import audit_s12_unnir_certificate as preflight
from devtools import verify_evand_angle_net_native as native
from devtools.retained_data import read_retained_text

RECEIPTS = preflight.PACKET / "receipts"
CONTROLS = RECEIPTS / "controls"
LOGS = preflight.SOURCE / "verification"
W = 9_985_226
#: The controls a coverage checker must refuse; ``truncated`` is refused by every parser.
COVERAGE_CONTROLS = ("double-denominator", "lowered-tight-orbit", "regrid-3999600")


@cache
def audit() -> dict[str, Any]:
    return preflight.audit()


@cache
def control_digests() -> dict[str, str]:
    _, cert = preflight.read(preflight.CERTIFICATE, preflight.CERTIFICATE_SHA256)
    pose = preflight.tight_pose(cert)
    return {
        name: hashlib.sha256(data).hexdigest()
        for name, data in preflight.control_bytes(cert, pose).items()
    }


def _lines(path: Path) -> list[str]:
    return read_retained_text(path).splitlines()


def _body(path: Path) -> str:
    return "\n".join(line for line in _lines(path) if not line.startswith("# "))


def _footer(path: Path) -> str:
    return _lines(path)[-1]


def test_preflight_passes_every_exact_check_and_equals_its_receipt() -> None:
    result = audit()
    assert result["status"] == "PASS"
    assert all(result["checks"].values()), result["checks"]
    retained = json.loads((RECEIPTS / "preflight.json").read_text(encoding="utf-8"))
    assert retained == result
    assert result["side"] == "9929/2500"
    assert result["advance_over_t095"] == "1/10000"
    assert result["total_weight"] == f"119787760/{W}"
    assert result["points"] == 4996
    assert result["orbits"] == 636
    pose = result["tight_pose"]
    assert pose["bin"] == preflight.TIGHT_BIN == 39531
    assert pose["least_capture"] == f"{W}/{W}"
    assert pose["unit_square_fits"] is True


def test_the_certificate_is_the_one_the_issue_names() -> None:
    assert preflight.CERTIFICATE_SHA256 == (
        "833b76a179a420a40775cc76305ec9ffb7f6ea27472e587958c234c4c4712cbd"
    )
    case = native.CASES["s12-unnir"]
    assert case.sha256 == preflight.CERTIFICATE_SHA256
    assert case.path == preflight.CERTIFICATE
    assert (case.n, case.net, case.source_bin) == (12, 96000, 39531)
    assert case.source_minimum == f"{W}/{W}"
    assert case.source_commit == "064c2955670765321aaf1c0a2d5c778949daab6b"


def test_each_control_has_the_digest_its_receipts_name() -> None:
    digests = control_digests()
    assert set(digests) == set(preflight.CONTROLS)
    for name, digest in digests.items():
        assert audit()["controls"][name]["sha256"] == digest
        for path in CONTROLS.glob(f"*-{name}*.log"):
            if path.name.startswith("native-"):
                continue
            assert digest[:8] in _lines(path)[1], path
        receipt = CONTROLS / f"native-{name}.json"
        if receipt.exists():
            data = json.loads(receipt.read_text(encoding="utf-8"))
            assert data["provenance"]["certificate_sha256"] == digest


def test_the_lowered_orbit_control_must_be_refused() -> None:
    """The tight pose captures two of the lowered orbit's points, and captured exactly W."""
    lowered = audit()["controls"]["lowered-tight-orbit"]
    assert lowered["orbit_points_captured_at_tight_pose"] == 2
    assert lowered["tight_pose_capture"] == f"{W - 2}/{W}"
    assert all(point[2] > 1 for point in lowered["orbit_points"])


def test_the_source_controls_reproduce_the_sources_logs() -> None:
    pairs = {
        "daniel-verify-double-denominator-bin-39531.log": "double-denominator-rust.log",
        "indep-scan-double-denominator-bin-39531.log": "double-denominator-cpp.log",
        "daniel-verify-truncated-bin-39531.log": "truncated-rust.log",
        "indep-scan-truncated-bin-39531.log": "truncated-cpp.log",
    }
    for ours, theirs in pairs.items():
        assert (
            _body(CONTROLS / ours).strip()
            == read_retained_text(LOGS / "controls" / theirs).strip()
        ), ours


def _stats(line: str) -> dict[str, str]:
    return dict(re.findall(r"(\w+)=([\w./]+)", line))


def test_daniels_verifier_with_overflow_checks_accepts_at_96000() -> None:
    path = RECEIPTS / "daniel-verify-ovf-N96000.log"
    header = _lines(path)[1]
    assert "CARGO_PROFILE_RELEASE_OVERFLOW_CHECKS=true" in header
    assert "VERIFY_STATS=1 and no other VERIFY_ or TIGHT_ variable" in header
    body = _body(path)
    assert "D4-symmetric atom set: true" in body
    assert "angles: k=0..39765 (N=96000)" in body
    assert f"min covered weight over ALL placements = {W}/{W}" in body
    assert "(at angle k=39531)" in body
    assert "VERIFIED: every CLOSED unit square inside C covers weight >= 1" in body
    for refusal in ("FAIL", "NOT VERIFIED", "PARTIAL"):
        assert refusal not in body
    assert "exit 0" in _footer(path)
    # Every line but the timing statistics is the source's; the work counted is equal.
    log = read_retained_text(LOGS / "logs/rust.log")
    ours = [line for line in body.splitlines() if not line.startswith("VERIFY_STATS")]
    theirs = [line for line in log.splitlines() if not line.startswith("VERIFY_STATS")]
    assert ours == theirs
    (mine,) = [line for line in body.splitlines() if line.startswith("VERIFY_STATS atoms")]
    (source,) = [line for line in log.splitlines() if line.startswith("VERIFY_STATS atoms")]
    for key in ("atoms", "bins", "strips", "cells", "active"):
        assert _stats(mine)[key] == _stats(source)[key], key
    swept = [int(v) for v in re.findall(r"swept (\d+) bins", body)]
    assert sum(swept) == 39765


def test_the_reporters_checker_sweeps_every_bin_and_matches_its_log() -> None:
    path = RECEIPTS / "indep-scan-N96000.log"
    command = _lines(path)[0]
    assert command.endswith("s12_lower_3.9716.txt 96000 1000000000000000 12")
    body = _body(path)
    assert "bins k = 0..95999 covering [0,90] deg (no symmetry assumed)" in body
    assert f"min captured weight over all bins = {W}/{W}" in body
    assert body.splitlines()[-1].startswith("VERIFIED")
    assert "exit 0" in _footer(path)
    assert body.strip() == read_retained_text(LOGS / "logs/cpp.log").strip()


@cache
def native_receipt() -> dict[str, Any]:
    return json.loads(read_retained_text(RECEIPTS / "native-parent-core-N96000.json"))


def test_the_native_decision_is_complete_on_a_clean_tree() -> None:
    receipt = native_receipt()
    assert receipt["status"] == "PASS_COMPLETE"
    assert receipt["case"] == "s12-unnir"
    assert receipt["net"] == 96000
    assert receipt["points"] == 4996
    assert receipt["complete"] is True
    assert receipt["refutations"] == []
    assert receipt["provenance"]["dirty"] is False
    assert receipt["provenance"]["certificate_sha256"] == preflight.CERTIFICATE_SHA256
    status = _lines(RECEIPTS / "native-parent-core-N96000.git-status.txt")
    assert status == [f"# HEAD {receipt['provenance']['git_commit']}"]
    assert receipt["catalogue_rows"] == len(native.net_rows(96000)) == 39765
    lines = read_retained_text(RECEIPTS / "native-parent-core-N96000.rows.jsonl").splitlines()
    rows = [json.loads(line) for line in lines[1:]]
    assert sorted(r["index"] for r in rows) == list(range(receipt["catalogue_rows"]))
    for row in rows:
        assert row["status"] == "certified"
        assert row["stalled"] == 0
        assert not row["budget_exhausted"]
        assert int(row["lower"]) >= receipt["threshold_units"]


@pytest.mark.parametrize("name", COVERAGE_CONTROLS)
def test_every_checker_refuses_each_coverage_control(name: str) -> None:
    indep = sorted(CONTROLS.glob(f"indep-scan-{name}*.log"))
    assert indep
    for path in indep:
        body = _body(path)
        assert body.splitlines()[-1] == "NOT VERIFIED"
        least = re.search(r"min captured weight over all bins = (\d+)/(\d+)", body)
        assert least is not None
        assert Fraction(int(least.group(1)), int(least.group(2))) < 1
        assert "exit 1" in _footer(path)

    daniel = sorted(CONTROLS.glob(f"daniel-verify-{name}-bin-*.log"))
    assert daniel
    for path in daniel:
        body = _body(path)
        fails = re.findall(r"FAIL at angle k=\d+: covered (\d+)/(\d+)", body)
        assert fails
        assert all(Fraction(int(a), int(b)) < 1 for a, b in fails)
        assert "NOT VERIFIED" in body
        assert "\nVERIFIED" not in body

    receipt = json.loads((CONTROLS / f"native-{name}.json").read_text(encoding="utf-8"))
    assert receipt["status"] == "UNRESOLVED"
    assert receipt["case"] == "s12-unnir"
    assert receipt["provenance"]["certificate_sha256"] != preflight.CERTIFICATE_SHA256
    assert any(row["status"] == "refuted" for row in receipt["rows"])
    witnesses = receipt["refutations"]
    assert witnesses
    assert all(w["admissible"] and Fraction(w["charge"]) < 1 for w in witnesses)


def test_every_parser_refuses_the_truncated_control() -> None:
    for name in ("daniel-verify-truncated-bin-39531.log", "indep-scan-truncated-bin-39531.log"):
        assert "ERROR:" in _body(CONTROLS / name)
        assert "exit 2" in _footer(CONTROLS / name)
    native_log = read_retained_text(CONTROLS / "native-truncated.log")
    assert "ValueError: point count does not match the file" in native_log
