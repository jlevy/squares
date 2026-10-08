"""Audit the 11SquaresFormalized Lean proof of s(11) = T from its retained packet.

Queuingtheorydotcom/11SquaresFormalized at ``cdc746ed`` proves ``ElevenSquare.optimality``,
``T-060``'s claim, in 7,920 Lean modules (about 1.09 GB), too large to build or retain
here. The packet ``resources/web/queuingtheorydotcom-n11-lean-2026-10-06`` keeps the
statement files, the closure of ``ElevenSquare.Foundations``, the top of the lower
bound's assembly and the run's portable evidence, and pins the rest by the commit and by
the source's final audit. This tool does the checks the import rests on, and writes their
receipts into the packet:

``axioms FINAL_AUDIT_GZ``
    Extracts from the source's final audit the axioms its public theorems depend on, and
    writes ``receipts/lean/axioms-public-theorems.json`` and ``native-axioms.txt``. The
    audit is pinned in the packet's manifest by SHA-256 and is refused if its bytes do
    not have that digest: it is downloaded, and that is the boundary the digest guards.

``scan FINAL_AUDIT_GZ``
    Streams the commit's archive from ``codeload.github.com`` without extracting it,
    hashes every Lean module and compares the hash with the final audit's ``source_sha256``
    map, and counts each of `TOKENS` in every Lean file, in the raw text and in the code
    with comments, strings and character literals blanked. It writes
    ``receipts/tree-scan.json``: each token's pattern and counts, zeros included, and the
    path, line and in-code flag of every raw hit of each token with at most
    `HIT_LIMIT` hits. A token count is not a parse. It matters most for ``axiom``: the
    source's finalizer accepts an axiom as an approved native certificate by its name, so
    the absence of hand-written ``axiom`` declarations is what this scan, and nothing in
    the final audit, establishes.

``stage --out DIR``
    Writes the 18-module closure of ``ElevenSquare.Foundations``, the three build pins and
    the statement probe ``receipts/lean/AuditN11Statement.lean`` from the packet into
    ``DIR``, copied from the packet's retained bytes.

``build --dir DIR --receipt LOG``
    Stages into ``DIR`` and builds the closure one module at a time in import order
    (``lake build ElevenSquare.<module>``), then elaborates the probe
    (``lake env lean AuditN11Statement.lean``), writing every command, its complete
    output, exit code and wall time to ``LOG``. ``DIR`` needs Mathlib ``d13f23b7``'s cache
    first (``lake exe cache get`` in ``DIR``), about 7 GB whole; the closure imports 1,836
    of its modules, and the rest may be removed to save disk.

Usage, from ``packing/``::

    uv run --frozen --all-extras --group dev python -m devtools.audit_n11_lean axioms AUDIT
    uv run --frozen --all-extras --group dev python -m devtools.audit_n11_lean scan AUDIT
    uv run --frozen --all-extras --group dev python -m devtools.audit_n11_lean stage --out W
    uv run --frozen --all-extras --group dev python -m devtools.audit_n11_lean build \\
        --dir W --receipt LOG
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import time
import urllib.request
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from datetime import UTC, datetime
from graphlib import TopologicalSorter
from pathlib import Path
from typing import IO, Any, cast

from strif import atomic_write_text

REPO = Path(__file__).resolve().parents[2]
PACKET = REPO / "packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06"
SOURCE = PACKET / "11SquaresFormalized"
RECEIPTS = PACKET / "receipts"
MANIFEST = PACKET / "acquisition/upstream-subtree.sha256"
COMMIT = "cdc746ed907d258057c283aeb6d077cb2c27e349"
ARCHIVE = f"https://codeload.github.com/Queuingtheorydotcom/11SquaresFormalized/tar.gz/{COMMIT}"
FINAL_AUDIT = "verification/completed-run-20261006/final-audit.json.gz"
#: The uncompressed final audit's SHA-256, as the source's ``summary.json`` records it.
FINAL_AUDIT_JSON_SHA256 = "d66a07c2dcf8f8405dc46151ba500ba40c7de521ff64a28d8cbf772f12575788"
STANDARD_AXIOMS = ("Classical.choice", "Quot.sound", "propext")
NATIVE_MARK = "._native.native_decide.ax_"
PUBLIC_THEOREMS = (
    "ElevenSquare.optimality",
    "ElevenSquare.optimal_side_lower_bound",
    "ElevenSquare.Pending.global_lower_bound",
    "ElevenSquare.Pending.baseline_certificate_exists",
    "ElevenSquare.Pending.prior_certificate_exists",
    "ElevenSquare.Pending.returned_certificate_exists",
)
#: The statement closure: ``ElevenSquare.Foundations`` and every local module it imports.
CLOSURE = (
    "BasicGeometry",
    "CaseCountSupport",
    "Cases",
    "Combinatorics",
    "Construction",
    "ConstructionData",
    "Cover",
    "CoverChecks",
    "CoverData",
    "Endpoint",
    "EndpointBounds",
    "Foundations",
    "GeneratedCover0",
    "GeneratedCover1",
    "GeneratedCover2",
    "GeneratedCover3",
    "Geometry",
    "Orientation",
)
PINS = ("lakefile.lean", "lake-manifest.json", "lean-toolchain")
PROBE = RECEIPTS / "lean/AuditN11Statement.lean"
#: Raw hits are listed one by one for a token with at most this many.
HIT_LIMIT = 200

#: Tokens that would let something other than the kernel decide a proof, or change how a
#: statement parses or which declaration a name means.
TOKENS: Mapping[str, str] = {
    "sorry": r"\bsorry\b",
    "admit": r"\badmit\b",
    "axiom_decl": (
        r"(?m)^[ \t]*(?:@\[[^\]]*\][ \t]*)?"
        r"(?:private[ \t]+|protected[ \t]+|noncomputable[ \t]+|unsafe[ \t]+)*axiom\b"
    ),
    "native_decide": r"\bnative_decide\b",
    "decide_native": r"decide[ \t]*\+native",
    "ofReduceBool": r"\bofReduceBool\b|\breduceBool\b",
    "trustCompiler": r"\btrustCompiler\b",
    "implemented_by": r"\bimplemented_by\b",
    "extern": r"@\[[^\]]*\bextern\b",
    "unsafe": r"\bunsafe\b",
    "skipKernelTC": r"skipKernelTC|debug\.skip",
    "exit": r"(?m)^[ \t]*#exit\b",
    "eval": r"(?m)^[ \t]*#eval\b",
    "run_cmd": r"\brun_cmd\b|\brun_elab\b|\brun_meta\b|\brun_tac\b",
    "env_mod": (
        r"\bmodifyEnv\b|\baddDecl\b|\baddDeclCore\b|\baddDeclWithoutChecking\b"
        r"|\bEnvironment\.add\b|\bsetEnv\b"
    ),
    "initialize": r"(?m)^[ \t]*(?:builtin_)?initialize\b",
    "notation": (
        r"(?m)^[ \t]*(?:@\[[^\]]*\][ \t]*)?(?:local[ \t]+|scoped[ \t]+)?"
        r"(?:notation\d*|infix|infixl|infixr|prefix|postfix)\b"
    ),
    "macro": (
        r"(?m)^[ \t]*(?:@\[[^\]]*\][ \t]*)?(?:local[ \t]+|scoped[ \t]+)?"
        r"(?:macro|macro_rules|syntax|elab|elab_rules|declare_syntax_cat)\b"
    ),
    "elab_attribute": (
        r"@\[[^\]]*\b(?:tactic|term_elab|command_elab|macro|delab|app_unexpander)\b"
    ),
    "export": r"(?m)^[ \t]*export\b",
    "open_renaming": r"\bopen\b[^\n]*\b(?:renaming|hiding)\b",
    "instance": (
        r"(?m)^[ \t]*(?:@\[[^\]]*\][ \t]*)?"
        r"(?:(?:scoped|local|private|noncomputable)[ \t]+)*instance\b"
    ),
    "import_Lean": r"(?m)^import[ \t]+Lean(?:\.|\s|$)",
    "opaque": (
        r"(?m)^[ \t]*(?:@\[[^\]]*\][ \t]*)?"
        r"(?:private[ \t]+|protected[ \t]+|noncomputable[ \t]+)*opaque\b"
    ),
    "csimp": r"@\[[^\]]*\bcsimp\b",
}
_COMPILED = {name: re.compile(pattern) for name, pattern in TOKENS.items()}
_IDENT = re.compile(r"[A-Za-z0-9_'!?.À-￿]")
_CHAR = re.compile(r"'(?:\\(?:x[0-9a-fA-F]{2}|u[0-9a-fA-F]{4}|.)|[^\\'\n])'")
_RAW = re.compile(r'r(#*)"')


def _blank(text: str) -> str:
    """The same text with every character but a newline replaced by a space."""
    return re.sub(r"[^\n]", " ", text)


def strip_code(text: str) -> str:
    """Lean source with comments, strings and character literals blanked, offsets kept.

    Nested ``/- -/`` blocks, ``--`` lines, ``"..."`` strings with escapes, raw strings
    ``r#"..."#`` and character literals such as ``'"'`` become spaces, newlines kept, so a
    match in the result is at the same offset and line as in the source.
    """
    out: list[str] = []
    i, n = 0, len(text)
    while i < n:
        if text.startswith("/-", i):
            depth, j = 1, i + 2
            while j < n and depth:
                if text.startswith("/-", j):
                    depth, j = depth + 1, j + 2
                elif text.startswith("-/", j):
                    depth, j = depth - 1, j + 2
                else:
                    j += 1
            out.append(_blank(text[i:j]))
            i = j
            continue
        if text.startswith("--", i):
            end = text.find("\n", i)
            j = n if end < 0 else end
            out.append(_blank(text[i:j]))
            i = j
            continue
        preceded = i > 0 and _IDENT.match(text[i - 1]) is not None
        raw = _RAW.match(text, i) if not preceded else None
        if raw:
            close = '"' + raw.group(1)
            end = text.find(close, raw.end())
            j = n if end < 0 else end + len(close)
            out.append(_blank(text[i:j]))
            i = j
            continue
        if text[i] == '"':
            j = i + 1
            while j < n and text[j] != '"':
                j += 2 if text[j] == "\\" else 1
            j = min(j + 1, n)
            out.append(_blank(text[i:j]))
            i = j
            continue
        char = _CHAR.match(text, i) if text[i] == "'" and not preceded else None
        if char:
            out.append(_blank(char.group(0)))
            i = char.end()
            continue
        out.append(text[i])
        i += 1
    return "".join(out)


def token_counts(text: str) -> dict[str, int]:
    """How often each of `TOKENS` occurs in the code of one Lean file."""
    code = strip_code(text)
    return {name: len(rx.findall(code)) for name, rx in _COMPILED.items()}


def token_hits(text: str) -> dict[str, list[tuple[int, bool]]]:
    """Every raw match of each token: its line, and whether it is in code."""
    code = strip_code(text)
    hits: dict[str, list[tuple[int, bool]]] = {}
    for name, rx in _COMPILED.items():
        for match in rx.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            in_code = rx.match(code, match.start()) is not None
            hits.setdefault(name, []).append((line, in_code))
    return hits


def manifest_sha256(manifest: Path = MANIFEST) -> dict[str, str]:
    """The packet manifest's SHA-256 by upstream path."""
    found: dict[str, str] = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        digest, _, name = line.partition("  ")
        found[name.removeprefix("./")] = digest
    return found


def pinned_sha256(path: str, manifest: Path = MANIFEST) -> str:
    """The SHA-256 the packet's manifest records for an upstream path."""
    found = manifest_sha256(manifest)
    if path not in found:
        msg = f"{path} is not in {manifest}"
        raise SystemExit(msg)
    return found[path]


def load_final_audit(path: Path, *, expected: str | None = None) -> dict[str, Any]:
    """The final audit, refused unless its bytes are the ones the packet pins."""
    raw = path.read_bytes()
    want = pinned_sha256(FINAL_AUDIT) if expected is None else expected
    if hashlib.sha256(raw).hexdigest() != want:
        msg = f"{path} is not the final audit the packet pins (SHA-256 {want})"
        raise SystemExit(msg)
    return cast("dict[str, Any]", json.loads(gzip.decompress(raw)))


def _native(axioms: Iterable[str]) -> list[str]:
    return sorted(a for a in axioms if NATIVE_MARK in a)


def _owner(axiom: str) -> str:
    return axiom.split(NATIVE_MARK, maxsplit=1)[0]


def axiom_receipt(audit: Mapping[str, Any], audit_bytes: bytes) -> dict[str, Any]:
    """The axioms of the public theorems, from the final audit's axiom map."""
    axioms = cast("Mapping[str, list[str]]", audit["axioms"])
    native_all = sorted(cast("list[str]", audit["native_certificate_axioms"]))
    rows: dict[str, Any] = {}
    for target in PUBLIC_THEOREMS:
        found = axioms.get(target)
        if found is None:
            rows[target] = None
            continue
        native = _native(found)
        rows[target] = {
            "axiom_count": len(found),
            "non_native_axioms": sorted(a for a in found if NATIVE_MARK not in a),
            "sorryAx": "sorryAx" in found,
            "native_decide_axioms": len(native),
            "native_decide_owner_declarations": len({_owner(a) for a in native}),
            "native_set_equals_audit_native_list": native == native_all,
            "native_subset_of_audit_native_list": set(native) <= set(native_all),
        }
    every = {a for listed in axioms.values() for a in listed}
    uncompressed = hashlib.sha256(gzip.decompress(audit_bytes)).hexdigest()
    return {
        "what": (
            "The axioms the source's final audit records for its public theorems, "
            "extracted here by devtools.audit_n11_lean from "
            f"{FINAL_AUDIT} at Queuingtheorydotcom/11SquaresFormalized {COMMIT}. The "
            "audit is the source's own: its finalizer parses '#print axioms' output from "
            "the compiler logs of EvolvingPrograms/11SquaresEvolving run 37414883750 "
            "(source commit 1bf942a7). Nothing here re-ran Lean on these theorems. The "
            "finalizer recognises a native axiom by its name; that no hand-written axiom "
            "takes such a name is the archive scan's finding (tree-scan.json), not this one."
        ),
        "final_audit_gz_sha256": hashlib.sha256(audit_bytes).hexdigest(),
        "final_audit_sha256": uncompressed,
        "summary_json_final_audit_uncompressed_sha256": FINAL_AUDIT_JSON_SHA256,
        "status": audit["status"],
        "trust_model": audit["trust_model"],
        "global_optimality_proved": audit["global_optimality_proved"],
        "checked_modules": audit["checked_modules"],
        "lean_toolchain": audit["lean_toolchain"],
        "mathlib_revision": audit["mathlib_revision"],
        "explicit_native_admissions": audit["explicit_native_admissions"],
        "audited_targets": len(axioms),
        "non_native_axioms_anywhere": sorted(a for a in every if NATIVE_MARK not in a),
        "native_decide_axioms_in_audit": len(native_all),
        "native_decide_owner_declarations_in_audit": len({_owner(a) for a in native_all}),
        "public_theorems": rows,
        "native_axiom_list": (
            "native-axioms.txt, the audit's native_certificate_axioms sorted, one per line"
        ),
        "final_audit_matches_summary": uncompressed == FINAL_AUDIT_JSON_SHA256,
    }


def write_axioms(audit_path: Path, out: Path) -> dict[str, Any]:
    """Write the axiom receipt and the sorted native-axiom list into ``out``."""
    audit = load_final_audit(audit_path)
    receipt = axiom_receipt(audit, audit_path.read_bytes())
    out.mkdir(parents=True, exist_ok=True)
    atomic_write_text(out / "axioms-public-theorems.json", json.dumps(receipt, indent=1) + "\n")
    native = sorted(cast("list[str]", audit["native_certificate_axioms"]))
    atomic_write_text(out / "native-axioms.txt", "\n".join(native) + "\n")
    return receipt


def scan_archive(stream: IO[bytes], expected: Mapping[str, str]) -> dict[str, Any]:
    """Hash and scan every Lean file of a gzip tar stream, against the audit's hash map."""
    seen: dict[str, str] = {}
    code_files: Counter[str] = Counter()
    code_uses: Counter[str] = Counter()
    raw_files: Counter[str] = Counter()
    raw_uses: Counter[str] = Counter()
    hits: dict[str, list[dict[str, object]]] = {name: [] for name in TOKENS}
    lean_bytes = all_files = all_bytes = 0
    with tarfile.open(fileobj=stream, mode="r|gz") as tar:
        for member in tar:
            if not member.isfile():
                continue
            extracted = tar.extractfile(member)
            if extracted is None:
                continue
            data = extracted.read()
            all_files += 1
            all_bytes += len(data)
            path = member.name.split("/", 1)[1]
            if not path.endswith(".lean"):
                continue
            lean_bytes += len(data)
            module = path.removesuffix(".lean").replace("/", ".")
            seen[module] = hashlib.sha256(data).hexdigest()
            for name, found in token_hits(data.decode("utf-8")).items():
                raw_files[name] += 1
                raw_uses[name] += len(found)
                in_code = [line for line, code in found if code]
                if in_code:
                    code_files[name] += 1
                    code_uses[name] += len(in_code)
                hits[name].extend(
                    {"path": path, "line": line, "in_code": code} for line, code in found
                )
    audited, present = set(expected), set(seen)
    return {
        "url": ARCHIVE,
        "lean_files": len(seen),
        "lean_bytes": lean_bytes,
        "all_files": all_files,
        "all_bytes": all_bytes,
        "final_audit_modules": len(audited),
        "sha256_match": sum(1 for m in audited & present if seen[m] == expected[m]),
        "sha256_mismatch": sorted(m for m in audited & present if seen[m] != expected[m]),
        "in_audit_not_in_tree": sorted(audited - present),
        "in_tree_not_in_audit": sorted(present - audited),
        "stripping": (
            "Comments (nested /- -/ blocks and -- lines), string literals with escapes, raw "
            'strings r#"..."# and character literals are blanked before the in-code count, '
            "offsets and lines kept."
        ),
        "tokens": {
            name: {
                "pattern": TOKENS[name],
                "files_code": code_files[name],
                "occurrences_code": code_uses[name],
                "files_raw": raw_files[name],
                "occurrences_raw": raw_uses[name],
                "raw_hits": hits[name] if len(hits[name]) <= HIT_LIMIT else "over the limit",
            }
            for name in TOKENS
        },
    }


def write_scan(audit_path: Path, out: Path, url: str = ARCHIVE) -> dict[str, Any]:
    """Stream the archive at ``url`` and write ``out``."""
    audit = load_final_audit(audit_path)
    expected = cast("Mapping[str, str]", audit["source_sha256"])
    with urllib.request.urlopen(url) as response:
        report = scan_archive(cast("IO[bytes]", response), expected)
    atomic_write_text(out, json.dumps(report, indent=1, sort_keys=True) + "\n")
    return report


def stage(out: Path, source: Path = SOURCE, probe: Path = PROBE) -> list[Path]:
    """Copy the statement closure, the pins and the probe into ``out``; return them.

    The packet's own bytes are copied as they are: ``devtools.acquire_source --check``
    holds the packet to its upstream manifest, and the repository is no trust boundary
    with itself (OR-16).
    """
    if (out / "ElevenSquare").exists():
        shutil.rmtree(out / "ElevenSquare")
    names = [*PINS, *(f"ElevenSquare/{module}.lean" for module in CLOSURE)]
    written: list[Path] = []
    for name in names:
        target = out / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / name, target)
        written.append(target)
    shutil.copyfile(probe, out / probe.name)
    written.append(out / probe.name)
    return written


def local_imports(text: str) -> set[str]:
    """The ``ElevenSquare`` modules a Lean file imports."""
    return {
        m.removeprefix("ElevenSquare.")
        for m in re.findall(r"(?m)^import\s+(ElevenSquare\.\S+)", text)
    }


def build_order(directory: Path) -> list[str]:
    """The staged closure's modules, each after every module it imports."""
    graph = {
        module: local_imports(
            (directory / "ElevenSquare" / f"{module}.lean").read_text("utf-8")
        )
        for module in CLOSURE
    }
    return list(TopologicalSorter(graph).static_order())


def _utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def build(directory: Path, receipt: Path) -> int:
    """Stage, build the closure module by module and run the probe; write one receipt."""
    staged = stage(directory)
    env = {**os.environ, "LEAN_NUM_THREADS": "2"}
    lines = [
        f"# devtools.audit_n11_lean build, Queuingtheorydotcom/11SquaresFormalized {COMMIT}",
        f"# staged {len(staged)} files from the packet's retained bytes",
        f"# host: {os.cpu_count()} cores; started {_utc()}; LEAN_NUM_THREADS=2, nice -n 10",
    ]
    steps: list[list[str]] = [["lean", "--version"], ["lake", "--version"]]
    steps += [["lake", "build", f"ElevenSquare.{module}"] for module in build_order(directory)]
    steps.append(["lake", "env", "lean", PROBE.name])
    worst = 0
    for argv in steps:
        started = time.monotonic()
        done = subprocess.run(
            ["nice", "-n", "10", *argv],
            cwd=directory,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        lines.append(f"# command: {' '.join(argv)}")
        lines.extend((done.stdout + done.stderr).rstrip("\n").splitlines())
        lines.append(f"# exit {done.returncode}; wall {time.monotonic() - started:.1f} s")
        worst = worst or done.returncode
    lines.append(f"# finished {_utc()}; exit {worst}")
    atomic_write_text(receipt, "\n".join(lines) + "\n")
    return worst


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    sub = command.add_subparsers(dest="command", required=True)
    axioms = sub.add_parser("axioms", help="write the axiom receipt from the final audit")
    axioms.add_argument("audit", type=Path)
    axioms.add_argument("--out-dir", type=Path, default=RECEIPTS / "lean")
    scan = sub.add_parser("scan", help="hash and scan the commit's archive")
    scan.add_argument("audit", type=Path)
    scan.add_argument("--out", type=Path, default=RECEIPTS / "tree-scan.json")
    scan.add_argument("--url", default=ARCHIVE)
    staged = sub.add_parser("stage", help="write the statement closure, ready to build")
    staged.add_argument("--out", type=Path, required=True)
    built = sub.add_parser("build", help="stage, build the closure and run the probe")
    built.add_argument("--dir", type=Path, required=True)
    built.add_argument(
        "--receipt", type=Path, default=RECEIPTS / "lean/build-statement-closure.log"
    )
    return command


def main(argv: Sequence[str] | None = None) -> int:
    arguments = parser().parse_args(argv)
    if arguments.command == "axioms":
        receipt = write_axioms(arguments.audit, arguments.out_dir)
        print(json.dumps(receipt["public_theorems"]["ElevenSquare.optimality"], indent=1))
        return 0 if receipt["final_audit_matches_summary"] else 1
    if arguments.command == "scan":
        report = write_scan(arguments.audit, arguments.out, arguments.url)
        found = {k: v["files_code"] for k, v in report["tokens"].items() if v["files_code"]}
        print(
            f"{report['sha256_match']} of {report['final_audit_modules']} modules match the "
            f"final audit; files with each token in code: {found}"
        )
        clean = not report["sha256_mismatch"] and not report["in_audit_not_in_tree"]
        return 0 if clean else 1
    if arguments.command == "build":
        return build(arguments.dir, arguments.receipt)
    for path in stage(arguments.out):
        print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
