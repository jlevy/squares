#!/usr/bin/env python3
"""No JavaScript in Python strings: the guard and its enforced empty exception set.

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
   `wait_for_function`, `add_init_script` or `add_script_tag`, positional or keyword, when
   it is a string literal, an f-string, a concatenation, a `%` or `.format` result, a
   string method applied to any of those, or a name bound to one. Bytes count: `b"..."`
   is the same script one `.decode()` later. **The rule is default-deny.** Two pass: a
   value the probe loader returned, or a name bound only to such values; and a name this
   module never binds, which is a parameter or an import
   whose text is written in the module that binds it, where rule 2 reads it. Everything
   else is a site, including the arguments nothing here can read -- a subscript, an
   attribute, `open().read()`, a `*args` unpacking -- because leaving them to the next two
   rules only ever worked for a string carrying a signature. `add_init_script(path=...)`
   and `add_script_tag(path=...)` name a file, which is the accepted form while the file is
   one Biome and `tsc` see: a `.js` or `.ts` path, not a `.txt`.
2. **A JavaScript string.** Any string whose literal text matches one of the signatures in
   `devtools/embedded-javascript.yaml`: arrow functions, `document.` and `window.`,
   `querySelector` and the like. Pieces of one concatenation or f-string are read as one
   string, so a script split across twenty implicit lines is one site, not twenty.
3. **A script body.** A string in which an opening `<script>` tag is followed by literal
   text. A generator that writes the tag and interpolates a `.js` file's contents after it
   is doing the right thing and passes.

A bare string statement -- a docstring, or the attribute docstrings under a dataclass
field -- is never a site: it is documentation, and it cannot reach a browser.

**The exception check.** The YAML's enforced exception set is empty, so any site fails.
The ratchet machinery remains because older revisions had recorded exceptions and
`--since REF` must still prove that a branch did not reintroduce one or raise a historical
count. `--inventory` prints every detected site.

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

#: Playwright's evaluate family, and where each one takes its script: the positional index,
#: or None when the method takes it by keyword only, and the keyword.
SCRIPT_ARGUMENT: dict[str, tuple[int | None, str]] = {
    "evaluate": (0, "expression"),
    "evaluate_handle": (0, "expression"),
    "evaluate_all": (0, "expression"),
    "eval_on_selector": (1, "expression"),
    "eval_on_selector_all": (1, "expression"),
    "wait_for_function": (0, "expression"),
    "add_init_script": (0, "script"),
    # `content=` is a script the page runs exactly as `evaluate` would (#175 R5).
    "add_script_tag": (None, "content"),
}

#: The methods that take a script as a *file*, which is the accepted form -- but only while
#: the file is one Biome formats and `tsc` types. A `.txt` holding JavaScript satisfied the
#: guard and defeated the invariant behind it, which is the most plausible-looking bypass a
#: real diff could carry: the script got long, so it moved to a data file.
PATH_ARGUMENT = frozenset({"add_init_script", "add_script_tag"})

#: What a `path=` argument may name. Everything else is a script the tools cannot see.
SCRIPT_SUFFIXES = (".js", ".mjs", ".cjs", ".ts", ".mts", ".cts")

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
type Verdict = Literal["loader", "opaque", "built", "unknown"]

#: The verdicts a script argument may have. Rule 1 is default-deny: everything else is a
#: site, including the arguments the analysis simply cannot read (#175 R3).
ACCEPTED: frozenset[Verdict] = frozenset({"loader", "opaque"})


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
    return parse_policy(path.read_text(encoding="utf-8"), str(path))


def parse_policy(text: str, path: str) -> Policy:
    """The policy in `text`, named by `path` in every message it can raise."""
    document = safe_load(text)
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


def base_allowlist(repo: Path, policy: Path, ref: str) -> dict[str, Entry] | None:
    """The allowlist as of `ref`, or None when that revision has no policy file.

    None is not a failure: before this file was first committed there was no list to
    compare against, and a comparison against a base that predates the guard would call
    every entry new.
    """
    try:
        relative = policy.resolve().relative_to(repo.resolve()).as_posix()
    except ValueError:
        return None
    shown = subprocess.run(
        ["git", "-C", str(repo), "show", f"{ref}:{relative}"],
        check=False,
        capture_output=True,
        text=True,
    )
    if shown.returncode != 0:
        return None
    return parse_policy(shown.stdout, f"{ref}:{relative}").allowlist


def allowlist_growth(current: dict[str, Entry], base: dict[str, Entry]) -> list[str]:
    """Every way the allowlist is wider than the base's.

    The ratchet in `ratchet` holds each entry against the code; this holds the list itself
    against where it came from. Without it the YAML's "Entries only ever leave" was a
    comment rather than a check, and a new file holding JavaScript passed the gate as soon
    as it brought its own stanza (#175 R2).
    """
    faults: list[str] = []
    for path, entry in sorted(current.items()):
        was = base.get(path)
        if was is None:
            faults.append(
                f"{path}: a new allowlist entry ({entry.sites} site(s), {entry.bead}). The "
                "list only ever shrinks; move the code into a probe file (see sqpack.probes)."
            )
        elif entry.sites > was.sites:
            faults.append(
                f"{path}: the allowlist records {entry.sites} site(s), {was.sites} at the "
                "base. An entry's count only ever falls."
            )
    return faults


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
        #: The names `text` is resolving, so a self-referential binding terminates.
        self._resolving: set[str] = set()
        # One walk, shared by every rule: on the free-threaded interpreter this project
        # runs, `ast.walk` is most of the cost, and seven walks per file cost seven times one.
        self.nodes = list(ast.walk(tree))
        self.bindings = _bindings(self.nodes)
        self.returns = _returns(self.nodes)
        (
            self.loader_functions,
            self.wrapper_functions,
            self.loader_modules,
        ) = _loader_names(self.nodes)

    # -- string text -------------------------------------------------------------------

    def text(self, node: ast.AST) -> str | None:
        """The literal text of a string-building expression, or None if it is not one."""
        if self._resolving:
            # A value read while a name is being resolved is read under a guard that can
            # suppress part of it, so it is not the answer to cache for everyone else.
            return self._text(node)
        key = id(node)
        if key not in self._texts:
            self._texts[key] = self._text(node)
        return self._texts[key]

    def _text(self, node: ast.AST) -> str | None:
        if isinstance(node, ast.Constant):
            return _constant_text(node.value)
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
        if isinstance(node, ast.Name):
            return self._name_text(node.id)
        return None

    def _name_text(self, name: str) -> str | None:
        """The text a name holds, when every value bound to it is text.

        Rule 3 replaced a name in a script body with a space, so a body spliced from a
        bound literal -- `"<script>" + code + "</script>"` -- had no code in it (#175 R7).
        The generator case the rule protects has a call or a parameter in the hole, which
        still resolves to nothing. Bindings that disagree resolve to a hole rather than to
        one of them: the value is text, and which text is not knowable here.
        """
        values = self.bindings.get(name)
        if not values or name in self._resolving:
            return None
        self._resolving.add(name)
        try:
            texts = [self.text(value) for value in values]
        finally:
            self._resolving.discard(name)
        if any(text is None for text in texts):
            return None
        return texts[0] if len(set(texts)) == 1 else HOLE

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
        """What a script argument is, of the four things it can be.

        **Default-deny**: only `loader` and `opaque` pass. `opaque` is the argument this
        cannot read *and* whose text is written elsewhere -- a parameter, or a name this
        module never binds, whose value some other module writes where rule 2 reads it.
        Everything else is a site, because the docstring's old promise that an argument
        rule 1 could not classify was "left to the next two rules" only held for strings
        carrying a signature: `Path(...).read_text()`, `open().read()`, a subscript, a
        parameter default and a `*args` unpacking all passed with a script that has
        none (#175 R3), and nothing counted or printed them (lane L6).
        """
        if self.text(node) is not None:
            return "built"
        match node:
            case ast.Call():
                verdict = self._classify_call(node, seen)
            case ast.BinOp(op=ast.Add() | ast.Mod()):
                # Concatenating or interpolating is building, whatever the pieces are.
                verdict = "built"
            case ast.BinOp(left=left, right=right):
                # `"ab" * 3` is text; `[zero] * arity` is a vector.
                sides = {self.classify(left, seen), self.classify(right, seen)}
                verdict = "built" if "built" in sides else "opaque"
            case ast.IfExp(body=body, orelse=orelse):
                verdict = _merged({self.classify(body, seen), self.classify(orelse, seen)})
            case ast.BoolOp(values=values):
                # `a or b` and `a and b` return an operand, not a Boolean. A file-backed
                # probe combined with built text can therefore still hand that text to
                # Playwright; merge every possible value just as for a conditional.
                verdict = _merged({self.classify(value, seen) for value in values})
            case ast.Name(id=name):
                verdict = self._classify_name(name, seen)
            case ast.Lambda():
                # A callable handed directly to Playwright is executable source, and a
                # called lambda is handled from `_classify_call` below.
                verdict = "unknown"
            case ast.Subscript() | ast.Attribute() | ast.Starred() | ast.Await():
                # A value this declines to follow, and every one of them can hold text:
                # `S["a"]`, `self.SCRIPT`, `*args`, `await build()` (#175 R3).
                verdict = "unknown"
            case (
                ast.Constant()
                | ast.Tuple()
                | ast.List()
                | ast.Dict()
                | ast.Set()
                | ast.ListComp()
                | ast.SetComp()
                | ast.DictComp()
                | ast.GeneratorExp()
                | ast.Compare()
                | ast.UnaryOp()
            ):
                # Not text, so not a script: a number, a container, a predicate. Any string
                # constant has already been answered by `text` above.
                verdict = "opaque"
            case _:
                verdict = "unknown"
        return verdict

    def _classify_name(self, name: str, seen: frozenset[str]) -> Verdict:
        """A name's verdict: its bindings merged, or accepted when this module binds none."""
        if name in seen:
            return "unknown"
        values = self.bindings.get(name)
        if values is None:
            return "opaque"
        return _merged({self.classify(value, seen | {name}) for value in values})

    def _classify_call(self, node: ast.Call, seen: frozenset[str]) -> Verdict:
        func = node.func
        match func:
            case ast.Lambda(body=body):
                # Unlike an imported callable, this function's return expression is
                # visible here. Treat it by the same default-deny rules as a named local
                # helper rather than accepting it as an opaque external call.
                verdict = self.classify(body, seen)
            case ast.Name(id=name) if name in self.loader_functions:
                verdict: Verdict = "loader"
            case ast.Name(id=name) if name in self.wrapper_functions:
                verdict = self._classify_wrapper(node, seen)
            case ast.Attribute(value=receiver, attr="probe") if (
                _dotted(receiver) in self.loader_modules
            ):
                verdict = "loader"
            case ast.Attribute(value=receiver, attr="applied") if (
                _dotted(receiver) in self.loader_modules
            ):
                verdict = self._classify_wrapper(node, seen)
            case ast.Attribute(value=receiver) if self.classify(receiver, seen) in {
                "built",
                "loader",
            }:
                # A method on text or on a probe is that value being edited, whatever the
                # method is named: `.decode()` and `.lower()` are no different from
                # `.replace()`, and the allowlist of method names is what let a bytes
                # constant through (#175 R1).
                verdict = "built"
            case ast.Name(id=name) if name in self.returns:
                # A helper in this module is not opaque: its returns are available here.
                # Accept it only when every value it can return is loader-backed. A literal
                # was the original bypass (L6), but treating only literal returns as local
                # let `return Path(...).read_text()` recreate the same hole one call away.
                returned = (
                    {self.classify(value, seen | {name}) for value in self.returns[name]}
                    if name not in seen
                    else {"unknown"}
                )
                verdict = "loader" if returned == {"loader"} else "built"
            case _ if any(self.text(argument) is not None for argument in node.args):
                # A call handed text and returning a script is building one: `str(b"...")`,
                # `b64decode("...")`, `dedent(...)` under any alias.
                verdict = "built"
            case _:
                # A call to something written in another module. Rule 2 reads its text where
                # that module writes it, which is also why `polynomial.evaluate(origin)` is
                # not reported: `evaluate` is a name mathematics uses too, and calling a
                # value nothing here can read a script would be a guess.
                verdict = "opaque"
        return verdict

    def _classify_wrapper(self, node: ast.Call, seen: frozenset[str]) -> Verdict:
        """Accept `applied` only when its source came from the probe loader."""
        named = [keyword.value for keyword in node.keywords if keyword.arg == "source"]
        if node.args and not isinstance(node.args[0], ast.Starred) and not named:
            source = node.args[0]
        elif not node.args and len(named) == 1:
            source = named[0]
        else:
            return "built"
        return "loader" if self.classify(source, seen) == "loader" else "built"

    def _names_a_script_file(self, node: ast.expr, seen: frozenset[str] = frozenset()) -> bool:
        """Whether the *effective* `path=` expression names checked browser source.

        This is deliberately an outer-expression analysis, not an AST walk: in
        `Path("decoy.js").with_suffix(".txt")`, the descendant `.js` literal is not the
        suffix Playwright opens. Unknown transformations fail closed.
        """
        text = self.text(node)
        if text is not None:
            accepted = text.endswith(SCRIPT_SUFFIXES)
        else:
            match node:
                case ast.Name(id=name) if name not in seen:
                    values = self.bindings.get(name, [])
                    accepted = bool(values) and all(
                        self._names_a_script_file(value, seen | {name}) for value in values
                    )
                case ast.BinOp(op=ast.Div() | ast.Add(), right=right):
                    # For pathlib joins and string concatenation, the final component owns
                    # the suffix. `text` above already handled a fully readable string.
                    accepted = self._names_a_script_file(right, seen)
                case ast.IfExp(body=body, orelse=orelse):
                    accepted = self._names_a_script_file(
                        body, seen
                    ) and self._names_a_script_file(orelse, seen)
                case ast.BoolOp(values=values):
                    accepted = bool(values) and all(
                        self._names_a_script_file(value, seen) for value in values
                    )
                case ast.Call(func=ast.Name(id=name), args=[first, *_]) if name in {
                    "Path",
                    "PurePath",
                    "str",
                }:
                    accepted = self._names_a_script_file(first, seen)
                case ast.Call(
                    func=ast.Attribute(attr="with_suffix"),
                    args=[suffix, *_],
                ):
                    accepted = self._names_a_script_file(suffix, seen)
                case ast.Call(
                    func=ast.Attribute(attr="with_name"),
                    args=[name, *_],
                ):
                    accepted = self._names_a_script_file(name, seen)
                case ast.Call(
                    func=ast.Attribute(attr="joinpath"),
                    args=[*_, last],
                ):
                    accepted = self._names_a_script_file(last, seen)
                case ast.Call(
                    func=ast.Attribute(value=value, attr="resolve" | "absolute" | "expanduser"),
                    args=[],
                ):
                    accepted = self._names_a_script_file(value, seen)
                case _:
                    accepted = False
        return accepted

    def refused_arguments(self) -> Iterator[ast.expr]:
        """The arguments refused without being classified, because there is nothing to read.

        A `path=` that does not name a file the JavaScript floor can see (lane L3), and a
        script handed over inside a `*args` or `**kwargs` unpacking (#175 R3).
        """
        for node in self.nodes:
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
                continue
            attribute = node.func.attr
            if attribute in PATH_ARGUMENT:
                for keyword in node.keywords:
                    if keyword.arg == "path" and not self._names_a_script_file(keyword.value):
                        yield keyword.value
            where = SCRIPT_ARGUMENT.get(attribute)
            if where is None:
                continue
            position, keyword_name = where
            if any(kw.arg == keyword_name for kw in node.keywords):
                continue
            reached = position is not None and len(node.args) > position
            if reached and not any(
                isinstance(arg, ast.Starred) for arg in node.args[: (position or 0) + 1]
            ):
                continue
            yield from (arg for arg in node.args if isinstance(arg, ast.Starred))
            yield from (kw.value for kw in node.keywords if kw.arg is None)

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
            if position is not None:
                positional = node.args[: position + 1]
                if len(positional) > position and not any(
                    isinstance(arg, ast.Starred) for arg in positional
                ):
                    yield positional[position]
                    continue

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
            if id(argument) not in found and self.classify(argument) not in ACCEPTED:
                found[id(argument)] = self._site(
                    argument, "script argument", ast.unparse(argument)
                )
        for argument in self.refused_arguments():
            if id(argument) not in found:
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
            # A combined match can consume a second signature inside a Lean arrow's
            # parameter span. Check each signature independently after the fast precheck.
            for signature in self.policy.signatures:
                for match in signature.finditer(text):
                    if not _lean_arrow(text, match):
                        return "JavaScript string"
        return None

    def _site(self, node: ast.AST, rule: Rule, text: str) -> Site:
        # The first line that says something: a line that is only an interpolation or
        # punctuation identifies nothing.
        rows = (row.strip() for row in text.replace(HOLE, "{...}").splitlines())
        first = next((row for row in rows if row.strip("{.}; ")), "")
        excerpt = first if len(first) <= 72 else first[:69] + "..."
        return Site(path=self.path, line=getattr(node, "lineno", 0), rule=rule, excerpt=excerpt)


def _lean_arrow(text: str, match: re.Match[str]) -> bool:
    """Recognize local Lean lambda/Option-arm syntax, without exempting its string.

    Lean's ``fun x`` lambda and ``match x with | none`` / ``| some (...)`` arms
    share the arrow spelling with JavaScript. Other signatures, arrows in their
    bodies, and every built browser-script argument still fail independently.
    """
    matched = match.group()
    if not matched.endswith("=>"):
        return False
    parameter = matched[:-2].strip()
    identifier = r"[A-Za-z_][A-Za-z0-9_]*"
    prefix = text[: match.start()]
    if re.fullmatch(identifier, parameter) and re.search(r"\bfun[ \t]+$", prefix):
        return True
    line = prefix.rsplit("\n", 1)[-1]
    if not re.search(r"\bmatch\s+[A-Za-z_][A-Za-z0-9_]*\s+with\b", line):
        return False
    tuple_pattern = rf"\(\s*{identifier}(?:\s*,\s*{identifier})*\s*\)"
    return bool(
        (parameter == "none" and re.search(r"\|\s*$", line))
        or (re.fullmatch(tuple_pattern, parameter) and re.search(r"\|\s*some\s*$", line))
    )


def _constant_text(value: object) -> str | None:
    """A constant's text. A bytes constant is the same script one `.decode()` later, and
    rule 2 never read one: `page.evaluate(b"() => document.title".decode())` passed both
    rules while the `str` spelling was reported (#175 R1)."""
    if isinstance(value, str):
        return value
    return value.decode("utf-8", "replace") if isinstance(value, bytes) else None


def _merged(verdicts: set[Verdict]) -> Verdict:
    """Built if any alternative is built; accepted only if every one is."""
    if "built" in verdicts:
        return "built"
    if not verdicts or "unknown" in verdicts:
        return "unknown"
    return "loader" if verdicts == {"loader"} else "opaque"


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
    """Every value bound to each plain name, in any scope.

    Scope-blind on purpose: a name bound to built text anywhere in the module makes every
    script argument of that name suspect, which errs toward reporting.

    Tuple and list targets are unpacked element by element when the value is a matching
    literal, so `a, b = "docu", "ment.title"` binds both halves rather than neither
    (#175 R3). A parameter's default is a binding too: a name with no binding is the one
    thing rule 1 accepts without reading it, and `def run(page, script="...")` wrote the
    script into the signature.
    """
    bound: dict[str, list[ast.expr]] = {}
    for node in nodes:
        match node:
            case ast.Assign(targets=targets, value=value):
                for target in targets:
                    _bind(bound, target, value)
            case ast.AnnAssign(target=ast.Name(id=name), value=ast.expr() as value):
                bound.setdefault(name, []).append(value)
            case ast.AugAssign(target=ast.Name(id=name), value=value):
                bound.setdefault(name, []).append(value)
            case ast.NamedExpr(target=ast.Name(id=name), value=value):
                bound.setdefault(name, []).append(value)
            case (
                ast.FunctionDef(args=arguments)
                | ast.AsyncFunctionDef(args=arguments)
                | ast.Lambda(args=arguments)
            ):
                positional = [*arguments.posonlyargs, *arguments.args]
                defaults = arguments.defaults
                for parameter, default in zip(
                    positional[len(positional) - len(defaults) :], defaults, strict=True
                ):
                    bound.setdefault(parameter.arg, []).append(default)
                for parameter, default in zip(
                    arguments.kwonlyargs, arguments.kw_defaults, strict=True
                ):
                    if default is not None:
                        bound.setdefault(parameter.arg, []).append(default)
            case _:
                pass
    return bound


def _bind(bound: dict[str, list[ast.expr]], target: ast.expr, value: ast.expr) -> None:
    """Record `target = value`, unpacking a tuple or list target against a matching value."""
    match target:
        case ast.Name(id=name):
            bound.setdefault(name, []).append(value)
        case ast.Tuple(elts=elements) | ast.List(elts=elements):
            pieces = value.elts if isinstance(value, ast.Tuple | ast.List) else []
            paired = pieces if len(pieces) == len(elements) else None
            for index, element in enumerate(elements):
                _bind(bound, element, paired[index] if paired is not None else value)
        case ast.Starred(value=inner):
            _bind(bound, inner, value)
        case _:
            # An attribute or a subscript target. Rule 1 denies an attribute or a subscript
            # argument outright, so binding one by its bare name would only collide with
            # the plain names it shares.
            pass


def _returns(nodes: Sequence[ast.AST]) -> dict[str, list[ast.expr]]:
    """Every expression each function in this module returns, by the function's name."""
    returned: dict[str, list[ast.expr]] = {}
    for node in nodes:
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            continue
        returned.setdefault(node.name, []).extend(
            inner.value
            for inner in ast.walk(node)
            if isinstance(inner, ast.Return) and inner.value is not None
        )
    return returned


def _loader_names(
    nodes: Sequence[ast.AST],
) -> tuple[frozenset[str], frozenset[str], frozenset[str]]:
    """The local names of `probe`, `applied`, and their module aliases."""
    loaders: set[str] = set()
    wrappers: set[str] = set()
    modules: set[str] = set()
    for node in nodes:
        match node:
            case ast.ImportFrom(module=str() as module, names=names, level=0):
                for alias in names:
                    local = alias.asname or alias.name
                    if module in LOADER_MODULES:
                        if alias.name == "probe":
                            loaders.add(local)
                        elif alias.name == "applied":
                            wrappers.add(local)
                    elif f"{module}.{alias.name}" in LOADER_MODULES:
                        modules.add(local)
            case ast.Import(names=names):
                for alias in names:
                    if alias.name in LOADER_MODULES:
                        modules.add(alias.asname or alias.name)
            case _:
                pass
    return frozenset(loaders), frozenset(wrappers), frozenset(modules)


def scan_source(path: str, source: str, policy: Policy) -> list[Site]:
    """The sites in one module's source. Raises `SyntaxError` if it does not parse."""
    tree = ast.parse(source, filename=path)
    return _Scanner(path, tree, policy).sites()


def scan(repo: Path, policy: Policy) -> tuple[dict[str, list[Site]], list[str], int]:
    """Sites by file, files that do not parse, and how many files were read."""
    files = repository_files(repo, ".py")

    def one(path: str) -> list[Site] | str:
        try:
            # utf-8-sig, as CPython reads source: a leading byte-order mark is valid there
            # and appears in retained third-party files, which are never edited.
            return scan_source(path, (repo / path).read_text(encoding="utf-8-sig"), policy)
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
    parser.add_argument(
        "--since",
        metavar="REF",
        help="also refuse an allowlist entry this revision does not have, or a count above "
        "its own; a revision with no policy file is reported and not compared",
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
    notes: list[str] = []
    if arguments.since:
        base = base_allowlist(arguments.repo, arguments.policy, arguments.since)
        if base is None:
            notes.append(
                f"{arguments.since} has no policy file, so the allowlist itself was not "
                "compared; only the counts were held against the code"
            )
        else:
            faults.extend(allowlist_growth(policy.allowlist, base))
    if read == 0:
        # The correct output is non-empty by construction: this file is Python.
        faults.append(f"no Python files found under {arguments.repo}; the scan read nothing")
    for note in notes:
        print(f"NOTE  {note}")
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
