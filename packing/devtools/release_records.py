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
`<YYYY-MM-DD>-<slug>.yaml`**: the day it is written and a few lower-case words naming the
change, such as `2026-11-02-l16-survey-replies.yaml`. It holds `components`, `paths`,
`outputs` and `reason`, the fields of `ReleaseNoPublicChange`; the schema beside the
directory, `no-public-change.schema.yaml`, is the contract, and a file that breaks it, or
is named otherwise, is refused with its name rather than skipped. Whether a fresh record
covers its change is still the gate's question. Records are read in name order: the 246
moved from the tuple keep its order as `0000-` to `0245-`, each named after its first
path, and every dated name sorts after them.

A union merge driver was measured and refused. Git applies one to a whole file, not to a
block, and `release.py` also conflicts at `DATA_REVISION` and the edition histories,
where keeping both sides is silently wrong. Even in the 41 merges where the tuple was
`release.py`'s only conflict, `git merge-file --union` gave Python that does not compile
in 25 and matched the committed resolution in none: Git aligns the lines two appended
records share, splits the conflict around them and keeps both sides of each piece, which
fuses the two records into one (`merge_conflicts --union`).

`python -m devtools.release_records migrate` moved the tuple, refusing unless every file
reads back as the record it came from; it is idempotent, and finds nothing on a tree with
no tuple. `check` reads every record, the quickest way to try a new file, and
`check --against origin/main` says how the records stand against those a revision holds,
as a tuple or as files.
"""

from __future__ import annotations

import argparse
import ast
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
_NAME = re.compile(r"[0-9]{4}-[a-z0-9]+(?:-[a-z0-9]+)*\.yaml")


@functools.cache
def _validator() -> Draft202012Validator:
    return Draft202012Validator(safe_load(SCHEMA.read_text(encoding="utf-8")))


def _checked(where: str, document: object) -> ReleaseNoPublicChange:
    errors = sorted(error.message for error in _validator().iter_errors(document))
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
    if not _NAME.fullmatch(name):
        raise ValueError(f"{where}: name a record <YYYY-MM-DD>-<slug>.yaml, in lower case")
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


def load(repo: Path = REPO) -> tuple[ReleaseNoPublicChange, ...]:
    """Every record in `repo`'s working tree, in name order."""
    directory = repo / DIRECTORY
    if not directory.is_dir():
        return ()
    records = []
    for path in sorted(directory.iterdir()):
        if not path.is_file():
            raise ValueError(f"{DIRECTORY}/{path.name}: a record is a file")
        records.append(parse(path.name, path.read_text(encoding="utf-8")))
    return tuple(records)


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
    """Every record as `revision` holds it, in name order, read in one `git cat-file`."""
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
        records.append(parse(name, body.decode("utf-8")))
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
    """The records a `release.py` from before the move holds as a literal tuple.

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
            _checked(
                where,
                {
                    key: list(value) if isinstance(value, tuple) else value
                    for key, value in values.items()
                },
            )
        )
    return tuple(records)


def _slug(record: ReleaseNoPublicChange) -> str:
    stem = PurePosixPath(record.paths[0]).stem if record.paths else ""
    return re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-") or "record"


def migrate(repo: Path = REPO) -> tuple[Path, ...]:
    """Move the literal tuple out of `release.py` into one file per record, in order.

    Writes `NNNN-<first path>.yaml` for the record at index NNNN, refuses to replace a
    file that holds a different record, and removes the tuple only once every file reads
    back as the record it came from. Returns the files written; none when there is no
    tuple to move.
    """
    release = repo / RELEASE_PATH
    source = release.read_bytes()
    node = _tuple_assignment(source)
    if node is None:
        return ()
    records = literal(source)
    directory = repo / DIRECTORY
    planned = []
    for index, record in enumerate(records):
        target = directory / f"{index:04d}-{_slug(record)}.yaml"
        text = render(record)
        if target.exists() and target.read_text(encoding="utf-8") != text:
            raise ValueError(
                f"{DIRECTORY}/{target.name} already holds a different record; "
                f"{TUPLE}[{index}] was not moved"
            )
        planned.append((target, text))
    directory.mkdir(parents=True, exist_ok=True)
    for target, text in planned:
        target.write_text(text, encoding="utf-8")
    moved = tuple(
        parse(target.name, target.read_text(encoding="utf-8")) for target, _ in planned
    )
    if moved != records:
        raise ValueError(f"{DIRECTORY} does not read back as {TUPLE}; the tuple stays")
    load(repo)
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
    return tuple(target for target, _ in planned)


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
    options = parser.parse_args(argv)
    try:
        if options.command == "migrate":
            written = migrate()
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
