#!/usr/bin/env python3
"""No JavaScript in Python strings: the guard, and the ratchet that retires what is left.

    uv run --frozen --all-extras --group dev python -m devtools.check_no_embedded_js
    uv run --frozen --all-extras --group dev python -m devtools.check_no_embedded_js --inventory

**The rule has no exceptions.** Browser code lives in `.js` and `.ts` files, where Biome
formats and lints it and `tsc` type-checks it. A Python tool that drives a page loads that
code through the probe loader, `sqpack.probes`, and hands values to it as the one argument
Playwright passes. JavaScript written as a Python string is invisible to every one of those
tools: nothing formats it, nothing parses it until a browser does, and an escape that is
wrong in Python is silently wrong in the page. A TeX `\\le` doubled inside an f-string
reached a published figure exactly that way.

This reads every tracked Python file's syntax tree, not its text, and counts three forms.
Each occurrence is one *site*:

1. **A built script argument.** The script argument of Playwright's `evaluate`,
   `evaluate_handle`, `evaluate_all`, `eval_on_selector`, `eval_on_selector_all`,
   `wait_for_function` or `add_init_script`, positional or keyword, when it is a string
   literal, an f-string, a concatenation, a `%` or `.format` result, a string method
   applied to any of those, or a name bound to one. The accepted argument is a value the
   probe loader returned, or a name bound only to such values. An argument this cannot
   classify -- a parameter, an attribute -- is left to the next two rules, which see the
   string wherever it was written.
2. **A JavaScript string.** Any string whose literal text matches one of the signatures in
   `devtools/embedded-javascript.yaml`: arrow functions, `document.` and `window.`,
   `querySelector` and the like. Pieces of one concatenation or f-string are read as one
   string, so a script split across twenty implicit lines is one site, not twenty.
3. **A script body.** A string in which an opening `<script>` tag is followed by literal
   text. A generator that writes the tag and interpolates a `.js` file's contents after it
   is doing the right thing and passes.

A bare string statement -- a docstring, or the attribute docstrings under a dataclass
field -- is never a site: it is documentation, and it cannot reach a browser.

**The ratchet.** The same YAML file lists each file that still offends, with its site count
and the bead that removes them. The check fails when a file not on the list offends, when a
count grows, when a count shrinks without the list being lowered to match, and when a
listed file no longer offends at all. Failing on an unrecorded shrink is deliberate: a
count left above the real number is headroom a later edit can fill without anything
objecting. `--inventory` prints every site and the list as the scan sees it, which is how
the list was first written.

Files are the repository's tracked and untracked-but-unignored `*.py`, as git lists them.
A source snapshot with no git of its own, which is what the negative controls run in, is
walked instead.
"""

from __future__ import annotations

import argparse
import ast
import os
import re
import subprocess
import sys
from collections import Counter
from collections.abc import Iterator, Sequence
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import Literal

from sqpack.yamlio import safe_load

#: Resolved from this file rather than from an installed package, so a negative control
#: that corrupts a snapshot's copy of the policy is checking the snapshot's copy.
ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
POLICY = ROOT / "devtools" / "embedded-javascript.yaml"

#: Playwright's evaluate family, and where each one takes its script: the positional index
#: and the keyword. `add_init_script(path=...)` names a file, which is the accepted form.
SCRIPT_ARGUMENT: dict[str, tuple[int, str]] = {
    "evaluate": (0, "expression"),
    "evaluate_handle": (0, "expression"),
    "evaluate_all": (0, "expression"),
    "eval_on_selector": (1, "expression"),
    "eval_on_selector_all": (1, "expression"),
    "wait_for_function": (0, "expression"),
    "add_init_script": (0, "script"),
}

#: The modules whose functions return a probe's text. The workbench package's loader is the
#: shared one bound to the package's own probe directory, so both spellings are one loader.
LOADER_MODULES = frozenset({"sqpack.probes", "workbench_tools.probes"})

#: String methods whose result is still built text. A probe passed through one of these is
#: a probe being edited by string formatting, which is the habit the loader exists to end.
STRING_METHODS = frozenset(
    {
        "dedent",
        "format",
        "format_map",
        "indent",
        "join",
        "lstrip",
        "removeprefix",
        "removesuffix",
        "replace",
        "rstrip",
        "strip",
    }
)

#: The node types that can carry string text; everything else is skipped without a match.
TEXT_BEARING = (ast.Constant, ast.JoinedStr, ast.BinOp, ast.Call)

#: The string methods that also exist as `textwrap` functions taking the text first.
DEDENT = frozenset({"dedent", "indent"})

#: Stands in for an interpolated or concatenated value inside a string's literal text.
HOLE = "\x00"

BEAD = re.compile(r"^think-[a-z0-9]{4}$")

#: Directories the snapshot walk skips. Git never lists them: they are environments, build
#: products, scratch, or somebody else's code.
NOT_OURS = frozenset(
    {
        ".git",
        ".venv",
        "__pycache__",
        "attic",
        "node_modules",
        "target",
        "vendor",
    }
)

type Rule = Literal["script argument", "JavaScript string", "script body"]
type Verdict = Literal["loader", "built", "unknown"]


@dataclass(frozen=True)
class Site:
    """One place a Python file holds or passes JavaScript."""

    path: str
    line: int
    rule: Rule
    excerpt: str

    def __str__(self) -> str:
        return f"{self.path}:{self.line}: {self.rule}: {self.excerpt}"


@dataclass(frozen=True)
class Entry:
    """One allowlisted file: how many sites it may still hold, and who removes them."""

    sites: int
    bead: str


@dataclass(frozen=True)
class Policy:
    signatures: tuple[re.Pattern[str], ...]
    script_tag: re.Pattern[str]
    script_code: re.Pattern[str]
    allowlist: dict[str, Entry]

    @property
    def any_signature(self) -> re.Pattern[str]:
        """The signatures as one alternation: one search per string rather than sixteen."""
        return _alternation(self.signatures)


@cache
def _alternation(patterns: tuple[re.Pattern[str], ...]) -> re.Pattern[str]:
    return re.compile("|".join(f"(?:{pattern.pattern})" for pattern in patterns))


class PolicyError(ValueError):
    """The policy file is malformed, which is a failure rather than an empty policy."""


def load_policy(path: Path = POLICY) -> Policy:
    """Read and validate the signatures, the script tag, and the allowlist."""
    document = safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise PolicyError(f"{path}: expected a mapping")
    raw_signatures = document.get("signatures")
    if not isinstance(raw_signatures, list) or not raw_signatures:
        # An empty list would make rule 2 recognise nothing and pass everything.
        raise PolicyError(f"{path}: `signatures` must be a non-empty list")
    signatures = tuple(re.compile(str(pattern)) for pattern in raw_signatures)
    raw_tag, raw_code = document.get("script_tag"), document.get("script_code")
    if not isinstance(raw_tag, str) or not raw_tag:
        raise PolicyError(f"{path}: `script_tag` must be a pattern")
    if not isinstance(raw_code, str) or not raw_code:
        raise PolicyError(f"{path}: `script_code` must be a pattern")
    allowlist: dict[str, Entry] = {}
    for item in document.get("allowlist") or []:
        if not isinstance(item, dict):
            raise PolicyError(f"{path}: allowlist entry is not a mapping: {item!r}")
        file, sites, bead = item.get("path"), item.get("sites"), item.get("bead")
        if not isinstance(file, str) or not file:
            raise PolicyError(f"{path}: allowlist entry without a path: {item!r}")
        if file in allowlist:
            raise PolicyError(f"{path}: {file} is listed twice")
        if not isinstance(sites, int) or isinstance(sites, bool) or sites < 1:
            raise PolicyError(f"{path}: {file}: `sites` must be a positive integer")
        if not isinstance(bead, str) or not BEAD.match(bead):
            raise PolicyError(f"{path}: {file}: `bead` must name a tracking bead")
        allowlist[file] = Entry(sites=sites, bead=bead)
    return Policy(
        signatures=signatures,
        script_tag=re.compile(raw_tag, re.IGNORECASE),
        script_code=re.compile(raw_code),
        allowlist=allowlist,
    )


def repository_files(repo: Path, suffix: str) -> list[str]:
    """Every file under `repo` ending in `suffix`, repository-relative, in a stable order.

    Git's list of tracked and untracked-but-unignored files when `repo` is the top of its
    own work tree, and a walk that skips `NOT_OURS` when it is not. Listed files that have
    been deleted from the working tree are dropped.
    """
    listed = _git_listed(repo, suffix)
    if listed is None:
        listed = _walked(repo, suffix)
    return sorted(path for path in listed if (repo / path).is_file())


def _git_listed(repo: Path, suffix: str) -> list[str] | None:
    """Git's list, or None when `repo` is not the top of its own work tree."""
    try:
        top = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except OSError, subprocess.CalledProcessError:
        return None
    if Path(top).resolve() != repo.resolve():
        # A snapshot inside someone else's checkout would otherwise scan that checkout.
        return None
    done = subprocess.run(
        [
            "git",
            "-C",
            str(repo),
            "ls-files",
            "-z",
            "--cached",
            "--others",
            "--exclude-standard",
            "--",
            f"*{suffix}",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return [path for path in done.stdout.split("\0") if path]


def _walked(repo: Path, suffix: str) -> list[str]:
    found: list[str] = []
    for directory, names, files in os.walk(repo):
        names[:] = [name for name in names if name not in NOT_OURS]
        found.extend(
            (Path(directory) / name).relative_to(repo).as_posix()
            for name in files
            if name.endswith(suffix)
        )
    return found


class _Scanner:
    """The three rules over one parsed module."""

    def __init__(self, path: str, tree: ast.Module, policy: Policy) -> None:
        self.path = path
        self.tree = tree
        self.policy = policy
        self._texts: dict[int, str | None] = {}
        # One walk, shared by every rule: on the free-threaded interpreter this project
        # runs, `ast.walk` is most of the cost, and seven walks per file cost seven times one.
        self.nodes = list(ast.walk(tree))
        self.bindings = _bindings(self.nodes)
        self.loader_functions, self.loader_modules = _loader_names(self.nodes)

    # -- string text -------------------------------------------------------------------

    def text(self, node: ast.AST) -> str | None:
        """The literal text of a string-building expression, or None if it is not one."""
        key = id(node)
        if key not in self._texts:
            self._texts[key] = self._text(node)
        return self._texts[key]

    def _text(self, node: ast.AST) -> str | None:
        if isinstance(node, ast.Constant):
            return node.value if isinstance(node.value, str) else None
        if isinstance(node, ast.JoinedStr):
            return "".join(
                part.value
                if isinstance(part, ast.Constant) and isinstance(part.value, str)
                else HOLE
                for part in node.values
            )
        if isinstance(node, ast.BinOp):
            return self._concatenated(node)
        if isinstance(node, ast.Call):
            return self._method_result(node)
        return None

    def _concatenated(self, node: ast.BinOp) -> str | None:
        """`"..." + x`, `x + "..."` and `"..." % x`; `x % "..."` is arithmetic, not text."""
        if not isinstance(node.op, ast.Add | ast.Mod):
            return None
        left, right = self.text(node.left), self.text(node.right)
        if left is None and (isinstance(node.op, ast.Mod) or right is None):
            return None
        return (HOLE if left is None else left) + (HOLE if right is None else right)

    def _method_result(self, node: ast.Call) -> str | None:
        """A string method applied to text, and `dedent("...")` in either spelling."""
        func, first = node.func, node.args[0] if node.args else None
        if isinstance(func, ast.Attribute) and func.attr in STRING_METHODS:
            receiver = self.text(func.value)
            if receiver is not None:
                return receiver + HOLE
            return self.text(first) if first is not None and func.attr in DEDENT else None
        if isinstance(func, ast.Name) and func.id in DEDENT and first is not None:
            return self.text(first)
        return None

    def consumed(self, node: ast.AST) -> Iterator[ast.AST]:
        """The children whose text `text(node)` already includes."""
        match node:
            case ast.JoinedStr(values=values):
                yield from values
            case ast.BinOp(left=left, right=right):
                yield left
                yield right
            case ast.Call(func=ast.Attribute(value=receiver, attr=attr), args=args):
                if self.text(receiver) is not None:
                    yield receiver
                elif attr in DEDENT and args:
                    yield args[0]
            case ast.Call(func=ast.Name(), args=[first, *_]):
                yield first
            case _:
                return

    # -- rule 1 ------------------------------------------------------------------------

    def classify(self, node: ast.AST, seen: frozenset[str] = frozenset()) -> Verdict:
        """Whether a script argument is the loader's value, built text, or unknown."""
        if self.text(node) is not None:
            return "built"
        if isinstance(node, ast.Call):
            return self._classify_call(node, seen)
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add | ast.Mod):
            # Concatenating onto a probe is editing it by string formatting: built.
            parts = {self.classify(node.left, seen), self.classify(node.right, seen)}
            return "built" if parts & {"built", "loader"} else "unknown"
        if isinstance(node, ast.IfExp):
            return _merged({self.classify(node.body, seen), self.classify(node.orelse, seen)})
        if isinstance(node, ast.Name) and node.id not in seen:
            values = self.bindings.get(node.id, [])
            return _merged({self.classify(value, seen | {node.id}) for value in values})
        return "unknown"

    def _classify_call(self, node: ast.Call, seen: frozenset[str]) -> Verdict:
        func = node.func
        if isinstance(func, ast.Name) and func.id in self.loader_functions:
            return "loader"
        if isinstance(func, ast.Attribute):
            if _dotted(func.value) in self.loader_modules:
                return "loader"
            if func.attr in STRING_METHODS and self.classify(func.value, seen) != "unknown":
                return "built"
        return "unknown"

    def script_arguments(self) -> Iterator[ast.expr]:
        for node in self.nodes:
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
                continue
            where = SCRIPT_ARGUMENT.get(node.func.attr)
            if where is None:
                continue
            position, keyword = where
            named = [kw.value for kw in node.keywords if kw.arg == keyword]
            if named:
                yield named[0]
                continue
            positional = node.args[: position + 1]
            if len(positional) > position and not any(
                isinstance(arg, ast.Starred) for arg in positional
            ):
                yield positional[position]

    # -- the scan ----------------------------------------------------------------------

    def sites(self) -> list[Site]:
        documentation = {
            id(node.value)
            for node in self.nodes
            if isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        }
        strings = [
            node
            for node in self.nodes
            if isinstance(node, TEXT_BEARING) and self.text(node) is not None
        ]
        inner = {id(child) for node in strings for child in self.consumed(node)}
        found: dict[int, Site] = {}
        for node in strings:
            text = self.text(node)
            if text is None or id(node) in inner or id(node) in documentation:
                continue
            rule = self._string_rule(text)
            if rule is not None:
                found[id(node)] = self._site(node, rule, text)
        for argument in self.script_arguments():
            if id(argument) not in found and self.classify(argument) == "built":
                found[id(argument)] = self._site(
                    argument, "script argument", ast.unparse(argument)
                )
        return sorted(found.values(), key=lambda site: (site.line, site.rule))

    def _string_rule(self, text: str) -> Rule | None:
        for match in self.policy.script_tag.finditer(text):
            rest = text[match.end() :]
            end = rest.lower().find("</script")
            body = rest if end < 0 else rest[:end]
            if self.policy.script_code.search(body.replace(HOLE, " ")):
                return "script body"
        if self.policy.any_signature.search(text):
            return "JavaScript string"
        return None

    def _site(self, node: ast.AST, rule: Rule, text: str) -> Site:
        # The first line that says something: a line that is only an interpolation or
        # punctuation identifies nothing.
        rows = (row.strip() for row in text.replace(HOLE, "{...}").splitlines())
        first = next((row for row in rows if row.strip("{.}; ")), "")
        excerpt = first if len(first) <= 72 else first[:69] + "..."
        return Site(path=self.path, line=getattr(node, "lineno", 0), rule=rule, excerpt=excerpt)


def _merged(verdicts: set[Verdict]) -> Verdict:
    """Built if any alternative is built; the loader's only if every one is."""
    if "built" in verdicts:
        return "built"
    return "loader" if verdicts == {"loader"} else "unknown"


def _dotted(node: ast.AST) -> str:
    match node:
        case ast.Name(id=name):
            return name
        case ast.Attribute(value=value, attr=attr):
            owner = _dotted(value)
            return f"{owner}.{attr}" if owner else ""
        case _:
            return ""


def _bindings(nodes: Sequence[ast.AST]) -> dict[str, list[ast.expr]]:
    """Every value assigned to each plain name, in any scope.

    Scope-blind on purpose: a name bound to built text anywhere in the module makes every
    script argument of that name suspect, which errs toward reporting.
    """
    bound: dict[str, list[ast.expr]] = {}
    for node in nodes:
        match node:
            case ast.Assign(targets=targets, value=value):
                for target in targets:
                    if isinstance(target, ast.Name):
                        bound.setdefault(target.id, []).append(value)
            case ast.AnnAssign(target=ast.Name(id=name), value=ast.expr() as value):
                bound.setdefault(name, []).append(value)
            case ast.AugAssign(target=ast.Name(id=name), value=value):
                bound.setdefault(name, []).append(value)
            case ast.NamedExpr(target=ast.Name(id=name), value=value):
                bound.setdefault(name, []).append(value)
            case _:
                pass
    return bound


def _loader_names(nodes: Sequence[ast.AST]) -> tuple[frozenset[str], frozenset[str]]:
    """The names this module calls the probe loader by: functions, and module aliases."""
    functions: set[str] = set()
    modules: set[str] = set()
    for node in nodes:
        match node:
            case ast.ImportFrom(module=str() as module, names=names, level=0):
                for alias in names:
                    local = alias.asname or alias.name
                    if module in LOADER_MODULES:
                        functions.add(local)
                    elif f"{module}.{alias.name}" in LOADER_MODULES:
                        modules.add(local)
            case ast.Import(names=names):
                for alias in names:
                    if alias.name in LOADER_MODULES:
                        modules.add(alias.asname or alias.name)
            case _:
                pass
    return frozenset(functions), frozenset(modules)


def scan_source(path: str, source: str, policy: Policy) -> list[Site]:
    """The sites in one module's source. Raises `SyntaxError` if it does not parse."""
    tree = ast.parse(source, filename=path)
    return _Scanner(path, tree, policy).sites()


def scan(repo: Path, policy: Policy) -> tuple[dict[str, list[Site]], list[str], int]:
    """Sites by file, files that do not parse, and how many files were read."""
    files = repository_files(repo, ".py")

    def one(path: str) -> list[Site] | str:
        try:
            return scan_source(path, (repo / path).read_text(encoding="utf-8"), policy)
        except (SyntaxError, UnicodeDecodeError, ValueError) as error:
            return f"{path}: cannot be read as Python: {error}"

    # Threads rather than processes: the project interpreter is free-threaded, so parsing
    # runs in parallel without paying to pickle a syntax tree back across a process.
    with ThreadPoolExecutor(max_workers=min(8, os.cpu_count() or 1)) as pool:
        results = list(pool.map(one, files))
    by_file: dict[str, list[Site]] = {}
    unreadable: list[str] = []
    for path, result in zip(files, results, strict=True):
        if isinstance(result, str):
            unreadable.append(result)
        elif result:
            by_file[path] = result
    return by_file, unreadable, len(files)


def ratchet(by_file: dict[str, list[Site]], allowlist: dict[str, Entry]) -> list[str]:
    """Every way the scan and the allowlist disagree."""
    faults: list[str] = []
    for path, sites in sorted(by_file.items()):
        count = len(sites)
        entry = allowlist.get(path)
        if entry is None:
            faults.append(
                f"{path}: {count} site(s) of JavaScript in Python, and the file is not on "
                "the allowlist. Move the code into a probe file (see sqpack.probes):"
            )
            faults.extend(f"    {site}" for site in sites)
        elif count > entry.sites:
            faults.append(
                f"{path}: {count} site(s), the allowlist records {entry.sites} "
                f"({entry.bead}). The count may only shrink; move the new code into a "
                "probe file. Every site in the file:"
            )
            faults.extend(f"    {site}" for site in sites)
        elif count < entry.sites:
            faults.append(
                f"{path}: {count} site(s), the allowlist records {entry.sites} "
                f"({entry.bead}). Lower the entry to {count} so the ratchet holds."
            )
    faults.extend(
        f"{path}: no JavaScript left, the allowlist still records {entry.sites} "
        f"({entry.bead}). Remove the entry."
        for path, entry in sorted(allowlist.items())
        if path not in by_file
    )
    return faults


def inventory(by_file: dict[str, list[Site]], allowlist: dict[str, Entry]) -> str:
    """Every site, then the allowlist the scan implies, ready to compare or paste."""
    lines: list[str] = []
    for sites in by_file.values():
        lines.extend(str(site) for site in sites)
    rules: Counter[Rule] = Counter(site.rule for sites in by_file.values() for site in sites)
    total = sum(rules.values())
    lines.append("")
    lines.append(
        f"# {total} site(s) in {len(by_file)} file(s): "
        + ", ".join(f"{count} {rule}" for rule, count in sorted(rules.items()))
    )
    lines.append("allowlist:")
    for path, sites in sorted(by_file.items()):
        entry = allowlist.get(path)
        lines.append(f"  - path: {path}")
        lines.append(f"    sites: {len(sites)}")
        lines.append(f"    bead: {entry.bead if entry else 'think-????'}")
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else "")
    parser.add_argument(
        "--inventory",
        action="store_true",
        help="print every site and the allowlist the scan implies, and exit 0",
    )
    parser.add_argument("--repo", type=Path, default=REPO, help=argparse.SUPPRESS)
    parser.add_argument("--policy", type=Path, default=POLICY, help=argparse.SUPPRESS)
    arguments = parser.parse_args(argv)

    try:
        policy = load_policy(arguments.policy)
    except PolicyError as error:
        print(f"FAIL  {error}")
        return 1
    by_file, unreadable, read = scan(arguments.repo, policy)

    if arguments.inventory:
        print(inventory(by_file, policy.allowlist))
        return 0

    faults = [*unreadable, *ratchet(by_file, policy.allowlist)]
    if read == 0:
        # The correct output is non-empty by construction: this file is Python.
        faults.append(f"no Python files found under {arguments.repo}; the scan read nothing")
    for fault in faults:
        print(fault if fault.startswith("    ") else f"FAIL  {fault}")
    remaining = sum(len(sites) for sites in by_file.values())
    if faults:
        # Site listings under a fault are indented and are not faults of their own.
        count = sum(not fault.startswith("    ") for fault in faults)
        print(f"\n{count} fault(s); {read} Python files read")
        return 1
    print(
        f"OK: {read} Python files read; {remaining} allowlisted site(s) of JavaScript in "
        f"{len(by_file)} file(s) remain, each tracked, and none was added"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
