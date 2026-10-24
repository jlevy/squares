"""The mechanisms that let the record decide rows above n = 1024 (think-llit's plan, W7).

W7 records nothing: every release keeps the window it was recorded with, every frozen walk
its reach and its rulings through 1024, and every receipt, frozen walk and claims record
rebuilds byte for byte (`test_beyond_horizon_replay.py` holds each to its rebuild). These
tests hold the mechanisms a records slice uses above 1024, negative controls first:

- a frozen release asked to decide a claim above its window is refused;
- a walk above 1024 whose rulings stop at 1024 fails `devtools.intake_ledger.answer_problems`;
- a deletion of two squares above 1024 is not settled by the D6 answer and stays held on
  think-kzme;
- a Kingbird catalogue side declared as a row before N1 is answered is refused;
- a recipe row with no decision, or one that differs from its derivation, is refused;
- the fast check reads a hosted row's side and blob without opening a shard, and
  ``source-history`` above 1024 reads the retained commit's files from the shards, each
  held to the clone's Git blob.
"""

from __future__ import annotations

import copy
import dataclasses
import hashlib
import io
import json
import subprocess
import tarfile
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import beyond_horizon_replay as replay
from devtools import construction_checker as checker
from devtools import hosted_shards
from devtools import intake_ledger as ledger
from devtools.retained_data import read_retained_bytes
from sqpack import hosted_data
from sqpack.retained_json import dumps as retained_dumps

#: A walk above 1024, as a records slice declares one (`Walk.above`, `Walk.through`).
ABOVE = "upper-bounds-above-1024-test"


def _above(**fields: Any) -> replay.Walk:
    """The walk above 1024, with ``fields`` in place of its defaults."""
    values: dict[str, Any] = {"later": {}, "awaiting": {}, "above": 1024, "through": None}
    return replay.Walk(ABOVE, **(values | fields))


def test_every_frozen_release_and_walk_keeps_its_window() -> None:
    """W7 sets no window above 1024: the 20 releases decide from the corpus to 1024 and
    name no walk above or hosted manifest; every walk reaches to 1024, and the five that
    apply the owner's rulings list both through 1024."""
    assert len(replay.RELEASES) == 20
    for chosen in replay.RELEASES.values():
        assert (chosen.decided_above, chosen.decided_through) == (324, replay.FROZEN_THROUGH)
        assert (chosen.walk_above, chosen.hosted, chosen.frozen) == ("", None, True)
    assert all(walk.through == replay.FROZEN_THROUGH for walk in replay.WALKS.values())
    assert len(replay.WALK_RULINGS) == 5
    for rulings in replay.WALK_RULINGS.values():
        assert [item["through"] for item in rulings] == [1024, 1024]


def test_a_frozen_release_asked_above_its_window_is_refused() -> None:
    """With its top lifted, #666 would decide 19 rows and #719 120: neither is the count
    each was recorded with, so the release is refused until a records slice lifts its
    window and its receipts together."""
    for issue, found, recorded in ((666, 19, 11), (719, 120, 112)):
        lifted = dataclasses.replace(replay.release(issue), decided_through=None)
        with pytest.raises(replay.ReplayError, match=f"{found} rows above 324, not {recorded}"):
            replay.decided_claims(lifted)
    above = dataclasses.replace(replay.release(666), decided_above=1024, decided_through=None)
    assert [row.n for row in replay.decided_claims(dataclasses.replace(above, decided=8))] == [
        1061,
        1128,
        1196,
        1266,
        1339,
        1413,
        1489,
        1568,
    ]
    assert replay.held_claims(above) == []


def test_a_walk_above_1024_applies_both_rulings_to_its_top_count() -> None:
    """The walk above 1024 lists both rulings with no top (`NO_LIMIT`). One whose rulings
    stop at 1024 leaves both answers unapplied above it, and `answer_problems` says so."""
    open_ended = replay.ruling_entries(through=None)
    assert all("through" not in item for item in open_ended)
    ruled = ledger.rulings_of({"rulings": open_ended})
    assert (ruled.restatement, ruled.classical) == (ledger.NO_LIMIT, ledger.NO_LIMIT)
    above = {"read_on": "2026-10-24", "rulings": open_ended}
    assert ledger.answer_problems(above, [1100, 2043], set()) == []
    stopped = {"read_on": "2026-10-24", "rulings": replay.ruling_entries()}
    restatement, classical = ledger.answer_problems(stopped, [1100, 2043], set())
    assert "restatement answer is not applied at n = 1100, 2043" in restatement
    assert "Göbel's baseline is not applied at n = 1100, 2043" in classical


def test_a_row_above_1024_belongs_to_the_walk_above(monkeypatch: pytest.MonkeyPatch) -> None:
    """`walk_of` reads the count: #666's rows to 1024 stay with the backlog walk, those
    above go to the walk above 1024 it names; with none named, or one that does not reach
    the count, the row is refused."""
    chosen = replay.release(666)
    with pytest.raises(replay.ReplayError, match="n=1061: no walk reaches it"):
        replay.walk_of(chosen, 1061)
    monkeypatch.setitem(replay.WALKS, ABOVE, _above())
    named = dataclasses.replace(chosen, walk_above=ABOVE)
    assert replay.walk_of(named, 464).name == replay.BACKLOG
    assert replay.walk_of(named, 1061).name == ABOVE
    assert [walk.name for walk in replay.walks_of(named)] == [replay.BACKLOG, ABOVE]
    monkeypatch.setitem(replay.WALKS, ABOVE, dataclasses.replace(_above(), through=1050))
    with pytest.raises(replay.ReplayError, match=f"n=1061: {ABOVE} does not reach it"):
        replay.walk_of(named, 1061)
    assert replay.WALKS[replay.ISSUE_719].reaches(1024)
    assert not replay.WALKS[replay.ISSUE_719].reaches(1061)


def test_a_window_above_1024_reads_goebel_s_construction_from_the_module() -> None:
    """A frozen window keeps the retained program and its receipt byte for byte (#791's
    review A, A11); #666 lifted reads the maintained module and writes the v2 receipt,
    every one of its 19 sides below Göbel's construction, the eight above 1024 included."""
    frozen = replay.release(666)
    sides = replay.decided_sides(frozen)
    kept = retained_dumps(replay.goebel_receipt(frozen, sides), sort_keys=True)
    assert kept == frozen.path(replay.GOEBEL).read_text(encoding="utf-8")
    assert json.loads(kept)["program"].endswith("review/goebel_beyond_horizon.py")
    lifted = dataclasses.replace(frozen, decided_through=None, decided=19)
    receipt = replay.goebel_receipt(lifted, replay.decided_sides(lifted))
    assert (receipt["format"], receipt["program"]) == (
        replay.GOEBEL_FORMAT_V2,
        "packing/devtools/goebel_construction.py",
    )
    assert receipt["comparison"]["tally"] == {"above": 0, "equal": 0, "below": 19}
    at = {item["n"]: item for item in receipt["comparison"]["detail"]}
    assert (at[1489]["goebel"], at[1489]["goebel_from_count"]) == ("20 + 27/2*sqrt(2)", 1489)
    assert replay.beyond_horizon_rows(lifted)["limit"] is None
    assert replay.beyond_horizon_rows(frozen, sides)["limit"] == replay.FROZEN_THROUGH


def test_a_deletion_bound_is_settled_only_one_square_from_the_next_count() -> None:
    """`deletion_holds` gives the history walk's holds of 4e4c8ce's 39 deletion bounds:
    36 one square from the next count's certificate, settled by the D6 answer; 751, 752
    and 927 waiting on think-kzme. Above 1024 a two-square deletion waits too, and every
    bound an issue claims, as #763's 1646 and 1727 would."""
    history = replay.HISTORY_HELD["franciscouzo/square-packing@4e4c8ce"]
    one = sorted(history[0].counts)
    bounds = [(n, n + 1, 1) for n in one] + [(751, 754, 3), (752, 754, 2), (927, 929, 2)]
    built = replay.deletion_holds(bounds)
    assert [(item.kind, item.bead, item.counts, item.answer) for item in built] == [
        (item.kind, item.bead, item.counts, item.answer) for item in history
    ]
    settled, waiting = replay.deletion_holds([(1101, 1102, 1), (1100, 1102, 2)])
    assert (settled.counts, settled.answer) == (frozenset({1101}), replay.DELETION_ANSWER)
    assert (waiting.counts, waiting.bead, waiting.answer) == (
        frozenset({1100}),
        "think-kzme",
        "",
    )
    (claimed,) = replay.deletion_holds([(1646, 1647, 1), (1727, 1728, 1)], claimed_by="think-x")
    assert (claimed.bead, claimed.also, claimed.answer) == ("think-x", ("think-kzme",), "")
    with pytest.raises(replay.ReplayError, match="1102 less 1 squares is not 1100"):
        replay.deletion_holds([(1100, 1102, 1)])


def test_a_catalogue_side_declared_as_a_row_before_n1_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The walk above 1024 records the Kingbird catalogue's sides and holds them on N1, so
    the chain passes over them; a register row from the catalogue at a held count is
    refused until the owner answers, and the walk's note counts the hold."""
    label = "Kingbird catalogue 2026-08-22"
    source = "kingbird-squares-in-squares-2026-08-22"
    walk = _above(later={label: source}, held={label: (replay.catalogue_hold([1453, 2043]),)})
    (tmp_path / ABOVE).mkdir()
    counts = [
        {"n": n, "start": [], "steps": [{"report": label, "verdict": replay.RECORDED}]}
        for n in (1453, 2043)
    ]
    (tmp_path / ABOVE / "ledger.json").write_text(json.dumps({"counts": counts}))
    monkeypatch.setattr(replay, "INTAKE", tmp_path)
    monkeypatch.setattr(replay, "WALKS", {ABOVE: walk})
    register: dict[str, Any] = {"beyond_horizon_claims": [{"n": 1453, "source_id": source}]}
    assert replay.held_problems(register) == [
        f"{ABOVE}: {label} n=1453: held for think-llit, yet {source} has a row there"
    ]
    assert replay.held_problems({"beyond_horizon_claims": []}) == []
    assert "2 catalogue sides, the capture of 2026-08-22" in replay.held_sentence(walk, label)
    steps = [{"report": label, "verdict": replay.RECORDED}]
    assert replay.recorded_reports(walk, {"n": 2043, "steps": steps}) == []


def _with_recipe(tmp_path: Path) -> replay.Release:
    """#763's release with its recipe at 444 declared as a row, in a copy of its packet's
    declaration and receipts: the parent, 403, is a replayed row of the release."""
    chosen = replay.release(763)
    item = next(
        claim
        for claim in replay.mapped_claims(chosen)
        if claim["n"] == 444 and claim["kind"] == "construction"
    )
    declared = json.loads((chosen.directory / chosen.declared).read_text(encoding="utf-8"))
    recipe = {
        "n": 444,
        "certificate": item["certificate"],
        "printed": replay.ceiling(Fraction(item["exact"])),
        "recipe": replay.declared_recipe(item),
    }
    declared["rows"] = sorted([*declared["rows"], recipe], key=lambda row: row["n"])
    (tmp_path / "declared-rows.json").write_text(json.dumps(declared), encoding="utf-8")
    receipts = tmp_path / "receipts"
    receipts.mkdir()
    for name in (replay.FILTERED.name, replay.FIRST_COMMITS.name):
        (receipts / name).write_bytes((chosen.directory / chosen.receipts / name).read_bytes())
    return dataclasses.replace(
        chosen,
        rows=185,
        decided=185,
        receipts=receipts,
        declared=tmp_path / "declared-rows.json",
    )


def test_a_recipe_row_is_decided_by_the_checker_and_held_to_its_receipt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A declared recipe row is no filtered row: the construction checker decides it from
    its replayed parent. With no decisions it is refused; written, they hold, every control
    refused; a decision changed afterwards differs from its derivation."""
    chosen = _with_recipe(tmp_path)
    monkeypatch.setitem(replay.RELEASES, chosen.label, chosen)
    assert [row.n for row in replay.recipe_claims(chosen)] == [444]
    assert 444 not in {row.n for row in replay.replayed_claims(chosen)}
    assert replay.recipe_problems(chosen, replay=False, workers=1) == [
        "#763: 1 recipe rows and no recipe decisions"
    ]
    assert replay.write_recipe_decisions([763], workers=1) == {"#763": 1}
    receipt = json.loads(chosen.path(replay.RECIPES).read_text(encoding="utf-8"))
    (decision,) = receipt["rows"]
    assert (decision["capacity"], decision["verdict"], receipt["parents"]) == (
        444,
        "decided",
        [],
    )
    assert receipt["controls"] == list(checker.CONTROLS)
    assert all(control["refused"] for control in decision["controls"])
    assert replay.recipe_problems(chosen, replay=False, workers=1) == []
    sides = replay.decided_sides(chosen)
    assert sides[444] == Fraction(decision["side"])
    (row,) = [
        row for row in replay.beyond_horizon_rows(chosen, sides)["results"] if row["n"] == 444
    ]
    assert row["recipe"]["source_n"] == 403
    forged = copy.deepcopy(receipt)
    forged["rows"][0]["capacity"] = 445
    chosen.path(replay.RECIPES).write_text(json.dumps(forged), encoding="utf-8")
    assert replay.recipe_problems(chosen, replay=False, workers=1) == [
        "#763: the recipe decisions differ from their derivation"
    ]


def test_the_fast_check_reads_a_hosted_row_without_opening_a_shard(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A hosted row's side and Git blob come from the source-history receipt, held to the
    packet's pin: no shard is opened, and a receipt whose digest is not the pin's is
    refused."""
    chosen = dataclasses.replace(replay.release(732), hosted=Path("packing/hosted/none.yaml"))
    row = replay.decided_claims(chosen)[0]
    raw = read_retained_bytes(replay.archive(chosen) / row.path)
    entry = {
        "n": row.n,
        "certificate": row.path,
        "sha256": replay.manifest(chosen)[row.path],
        "blob": replay.git_blob(raw),
        "side": legacy_side(raw, row.n),
    }
    monkeypatch.setattr(
        replay, "retained_exists", lambda path: not str(path).endswith(row.path)
    )
    monkeypatch.setattr(replay, "index_entries", lambda _chosen: {row.path: entry})

    def opened(*_args: object) -> bytes:
        raise AssertionError("the fast check opened a shard")

    monkeypatch.setattr(hosted_shards, "read", opened)
    assert replay.is_hosted(chosen, row.path)
    assert replay.decided_sides(chosen)[row.n] == Fraction(entry["side"])
    assert replay.blob_of(chosen, row.path) == entry["blob"]
    entry["sha256"] = "0" * 64
    with pytest.raises(replay.ReplayError, match="digest or count is not the packet's"):
        replay.decided_sides(chosen)


def legacy_side(raw: bytes, n: int) -> str:
    return str(replay.header_side(raw, n, "test"))


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=True
    ).stdout.strip()


def test_source_history_above_1024_reads_the_retained_commit_from_the_shards(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Above 1024 the files at the retained commit are read from the hosted shards, each
    held to the Git blob the clone's tree names; the earlier side at the same path is read
    from the clone, and a shard whose bytes are not the clone's blob is refused."""
    clone = tmp_path / "clone"
    subprocess.run(["git", "init", "-q", str(clone)], check=True)
    _git(clone, "config", "user.email", "test@example.com")
    _git(clone, "config", "user.name", "test")
    path = "certificates/1000-1999/n1025.cert"
    (clone / "certificates/1000-1999").mkdir(parents=True)
    for side in ("33", "65/2"):
        raw = f"1025 {side}\n".encode()
        (clone / path).write_bytes(raw)
        entry = {"certificate": path, "certificate_sha256": hashlib.sha256(raw).hexdigest()}
        index = {"witnesses": {"1025": entry | {"bound": side}}}
        (clone / "certificates/manifest.json").write_text(json.dumps(index))
        _git(clone, "add", "-A")
        _git(clone, "commit", "-q", "-m", side)
    head = _git(clone, "rev-parse", "HEAD")
    monkeypatch.setitem(replay.WALKS, ABOVE, _above())
    chosen = dataclasses.replace(
        replay.release(732), retained=head, hosted=Path("packing/hosted/none.yaml")
    )
    monkeypatch.setitem(replay.RELEASES, chosen.label, chosen)
    shard_bytes = {path: raw}
    read: list[str] = []

    def from_shard(_chosen: replay.Release, wanted: str) -> bytes:
        read.append(wanted)
        return shard_bytes[wanted]

    monkeypatch.setattr(replay, "certificate_bytes", from_shard)
    pin_blob = replay.git_blob(raw)
    blobs = replay._blobs  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]

    def clone_blobs(repo: Path, wanted: list[str]) -> dict[str, bytes]:
        assert pin_blob not in wanted, "read the retained commit's file from the clone"
        return blobs(repo, wanted)

    monkeypatch.setattr(replay, "_blobs", clone_blobs)
    found = replay.source_history(732, clone, replay.WALKS[ABOVE])
    assert read == [path]
    assert found["counts"] == [1025, None]
    (pinned,) = found["at_commit"]
    assert (pinned["n"], pinned["side"], pinned["blob"]) == (1025, "65/2", pin_blob)
    assert [item["side"] for item in found["publications"]] == ["33", "65/2"]
    shard_bytes[path] = raw + b"\n"
    with pytest.raises(replay.ReplayError, match="hosted bytes are not the clone's blob"):
        replay.source_history(732, clone, replay.WALKS[ABOVE])


def test_a_hosted_certificate_is_read_through_the_manifest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`certificate_bytes` reads a certificate the packet pins and does not retain through
    the release's hosted manifest (`sqpack.hosted_data.require`), held to the pin."""
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / ".gitignore").write_text("hosted/\n", encoding="utf-8")
    path = "certificates/1000-1999/n1025.cert"
    raw = b"1025 65/2\n"
    shard = tmp_path / "hosted/shards/one.tar.xz"
    shard.parent.mkdir(parents=True)
    with tarfile.open(shard, "w:xz") as archive:
        info = tarfile.TarInfo(path)
        info.size = len(raw)
        archive.addfile(info, io.BytesIO(raw))
    manifest = tmp_path / "manifests/test.yaml"
    hosted_data.stage(
        manifest, shard.parent, tmp_path, repository="jlevy/squares", tag="data/t-v1"
    )
    chosen = dataclasses.replace(replay.release(732), hosted=manifest.relative_to(tmp_path))
    pins = {path: hashlib.sha256(raw).hexdigest()}
    monkeypatch.setattr(replay, "hosted_pins", lambda _chosen: pins)
    monkeypatch.setattr(replay, "REPO", tmp_path)
    monkeypatch.setattr(replay, "archive", lambda _chosen: tmp_path / "no-packet")
    assert replay.certificate_bytes(chosen, path) == raw
    pins[path] = "0" * 64
    with pytest.raises(replay.ReplayError, match="not the ones the packet pins"):
        replay.certificate_bytes(chosen, path)
