#!/usr/bin/env python3
"""Re-derive every lower bound the register attributes to [Nagamochi 2005].

`E-nagamochi-lower` is the register's most-cited evidence record, and two different
counts describe it. 95 of the hundred case records cite this result; it supplies the
operative verified lower bound in 83 of them. The other 12 citations are context rather
than current bounds -- seven proved cases that never rested on the theorem, and the five
open cases `n = 17` through `n = 21`, where first-party certificates displaced it between
2026-08-31 (when the operative count was 88) and 2026-09-04. The next most-cited evidence
record carries two.

Nothing checked that the recorded values were what the theorem gives: `assurance.py`
verifies that a bound cites verified evidence of the right claim and scope, which is a
statement about the citation and not about the arithmetic. A transcription slip in any
one of the 83 operative verified-field values would have passed.

Theorem 2, as the evidence record states it and as re-derived here from Theorem 1
(`nu(a, b) < ab - (a + 1 - ceil(a)) - (b + 1 - ceil(b))` for `a, b >= 2`):

- `N` in `{m^2, m^2 - 1, m^2 - 2}` gives `s(N) >= m`. Put `a = b = m` in Theorem 1: it
  yields `nu(m, m) < m^2 - 2`, so `m^2 - 2` unit squares already do not fit strictly
  inside side `m`.
- otherwise `s(N) >= sqrt(N - 2k + 1) + 1` with `k = floor(sqrt(N))`. Put `a = b = k + t`
  and choose `t` so that `(k + t)^2 - 2t = N`; then `k + t` is the bound.

The two collapse to `min(ceil(sqrt(N)), sqrt(N - 2*floor(sqrt(N)) + 1) + 1)`, and this
checks that form against the record rather than assuming it.

Also checks the direction that would be a soundness defect rather than a bookkeeping one:
a lower bound may never exceed the reported upper bound for the same `n`.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.check_nagamochi_bounds
"""

from __future__ import annotations

import math
import re
from decimal import Decimal, localcontext
from pathlib import Path

from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"
RECORD = "E-nagamochi-lower"
#: The reader-facing prose that quotes the corpus count, in its two shapes. Both are
#: checked against the case records because the figure was typed once and outlived the
#: 4.5058 adoption by a day (D-430): the README said sixty-three when the corpus said sixty.
README = FRONTIER / "README.md"
_README_COUNT = re.compile(r"Of the (\d+) open cases,\s+\*\*(\d+)\*\* have\s+Nagamochi")
_BODY_COUNT = re.compile(r"(\d+) of the (\d+) open cases at\s+`n ≤ 100` are governed by it")

#: The register's own prose about this record, and the two counts it quotes. They are
#: different numbers and were conflated: a case record that names `E-nagamochi-lower`
#: anywhere *cites* it, while only one whose `verified_lower_bound` names it is
#: *operative*. The docstring above said 85, `results.yaml` said 86, `evidence.yaml`
#: said 88, and this checker printed 83 -- four figures for two quantities, none of them
#: derived. Both are now read from the case records in the shapes the prose uses, so
#: neither can outlive the corpus the way the README's open-case count no longer can.
SELF = Path(__file__)
RESULTS = FRONTIER / "results.yaml"
EVIDENCE = FRONTIER / "evidence.yaml"
_CITED_COUNT = re.compile(r"(\d+) of the hundred (?:frontier )?case records cite")
_OPERATIVE_COUNT = re.compile(r"operative verified lower bound in (\d+) of them")
_OPERATIVE_VALUES = re.compile(r"the (\d+) operative verified-field values")
_OTHER_CITATIONS = re.compile(r"[Tt]he other (\d+) citations")

#: Enough to compare against any decimal the register carries, and pinned rather than
#: inherited: `decimal`'s context is process-global (see `think-iskp`).
DIGITS = 80


def theorem_two(n: int) -> tuple[Decimal, bool]:
    """The bound Theorem 2 gives for `n`, and whether `n` is one of its exact cases."""
    root = math.isqrt(n)
    exact = any(n == m * m - offset for m in (root, root + 1) for offset in (0, 1, 2))
    with localcontext() as context:
        context.prec = DIGITS
        if exact:
            return Decimal(math.isqrt(n - 1) + 1), True
        return Decimal(n - 2 * root + 1).sqrt() + 1, False


def cases() -> dict[int, dict]:
    found = {}
    for path in sorted(FRONTIER.glob("n-*.md")):
        payload = safe_load(path.read_text(encoding="utf-8").split("---\n")[1])["packing"]
        found[payload["n"]] = payload
    return found


def cites(case: dict) -> bool:
    """Does this case record name the record anywhere in its front matter?

    The roll-up `evidence` list is meant to be exactly this set, but the question asked
    is "does the record appear", so it is answered by walking the whole payload rather
    than by trusting one field to be complete.
    """
    stack: list[object] = [case]
    while stack:
        node = stack.pop()
        if isinstance(node, dict):
            stack.extend(node.values())
        elif isinstance(node, list):
            stack.extend(node)
        elif node == RECORD:
            return True
    return False


def register_counts(found: dict[int, dict]) -> tuple[int, int]:
    """Case records citing the record, and those where it is the operative bound."""
    cited = sum(cites(case) for case in found.values())
    operative = sum(
        RECORD in ((case.get("verified_lower_bound") or {}).get("evidence") or [])
        for case in found.values()
    )
    return cited, operative


def register_prose_counts(found: dict[int, dict]) -> list[str]:
    """The two register-wide counts, wherever the prose that owns them quotes either.

    Read from this module's own docstring as well as `results.yaml` and `evidence.yaml`,
    because all three carried a figure for these quantities and all three were wrong in
    different ways. The two primary shapes must also be present: a count that is deleted
    rather than corrected is a count nothing checks.
    """
    cited, operative = register_counts(found)
    forms = (
        (_CITED_COUNT, cited, "case records citing the record", True),
        (_OPERATIVE_COUNT, operative, "operative verified lower bounds", True),
        (_OPERATIVE_VALUES, operative, "operative verified-field values", False),
        (_OTHER_CITATIONS, cited - operative, "citations that are not operative", False),
    )
    problems: list[str] = []
    seen = dict.fromkeys((form[0] for form in forms), 0)
    for source in (SELF, RESULTS, EVIDENCE):
        text = source.read_text(encoding="utf-8")
        for pattern, expected, description, _ in forms:
            for match in pattern.finditer(text):
                seen[pattern] += 1
                if int(match.group(1)) != expected:
                    problems.append(
                        f"{source.name} says {match.group(1)} {description}; "
                        f"the case records say {expected}"
                    )
    problems.extend(
        f"no '{description}' sentence anywhere in "
        f"{SELF.name}, {RESULTS.name} or {EVIDENCE.name} to check"
        for pattern, _, description, required in forms
        if required and not seen[pattern]
    )
    return problems


def prose_counts(found: dict[int, dict]) -> list[str]:
    """Every sentence that quotes the count must quote the corpus, not a memory of it."""
    open_cases = [case for case in found.values() if case.get("status") == "open"]
    nagamochi_open = sum(
        RECORD in ((case.get("verified_lower_bound") or {}).get("evidence") or [])
        for case in open_cases
    )
    corpus = (nagamochi_open, len(open_cases))
    problems: list[str] = []
    match = _README_COUNT.search(README.read_text(encoding="utf-8"))
    if match is None:
        problems.append(
            f"{README.name}: no 'Of the N open cases, **M** have Nagamochi' sentence to check"
        )
    elif (int(match.group(2)), int(match.group(1))) != corpus:
        problems.append(
            f"{README.name} says {match.group(2)} of {match.group(1)} open cases rest on "
            f"Nagamochi; the case records say {corpus[0]} of {corpus[1]}"
        )
    for path in sorted(FRONTIER.glob("n-*.md")):
        problems.extend(
            f"{path.name} says {match.group(1)} of {match.group(2)} open cases; "
            f"the case records say {corpus[0]} of {corpus[1]}"
            for match in _BODY_COUNT.finditer(path.read_text(encoding="utf-8"))
            if (int(match.group(1)), int(match.group(2))) != corpus
        )
    problems.extend(register_prose_counts(found))
    return problems


def main() -> int:
    problems: list[str] = []
    checked = 0
    inversions: list[str] = []
    found = cases()
    prose = prose_counts(found)

    for n, case in sorted(found.items()):
        lower = case.get("verified_lower_bound") or {}
        if RECORD not in (lower.get("evidence") or []):
            continue
        checked += 1

        expected, is_exact = theorem_two(n)
        recorded = Decimal(str(lower["value"]))
        with localcontext() as context:
            context.prec = DIGITS
            # The record may carry fewer digits than the theorem's value has; it must be a
            # correct rendering of it, not merely close, so compare at the record's places.
            # `exponent` is only an int for a finite Decimal, and a bound that is NaN or
            # infinite is a malformed record rather than a disagreement, so say which.
            exponent = recorded.as_tuple().exponent
            if not isinstance(exponent, int):
                problems.append(
                    f"n={n}: recorded lower bound {recorded} is not a finite number"
                )
                continue
            places = -exponent
            if abs(expected - recorded) > Decimal(1).scaleb(-places):
                problems.append(
                    f"n={n}: record says {recorded}, Theorem 2 gives {expected:.{places + 2}f}"
                )
            if is_exact and recorded != recorded.to_integral_value():
                problems.append(f"n={n}: an exact case should carry an integer, not {recorded}")

        reported = case.get("reported_upper_bound") or {}
        if (upper := reported.get("value")) is not None and recorded > Decimal(str(upper)):
            inversions.append(f"n={n}: lower {recorded} exceeds reported upper {upper}")

    if inversions:
        print("SOUNDNESS: a lower bound exceeds the upper bound it sits under:")
        for line in inversions:
            print(f"  {line}")
        return 1
    if problems:
        print(f"{len(problems)} of {checked} Nagamochi-derived bounds disagree with Theorem 2:")
        for line in problems:
            print(f"  {line}")
        return 1

    if prose:
        print(f"{len(prose)} prose count(s) disagree with the case records (D-430):")
        for line in prose:
            print(f"  {line}")
        return 1

    cited, operative = register_counts(found)
    print(
        f"{checked} lower bounds re-derived from Theorem 2, all agreeing, none inverted; "
        f"the README, case-body, citation ({cited}) and operative ({operative}) counts "
        "agree with the records"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
