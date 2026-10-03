"""The kernel's memos: the checker's facet cache, the producer's collision terms, and the
cover backend of a saved check. Each memo must change no value, no verdict and no count."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

import pytest

from devtools import check_n17_subpattern as tool
from devtools.check_hull_kernel_mask0 import n17_unique_frame
from sqpack.hull_kernel import Budget, RefusalError, collision, node, producer, sequential
from sqpack.hull_kernel.frame import Frame, make_frame
from sqpack.hull_kernel.induction import convex, hull
from sqpack.hull_kernel.node import points
from sqpack.hull_kernel.rational import Q


def budget() -> Budget:
    return Budget(time.monotonic() + 120, 200_000)


@pytest.fixture(scope="module")
def blind_pair() -> Frame:
    triangle = [(Q(1), Q(1)), (Q(19, 10), Q(1)), (Q(29, 20), Q(89, 50))]
    shifted = [(x + Q(1, 100), y) for x, y in triangle]
    return make_frame(
        name="blind-pair",
        cap=Q(3),
        length=Q(3),
        cells=[triangle, shifted],
        cell_names=["left", "right"],
        occupancy=2,
        action_names=("r0",),
    )


@pytest.fixture(scope="module")
def production(blind_pair: Frame) -> producer.Production:
    return producer.produce(blind_pair, [0, 1], bins=16, max_rounds=2, budget=budget())


def collision_step(production: producer.Production) -> tuple[dict[str, Any], dict[str, Any]]:
    """A step with a collision region, and the row that carries it."""
    for step in production.node["steps"]:
        for row in step["rows"]:
            if row["collision_regions"]:
                return step, row
    raise AssertionError("the blind pair closes through collision")


def partner_rows(step: dict[str, Any], partner: int) -> list[tuple[list[Any], list[Any]]]:
    return [
        (hull(points(item["domain"])), convex(points(item["core"])))
        for item in step["prior_partner_pose_covers"][str(partner)]
        if item["domain"]
    ]


def test_the_cached_collision_check_is_the_reference_check(
    production: producer.Production,
) -> None:
    step, row = collision_step(production)
    core = convex(points(row["core_vertices"]))
    domain = convex(points(row["input_domain"]))
    item = row["collision_regions"][0]
    region = convex(points(item["vertices"]))
    rows = partner_rows(step, item["partner"])
    prepared = collision.prepare_rows(rows)
    facets: collision.FacetCache = {}
    reference = collision.integer_universal_collision(
        core, domain, rows, region, budget=budget()
    )
    cached = collision.cached_universal_collision(
        core, domain, prepared, region, budget=budget(), facets=facets
    )
    assert cached == reference > 0
    assert 0 < len(facets) <= len(rows)
    # The memo is read back on a second pass, with the same count.
    again = collision.cached_universal_collision(
        core, domain, prepared, region, budget=budget(), facets=facets
    )
    assert again == reference
    assert all(len(found) >= 3 for found in facets.values())
    # Mixed input: prepared rows stay, raw pairs are prepared.
    mixed = collision.as_prepared([prepared[0], rows[1]])
    assert mixed[0] is prepared[0]
    assert mixed[1].domain == rows[1][0]
    # A region pushed past its tightest facet is refused by both forms.
    forged = [(x + Q(1, 2), y) for x, y in region]
    for check in (
        lambda: collision.integer_universal_collision(
            core, domain, rows, forged, budget=budget()
        ),
        lambda: collision.cached_universal_collision(
            core, domain, prepared, forged, budget=budget(), facets=facets
        ),
    ):
        with pytest.raises(RefusalError, match="escapes"):
            _ = check()


def test_a_prepared_row_needs_a_domain_and_a_core_of_positive_area() -> None:
    square = [(Q(0), Q(0)), (Q(1), Q(0)), (Q(1), Q(1)), (Q(0), Q(1))]
    with pytest.raises(RefusalError, match="partner core or domain"):
        _ = collision.prepare_rows([([], square)])
    with pytest.raises(RefusalError, match="partner core or domain"):
        _ = collision.prepare_rows([(square, square[:2])])
    (prepared,) = collision.prepare_rows([(square, square)])
    assert prepared.minimum(2, 0) == (0, 1)
    assert prepared.minimum(-2, -2) == (-4, 1)
    assert prepared.minima == {(1, 0): (0, 1), (-1, -1): (-2, 1)}


def test_the_cached_collision_planes_are_the_uncached_planes(
    blind_pair: Frame, production: producer.Production
) -> None:
    step, row = collision_step(production)
    cores = producer.CoreCache("envelope")
    terms = producer.CollisionTerms()
    lo, hi = (Q(value) for value in row["interval"])
    key = (row["interval"][0], row["interval"][1])
    core = producer.cached_core(blind_pair, lo, hi, cores)
    assert core == convex(points(row["core_vertices"]))
    for partner, items in step["prior_partner_pose_covers"].items():
        for item in items:
            if not item["domain"]:
                continue
            prepared = producer.prepare_partner(
                hull(points(item["domain"])),
                convex(points(item["core"])),
                (item["interval"][0], item["interval"][1]),
            )
            uncached = producer.collision_planes(core, prepared)
            cached = producer.cached_collision_planes(key, core, prepared, terms)
            assert cached == uncached, (partner, item["interval"])
            assert producer.cached_collision_planes(key, core, prepared, terms) == uncached
    assert len(terms.cores) == 1
    assert len(terms.pairs) == len(
        {
            (item["interval"][0], item["interval"][1])
            for items in step["prior_partner_pose_covers"].values()
            for item in items
            if item["domain"]
        }
    )


def test_production_does_not_retain_partner_generations(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    frame = n17_unique_frame()
    mask = sorted(frame.cell_names.index(cell) for cell in tool.PATTERNS["W7"])
    original = producer.partner_cover
    observed: list[producer.PartnerMemo] = []
    sizes: list[int] = []

    def cover(
        frame: Frame,
        accepted: list[dict[str, Any]],
        cores: dict[Any, Any],
        memo: producer.PartnerMemo | None = None,
    ) -> tuple[list[dict[str, Any]], list[producer.PartnerRow]]:
        result = original(frame, accepted, cores, memo)
        assert memo is not None
        sizes.append(len(memo))
        if not observed:
            observed.append(memo)
        return result

    monkeypatch.setattr(producer, "partner_cover", cover)
    result = producer.produce(frame, mask, bins=8, max_rounds=6, budget=budget())
    assert len(result.node["steps"]) > len(mask)
    # A run that revisits every owner may cache one generation, never its history.
    assert max(sizes) <= len(mask) * 8
    assert len(observed[0]) <= (len(mask) - 1) * 8


def test_the_partner_memo_follows_the_accepted_row_object(
    blind_pair: Frame, production: producer.Production
) -> None:
    cores = producer.CoreCache("envelope")
    memo: producer.PartnerMemo = {}
    accepted = [
        {
            "interval": row["interval"],
            "reference": row["reference"],
            "outer_domain": row["outer_domain"],
            "residual_polygons": row["residual_polygons"],
        }
        for row in production.seed["cells"]["1"]
    ]
    given, live = producer.partner_cover(blind_pair, accepted, cores, memo)
    again, reused = producer.partner_cover(blind_pair, accepted, cores, memo)
    assert given == again
    assert all(a is b for a, b in zip(live, reused, strict=True))
    assert all(
        row.key == (row_dict["interval"][0], row_dict["interval"][1])
        for row, row_dict in zip(
            live, [r for r in accepted if r["residual_polygons"]], strict=True
        )
    )
    replaced = [dict(row) for row in accepted]
    _, fresh = producer.partner_cover(blind_pair, replaced, cores, memo)
    assert all(a is not b for a, b in zip(live, fresh, strict=True))
    assert len(memo) == 2 * len(live)
    without_memo = producer.partner_cover(blind_pair, accepted, cores)[1]
    assert [row.own for row in without_memo] == [row.own for row in live]


def test_a_saved_check_reports_the_same_cover_under_either_backend(
    blind_pair: Frame, production: producer.Production, tmp_path: Path
) -> None:
    tool.save_certificate(tmp_path, production.seed, production.node)
    indexed = tool.check_saved(tmp_path, blind_pair, max_seconds=120, require_no_producer=False)
    reference = tool.check_saved(
        tmp_path, blind_pair, max_seconds=120, require_no_producer=False, cover="reference"
    )
    assert indexed["cover_backend"] == "indexed"
    assert reference["cover_backend"] == "reference"
    for key in ("status", "steps_checked", "rows_checked", "events", "collision_regions"):
        assert indexed[key] == reference[key], key
    assert indexed["status"] == "PASS_SAVED_CLOSED"
    with pytest.raises(KeyError):
        _ = tool.check_saved(
            tmp_path, blind_pair, max_seconds=120, require_no_producer=False, cover="area"
        )
    assert sequential.COVERS["indexed"] is not sequential.COVERS["reference"]


def test_emptying_the_pair_memos_at_every_step_changes_nothing(
    blind_pair: Frame, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The producer's core-pair terms and the replay's facet memo are emptied at a step's
    start once they pass their bound. With the bound at zero they are emptied at every
    step, and the produced bytes, the checked counts and the closure are the same."""

    def produce() -> producer.Production:
        return producer.produce(
            blind_pair,
            [0, 1],
            bins=2,
            max_rounds=12,
            budget=budget(),
            split=producer.SplitPolicy(floor=64, max_rows=200),
        )

    def replay(production: producer.Production) -> sequential.SequentialTrace:
        admitted = node.admit_seed(
            blind_pair,
            production.seed,
            mask=[0, 1],
            bins=2,
            budget=budget(),
            allow_empty_groups=True,
        )
        return sequential.replay_sequential(
            blind_pair,
            production.node,
            admitted,
            mask=[0, 1],
            seed_sha256=tool.content_sha256(production.seed),
            budget=budget(),
            cover="indexed",
        )

    bounded = produce()
    bounded_trace = replay(bounded)
    monkeypatch.setattr(producer, "TERM_MEMO_PAIRS", 0)
    monkeypatch.setattr(sequential, "FACET_MEMO_PAIRS", 0)
    emptied = produce()
    assert tool.canonical_bytes(emptied.node) == tool.canonical_bytes(bounded.node)
    emptied_trace = replay(emptied)
    assert emptied_trace.steps == bounded_trace.steps
    assert emptied_trace.closure == bounded_trace.closure is not None
