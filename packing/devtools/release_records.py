#!/usr/bin/env python3
"""The reviewed no-public-change records: one YAML file each, never a shared tuple.

`devtools.check_release_impact` asks a change to a paper's or the posters' inputs for an
owning successor or a fresh `ReleaseNoPublicChange`: a reviewed finding, scoped to exact
paths, that the outputs it names did not change. Until 1 November 2026 every such finding
was a literal entry appended to `RELEASE_NO_PUBLIC_CHANGES` at the end of `release.py`,
so any two open records pull requests touched one hunk and each merge of `main` into the
other conflicted there. `devtools.merge_conflicts` recomputed the 174 merges from 24
October to 1 November: 82 conflicted, the tuple in 64 of them, across 33 pull requests,
and in 31 it was the only conflict, each a hand resolution and another CI cycle that
nothing else asked for (think-nrp6).

A record is now its own file in `packing/release-records/no-public-change/`, so two
additions are two new paths and merge without a shared hunk. **Name a new one
`<YYYY-MM-DD>-<lane or bead>-<topic>.yaml`**: a real calendar date, the day it is
written, then the lane or bead that writes it, then a word or two for the change, all in
lower case, such as `2026-11-02-l16-think-r94q-survey.yaml`. The lane or bead keeps two
lanes writing on one day from choosing one name. It holds `components`, `paths`,
`outputs` and `reason`, the fields of `ReleaseNoPublicChange`; the schema beside the
directory, `no-public-change.schema.yaml`, is the contract, and a file that breaks it, or
is named otherwise, is refused with its name rather than skipped. Whether a fresh record
covers its change is still the gate's question. Records are read in name order: the 247
moved from the tuple keep its order as `0000-` to `0246-`, each named after its first
path. Those numbers are frozen (`MIGRATED`): `0247-` is refused, since two lanes copying
the listing's last name would collide on it, and every dated name sorts after them.

**The records are append-only.** The gate refuses a head that no longer holds a record
its base holds, whether deleted or rewritten; a later finding is a new record. No record
was dropped or rewritten after its merge while they were a tuple, and there is no
supersession for them.

A union merge driver was measured and refused. Git applies one to a whole file, not to a
block, and `release.py` also conflicts at `DATA_REVISION` and the edition histories,
where keeping both sides is silently wrong. Even in the 41 merges where the tuple was
`release.py`'s only conflict, `git merge-file --union` gave Python that does not compile
in 25 and matched the committed resolution in none: Git aligns the lines two appended
records share, splits the conflict around them and keeps both sides of each piece, which
fuses the two records into one. `merge_conflicts --since 2026-10-24 --path
packing/src/sqpack/release.py --union` prints those figures.

`python -m devtools.release_records migrate` moved the tuple, refusing unless every file
it writes reads back as the record it came from; it is idempotent, and finds nothing on a
tree with no tuple. On a branch cut before the move, whose merge of main keeps its own
tuple, it is the way out: the tuple's records the files already hold are matched by
value, since main's tuple took entries mid-way and indexes no longer line up, and only the
lane's own are written, as `<today>-<slug>.yaml` from `--slug <lane or bead>-<topic>`.
`check` reads every record, the quickest way to try a new file, and
`check --against origin/main` says how the records stand against those a revision holds,
as a tuple or as files.
"""

from __future__ import annotations

import argparse
import ast
import datetime
import functools
import re
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path, PurePosixPath
from typing import Any, override

import yaml
from jsonschema_rs import Draft202012Validator

from sqpack.release import ReleaseNoPublicChange
from sqpack.yamlio import load_yaml, safe_load

REPO = Path(__file__).resolve().parents[2]
#: Where the records live, repository-relative, at every revision a gate reads.
DIRECTORY = "packing/release-records/no-public-change"
SCHEMA = REPO / "packing/release-records/no-public-change.schema.yaml"
RELEASE_PATH = "packing/src/sqpack/release.py"
#: The name the tuple had in `release.py`, which a base before the move still holds.
TUPLE = "RELEASE_NO_PUBLIC_CHANGES"
#: The records the move wrote, `0000-` to `0246-` in the tuple's order. The numbered names
#: are frozen at these: a lane copying the listing's last name would write `0247-`, and
#: two lanes doing that collide, so every later record is dated (review A of #873).
MIGRATED = 247
_SLUG = r"[a-z0-9]+(?:-[a-z0-9]+)*"
_DATED = re.compile(rf"(?P<day>[0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}})-{_SLUG}\.yaml")
_NUMBERED = re.compile(rf"(?P<index>[0-9]{{4}})-{_SLUG}\.yaml")
#: The form of a new record's name, in every message that asks for one.
NEW_NAME = "<YYYY-MM-DD>-<lane or bead>-<topic>.yaml"
#: A record and where it is: its repository-relative file, or its entry in the old tuple.
Named = tuple[str, ReleaseNoPublicChange]


@functools.cache
def _validator() -> Draft202012Validator:
    return Draft202012Validator(safe_load(SCHEMA.read_text(encoding="utf-8")))


def _name_problem(name: str) -> str | None:
    """Why `name` cannot name a record, or None: a real date, or a migrated number."""
    if dated := _DATED.fullmatch(name):
        try:
            datetime.date.fromisoformat(dated["day"])
        except ValueError:
            return f"{dated['day']} is not a calendar date; name a record {NEW_NAME}"
        return None
    if (numbered := _NUMBERED.fullmatch(name)) and int(numbered["index"]) < MIGRATED:
        return None
    if numbered:
        return (
            f"0000 to {MIGRATED - 1:04d} are the records moved from the tuple, and a new "
            f"record is dated: name it {NEW_NAME}"
        )
    return f"name a record {NEW_NAME}, in lower case"


def _checked(where: str, document: object) -> ReleaseNoPublicChange:
    errors = sorted(
        f"{'/'.join(str(part) for part in error.instance_path) or 'record'}: {error.message}"
        for error in _validator().iter_errors(document)
    )
    if errors or not isinstance(document, dict):
        raise ValueError(f"{where}: {'; '.join(errors) or 'not a record'}")
    fields: dict[str, Any] = document  # pyright: ignore[reportUnknownVariableType]
    return ReleaseNoPublicChange(
        tuple(fields["components"]),
        tuple(fields["paths"]),
        tuple(fields["outputs"]),
        fields["reason"],
    )


def parse(name: str, text: str) -> ReleaseNoPublicChange:
    """One record file's record, refusing a name or a body the contract does not allow."""
    where = f"{DIRECTORY}/{name}"
    if (problem := _name_problem(name)) is not None:
        raise ValueError(f"{where}: {problem}")
    try:
        document = load_yaml(text)
    except yaml.YAMLError as error:
        raise ValueError(f"{where}: {error}") from error
    return _checked(where, document)


class _Folded(str):
    """A reason, written as a folded block so it reads as the prose it is."""

    __slots__ = ()


class _Dumper(yaml.SafeDumper):
    """Indents a list under its key and folds the reason, as a record is written by hand."""

    @override
    def increase_indent(self, flow: bool = False, indentless: bool = False) -> None:
        super().increase_indent(flow=flow, indentless=False)


_Dumper.add_representer(
    _Folded,
    lambda dumper, text: dumper.represent_scalar("tag:yaml.org,2002:str", text, style=">"),
)


def render(record: ReleaseNoPublicChange) -> str:
    """The file text for one record; `parse` reads it back as the same record."""
    document = {
        "components": list(record.components),
        "paths": list(record.paths),
        "outputs": list(record.outputs),
        "reason": _Folded(record.reason),
    }
    return yaml.dump(document, Dumper=_Dumper, sort_keys=False, width=88, allow_unicode=True)


def load_named(repo: Path = REPO) -> tuple[Named, ...]:
    """Every record in `repo`'s working tree with its file, in name order."""
    directory = repo / DIRECTORY
    if not directory.is_dir():
        return ()
    records = []
    for path in sorted(directory.iterdir()):
        if not path.is_file():
            raise ValueError(f"{DIRECTORY}/{path.name}: a record is a file")
        records.append(
            (f"{DIRECTORY}/{path.name}", parse(path.name, path.read_text(encoding="utf-8")))
        )
    return tuple(records)


def load(repo: Path = REPO) -> tuple[ReleaseNoPublicChange, ...]:
    """Every record in `repo`'s working tree, in name order."""
    return tuple(record for _where, record in load_named(repo))


def _git(repo: Path, *args: str, stdin: bytes | None = None) -> bytes:
    result = subprocess.run(
        ["git", *args], cwd=repo, input=stdin, capture_output=True, check=False
    )
    if result.returncode:
        raise ValueError(
            f"git {args[0]} failed: {result.stderr.decode(errors='replace').strip()}"
        )
    return result.stdout


def load_at(repo: Path, revision: str) -> tuple[ReleaseNoPublicChange, ...]:
    """Every record as `revision` holds it, in name order."""
    return tuple(record for _where, record in load_at_named(repo, revision))


def load_at_named(repo: Path, revision: str) -> tuple[Named, ...]:
    """Every record `revision` holds with its file, in name order, read in one
    `git cat-file`."""
    entries = []
    for row in _git(repo, "ls-tree", "-z", revision, "--", f"{DIRECTORY}/").split(b"\0"):
        if row:
            meta, _, path = row.partition(b"\t")
            _mode, kind, blob = meta.decode().split(" ")
            entries.append((PurePosixPath(path.decode()).name, kind, blob))
    entries.sort()
    if not entries:
        return ()
    for name, kind, _blob in entries:
        if kind != "blob":
            raise ValueError(f"{DIRECTORY}/{name}: a record is a file")
    output = _git(
        repo, "cat-file", "--batch", stdin=b"".join(f"{e[2]}\n".encode() for e in entries)
    )
    records = []
    offset = 0
    for name, _kind, _blob in entries:
        header = output.index(b"\n", offset)
        size = int(output[offset:header].split(b" ")[2])
        body = output[header + 1 : header + 1 + size]
        records.append((f"{DIRECTORY}/{name}", parse(name, body.decode("utf-8"))))
        offset = header + 1 + size + 1
    return tuple(records)


def _tuple_assignment(source: bytes) -> ast.Assign | ast.AnnAssign | None:
    found = [
        node
        for node in ast.parse(source, filename=RELEASE_PATH).body
        if (
            isinstance(node, ast.Assign)
            and any(
                isinstance(target, ast.Name) and target.id == TUPLE for target in node.targets
            )
        )
        or (
            isinstance(node, ast.AnnAssign)
            and isinstance(node.target, ast.Name)
            and node.target.id == TUPLE
        )
    ]
    if len(found) > 1:
        raise ValueError(f"{RELEASE_PATH} assigns {TUPLE} {len(found)} times")
    return found[0] if found else None


def literal(source: bytes | None) -> tuple[ReleaseNoPublicChange, ...]:
    """The records a `release.py` from before the move holds as a literal tuple."""
    return tuple(record for _where, record in literal_named(source))


def literal_named(source: bytes | None) -> tuple[Named, ...]:
    """The literal tuple's records, each named by its entry.

    Parsed, never executed, and held to the same schema as a file: a base before
    1 November 2026 keeps its records this way, and the gate counts them as retained.
    """
    node = None if source is None else _tuple_assignment(source)
    if node is None or node.value is None:
        return ()
    if not isinstance(node.value, (ast.Tuple, ast.List)):
        raise TypeError(f"{TUPLE} must retain a literal tuple of records")
    records = []
    for index, call in enumerate(node.value.elts):
        where = f"{RELEASE_PATH} {TUPLE}[{index}]"
        if (
            not isinstance(call, ast.Call)
            or not isinstance(call.func, ast.Name)
            or call.func.id != "ReleaseNoPublicChange"
            or any(keyword.arg is None for keyword in call.keywords)
        ):
            raise ValueError(f"{where}: requires a ReleaseNoPublicChange of explicit fields")
        try:
            values = {
                **dict(
                    zip(
                        ReleaseNoPublicChange._fields,
                        (ast.literal_eval(argument) for argument in call.args),
                        strict=False,
                    )
                ),
                **{
                    str(keyword.arg): ast.literal_eval(keyword.value)
                    for keyword in call.keywords
                },
            }
        except ValueError as error:
            raise ValueError(f"{where}: requires literal fields") from error
        records.append(
            (
                where,
                _checked(
                    where,
                    {
                        key: list(value) if isinstance(value, tuple) else value
                        for key, value in values.items()
                    },
                ),
            )
        )
    return tuple(records)


def _slug(record: ReleaseNoPublicChange) -> str:
    stem = PurePosixPath(record.paths[0]).stem if record.paths else ""
    return re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-") or "record"


def _planned(
    records: Sequence[ReleaseNoPublicChange],
    held: Sequence[ReleaseNoPublicChange],
    *,
    slug: str | None,
    day: datetime.date,
) -> list[tuple[str, ReleaseNoPublicChange]]:
    """The file name each record the files do not hold yet is written under."""
    if not held:
        # The move itself, on a tree with no records: the tuple's order, numbered.
        return [
            (f"{index:04d}-{_slug(record)}.yaml", record)
            for index, record in enumerate(records)
        ]
    # A branch cut before the move, merging main: its tuple's indexes no longer line up
    # with main's files, since entries were inserted mid-tuple, so its records are matched
    # by value, and only the lane's own are written, dated.
    new = list(dict.fromkeys(record for record in records if record not in set(held)))
    if not new:
        return []
    if not slug:
        raise ValueError(
            f"{len(new)} of the tuple's {len(records)} records are not in {DIRECTORY}: "
            "rerun `python -m devtools.release_records migrate --slug <lane or bead>-"
            f"<topic>` to write them as {day.isoformat()}-<slug>.yaml, or write each "
            f"there by hand as {NEW_NAME} and delete the tuple"
        )
    if len(new) == 1:
        return [(f"{day.isoformat()}-{slug}.yaml", new[0])]
    return [(f"{day.isoformat()}-{slug}-{n}.yaml", record) for n, record in enumerate(new, 1)]


def migrate(
    repo: Path = REPO, *, slug: str | None = None, day: datetime.date | None = None
) -> tuple[Path, ...]:
    """Move the literal tuple out of `release.py`, writing a file for each record the
    directory does not already hold, and return the files written.

    On a tree with no records, which is how `0000-` to `0246-` were written, each record
    is `NNNN-<first path>.yaml` at its tuple index. On a tree that has records, a branch
    from before the move merging main, the tuple's records the files hold are dropped,
    wherever they sit, and the rest are written as `<day>-<slug>.yaml` (numbered `-1`,
    `-2` when there are several), which needs `slug`. Refuses to replace a file holding a
    different record, and removes the tuple only once every file it wrote reads back as
    the record it came from. Writes nothing when there is no tuple.
    """
    release = repo / RELEASE_PATH
    source = release.read_bytes()
    node = _tuple_assignment(source)
    if node is None:
        return ()
    records = literal(source)
    directory = repo / DIRECTORY
    planned = []
    for name, record in _planned(
        records, load(repo), slug=slug, day=day or datetime.datetime.now(datetime.UTC).date()
    ):
        if (problem := _name_problem(name)) is not None:
            raise ValueError(f"{DIRECTORY}/{name}: {problem}")
        target, text = directory / name, render(record)
        if target.exists() and target.read_text(encoding="utf-8") != text:
            raise ValueError(
                f"{DIRECTORY}/{name} already holds a different record; the tuple stays"
            )
        planned.append((target, text, record))
    directory.mkdir(parents=True, exist_ok=True)
    for target, text, _record in planned:
        target.write_text(text, encoding="utf-8")
    for target, _text, record in planned:
        if parse(target.name, target.read_text(encoding="utf-8")) != record:
            raise ValueError(f"{DIRECTORY}/{target.name} does not read back; the tuple stays")
    if not set(records) <= set(load(repo)):
        raise ValueError(f"{DIRECTORY} does not hold every record of {TUPLE}; the tuple stays")
    lines = source.decode("utf-8").splitlines(keepends=True)
    start, end = node.lineno - 1, node.end_lineno or node.lineno
    while end < len(lines) and not lines[end].strip():
        end += 1
    if end == len(lines):
        while start and not lines[start - 1].strip():
            start -= 1
    release.write_text("".join(lines[:start] + lines[end:]), encoding="utf-8")
    if _tuple_assignment(release.read_bytes()) is not None:
        raise ValueError(f"{RELEASE_PATH} still assigns {TUPLE}")
    return tuple(target for target, _text, _record in planned)


def retained_at(repo: Path, revision: str) -> tuple[ReleaseNoPublicChange, ...]:
    """Every record `revision` holds: its literal tuple, if any, then its files."""
    listed = _git(repo, "ls-tree", "--name-only", revision, "--", RELEASE_PATH)
    source = _git(repo, "show", f"{revision}:{RELEASE_PATH}") if listed.strip() else None
    return (*literal(source), *load_at(repo, revision))


def compared(repo: Path, revision: str) -> str:
    """How the working tree's records stand against `revision`'s, in one line."""
    current, retained = load(repo), retained_at(repo, revision)
    fresh = sum(record not in set(retained) for record in current)
    kept = current[: len(retained)] == retained
    return (
        f"{len(current)} records; {revision} holds {len(retained)}, which the working "
        f"tree {'keeps' if kept else 'does not keep'} in order; {fresh} fresh"
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "migrate"))
    parser.add_argument(
        "--against",
        metavar="REVISION",
        help="With check, compare with the records a revision holds, tuple or files",
    )
    parser.add_argument(
        "--slug",
        help="With migrate on a tree that has records: <lane or bead>-<topic>, naming "
        "the files written for the tuple's records the directory lacks",
    )
    parser.add_argument(
        "--date",
        type=datetime.date.fromisoformat,
        help="With migrate: the day those files are dated, by default today in UTC",
    )
    options = parser.parse_args(argv)
    try:
        if options.command == "migrate":
            written = migrate(slug=options.slug, day=options.date)
            print(f"release records: moved {len(written)} records into {DIRECTORY}")
        elif options.against:
            print(f"release records: {compared(REPO, options.against)}")
        else:
            print(f"release records: {len(load())} records in {DIRECTORY} read")
    except (OSError, TypeError, ValueError, SyntaxError) as error:
        print(f"release records: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
