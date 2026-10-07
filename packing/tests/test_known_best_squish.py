"""SQUISH source selection and exact geometry at the atlas boundary."""

from __future__ import annotations

import copy
from fractions import Fraction

import pytest

from devtools import build_known_best_atlas as atlas
from devtools import squish_upper_bound_packets as squish
from sqpack.render.model import EvidenceTier
from sqpack.witness import check_witness_semantics


def _case(n: int, side: str, source_key: str) -> atlas.FrontierCase:
    return atlas.FrontierCase(n, side, atlas.FRONTIER / f"n-{n:03d}.md", "", source_key)


@pytest.mark.parametrize("n", [108, 153])
def test_squish_release_and_supplement_select_exact_facts(n: int) -> None:
    fact = squish.read_fact(n)
    case = _case(n, fact["printed_side"], squish.source_key(n))
    plan = atlas._source_plan(case, {}, {})  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    assert plan.kind == atlas.PACKET_KIND
    assert plan.path == squish.fact_path(n)
    assert plan.url == squish.source_url(n)
    index = atlas._source_index({n: plan})  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    source = index["sources"][0]
    assert source["raw_asset_retained"] is False
    assert source["license_status"] == "no-licence-published"
    assert squish.AUTHOR in source["attribution"]


@pytest.mark.parametrize(("n", "key_n"), [(153, 108), (108, 153), (109, 108)])
def test_squish_keys_refuse_counts_outside_their_release(n: int, key_n: int) -> None:
    case = _case(n, "12.1", squish.source_key(key_n))
    with pytest.raises(ValueError, match="retains no facts"):
        atlas._source_plan(case, {}, {})  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001


def test_squish_atlas_verifies_exact_corners_and_preserves_source_display() -> None:
    fact = squish.read_fact(108)
    case = _case(108, fact["printed_side"], squish.source_key(108))
    plan = atlas._source_plan(case, {}, {})  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    witness = atlas._build_witness(case, plan)  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    assert not check_witness_semantics(witness)
    assert witness["id"] == "W-known-best-n108"
    assert witness["representation"] == "corners"
    assert witness["scalar"]["kind"] == "rational"
    assert witness["side"] == fact["side"]
    assert witness["certificate"]["result"]["verification_passed"]
    assert witness["source"]["key"] == squish.source_key(108)
    assert witness["source"]["path"] == plan.path.relative_to(atlas.ROOT).as_posix()
    assert "not a legal conclusion" in witness["claim"]["limitations"]
    frame = atlas.frame_from_witness(witness)
    assert frame.evidence == EvidenceTier.CERTIFIED_UPPER_BOUND
    assert len(frame.squares) == 108
    assert (
        "packing-witness verify witnesses/known-best/n-108.yaml"
        in (witness["certificate"]["replay"])
    )


@pytest.mark.parametrize("mutation", ["display", "overlap", "outside"])
def test_squish_atlas_refuses_changed_bound_or_infeasible_exact_geometry(
    monkeypatch: pytest.MonkeyPatch, mutation: str
) -> None:
    # A small-denominator grid keeps the complete 108-square exact check cheap while
    # testing the same adapter, including failures beyond a source's display digits.
    fact = {
        "n": 108,
        "side": "111/10",
        "printed_side": "11.1000000000000000",
        "squares": [
            {
                "x": str(Fraction(index % 11) + Fraction(1, 2)),
                "y": str(Fraction(index // 11) + Fraction(1, 2)),
                "t": "0",
            }
            for index in range(108)
        ],
    }
    case = _case(108, fact["printed_side"], squish.source_key(108))
    plan = atlas._source_plan(case, {}, {})  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    altered = copy.deepcopy(fact)
    if mutation == "display":
        altered["printed_side"] = "11.1000000000000001"
    elif mutation == "overlap":
        altered["squares"][1] = altered["squares"][0].copy()
    else:
        altered["squares"][0]["x"] = "0"
    monkeypatch.setattr(squish, "read_fact", lambda _n: altered)
    message = "source display" if mutation == "display" else "exact feasibility"
    with pytest.raises(ValueError, match=message):
        atlas._build_witness(case, plan)  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
