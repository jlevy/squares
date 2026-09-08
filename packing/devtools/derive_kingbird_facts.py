#!/usr/bin/env python3
r"""Acquire the Kingbird catalogue cases above `n = 100` once, and keep only the numbers.

This is the one-time fetch-and-derive pass that decision `D2` of the atlas expansion
plan authorises, and it is the only code path in this repository that can produce a new
Kingbird-derived witness. The 34 witnesses at `n <= 100` were made this way in August
2026 from SVGs that were never committed, so nothing since then has been able to add a
thirty-fifth; that is what this tool restores, for `n = 101..324`.

**What it retains, and what it refuses to.** Each catalogue SVG is fetched into memory,
parsed to normalized centre-and-angle facts, and dropped. No SVG is written anywhere,
no response is cached, and the tool refuses to start at all if a raw Kingbird directory
has appeared under the source inventory or if the output root is inside a directory
named `kingbird`. The retained artefact is a `Witness/v2` record carrying the numbers,
the attribution, the source URL, and its own finite-precision feasibility receipt --
exactly the shape `witnesses/known-best/n-071.yaml` already has. The reasoning is in
`resources/web/known-best-packings/README.md`; this file implements it rather than
restating it.

**The subpacking rule, and the evidence for it.** Thirteen catalogue pictures in
`101..324` serve two counts each. The picture holds the larger count, and the smaller
needs one square removed. Two facts decide how:

1. The catalogue states the rule itself, in the paragraph above its grid: *"If a
   pictured packing has multiple numbers in its label above, the picture represents the
   largest; each smaller is represented by removing any square."* The source therefore
   licenses removing **any** square, and the choice is free rather than guessed.
2. The picture marks nothing. Inspected on 2026-09-07, `square-148.svg` -- the
   `147, 148` entry -- contains `fill:none` only on the paths that draw the internal
   grid lines of its two blocks and on the closing `<use href="#outer">` frame. Every
   one of those is scenery the adapter already skips, and none of them is a square the
   source is offering up for removal. There is no dashed square, no differently filled
   square, and no annotated group.

So the rule is: **take the source's licence, and spend it deterministically.** The
squares are ordered by their normalized centre, descending, comparing exact decimals --
`x`, then `y`, then the angle -- and the first `source_n - n` of them are dropped. The
order is a property of the recovered geometry rather than of the document, so
reformatting the SVG upstream cannot change which square goes; and because it is
descending, what goes is a square at the far edge rather than one out of the middle.
Measured on the one shared entry below `n = 200`: deriving `n = 147` from the `147, 148`
picture drops the square centred at `(s - 1/2, s - 1/2)`, the container's top-right
corner, and the other three corners of the `s = 12.6568...` container keep theirs.
The licence sentence is re-read from the retained transcription every time a subpacking
is built, and its absence is a refusal: if the catalogue stops saying that, this rule
has lost its warrant and the case needs a person, not a default.

**What is skipped rather than derived.** A case whose catalogue side is a whole number
covering it -- `n = 119, 120, 142, 143, 167, 168, 194, 195, 223, 224, 254, 255, 287,
288, 322, 323` -- is a grid case in this atlas even though the catalogue pictures it,
exactly as `n = 47, 48, 62, 63, 79, 80, 98, 99` are at `n <= 100`. The builder generates
those exactly, and a derived witness for one would be overwritten on the next
`--update`, so this tool leaves them alone and says so.

Usage, from `packing/`::

    uv run --frozen --all-extras --group dev python -m devtools.derive_kingbird_facts \
        --range 101 200 --dry-run
    uv run --frozen --all-extras --group dev python -m devtools.derive_kingbird_facts \
        --n 147

The source is one person's personal site. Fetches are sequential by default, each
followed by a pause, and `--jobs` is capped low on purpose.
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from collections.abc import Callable, Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

import mpmath as mp
from strif import atomic_output_file

from devtools.build_known_best_atlas import (
    FRONTIER,
    KINGBIRD_RAW_ROOT,
    ROOT,
    SOURCE_MANIFEST,
    USER_AGENT,
    WITNESS_ROOT,
)
from sqpack.kingbird_catalogue import CatalogueEntry, default_catalogue_path, parse_catalogue
from sqpack.known_best import (
    KINGBIRD_TOLERANCE,
    SourceGeometryError,
    SquarePose,
    kingbird_derived_witness,
    parse_kingbird_svg,
)
from sqpack.witness import check_witness_semantics, witness_document
from sqpack.yamlio import safe_load

AVAILABILITY = ROOT / "atlas/prospective/source-availability-101-324.json"

#: What `--help` says. Written out rather than sliced off `__doc__`, which is stripped
#: under `-OO` and is longer than a usage screen wants anyway.
SUMMARY = (
    "Acquire the Kingbird catalogue cases above n = 100 once, keeping only the derived "
    "numerical facts. No source SVG is written to disk."
)

#: The source-availability key this tool acts on. Every other key in that map is served
#: by the grid rule or by a retained UnitSquare rendering, neither of which needs a
#: fetch.
CATALOGUE_SOURCE_KEY = "kingbird-current-catalogue"

#: The date this acquisition pass read the catalogue, recorded in every witness it
#: writes. Not `sqpack.known_best.RETRIEVED_DATE`, which belongs to the 2026-08-26 pass
#: and must keep saying so for the 34 witnesses that carry it.
DERIVED_RETRIEVED_DATE = "2026-09-07"

#: The catalogue's own sentence licensing a subpacking. Checked against the retained
#: transcription before any square is dropped; see this module's docstring.
REMOVAL_LICENCE = "each smaller is represented by removing any square"

#: Politeness, matching `build_known_best_atlas._fetch_one`: one pause per fetch, taken
#: inside the worker that fetched, so `--jobs` raises the rate by at most its own factor.
FETCH_PAUSE_SECONDS = 0.15
FETCH_ATTEMPTS = 3
FETCH_TIMEOUT_SECONDS = 30
#: Low on purpose. The ceiling is not a resource limit on this machine; it is a limit on
#: what this tool can do to someone else's web server.
MAX_JOBS = 4


class DerivationRefusedError(RuntimeError):
    """A typed refusal to derive one case, carrying the reason a report can group on."""

    def __init__(self, kind: str, detail: str) -> None:
        super().__init__(f"{kind}: {detail}")
        self.kind: str = kind
        self.detail: str = detail


@dataclass(frozen=True)
class DerivationPlan:
    """One case this pass intends to acquire, with everything the fetch needs."""

    n: int
    source_n: int
    listed_n: tuple[int, ...]
    source_path: str
    url: str
    #: The catalogue's printed decimal side. This is the reported value the receipt is
    #: checked against, because a frontier record for `n > 100` may not exist yet.
    catalogue_side: str
    witness_path: Path

    @property
    def removals(self) -> int:
        """How many squares the subpacking rule drops; zero for a pictured count."""
        return self.source_n - self.n


@dataclass(frozen=True)
class SkippedCase:
    """One case this pass deliberately does not acquire, and why."""

    n: int
    reason: str
    detail: str


@dataclass(frozen=True)
class DerivedCase:
    """One acquired case: the witness, its serialization, and where it was written."""

    plan: DerivationPlan
    witness: dict[str, Any]
    text: str
    path: Path

    @property
    def receipt(self) -> dict[str, Any]:
        """The feasibility receipt `kingbird_derived_witness` wrote into the record."""
        return self.witness["certificate"]["result"]


def _relative(path: Path) -> str:
    """Repository-relative where it can be, absolute where the caller went elsewhere."""
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def availability_entries(path: Path | None = None) -> dict[int, dict[str, Any]]:
    """The prospective source map, keyed by `n`."""
    target = AVAILABILITY if path is None else path
    document = json.loads(target.read_text(encoding="utf-8"))
    return {int(entry["n"]): entry for entry in document["availability"]["entries"]}


def _grid_covered(n: int, side: str) -> bool:
    """Whether the catalogue's own side is a whole number a plain grid already reaches."""
    value = Fraction(side)
    return value.denominator == 1 and value.numerator * value.numerator >= n


def _cross_check(n: int, entry: dict[str, Any], catalogued: CatalogueEntry) -> None:
    """Refuse where the source map and the reparsed catalogue disagree about a case.

    Two independent readings of the same page: the 2026-08-26 audit that wrote the map,
    and `sqpack.kingbird_catalogue` reading the retained transcription today. A case is
    only acquired where they agree on which picture serves it and on which counts that
    picture holds.
    """
    if catalogued.svg_path != entry["source_path"]:
        raise DerivationRefusedError(
            "source-map-disagrees",
            f"n={n}: the map names {entry['source_path']!r} and the catalogue names "
            f"{catalogued.svg_path!r}",
        )
    listed = tuple(int(value) for value in entry["listed_n"])
    if catalogued.listed_n != listed or catalogued.n != int(entry["source_n"]):
        raise DerivationRefusedError(
            "source-map-disagrees",
            f"n={n}: the map lists {listed} under source_n={entry['source_n']} and the "
            f"catalogue lists {catalogued.listed_n} under n={catalogued.n}",
        )


def derivation_plans(
    numbers: Sequence[int],
    *,
    out_root: Path,
    availability: dict[int, dict[str, Any]] | None = None,
    catalogue: dict[int, CatalogueEntry] | None = None,
) -> tuple[list[DerivationPlan], list[SkippedCase], list[tuple[int, DerivationRefusedError]]]:
    """Split the requested counts into what this pass acquires, leaves, and refuses.

    Nothing raises: one unreadable case in a hundred-case range is that case's refusal,
    reported with the rest, rather than an abort that loses the other ninety-nine. A
    skip and a refusal differ in kind -- a skip is a case this tool was never going to
    touch (a grid case, a UnitSquare case, one already retained), a refusal is one it
    should have been able to touch and could not.
    """
    entries = availability_entries() if availability is None else availability
    catalogued = parse_catalogue() if catalogue is None else catalogue
    plans: list[DerivationPlan] = []
    skipped: list[SkippedCase] = []
    refusals: list[tuple[int, DerivationRefusedError]] = []
    for n in numbers:
        try:
            plan = _plan_one(n, entries, catalogued, out_root=out_root)
        except DerivationRefusedError as error:
            refusals.append((n, error))
            continue
        if isinstance(plan, SkippedCase):
            skipped.append(plan)
        else:
            plans.append(plan)
    return plans, skipped, refusals


def _plan_one(
    n: int,
    entries: dict[int, dict[str, Any]],
    catalogued: dict[int, CatalogueEntry],
    *,
    out_root: Path,
) -> DerivationPlan | SkippedCase:
    """Decide one count: acquire it, skip it, or refuse it."""
    entry = entries.get(n)
    if entry is None:
        raise DerivationRefusedError(
            "no-availability-entry", f"n={n}: outside the audited 101..324 source map"
        )
    source_key = str(entry["source_key"])
    if source_key != CATALOGUE_SOURCE_KEY:
        return SkippedCase(n, "other-source", f"served by {source_key}")
    listed = catalogued.get(n)
    if listed is None:
        raise DerivationRefusedError(
            "not-in-catalogue",
            f"n={n}: the source map says catalogue, the catalogue is silent",
        )
    _cross_check(n, entry, listed)
    if _grid_covered(n, listed.side_decimal):
        return SkippedCase(n, "grid-covered", f"catalogue side {listed.side_decimal} is a grid")
    witness_path = out_root / f"n-{n:03d}.yaml"
    if witness_path.is_file():
        return SkippedCase(n, "existing", _relative(witness_path))
    return DerivationPlan(
        n=n,
        source_n=int(entry["source_n"]),
        listed_n=listed.listed_n,
        source_path=str(entry["source_path"]),
        url=str(entry["source_url"]),
        catalogue_side=listed.side_decimal,
        witness_path=witness_path,
    )


def fetch_svg(url: str) -> str:
    """Fetch one catalogue SVG into memory, with the builder's retries and politeness.

    Returns the text. Nothing here writes, and no caller is given a path: the bytes exist
    only for as long as the derivation that parses them.
    """
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    last_error: Exception | None = None
    for attempt in range(FETCH_ATTEMPTS):
        try:
            with urllib.request.urlopen(request, timeout=FETCH_TIMEOUT_SECONDS) as response:
                content = response.read()
        except (OSError, urllib.error.HTTPError, urllib.error.URLError) as error:
            last_error = error
            if attempt < FETCH_ATTEMPTS - 1:
                time.sleep(2**attempt)
        else:
            if b"<svg" not in content[:100_000]:
                raise DerivationRefusedError("not-svg", f"upstream response is not SVG: {url}")
            time.sleep(FETCH_PAUSE_SECONDS)
            return content.decode("utf-8")
    raise DerivationRefusedError("fetch-failed", f"{url}: {last_error}")


def _pose_key(pose: SquarePose) -> tuple[Decimal, Decimal, Decimal]:
    """A pose's exact decimal ordering key. `Decimal` because these strings are exact."""
    return (
        Decimal(pose.center_x),
        Decimal(pose.center_y),
        Decimal(pose.angle_degrees),
    )


def assert_removal_licence(catalogue_text: str) -> None:
    """Refuse to build a subpacking unless the catalogue still licenses one."""
    if REMOVAL_LICENCE not in catalogue_text:
        raise DerivationRefusedError(
            "removal-licence-absent",
            "the retained catalogue no longer states that a smaller listed count is the "
            "pictured packing with any square removed; a subpacking has lost its warrant",
        )


def subpacking_poses(
    poses: Sequence[SquarePose], *, n: int, source_n: int, catalogue_text: str
) -> tuple[SquarePose, ...]:
    """The `n` squares this repository keeps from a picture holding `source_n` of them.

    Identity where the picture is the case. Otherwise the catalogue's own licence is
    checked and then spent deterministically: drop the `source_n - n` squares whose
    normalized centres sort last, exact decimals, `x` then `y` then angle. Survivors keep
    the order they were recovered in, which is the order every retained witness is in.
    """
    if len(poses) != source_n:
        raise DerivationRefusedError(
            "square-count-mismatch",
            f"the picture for n={source_n} yielded {len(poses)} squares",
        )
    if n == source_n:
        return tuple(poses)
    if not 1 <= n < source_n:
        raise DerivationRefusedError(
            "subpacking-out-of-range", f"n={n} is not a subpacking of n={source_n}"
        )
    assert_removal_licence(catalogue_text)
    order = sorted(range(source_n), key=lambda index: _pose_key(poses[index]), reverse=True)
    dropped = set(order[: source_n - n])
    return tuple(pose for index, pose in enumerate(poses) if index not in dropped)


def _assert_side_matches(reported: str, actual: str, *, what: str, n: int) -> None:
    """The builder's side agreement, at the tolerance the Kingbird facts are checked at."""
    with mp.workdps(120):
        difference = abs(mp.mpf(reported) - mp.mpf(actual))
        tolerance = max(mp.mpf("1e-8"), abs(mp.mpf(reported)) * mp.mpf("1e-12"))
    if difference > tolerance:
        raise DerivationRefusedError(
            "side-mismatch", f"n={n}: source side {actual} disagrees with {what} {reported}"
        )


def frontier_reported_side(n: int, *, frontier_root: Path | None = None) -> str | None:
    """What `frontier/n-NNN.md` reports as the upper bound, or None where no record is."""
    root = FRONTIER if frontier_root is None else frontier_root
    path = root / f"n-{n:03d}.md"
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise DerivationRefusedError("frontier-malformed", f"{path.name}: missing frontmatter")
    metadata = safe_load(text.split("---\n", 2)[1])
    return str(metadata["packing"]["reported_upper_bound"]["value"])


def derive_witness(
    plan: DerivationPlan,
    source_text: str,
    *,
    catalogue_text: str,
    retrieved: str = DERIVED_RETRIEVED_DATE,
    frontier_root: Path | None = None,
) -> dict[str, Any]:
    """Parse one fetched SVG and return the checked `Witness/v2` record for one `n`.

    The retained shape is assembled here; every claim, source and certificate field is
    written by `kingbird_derived_witness`, which is the same code that rechecks the 34
    existing rows on every build.
    """
    try:
        geometry = parse_kingbird_svg(source_text, expected_n=plan.source_n)
    except SourceGeometryError as error:
        raise DerivationRefusedError(
            error.kind, f"n={plan.n} from {plan.source_path}: {error}"
        ) from error
    _assert_side_matches(plan.catalogue_side, geometry.side, what="the catalogue", n=plan.n)
    recorded = frontier_reported_side(plan.n, frontier_root=frontier_root)
    if recorded is not None:
        _assert_side_matches(recorded, geometry.side, what="the frontier record", n=plan.n)
    poses = subpacking_poses(
        geometry.poses, n=plan.n, source_n=plan.source_n, catalogue_text=catalogue_text
    )
    retained = {
        "id": f"W-known-best-n{plan.n:03d}",
        "n": plan.n,
        "side": geometry.side,
        "square_size": "1",
        "representation": "center-angle",
        "scalar": {"kind": "decimal"},
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "degrees",
        },
        "squares": [
            {
                "id": index,
                "center": [pose.center_x, pose.center_y],
                "angle": pose.angle_degrees,
            }
            for index, pose in enumerate(poses, start=1)
        ],
    }
    try:
        witness = kingbird_derived_witness(
            plan.n,
            retained,
            source_n=plan.source_n,
            source_path=_relative(SOURCE_MANIFEST),
            source_url=plan.url,
            retrieved=retrieved,
        )
    except (SourceGeometryError, ValueError) as error:
        raise DerivationRefusedError("witness-rejected", f"n={plan.n}: {error}") from error
    problems = check_witness_semantics(witness)
    if problems:
        raise DerivationRefusedError("witness-rejected", f"n={plan.n}: {problems[0]}")
    return witness


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(path) as temporary:
        temporary.write_text(text, encoding="utf-8")


def assert_no_raw_retention(out_root: Path) -> None:
    """The two ways this pass could start leaving source bytes behind, refused up front."""
    if KINGBIRD_RAW_ROOT.exists():
        raise DerivationRefusedError(
            "raw-kingbird-retained",
            f"{_relative(KINGBIRD_RAW_ROOT)} exists; the retention policy keeps no raw "
            "Kingbird asset, so this pass will not add derived facts beside one",
        )
    if any(part.lower() == "kingbird" for part in out_root.resolve().parts):
        raise DerivationRefusedError(
            "output-under-kingbird-directory",
            f"{out_root} is inside a directory named kingbird; witnesses are derived "
            "facts and do not live with source assets",
        )


def fetch_pictures(
    plans: Sequence[DerivationPlan], *, jobs: int, fetch: Callable[[str], str] = fetch_svg
) -> tuple[dict[str, str], dict[str, DerivationRefusedError]]:
    """Fetch each distinct picture once, however many counts it serves."""
    urls = sorted({plan.url for plan in plans})
    fetched: dict[str, str] = {}
    failures: dict[str, DerivationRefusedError] = {}
    if not urls:
        return fetched, failures
    with ThreadPoolExecutor(max_workers=min(jobs, len(urls))) as executor:
        futures = {executor.submit(fetch, url): url for url in urls}
        for future in as_completed(futures):
            url = futures[future]
            try:
                fetched[url] = future.result()
            except DerivationRefusedError as error:
                failures[url] = error
    return fetched, failures


def derive(
    numbers: Sequence[int],
    *,
    out_root: Path,
    jobs: int = 1,
    dry_run: bool = False,
    retrieved: str = DERIVED_RETRIEVED_DATE,
    fetch: Callable[[str], str] = fetch_svg,
) -> int:
    """Run one acquisition pass and report it. Returns the process exit status."""
    assert_no_raw_retention(out_root)
    plans, skipped, refusals = derivation_plans(numbers, out_root=out_root)
    for case in skipped:
        print(f"  n={case.n:<3} skipped  {case.reason}: {case.detail}")
    for n, refusal in refusals:
        print(f"  n={n:<3} refused  {refusal}")
    if dry_run:
        for plan in plans:
            print(
                f"  n={plan.n:<3} planned  {plan.source_path} "
                f"(source_n={plan.source_n}, drop={plan.removals}, "
                f"side={plan.catalogue_side}) -> {_relative(plan.witness_path)}"
            )
        pictures = len({plan.url for plan in plans})
        print(
            f"dry run: {len(plans)} to derive from {pictures} picture"
            f"{'' if pictures == 1 else 's'}, {len(skipped)} skipped, "
            f"{len(refusals)} refused, 0 fetched"
        )
        return 1 if refusals else 0

    catalogue_text = default_catalogue_path().read_text(encoding="utf-8")
    sources, failures = fetch_pictures(plans, jobs=jobs, fetch=fetch)
    derived: list[DerivedCase] = []
    for index, plan in enumerate(plans, start=1):
        source_text = sources.get(plan.url)
        if source_text is None:
            refusal = failures.get(plan.url) or DerivationRefusedError(
                "fetch-failed", f"{plan.url}: no response retained"
            )
            refusals.append((plan.n, refusal))
            print(f"  [{index:03d}/{len(plans):03d}] n={plan.n:<3} refused  {refusal}")
            continue
        try:
            witness = derive_witness(
                plan,
                source_text,
                catalogue_text=catalogue_text,
                retrieved=retrieved,
            )
        except DerivationRefusedError as error:
            refusals.append((plan.n, error))
            print(f"  [{index:03d}/{len(plans):03d}] n={plan.n:<3} refused  {error}")
            continue
        text = witness_document(witness, schema="../witness.schema.yaml")
        _write(plan.witness_path, text)
        case = DerivedCase(plan, witness, text, plan.witness_path)
        derived.append(case)
        receipt = case.receipt
        print(
            f"  [{index:03d}/{len(plans):03d}] n={plan.n:<3} derived  "
            f"side={str(witness['side'])[:18]} squares={plan.n} drop={plan.removals} "
            f"tolerance={KINGBIRD_TOLERANCE} "
            f"check={'passed' if receipt['check_passed'] else 'failed'} "
            f"-> {_relative(case.path)}"
        )
    existing = sum(1 for case in skipped if case.reason == "existing")
    print(
        f"derived {len(derived)}, fetched {len(sources)} picture"
        f"{'' if len(sources) == 1 else 's'}, skipped {len(skipped)} "
        f"({existing} already retained), refused {len(refusals)}"
    )
    for n, refusal in refusals:
        print(f"  refused n={n}: {refusal.kind}: {refusal.detail}")
    return 1 if refusals else 0


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=SUMMARY)
    selection = command.add_mutually_exclusive_group(required=True)
    selection.add_argument(
        "--range",
        nargs=2,
        type=int,
        metavar=("FIRST", "LAST"),
        help="derive every eligible case in this closed range",
    )
    selection.add_argument("--n", type=int, help="derive one case")
    command.add_argument(
        "--out",
        type=Path,
        default=WITNESS_ROOT,
        help="where witnesses are written (default: the known-best witness root)",
    )
    command.add_argument(
        "--dry-run", action="store_true", help="report the plan without fetching or writing"
    )
    command.add_argument(
        "--jobs",
        type=int,
        default=1,
        help=f"concurrent fetches, 1..{MAX_JOBS} (default: 1)",
    )
    return command


def main(argv: Sequence[str] | None = None) -> int:
    command = parser()
    args = command.parse_args(argv)
    if not 1 <= args.jobs <= MAX_JOBS:
        command.error(f"--jobs takes 1 to {MAX_JOBS}, to stay gentle with one small site")
    if args.range is not None:
        first, last = args.range
        if first < 1 or last < first:
            command.error("--range takes a nonempty positive range")
        numbers = list(range(first, last + 1))
    else:
        if args.n < 1:
            command.error("--n takes a positive count")
        numbers = [args.n]
    try:
        return derive(numbers, out_root=args.out, jobs=args.jobs, dry_run=args.dry_run)
    except DerivationRefusedError as error:
        print(f"refused: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
