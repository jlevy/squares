"""Count what the statement audit of the Lean proof that s(12) = 4 cites, from its closure.

Queuingtheorydotcom/Jatloe12SquaresFormalized at ``d0caf45`` proves
``N12Compact.Final.optimality : S12.packingConstant12 = 4``, ``T-243``'s claim, in the
5,377 project modules ``devtools.lean_closure`` found under ``Compact.Assembly.Final``,
too many to retain here. The packet ``resources/web/jatloe-n12-lean-2026-10-16`` keeps
that closure receipt (``receipts/lean-closure.json.gz``), the 109 modules the statement's
module imports, the assembly and the source's run evidence
(``verification/run-38849916588/``). The statement audit
(``docs/project/reviews/review-2026-10-25-n12-lean-formalization-statement-audit.md``)
reads the source line by line; this tool makes the counts it cites, over every module the
receipt names and over the statement closure, and writes them as one receipt
(``receipts/statement-audit.json``):

- ``tokens``: each of `devtools.audit_n11_lean.TOKENS` and `EXTRA_TOKENS`, in the code
  (comments, strings and character literals blanked by `audit_n11_lean.strip_code`) and
  in the raw text, with the path and line of every hit in code for a token with at most
  `HIT_LIMIT` of them;
- ``set_option``, each option's name and count, and ``instances``, each ``instance``
  declaration's class, with the place of every one that is not a ``Decidable`` class;
- ``shadowing``: every declaration whose last name is one of `STATEMENT_NAMES`, with the
  namespaces open around it, and every namespace `STATEMENT_NAMESPACES` names nested inside
  another, which is where a name of the statement could resolve to a declaration it does
  not mean;
- ``native``: the declaration that holds each ``native_decide`` call, matched with the
  owners of the ``native_decide`` axioms in the source's final axiom log: how many owners
  there are, whether every owner holds as many calls as it has axioms, and the calls the
  final theorem's axioms do not reach, by module;
- ``manifest`` and ``axiom_log``: each module's bytes against the SHA-256 the run's
  ``verified-source-manifest.json`` states, the log's axioms against the run's
  ``global-native-axiom-audit.json``, and the two files' digests against the ones
  ``SOURCE-PROVENANCE.json`` records.

Every module is read by the Git blob the closure receipt names: from a checkout's object
database, its path checked against the receipt's commit (`scan`), or from the packet's
retained bytes for the statement closure (`check`, which recomputes every part of the
receipt the packet can and compares). It reads no working tree of the checkout and runs
nothing from the source. Declarations are found by matching their headers and the open
namespaces, not by parsing, and a token count is not a parse: a construct spelled in a way
no pattern matches would pass it.

Usage, from ``packing/``::

    uv run --frozen --all-extras --group dev python -m devtools.audit_n12_lean scan CHECKOUT
    uv run --frozen --all-extras --group dev python -m devtools.audit_n12_lean check
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any, NamedTuple, cast

from strif import atomic_write_text

from devtools.audit_n11_lean import TOKENS, strip_code
from devtools.lean_closure import Source
from devtools.retained_data import git_blob, read_retained_bytes
from sqpack import retained_json

REPO = Path(__file__).resolve().parents[2]
PACKET = REPO / "packing/resources/web/jatloe-n12-lean-2026-10-16"
SOURCE = PACKET / "Jatloe12SquaresFormalized"
CLOSURE = PACKET / "receipts/lean-closure.json.gz"
RUN = SOURCE / "verification/run-38849916588"
PROVENANCE = SOURCE / "SOURCE-PROVENANCE.json"
RECEIPT = PACKET / "receipts/statement-audit.json"
KIND = "n12-lean-statement-audit/v1"
#: The module the statement's definitions are complete in: its closure is what has to be
#: elaborated before the theorem's type means anything.
STATEMENT_TARGETS = ("S12.PackingConstant",)
#: The names the theorem's type and the grid use, and the final theorem's own.
STATEMENT_NAMES = (
    "Final",
    "InBands",
    "Inside",
    "OpenSquare",
    "UnitPacking",
    "feasibleSides",
    "four_feasible",
    "gridPacking",
    "optimality",
    "packingConstant12",
)
#: The namespaces the statement's names live in; one nested in another would let
#: ``S12.packingConstant12`` resolve inside ``N12Compact`` to something else.
STATEMENT_NAMESPACES = ("S12", "S12Pilot")
STANDARD_AXIOMS = ("Classical.choice", "Quot.sound", "propext")
NATIVE_MARK = "._native.native_decide.ax_"
#: In-code hits are listed one by one for a token with at most this many.
HIT_LIMIT = 100
#: Patterns the statement audit counts beside the eleven-square audit's `TOKENS`.
EXTRA_TOKENS: Mapping[str, str] = {
    "set_option": r"\bset_option\s+([A-Za-z_.]+)",
    "attribute_cmd": r"(?m)^[ \t]*attribute\s*\[[^\]]*\]",
    "debug_option": r"\bdebug\.[A-Za-z]",
    "axiom_word": r"\baxiom\b",
    "decide_kernel": r"decide\s*\+kernel",
    "noncomputable": r"\bnoncomputable\b",
    "Float": r"\bFloat\b",
    "UInt": r"\bUInt(?:8|16|32|64)\b|\bUSize\b",
    "OfNat": r"\bOfNat\b",
    "reducible": r"@\[[^\]]*\b(?:reducible|irreducible)\b",
    "priority": r"\bpriority\s*:=",
    "Lean_Elab_use": r"\bLean\.(?:Elab|Meta)\b",
    "import_Std": r"(?m)^import[ \t]+Std(?:\.|\s|$)",
}
PATTERNS: Mapping[str, str] = {**TOKENS, **EXTRA_TOKENS}
_COMPILED = {name: re.compile(pattern) for name, pattern in PATTERNS.items()}
_NAME = r"[A-Za-z_][A-Za-z_0-9'!?]*(?:\.[A-Za-z_][A-Za-z_0-9'!?]*)*"
#: A command that opens a declaration whose body can hold a ``native_decide``, or that
#: opens or closes a scope, at the start of a line.
_OWNER = re.compile(
    r"(?m)^(?:@\[[^\]]*\]\s*)?(?:(?:private|protected|noncomputable|nonrec)\s+)*"
    r"(theorem|lemma|def|abbrev|instance|example|namespace|end|section)\b\s*(" + _NAME + r")?"
)
#: Any declaration a name can resolve to, or a scope command, indented or not.
_DECLARATION = re.compile(
    r"(?m)^[ \t]*(?:@\[[^\]]*\]\s*)?"
    r"(?:(?:private|protected|noncomputable|nonrec|partial)\s+)*"
    r"(theorem|lemma|def|abbrev|structure|class|inductive|instance|opaque|axiom|namespace|end"
    r"|section)\b\s*(" + _NAME + r")?"
)
_NATIVE = re.compile(r"\bnative_decide\b")
_OPENERS, _CLOSERS = "([{⟨", ")]}⟩"


class Module(NamedTuple):
    """One project module of the closure: its name, path, text, and its code, the text
    with comments, strings and character literals blanked (`strip_code`)."""

    module: str
    path: str
    text: str
    code: str

    @classmethod
    def of(cls, module: str, path: str, text: str) -> Module:
        return cls(module, path, text, strip_code(text))


def load_closure(path: Path = CLOSURE) -> dict[str, Any]:
    """The closure receipt ``devtools.lean_closure`` wrote, plain or gzip."""
    return cast("dict[str, Any]", json.loads(read_retained_bytes(path)))


def subclosure(closure: Mapping[str, Any], targets: Iterable[str]) -> list[str]:
    """The receipt's modules that ``targets`` import, themselves included, sorted."""
    imports = {m["module"]: m["imports"] for m in closure["modules"]}
    seen: set[str] = set()
    stack = list(targets)
    while stack:
        name = stack.pop()
        if name in seen or name not in imports:
            continue
        seen.add(name)
        stack.extend(imports[name])
    return sorted(seen)


def _cat_blobs(checkout: Path, blobs: Sequence[str]) -> dict[str, bytes]:
    """The bytes of each blob in the checkout's object database, by ``git cat-file``."""
    done = subprocess.run(
        ("git", "-C", str(checkout), "cat-file", "--batch"),
        input="".join(f"{blob}\n" for blob in blobs).encode(),
        capture_output=True,
        check=False,
    )
    if done.returncode:
        raise SystemExit(f"git cat-file --batch: {done.stderr.decode(errors='replace')}")
    out, at, found = done.stdout, 0, {}
    for blob in blobs:
        end = out.index(b"\n", at)
        header = out[at:end].decode().split()
        if header[1:2] != ["blob"]:
            raise SystemExit(f"{blob} is not a blob in {checkout}: {' '.join(header)}")
        size = int(header[2])
        found[blob] = out[end + 1 : end + 1 + size]
        at = end + 2 + size
    return found


def _checked(entry: Mapping[str, Any], data: bytes) -> Module:
    if git_blob(data) != entry["blob"]:
        raise SystemExit(f"{entry['path']}: the bytes read are not blob {entry['blob']}")
    return Module.of(entry["module"], entry["path"], data.decode("utf-8"))


def read_checkout(checkout: Path, closure: Mapping[str, Any]) -> list[Module]:
    """Every module of the receipt, from the checkout's Git objects at its commit."""
    tree = Source(checkout, closure["commit"]).blobs
    entries = closure["modules"]
    for entry in entries:
        if tree.get(entry["path"]) != entry["blob"]:
            raise SystemExit(f"{entry['path']} is not blob {entry['blob']} at the commit")
    data = _cat_blobs(checkout, [entry["blob"] for entry in entries])
    return [_checked(entry, data[entry["blob"]]) for entry in entries]


def read_retained(
    closure: Mapping[str, Any], modules: Iterable[str], source: Path = SOURCE
) -> list[Module]:
    """The named modules of the receipt, from the packet's retained bytes."""
    entries = {m["module"]: m for m in closure["modules"]}
    return [
        _checked(entries[name], read_retained_bytes(source / entries[name]["path"]))
        for name in modules
    ]


def _line(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def instance_class(declaration: str) -> str:
    """The class an ``instance`` header declares: the first word after its last colon
    outside brackets, or ``?``."""
    depth, last = 0, -1
    for index, character in enumerate(declaration):
        if character in _OPENERS:
            depth += 1
        elif character in _CLOSERS:
            depth -= 1
        elif character == ":" and depth == 0:
            last = index
    words = declaration[last + 1 :].split() if last >= 0 else []
    return words[0] if words else "?"


def census(modules: Sequence[Module], sizes: Mapping[str, int]) -> dict[str, Any]:
    """Token, ``set_option`` and instance counts over ``modules``."""
    code_uses: Counter[str] = Counter()
    raw_uses: Counter[str] = Counter()
    files: Counter[str] = Counter()
    hits: dict[str, list[str]] = {name: [] for name in PATTERNS}
    options: Counter[str] = Counter()
    classes: Counter[str] = Counter()
    other_instances: list[str] = []
    libraries: Counter[str] = Counter()
    for module in modules:
        libraries[module.module.split(".")[0]] += 1
        code = module.code
        for name, pattern in _COMPILED.items():
            raw_uses[name] += len(pattern.findall(module.text))
            found = list(pattern.finditer(code))
            if not found:
                continue
            files[name] += 1
            code_uses[name] += len(found)
            hits[name].extend(f"{module.path}:{_line(code, m.start())}" for m in found)
            if name == "set_option":
                options.update(m.group(1) for m in found)
            if name == "instance":
                for match in found:
                    segment = code[match.start() : match.start() + 600]
                    stop = re.search(r":=|\bwhere\b", segment)
                    kind = instance_class(segment[: stop.start()] if stop else segment)
                    classes[kind] += 1
                    if not kind.startswith("Decidable"):
                        place = f"{module.path}:{_line(code, match.start())}"
                        other_instances.append(f"{place}: {kind}")
    return {
        "modules": len(modules),
        "bytes": sum(sizes[module.module] for module in modules),
        "libraries": dict(sorted(libraries.items())),
        "tokens": {
            name: {
                "pattern": PATTERNS[name],
                "occurrences_code": code_uses[name],
                "occurrences_raw": raw_uses[name],
                "files_code": files[name],
                "hits_code": hits[name] if len(hits[name]) <= HIT_LIMIT else "over the limit",
            }
            for name in PATTERNS
        },
        "set_option": dict(sorted(options.items(), key=lambda item: (-item[1], item[0]))),
        "instances": dict(sorted(classes.items(), key=lambda item: (-item[1], item[0]))),
        "instances_not_decidable": other_instances,
    }


def _scoped(modules: Sequence[Module], pattern: re.Pattern[str]) -> Iterable[tuple[Any, ...]]:
    """Each declaration command of ``modules`` with the namespaces open at it, its body's
    end and the module's code: ``(module, code, kind, name, namespaces, start, end)``."""
    for module in modules:
        code = module.code
        scopes: list[list[str]] = []
        marks = list(pattern.finditer(code))
        for index, mark in enumerate(marks):
            kind, name = mark.group(1), mark.group(2) or ""
            if kind == "namespace":
                scopes.append(name.split("."))
                continue
            if kind == "section":
                scopes.append([])
                continue
            if kind == "end":
                if scopes:
                    scopes.pop()
                continue
            end = marks[index + 1].start() if index + 1 < len(marks) else len(code)
            namespaces = [part for scope in scopes for part in scope]
            yield module, code, kind, name, namespaces, mark.start(), end


def shadowing(modules: Sequence[Module]) -> dict[str, Any]:
    """Every declaration of a statement name, and every nested statement namespace."""
    declared: dict[str, list[str]] = {name: [] for name in STATEMENT_NAMES}
    nested: list[str] = []
    for module in modules:
        code = module.code
        scopes: list[str] = []
        for mark in _DECLARATION.finditer(code):
            kind, name = mark.group(1), mark.group(2) or ""
            place = f"{module.path}:{_line(code, mark.start())}"
            if kind == "namespace":
                scopes.append(name)
                parts = [part for scope in scopes if scope for part in scope.split(".")]
                if any(space in parts[1:] for space in STATEMENT_NAMESPACES):
                    nested.append(f"{place}: {'.'.join(scopes)}")
                continue
            if kind == "section":
                scopes.append("")
                continue
            if kind == "end":
                if scopes:
                    scopes.pop()
                continue
            last = name.split(".")[-1]
            if last in declared:
                qualified = ".".join([scope for scope in scopes if scope] + [name])
                declared[last].append(f"{kind} {qualified} {place}")
    return {"declarations": declared, "nested_namespaces": nested}


def log_axioms(log: str) -> list[str]:
    """The axioms a ``#print axioms`` log lists after ``depends on axioms:``."""
    return re.findall(r"[\w.']+", log.split("depends on axioms:", 1)[1])


def _owner(axiom: str) -> str:
    return axiom.split(NATIVE_MARK, maxsplit=1)[0]


def _family(name: str) -> str:
    return re.sub(r"\d+", "#", name)


def native_sites(modules: Sequence[Module], axioms: Sequence[str]) -> dict[str, Any]:
    """Each ``native_decide`` call's declaration, against the final theorem's axioms."""
    owners = Counter(_owner(axiom) for axiom in axioms if NATIVE_MARK in axiom)
    sites: dict[str, tuple[str, int, str]] = {}
    anonymous: list[str] = []
    for module, code, kind, name, namespaces, start, end in _scoped(modules, _OWNER):
        calls = len(_NATIVE.findall(code, start, end))
        if not calls:
            continue
        if kind == "example" or not name:
            anonymous.append(f"{module.path}:{_line(code, start)}: {calls}")
            continue
        sites[".".join([*namespaces, name])] = (module.path, calls, kind)
    on = {name: site for name, site in sites.items() if name in owners}
    off = {name: site for name, site in sites.items() if name not in owners}

    def by_module(chosen: Mapping[str, tuple[str, int, str]]) -> dict[str, Any]:
        rows: dict[str, dict[str, Any]] = {}
        for name, (path, calls, _) in sorted(chosen.items()):
            row = rows.setdefault(path, {"declarations": 0, "calls": 0, "names": []})
            row["declarations"] += 1
            row["calls"] += calls
            row["names"].append(name)
        for row in rows.values():
            if row["declarations"] > 10:
                del row["names"]
        return dict(sorted(rows.items()))

    def families(chosen: Mapping[str, tuple[str, int, str]]) -> dict[str, list[int]]:
        found: dict[str, list[int]] = {}
        for name, (_, calls, _) in chosen.items():
            row = found.setdefault(_family(name), [0, 0])
            row[0] += 1
            row[1] += calls
        return dict(sorted(found.items()))

    modules_with = {path for path, _, _ in sites.values()}
    return {
        "calls": sum(calls for _, calls, _ in sites.values()),
        "modules": len(modules_with),
        "libraries": dict(
            sorted(
                Counter(
                    module.module.split(".")[0]
                    for module in modules
                    if module.path in modules_with
                ).items()
            )
        ),
        "declarations": len(sites),
        "declarations_by_kind": dict(sorted(Counter(k for _, _, k in sites.values()).items())),
        "anonymous": anonymous,
        "axioms": len(axioms),
        "standard_axioms": sorted(a for a in axioms if NATIVE_MARK not in a),
        "native_axioms": sum(owners.values()),
        "native_owners": len(owners),
        "owners_without_a_site": sorted(owner for owner in owners if owner not in sites),
        "owners_whose_axioms_are_not_their_calls": sorted(
            f"{name}: {owners[name]} axioms, {calls} calls"
            for name, (_, calls, _) in on.items()
            if owners[name] != calls
        ),
        "on_path": {
            "declarations": len(on),
            "calls": sum(calls for _, calls, _ in on.values()),
            "by_module": by_module(on),
            "families": families(on),
        },
        "off_path": {
            "declarations": len(off),
            "calls": sum(calls for _, calls, _ in off.values()),
            "by_module": by_module(off),
            "families": families(off),
        },
    }


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run_evidence(
    modules: Sequence[Module], closure: Mapping[str, Any], run: Path, provenance: Path
) -> dict[str, Any]:
    """The run's manifest against the modules read, and its axiom log against its
    native-axiom audit and the source's provenance record."""
    manifest_bytes = read_retained_bytes(run / "verified-source-manifest.json")
    log_bytes = read_retained_bytes(run / "global-type-axiom-audit.log")
    native_bytes = read_retained_bytes(run / "global-native-axiom-audit.json")
    record = json.loads(provenance.read_bytes())
    manifest = json.loads(manifest_bytes)
    listed = {m["module"]: m for m in manifest["modules"]}
    receipt = {m["module"]: m for m in closure["modules"]}
    read = {module.module: module for module in modules}
    axioms = log_axioms(log_bytes.decode("utf-8"))
    final = json.loads(native_bytes)["final_axioms"]
    return {
        "manifest": {
            "modules": len(listed),
            "same_modules_as_closure": set(listed) == set(receipt),
            "same_paths_as_closure": all(
                receipt[name]["path"] == entry["path"]
                for name, entry in listed.items()
                if name in receipt
            ),
            "modules_compared": sum(1 for name in listed if name in read),
            "sha256_mismatches": sorted(
                name
                for name, entry in listed.items()
                if name in read and _sha256(read[name].text.encode("utf-8")) != entry["sha256"]
            ),
            "source_commit": manifest["source_commit"],
            "root_module": manifest["root_module"],
            "sha256": _sha256(manifest_bytes),
            "provenance_sha256": record["source_manifest_sha256"],
        },
        "axiom_log": {
            "axioms": len(axioms),
            "distinct": len(set(axioms)),
            "sorryAx": "sorryAx" in axioms,
            "standard_axioms": sorted(a for a in axioms if NATIVE_MARK not in a),
            "native_axioms": sum(1 for a in axioms if NATIVE_MARK in a),
            "equals_native_audit_final_axioms": sorted(axioms) == sorted(final),
            "sha256": _sha256(log_bytes),
            "provenance_sha256": record["final_audit_log_sha256"],
        },
    }


def _path(path: Path) -> str:
    """``path`` repository-relative, or as given when it lies outside the repository."""
    resolved = path.resolve()
    return resolved.relative_to(REPO).as_posix() if resolved.is_relative_to(REPO) else str(path)


def audit(
    modules: Sequence[Module],
    closure: Mapping[str, Any],
    *,
    closure_path: Path = CLOSURE,
    run: Path = RUN,
    provenance: Path = PROVENANCE,
    statement_targets: Sequence[str] = STATEMENT_TARGETS,
) -> dict[str, Any]:
    """The receipt: every count over ``modules`` and over their statement closure."""
    sizes = {m["module"]: m["bytes"] for m in closure["modules"]}
    statement_names = set(subclosure(closure, statement_targets))
    statement = [module for module in modules if module.module in statement_names]
    if len(statement) != len(statement_names):
        raise SystemExit("the modules read do not hold the statement closure")
    whole = len(modules) == len(closure["modules"])
    axioms = log_axioms(read_retained_bytes(run / "global-type-axiom-audit.log").decode())
    return {
        "kind": KIND,
        "what": (
            "Counts over the import closure of the final theorem's module and over the "
            "statement closure, made by devtools.audit_n12_lean from the modules the "
            "closure receipt names, each read by its Git blob, and the source's run "
            "evidence as the packet retains it. Read as data: no Lean was run, and a "
            "token count or a header match is not a parse."
        ),
        "source_url": closure["source_url"],
        "commit": closure["commit"],
        "root": closure["root"],
        "closure_receipt": _path(closure_path),
        "targets": closure["targets"],
        "statement_targets": list(statement_targets),
        "stripping": (
            "audit_n11_lean.strip_code: nested /- -/ comments, -- comments, strings, raw "
            "strings and character literals are blanked before the in-code count, offsets "
            "and lines kept."
        ),
        "closure": census(modules, sizes) if whole else None,
        "statement": census(statement, sizes),
        "shadowing": shadowing(modules) if whole else None,
        "native": native_sites(modules, axioms) if whole else None,
        **run_evidence(modules, closure, run, provenance),
    }


def write(receipt: Mapping[str, Any], out: Path) -> None:
    atomic_write_text(out, retained_json.dumps(receipt) + "\n")


def check(retained: Path = RECEIPT, closure_path: Path = CLOSURE) -> list[str]:
    """Every difference between the retained receipt and what the packet recomputes:
    the statement closure from its retained bytes, and the run evidence."""
    closure = load_closure(closure_path)
    kept = cast("dict[str, Any]", json.loads(retained.read_text(encoding="utf-8")))
    statement = subclosure(closure, kept["statement_targets"])
    fresh = audit(
        read_retained(closure, statement),
        closure,
        closure_path=closure_path,
        statement_targets=kept["statement_targets"],
    )
    problems = [
        f"{key} differs from the packet's recomputation"
        for key in ("kind", "source_url", "commit", "root", "closure_receipt", "statement")
        if kept[key] != fresh[key]
    ]
    for key in ("manifest", "axiom_log"):
        for field, value in fresh[key].items():
            if (
                field not in {"modules_compared", "sha256_mismatches"}
                and kept[key][field] != value
            ):
                problems.append(f"{key}.{field} differs from the packet's recomputation")
    if fresh["manifest"]["sha256_mismatches"]:
        problems.append("a retained statement module differs from the run's manifest")
    return problems


def summary(receipt: Mapping[str, Any]) -> str:
    native = receipt["native"] or {}
    statement = receipt["statement"]
    return (
        f"statement closure {statement['modules']} modules, "
        f"{statement['tokens']['native_decide']['occurrences_code']} native_decide; "
        f"native axioms {native.get('native_axioms')} owned by {native.get('native_owners')} "
        f"declarations, off the path {native.get('off_path', {}).get('calls')} calls; "
        f"manifest mismatches {len(receipt['manifest']['sha256_mismatches'])}"
    )


def main(argv: Sequence[str] | None = None) -> int:
    command = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    sub = command.add_subparsers(dest="command", required=True)
    scan = sub.add_parser("scan", help="count over a checkout's closure; write the receipt")
    scan.add_argument("checkout", type=Path, help="a Git checkout holding the commit")
    scan.add_argument("--closure", type=Path, default=CLOSURE)
    scan.add_argument("--run", type=Path, default=RUN, help="the run's evidence directory")
    scan.add_argument("--provenance", type=Path, default=PROVENANCE)
    scan.add_argument("--statement", nargs="+", default=list(STATEMENT_TARGETS))
    scan.add_argument("--out", type=Path, default=RECEIPT)
    held = sub.add_parser("check", help="hold the receipt to the packet's retained bytes")
    held.add_argument("--receipt", type=Path, default=RECEIPT)
    held.add_argument("--closure", type=Path, default=CLOSURE)
    arguments = command.parse_args(argv)
    if arguments.command == "check":
        problems = check(arguments.receipt, arguments.closure)
        for problem in problems:
            print(problem)
        if not problems:
            print(f"{_path(arguments.receipt)} agrees with the packet")
        return 1 if problems else 0
    closure = load_closure(arguments.closure)
    receipt = audit(
        read_checkout(arguments.checkout, closure),
        closure,
        closure_path=arguments.closure,
        run=arguments.run,
        provenance=arguments.provenance,
        statement_targets=arguments.statement,
    )
    write(receipt, arguments.out)
    print(summary(receipt))
    clean = not receipt["manifest"]["sha256_mismatches"] and not (
        receipt["native"]["owners_without_a_site"]
        or receipt["native"]["owners_whose_axioms_are_not_their_calls"]
    )
    return 0 if clean else 1


if __name__ == "__main__":
    sys.exit(main())
