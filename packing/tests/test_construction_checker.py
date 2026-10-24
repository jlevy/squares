"""The construction checker: recipe rows decided exactly from the recipe and a replayed parent.

`devtools.construction_checker` is D2's maintained checker (think-f2io; think-llit's plan,
Recipe Rows). The refusals come first, each before any positive counts: the controls every
recipe carries, a parent that fails both routes (the duplicate-square control), a parent
not yet replayed, Friedman's classical parent (think-zkxy), and a Fang composite with
unstated parts. Then the positives: #763's recipes whose parents its packet replays, decided
from the retained parents held to their SHA-256; the capacity of each of #715's 68 replayed
L-border and deletion files; and a small replayed certificate tiled with t = 2, written out
and decided on both routes.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import beyond_horizon_replay as replay
from devtools import construction_checker as checker
from devtools import couzo_678_replay as base
from devtools import evand_exact_certificates as legacy
from devtools.retained_data import read_retained_bytes, read_retained_text

I763 = replay.WEB / "couzo-issue763-2026-10-23"
I715 = replay.WEB / "couzo-issue715-2026-10-21"
#: A small exact certificate the record retains, for the tiling fixture.
SMALL = replay.WEB / "couzo-exact-certificates-2026-10-09/source/certificates/n68.cert"


def _read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _recipes_763() -> list[dict[str, Any]]:
    """#763's recipes to 1024, which its walk holds on think-g2qy."""
    claims = _read(I763 / "receipts/claim-map.json")["claims"]
    return [item for item in claims if item["kind"] == "construction" and item["n"] <= 1024]


def _parent_763(item: dict[str, Any]) -> checker.Parent:
    """A #763 recipe's parent: the retained certificate the claim map names, held to its
    SHA-256, at its exact header side, with #763's filtered receipt row for it if any."""
    raw = read_retained_bytes(I763 / "source" / item["certificate"])
    rows = {row["n"]: row for row in _read(I763 / replay.FILTERED)["rows"]}
    n = item["construction"]["source_n"]
    row = rows.get(n)
    return checker.Parent(
        n=n,
        side=replay.header_side(raw, n, item["certificate"]),
        path=item["certificate"],
        sha256=hashlib.sha256(raw).hexdigest(),
        replay=row if row is not None and row["certificate"] == item["certificate"] else None,
    )


def _decided(
    certificate: legacy.Certificate, path: str, *, controls: bool = True
) -> dict[str, Any]:
    """A certificate decided on both routes, with its six controls unless ``controls`` is
    False, as a receipt row."""
    result = base.decide(base.geometry(certificate))
    return {
        "n": certificate.n,
        "certificate": path,
        "certificate_sha256": hashlib.sha256(
            legacy.serialize(certificate).encode()
        ).hexdigest(),
        "exact_side": legacy.literal(certificate.side),
        "verified": result["passed"],
        "decision": result,
        "controls": base.decide_controls(certificate) if controls else [],
    }


def test_every_recipe_control_is_refused() -> None:
    """Each control a recipe carries is refused, for the reason it names."""
    item = next(item for item in _recipes_763() if item["n"] == 444)
    recipe, parent = checker.recipe_from_index(item), _parent_763(item)
    assert checker.decide(recipe, parent)["verdict"] == checker.DECIDED
    found = {row["control"]: row for row in checker.controls(recipe, parent)}
    assert all(row["refused"] for row in found.values()), found
    assert "above the capacity 444" in found["count above the capacity"]["reason"]
    assert "is not tS + L" in found["bound one unit below"]["reason"]
    assert "by path and SHA-256" in found["parent digest altered"]["reason"]
    assert "the recipe names n404" in found["parent count wrong"]["reason"]
    assert found["no tiles"]["reason"].startswith("t = 0")
    assert found["negative layers"]["reason"].startswith("t = 1, L = -1")
    assert "is not replayed" in found["parent not replayed"]["reason"]
    assert "not a recipe this checker reads" in found["unknown kind"]["reason"]
    assert "deletes 444 of the 444 squares" in found["deletes every square"]["reason"]


def test_a_parent_that_fails_both_routes_is_refused() -> None:
    """The duplicate-square control of a replayed parent fails both routes, so a recipe on
    it is refused even with the parent's path, digest and count."""
    item = next(item for item in _recipes_763() if item["n"] == 444)
    recipe, parent = checker.recipe_from_index(item), _parent_763(item)
    raw = read_retained_text(I763 / "source" / item["certificate"])
    duplicated = base.mutant_certificate(legacy.parse(raw), "duplicate-square")
    failed = _decided(duplicated, parent.path, controls=False)
    failed["certificate_sha256"] = parent.sha256
    assert not failed["verified"]
    with pytest.raises(checker.RecipeRefusedError, match="did not pass both routes"):
        checker.decide(recipe, dataclasses.replace(parent, replay=failed))
    assert parent.replay is not None
    stored = dict(parent.replay)
    accepted = [{**row, "refused_by_independent": False} for row in stored["controls"]]
    with pytest.raises(checker.RecipeRefusedError, match="six controls are not all refused"):
        checker.decide(
            recipe, dataclasses.replace(parent, replay={**stored, "controls": accepted})
        )


def test_a_parent_not_yet_replayed_is_refused() -> None:
    """#763's 365 builds on 328, and 909 and 970 on 850, none of which its packet replays
    (850 restates f1ceee4, think-fwa9): the records slice replays such parents first."""
    refused = []
    for item in _recipes_763():
        parent = _parent_763(item)
        if parent.replay is None:
            with pytest.raises(checker.RecipeRefusedError, match="is not replayed"):
                checker.decide(checker.recipe_from_index(item), parent)
            refused.append(item["n"])
    assert refused == [365, 909, 970]


def test_friedman_s_parent_and_a_fang_composite_are_refused() -> None:
    """A recipe on Friedman's off-centre family has a classical construction for a parent,
    which the record does not replay (think-zkxy); a composite of Kevin Fang's table with no
    parts stated is refused, and so is one with parts, since no rule here reads a composite."""
    item = next(item for item in _recipes_763() if item["n"] == 444)
    recipe, parent = checker.recipe_from_index(item), _parent_763(item)
    friedman = dataclasses.replace(parent, classical="Friedman's off-centre family")
    with pytest.raises(checker.RecipeRefusedError, match=r"classical construction.*think-zkxy"):
        checker.decide(recipe, friedman)
    composite = dataclasses.replace(recipe, kind=checker.COMPOSITE)
    with pytest.raises(checker.RecipeRefusedError, match="parts its table does not state"):
        checker.decide(composite, parent)
    with pytest.raises(checker.RecipeRefusedError, match="no rule here reads one"):
        checker.decide(dataclasses.replace(composite, parts=("n027_j1",)), parent)
    deletion = dataclasses.replace(recipe, kind=checker.DELETION, layers=0, deleted=404, n=-1)
    with pytest.raises(checker.RecipeRefusedError, match="deletes 404 of the 403 squares"):
        checker.decide(deletion, parent)


def test_763_s_recipes_on_replayed_parents_are_decided_exactly() -> None:
    """Each of #763's recipes to 1024 whose parent its packet replays is decided from the
    retained parent, held to the SHA-256 the claim map states: the stated bound is tS + L
    and the stated capacity the lemma's, with every control refused."""
    decided = []
    for item in _recipes_763():
        parent = _parent_763(item)
        if parent.replay is None:
            continue
        recipe = checker.recipe_from_index(item)
        result = checker.decide(recipe, parent)
        assert Fraction(result["side"]) == Fraction(item["exact"])
        assert result["capacity"] == item["construction"]["capacity"]
        assert all(row["refused"] for row in checker.controls(recipe, parent))
        decided.append(item["n"])
    assert decided == [444, 487, 632, 733, 734, 737, 788, 789, 845, 910, 966]


def test_the_capacity_of_each_of_715_s_replayed_constructions() -> None:
    """#715's filtered receipt holds 59 L-border files and 13 deletion rows to 1024, each
    written out in full and verified on both routes against its parent: its first poses the
    parent's, the rest axis-aligned, its side the parent's plus its layers. For each, the
    lemma's capacity less the stated deletions is the count the file holds."""
    rows = [
        row
        for row in _read(I715 / "receipts/filtered-exact-replay.json")["rows"]
        if row["source_index"]["kind"] == "construction"
        or row["source_index"]["deleted_squares"]
    ]
    assert len(rows) == 68
    assert sum(1 for row in rows if row["source_index"]["kind"] == "construction") == 59
    assert sum(1 for row in rows if row["source_index"]["deleted_squares"]) == 13
    for row in rows:
        index = row["source_index"]
        assert row["verified"]
        assert index["parent_poses_lead"]
        assert index["side_is_parent_side_plus_layers"]
        assert index["added_squares_axis_aligned"]
        t, layers = index["tiles_per_side"], index["layers"]
        kind = checker.TILING if index["kind"] == "construction" else checker.DELETION
        side = (Fraction(row["exact_side"]) - layers) / t
        recipe = checker.Recipe(
            n=row["n"],
            kind=kind,
            source_n=index["parent_n"],
            parent=index["parent"],
            parent_sha256="",
            bound=Fraction(row["exact_side"]),
            tiles_per_side=t,
            layers=layers,
            deleted=index["deleted_squares"],
        )
        assert checker.capacity(recipe, side) - recipe.deleted == row["n"], row["n"]


def test_a_tiled_certificate_written_out_is_decided_on_both_routes() -> None:
    """None of #715's constructions tiles (t = 1 throughout), so a small certificate the
    record retains, decided here on both routes with its six controls, is tiled with t = 2
    and one L-border layer: the packing written out passes both routes, holds the lemma's
    capacity at side 2S + 1, and the checker decides the recipe to the same side."""
    text = read_retained_text(SMALL)
    small = legacy.parse(text, expected_n=68)
    row = _decided(small, "certificates/n68.cert")
    row["certificate_sha256"] = hashlib.sha256(text.encode()).hexdigest()
    assert row["verified"]
    assert all(
        item["refused_by_sqpack"] and item["refused_by_independent"] for item in row["controls"]
    )
    parent = checker.parent_from_replay(row)
    held = checker.capacity(
        checker.Recipe(0, checker.TILING, 68, "", "", Fraction(0), 2, 1), small.side
    )
    recipe = checker.Recipe(
        n=held - 2,
        kind=checker.TILING,
        source_n=68,
        parent=parent.path,
        parent_sha256=parent.sha256,
        bound=2 * small.side + 1,
        tiles_per_side=2,
        layers=1,
        deleted=2,
        capacity=held,
    )
    written = checker.write_out(recipe, small)
    assert (written.n, written.side) == (held - 2, 2 * small.side + 1)
    assert base.decide(base.geometry(written))["passed"]
    result = checker.decide(recipe, parent)
    assert (result["capacity"], Fraction(result["side"])) == (held, written.side)
    assert all(item["refused"] for item in checker.controls(recipe, parent))
