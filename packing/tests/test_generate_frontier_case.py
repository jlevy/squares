#!/usr/bin/env python3
"""The generator's rules must be the rules the hand-written register already follows.

`devtools/generate_frontier_case.py` drafts a `SquarePackingCase/v2` record for an `n`
the register does not yet cover. Nothing about that is checkable by reading the output:
a record can validate, read fluently, and still carry a bound rule that the first hundred
cases do not use. So the generator is pointed back at cases a person wrote and asked to
reproduce them **field by field**, on the same inputs.

Five cases, chosen so that every branch of the generator is exercised by a record whose
correctness someone already argued:

- `n = 100` and `n = 64` -- perfect squares. The lower bound is the area bound, the
  resource block drops Nagamochi, and the roll-up carries four evidence ids.
- `n = 99` and `n = 98` -- `m^2 - 1` and `m^2 - 2`. Proved on Nagamochi's exact branch,
  reported as the integer, with the three-resource block.
- `n = 50` -- open, catalogue-sourced, with a certified ceiling that trails the report
  and the `mathematics` blocker that gap requires.

**Nothing is skipped quietly.** Every key of the front matter is compared. The three
kinds of mismatch a reader would want to know about are named separately:

- `GENERATOR_OWNS` -- must be byte-equal. A difference here is a failure.
- `SUPPLIED` -- values the generator takes as arguments because they are not derivable
  from any source: the two dates, and the two facts that live in the catalogue's credit
  line rather than in its structured row. The test passes them in and reports that it
  did, so nobody reads their agreement as a derivation.
- `NOT_REPRODUCED` -- fields the generator deliberately leaves for a later step, which
  is `rigidity` and, for `n = 100`, a hand-written body about the edge of the corpus.

`test_reports_what_the_adapter_cannot_derive` is the same comparison run through the real
catalogue parser instead of injected facts, so the report says which fields a fully
automatic run would leave at their "not reviewed yet" defaults.
"""

from __future__ import annotations

import math
import shutil
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import pytest

from devtools import validate_schemas
from devtools.check_basic_bounds import check_case_basic_bounds
from devtools.check_case_prose import check_case_file
from devtools.generate_frontier_case import (
    CATALOGUE_CLASSIFICATION,
    GRID_CLASSIFICATION,
    CatalogueFacts,
    GenerationError,
    SourceAvailability,
    facts_from_catalogue_entry,
    generate_record,
    grid_ceiling,
    load_availability,
    main,
    record_path,
    refuse_reason,
    write_record,
)
from sqpack.assurance import check_case_semantics
from sqpack.yamlio import safe_load

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FRONTIER = PROJECT_ROOT / "frontier"
SCHEMA = FRONTIER / "square-packing-case.schema.yaml"

GOLDEN_CASES = (100, 99, 98, 64, 50)

#: Front-matter paths the generator derives from its inputs and must reproduce exactly.
#: Everything not named in the two sets below falls here, so a field added to the schema
#: is compared by default rather than forgotten.
SUPPLIED = {
    "packing.source_reviewed": "the review date is an argument; no source carries it",
    "packing.reported_upper_bound.retrieved_date": (
        "the fetch date is an argument; the catalogue does not date itself"
    ),
    "packing.reported_upper_bound.construction_method": (
        "read from the catalogue's credit line, which the structured entry does not carry"
    ),
    "packing.reported_upper_bound.analytically_optimized": (
        "read from the same credit line, for the same reason"
    ),
    "packing.reported_upper_bound.improved_by": (
        "read from the same credit line, for the same reason"
    ),
}
NOT_REPRODUCED = {
    "packing.rigidity": (
        "left null on purpose: the translation-escape screen and the rigidity assessment "
        "write this field later in the promotion path"
    ),
}
#: Cases whose prose is bespoke rather than templated, and why.
BODY_NOT_REPRODUCED = {
    100: "an editorial section about the edge of the corpus, written for this one case",
}


def _availability(n: int, *, grid: bool) -> SourceAvailability:
    if grid:
        return SourceAvailability(
            n, GRID_CLASSIFICATION, "catalogue-trivial-grid-rule", grid_ceiling(n)
        )
    return SourceAvailability(n, CATALOGUE_CLASSIFICATION, "kingbird-current-catalogue", None)


def _committed(n: int) -> tuple[dict[str, Any], str]:
    """The committed record's front matter document and body."""
    text = (FRONTIER / f"n-{n:03d}.md").read_text(encoding="utf-8")
    _, front, body = text.split("---\n", 2)
    return safe_load(front), body


def _injected_facts(n: int) -> CatalogueFacts:
    """A `CatalogueFacts` built from the values the committed record transcribes.

    This is the catalogue entry as a person read it, credit line included, so the
    comparison tests the generator's assembly rather than the parser's reading.
    """
    reported = _committed(n)[0]["packing"]["reported_upper_bound"]
    return CatalogueFacts(
        n=n,
        side_decimal=str(reported["value"]),
        exact_form=reported["exact_form"],
        algebraic_degree=reported["algebraic_degree"],
        minimal_polynomial=reported["minimal_polynomial"],
        found_by=tuple(reported["found_by"]),
        found_year=reported["found_year"],
        catalogue_rigid=reported["catalogue_rigid"],
        catalogue_pictured=reported["catalogue_pictured"],
        construction_method=reported["construction_method"],
        analytically_optimized=reported["analytically_optimized"],
        improved_by=tuple(reported["improved_by"]),
    )


def _regenerate(n: int, *, facts: CatalogueFacts | None = None) -> str:
    """Draft `n` on the same inputs and dates the committed record declares."""
    document, _ = _committed(n)
    payload = document["packing"]
    grid = payload["reported_upper_bound"]["construction_method"] == "trivial-grid"
    if not grid and facts is None:
        facts = _injected_facts(n)
    return generate_record(
        n,
        availability={n: _availability(n, grid=grid)},
        catalogue=None if facts is None else {n: facts},
        review_date=str(payload["source_reviewed"]),
        retrieved_date=str(payload["reported_upper_bound"]["retrieved_date"]),
    )


def _flatten(value: object, prefix: str = "") -> dict[str, object]:
    """Dotted paths to leaf values; lists are leaves, since these are short and ordered."""
    if not isinstance(value, Mapping):
        return {prefix: value}
    flat: dict[str, object] = {}
    for key, item in value.items():
        path = f"{prefix}.{key}" if prefix else str(key)
        flat.update(_flatten(item, path))
    return flat


def _compare(n: int) -> tuple[dict[str, object], list[str]]:
    """Every front-matter path, with a verdict, plus the paths that failed."""
    committed_document, _ = _committed(n)
    generated_document = safe_load(_regenerate(n).split("---\n", 2)[1])
    committed = _flatten(committed_document)
    generated = _flatten(generated_document)

    verdicts: dict[str, object] = {}
    failures: list[str] = []
    for path in sorted(set(committed) | set(generated)):
        left = committed.get(path, "<absent>")
        right = generated.get(path, "<absent>")
        if path in SUPPLIED or any(path.startswith(f"{key}.") for key in SUPPLIED):
            verdicts[path] = "supplied"
            if left != right:
                failures.append(f"{path}: supplied {right!r} but the record says {left!r}")
        elif path in NOT_REPRODUCED or any(
            path.startswith(f"{key}.") for key in NOT_REPRODUCED
        ):
            verdicts[path] = "not reproduced"
        elif left == right:
            verdicts[path] = "reproduced"
        else:
            verdicts[path] = "MISMATCH"
            failures.append(f"{path}: record {left!r}, generated {right!r}")
    return verdicts, failures


@pytest.mark.parametrize("n", GOLDEN_CASES)
def test_regenerates_a_hand_written_record_field_by_field(n: int) -> None:
    verdicts, failures = _compare(n)
    counts = {
        verdict: sum(1 for value in verdicts.values() if value == verdict)
        for verdict in ("reproduced", "supplied", "not reproduced", "MISMATCH")
    }
    print(f"n={n}: {counts}")
    for path, verdict in verdicts.items():
        if verdict != "reproduced":
            print(f"  {verdict}: {path}")
    assert failures == [], "\n".join(failures)
    # The allowlists are not a place to hide a growing set of exceptions: exactly one
    # front-matter block is left for a later step, and it is `rigidity`.
    unreproduced = [path for path, verdict in verdicts.items() if verdict == "not reproduced"]
    assert unreproduced, "the rigidity block should be reported, not silently absent"
    assert all(path.startswith("packing.rigidity") for path in unreproduced), unreproduced


@pytest.mark.parametrize("n", GOLDEN_CASES)
def test_regenerates_the_prose_a_person_wrote(n: int) -> None:
    committed_body = _committed(n)[1]
    generated_body = _regenerate(n).split("---\n", 2)[2]
    if n in BODY_NOT_REPRODUCED:
        print(f"n={n}: body not reproduced -- {BODY_NOT_REPRODUCED[n]}")
        assert generated_body != committed_body
        return
    assert generated_body == committed_body


@pytest.mark.parametrize("n", GOLDEN_CASES)
def test_the_whole_record_is_byte_identical_apart_from_the_allowlist(n: int) -> None:
    """The only textual differences are the ones the two allowlists already named."""
    committed = (FRONTIER / f"n-{n:03d}.md").read_text(encoding="utf-8")
    generated = _regenerate(n)
    if n in BODY_NOT_REPRODUCED:
        return
    # Drop the rigidity block from the committed record and the `rigidity: null` line
    # from the generated one; nothing else may differ.
    stripped = _without_rigidity(committed)
    assert _without_rigidity(generated) == stripped


def _without_rigidity(text: str) -> str:
    lines = text.splitlines(keepends=True)
    kept: list[str] = []
    dropping = False
    for line in lines:
        if line.startswith("  rigidity:"):
            dropping = True
            continue
        if dropping:
            if line.startswith("    "):
                continue
            dropping = False
        kept.append(line)
    return "".join(kept)


def test_reports_what_the_adapter_cannot_derive() -> None:
    """The same comparison through the real parser, so the gap is named rather than assumed."""
    catalogue = pytest.importorskip("sqpack.kingbird_catalogue")
    entry = catalogue.parse_catalogue()[50]
    facts = facts_from_catalogue_entry(entry, n=50)
    generated = safe_load(_regenerate(50, facts=facts).split("---\n", 2)[1])
    committed, _ = _committed(50)

    generated_upper = generated["packing"]["reported_upper_bound"]
    committed_upper = committed["packing"]["reported_upper_bound"]
    undecided = {
        key: (committed_upper[key], generated_upper[key])
        for key in ("construction_method", "analytically_optimized", "improved_by")
    }
    print(f"n=50 through the real parser, credit-line fields: {undecided}")
    # The structured entry carries no credit line, so these three stay at the values that
    # say "not reviewed". Everything the entry does carry must still agree.
    assert generated_upper["construction_method"] == "unknown"
    assert generated_upper["analytically_optimized"] is None
    assert generated_upper["improved_by"] == []
    for key in ("value", "exact_form", "algebraic_degree", "minimal_polynomial"):
        assert generated_upper[key] == committed_upper[key], key
    for key in ("found_by", "found_year", "catalogue_rigid", "catalogue_pictured"):
        assert generated_upper[key] == committed_upper[key], key


@pytest.mark.parametrize("n", GOLDEN_CASES)
def test_a_regenerated_record_validates_and_replays(n: int, tmp_path: Path) -> None:
    """Schema, cross-field assurance, bound instantiation and prose, on generated bytes."""
    shutil.copy(SCHEMA, tmp_path / SCHEMA.name)
    path = record_path(tmp_path, n)
    write_record(_regenerate(n), path)
    assert validate_schemas.check(path) == []

    payload = safe_load(path.read_text(encoding="utf-8").split("---\n")[1])["packing"]
    evidence = {
        record["id"]: record
        for record in safe_load((FRONTIER / "evidence.yaml").read_text(encoding="utf-8"))[
            "evidence"
        ]
    }
    assert check_case_semantics(payload, evidence) == []
    assert check_case_basic_bounds(payload) == []
    assert [finding.render() for finding in check_case_file(path)] == []


def test_generated_cases_past_the_register_validate(tmp_path: Path) -> None:
    """A sample of the new range, over both classifications and both statuses."""
    catalogue_module = pytest.importorskip("sqpack.kingbird_catalogue")
    availability = load_availability()
    catalogue = {
        n: facts_from_catalogue_entry(entry, n=n)
        for n, entry in catalogue_module.parse_catalogue().items()
    }
    shutil.copy(SCHEMA, tmp_path / SCHEMA.name)
    for n in (101, 111, 119, 121, 123, 324):
        path = record_path(tmp_path, n)
        write_record(
            generate_record(
                n,
                availability=availability,
                catalogue=catalogue,
                review_date="2026-09-07",
                retrieved_date="2026-09-07",
            ),
            path,
        )
        assert validate_schemas.check(path) == [], n
        payload = safe_load(path.read_text(encoding="utf-8").split("---\n")[1])["packing"]
        assert check_case_basic_bounds(payload) == [], n
        assert [finding.render() for finding in check_case_file(path)] == [], n
        # The register's own evidence records are still scoped to n <= 100, so
        # `check_case_semantics` cannot pass here yet. That widening is a separate
        # change, and this test does not pretend it has happened.
        assert payload["rigidity"] is None


def test_the_new_range_proves_exactly_the_twenty_four_cases_the_plan_names() -> None:
    """`k^2`, `k^2 - 1` and `k^2 - 2` for `k = 11..18`, and nothing else in 101..324."""
    catalogue_module = pytest.importorskip("sqpack.kingbird_catalogue")
    availability = load_availability()
    catalogue = {
        n: facts_from_catalogue_entry(entry, n=n)
        for n, entry in catalogue_module.parse_catalogue().items()
    }
    proved: list[int] = []
    for n in sorted(availability):
        text = generate_record(
            n,
            availability=availability,
            catalogue=catalogue,
            review_date="2026-09-07",
            retrieved_date="2026-09-07",
        )
        payload = safe_load(text.split("---\n")[1])["packing"]
        if payload["status"] == "proved":
            proved.append(n)
    expected = sorted(
        n for k in range(11, 19) for n in (k * k, k * k - 1, k * k - 2) if 101 <= n <= 324
    )
    print(f"proved in 101..324: {proved}")
    assert proved == expected
    assert len(proved) == 24


def test_nagamochi_values_carry_the_two_precisions_the_register_uses() -> None:
    """13 significant figures reported, 12 verified, trailing zeros dropped in both."""
    payload = safe_load(_regenerate(50).split("---\n")[1])["packing"]
    assert payload["reported_lower_bound"]["value"] == "7.082762530298"
    assert payload["verified_lower_bound"]["value"] == "7.0827625303"
    assert (
        payload["verified_lower_bound"]["exact_form"] == "sqrt(50 - 2*floor(sqrt(50)) + 1) + 1"
    )


def test_the_verified_upper_bound_is_the_grid_ceiling_and_says_so() -> None:
    """`verified_upper_bound` is `ceil(sqrt(n))`, never a reading of the reported side."""
    availability = load_availability()
    for n in (111, 121, 324):
        payload = safe_load(
            generate_record(
                n,
                availability=availability,
                catalogue=None,
                review_date="2026-09-07",
                retrieved_date="2026-09-07",
            ).split("---\n")[1]
        )["packing"]
        side = math.isqrt(n) if math.isqrt(n) ** 2 == n else math.isqrt(n) + 1
        assert payload["verified_upper_bound"] == {
            "value": str(side),
            "exact_form": str(side),
            "evidence": ["E-basic-grid-upper"],
        }


def test_refuses_to_touch_the_hand_authored_range_or_overwrite_a_record(
    tmp_path: Path,
) -> None:
    assert refuse_reason(50, FRONTIER, force=False) is not None
    assert "hand-authored" in str(refuse_reason(50, FRONTIER, force=False))
    # The same n is allowed into a scratch directory, which is what the golden test needs.
    assert refuse_reason(50, tmp_path, force=False) is None
    assert refuse_reason(325, tmp_path, force=False) is not None

    target = record_path(tmp_path, 111)
    target.write_text("placeholder\n", encoding="utf-8")
    assert refuse_reason(111, tmp_path, force=False) is not None
    assert refuse_reason(111, tmp_path, force=True) is None


def test_a_catalogue_case_without_facts_refuses_rather_than_guesses() -> None:
    with pytest.raises(GenerationError):
        generate_record(
            101,
            availability=load_availability(),
            catalogue=None,
            review_date="2026-09-07",
            retrieved_date="2026-09-07",
        )
    with pytest.raises(GenerationError):
        generate_record(
            999,
            availability=load_availability(),
            catalogue=None,
            review_date="2026-09-07",
            retrieved_date="2026-09-07",
        )


def test_the_cli_writes_a_range_and_then_checks_it(tmp_path: Path) -> None:
    out = str(tmp_path)
    assert main(["--range", "111", "118", "--out", out, "--review-date", "2026-09-07"]) == 0
    assert sorted(path.name for path in tmp_path.glob("n-*.md")) == [
        f"n-{n}.md" for n in range(111, 119)
    ]
    # A second write refuses, and --check on what was written reports no drift even
    # though today's default review date is not the one the records carry.
    assert main(["--n", "111", "--out", out]) == 1
    assert main(["--range", "111", "118", "--out", out, "--check"]) == 0

    edited = record_path(tmp_path, 112)
    edited.write_text(
        edited.read_text(encoding="utf-8").replace("conjectured_optimum: integer", ""),
        encoding="utf-8",
    )
    assert main(["--range", "111", "118", "--out", out, "--check"]) == 1


def test_the_module_runs_as_a_devtool() -> None:
    """The documented invocation is the one that works."""
    completed = subprocess.run(
        [sys.executable, "-m", "devtools.generate_frontier_case", "--n", "50"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 1
    assert "hand-authored" in completed.stdout
