#!/usr/bin/env python3
"""Every exact certificate this repository holds must be cited by the record it bears on.

`assurance.py` already checks a frontier record against itself: that a `verified` claim
uses a formal method, that a formal upper bound trailing the reported one carries a
blocker, that the blocker goes when the bounds agree. Every one of those reads the
record's own fields, so none of them can notice a certificate the record was never told
about.

`D-398` is what that permitted. `cases/gobel40` and `cases/gobel_family` decided 780,
2080 and 3916 pairs by exact sign over `Q(sqrt 2)`, ran in the gate for two sessions, and
the three records they bear on went on declaring a blocker of kind `mathematics` reading
"No formal certificate currently supports the tighter reported upper bound". Nothing was
false and nothing failed; the record was simply behind its own toolchain, in the
conservative direction, silently.

This sweep runs the other way. Each `cases/*/verify_exact.py` declares `CERTIFIES`, the
sizes it decides, and each of those sizes must have a frontier record citing that package
as the `certificate` of some evidence record it names. An undeclared `CERTIFIES` is a
refusal rather than a skip, so adding a case package cannot quietly opt out of the check.

The declaration is read with `ast` rather than by importing: `verify_exact` modules set
`getcontext().prec` when they run, and a checker that mutates process-global decimal
precision as a side effect of counting files would be its own defect.

Usage:
    uv run --frozen --all-extras --group dev python -m devtools.check_certificate_citations
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
CASES = ROOT / "cases"
FRONTIER = ROOT / "frontier"


class UndeclaredError(Exception):
    """`CERTIFIES` is present but not readable as a literal, which is a refusal.

    Reading the declaration statically is what keeps this checker free of the import
    side effects described in the module docstring, and the cost of that choice is that
    `CERTIFIES = tuple(range(...))` cannot be evaluated. That has to surface as a message
    naming the package rather than as a traceback: an exception escaping `main` aborts the
    sweep, so one unreadable declaration would silently stop every later package from being
    checked at all -- a guard that fails open on the one input designed to confuse it.
    """


def declared_sizes(module: Path) -> tuple[int, ...] | None:
    """Return the module's `CERTIFIES` tuple, or None if it declares none.

    Raises `Undeclared` if `CERTIFIES` is present but not a literal.
    """
    tree = ast.parse(module.read_text(encoding="utf-8"))
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "CERTIFIES":
                try:
                    value = ast.literal_eval(node.value)
                    return tuple(int(n) for n in value)
                except (ValueError, TypeError) as exc:
                    raise UndeclaredError(
                        "CERTIFIES must be a literal tuple of integers, readable without "
                        f"importing the module ({exc})"
                    ) from exc
    return None


def cited_certificates(n: int, evidence_by_id: dict[str, dict]) -> set[str]:
    """Return the certificate paths the record for `n` reaches through *verified* evidence.

    Verified is part of the question, not a separate one. The point of the sweep is that an
    exact certificate is named by the record it bears on, and a `reported` evidence record
    carrying a path into a case package would satisfy the letter of that while asserting
    nothing this repository checked -- the record would cite the certificate and still not
    claim it. Requiring the citing record to be `verified` is what makes a pass mean what
    the step name says.
    """
    path = FRONTIER / f"n-{n:03d}.md"
    if not path.exists():
        return set()
    case = safe_load(path.read_text(encoding="utf-8").split("---\n")[1])
    packing = case["packing"]

    referenced: set[str] = set()
    for key in ("reported_upper_bound", "verified_upper_bound", "rigidity"):
        block = packing.get(key)
        if isinstance(block, dict):
            referenced.update(block.get("evidence") or [])

    return {
        certificate
        for ref in referenced
        if (record := evidence_by_id.get(ref))
        and record.get("assurance") == "verified"
        and (certificate := record.get("certificate"))
    }


def main() -> int:
    document = safe_load((FRONTIER / "evidence.yaml").read_text(encoding="utf-8"))
    evidence_by_id = {record["id"]: record for record in document["evidence"]}

    problems: list[str] = []
    checked: list[str] = []

    for module in sorted(CASES.glob("*/verify_exact.py")):
        package = module.parent.name
        try:
            sizes = declared_sizes(module)
        except UndeclaredError as exc:
            problems.append(f"cases/{package}/verify_exact.py: {exc}")
            continue
        if sizes is None:
            problems.append(
                f"cases/{package}/verify_exact.py declares no CERTIFIES; "
                "name the sizes it decides so the frontier records can be checked against it"
            )
            continue
        if not sizes:
            problems.append(f"cases/{package}: CERTIFIES is empty")
            continue

        prefix = f"cases/{package}/"
        out_of_range = [n for n in sizes if not (FRONTIER / f"n-{n:03d}.md").exists()]
        if out_of_range:
            problems.append(
                f"cases/{package}: CERTIFIES names {out_of_range}, "
                "which have no frontier record"
            )
            continue
        for n in sizes:
            certificates = cited_certificates(n, evidence_by_id)
            if not any(path.startswith(prefix) for path in certificates):
                problems.append(
                    f"n={n}: cases/{package} verifies this size exactly, but frontier/"
                    f"n-{n:03d}.md cites no evidence whose certificate is in that package "
                    f"(it cites {sorted(certificates) or 'none'})"
                )
        checked.append(f"cases/{package} -> {list(sizes)}")

    if problems:
        print("exact certificates that no frontier record names:")
        for problem in problems:
            print(f"  {problem}")
        return 1

    total = sum(len(entry.split("->")[1].split(",")) for entry in checked)
    print(f"{len(checked)} case packages certify {total} sizes, every one cited by its record")
    for entry in checked:
        print(f"  {entry}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
