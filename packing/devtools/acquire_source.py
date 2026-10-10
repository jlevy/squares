"""Retain part of a pinned Git checkout as a source packet, and check the packet.

A result by another author is retained under ``packing/resources/web/<packet>/`` at a
pinned revision (``packing/campaign/result-import.md``, stage 2). This command does the
mechanical part. It reads the declaration the packet carries,
``acquisition/declaration.json`` (`Declaration`), and a local checkout at the declared
commit, and writes:

- the retained files, byte-identical at their upstream paths under the declared
  directory, with data files of more than 1,000 lines stored as deterministic gzip by
  the archive's rule (`devtools.retained_data`);
- ``acquisition/upstream-subtree.sha256``, the SHA-256 of every file in the declared
  scope, retained or not, in ``sha256sum`` form with ``./``-relative upstream paths; and
- ``acquisition/sources.json``, the acquisition record. `Record`, `Source` and
  `PinnedOnly` are its contract: every field they name is required unless marked
  optional, and their docstrings say what each field means.

It only reads the checkout. The revision, tree and commit date come from Git, and each
file's bytes are bound to the commit by comparing its Git blob with ``git ls-tree``, so a
shallow or sparse checkout is enough and a locally modified file is refused. A file the
declaration pins by digest only is listed in the record with its size, digest and reason;
where the reason is that another packet already retains the same bytes, the declaration
names that copy and the bytes are compared. A copy that its packet's ``Original Gzip
Files`` table lists is compared as stored; any other is compared after decompression.

``--check`` needs no checkout. From the packet alone it re-derives that the record and
the declaration have every required field, that every retained file, after decompression,
has the digest the manifest records, that the manifest is exactly the retained files plus
the pinned-only ones, that every count, size and named identical copy in the record is
true, that the declaration still yields this record, and that the README's Compressed
Files table matches the stored files. It decides nothing about what the files claim.

The packet's ``README.md`` is prose and is not written here; writing the packet prints
the rows its Compressed Files table needs. Three limits are deliberate. One packet holds
one source. An upstream file whose own name ends in ``.gz`` is pinned only by default.
A declaration may explicitly retain selected ``original_gzip`` upstream paths unchanged;
the record repeats their stored paths and a separate ``Original Gzip Files`` table binds
their compressed bytes. These files are never renamed or recompressed. The record lists
every pinned-only file, so the scope is the claim directories and the few root files a
packet answers for, not a whole tree.

Usage, from ``packing/``::

    uv run --frozen --all-extras --group dev python -m devtools.acquire_source \\
        PACKET --checkout CHECKOUT
    uv run --frozen --all-extras --group dev python -m devtools.acquire_source PACKET --check
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import zlib
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import NotRequired, TypedDict, cast, get_args, get_origin, get_type_hints

from strif import atomic_write_text

from devtools.retained_data import (
    DATA_SUFFIXES,
    GZIP_SUFFIX,
    LINE_THRESHOLD,
    ORIGINAL_GZIP_HEADING,
    candidates,
    check_packet,
    compress,
    describe,
    describe_original_gzip,
    git_blob,
    read_original_gzip_bytes,
    read_retained_bytes,
    read_table,
)

REPO = Path(__file__).resolve().parents[2]
_WEB = PurePosixPath("packing/resources/web")
WEB = REPO / _WEB

FORMAT = "external-source-acquisition-v1"
DECLARATION_FORMAT = "external-source-declaration-v1"
DECLARATION = Path("acquisition/declaration.json")
RECORD = Path("acquisition/sources.json")
MANIFEST = Path("acquisition/upstream-subtree.sha256")

_HEX40 = re.compile(r"[0-9a-f]{40}")
_HEX64 = re.compile(r"[0-9a-f]{64}")
_UTC = re.compile(r"\d{4}-\d\d-\d\dT\d\d:\d\d(:\d\d)?Z")
_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
_REGULAR_FILE_MODES = frozenset({"100644", "100755"})


# --------------------------------------------------------------------------- the contract


class PinnedOnly(TypedDict):
    """One upstream file in the scope that is pinned by digest and not copied.

    - ``path``: the file's path in the upstream tree.
    - ``bytes``: its size, which the manifest does not carry.
    - ``sha256``: its SHA-256, equal to its line in the subtree manifest.
    - ``reason``: why it is not retained, as the declaration's rule states it.
    - ``identical_to`` (optional): the repository-relative path of a file this
      repository already retains with the same bytes, plain or as ``X.gz``, or as an
      original gzip that its packet's ``Original Gzip Files`` table lists, whose stored
      bytes are compared.
    """

    path: str
    bytes: int
    sha256: str
    reason: str
    identical_to: NotRequired[str]


class Source(TypedDict):
    """One upstream repository at one commit, and what the packet keeps of it.

    - ``id``: a short name for the source, stable across packets of the same source.
    - ``source_url``: the address the checkout was cloned from.
    - ``source_ref``: the ref that pointed at the commit when it was retrieved.
    - ``source_commit``: the full commit id, which is the pin.
    - ``committed_utc``: the commit's committer date in UTC. Its date names the packet.
    - ``git_tree``: the commit's tree id.
    - ``archived_path``: the repository-relative directory holding the retained files at
      their upstream paths.
    - ``subtree_manifest``: the repository-relative ``sha256sum``-style list of every
      file in the scope.
    - ``subtree_scope``: the upstream files and directories the manifest covers. The
      rest of the tree is pinned by the commit alone.
    - ``subtree_file_count``, ``subtree_total_bytes``: the files in the manifest and
      their total upstream size.
    - ``retained_file_count``, ``retained_total_bytes``: the files copied here and their
      logical upstream size (raw bytes for original gzip, decoded for archive compression).
    - ``compressed``: the packet-relative stored paths of the retained files kept as
      deterministic gzip.
    - ``original_gzip`` (optional): packet-relative original upstream gzip paths,
      retained without recompression; their counts and digests refer to raw bytes.
    - ``pinned_only``: every file in the manifest that is not retained (`PinnedOnly`).
    - ``license``: the licence the source's own files state.
    - ``claims``: the results the retained files are evidence for, one line each, as
      the source states them.
    """

    id: str
    source_url: str
    source_ref: str
    source_commit: str
    committed_utc: str
    git_tree: str
    archived_path: str
    subtree_manifest: str
    subtree_scope: list[str]
    subtree_file_count: int
    subtree_total_bytes: int
    retained_file_count: int
    retained_total_bytes: int
    compressed: list[str]
    original_gzip: NotRequired[list[str]]
    pinned_only: list[PinnedOnly]
    license: str
    claims: list[str]


class Record(TypedDict):
    """The acquisition record, ``acquisition/sources.json``.

    - ``format``: `FORMAT`.
    - ``retrieved_at_utc``: when the checkout was fetched, to the minute or second.
    - ``git_scope``: how much of the repository was fetched and what the manifest
      covers, in a sentence.
    - ``sources``: the sources retained. This tool writes one (`Source`).
    """

    format: str
    retrieved_at_utc: str
    git_scope: str
    sources: list[Source]


class Rule(TypedDict):
    """Which files of the scope are pinned by digest only, and why.

    - ``match``: a glob over upstream paths. ``*`` stays within one path component and
      ``**`` crosses them. The first rule that matches a file decides it.
    - ``reason``: why the files are not retained.
    - ``identical_to`` (optional): the repository-relative path of a retained file with
      the same bytes, or of a directory holding one under each matched file's name. The
      bytes are compared as `PinnedOnly` says.
    """

    match: str
    reason: str
    identical_to: NotRequired[str]


class Declaration(TypedDict):
    """What to retain, ``acquisition/declaration.json``: the input a person writes.

    - ``format``: `DECLARATION_FORMAT`.
    - ``id``, ``source_url``, ``source_ref``, ``source_commit``, ``retrieved_at_utc``,
      ``git_scope``, ``license``, ``claims``: copied into the record (`Record`,
      `Source`). A checkout at any other commit is refused.
    - ``archived_dir``: the directory inside the packet that receives the retained
      files. It is replaced whole on every run.
    - ``scope``: the upstream files and directories to digest.
    - ``original_gzip`` (optional): exact upstream gzip paths to retain unchanged.
    - ``pinned_only``: the rules for what is digested and not copied (`Rule`). A file in
      the scope that no rule matches is retained.
    """

    format: str
    id: str
    source_url: str
    source_ref: str
    source_commit: str
    retrieved_at_utc: str
    git_scope: str
    archived_dir: str
    license: str
    claims: list[str]
    scope: list[str]
    pinned_only: list[Rule]
    original_gzip: NotRequired[list[str]]


type _Shape = type[PinnedOnly | Source | Record | Rule | Declaration]


def _kind_problems(value: object, hint: object, where: str) -> list[str]:
    if hint is str:
        if not isinstance(value, str):
            return [f"{where} is not a string"]
        return [] if value else [f"{where} is empty"]
    if hint is int:
        whole = isinstance(value, int) and not isinstance(value, bool)
        return [] if whole else [f"{where} is not an integer"]
    if get_origin(hint) is list:
        if not isinstance(value, list):
            return [f"{where} is not a list"]
        (item,) = get_args(hint)
        return [
            problem
            for index, member in enumerate(cast("list[object]", value))
            for problem in _kind_problems(member, item, f"{where}[{index}]")
        ]
    return shape_problems(value, cast("_Shape", hint), where)


def shape_problems(value: object, shape: _Shape, where: str) -> list[str]:
    """Every required field of ``shape`` that ``value`` lacks, and every mistyped one."""
    if not isinstance(value, dict):
        return [f"{where} is not an object"]
    fields = cast("dict[str, object]", value)
    problems: list[str] = []
    # Read from the hints, not `__required_keys__`, which counts a `NotRequired` field as
    # required when the module's annotations are strings.
    for name, hint in get_type_hints(shape, include_extras=True).items():
        optional = get_origin(hint) is NotRequired
        if name in fields:
            kind = get_args(hint)[0] if optional else hint
            problems.extend(_kind_problems(fields[name], kind, f"{where}.{name}"))
        elif not optional:
            problems.append(f"{where} lacks the required field {name}")
    return problems


# --------------------------------------------------------------------------- helpers


def _require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _git(checkout: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=checkout, capture_output=True, text=True, check=True
    ).stdout


def _in_scope(path: str, scope: Sequence[str]) -> bool:
    return any(path == entry or path.startswith(entry.rstrip("/") + "/") for entry in scope)


def _rule_for(path: str, rules: Sequence[Rule]) -> Rule | None:
    return next((rule for rule in rules if PurePosixPath(path).full_match(rule["match"])), None)


def _twin(rule: Rule, path: str, root: Path) -> str | None:
    """The repository-relative file the rule says holds the same bytes as ``path``."""
    target = rule.get("identical_to")
    if target is None:
        return None
    return f"{target}/{PurePosixPath(path).name}" if (root / target).is_dir() else target


def _original_gzip_twin(twin: str, root: Path) -> bool:
    """Whether the packet holding ``twin`` lists it in its ``Original Gzip Files`` table.

    That table is the custody that binds an upstream gzip's raw bytes
    (`devtools.retained_data`), so it, and never the file's name, decides that the stored
    bytes are the upstream bytes.
    """
    parts, web = PurePosixPath(twin).parts, _WEB.parts
    if parts[: len(web)] != web or len(parts) < len(web) + 2:
        return False
    readme = root.joinpath(*parts[: len(web) + 1], "README.md")
    stored = PurePosixPath(*parts[len(web) + 1 :]).as_posix()
    return readme.is_file() and any(
        row.stored == stored for row in read_table(readme, heading=ORIGINAL_GZIP_HEADING)
    )


def _twin_bytes(twin: str, root: Path) -> bytes:
    """The upstream bytes of the retained file ``twin``: as stored for an original gzip,
    and otherwise plain or decompressed from ``X.gz`` (`read_retained_bytes`)."""
    path = root / twin
    if _original_gzip_twin(twin, root):
        return read_original_gzip_bytes(path)
    return read_retained_bytes(path)


def load_declaration(packet: Path) -> Declaration:
    """The packet's declaration, refused unless it has every field of `Declaration`."""
    value: object = json.loads((packet / DECLARATION).read_text(encoding="utf-8"))
    problems = shape_problems(value, Declaration, DECLARATION.as_posix())
    _require(not problems, "; ".join(problems))
    declaration = cast("Declaration", value)
    _require(declaration["format"] == DECLARATION_FORMAT, f"format is not {DECLARATION_FORMAT}")
    directory = declaration["archived_dir"]
    _require(
        _NAME.fullmatch(directory) is not None and directory != DECLARATION.parts[0],
        f"archived_dir must be one plain directory name: {directory!r}",
    )
    originals = declaration.get("original_gzip", [])
    _require(len(originals) == len(set(originals)), "original_gzip lists a path twice")
    for path in originals:
        relative = PurePosixPath(path)
        _require(
            not relative.is_absolute()
            and ".." not in relative.parts
            and relative.as_posix() == path
            and path.endswith(GZIP_SUFFIX)
            and _in_scope(path, declaration["scope"]),
            f"invalid original_gzip path: {path}",
        )
    return declaration


def read_manifest(path: Path) -> dict[str, str]:
    """The ``sha256sum``-style list of ``./``-relative upstream paths, as path to digest."""
    expected: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        digest, separator, name = line.partition("  ")
        relative = PurePosixPath(name.removeprefix("./"))
        _require(
            bool(separator)
            and _HEX64.fullmatch(digest) is not None
            and name.startswith("./")
            and relative.as_posix() == name.removeprefix("./")
            and ".." not in relative.parts
            and relative.as_posix() not in expected,
            f"invalid or duplicate manifest entry: {line!r}",
        )
        expected[relative.as_posix()] = digest
    _require(bool(expected), "empty subtree manifest")
    return expected


# --------------------------------------------------------------------------- acquire


def _pinned_tree(checkout: Path, scope: Sequence[str]) -> dict[str, bytes]:
    """Every file of the scope at HEAD, read from the working tree and bound to its blob."""
    tree: dict[str, tuple[str, str]] = {}
    for line in _git(checkout, "ls-tree", "-r", "-z", "HEAD").split("\0"):
        if line:
            meta, _, name = line.partition("\t")
            mode, _, blob = meta.split()
            tree[name] = (mode, blob)
    for entry in scope:
        _require(
            any(_in_scope(path, [entry]) for path in tree),
            f"scope entry is not in the tree: {entry}",
        )
    contents: dict[str, bytes] = {}
    for path in sorted(path for path in tree if _in_scope(path, scope)):
        mode, blob = tree[path]
        _require(mode in _REGULAR_FILE_MODES, f"not a regular file (mode {mode}): {path}")
        data = (checkout / path).read_bytes()
        _require(git_blob(data) == blob, f"bytes are not the pinned blob: {path}")
        contents[path] = data
    return contents


def acquire(packet: Path, checkout: Path, root: Path) -> Source:
    """Write the packet's retained files, manifest and record from a pinned checkout.

    ``root`` is the repository root that the record's paths are relative to. Only the
    declared directory and the two acquisition files are written; the directory is
    replaced whole, so a file the declaration no longer retains does not linger.
    """
    declaration = load_declaration(packet)
    commit = _git(checkout, "rev-parse", "HEAD").strip()
    _require(
        commit == declaration["source_commit"],
        f"checkout is at {commit}, not the declared {declaration['source_commit']}",
    )
    committed = datetime.fromisoformat(_git(checkout, "show", "-s", "--format=%cI").strip())
    committed_utc = committed.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    _require(
        packet.name.endswith(committed_utc[:10]),
        f"a packet is named for the UTC date of its pin, {committed_utc[:10]}: {packet.name}",
    )
    contents = _pinned_tree(checkout, declaration["scope"])
    rules = declaration["pinned_only"]
    chosen = {path: _rule_for(path, rules) for path in contents}
    for rule in rules:
        _require(
            any(used is rule for used in chosen.values()),
            f"pinned_only rule decides no file: {rule['match']}",
        )
    originals = declaration.get("original_gzip", [])
    for path in originals:
        _require(
            path in contents and chosen[path] is None,
            f"original_gzip must name a retained source file: {path}",
        )
    pinned: list[PinnedOnly] = []
    for path, rule in chosen.items():
        if rule is None:
            _require(
                not path.endswith(GZIP_SUFFIX) or path in originals,
                f"an upstream {GZIP_SUFFIX} file can be pinned but not retained: {path}",
            )
            continue
        item: PinnedOnly = {
            "path": path,
            "bytes": len(contents[path]),
            "sha256": _sha256(contents[path]),
            "reason": rule["reason"],
        }
        twin = _twin(rule, path, root)
        if twin is not None:
            _require(
                _twin_bytes(twin, root) == contents[path],
                f"{path} is not the bytes of {twin}",
            )
            item["identical_to"] = twin
        pinned.append(item)
    retained = [path for path, rule in chosen.items() if rule is None]

    source = packet / declaration["archived_dir"]
    if source.exists():
        shutil.rmtree(source)
    compressed: list[str] = []
    for path in retained:
        target = source / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(contents[path])
        if target.suffix in DATA_SUFFIXES and contents[path].count(b"\n") > LINE_THRESHOLD:
            compressed.append(compress(target).relative_to(packet).as_posix())
    atomic_write_text(
        packet / MANIFEST,
        "".join(f"{_sha256(data)}  ./{path}\n" for path, data in contents.items()),
        encoding="utf-8",
    )
    entry: Source = {
        "id": declaration["id"],
        "source_url": declaration["source_url"],
        "source_ref": declaration["source_ref"],
        "source_commit": commit,
        "committed_utc": committed_utc,
        "git_tree": _git(checkout, "rev-parse", "HEAD^{tree}").strip(),
        "archived_path": source.relative_to(root).as_posix(),
        "subtree_manifest": (packet / MANIFEST).relative_to(root).as_posix(),
        "subtree_scope": declaration["scope"],
        "subtree_file_count": len(contents),
        "subtree_total_bytes": sum(len(data) for data in contents.values()),
        "retained_file_count": len(retained),
        "retained_total_bytes": sum(len(contents[path]) for path in retained),
        "compressed": compressed,
        "pinned_only": pinned,
        "license": declaration["license"],
        "claims": declaration["claims"],
    }
    if originals:
        entry["original_gzip"] = [f"{declaration['archived_dir']}/{path}" for path in originals]
    record: Record = {
        "format": FORMAT,
        "retrieved_at_utc": declaration["retrieved_at_utc"],
        "git_scope": declaration["git_scope"],
        "sources": [entry],
    }
    atomic_write_text(packet / RECORD, json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return entry


# --------------------------------------------------------------------------- check


def _retained(
    source: Path, manifest: Mapping[str, str], original_gzip: Sequence[str] = ()
) -> tuple[dict[str, int], list[str]]:
    """Each stored file's upstream path and decompressed size, and what is wrong with any."""
    sizes: dict[str, int] = {}
    problems: list[str] = []
    for path in sorted(path for path in source.rglob("*") if path.is_file()):
        stored = path.relative_to(source).as_posix()
        original = f"{source.name}/{stored}" in original_gzip
        upstream = stored if original else stored.removesuffix(GZIP_SUFFIX)
        if upstream in sizes:
            problems.append(f"{upstream} is retained twice, plain and compressed")
            continue
        try:
            data = read_original_gzip_bytes(path) if original else read_retained_bytes(path)
        except (OSError, ValueError, EOFError, zlib.error) as error:
            problems.append(f"{stored} cannot be read: {error}")
            continue
        sizes[upstream] = len(data)
        if upstream not in manifest:
            problems.append(f"{stored} is retained but is not in the subtree manifest")
        elif _sha256(data) != manifest[upstream]:
            problems.append(f"{stored} does not have the digest its manifest records")
    return sizes, problems


def _pinned_problems(
    entry: Source, manifest: Mapping[str, str], sizes: Mapping[str, int], root: Path
) -> list[str]:
    """The manifest is the retained files plus the pinned-only ones, each as recorded."""
    problems: list[str] = []
    pinned = {item["path"]: item for item in entry["pinned_only"]}
    if len(pinned) != len(entry["pinned_only"]):
        problems.append("pinned_only lists a path twice")
    problems.extend(
        f"{path} is both retained and pinned only" for path in sorted(sizes.keys() & pinned)
    )
    problems.extend(
        f"{path} is in the subtree manifest but neither retained nor pinned only"
        for path in sorted(manifest.keys() - sizes.keys() - pinned.keys())
    )
    for path, item in pinned.items():
        if manifest.get(path) != item["sha256"]:
            problems.append(f"pinned-only {path} does not have its manifest digest")
        twin = item.get("identical_to")
        if twin is None:
            continue
        try:
            same = _sha256(_twin_bytes(twin, root)) == item["sha256"]
        except OSError, ValueError, EOFError, zlib.error:
            same = False
        if not same:
            problems.append(f"pinned-only {path} is not the bytes of {twin}")
    return problems


def _derived_problems(
    packet: Path, entry: Source, manifest: Mapping[str, str], sizes: Mapping[str, int]
) -> list[str]:
    """Every field of the record that the packet's own files determine."""
    source = packet / PurePosixPath(entry["archived_path"]).name
    retained_bytes = sum(sizes.values())
    derived: list[tuple[str, object, object]] = [
        ("subtree_file_count", entry["subtree_file_count"], len(manifest)),
        ("retained_file_count", entry["retained_file_count"], len(sizes)),
        ("retained_total_bytes", entry["retained_total_bytes"], retained_bytes),
        (
            "subtree_total_bytes",
            entry["subtree_total_bytes"],
            retained_bytes + sum(item["bytes"] for item in entry["pinned_only"]),
        ),
        (
            "compressed",
            sorted(entry["compressed"]),
            sorted(
                path.relative_to(packet).as_posix()
                for path in source.rglob(f"*{GZIP_SUFFIX}")
                if path.relative_to(packet).as_posix() not in entry.get("original_gzip", [])
            ),
        ),
    ]
    problems = [
        f"{name} is {recorded!r}, and the packet's files give {found!r}"
        for name, recorded, found in derived
        if recorded != found
    ]
    originals = entry.get("original_gzip", [])
    if len(originals) != len(set(originals)):
        problems.append("original_gzip lists a path twice")
    retained_names = {f"{source.name}/{name}" for name in sizes}
    problems.extend(
        f"original_gzip is not a retained upstream gzip: {path}"
        for path in originals
        if path not in retained_names or not path.endswith(GZIP_SUFFIX)
    )
    scope = entry["subtree_scope"]
    problems.extend(
        f"{path} is in the manifest but outside subtree_scope"
        for path in manifest
        if not _in_scope(path, scope)
    )
    problems.extend(
        f"subtree_scope entry covers no manifest file: {item}"
        for item in scope
        if not any(_in_scope(path, [item]) for path in manifest)
    )
    for name, value, pattern in (
        ("source_commit", entry["source_commit"], _HEX40),
        ("git_tree", entry["git_tree"], _HEX40),
        ("committed_utc", entry["committed_utc"], _UTC),
    ):
        if pattern.fullmatch(value) is None:
            problems.append(f"{name} is malformed: {value!r}")
    if not packet.name.endswith(entry["committed_utc"][:10]):
        problems.append(f"the packet is not named for the UTC date of its pin, {packet.name}")
    problems.extend(
        f"{path.relative_to(packet).as_posix()} is a data file of more than "
        f"{LINE_THRESHOLD} lines stored plain"
        for path in candidates(source)
    )
    return problems


def _declaration_problems(
    packet: Path, record: Record, entry: Source, manifest: Mapping[str, str], root: Path
) -> list[str]:
    """The declaration still yields this record, so the same command reproduces it."""
    try:
        declaration = load_declaration(packet)
    except (OSError, ValueError) as error:
        return [f"{DECLARATION}: {error}"]
    copied: list[tuple[str, object, object]] = [
        ("id", declaration["id"], entry["id"]),
        ("source_url", declaration["source_url"], entry["source_url"]),
        ("source_ref", declaration["source_ref"], entry["source_ref"]),
        ("source_commit", declaration["source_commit"], entry["source_commit"]),
        ("license", declaration["license"], entry["license"]),
        ("claims", declaration["claims"], entry["claims"]),
        ("scope", declaration["scope"], entry["subtree_scope"]),
        ("retrieved_at_utc", declaration["retrieved_at_utc"], record["retrieved_at_utc"]),
        ("git_scope", declaration["git_scope"], record["git_scope"]),
        (
            "archived_dir",
            declaration["archived_dir"],
            PurePosixPath(entry["archived_path"]).name,
        ),
    ]
    problems = [
        f"the declaration's {name} is not the record's"
        for name, ours, theirs in copied
        if ours != theirs
    ]
    expected_originals = [
        f"{declaration['archived_dir']}/{path}" for path in declaration.get("original_gzip", [])
    ]
    if expected_originals != entry.get("original_gzip", []):
        problems.append("the declaration's original_gzip is not the record's")
    pinned = {item["path"]: item for item in entry["pinned_only"]}
    for path in manifest:
        rule = _rule_for(path, declaration["pinned_only"])
        item = pinned.get(path)
        expected = None if rule is None else (rule["reason"], _twin(rule, path, root))
        recorded = None if item is None else (item["reason"], item.get("identical_to"))
        if expected != recorded:
            problems.append(f"the declaration's rules no longer decide {path} as recorded")
    return problems


def _source_problems(packet: Path, record: Record, entry: Source, root: Path) -> list[str]:
    source = packet / PurePosixPath(entry["archived_path"]).name
    if (root / entry["archived_path"]) != source:
        return [f"archived_path is not a directory of this packet: {entry['archived_path']}"]
    if (root / entry["subtree_manifest"]) != packet / MANIFEST:
        return [f"subtree_manifest is not this packet's: {entry['subtree_manifest']}"]
    try:
        manifest = read_manifest(packet / MANIFEST)
    except (OSError, ValueError) as error:
        return [f"{MANIFEST}: {error}"]
    sizes, problems = _retained(source, manifest, entry.get("original_gzip", []))
    problems.extend(_pinned_problems(entry, manifest, sizes, root))
    problems.extend(_derived_problems(packet, entry, manifest, sizes))
    problems.extend(_declaration_problems(packet, record, entry, manifest, root))
    return problems


def check(packet: Path, root: Path) -> list[str]:
    """Every way the packet falls short of its contract, from the packet's files alone."""
    try:
        value: object = json.loads((packet / RECORD).read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        return [f"{packet.name}: {RECORD}: {error}"]
    problems = shape_problems(value, Record, RECORD.as_posix())
    if not problems:
        record = cast("Record", value)
        if record["format"] != FORMAT:
            problems.append(f"format is not {FORMAT}")
        if _UTC.fullmatch(record["retrieved_at_utc"]) is None:
            problems.append(f"retrieved_at_utc is malformed: {record['retrieved_at_utc']!r}")
        if len(record["sources"]) != 1:
            problems.append("this tool's packets hold exactly one source")
        for entry in record["sources"]:
            problems.extend(_source_problems(packet, record, entry, root))
        if (packet / "README.md").is_file():
            problems.extend(check_packet(packet))
            origins = {row.stored: row.origin for row in read_table(packet / "README.md")}
            problems.extend(
                f"{stored} is not an upstream row of the README's Compressed Files table"
                for entry in record["sources"]
                for stored in entry["compressed"]
                if origins.get(stored) != "upstream"
            )
            original_rows = read_table(packet / "README.md", heading=ORIGINAL_GZIP_HEADING)
            expected_originals = {
                path for entry in record["sources"] for path in entry.get("original_gzip", [])
            }
            if {row.stored for row in original_rows} != expected_originals:
                problems.append("Original Gzip Files table differs from declared original_gzip")
        else:
            problems.append("the packet has no README.md")
    return [
        problem if problem.startswith(f"{packet.name}: ") else f"{packet.name}: {problem}"
        for problem in problems
    ]


# --------------------------------------------------------------------------- command


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        allow_abbrev=False,
    )
    parser.add_argument(
        "packet", help="the packet's directory name under packing/resources/web/"
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--checkout",
        type=Path,
        help="write the packet from this checkout at the declared commit",
    )
    mode.add_argument(
        "--check", action="store_true", help="re-derive the contract from the packet alone"
    )
    args = parser.parse_args(argv)
    if _NAME.fullmatch(args.packet) is None:
        parser.error(f"not a packet name: {args.packet}")
    packet = WEB / args.packet
    if args.check:
        problems = check(packet, REPO)
        for problem in problems:
            print(problem, file=sys.stderr)
        print("PACKET_DIFFERS_FROM_ITS_CONTRACT" if problems else "PACKET_MATCHES_ITS_CONTRACT")
        return 1 if problems else 0
    entry = acquire(packet, args.checkout.resolve(), REPO)
    pinned_bytes = entry["subtree_total_bytes"] - entry["retained_total_bytes"]
    print(
        f"{entry['source_commit']} committed {entry['committed_utc']}: "
        f"retained {entry['retained_file_count']} files, "
        f"{entry['retained_total_bytes']} bytes; "
        f"pinned only {len(entry['pinned_only'])} files, {pinned_bytes} bytes"
    )
    for stored in entry["compressed"]:
        print(describe(packet, packet / stored, "upstream").markdown())
    for stored in entry.get("original_gzip", []):
        print(describe_original_gzip(packet, packet / stored).markdown())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
