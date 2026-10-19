#!/usr/bin/env python3
"""Hold each result's derived standing to the bounds its own words state.

Standing is derived and never stored: `render_recent_results.standing` reads it from the
case records, by following evidence ids. An entry holds a case bound where a case
record's bound cites the evidence the entry carries. Where it claims a bound and no case
bound rests on it, it is *superseded*, unless a bound it states is strictly better than
the case record's (`improvements`): then nothing has replaced it, and it is *pending
adoption*. That second step reads this module's numbers; the first never compares one,
so it is only as good as the citations: a case record that cites the wrong entry, or an
entry whose value is still the best on record while another entry is cited for it, would
be labelled wrongly and nothing would say so.

This check comes at it from the other side. It reads the bounds an entry states, from
its headline, or from its claim where the headline states none, as `s(n) ≥ value`,
`s(n) ≤ value` or `s(n) = value`, and holds each against the case record's bound of the
same direction, in both lanes:

- a **superseded** entry is beaten at every case and direction it states: its value is
  strictly worse than the verified bound, and than the reported one. An entry no replay
  has confirmed (`C0` or `C1`) is a report, which can hold the reported lane and never the
  verified one, so it is held to the reported bound alone: `T-046`'s rectangle
  certificates equal verified bounds that their replays (`T-045`, `T-070`) hold, and are
  above others that no replay holds yet. One whose words state no bound this can read is
  held to the weaker structural rule that another entry holds a verified bound at every
  case in its scope;
- an entry **pending adoption** states, at some case, a bound strictly better than the
  case record's in a lane it can hold, and no case bound rests on it: `T-128`'s eight
  rational certificates, below the ceilings `T-125` and others hold, before the case
  records take them in;
- an entry that is the **current best** states, at some case, exactly the verified bound
  (the reported one, where it is the current best as reported), and never more than the
  record carries;
- a **second certificate** states exactly the verified value at every case, and a
  reported one may state exactly the reported value instead where the verified lane does
  not beat it: a report that proves again a value an open case's reported lane holds under
  another entry's citation (`restates`);
- an entry with **no standing**, one whose evidence claims no bound, states none.

An entry that still holds one case of several is not superseded, and this reports the
cases it no longer holds without refusing them: `T-047` holds `n = 26, 29, 30` and is
beaten at `n = 11, 27, 28, 31`.

A simplification or a formalization proves again a value the record holds, so one that
states a bound strictly better than its case's reported one is refused whatever its
standing: no lane holds that value. It moves no bound by itself, so one that a case bound
rests on is refused too, until the register records the kind the owner decides for it
(`second_proof_problems`).

What a table of results draws of a standing is its place on the frontier, `superseded`
or `second certificate`, beside the result's status (`devtools.result_status`); the
"Hide superseded" filter reads the same word. So this check is what holds that mark,
and that filter, to the numbers, for a bound. A result of another kind is marked only
where its entry declares a later result that implies it (`superseded_by`), which
`devtools.check_results` holds to the register instead.

A value written as cut decimals, `3.8100257…`, stands for every number that starts so,
and equals a bound that does. A case record's bound beside a closed form stands for every
number within one unit of its printed value's last place (`render_recent_results.span`),
since that value is a display, cut or rounded. Two lanes are never mixed: a verified
bound is not beaten by a higher reported one, which is what `current best, reported` is
for.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.check_standing [--list]

`--list` prints each entry's standing and where its stated bounds hold or are beaten;
`--cases` adds every stated bound, case by case. `packing-validate --records` runs it.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Mapping, Sequence
from fractions import Fraction
from typing import Any, NamedTuple

from devtools import render_recent_results as view
from devtools.build_bound_citations import own_evidence
from devtools.check_results import SECOND_PROOF_KINDS, kind_label, scope_values

LOWER = "lower"
UPPER = "upper"
#: The two lanes of a case record, each with a bound in each direction.
LANES = ("verified", "reported")
#: What each relation bounds: `=` states both.
DIRECTIONS: Mapping[str, tuple[str, ...]] = {
    "≥": (LOWER,),
    ">": (LOWER,),
    ">=": (LOWER,),
    "≤": (UPPER,),
    "<=": (UPPER,),
    "=": (LOWER, UPPER),
}
CUT = r"(?:…|\.\.\.)"
#: `s(17) ≥ 4613/1000`, `s(27), s(28) ≥ 28/5`, `s(n) ≥ 24/5 = 4.80`, `s(29) ≤ 5.9338…`:
#: a value that is a whole number, a fraction or decimals, and no part of a longer
#: expression such as `2 + 4/√5`.
_PLAIN = re.compile(
    r"s\((?P<n>\d+|n)\)(?P<more>(?:, s\(\d+\))*) (?P<op>>=|<=|≥|≤|>|=) "
    rf"(?P<value>\d+(?:/\d+|\.\d+)?)(?P<cut>{CUT})?"
    r"(?![\d/√(*^]|\.\d| [+*^-]| sqrt)"
    rf"(?: = \d+\.\d+{CUT}?)?"
)
#: `s(11) ≥ 38100√(…)/899996306539 = 3.8100257…`: a closed form, then its decimals.
_CLOSED = re.compile(
    r"s\((?P<n>\d+)\) (?P<op>>=|<=|≥|≤|>|=) [^=`,;]*(?:√|sqrt)[^=`,;]* = "
    rf"(?P<value>\d+\.\d+)(?P<cut>{CUT})?"
)
#: The cases a statement about `s(n)` is for: `` for `n = 26…28` ``, `for n = 17, 18, 19`.
_FOR = re.compile(r"`? for `?n = (?P<cases>\d[\d, …]*(?: and \d+)?)")

BEATEN = "beaten"
#: Confirmation rungs that no replay reached: an entry at one is held in the reported
#: lane alone. The one partition `render_recent_results` also labels a second certificate
#: by, so the lane and the word agree at every rung.
UNREPLAYED = view.UNREPLAYED
EN_DASH = "\u2013"
EQUAL = "equal"
EXCEEDS = "exceeds"
#: The directions each bound kind bounds, the only ones in which it can improve on its
#: case record: a lower bound's words may quote a ceiling, and that is no claim of its. A
#: second proof, a simplification or a formalization, has none of its own; the relations
#: its words state stand in (`directions`).
KIND_DIRECTIONS: Mapping[str, tuple[str, ...]] = {
    "lower-bound": (LOWER,),
    "upper-bound": (UPPER,),
    "optimality": (LOWER, UPPER),
}


class Stated(NamedTuple):
    """A bound an entry states: its value, and how far cut decimals may fall short."""

    value: Fraction
    slack: Fraction


class Finding(NamedTuple):
    """One stated bound against its case record, in each lane; None where the case
    record carries no bound of that direction in that lane."""

    n: int
    direction: str
    stated: Stated
    verified: str | None
    reported: str | None


def compress(cases: Sequence[int]) -> str:
    """`18, 19, 20, 21, 26` as `18-21, 26` (en dash): a run of three or more is a range. The
    site writes its cases the same way (`overview_data.compress`); this check reads the
    record only and does not import the site's data layer for it."""
    runs: list[list[int]] = []
    for n in sorted(cases):
        if runs and n == runs[-1][-1] + 1:
            runs[-1].append(n)
        else:
            runs.append([n])
    return ", ".join(
        f"{run[0]}{EN_DASH}{run[-1]}" if len(run) >= 3 else ", ".join(map(str, run))
        for run in runs
    )


def _cases(text: str) -> set[int]:
    found: set[int] = set()
    for part in re.split(r",| and ", text):
        low, _, high = part.strip().partition("…")
        if low.isdigit():
            found.update(range(int(low), int(high or low) + 1))
    return found


def _stated(value: str, cut: str | None) -> Stated:
    places = len(value.partition(".")[2])
    return Stated(Fraction(value), Fraction(1, 10**places) if cut else Fraction(0))


def statements(text: str, scope: Sequence[int]) -> dict[tuple[int, str], Stated]:
    """The strongest bound `text` states for each case of `scope` and each direction."""
    found: dict[tuple[int, str], Stated] = {}

    def keep(cases: set[int], relation: str, stated: Stated) -> None:
        for n in cases & set(scope):
            for direction in DIRECTIONS[relation]:
                held = found.get((n, direction))
                stronger = held is None or (
                    stated.value > held.value
                    if direction == LOWER
                    else stated.value < held.value
                )
                if stronger:
                    found[(n, direction)] = stated

    for match in _PLAIN.finditer(text):
        if match["n"] == "n":
            named = _FOR.match(text, match.end())
            cases = _cases(named["cases"]) if named else set(scope)
        else:
            cases = {int(match["n"]), *(int(n) for n in re.findall(r"\d+", match["more"]))}
        keep(cases, match["op"], _stated(match["value"], match["cut"]))
    for match in _CLOSED.finditer(text):
        keep({int(match["n"])}, match["op"], _stated(match["value"], match["cut"]))
    return found


def stated_bounds(record: Mapping[str, Any]) -> dict[tuple[int, str], Stated]:
    """The bounds an entry states: its headline's, or its claim's where the headline
    states none. The claim is the fallback and not an addition, since a claim may quote
    a bound that is another entry's."""
    scope = sorted(scope_values(dict(record["scope"])))
    headline = statements(str(record.get("headline") or ""), scope)
    return headline or statements(" ".join(str(record.get("claim") or "").split()), scope)


def relation(stated: Stated, bound: Mapping[str, Any] | None, direction: str) -> str | None:
    """How a stated bound stands against a case record's: beaten by it, equal to it at
    the precision written, or more than it.

    Both sides are sets of numbers, compared exactly: cut decimals are every number from
    `low` up to, and not including, `high`, and the case record's bound is its `span`, a
    single number where it is exact and a unit either side of a closed form's printed
    value. Where the two sets meet, nothing tells them apart and they are equal; beaten
    and more mean every number of one is better than every number of the other."""
    if not bound:
        return None
    floor, ceiling = view.span(bound)
    low, high = stated.value, stated.value + stated.slack
    meets = floor < high and ceiling >= low if stated.slack else floor <= low <= ceiling
    if meets:
        return EQUAL
    if direction == LOWER:
        return BEATEN if floor > low else EXCEEDS
    return BEATEN if ceiling < low else EXCEEDS


def findings(record: Mapping[str, Any], records: view.Records) -> list[Finding]:
    found = []
    for (n, direction), stated in sorted(stated_bounds(record).items()):
        case = records.cases.get(n)
        if case is None:
            continue
        found.append(
            Finding(
                n,
                direction,
                stated,
                relation(stated, case.get(f"verified_{direction}_bound"), direction),
                relation(stated, case.get(f"reported_{direction}_bound"), direction),
            )
        )
    return found


def directions(record: Mapping[str, Any], found: Sequence[Finding]) -> frozenset[str]:
    """The directions in which an entry's stated bounds are claims of its own: those its
    kind bounds (`KIND_DIRECTIONS`), and for a second proof, a simplification or a
    formalization (`SECOND_PROOF_KINDS`), which proves again a result the record holds and
    states that result's relation, every direction its words state. So `s(17) = …` is a
    claim on both sides whether its kind is optimality or a second proof of one, and a
    kind that is no bound claims none."""
    kind = str(record.get("kind"))
    if kind in SECOND_PROOF_KINDS:
        return frozenset(finding.direction for finding in found)
    return frozenset(KIND_DIRECTIONS.get(kind, ()))


def improvements(record: Mapping[str, Any], records: view.Records) -> list[Finding]:
    """The bounds an entry states that are strictly better than its case record's bound of
    the same direction in a lane the entry can hold: the reported lane for a report
    (`UNREPLAYED`), either lane for a replayed result, since two lanes are never mixed.
    Only a direction the entry claims counts (`directions`), and a kind that is no bound
    improves on nothing.

    Each is a bound that nothing on record has replaced, so an entry that holds no case
    bound and states one is pending adoption (`render_recent_results.PENDING_ADOPTION`)
    and not superseded: a simplification or a formalization replayed here before its case
    records adopt the value it proves again is one. A tie is no improvement: the case
    record holds that value under another entry's citation. Compared as `relation`
    compares, by sets of numbers: cut decimals improve on a bound only where every number
    they stand for is better than every number the case record's bound may be."""
    report = str(record.get("confirmation")) in UNREPLAYED
    found = findings(record, records)
    claimed = directions(record, found)
    return [
        finding
        for finding in found
        if finding.direction in claimed
        and (finding.reported == EXCEEDS or (not report and finding.verified == EXCEEDS))
    ]


def restates(record: Mapping[str, Any], records: view.Records) -> bool:
    """Whether an entry states at least one bound and every one equals its case record's
    bound of the same direction in the lane the entry can hold: the verified lane for a
    replayed result, and for a report (`UNREPLAYED`) the reported lane, where the verified
    lane must not beat it either, since a reported value the verified lane has passed is
    replaced whatever the reported lane still carries. A simplification or a formalization
    that holds no bound and restates its case record's value so is a second certificate
    (`render_recent_results.standing`), such as a report that proves again the value an
    open case's reported lane holds under another entry's citation."""
    found = findings(record, records)
    if str(record.get("confirmation")) in UNREPLAYED:
        held = [f.reported == EQUAL and f.verified != BEATEN for f in found]
    else:
        held = [f.verified == EQUAL for f in found]
    return bool(held) and all(held)


def citing(record: Mapping[str, Any], records: view.Records) -> list[int]:
    """The cases in an entry's scope whose bounds, in either lane and direction, cite
    evidence of its own (not the grid's or the area bound's). Read from the evidence ids
    alone, apart from the holders `standing` credits: a case that cites an entry pending
    adoption has taken it in, and the credit has gone to another entry."""
    own = set(own_evidence(record["evidence"], records.register))
    found = []
    for n in sorted(scope_values(dict(record["scope"]))):
        case = records.cases.get(n) or {}
        bounds = [case.get(f"{lane}_{way}_bound") for lane in LANES for way in (LOWER, UPPER)]
        if any(
            own & {str(item) for item in (bound or {}).get("evidence") or []}
            for bound in bounds
        ):
            found.append(n)
    return found


def _at(found: Sequence[Finding]) -> str:
    return "n = " + compress(sorted({finding.n for finding in found}))


def second_proof_problems(
    record: Mapping[str, Any], standing: str, found: Sequence[Finding]
) -> list[str]:
    """What a simplification or a formalization may not be (epistemics.md, Result Kinds).

    - It proves again a value the record holds, so a bound it states strictly better than
      its case's reported one, in a direction it claims (`directions`), is a value no lane
      holds: by the first rule of Result Kinds it takes that value's kind. Replayed, a
      second proof may still beat the verified lane alone, as one whose build lands before
      that of the result it proves again does; that is pending adoption, not this.
    - It moves no bound by itself, so once a case bound rests on it (`HOLDS` or
      `HOLDS_REPORTED`) its kind is revisited: the owner decides what kind it then is, and
      its result page's registered identity is amended with a dated reason
      (`packing/site-urls.yaml`). This refuses until the register records the decision.
    """
    kind = str(record.get("kind"))
    if kind not in SECOND_PROOF_KINDS:
        return []
    entry, label = record["id"], kind_label(kind)
    wrong = []
    claimed = directions(record, found)
    beyond = [f for f in found if f.direction in claimed and f.reported == EXCEEDS]
    if beyond:
        wrong.append(
            f"{entry} is a {label}, yet at {_at(beyond)} it states a bound better than the "
            "reported one: no lane holds that value, so it is no second proof and takes that "
            "value's kind"
        )
    if standing in {view.HOLDS, view.HOLDS_REPORTED}:
        wrong.append(
            f"{entry} is a {label}, yet a case bound rests on it ({standing}), and a second "
            "proof moves no bound by itself: its kind is revisited, as the owner decides, "
            "and its result page's registered identity amended with a dated reason in "
            "packing/site-urls.yaml"
        )
    return wrong


def problems(record: Mapping[str, Any], standing: str, records: view.Records) -> list[str]:
    """What is wrong with `standing` for this entry, by the bounds its words state."""
    entry = str(record["id"])
    found = findings(record, records)
    stands = [f for f in found if f.verified in {EQUAL, EXCEEDS}]
    reported = [f for f in found if f.reported in {EQUAL, EXCEEDS}]
    wrong: list[str] = second_proof_problems(record, standing, found)
    if standing == view.NO_STANDING:
        if found:
            wrong.append(f"{entry} has no standing, yet states a bound at {_at(found)}")
    elif standing == view.SUPERSEDED:
        if str(record.get("confirmation")) in UNREPLAYED:
            # Two lanes are never mixed: a report never holds the verified lane.
            stands = []
        if stands:
            wrong.append(
                f"{entry} is superseded, yet at {_at(stands)} its stated bound is no "
                "worse than the verified one"
            )
        only_reported = [f for f in reported if f not in stands]
        if only_reported:
            wrong.append(
                f"{entry} is superseded, yet at {_at(only_reported)} its stated bound is "
                "no worse than the reported one"
            )
        if not found:
            scope = sorted(scope_values(dict(record["scope"])))
            alone = [
                n
                for n in scope
                if n in records.cases and not view.held(n, records).verified - {entry}
            ]
            if alone:
                wrong.append(
                    f"{entry} is superseded and states no bound this reads, and at n = "
                    f"{compress(alone)} no other entry holds a verified bound"
                )
    elif standing == view.PENDING_ADOPTION:
        # `standing` derives this word from `improvements`, so the first test only holds a
        # standing given from elsewhere to the numbers; the second reads the case records
        # apart from the derivation's holders.
        if not improvements(record, records):
            wrong.append(
                f"{entry} is pending adoption, yet no bound it states is better than the "
                "bound its case record holds"
            )
        if cases := citing(record, records):
            wrong.append(
                f"{entry} is pending adoption, yet a case bound at n = {compress(cases)} "
                "cites its evidence: the record has taken it in"
            )
    elif standing in {view.SECOND_CERTIFICATE, view.SECOND_CERTIFICATE_REPORTED}:
        # A reported second certificate may restate the reported value of an open case,
        # where the verified lane does not beat it (`restates`).
        reported_ok = standing == view.SECOND_CERTIFICATE_REPORTED
        off = [
            f
            for f in found
            if f.verified != EQUAL
            and not (reported_ok and f.reported == EQUAL and f.verified != BEATEN)
        ]
        if off:
            stated = "the verified value"
            if reported_ok:
                stated += ", or a reported one the verified bound does not beat"
            wrong.append(
                f"{entry} is a second certificate, yet at {_at(off)} it does not state {stated}"
            )
    else:
        lane = "reported" if standing == view.HOLDS_REPORTED else "verified"
        placed = [f.reported if lane == "reported" else f.verified for f in found]
        over = [f for f, where in zip(found, placed, strict=True) if where == EXCEEDS]
        if over:
            wrong.append(
                f"{entry} states more than the {lane} bound its case record carries at "
                f"{_at(over)}"
            )
        if found and all(where == BEATEN for where in placed):
            wrong.append(
                f"{entry} is {standing}, yet every bound it states is beaten in the "
                f"{lane} lane: it reads as superseded"
            )
    return wrong


def summary(record: Mapping[str, Any], standing: str, records: view.Records) -> str:
    """One line for an entry: its standing, and where its stated bounds still hold."""
    found = findings(record, records)
    reported = standing == view.HOLDS_REPORTED or (
        standing == view.SECOND_CERTIFICATE_REPORTED and restates(record, records)
    )
    lane = "reported" if reported else "verified"
    holds = [f for f in found if (f.reported if lane == "reported" else f.verified) == EQUAL]
    better = improvements(record, records) if standing == view.PENDING_ADOPTION else []
    beaten = [f for f in found if f.verified == BEATEN and f not in holds]
    name = standing or f"({kind_label(str(record['kind']))})"
    parts = [f"{record['id']}  {name:<28s}"]
    if not found:
        parts.append("states no bound this reads")
    if better:
        parts.append(f"better than the case record at {_at(better)}")
    if holds:
        parts.append(f"equals the {lane} bound at {_at(holds)}")
    if beaten:
        parts.append(f"beaten at {_at(beaten)}")
    return "  ".join(parts)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="check_standing",
        description="Hold each result's derived standing to the bounds its words state.",
    )
    parser.add_argument(
        "--list", action="store_true", help="print each entry's standing and where it holds"
    )
    parser.add_argument(
        "--cases", action="store_true", help="also print every stated bound, case by case"
    )
    arguments = parser.parse_args(argv)
    records = view.load_records()
    wrong: list[str] = []
    read = 0
    for record in records.register.results:
        standing = view.standing(record, records)
        read += bool(stated_bounds(record))
        if arguments.list or arguments.cases:
            print(summary(record, standing, records))
        if arguments.cases:
            for finding in findings(record, records):
                print(
                    f"    n = {finding.n} {finding.direction} {finding.stated.value}"
                    f"{'…' if finding.stated.slack else ''}: verified {finding.verified}, "
                    f"reported {finding.reported}"
                )
        wrong.extend(problems(record, standing, records))
    total = len(records.register.results)
    if wrong:
        for line in wrong:
            print(f"FAIL  {line}", file=sys.stderr)
        print(
            f"{len(wrong)} standing(s) of {total} disagree with a stated bound", file=sys.stderr
        )
        return 1
    print(
        f"OK: {total} results, each standing agrees with the bounds the entry states; "
        f"{read} state a bound this reads"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
