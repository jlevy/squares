#!/usr/bin/env python3
"""Record the day each register entry reached `main`, its `landed` date.

`registered` is the day a lane wrote an entry. The entry reaches `main`, and the site
built from it, when its pull request merges: on the register of 14 October 2026, 67 of
160 entries the same day, 69 a day later and 24 two days later (#514's review A,
finding A1). The results page's "Added in the Last Seven Days" and its table's Added
filters read `landed`, so "added" means the day a reader could first see the result.

Every entry carries `landed`; `results.schema.yaml` requires it. A lane writes it with
the entry, as the day it registers it, and the merge step re-dates the entries a records
pull request adds to the day it merges. No gate reads Git: the schema holds the field's
presence and `problems` its form and order, both on the tree alone (OR-18; #514's review
B, finding B3). A pull request whose re-date is forgotten reads a day or two early, the
lag A1 measured, and nothing turns red; `--audit` finds it.

Modes, from `packing/`:

- The default is the merge step. It lists the entries `origin/main`'s register does not
  hold, the ones this branch adds, and `--apply` re-dates each to `--date`, today in UTC
  unless given. Run it, with its re-pin, as the last commits before a records pull
  request merges (`campaign/result-import.md`, Stage 5, Before merge). Run again after a
  re-merge, or when the merge slipped past midnight UTC, it re-dates them again. So
  `landed` is the day of the stamp, which is the merge day when the stamp is the last
  step before the merge.
- `--audit` compares the `landed` of every entry `origin/main` holds with `main`'s
  first-parent history: the UTC day of the first commit whose register holds the entry,
  for a merged pull request the merge. It lists each that differs, and `--apply`
  corrects them. It gates nothing; the intake sweep runs it, and its corrections ride
  the next records pull request.
- `--backfill` dates each entry that has no `landed` the same way. It ran once, when the
  field was introduced.

The same modes write the landing record, `frontier/landings.yaml`: the day each count's
house best packing and each source's dated beyond-horizon rows reached `main`, which the
home page's Recently Added places them by (#736's review A, finding A2). Those records
carry no date field of their own; the merge step stamps what a branch adds, and
`--audit` and `--backfill` read the same first-parent history.

History is read only here, by a tool, and its answer is written into the record; nothing
that renders a page or gates a change reads Git (OR-18).

The tool rewrites an entry's `landed:` line, or inserts one after its `registered:` line,
and leaves every other byte of the file alone. The ids are the parsed register's and must
match a scan of its `- id:` lines, so an entry the scan cannot see fails loudly rather than
going unstamped (#514's review B, finding B7).

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.stamp_landed
    uv run --frozen --all-extras --group dev python -m devtools.stamp_landed --apply
    uv run --frozen --all-extras --group dev python -m devtools.stamp_landed --audit
    uv run --frozen --all-extras --group dev python -m devtools.stamp_landed --audit --apply
"""

from __future__ import annotations

import argparse
import ast
import re
import subprocess
from collections.abc import Iterable, Mapping, Sequence
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any, NamedTuple

from strif import atomic_output_file

from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
RESULTS = ROOT / "frontier" / "results.yaml"
#: The register's path from the repository root, as Git names it.
RESULTS_PATH = "packing/frontier/results.yaml"
#: The branch whose register says which entries a branch adds, and whose first-parent
#: history says when each entry landed.
MAIN = "origin/main"

#: The first line of an entry, as the register writes it, its id bare or quoted.
_ID_LINE = re.compile(
    r"""^(?P<indent>\s*)- id: (?P<quote>['"]?)(?P<id>[^'"\s]+)(?P=quote)\s*$"""
)
_REGISTERED = re.compile(r"^(?P<indent>\s*)registered:")
_LANDED = re.compile(r"^\s*landed:")


def register_ids(text: str) -> list[str]:
    """The ids a register's text holds, in its order: the parsed register's, which a scan
    of its `- id:` lines must find the same, so that `set_landed` can reach every one."""
    parsed = [str(entry["id"]) for entry in safe_load(text)["results"]]
    scanned = [match["id"] for line in text.splitlines() if (match := _ID_LINE.match(line))]
    if parsed != scanned:
        missed = sorted(set(parsed) - set(scanned)) or sorted(set(scanned) - set(parsed))
        raise ValueError(
            "the register's `- id:` lines do not match its parsed entries"
            f"{': ' + ', '.join(missed) if missed else ', in order'}"
        )
    return parsed


def recorded(text: str) -> dict[str, str | None]:
    """Each entry's `landed` as the register records it, or None where it has none."""
    register_ids(text)
    return {
        str(entry["id"]): (str(entry["landed"]) if "landed" in entry else None)
        for entry in safe_load(text)["results"]
    }


def set_landed(text: str, dates: Mapping[str, str]) -> str:
    """The register text with each entry `dates` names landed on its date: its `landed:`
    line rewritten, or one inserted after its `registered:` line. Every other byte is
    kept."""
    register_ids(text)
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    current: str | None = None
    for index, line in enumerate(lines):
        if match := _ID_LINE.match(line):
            current = match["id"]
            out.append(line)
            continue
        registered = _REGISTERED.match(line)
        if current is None or registered is None or current not in dates:
            out.append(line)
            continue
        out.append(line)
        following = lines[index + 1] if index + 1 < len(lines) else ""
        stamp = f"{registered['indent']}landed: '{dates[current]}'\n"
        if _LANDED.match(following):
            lines[index + 1] = stamp
        else:
            out.append(stamp)
        current = None
    return "".join(out)


def branch_entries(text: str, main_text: str) -> list[str]:
    """The ids a branch's register holds that `main`'s does not: the entries it adds."""
    on_main = set(register_ids(main_text))
    return [result_id for result_id in register_ids(text) if result_id not in on_main]


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=REPO, check=True, capture_output=True, text=True
    ).stdout


def first_landings(ref: str = MAIN, path: str = RESULTS_PATH) -> dict[str, str]:
    """Each id `ref`'s register has ever held, with the UTC day of the first commit on
    `ref`'s first-parent history whose register holds it."""
    landed: dict[str, str] = {}
    log = _git("log", "--first-parent", "--reverse", "--format=%H %cI", ref, "--", path)
    for line in log.splitlines():
        commit, when = line.split()
        day = datetime.fromisoformat(when).astimezone(UTC).date().isoformat()
        for result_id in register_ids(_git("show", f"{commit}:{path}")):
            landed.setdefault(result_id, day)
    return landed


def audit(
    dates: Mapping[str, str | None], history: Mapping[str, str], on_main: Iterable[str]
) -> dict[str, str]:
    """The entries on `main` whose recorded `landed` differs from the day its first-parent
    history gives, with that day."""
    return {
        result_id: history[result_id]
        for result_id in on_main
        if result_id in dates
        and result_id in history
        and dates[result_id] != history[result_id]
    }


def problems(register: Mapping[str, Any]) -> list[str]:
    """What keeps the register's `landed` dates whole, read from the tree alone: an entry
    without one, a malformed date, or a date before the entry's `registered`."""
    found: list[str] = []
    for entry in register["results"]:
        result_id = str(entry["id"])
        if "landed" not in entry:
            found.append(f"{result_id} carries no `landed` date")
            continue
        try:
            landed = date.fromisoformat(str(entry["landed"]))
        except ValueError:
            found.append(f"{result_id}: `landed` {entry['landed']!r} is not a date")
            continue
        if landed < date.fromisoformat(str(entry["registered"])):
            found.append(
                f"{result_id} landed on {landed} before it was registered on "
                f"{entry['registered']}"
            )
    return found


# ------------------------------------------------------------------- house and row landings
#
# The home page's Recently Added places three kinds of arrival by the day each reached
# `main` (#736's review A, finding A2): a register entry by its `landed`; a count's house
# best packing, by the day `main` first held its current house (`upper_bound_houses.ADOPTED`);
# and a source's dated beyond-horizon rows (`source-coverage.yaml`), by the day `main` first
# held any of them. The last two have no field of their own in their records, so the
# landing record `frontier/landings.yaml` holds them, written here as `landed` is: the
# merge step stamps what a branch adds, and `--audit` and `--backfill` read `main`'s
# first-parent history. Every source's rows reach `main` in one merge, so a source carries
# one day: rows a later merge adds to a landed release are declared under a source of their
# own (`beyond_horizon_replay.Split`; #800's review A, A1), as #763's 13 recipes are.

LANDINGS = ROOT / "frontier" / "landings.yaml"
LANDINGS_PATH = "packing/frontier/landings.yaml"
COVERAGE = ROOT / "frontier" / "source-coverage.yaml"
COVERAGE_PATH = "packing/frontier/source-coverage.yaml"
HOUSES_PATH = "packing/devtools/upper_bound_houses.py"
#: What opens the landing record, above its two lists.
LANDINGS_HEADER = """\
# The day each count's house best packing and each source's dated beyond-horizon rows
# reached `main`, in UTC, as `landed` is for a register entry. The home page's Recently
# Added places them by it. Written by `devtools.stamp_landed`: the merge step stamps what
# a branch adds, and `--audit` compares every entry with `main`'s first-parent history.
# `houses` follows `upper_bound_houses.ADOPTED`, one entry a count with the result that
# houses it now; `sources` names every source with rows in `source-coverage.yaml`.
softschema:
  contract: packing.squares:Landings/v1
  schema: landings.schema.yaml
  status: enforced
"""


class Landings(NamedTuple):
    """The landing record: each adopted count's house result and the day `main` first
    held it, and each row source's day."""

    houses: dict[int, tuple[str, str]]
    sources: dict[str, str]


def adopted_houses(text: str) -> dict[int, str]:
    """`ADOPTED` as a text of `upper_bound_houses` assigns it, read without running it:
    each adopted count and the result that houses it."""
    for node in ast.parse(text).body:
        if isinstance(node, ast.Assign):
            targets, value = node.targets, node.value
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            targets, value = [node.target], node.value
        else:
            continue
        if any(isinstance(target, ast.Name) and target.id == "ADOPTED" for target in targets):
            return {int(n): str(result) for n, result in ast.literal_eval(value).items()}
    raise ValueError("no ADOPTED assignment in upper_bound_houses")


def row_sources(text: str) -> set[str]:
    """The sources a coverage register's text holds beyond-horizon rows from."""
    return {str(row["source_id"]) for row in safe_load(text)["beyond_horizon_claims"]}


def read_landings(text: str) -> Landings:
    """The landing record's text, parsed."""
    record = safe_load(text) or {}
    return Landings(
        houses={
            int(entry["n"]): (str(entry["result"]), str(entry["landed"]))
            for entry in record.get("houses") or []
        },
        sources={
            str(entry["id"]): str(entry["landed"]) for entry in record.get("sources") or []
        },
    )


def write_landings(landings: Landings) -> str:
    """The landing record's text: its header, then the houses by count and the sources by
    id, every date quoted, so the same record is always the same bytes."""
    lines = [LANDINGS_HEADER, "houses:\n"]
    for n, (result, day) in sorted(landings.houses.items()):
        lines.append(f"  - n: {n}\n    result: {result}\n    landed: '{day}'\n")
    lines.append("sources:\n")
    for source, day in sorted(landings.sources.items()):
        lines.append(f"  - id: {source}\n    landed: '{day}'\n")
    return "".join(lines)


def landings_problems(
    landings: Landings, adopted: Mapping[int, str], sources: set[str]
) -> list[str]:
    """What keeps the landing record whole, read from the tree alone: one house entry for
    every adopted count, naming the result that houses it now, and one entry for every
    source with rows, each with a date."""
    found: list[str] = []
    for n in sorted(set(adopted) | set(landings.houses)):
        if n not in landings.houses:
            found.append(f"n={n}: its house, {adopted[n]}, has no landing")
        elif n not in adopted:
            found.append(f"n={n}: a landing for a count no adoption houses")
        elif landings.houses[n][0] != adopted[n]:
            found.append(
                f"n={n}: the landing names {landings.houses[n][0]}, the house is {adopted[n]}"
            )
    for source in sorted(sources | set(landings.sources)):
        if source not in landings.sources:
            found.append(f"{source}: its rows have no landing")
        elif source not in sources:
            found.append(f"{source}: a landing for a source with no rows")
    days = [day for _, day in landings.houses.values()] + list(landings.sources.values())
    for day in days:
        try:
            date.fromisoformat(day)
        except ValueError:
            found.append(f"landing {day!r} is not a date")
    return found


def current_landings() -> tuple[dict[int, str], set[str]]:
    """What the tree says the record must cover: the adopted counts and the row sources."""
    return (
        adopted_houses((REPO / HOUSES_PATH).read_text(encoding="utf-8")),
        row_sources(COVERAGE.read_text(encoding="utf-8")),
    )


def _first_parent(ref: str, path: str) -> list[tuple[str, str]]:
    """Each commit on `ref`'s first-parent history that changed `path`, oldest first,
    with its UTC day."""
    log = _git("log", "--first-parent", "--reverse", "--format=%H %cI", ref, "--", path)
    return [
        (commit, datetime.fromisoformat(when).astimezone(UTC).date().isoformat())
        for commit, when in (line.split() for line in log.splitlines())
    ]


def branch_additions(
    adopted: Mapping[int, str], sources: set[str], day: str, ref: str = MAIN
) -> Landings:
    """What a branch adds to `ref`'s tree, dated `day`: each count whose house it changes
    or adds, by `ref`'s `ADOPTED`, and each source whose rows `ref` does not hold. The
    merge step dates these and nothing else; what `ref` already holds keeps its day from
    `ref`'s record or, where `ref` has none yet, the branch's."""
    held = adopted_houses(_git("show", f"{ref}:{HOUSES_PATH}"))
    rows = row_sources(_git("show", f"{ref}:{COVERAGE_PATH}"))
    return Landings(
        {n: (result, day) for n, result in adopted.items() if held.get(n) != result},
        {source: day for source in sources if source not in rows},
    )


def main_landings(ref: str = MAIN) -> Landings:
    """`ref`'s landing record, or an empty one where `ref` holds none yet."""
    listed = _git("ls-tree", "--name-only", ref, "--", LANDINGS_PATH).strip()
    return read_landings(_git("show", f"{ref}:{LANDINGS_PATH}") if listed else "")


def landing_history(ref: str = MAIN) -> Landings:
    """`ref`'s first-parent history read as a landing record: for each count, the day its
    house last changed to the result that houses it at `ref`, and for each source, the day
    `ref` first held a row of it."""
    houses: dict[int, tuple[str, str]] = {}
    for commit, day in _first_parent(ref, HOUSES_PATH):
        for n, result in adopted_houses(_git("show", f"{commit}:{HOUSES_PATH}")).items():
            if houses.get(n, ("", ""))[0] != result:
                houses[n] = (result, day)
    sources: dict[str, str] = {}
    for commit, day in _first_parent(ref, COVERAGE_PATH):
        for source in row_sources(_git("show", f"{commit}:{COVERAGE_PATH}")):
            sources.setdefault(source, day)
    return Landings(houses, sources)


def stamp_landings(
    adopted: Mapping[int, str],
    sources: set[str],
    known: Sequence[Landings],
    day: str | None,
) -> Landings:
    """The record the tree needs: every adopted count and row source, each taking its day
    from the first record in `known` that names the same house or source, else `day`.

    The merge step passes the branch's additions dated the day it merges
    (`branch_additions`), then `main`'s record, then the branch's, with no day: what the
    branch adds is dated the merge day, whatever a lane wrote, and what `main` holds keeps
    its day. `--backfill` passes the branch's record and then the history. With no day,
    an entry nothing dates is left out for `landings_problems` to name."""
    houses: dict[int, tuple[str, str]] = {}
    for n, result in adopted.items():
        found = next(
            (
                record.houses[n][1]
                for record in known
                if record.houses.get(n, ("",))[0] == result
            ),
            day,
        )
        if found is not None:
            houses[n] = (result, found)
    rows: dict[str, str] = {}
    for source in sources:
        found = next(
            (record.sources[source] for record in known if source in record.sources), day
        )
        if found is not None:
            rows[source] = found
    return Landings(houses, rows)


def landings_audit(landings: Landings, history: Landings, on_main: Landings) -> list[str]:
    """The entries `main`'s record holds whose recorded day differs from the day `main`'s
    history gives, each as a line naming both."""
    found: list[str] = []
    for n, (result, day) in sorted(landings.houses.items()):
        held = history.houses.get(n, ("", ""))
        if on_main.houses.get(n, ("",))[0] == result == held[0] and held[1] != day:
            found.append(f"n={n} ({result}) records {day}; history gives {held[1]}")
    for source, day in sorted(landings.sources.items()):
        held_day = history.sources.get(source)
        if source in on_main.sources and held_day is not None and held_day != day:
            found.append(f"{source} records {day}; history gives {held_day}")
    return found


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n", 1)[0])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--audit", action="store_true", help=f"compare with {MAIN}'s history")
    mode.add_argument("--backfill", action="store_true", help="date entries that have none")
    parser.add_argument("--date", help="the merge step's day, YYYY-MM-DD (default: today, UTC)")
    parser.add_argument("--apply", action="store_true", help="write the dates in place")
    options = parser.parse_args(argv)
    text = RESULTS.read_text(encoding="utf-8")
    current = recorded(text)
    if options.audit or options.backfill:
        history = first_landings()
        if options.audit:
            on_main = register_ids(_git("show", f"{MAIN}:{RESULTS_PATH}"))
            dates = audit(current, history, on_main)
            for result_id, day in dates.items():
                print(f"{result_id} records {current[result_id]}; {MAIN} took it in on {day}")
            print(f"landed audit: {len(dates)} of {len(on_main)} entries on {MAIN} differ")
        else:
            dates = {
                result_id: history[result_id]
                for result_id, day in current.items()
                if day is None and result_id in history
            }
            for result_id, day in dates.items():
                print(f"{result_id} {day}")
    else:
        day = options.date or datetime.now(UTC).date().isoformat()
        date.fromisoformat(day)
        dates = dict.fromkeys(branch_entries(text, _git("show", f"{MAIN}:{RESULTS_PATH}")), day)
        for result_id in dates:
            print(f"{result_id} {current[result_id] or 'none'} -> {day}")
        if not dates:
            print(f"this branch adds no entry to {MAIN}'s register; nothing to stamp")
    if options.apply and dates:
        with atomic_output_file(RESULTS) as temporary:
            temporary.write_text(set_landed(text, dates), encoding="utf-8")
        print(f"wrote {RESULTS.relative_to(REPO)}")
    return _landings(options)


def _landings(options: argparse.Namespace) -> int:
    """The landing record's half of each mode: the merge step dates the houses and row
    sources the branch adds, `--audit` compares `main`'s with its history, and
    `--backfill` dates from history whatever the record lacks."""
    text = LANDINGS.read_text(encoding="utf-8") if LANDINGS.is_file() else ""
    landings = read_landings(text)
    adopted, sources = current_landings()
    if options.audit:
        on_main = main_landings()
        found = landings_audit(landings, landing_history(), on_main)
        for line in found:
            print(line)
        print(f"landings audit: {len(found)} differ from {MAIN}'s history")
        if not found:
            return 0
        history = landing_history()
        stamped = Landings(
            {n: history.houses.get(n, entry) for n, entry in landings.houses.items()},
            {s: history.sources.get(s, day) for s, day in landings.sources.items()},
        )
    elif options.backfill:
        stamped = stamp_landings(adopted, sources, (landings, landing_history()), None)
    else:
        day = options.date or datetime.now(UTC).date().isoformat()
        date.fromisoformat(day)
        stamped = stamp_landings(
            adopted,
            sources,
            (branch_additions(adopted, sources, day), main_landings(), landings),
            None,
        )
    for n, entry in sorted(stamped.houses.items()):
        if landings.houses.get(n) != entry:
            print(f"n={n} {entry[0]} -> {entry[1]}")
    for source, day in sorted(stamped.sources.items()):
        if landings.sources.get(source) != day:
            print(f"{source} -> {day}")
    if options.apply and stamped != landings:
        with atomic_output_file(LANDINGS) as temporary:
            temporary.write_text(write_landings(stamped), encoding="utf-8")
        print(f"wrote {LANDINGS.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
