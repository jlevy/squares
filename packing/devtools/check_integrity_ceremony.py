#!/usr/bin/env python3
"""The integrity-ceremony ratchet: digest checks of the repository against itself only leave.

    uv run --frozen --all-extras --group dev python -m devtools.check_integrity_ceremony
    ... --inventory   every site, allowlisted files marked
    ... --update      the baseline rewritten once counts have fallen

OR-16 reserves checksums for real trust boundaries: a downloaded packet against a value
pinned at review, an external checker at a revision, Git ancestry. A tool that hashes its
own source and refuses a checkpoint whose digest moved, a ledger that lists verifiers by
SHA-256, an audit that fails a working file against its historical blob: each compares
the repository with itself, catches nothing Git does not, and has charged real re-runs,
the 6,197 s n11 native run for a dependency change and a capture run sent back to round 0
by a kernel speedup with identical output. The audit of 2026-10-03,
`docs/project/reviews/review-2026-10-03-integrity-ceremony-audit.md`, inventoried every
instance and found the pattern re-added on four dates after OR-16 was written, which is
why it now has a count.

This reads every tracked Python file's syntax tree and counts two forms. Each occurrence
is one *site*:

1. **A self-digest.** A call to a hash function, meaning the callee is named like one
   (`sha256`, `sha`, `digest`, `hexdigest`, `blake2b`, `md5`, `checksum`), whose arguments
   mention `__file__`: a module hashing its own bytes, or a sibling's, to pin them.
2. **A digest comparison.** An `==` or `!=` with an operand that names a digest: an
   identifier such as `MODULE_SHA256`, `expected_sha256` or `digest`; a subscript or `.get`
   whose key is one, such as `record["tool_sha256"]`; or a call to a hash function, such
   as `hashlib.sha256(raw).hexdigest()`. `is` and `in` are not comparisons of a value, and
   a set of expected keys is not a digest.

What names a digest is the `mark` pattern in `devtools/integrity-ceremony.yaml`, held as
data so that this file carries no identifier the pattern would match.

The register has two parts. The **allowlist** names the files whose sites cross a boundary
the review admitted, each with the boundary's `kind` (`download`, `external-checkout`,
`generated-artifact` or `legacy-manifest`) and a sentence naming it. No kind exists for a
file this repository wrote, so an internal pin cannot be listed. Every other file's sites
are held against the **baseline**, a per-file count first seeded on 2026-10-03 from the
tree at `f4642c051`; `--inventory` prints the current total. Only growth is a finding: a
file above its baseline, or a file the baseline does not record that holds a site. Growth
names the file and lists its sites. A fall is never a finding, because removing ceremony
must not cost bookkeeping; the check prints how many files sit below their baseline, and
`--update` tightens the register whenever convenient. `--update` seeds an empty baseline
and otherwise refuses to raise one.

Files are the repository's tracked and untracked-but-unignored `*.py`, as git lists them,
less the literature archive (other authors' bytes, as the lint floor excludes it), the
vendored submodules, the skill mirror and test files. A test that asserts a receipt names
the digest of what ran checks a record; it refuses nothing at run time, so it can charge
no recomputation, and a scan of source text cannot tell it from a tool's refusal. A byte
prescan skips a file that mentions no
digest, so the whole tree costs a few seconds. It is a static scan of source text: it
runs nothing, hashes nothing and reads no retained result, so it can never demand a
recomputation, which is the ceremony it guards against. It runs under the project
interpreter:
`except A, B:` parses on 3.14 and nowhere older (`D-397`).
"""

from __future__ import annotations

import argparse
import ast
import os
import re
import subprocess
from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

from sqpack.yamlio import safe_load

PACKING = Path(__file__).resolve().parent.parent
REPO = PACKING.parent
REGISTER = PACKING / "devtools" / "integrity-ceremony.yaml"
#: Trees the scan leaves alone, each for the reason `test_lint_floor_contract` names.
NOT_OURS = ("packing/resources/", "vendor/", ".claude/skills/", "node_modules/", ".venv/")
#: The boundaries OR-16 admits. There is deliberately no kind for our own files.
KINDS = ("download", "external-checkout", "generated-artifact", "legacy-manifest")
BASELINE_KEY = "baseline:"
#: The two forms. Named so that neither constant is itself a name the mark matches.
FORM_OWN = "self-digest"
FORM_COMPARE = "comparison"
EXCERPT_WIDTH = 88
MAX_WORKERS = 8


class RegisterError(ValueError):
    """The register is not in the shape this tool reads."""


@dataclass(frozen=True)
class Site:
    path: str
    line: int
    form: str
    text: str

    def __str__(self) -> str:
        return f"{self.path}:{self.line}: {self.form}: {self.text}"


@dataclass(frozen=True)
class Entry:
    path: str
    kind: str
    boundary: str


@dataclass(frozen=True)
class Register:
    mark: re.Pattern[str]
    allowlist: dict[str, Entry]
    baseline: dict[str, int]


# ---------------------------------------------------------------------------
# The register
# ---------------------------------------------------------------------------


def _string(value: object, what: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RegisterError(f"{what} must be a non-empty string, not {value!r}")
    return value


def parse_register(text: str, label: str) -> Register:
    """The register's three parts, each refused in the shape it is not."""
    document = safe_load(text)
    if not isinstance(document, dict):
        raise RegisterError(f"{label}: expected a mapping at the top level")
    try:
        mark = re.compile(_string(document.get("mark"), f"{label}: mark"))
    except re.error as error:
        raise RegisterError(f"{label}: mark is not a regular expression: {error}") from error
    allowlist: dict[str, Entry] = {}
    for index, item in enumerate(document.get("allowlist") or []):
        where = f"{label}: allowlist[{index}]"
        if not isinstance(item, dict) or set(item) != {"path", "kind", "boundary"}:
            raise RegisterError(f"{where}: an entry has exactly path, kind and boundary")
        entry = Entry(
            _string(item["path"], f"{where}.path"),
            _string(item["kind"], f"{where}.kind"),
            _string(item["boundary"], f"{where}.boundary"),
        )
        if entry.kind not in KINDS:
            raise RegisterError(
                f"{where}: kind {entry.kind!r} is not one of {', '.join(KINDS)}; a file "
                "this repository wrote has no kind, which is the point"
            )
        if entry.path in allowlist:
            raise RegisterError(f"{where}: {entry.path} is listed twice")
        allowlist[entry.path] = entry
    baseline_raw = document.get("baseline")
    if baseline_raw is None:
        baseline_raw = {}
    if not isinstance(baseline_raw, dict):
        raise RegisterError(f"{label}: baseline must map a path to a count")
    baseline: dict[str, int] = {}
    for path, count in baseline_raw.items():
        _string(path, f"{label}: baseline path")
        if type(count) is not int or count < 1:
            raise RegisterError(f"{label}: baseline[{path}] must be a positive count")
        if path in allowlist:
            raise RegisterError(f"{label}: {path} is both allowlisted and in the baseline")
        baseline[str(path)] = count
    return Register(mark, allowlist, baseline)


def load_register(path: Path = REGISTER) -> Register:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as error:
        raise RegisterError(f"{path}: cannot be read: {error}") from error
    return parse_register(text, path.name)


# ---------------------------------------------------------------------------
# The scan
# ---------------------------------------------------------------------------


def _callee(node: ast.expr) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def _mentions_own_file(call: ast.Call) -> bool:
    """Do the call's arguments reach `__file__`, bare or as a module's attribute?"""
    for argument in (*call.args, *(keyword.value for keyword in call.keywords)):
        for node in ast.walk(argument):
            if isinstance(node, ast.Name) and node.id == "__file__":
                return True
            if isinstance(node, ast.Attribute) and node.attr == "__file__":
                return True
    return False


def _marked(node: ast.expr, mark: re.Pattern[str]) -> bool:
    """Does the operand name a digest, by identifier, by key, or by the function called?

    A literal tuple, list, set or dict names one when an element does, so a record
    compared with `{"path": ROOT, "sha256": ROOT_SHA}` counts; a set of key strings does
    not, because a constant is never a name.
    """
    children: list[ast.expr] = []
    if isinstance(node, ast.Name):
        hit = mark.search(node.id) is not None
    elif isinstance(node, ast.Attribute):
        hit = mark.search(node.attr) is not None
        children = [node.value]
    elif isinstance(node, ast.Subscript):
        hit = _marked_key(node.slice, mark)
        children = [node.value]
    elif isinstance(node, ast.Call):
        name = _callee(node.func)
        hit = (name is not None and mark.search(name) is not None) or (
            name == "get" and bool(node.args) and _marked_key(node.args[0], mark)
        )
        children = list(node.args)
    elif isinstance(node, (ast.Tuple, ast.List, ast.Set)):
        hit = False
        children = list(node.elts)
    elif isinstance(node, ast.Dict):
        hit = False
        children = [value for value in node.values if value is not None]
    else:
        hit = False
    return hit or any(_marked(child, mark) for child in children)


def _marked_key(node: ast.expr, mark: re.Pattern[str]) -> bool:
    """A string constant, a subscript key or a `.get` argument, that names a digest."""
    return (
        isinstance(node, ast.Constant)
        and isinstance(node.value, str)
        and mark.search(node.value) is not None
    )


def _excerpt(source: str, node: ast.AST) -> str:
    segment = ast.get_source_segment(source, node) or ""
    flat = " ".join(segment.split())
    if len(flat) > EXCERPT_WIDTH:
        return flat[: EXCERPT_WIDTH - 1] + "…"
    return flat


def sites_in(path: str, source: str, mark: re.Pattern[str]) -> list[Site]:
    """Every site in one module's source, in line order."""
    if mark.search(source) is None:
        return []
    found: list[Site] = []
    for node in ast.walk(ast.parse(source, filename=path)):
        if isinstance(node, ast.Call):
            name = _callee(node.func)
            if name is not None and mark.search(name) is not None and _mentions_own_file(node):
                found.append(Site(path, node.lineno, FORM_OWN, _excerpt(source, node)))
        elif isinstance(node, ast.Compare) and any(
            isinstance(op, (ast.Eq, ast.NotEq)) for op in node.ops
        ):
            operands = (node.left, *node.comparators)
            if any(_marked(operand, mark) for operand in operands):
                found.append(Site(path, node.lineno, FORM_COMPARE, _excerpt(source, node)))
    return sorted(found, key=lambda site: (site.line, site.form, site.text))


def _ours(path: str) -> bool:
    return not any(path.startswith(prefix) or f"/{prefix}" in f"/{path}" for prefix in NOT_OURS)


def _a_test(path: str) -> bool:
    """A test file: under a `tests/` directory, or named `test_*.py` or `conftest.py`."""
    name = path.rsplit("/", 1)[-1]
    return "/tests/" in f"/{path}" or name.startswith("test_") or name == "conftest.py"


def repository_files(repo: Path) -> list[str]:
    """Every Python file of ours that is not a test, repository-relative, in a stable order.

    Git's tracked and untracked-but-unignored list when `repo` is a work tree, and a walk
    when it is not (a source snapshot, which the negative controls run in).
    """
    listed = _git_listed(repo)
    if listed is None:
        listed = _walked(repo)
    return sorted(
        path for path in listed if _ours(path) and not _a_test(path) and (repo / path).is_file()
    )


def _git_listed(repo: Path) -> list[str] | None:
    listing = ("ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", "*.py")
    try:
        result = subprocess.run(("git", *listing), cwd=repo, capture_output=True, check=False)
        toplevel = subprocess.run(
            ("git", "rev-parse", "--show-toplevel"), cwd=repo, capture_output=True, check=False
        )
    except OSError:
        return None
    if result.returncode != 0 or toplevel.returncode != 0:
        return None
    if Path(toplevel.stdout.decode().strip()).resolve() != repo.resolve():
        return None
    return [entry.decode() for entry in result.stdout.split(b"\0") if entry]


def _walked(repo: Path) -> list[str]:
    found: list[str] = []
    for directory, names, files in os.walk(repo):
        relative = Path(directory).relative_to(repo).as_posix()
        prefix = "" if relative == "." else relative + "/"
        names[:] = sorted(name for name in names if _ours(prefix + name + "/"))
        found.extend(prefix + name for name in files if name.endswith(".py"))
    return found


def scan(repo: Path, register: Register) -> tuple[dict[str, list[Site]], list[str], int]:
    """Sites by file, the files that could not be read, and how many files were read."""
    files = repository_files(repo)

    def one(path: str) -> list[Site] | str:
        try:
            return sites_in(path, (repo / path).read_text(encoding="utf-8"), register.mark)
        except (SyntaxError, UnicodeDecodeError, ValueError) as error:
            return f"{path}: cannot be read as Python: {error}"

    # Threads: the project interpreter is free-threaded, so parsing runs in parallel
    # without pickling a syntax tree across a process.
    with ThreadPoolExecutor(max_workers=min(MAX_WORKERS, os.cpu_count() or 1)) as pool:
        results = list(pool.map(one, files))
    by_file: dict[str, list[Site]] = {}
    unreadable: list[str] = []
    for path, result in zip(files, results, strict=True):
        if isinstance(result, str):
            unreadable.append(result)
        elif result:
            by_file[path] = result
    return by_file, unreadable, len(files)


# ---------------------------------------------------------------------------
# The ratchet
# ---------------------------------------------------------------------------


def ratchet(by_file: dict[str, list[Site]], register: Register, repo: Path) -> list[str]:
    """Every finding: growth, and an allowlist entry that names no site. A fall is none."""
    faults: list[str] = []
    for path, entry in sorted(register.allowlist.items()):
        if not (repo / path).is_file():
            faults.append(f"{path}: allowlisted ({entry.kind}) but there is no such file")
        elif path not in by_file:
            faults.append(
                f"{path}: allowlisted ({entry.kind}) but holds no site; remove the entry"
            )
    for path, sites in sorted(by_file.items()):
        if path in register.allowlist:
            continue
        count = len(sites)
        recorded = register.baseline.get(path)
        if recorded is None:
            faults.append(
                f"{path}: {count} site(s) of integrity ceremony in a file the baseline does "
                "not record. Identify the file by Git revision and path instead (OR-16); a "
                "real boundary is allowlisted with its kind. Every site:"
            )
            faults.extend(f"    {site}" for site in sites)
        elif count > recorded:
            faults.append(
                f"{path}: {count} site(s), the baseline records {recorded}. The count only "
                "falls (OR-16); identify by Git revision and path instead. Every site:"
            )
            faults.extend(f"    {site}" for site in sites)
    return faults


def slack(by_file: dict[str, list[Site]], register: Register) -> list[str]:
    """Every file below its baseline, absent ones included: what `--update` would lower."""
    return [
        path
        for path, recorded in sorted(register.baseline.items())
        if len(by_file.get(path, ())) < recorded
    ]


def growth(by_file: dict[str, list[Site]], register: Register) -> list[str]:
    """Every counted file above its baseline, or absent from it: what `--update` refuses."""
    grown: list[str] = []
    for path, sites in sorted(by_file.items()):
        if path in register.allowlist:
            continue
        recorded = register.baseline.get(path, 0)
        if len(sites) > recorded:
            grown.append(f"{path}: {len(sites)} site(s), the baseline records {recorded}")
    return grown


def totals(by_file: dict[str, list[Site]], register: Register) -> tuple[int, int, int, int]:
    """(counted sites, counted files, self-digests among them, allowlisted files)."""
    counted = {path: sites for path, sites in by_file.items() if path not in register.allowlist}
    sites = sum(len(sites) for sites in counted.values())
    own = sum(1 for sites in counted.values() for site in sites if site.form == FORM_OWN)
    listed = sum(1 for path in by_file if path in register.allowlist)
    return sites, len(counted), own, listed


def inventory(by_file: dict[str, list[Site]], register: Register) -> str:
    """Every site, allowlisted files marked, then the summary line."""
    lines: list[str] = []
    for path, sites in sorted(by_file.items()):
        entry = register.allowlist.get(path)
        if entry is not None:
            lines.append(f"# {path}: allowlisted, {entry.kind}: {entry.boundary}")
        lines.extend(str(site) for site in sites)
    sites, files, own, listed = totals(by_file, register)
    lines.append("")
    lines.append(
        f"# {sites} counted site(s) in {files} file(s), {own} of them self-digests; "
        f"{listed} allowlisted file(s)"
    )
    return "\n".join(lines)


def render_baseline(by_file: dict[str, list[Site]], register: Register) -> str:
    """The baseline block the scan implies."""
    rows = [
        f"  {path}: {len(sites)}"
        for path, sites in sorted(by_file.items())
        if path not in register.allowlist
    ]
    return "\n".join([BASELINE_KEY, *rows]) + "\n"


def update(
    register_path: Path, by_file: dict[str, list[Site]], register: Register
) -> list[str]:
    """Rewrite the baseline block from the scan.

    An empty baseline is seeded from the scan, which is how the register was first
    written. A seeded baseline only ever lowers: growth stays a finding.
    """
    grown = growth(by_file, register) if register.baseline else []
    if grown:
        return ["--update lowers the baseline; it does not absorb growth:", *grown]
    text = register_path.read_text(encoding="utf-8")
    head, found, _ = text.partition(f"\n{BASELINE_KEY}")
    if not found:
        return [f"{register_path.name}: no `{BASELINE_KEY}` line to rewrite after"]
    register_path.write_text(head + "\n" + render_baseline(by_file, register), encoding="utf-8")
    return []


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else "")
    _ = parser.add_argument(
        "--inventory", action="store_true", help="print every site and exit 0"
    )
    _ = parser.add_argument(
        "--update",
        action="store_true",
        help="rewrite the register's baseline from the scan when counts have fallen",
    )
    _ = parser.add_argument("--repo", type=Path, default=REPO, help=argparse.SUPPRESS)
    _ = parser.add_argument("--register", type=Path, default=REGISTER, help=argparse.SUPPRESS)
    arguments = parser.parse_args(argv)
    repo: Path = arguments.repo
    register_path: Path = arguments.register

    try:
        register = load_register(register_path)
    except RegisterError as error:
        print(f"FAIL  {error}")
        return 1
    by_file, unreadable, read = scan(repo, register)

    if arguments.inventory:
        print(inventory(by_file, register))
        return 0
    if arguments.update:
        faults = [*unreadable, *update(register_path, by_file, register)]
        if faults:
            print("\n".join(f"FAIL  {fault}" for fault in faults))
            return 1
        sites, files, _, _ = totals(by_file, register)
        print(f"  {register_path.name}: baseline rewritten, {sites} site(s) in {files} file(s)")
        return 0

    faults = [*unreadable, *ratchet(by_file, register, repo)]
    if faults:
        print("\n".join(f"FAIL  {fault}" for fault in faults))
        print(f"FAIL  {len(faults)} finding(s); see devtools/check_integrity_ceremony.py")
        return 1
    sites, files, own, listed = totals(by_file, register)
    print(
        f"  {sites} site(s) of integrity ceremony in {files} file(s), {own} self-digests, "
        f"none above the baseline; {listed} allowlisted file(s) name their boundary; "
        f"{read} files read"
    )
    below = slack(by_file, register)
    if below:
        print(f"  {len(below)} file(s) below their baseline; --update tightens it (optional)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
