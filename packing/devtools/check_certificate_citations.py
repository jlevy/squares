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

A verified certificate a register entry cites may wait for its case records only by a
recorded decision. `certificate-citation-deferrals.yaml` beside this module lists each
such orphan with the register entries that cite it, the open bead that owns the case
adoption, what the adoption waits on, the day it was recorded and why: on 2026-10-10 the
replays of T-128, T-130 and T-131 were reviewed while house adoption waited for a pull
request that rewrites every case record. A deferral is not a silent skip. It fails as soon
as a case record cites its evidence, a named entry stops citing it, or it is more than
`DEFERRAL_DAYS` older than the evidence register's `last_reviewed`, so the list cannot
outlive what it defers, and an orphan it does not name fails as before.

Usage:
    uv run --frozen --all-extras --group dev python -m devtools.check_certificate_citations
"""

from __future__ import annotations

import ast
import re
from collections.abc import Mapping, Sequence
from datetime import date
from pathlib import Path

from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
CASES = ROOT / "cases"
FRONTIER = ROOT / "frontier"
#: Orphans whose case adoption was deferred by a recorded decision.
DEFERRALS = Path(__file__).with_name("certificate-citation-deferrals.yaml")
#: How long a deferral stands before it must be re-dated with what happened since, as a
#: register entry's `activity` must (`devtools.check_results`).
DEFERRAL_DAYS = 30
_BEAD = re.compile(r"think-[a-z0-9]{4}")
_RESULT = re.compile(r"T-\d{3}")


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


def referenced_evidence(node: object) -> set[str]:
    """Every evidence id the record reaches, from any block that carries one.

    Walking rather than naming three blocks: the schema puts `evidence` on both bounds,
    both reported bounds, the rigidity block, the case roster, each conflict and each
    blocker, and a sweep that reads a subset of those reports a citation as missing when it
    is merely somewhere else. That direction is safe -- it over-reports -- but a guard that
    cries wolf gets switched off, which is the failure this one exists to avoid.
    """
    found: set[str] = set()
    if isinstance(node, Mapping):
        for key, value in node.items():
            if key == "evidence" and isinstance(value, list):
                found.update(item for item in value if isinstance(item, str))
            else:
                found |= referenced_evidence(value)
    elif isinstance(node, list):
        for item in node:
            found |= referenced_evidence(item)
    return found


#: What an evidence entry claims when it bears on a bound of `s(n)`. Only a case record
#: stands as the citation of such an entry, whatever result also cites it.
BOUND_CLAIMS = frozenset({"lower-bound", "upper-bound", "exact-value"})


def method_limit_evidence(evidence_by_id: Mapping[str, Mapping[str, object]]) -> set[str]:
    """Evidence a registered result of kind `method-limit` cites, claiming no bound.

    A method limit's evidence says how far a proof method can reach, not what `s(n)` is,
    so its citing record is the method-limit result. An entry that claims a bound is left
    to the case records even when a method-limit result cites it too, so the exception
    cannot hide a bound no case carries.
    """
    register = safe_load((FRONTIER / "results.yaml").read_text(encoding="utf-8"))
    return {
        identifier
        for result in register["results"]
        if result.get("kind") == "method-limit"
        for identifier in result.get("evidence", [])
        if (evidence_by_id.get(identifier) or {}).get("claim") not in BOUND_CLAIMS
    }


def orphaned_evidence(evidence_by_id: dict[str, dict]) -> list[str]:
    """Verified, replayable evidence that no frontier record cites.

    The `CERTIFIES` sweep below runs from case packages, and a case package is only one
    place a certificate lives. `E-n029-interval-certified-upper` is `verified`, replays,
    proves a bound tighter than the one `n = 029` carries -- and was cited by nothing,
    while that record's blocker said no formal certificate existed. The certificate is a
    witness file, so nothing keyed on `cases/` could have found it.

    This is the general form: evidence that is verified, has passed its replay, and names a
    certificate is evidence somebody meant to bear on a case. If no case cites it, either
    the record is behind or the evidence should not be in the register.

    A method limit is the one exception to "a case cites it": it bounds what a proof
    method can reach across many cases, and a case record has no block for that. Its
    citing record is the method-limit result in the register (T-058's exact ceilings).
    Evidence that claims a bound still needs a case to cite it (`method_limit_evidence`).
    """
    cited: set[str] = set()
    for path in sorted(FRONTIER.glob("n-*.md")):
        case = safe_load(path.read_text(encoding="utf-8").split("---\n")[1])
        cited |= referenced_evidence(case["packing"])
    cited |= method_limit_evidence(evidence_by_id)

    return sorted(
        identifier
        for identifier, record in evidence_by_id.items()
        if record.get("assurance") == "verified"
        and record.get("replay_status") == "passed"
        and record.get("certificate")
        and identifier not in cited
    )


def _strings(value: object) -> list[str]:
    """A YAML list of strings as one, and anything else as none."""
    return [str(item) for item in value] if isinstance(value, list) else []


def load_deferrals(path: Path = DEFERRALS) -> list[Mapping[str, object]]:
    """The declared deferrals, in file order."""
    document = safe_load(path.read_text(encoding="utf-8")) or {}
    return list(document.get("deferrals") or [])


def deferred(
    evidence_by_id: dict[str, dict],
    deferrals: Sequence[Mapping[str, object]],
    results: Sequence[Mapping[str, object]],
    reviewed: str,
) -> tuple[set[str], list[str]]:
    """The orphans the deferrals excuse, and what is wrong with the deferrals themselves.

    A deferral excuses an orphan only while it is one: verified, replayed, naming a
    certificate and cited by no case record. It names the register entries that cite the
    evidence, an owning bead, what it waits on and why, and it expires `DEFERRAL_DAYS`
    after `recorded`, read against `reviewed`, the evidence register's `last_reviewed`.
    """
    orphans = set(orphaned_evidence(evidence_by_id))
    citing = {
        str(result.get("id")): set(_strings(result.get("evidence"))) for result in results
    }
    excused: set[str] = set()
    problems: list[str] = []
    for deferral in deferrals:
        identifier = str(deferral.get("evidence", ""))
        where = f"deferral of {identifier or '<no evidence>'}"
        if identifier in excused:
            problems.append(f"{where}: listed twice")
            continue
        named = _strings(deferral.get("results"))
        recorded = str(deferral.get("recorded", ""))
        missing = [
            field
            for field in ("evidence", "results", "bead", "blocked_on", "recorded", "reason")
            if not deferral.get(field)
        ]
        if missing:
            problems.append(f"{where}: names no {', '.join(missing)}")
            continue
        if not _BEAD.fullmatch(str(deferral["bead"])):
            problems.append(f"{where}: its bead is not a think- alias")
        if identifier not in evidence_by_id:
            problems.append(f"{where}: no such evidence entry")
            continue
        if identifier not in orphans:
            problems.append(
                f"{where}: stale, since a case record cites it now or it is no longer a "
                "verified, replayed certificate; remove the deferral"
            )
            continue
        problems.extend(
            f"{where}: {result} does not cite it"
            for result in named
            if not _RESULT.fullmatch(result) or identifier not in citing.get(result, set())
        )
        try:
            age = (date.fromisoformat(reviewed) - date.fromisoformat(recorded)).days
        except ValueError:
            problems.append(f"{where}: recorded {recorded!r} is not a date")
            continue
        if age > DEFERRAL_DAYS:
            problems.append(
                f"{where}: recorded {recorded}, {age} days before the register's last review; "
                "adopt it in the case records or re-date it with what happened since"
            )
            continue
        excused.add(identifier)
    return excused, problems


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

    referenced = referenced_evidence(packing)

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

    register = safe_load((FRONTIER / "results.yaml").read_text(encoding="utf-8"))
    excused, deferral_problems = deferred(
        evidence_by_id, load_deferrals(), register["results"], str(document["last_reviewed"])
    )
    problems.extend(
        f"{identifier} is verified, replays, and names a certificate, but no frontier "
        "record cites it -- either a record is behind its own evidence, or the evidence "
        "does not belong in the register"
        for identifier in orphaned_evidence(evidence_by_id)
        if identifier not in excused
    )
    problems.extend(deferral_problems)

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
    if excused:
        print(
            f"{len(excused)} verified certificates wait for their case records by a recorded "
            f"deferral ({DEFERRALS.name}): {', '.join(sorted(excused))}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
