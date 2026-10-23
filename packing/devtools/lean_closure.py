"""Read a Lean project's import closure at a pinned Git commit, and count its kernel escapes.

A formal proof by another author is retained at stage 2 of
``packing/campaign/result-import.md`` as the modules its theorem imports, the build pins
and the proof's own scripts, not as a whole tree. This command says what that is. Given a
checkout of the source, a commit, the Lean project's directory in it and the modules a
theorem lives in, it follows every ``import`` from those modules through the project's
own modules at that commit, and reports:

- the toolchain (``lean-toolchain``) and every package ``lake-manifest.json`` pins, with
  the revision it pins;
- each project module of the closure: its path, Git blob, size, lines, its imports, and
  the count of each kernel-escape token in its code with comments removed
  (`devtools.stage_evand_bentz_lean.ESCAPES`);
- each project module the closure imports and the commit does not hold, which is a
  generated file the source does not store;
- the external roots the closure imports (``Mathlib``, ``Init`` and the like), with the
  number of import lines naming each; and
- ``scope``, the upstream paths an acquisition declaration lists to retain the closure:
  the three build pins and every module found.

It reads Git objects only, with ``git cat-file``, never the working tree, so a
blob-filtered clone with no checkout is enough; each blob is fetched as it is read. It
runs nothing from the source, and builds nothing: a token count is not a parse, and an
escape in a module is reported, never judged.

Usage, from ``packing/``::

    uv run --frozen --all-extras --group dev python -m devtools.lean_closure \\
        CHECKOUT --commit C --root lean Sqpack.RyuBound [--json OUT]
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tomllib
from collections import Counter
from collections.abc import Sequence
from pathlib import Path, PurePosixPath
from typing import TypedDict, cast

from strif import atomic_write_text

from devtools.retained_data import git_blob
from devtools.stage_evand_bentz_lean import ESCAPES, strip_comments

KIND = "lean-import-closure/v1"
PINS = ("lean-toolchain", "lakefile.toml", "lakefile.lean", "lake-manifest.json")

#: One header command: an optional ``module``/``prelude``, then the import lines, which
#: Lean 4 allows to carry ``public``, ``private``, ``meta`` and ``all`` and several names.
_IMPORT = re.compile(r"^(?:(?:public|private)\s+)?(?:meta\s+)?import\s+(?:all\s+)?(.+)$")
_HEADER_WORDS = frozenset({"module", "prelude"})
_LEAN_LIB = re.compile(r"\blean_lib\s+«?([A-Za-z_][A-Za-z0-9_']*)»?")


class Module(TypedDict):
    """One project module of the closure, as the commit holds it."""

    module: str
    path: str
    blob: str
    bytes: int
    lines: int
    imports: list[str]
    escapes: dict[str, int]


class Package(TypedDict):
    """One package ``lake-manifest.json`` pins."""

    name: str
    rev: str
    input_rev: str


class Closure(TypedDict):
    """What `closure` reports, written as JSON by `main`."""

    kind: str
    source_url: str
    commit: str
    tree: str
    root: str
    targets: list[str]
    toolchain: str
    packages: list[Package]
    libraries: list[str]
    modules: list[Module]
    missing: list[str]
    external: dict[str, int]
    escapes: dict[str, int]
    scope: list[str]


class Source:
    """The Git objects of one commit of a checkout, read without its working tree."""

    def __init__(self, checkout: Path, commit: str) -> None:
        self.checkout = checkout
        self.commit = self._git("rev-parse", "--verify", f"{commit}^{{commit}}").strip()
        self.tree = self._git("rev-parse", f"{self.commit}^{{tree}}").strip()
        listing = self._git("ls-tree", "-r", "--full-tree", self.commit)
        self.blobs: dict[str, str] = {}
        for line in listing.splitlines():
            meta, _, path = line.partition("\t")
            mode, kind, blob = meta.split()
            if kind == "blob" and mode in {"100644", "100755"}:
                self.blobs[path] = blob

    def _git(self, *arguments: str) -> str:
        done = subprocess.run(
            ("git", "-C", str(self.checkout), *arguments),
            capture_output=True,
            text=True,
            check=False,
        )
        if done.returncode:
            raise SystemExit(f"git {' '.join(arguments)}: {done.stderr.strip()}")
        return done.stdout

    def url(self) -> str:
        done = subprocess.run(
            ("git", "-C", str(self.checkout), "remote", "get-url", "origin"),
            capture_output=True,
            text=True,
            check=False,
        )
        return done.stdout.strip()

    def read(self, path: str) -> bytes:
        """The bytes of ``path`` at the commit, checked against the tree's blob."""
        blob = self.blobs[path]
        data = subprocess.run(
            ("git", "-C", str(self.checkout), "cat-file", "blob", blob),
            capture_output=True,
            check=True,
        ).stdout
        if git_blob(data) != blob:
            raise SystemExit(f"{path}: the bytes read are not blob {blob}")
        return data


def header_imports(text: str) -> list[str]:
    """The modules a Lean file's header imports, in order, comments removed."""
    found: list[str] = []
    for raw in strip_comments(text).splitlines():
        line = raw.strip()
        if not line or line in _HEADER_WORDS:
            continue
        match = _IMPORT.match(line)
        if not match:
            break
        found.extend(name.strip("«»") for name in match.group(1).split())
    return found


def libraries(source: Source, root: str) -> list[str]:
    """The ``lean_lib`` names the project's lakefile declares, else its top-level names."""
    base = PurePosixPath(root)
    toml, lean = str(base / "lakefile.toml"), str(base / "lakefile.lean")
    if toml in source.blobs:
        data = tomllib.loads(source.read(toml).decode("utf-8"))
        libs = cast("list[dict[str, object]]", data.get("lean_lib") or [])
        names = [str(lib["name"]) for lib in libs if "name" in lib]
        if names:
            return sorted(names)
    if lean in source.blobs:
        names = _LEAN_LIB.findall(source.read(lean).decode("utf-8"))
        if names:
            return sorted(set(names))
    prefix = f"{base}/" if root not in {"", "."} else ""
    tops = {
        PurePosixPath(path[len(prefix) :]).parts[0].removesuffix(".lean")
        for path in source.blobs
        if path.startswith(prefix) and path.endswith(".lean")
    }
    return sorted(tops)


def _packages(source: Source, root: str) -> list[Package]:
    path = str(PurePosixPath(root) / "lake-manifest.json")
    if path not in source.blobs:
        return []
    data = cast("dict[str, object]", json.loads(source.read(path)))
    entries = cast("list[dict[str, object]]", data.get("packages") or [])
    return [
        Package(
            name=str(entry.get("name", "")),
            rev=str(entry.get("rev", "")),
            input_rev=str(entry.get("inputRev", "")),
        )
        for entry in entries
    ]


def _module_path(root: str, module: str) -> str:
    return str(PurePosixPath(root, *module.split("."))) + ".lean"


def escape_counts(text: str) -> dict[str, int]:
    """Occurrences of each kernel-escape token in ``text`` with its comments removed."""
    code = strip_comments(text)
    return {token: len(re.findall(token, code, flags=re.MULTILINE)) for token in ESCAPES}


def closure(source: Source, root: str, targets: Sequence[str]) -> Closure:
    """Follow every import from ``targets`` through the project's modules at the commit."""
    libs = libraries(source, root)
    modules: dict[str, Module] = {}
    missing: set[str] = set()
    external: Counter[str] = Counter()
    queue = list(targets)
    while queue:
        name = queue.pop()
        if name in modules or name in missing:
            continue
        top = name.split(".")[0]
        if top not in libs:
            external[top] += 1
            continue
        path = _module_path(root, name)
        if path not in source.blobs:
            missing.add(name)
            continue
        data = source.read(path)
        text = data.decode("utf-8")
        imports = header_imports(text)
        modules[name] = Module(
            module=name,
            path=path,
            blob=source.blobs[path],
            bytes=len(data),
            lines=text.count("\n"),
            imports=imports,
            escapes=escape_counts(text),
        )
        for imported in imports:
            if imported.split(".")[0] in libs:
                queue.append(imported)
            else:
                external[imported.split(".")[0]] += 1
    toolchain_path = str(PurePosixPath(root) / "lean-toolchain")
    toolchain = (
        source.read(toolchain_path).decode("utf-8").strip()
        if toolchain_path in source.blobs
        else ""
    )
    totals: Counter[str] = Counter()
    for module in modules.values():
        totals.update(module["escapes"])
    pins = [str(PurePosixPath(root) / pin) for pin in PINS]
    scope = sorted(
        [pin for pin in pins if pin in source.blobs]
        + [module["path"] for module in modules.values()]
    )
    return Closure(
        kind=KIND,
        source_url=source.url(),
        commit=source.commit,
        tree=source.tree,
        root=root,
        targets=list(targets),
        toolchain=toolchain,
        packages=_packages(source, root),
        libraries=libs,
        modules=[modules[name] for name in sorted(modules)],
        missing=sorted(missing),
        external=dict(sorted(external.items())),
        escapes={token: totals.get(token, 0) for token in ESCAPES},
        scope=scope,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("checkout", type=Path, help="a Git checkout of the source")
    parser.add_argument("--commit", required=True, help="the pinned commit")
    parser.add_argument("--root", default=".", help="the Lean project's directory in it")
    parser.add_argument("modules", nargs="+", help="the modules the theorems live in")
    parser.add_argument("--json", type=Path, help="also write the report here")
    args = parser.parse_args(argv)
    report = closure(Source(args.checkout, args.commit), args.root, args.modules)
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.json:
        atomic_write_text(args.json, text)
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
