"""Hyukdong Kim's exact configurations for T-244 (issue 804): custody, side, both routes.

`devtools.configuration_fact_replay` reads the two configurations the
``hyukdongkim-t244-configurations-2026-10-25`` packet keeps as derived facts. This holds
each fact to the member digest the comment states, each side to T-244's, the route-1
receipts to the witness rebuilt from each fact, and the route-2 receipt to the checker
that ran and to its controls; and refuses a fact that no longer rebuilds the author's file.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import zipfile
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from devtools import configuration_fact_replay as replay

SIDE_297 = (
    replay.ROOT / "campaign/issue-intake/upper-bounds-issue804-297-20261025/review/side_297.py"
)


def test_each_fact_rebuilds_the_certificate_the_comment_pins() -> None:
    rows = replay.custody()
    assert [row["n"] for row in rows] == [172, 263]
    assert [row["field_degree"] for row in rows] == [24, 17]
    assert [row["rebuilt_bytes"] for row in rows] == [197519, 269624]


def test_each_rebuilt_file_is_the_file_the_comment_pins() -> None:
    """The custody claim the records make: each fact rebuilds the author's file, whose
    SHA-256 the comment states, and a changed configuration does not."""
    for row in replay.custody():
        assert row["rebuilt_sha256"] == row["member_sha256"]
    fact = replay.load(263)
    changed = copy.deepcopy(fact)
    changed["configuration"]["squares"][0]["x"][0] = "1/3"
    assert replay.sha256(replay.certificate_bytes(changed)) != fact["source"]["member_sha256"]


def test_route_two_ran_on_the_rebuilt_files() -> None:
    receipt = json.loads(replay.ROUTE2_RECEIPT.read_text(encoding="utf-8"))
    stated = {row["n"]: row["member_sha256"] for row in replay.custody()}
    for row in receipt["rows"]:
        assert row["positive"]["input_sha256"] == stated[row["n"]]


def test_each_side_is_t244s_and_the_receipt_says_so() -> None:
    record = replay.side_check()
    assert record["agrees"] is True
    stored = json.loads(replay.SIDE_RECEIPT.read_text(encoding="utf-8"))
    assert stored == record


def test_the_controls_mutate_what_they_name() -> None:
    data = replay.load(172)["configuration"]
    for kind in replay.CONTROLS:
        mutated, what = replay.mutate(data, kind)
        assert mutated != data
        assert what
    with pytest.raises(replay.ReplayError):
        replay.mutate(data, "unknown")


def test_route_one_receipts_hold_each_rebuilt_witness() -> None:
    for n in replay.COUNTS:
        record = replay.check_route1(n)
        assert record["cases"][0]["exact_verify"]["verification_passed"] is True


def test_route_two_accepts_both_files_and_refuses_every_control() -> None:
    summary = replay.check_route2()
    assert summary == {"positives_valid": 2, "controls_refused": 8, "controls": 8}


@pytest.mark.parametrize("kind", [None, "duplicate-square"])
def test_route_two_runs_nothing_on_a_file_that_is_not_the_stated_one(
    kind: str | None, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Finding 10 of review A on #868: the job refuses a rebuilt file whose SHA-256 is not
    the one the comment states before the checker sees it, not only in a test afterwards."""
    fact = replay.load(263)
    changed = copy.deepcopy(fact)
    changed["configuration"]["squares"][0]["x"][0] = "1/3"
    monkeypatch.setattr(replay, "load", lambda _n, _packet=replay.T244: changed)

    def never(_path: Path) -> dict[str, Any]:
        raise AssertionError("the checker ran on a file out of custody")

    monkeypatch.setattr(replay, "run_checker", never)
    with pytest.raises(replay.ReplayError, match="nothing was run"):
        replay.route2_job(263, kind, tmp_path)
    assert list(tmp_path.iterdir()) == []


# ------------------------------------------------------- T-247's configuration at 297


S297 = replay.S297


def test_the_retained_297_file_is_the_one_the_comment_pins() -> None:
    """Route B of T-247 (think-ozx8): Kim's n297.minpoly.json, kept itself since his CC0
    dedication and public copy, is the file whose SHA-256 his comment states."""
    rows = replay.custody(S297)
    assert [row["n"] for row in rows] == [297]
    assert (
        rows[0]["rebuilt_sha256"]
        == rows[0]["member_sha256"]
        == ("e5c340b8af2ff75d01b9b414e32ef19d9c3d07ecce665c8fddad9c5952252826")
    )
    assert rows[0]["field_degree"] == 21
    assert rows[0]["rebuilt_bytes"] == 347690
    sources = json.loads(S297.sources.read_text(encoding="utf-8"))
    assert sources["attachment"]["sha256"] == (
        "e08b5d0a64c5c68eed827ee7e323687929048a4cfea438bb77ef390bdd4147a7"
    )
    assert sources["attachment"]["public_copy"]["commit"] == (
        "f480441e73824668fb18779151369e4d3ba6179a"
    )
    assert all(member["retained"] for member in sources["members"])
    assert len(sources["members"]) == 6


def side_297() -> ModuleType:
    spec = importlib.util.spec_from_file_location("side_297_804", SIDE_297)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_the_297_bundle_is_kept_as_the_member_digests_name_them() -> None:
    """Finding 10 of review A on #868, as T-244's exact-forms packet's test holds its own:
    the packet keeps exactly the six members ``sources.json`` names, each at its size and
    SHA-256; the bundle's own SHA256SUMS checks; the certificate is the file the comment
    pins; and ``side_297.py derive --check`` finds the record what it would write."""
    source = S297.directory / "source"
    sources = json.loads(S297.sources.read_text(encoding="utf-8"))
    kept = sorted(p.relative_to(source).as_posix() for p in source.rglob("*") if p.is_file())
    assert kept == sorted(member["path"] for member in sources["members"])
    for member in sources["members"]:
        data = (S297.directory / member["retained_at"]).read_bytes()
        assert len(data) == member["bytes"]
        assert hashlib.sha256(data).hexdigest() == member["sha256"]
    bundle = source / "s297-exact-configuration"
    for line in (bundle / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        assert hashlib.sha256((bundle / name).read_bytes()).hexdigest() == digest
    certificate = bundle / "n297.minpoly.json"
    assert hashlib.sha256(certificate.read_bytes()).hexdigest() == (
        "e5c340b8af2ff75d01b9b414e32ef19d9c3d07ecce665c8fddad9c5952252826"
    )
    assert side_297().main(["derive", "--check"]) == 0


@pytest.mark.parametrize(
    "member",
    [
        "../escape.txt",
        "s297-exact-configuration/../../escape.txt",
        "s297-exact-configuration/..",
        "other/README.md",
        "s297-exact-configuration/sub/x.py",
    ],
)
def test_the_297_retain_refuses_a_member_outside_its_one_directory(
    member: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    program = side_297()
    certificate = S297.directory / "source/s297-exact-configuration/n297.minpoly.json"
    archive = tmp_path / "bundle.zip"
    with zipfile.ZipFile(archive, "w") as bundle:
        bundle.writestr("s297-exact-configuration/n297.minpoly.json", certificate.read_bytes())
        bundle.writestr(member, b"x")
    # Only the guard is under test: the stand-in zip is admitted as if it were pinned.
    monkeypatch.setattr(
        program, "ARCHIVE_SHA256", hashlib.sha256(archive.read_bytes()).hexdigest()
    )
    monkeypatch.setattr(program, "ARCHIVE_BYTES", archive.stat().st_size)
    with pytest.raises(SystemExit, match="outside the archive's one directory"):
        program.retain(archive, check=True)


def test_the_297_side_is_t247s_and_the_receipt_says_so() -> None:
    record = replay.side_check(S297)
    assert record["agrees"] is True
    assert record["rows"][0]["same_polynomial_as_t247"] is True
    stored = json.loads(S297.side_receipt.read_text(encoding="utf-8"))
    assert stored == record


def test_route_two_accepts_the_297_file_and_refuses_every_control() -> None:
    assert replay.check_route2(S297) == {
        "positives_valid": 1,
        "controls_refused": 4,
        "controls": 4,
    }
    receipt = json.loads(S297.route2_receipt.read_text(encoding="utf-8"))
    assert receipt["bead"] == "think-ozx8"
    stated = replay.custody(S297)[0]["member_sha256"]
    assert receipt["rows"][0]["positive"]["input_sha256"] == stated


def test_the_297_witness_names_the_public_copy() -> None:
    built = replay.witness(297, S297)
    assert built["id"] == "W-kim-t247-configuration-n297"
    assert built["source"]["url"].startswith(
        "https://github.com/HyukdongKim/square-packing-exact-sides/blob/f480441e"
    )
    assert built["source"]["path"].endswith("source/s297-exact-configuration/n297.minpoly.json")


def test_route_one_receipt_holds_the_297_witness() -> None:
    record = replay.check_route1(297, packet=S297)
    verdicts = [case["exact_verify"] for case in record["cases"]]
    assert [verdict["verification_passed"] for verdict in verdicts] == [True, False, False]
    assert [kind for verdict in verdicts[1:] for kind, _ in verdict["failures"][:1]] == [
        "overlap",
        "container",
    ]
