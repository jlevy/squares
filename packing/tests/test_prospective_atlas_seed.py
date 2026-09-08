#!/usr/bin/env python3
"""Controls for the retired prospective atlas seed.

The seed itself is gone: 101 witnesses and 101 house renderings were removed on
2026-09-07, when the known-best atlas widened to cover the whole audited
`n = 101..324` range under the same retention policy. What is checked here is that the
retirement is a pointer rather than a hole -- the record validates, names the successor
that really holds those cases, keeps the source-availability map that is still this
collection's provenance, and cannot be read as an annotation source -- and that neither
the files nor the builder that wrote them can come back by accident.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema_rs import Draft202012Validator

from devtools import build_prospective_atlas as prospective
from devtools.build_prospective_atlas import MANIFEST, retired_record, retirement_errors
from sqpack.yamlio import load_yaml

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
SOURCE_MAP = ROOT / "atlas/prospective/source-availability-101-324.json"
SCHEMA = ROOT / "atlas/prospective/prospective-atlas-seed.schema.yaml"


def _seed_shaped_record() -> dict:
    """A record in the shape this collection carried until 2026-09-07.

    Synthetic rather than recovered from git: what the retired branch has to stay
    exclusive against is the *shape*, and a test that shelled out to `git show` would be
    measuring the history's availability instead. The four UnitSquare cases and the 97
    generated grids are the real selection, so the counts the seed branch pins are met.
    """
    unitsquare = (103, 105, 110, 131)
    grids = [n for n in range(101, 300) if n not in unitsquare][:97]
    entries = []
    for n in sorted([*grids, *unitsquare]):
        source = (
            {
                "derivation": "complete normalization of the retained six-decimal source SVG",
                "kind": "unitsquare-rendering",
                "path": f"packing/resources/web/prospective-packings/unitsquare/n{n:03d}.svg",
                "source_key": "unitsquare-release-1",
                "url": f"https://www.hmbelvedere.com/packings/n{n:03d}.svg",
            }
            if n in unitsquare
            else {
                "derivation": "canonical row-major subset of the exact catalogue-rule grid",
                "kind": "exact-generated-grid",
                "source_key": "catalogue-trivial-grid-rule",
            }
        )
        entries.append(
            {
                "annotation_status": "prohibited-uncomputed",
                "n": n,
                "rendering": {
                    "path": f"atlas/prospective/rendering/n-{n:03d}.svg",
                    "renderer": "sqpack deterministic house renderer",
                },
                "source": source,
                "witness": {
                    "coordinate_provenance": "numerically-checked",
                    "id": f"W-prospective-source-n{n:03d}",
                    "method": "numerical-multiprecision",
                    "path": f"witnesses/prospective/n-{n:03d}.yaml",
                },
            }
        )
    return {
        "annotation_policy": "No contact, chunk, rigidity, or grammar annotations.",
        "entries": entries,
        "excluded": {
            "count": 123,
            "reason": "Kingbird acquisition is deferred pending license review.",
            "source_key": "kingbird-current-catalogue",
        },
        "generated_by": "python -m devtools.build_prospective_atlas",
        "rendering_policy": "repository deterministic house renderer",
        "retained_sources": [
            {
                "bytes": 1,
                "creator": "UnitSquare Project",
                "license": "CC-BY-4.0-in-dataset-page-metadata",
                "n": n,
                "path": f"packing/resources/web/prospective-packings/unitsquare/n{n:03d}.svg",
                "retrieved": "2026-08-26",
                "url": f"https://www.hmbelvedere.com/packings/n{n:03d}.svg",
            }
            for n in unitsquare
        ],
        "selection": {
            "count": 101,
            "exact_generated_grid_cases": 97,
            "unitsquare_rendering_cases": 4,
        },
        "source_map": {"path": "packing/atlas/prospective/source-availability-101-324.json"},
        "status": "partial-prospective-corpus-seed-not-hypothesis-evidence",
    }


def test_the_retired_record_validates_and_points_at_the_known_best_atlas() -> None:
    record = retired_record()
    assert not retirement_errors(record)
    assert record["status"] == "retired-2026-09-07"
    assert record["retired_on"] == "2026-09-07"
    assert record["range"] == {"count": 224, "first_n": 101, "last_n": 324}
    assert record["retired_seed"] == {"house_renderings": 101, "witnesses": 101}

    successor = ROOT / record["superseded_by"]["path"]
    assert successor == ROOT / "atlas/known-best/manifest.json"
    assert successor.is_file()
    # The pointer has to resolve to the collection that actually holds these cases, not
    # merely to a file that exists: a retirement whose successor indexes nothing in the
    # retired range is a hole with a link in it.
    atlas = json.loads(successor.read_text(encoding="utf-8"))["atlas"]
    covered = {entry["n"] for entry in atlas["entries"]}
    assert covered >= set(range(101, 201))


def test_the_retired_record_is_not_an_annotation_source() -> None:
    """`D4`'s boundary survives the retirement, in the record a reader would find.

    The seed carried `annotation_status: prohibited-uncomputed` on every entry, and the
    entries are gone. Carrying it on the retirement record itself is what stops the
    prohibition from being deleted along with the thing it applied to.
    """
    record = retired_record()
    assert record["annotation_status"] == "prohibited-uncomputed"
    assert record["entries"] == []
    assert "chunk" in record["annotation_policy"]
    assert "rigidity" in record["annotation_policy"]


def test_the_source_availability_map_stays_as_the_provenance_record() -> None:
    """Half the collection is retired and half is not, and the halves are different.

    The seed was a local retention of geometry, superseded by a collection that retains
    the same cases better. The map is the audit of what sources exist for the range and
    under what terms, which nothing supersedes -- so the record still names it, and it
    is still on disk.
    """
    record = retired_record()
    assert REPO / record["source_map"]["path"] == SOURCE_MAP
    assert SOURCE_MAP.is_file()


def test_no_seed_witness_or_house_rendering_remains() -> None:
    assert not (ROOT / "witnesses/prospective").exists()
    assert not (ROOT / "atlas/prospective/rendering").exists()
    assert prospective.returned_seed_files() == []
    assert MANIFEST.is_file()


def test_a_returned_seed_file_fails_the_check(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The emptiness is measured, not assumed.

    Without this, `test_no_seed_witness_or_house_rendering_remains` and the check both
    pass on any tree at all, including one where the glob is broken and reports nothing
    whatever is on disk.
    """
    returned = tmp_path / "witnesses/prospective"
    returned.mkdir(parents=True)
    (returned / "n-101.yaml").write_text("id: W-prospective-source-n101\n", encoding="utf-8")
    monkeypatch.setattr(prospective, "WITNESS_ROOT", returned)
    assert prospective.returned_seed_files() != []
    with pytest.raises(ValueError, match="retired seed file is back"):
        prospective.check()


def test_update_refuses_and_names_the_builder_that_owns_the_range() -> None:
    with pytest.raises(SystemExit) as refusal:
        prospective.update()
    message = str(refusal.value)
    assert "retired" in message
    assert "devtools.build_known_best_atlas" in message

    with pytest.raises(SystemExit):
        prospective.main(["--update"])
    assert prospective.main(["--check"]) == 0


def test_the_retirement_cross_fields_reject_a_broken_pointer_and_a_returned_seed() -> None:
    """`retirement_errors` is what the schema cannot say, so each mutation is refused.

    The schema pins every constant in the record, which is most of it. What it cannot
    see is the tree around the file: a successor or a source map that is not there, a
    date that disagrees with the status it is embedded in, and an entry list that has
    started indexing something again. Those are the four ways this retirement could stop
    being true while still validating.
    """
    record = retired_record()
    assert not retirement_errors(record)

    missing_successor = json.loads(json.dumps(record))
    missing_successor["superseded_by"]["path"] = "atlas/known-best/manifest.json/nowhere"
    assert retirement_errors(missing_successor)

    missing_source_map = json.loads(json.dumps(record))
    missing_source_map["source_map"]["path"] = "packing/atlas/prospective/gone.json"
    assert retirement_errors(missing_source_map)

    wrong_date = json.loads(json.dumps(record))
    wrong_date["retired_on"] = "2026-09-06"
    assert retirement_errors(wrong_date)

    indexing_again = json.loads(json.dumps(record))
    indexing_again["entries"] = [{"n": 101}]
    assert retirement_errors(indexing_again)

    wrong_generator = json.loads(json.dumps(record))
    wrong_generator["generated_by"] = "python -m devtools.build_known_best_atlas"
    assert retirement_errors(wrong_generator)


def test_the_schema_still_reads_the_seed_shape_it_retired() -> None:
    """History has to stay readable, which is why the seed shape is still in the schema.

    A reader who recovers the 2026-09-06 manifest from git needs a validator that
    accepts it; a `oneOf` that had dropped the seed branch would report the record this
    collection carried for twelve days as invalid. The two branches also have to stay
    exclusive, so the retirement cannot be mistaken for a seed with 101 cases missing.
    """
    schema = load_yaml(SCHEMA.read_text(encoding="utf-8"))
    assert [branch["$ref"] for branch in schema["oneOf"]] == [
        "#/$defs/seed",
        "#/$defs/retired",
    ]
    whole = Draft202012Validator(schema)
    seed_only = Draft202012Validator({**schema["$defs"]["seed"], "$defs": schema["$defs"]})
    retired_only = Draft202012Validator(
        {**schema["$defs"]["retired"], "$defs": schema["$defs"]}
    )

    seed = _seed_shaped_record()
    retired = retired_record()
    assert whole.is_valid(seed)
    assert whole.is_valid(retired)
    # Exclusive in both directions, so a retirement cannot pass as a seed that has lost
    # its 101 cases, and a live seed cannot pass as a retirement.
    assert seed_only.is_valid(seed)
    assert not seed_only.is_valid(retired)
    assert retired_only.is_valid(retired)
    assert not retired_only.is_valid(seed)


def test_the_four_retained_unitsquare_svgs_are_not_part_of_the_retirement() -> None:
    """They are the known-best collection's sources now, and they stay where they are.

    `build_known_best_atlas` resolves a UnitSquare case by looking in both roots rather
    than by range, so moving these four would move bytes the successor reads, under a
    digest declaration that is a fact about where they were retrieved. The retirement
    removes what this collection generated, never what it acquired.
    """
    retained = ROOT / "resources/web/prospective-packings/unitsquare"
    assert sorted(path.name for path in retained.glob("*.svg")) == [
        "n103.svg",
        "n105.svg",
        "n110.svg",
        "n131.svg",
    ]
    record = retired_record()
    assert "prospective-packings" not in json.dumps(record, sort_keys=True)
    assert not hasattr(prospective, "fetch")
    assert prospective.parser().parse_args(["--check"]).check
    with pytest.raises(SystemExit):
        prospective.parser().parse_args(["--fetch"])
