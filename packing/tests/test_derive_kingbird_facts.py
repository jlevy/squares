#!/usr/bin/env python3
"""What the one-time Kingbird acquisition pass may retain, drop, and refuse.

Nothing here reaches the network. `urllib.request.urlopen` is replaced in every test
that fetches, so a test that starts making requests fails loudly rather than quietly
becoming a live audit of someone's website.
"""

from __future__ import annotations

import urllib.error
import urllib.request
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
from sqpack.known_best import parse_kingbird_svg
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
    """The two methods `fetch_svg` uses of a `urlopen` result, and nothing else."""

    def __init__(self, payload: bytes) -> None:
        self.payload: bytes = payload

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
