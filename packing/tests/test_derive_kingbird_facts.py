#!/usr/bin/env python3
"""What the one-time Kingbird acquisition pass may retain, drop, and refuse.

Nothing here reaches the network. `urllib.request.urlopen` is replaced in every test
that fetches, so a test that starts making requests fails loudly rather than quietly
becoming a live audit of someone's website.
"""

from __future__ import annotations

import hashlib
import urllib.error
import urllib.request
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any, Self

import pytest

from devtools import derive_kingbird_facts as derive_tool
from devtools.derive_kingbird_facts import (
    REMOVAL_LICENCE,
    DerivationPlan,
    DerivationRefusedError,
)
from sqpack.kingbird_catalogue import CatalogueEntry, default_catalogue_path
from sqpack.known_best import kingbird_derived_witness, parse_kingbird_svg
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
WITNESSES = ROOT / "witnesses/known-best"

#: A picture in the shape the adapter accepts: a 2.5-sided container holding one
#: two-by-two block of unit squares. Small enough to reason about pose by pose, and
#: deliberately not a grid case, so the acquisition pass does not skip it.
SYNTHETIC_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg">'
    '<defs><rect id="outer" width="2.5" height="2.5" fill="none"/></defs>'
    '<rect width="2" height="2"/>'
    "</svg>"
)
SYNTHETIC_SIDE = "2.5"
SYNTHETIC_URL = "https://example.invalid/packing/square-4.svg"

#: The four poses `SYNTHETIC_SVG` yields, in the order the adapter recovers them.
SYNTHETIC_CENTERS = [("0.5", "2.0"), ("0.5", "1.0"), ("1.5", "2.0"), ("1.5", "1.0")]


def catalogue_entry(n: int, listed_n: tuple[int, ...], side: str) -> CatalogueEntry:
    return CatalogueEntry(
        n=n,
        listed_n=listed_n,
        side_decimal=side,
        exact_form=None,
        algebraic_degree=None,
        minimal_polynomial=None,
        found_by=(),
        found_year=None,
        catalogue_rigid="not-stated",
        catalogue_pictured=True,
        svg_path=f"square-{n}.svg",
        source_line=1,
    )


def availability_entry(n: int, listed_n: tuple[int, ...]) -> dict[str, Any]:
    return {
        "n": n,
        "source_key": "kingbird-current-catalogue",
        "source_n": max(listed_n),
        "listed_n": list(listed_n),
        "source_path": f"square-{max(listed_n)}.svg",
        "source_url": SYNTHETIC_URL,
    }


def synthetic_plan(n: int, *, source_n: int, out_root: Path) -> DerivationPlan:
    return DerivationPlan(
        n=n,
        source_n=source_n,
        listed_n=(n, source_n) if n != source_n else (n,),
        source_path=f"square-{source_n}.svg",
        url=SYNTHETIC_URL,
        catalogue_side=SYNTHETIC_SIDE,
        witness_path=out_root / f"n-{n:03d}.yaml",
    )


class FakeResponse:
    """What `fetch_picture` uses of a `urlopen` result, and nothing else."""

    def __init__(self, payload: bytes, last_modified: str | None = None) -> None:
        self.payload: bytes = payload
        self.headers: dict[str, str] = (
            {} if last_modified is None else {"Last-Modified": last_modified}
        )

    def read(self) -> bytes:
        return self.payload

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_exception: object) -> bool:
        return False


@pytest.fixture
def offline(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    """Serve `SYNTHETIC_SVG` for any URL, and record what was asked for."""
    requested: list[str] = []

    def fake_urlopen(request: urllib.request.Request, timeout: float = 0) -> FakeResponse:
        del timeout
        assert request.get_header("User-agent") == derive_tool.USER_AGENT
        requested.append(request.full_url)
        return FakeResponse(SYNTHETIC_SVG.encode("utf-8"))

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(derive_tool.time, "sleep", lambda _seconds: None)
    return requested


@pytest.fixture
def synthetic_corpus(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Point the plan builder at a two-case corpus served by one picture.

    The frontier root moves with it. These counts are fictional -- the real `n = 3` and
    `n = 4` records report a side of 2 -- so consulting the real register would check
    this picture against a record that is not about it.
    """
    entries = {3: availability_entry(3, (3, 4)), 4: availability_entry(4, (3, 4))}
    catalogue = {
        3: catalogue_entry(4, (3, 4), SYNTHETIC_SIDE),
        4: catalogue_entry(4, (3, 4), SYNTHETIC_SIDE),
    }
    monkeypatch.setattr(derive_tool, "availability_entries", lambda: entries)
    monkeypatch.setattr(derive_tool, "parse_catalogue", lambda: catalogue)
    monkeypatch.setattr(derive_tool, "FRONTIER", tmp_path / "no-such-frontier")


def test_the_retained_catalogue_still_licenses_a_subpacking() -> None:
    # The subpacking rule is the source's own sentence, not this repository's default.
    # If the retained page stops saying it, the rule loses its warrant and every
    # derivation that needs one must fail rather than pick a square.
    text = default_catalogue_path().read_text(encoding="utf-8")

    assert REMOVAL_LICENCE in text


def test_a_derived_witness_has_the_shape_the_retained_corpus_already_has(
    tmp_path: Path,
) -> None:
    plan = synthetic_plan(4, source_n=4, out_root=tmp_path)

    witness = derive_tool.derive_witness(
        plan,
        SYNTHETIC_SVG,
        catalogue_text=REMOVAL_LICENCE,
        retrieved="2026-09-07",
        frontier_root=tmp_path,
    )

    assert witness["id"] == "W-known-best-n004"
    assert witness["n"] == 4
    assert witness["side"] == "2.5"
    assert witness["square_size"] == "1"
    assert witness["representation"] == "center-angle"
    assert witness["scalar"] == {"kind": "decimal"}
    assert witness["coordinates"]["angle_unit"] == "degrees"
    assert [square["id"] for square in witness["squares"]] == [1, 2, 3, 4]
    assert [tuple(square["center"]) for square in witness["squares"]] == [
        tuple(center) for center in SYNTHETIC_CENTERS
    ]
    assert {square["angle"] for square in witness["squares"]} == {"0"}
    assert witness["claim"]["coordinate_provenance"] == "numerically-checked"
    assert witness["source"]["url"] == SYNTHETIC_URL
    assert witness["source"]["retrieved"] == "2026-09-07"
    assert witness["certificate"]["kind"] == "numerical-feasibility-receipt"
    assert witness["certificate"]["result"]["check_passed"] is True


def test_a_derived_witness_carries_the_same_keys_as_a_retained_one(tmp_path: Path) -> None:
    # n = 71 is one of the 34 rows the August pass produced from a source no longer
    # retained. A new row has to be indistinguishable in shape from an old one, or the
    # corpus would carry two kinds of Kingbird witness.
    retained = safe_load((WITNESSES / "n-071.yaml").read_text(encoding="utf-8"))["witness"]
    plan = synthetic_plan(4, source_n=4, out_root=tmp_path)

    witness = derive_tool.derive_witness(
        plan, SYNTHETIC_SVG, catalogue_text=REMOVAL_LICENCE, frontier_root=tmp_path
    )

    assert list(witness) == list(retained)
    assert list(witness["claim"]) == list(retained["claim"])
    assert list(witness["source"]) == list(retained["source"])
    assert list(witness["certificate"]) == list(retained["certificate"])
    assert list(witness["squares"][0]) == list(retained["squares"][0])
    assert witness["source"]["retrieved"] == derive_tool.DERIVED_RETRIEVED_DATE
    assert retained["source"]["retrieved"] == "2026-08-26"


def test_a_subpacking_drops_the_squares_the_ordering_puts_last() -> None:
    geometry = parse_kingbird_svg(SYNTHETIC_SVG, expected_n=4)

    kept = derive_tool.subpacking_poses(
        geometry.poses, n=3, source_n=4, catalogue_text=REMOVAL_LICENCE
    )

    # Descending by centre, x then y: (1.5, 2.0) sorts last and is the one that goes.
    # The survivors keep the order they were recovered in.
    assert [(pose.center_x, pose.center_y) for pose in kept] == [
        ("0.5", "2.0"),
        ("0.5", "1.0"),
        ("1.5", "1.0"),
    ]


def test_a_pictured_count_is_kept_whole() -> None:
    geometry = parse_kingbird_svg(SYNTHETIC_SVG, expected_n=4)

    kept = derive_tool.subpacking_poses(geometry.poses, n=4, source_n=4, catalogue_text="")

    assert kept == geometry.poses


def test_a_subpacking_is_refused_when_the_catalogue_stops_licensing_one() -> None:
    geometry = parse_kingbird_svg(SYNTHETIC_SVG, expected_n=4)

    with pytest.raises(DerivationRefusedError) as refusal:
        derive_tool.subpacking_poses(
            geometry.poses, n=3, source_n=4, catalogue_text="a page that no longer says it"
        )

    assert refusal.value.kind == "removal-licence-absent"


def test_a_picture_that_does_not_hold_the_stated_count_is_refused() -> None:
    geometry = parse_kingbird_svg(SYNTHETIC_SVG, expected_n=4)

    with pytest.raises(DerivationRefusedError) as refusal:
        derive_tool.subpacking_poses(
            geometry.poses, n=5, source_n=5, catalogue_text=REMOVAL_LICENCE
        )

    assert refusal.value.kind == "square-count-mismatch"


def test_a_side_the_catalogue_disagrees_with_is_refused(tmp_path: Path) -> None:
    plan = synthetic_plan(4, source_n=4, out_root=tmp_path)
    wrong = DerivationPlan(**{**vars(plan), "catalogue_side": "2.6"})

    with pytest.raises(DerivationRefusedError) as refusal:
        derive_tool.derive_witness(
            wrong, SYNTHETIC_SVG, catalogue_text=REMOVAL_LICENCE, frontier_root=tmp_path
        )

    assert refusal.value.kind == "side-mismatch"
    assert "the catalogue" in refusal.value.detail


def test_a_frontier_record_is_checked_where_one_exists(tmp_path: Path) -> None:
    # Above n = 100 there may be no record yet, so the catalogue is what the receipt is
    # checked against -- but a record that does exist may not be allowed to disagree.
    frontier = tmp_path / "frontier"
    frontier.mkdir()
    (frontier / "n-004.md").write_text(
        "---\npacking:\n  n: 4\n  reported_upper_bound:\n    value: '2.6'\n---\nbody\n",
        encoding="utf-8",
    )
    plan = synthetic_plan(4, source_n=4, out_root=tmp_path)

    with pytest.raises(DerivationRefusedError) as refusal:
        derive_tool.derive_witness(
            plan, SYNTHETIC_SVG, catalogue_text=REMOVAL_LICENCE, frontier_root=frontier
        )

    assert refusal.value.kind == "side-mismatch"
    assert "the frontier record" in refusal.value.detail


def test_a_frontier_record_that_agrees_is_no_obstacle(tmp_path: Path) -> None:
    frontier = tmp_path / "frontier"
    frontier.mkdir()
    (frontier / "n-004.md").write_text(
        "---\npacking:\n  n: 4\n  reported_upper_bound:\n    value: '2.5'\n---\nbody\n",
        encoding="utf-8",
    )
    plan = synthetic_plan(4, source_n=4, out_root=tmp_path)

    witness = derive_tool.derive_witness(
        plan, SYNTHETIC_SVG, catalogue_text=REMOVAL_LICENCE, frontier_root=frontier
    )

    assert witness["n"] == 4


@pytest.mark.usefixtures("synthetic_corpus")
def test_an_already_retained_witness_is_skipped_rather_than_refetched(
    tmp_path: Path, offline: list[str]
) -> None:
    (tmp_path / "n-004.yaml").write_text("already here\n", encoding="utf-8")

    status = derive_tool.derive([3, 4], out_root=tmp_path)

    assert status == 0
    assert (tmp_path / "n-004.yaml").read_text(encoding="utf-8") == "already here\n"
    assert (tmp_path / "n-003.yaml").is_file()
    assert offline == [SYNTHETIC_URL]


@pytest.mark.usefixtures("synthetic_corpus")
def test_a_refresh_replaces_only_a_witness_whose_side_the_catalogue_left(
    tmp_path: Path, offline: list[str]
) -> None:
    """After the page is captured again, a moved side is re-derived and nothing else is."""
    stale = "witness:\n  side: '2.6'\n"
    current = "witness:\n  side: '2.5'\n"
    (tmp_path / "n-003.yaml").write_text(stale, encoding="utf-8")
    (tmp_path / "n-004.yaml").write_text(current, encoding="utf-8")

    status = derive_tool.derive([3, 4], out_root=tmp_path, refresh=True, retrieved="2026-09-30")

    assert status == 0
    assert offline == [SYNTHETIC_URL]
    assert (tmp_path / "n-004.yaml").read_text(encoding="utf-8") == current
    rewritten = safe_load((tmp_path / "n-003.yaml").read_text(encoding="utf-8"))["witness"]
    assert rewritten["side"] == SYNTHETIC_SIDE
    assert rewritten["source"]["retrieved"] == "2026-09-30"


@pytest.mark.usefixtures("synthetic_corpus")
def test_a_refresh_leaves_a_count_whose_record_reports_another_source(
    tmp_path: Path, offline: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """A certified packet's count keeps that packet's witness, whatever the page prints."""
    frontier = tmp_path / "frontier"
    frontier.mkdir()
    (frontier / "n-003.md").write_text(
        "---\npacking:\n  n: 3\n  reported_upper_bound:\n    value: '2.4'\n"
        "    source_key: '[Elsewhere]'\n---\nbody\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(derive_tool, "FRONTIER", frontier)
    out = tmp_path / "witnesses"
    out.mkdir()
    packet = "witness:\n  side: '2.4'\n"
    (out / "n-003.yaml").write_text(packet, encoding="utf-8")

    plans, skipped, refusals = derive_tool.derivation_plans([3], out_root=out, refresh=True)

    assert (plans, refusals) == ([], [])
    assert [(case.n, case.reason) for case in skipped] == [(3, "other-source")]
    assert offline == []


@pytest.mark.usefixtures("synthetic_corpus")
def test_without_refresh_a_stale_witness_is_still_left_alone(
    tmp_path: Path, offline: list[str]
) -> None:
    stale = "witness:\n  side: '2.6'\n"
    for name in ("n-003.yaml", "n-004.yaml"):
        (tmp_path / name).write_text(stale, encoding="utf-8")

    assert derive_tool.derive([3, 4], out_root=tmp_path) == 0

    assert offline == []
    assert (tmp_path / "n-003.yaml").read_text(encoding="utf-8") == stale


@pytest.mark.usefixtures("synthetic_corpus")
def test_one_picture_serving_two_counts_is_fetched_once(
    tmp_path: Path, offline: list[str]
) -> None:
    status = derive_tool.derive([3, 4], out_root=tmp_path)

    assert status == 0
    assert offline == [SYNTHETIC_URL]
    assert sorted(path.name for path in tmp_path.iterdir()) == ["n-003.yaml", "n-004.yaml"]


@pytest.mark.usefixtures("synthetic_corpus", "offline")
def test_no_source_asset_is_ever_written(tmp_path: Path) -> None:
    # The retention policy is the point of the tool: the SVG exists in memory for the
    # length of one parse and nowhere else. Nothing written may be a source asset, and
    # nothing may be written into a directory that names the source.
    derive_tool.derive([3, 4], out_root=tmp_path)

    written = sorted(path for path in tmp_path.rglob("*") if path.is_file())
    assert [path.name for path in written] == ["n-003.yaml", "n-004.yaml"]
    assert not any(path.suffix == ".svg" for path in tmp_path.rglob("*"))
    assert not any(
        part.lower() == "kingbird" for path in tmp_path.rglob("*") for part in path.parts
    )


def test_an_output_root_inside_a_kingbird_directory_is_refused(tmp_path: Path) -> None:
    with pytest.raises(DerivationRefusedError) as refusal:
        derive_tool.assert_no_raw_retention(tmp_path / "kingbird" / "witnesses")

    assert refusal.value.kind == "output-under-kingbird-directory"


def test_a_retained_raw_kingbird_directory_stops_the_pass(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    raw = tmp_path / "kingbird"
    raw.mkdir()
    monkeypatch.setattr(derive_tool, "KINGBIRD_RAW_ROOT", raw)

    with pytest.raises(DerivationRefusedError) as refusal:
        derive_tool.assert_no_raw_retention(tmp_path / "out")

    assert refusal.value.kind == "raw-kingbird-retained"


def test_the_raw_kingbird_directory_this_pass_refuses_is_still_absent() -> None:
    assert not derive_tool.KINGBIRD_RAW_ROOT.exists()


def test_a_count_outside_the_audited_map_is_refused(tmp_path: Path) -> None:
    # Reported rather than raised: one unreadable case in a range does not take the rest
    # of the pass down with it. 101 is derivable and stays derivable.
    plans, _skipped, refusals = derive_tool.derivation_plans([101, 500], out_root=tmp_path)

    assert [plan.n for plan in plans] == [101]
    assert [(n, refusal.kind) for n, refusal in refusals] == [(500, "no-availability-entry")]


def test_the_real_map_routes_the_two_kinds_this_pass_leaves_alone(tmp_path: Path) -> None:
    # 103 is a retained UnitSquare rendering and 119 is a grid case the catalogue happens
    # to picture; 147 needs the shared-picture subpacking and 101 does not.
    plans, skipped, refusals = derive_tool.derivation_plans(
        [101, 103, 119, 147], out_root=tmp_path
    )

    assert refusals == []
    reasons = {case.n: case.reason for case in skipped}
    assert reasons == {103: "other-source", 119: "grid-covered"}
    assert [(plan.n, plan.source_n, plan.removals) for plan in plans] == [
        (101, 101, 0),
        (147, 148, 1),
    ]
    assert plans[1].url == "https://kingbird.myphotos.cc/packing/square-148.svg"


@pytest.mark.usefixtures("synthetic_corpus")
def test_a_dry_run_touches_neither_the_network_nor_the_disk(
    tmp_path: Path, offline: list[str]
) -> None:
    status = derive_tool.derive([3, 4], out_root=tmp_path, dry_run=True)

    assert status == 0
    assert offline == []
    assert list(tmp_path.iterdir()) == []


def test_a_fetch_that_never_succeeds_is_a_refusal(monkeypatch: pytest.MonkeyPatch) -> None:
    attempts: list[str] = []

    def failing_urlopen(request: urllib.request.Request, timeout: float = 0) -> FakeResponse:
        del timeout
        attempts.append(request.full_url)
        raise urllib.error.URLError("no route")

    monkeypatch.setattr(urllib.request, "urlopen", failing_urlopen)
    monkeypatch.setattr(derive_tool.time, "sleep", lambda _seconds: None)

    with pytest.raises(DerivationRefusedError) as refusal:
        derive_tool.fetch_svg(SYNTHETIC_URL)

    assert refusal.value.kind == "fetch-failed"
    assert len(attempts) == derive_tool.FETCH_ATTEMPTS


def test_a_response_that_is_not_svg_is_a_refusal(monkeypatch: pytest.MonkeyPatch) -> None:
    def html_urlopen(request: urllib.request.Request, timeout: float = 0) -> FakeResponse:
        del request, timeout
        return FakeResponse(b"<html>not here</html>")

    monkeypatch.setattr(urllib.request, "urlopen", html_urlopen)
    monkeypatch.setattr(derive_tool.time, "sleep", lambda _seconds: None)

    with pytest.raises(DerivationRefusedError) as refusal:
        derive_tool.fetch_svg(SYNTHETIC_URL)

    assert refusal.value.kind == "not-svg"


def test_an_svg_behind_a_long_comment_is_still_svg(monkeypatch: pytest.MonkeyPatch) -> None:
    """`square-179.svg` puts 166,839 bytes of polynomial comment ahead of its `<svg>`."""
    preamble = b'<?xml version="1.0"?>\n<!--' + b"x" * 200_000 + b"-->\n"

    def long_urlopen(request: urllib.request.Request, timeout: float = 0) -> FakeResponse:
        del request, timeout
        return FakeResponse(preamble + SYNTHETIC_SVG.encode("utf-8"))

    monkeypatch.setattr(urllib.request, "urlopen", long_urlopen)
    monkeypatch.setattr(derive_tool.time, "sleep", lambda _seconds: None)

    assert derive_tool.fetch_svg(SYNTHETIC_URL).endswith(SYNTHETIC_SVG)


@pytest.mark.usefixtures("synthetic_corpus")
def test_a_refused_case_exits_nonzero(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def failing_urlopen(request: urllib.request.Request, timeout: float = 0) -> FakeResponse:
        del request, timeout
        raise urllib.error.URLError("no route")

    monkeypatch.setattr(urllib.request, "urlopen", failing_urlopen)
    monkeypatch.setattr(derive_tool.time, "sleep", lambda _seconds: None)

    status = derive_tool.derive([3, 4], out_root=tmp_path)

    assert status == 1
    assert list(tmp_path.iterdir()) == []


@pytest.mark.usefixtures("synthetic_corpus", "offline")
def test_the_command_line_derives_one_case(tmp_path: Path) -> None:
    status = derive_tool.main(["--n", "4", "--out", str(tmp_path)])

    assert status == 0
    assert (tmp_path / "n-004.yaml").is_file()


def test_the_command_line_refuses_an_impolite_job_count(tmp_path: Path) -> None:
    with pytest.raises(SystemExit):
        derive_tool.main(["--n", "4", "--out", str(tmp_path), "--jobs", "99"])


def test_a_refused_plan_exits_nonzero_without_fetching(tmp_path: Path) -> None:
    status = derive_tool.derive([500], out_root=tmp_path, dry_run=True)

    assert status == 1
    assert list(tmp_path.iterdir()) == []


# --------------------------------------------------------------------------------------
# A pinned third-party parse in place of the picture (`--from-parse`)
# --------------------------------------------------------------------------------------

#: The picture's own poses as Evan Daniel's export writes them, binary64 `[cx, cy, angle]`.
SYNTHETIC_PARSE = (
    '{"name": "square-4.svg", "s": "2.5", "n": 4, '
    '"squares": [[0.5, 2.0, 0.0], [0.5, 1.0, 0.0], [1.5, 2.0, 0.0], [1.5, 1.0, 0.0]]}'
)
PARSE_REVISION = "evand/square-packing@7ff3b2113532889708a3baa4d56bc44294022e63:site/www/data/p"
#: What the witness records of the parse it was read from: these bytes and no others.
PARSE_SHA256 = hashlib.sha256(SYNTHETIC_PARSE.encode("utf-8")).hexdigest()


def write_parse(directory: Path, text: str = SYNTHETIC_PARSE) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "square-4.json").write_text(text, encoding="utf-8")
    return directory


def test_a_parse_stands_in_for_the_picture_and_the_witness_says_whose_it_is(
    tmp_path: Path,
) -> None:
    plan = synthetic_plan(4, source_n=4, out_root=tmp_path)

    witness = derive_tool.derive_witness(
        plan,
        SYNTHETIC_PARSE,
        catalogue_text=REMOVAL_LICENCE,
        retrieved="2026-10-05",
        frontier_root=tmp_path,
        parse_revision=PARSE_REVISION,
    )

    assert [tuple(square["center"]) for square in witness["squares"]] == [
        tuple(center) for center in SYNTHETIC_CENTERS
    ]
    assert {square["angle"] for square in witness["squares"]} == {"0"}
    assert witness["source"]["revision"] == f"{PARSE_REVISION}/square-4.json"
    assert witness["source"]["revision_sha256"] == PARSE_SHA256
    assert witness["source"]["url"] == SYNTHETIC_URL
    assert (
        "a third party's binary64 parse of the catalogue SVG"
        in (witness["claim"]["limitations"])
    )
    assert witness["certificate"]["result"]["check_passed"] is True


def test_a_parse_the_printed_side_does_not_truncate_is_refused(tmp_path: Path) -> None:
    # 2.4999999999 is within the 1e-8 a fetched picture is held to, and is still not a
    # picture whose side the page prints as 2.5: the page cuts its digits short.
    plan = synthetic_plan(4, source_n=4, out_root=tmp_path)
    below = SYNTHETIC_PARSE.replace('"s": "2.5"', '"s": "2.4999999999"')

    with pytest.raises(DerivationRefusedError) as refusal:
        derive_tool.derive_witness(
            plan,
            below,
            catalogue_text=REMOVAL_LICENCE,
            frontier_root=tmp_path,
            parse_revision=PARSE_REVISION,
        )

    assert refusal.value.kind == "side-mismatch"


@pytest.mark.parametrize(
    ("text", "kind"),
    [
        ("not json", "parse-unreadable"),
        ('{"s": "2.5", "n": 4, "squares": [[0.5, 2.0, 0.0]]}', "square-count-mismatch"),
        (SYNTHETIC_PARSE.replace("[1.5, 1.0, 0.0]", "[1.5, 1.0, 90.0]"), "parse-unreadable"),
        (SYNTHETIC_PARSE.replace("[1.5, 1.0, 0.0]", '[1.5, "1.0", 0.0]'), "parse-unreadable"),
        (SYNTHETIC_PARSE.replace('"s": "2.5"', '"s": "two and a half"'), "parse-unreadable"),
        (SYNTHETIC_PARSE.replace('"s": "2.5"', '"s": ""'), "parse-unreadable"),
    ],
)
def test_a_parse_that_is_not_the_export_shape_is_refused(text: str, kind: str) -> None:
    with pytest.raises(DerivationRefusedError) as refusal:
        derive_tool.geometry_from_parse(text, expected_n=4, where="square-4.json")

    assert refusal.value.kind == kind


def test_a_parse_without_its_pinned_revision_is_refused(tmp_path: Path) -> None:
    with pytest.raises(DerivationRefusedError) as refusal:
        derive_tool.derive([4], out_root=tmp_path, from_parse=write_parse(tmp_path / "p"))

    assert refusal.value.kind == "parse-unpinned"


@pytest.mark.parametrize(
    "revision",
    [
        "evand/square-packing@0123abc:site/www/data/p",
        "evand/square-packing@main:site/www/data/p",
        "evand/square-packing:site/www/data/p",
        "evand/square-packing@7ff3b2113532889708a3baa4d56bc44294022e63",
        "evand/square-packing@7ff3b2113532889708a3baa4d56bc44294022e63:",
        "Evan Daniel's export of 5 October",
    ],
)
def test_a_parse_revision_that_pins_no_commit_and_directory_is_refused(
    tmp_path: Path, revision: str
) -> None:
    """`--parse-revision` is written into every witness: it must name a repository, a full
    commit and a directory, not a branch, a short id or a sentence."""
    with pytest.raises(DerivationRefusedError) as refusal:
        derive_tool.derive(
            [4], out_root=tmp_path, from_parse=tmp_path / "p", parse_revision=revision
        )
    assert refusal.value.kind == "parse-unpinned"
    plan = synthetic_plan(4, source_n=4, out_root=tmp_path)
    with pytest.raises(DerivationRefusedError) as direct:
        derive_tool.derive_witness(
            plan,
            SYNTHETIC_PARSE,
            catalogue_text=REMOVAL_LICENCE,
            frontier_root=tmp_path,
            parse_revision=revision,
        )
    assert direct.value.kind == "parse-unpinned"


def test_a_witness_read_from_a_parse_must_carry_the_parses_digest() -> None:
    """The parse is not retained, so its digest is what ties the witness to its bytes; a
    rebuild of a retained witness that names a revision and no digest is refused."""
    retained = safe_load((derive_tool.WITNESS_ROOT / "n-071.yaml").read_text(encoding="utf-8"))[
        "witness"
    ]
    with pytest.raises(ValueError, match="revision_sha256"):
        kingbird_derived_witness(
            71,
            retained,
            source_n=71,
            source_path="resources/web/known-best-packings/sources.json",
            source_url="https://kingbird.myphotos.cc/packing/square-71.svg",
            revision=f"{PARSE_REVISION}/square-71.json",
        )


@pytest.mark.usefixtures("synthetic_corpus")
def test_a_pass_from_a_parse_fetches_nothing_and_writes_the_revision(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def no_network(*_arguments: object, **_options: object) -> FakeResponse:
        raise AssertionError("a pass from a parse must not fetch")

    monkeypatch.setattr(urllib.request, "urlopen", no_network)
    out = tmp_path / "out"
    parse = write_parse(tmp_path / "parse")
    raw = SYNTHETIC_PARSE.replace(", ", ",\r\n").encode("utf-8") + b"\r\n"
    (parse / "square-4.json").write_bytes(raw)

    status = derive_tool.main(
        [
            "--n",
            "4",
            "--out",
            str(out),
            "--retrieved",
            "2026-10-05",
            "--from-parse",
            str(parse),
            "--parse-revision",
            PARSE_REVISION,
        ]
    )

    assert status == 0
    written = safe_load((out / "n-004.yaml").read_text(encoding="utf-8"))["witness"]
    assert written["source"]["revision"] == f"{PARSE_REVISION}/square-4.json"
    assert written["source"]["retrieved"] == "2026-10-05"
    # The digest is of the file's bytes, line endings included, not of a decoded text.
    assert written["source"]["revision_sha256"] == hashlib.sha256(raw).hexdigest()
    assert written["source"]["revision_sha256"] != PARSE_SHA256


@pytest.mark.usefixtures("synthetic_corpus")
def test_a_missing_parse_is_a_refusal(tmp_path: Path) -> None:
    status = derive_tool.derive(
        [4],
        out_root=tmp_path / "out",
        from_parse=tmp_path / "empty",
        parse_revision=PARSE_REVISION,
    )

    assert status == 1
    assert not (tmp_path / "out").exists()


def test_a_refresh_plans_a_hand_audited_count_from_the_catalogue(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The 34 witnesses at `n <= 100` have no source-map row; the page names their picture."""
    monkeypatch.setattr(derive_tool, "availability_entries", dict)
    monkeypatch.setattr(
        derive_tool, "parse_catalogue", lambda: {4: catalogue_entry(4, (4,), SYNTHETIC_SIDE)}
    )
    monkeypatch.setattr(derive_tool, "FRONTIER", tmp_path / "no-such-frontier")
    (tmp_path / "n-004.yaml").write_text("witness:\n  side: '2.6'\n", encoding="utf-8")

    plans, _skipped, refusals = derive_tool.derivation_plans(
        [4], out_root=tmp_path, refresh=True
    )
    _plans, _skipped, refused_without = derive_tool.derivation_plans([4], out_root=tmp_path)

    assert refusals == []
    assert [(plan.n, plan.source_path, plan.url) for plan in plans] == [
        (4, "square-4.svg", f"{derive_tool.KINGBIRD_BASE_URL}/square-4.svg")
    ]
    assert [(n, refusal.kind) for n, refusal in refused_without] == [
        (4, "no-availability-entry")
    ]


def test_a_checkout_named_kingbird_is_not_a_kingbird_directory(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    # The guard is about what the repository retains, not where a person cloned it.
    checkout = tmp_path / "kingbird"
    monkeypatch.setattr(derive_tool, "ROOT", checkout / "packing")

    derive_tool.assert_no_raw_retention(checkout / "packing" / "witnesses" / "known-best")
    with pytest.raises(DerivationRefusedError):
        derive_tool.assert_no_raw_retention(checkout / "packing" / "kingbird" / "witnesses")


def test_a_parse_is_compared_with_a_witness_read_from_the_same_picture(tmp_path: Path) -> None:
    plan = synthetic_plan(4, source_n=4, out_root=tmp_path)
    witness = derive_tool.derive_witness(
        plan, SYNTHETIC_SVG, catalogue_text=REMOVAL_LICENCE, frontier_root=tmp_path
    )
    path = tmp_path / "n-004.yaml"
    path.write_text(derive_tool.witness_document(witness, schema="x"), encoding="utf-8")

    same = derive_tool.compare_parse(4, SYNTHETIC_PARSE, path)
    moved = derive_tool.compare_parse(
        4, SYNTHETIC_PARSE.replace("[1.5, 1.0, 0.0]", "[1.5, 1.0000001, 0.0]"), path
    )

    assert same.same_side
    assert same.worst == 0
    assert moved.worst > 1


# -- `--compare-pictures`: the retained witnesses against the pictures served today -----

KINGBIRD_PICTURE = f"{derive_tool.KINGBIRD_BASE_URL}/square-4.svg"
CREDITED_SVG = (
    "<?xml version='1.0'?>\n<!--\n    Found by A. Person on May 1, 2026.\n"
    "    Optimized by B. Person on May 2, 2026.\n\n    s = Root[...]\n-->\n" + SYNTHETIC_SVG
)
PICTURES = ROOT / "resources/web/known-best-packings/receipts/kingbird-2026-10-05-pictures.json"


def _serving(
    answers: Mapping[str, tuple[bytes, str | None]],
) -> Callable[[str], tuple[bytes, str | None]]:
    return answers.__getitem__


def _retained_from_picture(tmp_path: Path, *, parse: bool = False) -> Path:
    plan = DerivationPlan(
        n=4,
        source_n=4,
        listed_n=(3, 4),
        source_path="square-4.svg",
        url=KINGBIRD_PICTURE,
        catalogue_side=SYNTHETIC_SIDE,
        witness_path=tmp_path / "n-004.yaml",
    )
    witness = derive_tool.derive_witness(
        plan,
        SYNTHETIC_PARSE if parse else SYNTHETIC_SVG,
        catalogue_text=REMOVAL_LICENCE,
        frontier_root=tmp_path,
        parse_revision=PARSE_REVISION if parse else None,
    )
    plan.witness_path.write_text(
        derive_tool.witness_document(witness, schema="x"), encoding="utf-8"
    )
    return plan.witness_path


def test_a_pictures_credits_are_its_comments_first_paragraph() -> None:
    assert derive_tool.picture_credits(CREDITED_SVG) == (
        "Found by A. Person on May 1, 2026.",
        "Optimized by B. Person on May 2, 2026.",
    )
    assert derive_tool.picture_credits(SYNTHETIC_SVG) == ()


@pytest.mark.usefixtures("synthetic_corpus")
def test_a_witness_is_read_again_against_its_picture(tmp_path: Path) -> None:
    _retained_from_picture(tmp_path)
    served = {KINGBIRD_PICTURE: (CREDITED_SVG.encode(), "Thu, 24 Sep 2026 16:37:57 GMT")}
    readings, refusals = derive_tool.compare_pictures(
        [3, 4], out_root=tmp_path, fetch=_serving(served)
    )

    assert refusals == []
    (reading,) = readings
    assert reading.identical
    assert not reading.from_parse
    assert reading.credits[0] == "Found by A. Person on May 1, 2026."
    receipt = derive_tool.picture_receipt(
        readings, refusals, retrieved_utc="2026-10-05T23:00:00Z"
    )
    assert (receipt["compared"], receipt["identical"], receipt["agree_to_one_ulp"]) == (1, 1, 1)


@pytest.mark.usefixtures("synthetic_corpus")
def test_a_witness_read_from_a_parse_agrees_with_its_picture_to_one_ulp(tmp_path: Path) -> None:
    _retained_from_picture(tmp_path, parse=True)
    moved = SYNTHETIC_SVG.replace('width="2" height="2"', 'width="2" height="2" x="0.25"')
    served = {KINGBIRD_PICTURE: (SYNTHETIC_SVG.encode(), None)}
    shifted = {KINGBIRD_PICTURE: (moved.encode(), None)}

    (same,), _ = derive_tool.compare_pictures([4], out_root=tmp_path, fetch=_serving(served))
    (other,), _ = derive_tool.compare_pictures([4], out_root=tmp_path, fetch=_serving(shifted))

    assert same.from_parse
    assert same.same_side
    assert same.worst <= 1
    assert other.worst > 1
    assert derive_tool.report_pictures([other], []) == 1


def test_every_retained_kingbird_witness_agreed_with_the_pictures_of_5_october() -> None:
    receipt = safe_load(PICTURES.read_text(encoding="utf-8"))
    readings = {row["n"]: row for row in receipt["readings"]}
    assert receipt["refused"] == []
    assert receipt["compared"] == receipt["agree_to_one_ulp"] == len(readings) == 98
    retained = {
        int(path.stem.removeprefix("n-"))
        for path in WITNESSES.glob("n-*.yaml")
        if "kingbird.myphotos.cc" in path.read_text(encoding="utf-8")
    }
    # This is the frozen 98-picture audit of 5 October. Later packings can replace
    # active witnesses without changing which pictures this receipt actually checked.
    assert retained <= set(readings)
    assert all(row["identical"] or row["worst_ulp"] <= 1 for row in readings.values())
    for n in (69, 83, 87):
        assert readings[n]["from_parse"]
        assert readings[n]["same_side"]
        assert readings[n]["worst_ulp"] <= 1
