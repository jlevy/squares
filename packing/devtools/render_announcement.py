"""Render an intake pass's new results as an announcement: one short line per result.

The owner announces new results from this (2026-10-11): a header with the date and a
count, then one brief line per register entry, at most `BRIEF_LIMIT` characters before
its link, crediting the result's finders by their X handles where the record has
evidence of one and by name otherwise:

    s(267) ≤ 16.83882, new best known (verified): Francisco Couzo https://…#t-134

Agents render it into the intake pull request's description; only the owner posts it
(`campaign/result-import.md`, Running an Intake Pass). Every fact on a line is read
from the record, and the wording is chosen not to overstate it:

- **The bound.** The bounds an entry states, as `devtools.check_standing` reads them
  from its headline or claim, are held at each count against every other bound on record
  there: the case record's, in both lanes, and every other entry's. An upper bound is
  printed rounded up and a lower bound rounded down, so the printed number is itself a
  true bound, to as many places as it takes to stay strictly better than the previous
  best. An entry that states no bound but holds its case's bound prints that bound. A
  line about several counts prints each bound where they are at most `LISTED_COUNTS`
  and the line stays within `BRIEF_LIMIT`; otherwise it elides them, and past
  `LISTED_COUNTS` gives how many counts and their range.
- **New best known**, or **new best lower bound**: said only at the counts where
  nothing on record is as good: the case record holds this entry's bound or a worse one,
  and no other entry states a better bound, or an equal one registered first. That is
  the case's house, or an entry pending adoption that is still below every other. A
  regularization of the entry's own packing (`regularizations`) is the same packing and
  does not count against it, as another entry or as the case record it holds; where its
  side is the smaller, the line elides the entry's number there. `--margins` adds how
  far the bound passes the best one on record before the entry was registered, cut to
  two significant figures; the previous holder is never named, so a line never credits a
  bound to the wrong person.
- **(verified)** at `V3` and above, and **(reported)** below, which is never called
  verified. The rungs, and which code confirmed the result, are on its row, which the
  line links.
- **Credit.** The result's finders: the names before `after` in the register's credit
  line (`result_credit.credit_line`), each by its full name where the bibliography's
  `credited_names` or a contributor profile gives one, and whose packing it refines or
  regularizes, as its `regularizations` say, or its headline (`refinements of Ryan Xu's
  packings`) and, where that names a request rather than a person, the entry its claim
  names (`refined`). `--lineage` adds the names after `after`. The project's owner
  (`result_credit.PROJECT_AUTHOR`) is never credited or tagged: the announcement is the
  owner's own post, and `after Levy` is this project's lineage, not a finding.

The results are selected by `--ids`, or by `--since`, the date the register received
them (`registered`, the field an intake pass sets), and by `--min-significance`, 3 by
default. A selected bound that is the best known at no count, because it is superseded
or a later entry betters it everywhere, is left out unless `--all` keeps it, at
`PLACES` decimals with what betters, equals or supersedes it: up to `SINCE_NAMED` by
name, else how many. stderr says why each result was left out.

A handle comes only from evidence, in this order, and never from a user name:

1. a contributor profile, `contributors/*.md`, whose names include the credited name
   and whose `links` include one of kind `twitter`;
2. with `--github`, the `twitter_username` a GitHub account declares on its profile,
   read through `gh api users/<login>` and stored nowhere. The account is tied to the
   credited name by a contributor profile's `github` link; by the bibliography's
   `credited_names`, as `Full Name (login)` or by the full name the profile declares; by
   a login that is itself the credited name; or by issues in
   `campaign/result-requests.yaml` whose every mapped result credits that one person
   first. The requests record's owner is never a candidate;
3. a handle the record states with its source (`RECORD_HANDLES`), which is checked
   against the file that states it.

stderr says where each handle came from, and which credited names have none.

The owner announces from it as they choose. Each line is held to `POST_LIMIT` on its
own, so that a thread of one line a post fits, and stderr says whether the whole
announcement also fits one post (`block_fit`).

Usage, from `packing/`, selecting an intake pass's own results by id, since `--since`
also picks up what other passes registered that day:
    uv run --frozen --all-extras --group dev python -m devtools.render_announcement \\
        --ids T-147 T-148 [--github] [--min-significance 3] [--all] [--lineage] \\
        [--margins] [--date YYYY-MM-DD]
    uv run --frozen --all-extras --group dev python -m devtools.render_announcement \\
        --since 2026-10-11 [--github]
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field, replace
from datetime import UTC, date, datetime
from fractions import Fraction
from pathlib import Path
from typing import Any, NamedTuple
from urllib.parse import urlsplit

from devtools.check_results import scope_values
from devtools.check_standing import (
    EN_DASH,
    KIND_DIRECTIONS,
    LOWER,
    UPPER,
    Stated,
    compress,
    stated_bounds,
)
from devtools.render_overview import RESULTS_PAGE, SITE_URL
from devtools.render_recent_results import (
    ELLIPSIS,
    SUPERSEDED,
    Records,
    lane_holders,
    listed,
    load_records,
    span,
    standing,
    superseding,
)
from devtools.result_credit import PROJECT_AUTHOR, credit_line
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
REQUESTS = ROOT / "campaign" / "result-requests.yaml"
BIBLIOGRAPHY = ROOT / "resources" / "bibliography.yaml"
#: Contributor profiles, one Markdown file a person (draft jlevy/squares#490); read when
#: present.
CONTRIBUTORS = ROOT / "contributors"

#: The fewest decimal places a bound is printed to, and the most.
PLACES = 5
MAX_PLACES = 40
#: The significance a result needs by default to be announced (epistemics.md, Significance).
MIN_SIGNIFICANCE = 3
#: The verification rung from which a line says "verified".
VERIFIED_FROM = 3
BOUND_KINDS = frozenset({"lower-bound", "upper-bound"})
RELATIONS = {(UPPER, False): "≤", (UPPER, True): "<", (LOWER, False): "≥", (LOWER, True): ">"}
MONTHS = (
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
)
#: A GitHub login, checked before it is put into an API path.
LOGIN = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$")
#: A `credited_names` key that carries its person's login: `Nate Chaoweeraprasit (itsnaka)`.
NAMED_LOGIN = re.compile(r"^(.+) \(([A-Za-z0-9-]+)\)$")
#: A headline's own words for whose packings an entry refines, and whether it says one
#: or several: `refinement of Ryan Xu's packing`, `refining Ryan Xu's packing`,
#: `refinements of SQUISH's Mondrian packings`.
REFINED = re.compile(
    r"\brefin(?:ements? of|ing) ((?:[A-Z][\w.-]*\s)*[A-Z][\w.-]*)['\u2019]s "
    r"(?:[\w-]+ ){0,3}(packings?)\b"
)
#: A register id, as a claim names another entry.
RESULT_ID = re.compile(r"\bT-\d{3}\b")
#: What a line says a bound is, where it is the best on record.
NEWS = {UPPER: "new best known", LOWER: "new best lower bound"}
#: The most characters a line holds before its link (the owner, 2026-10-11).
BRIEF_LIMIT = 140
#: The separators of a credit line: sources, `after`, names. A credited name never holds one.
SEPARATORS = re.compile(r"(; | after |, | and )")
ET_AL = " et al."
#: The most counts a line lists one by one; past it, a line gives how many and the range.
LISTED_COUNTS = 6
#: The most results or case records a `since` clause names; past it, it says how many.
SINCE_NAMED = 3
#: How a rival that is a case record, with no register entry under it, is labelled.
CASE_LABEL = re.compile(r"^the n = \d+ case record$")
#: X's limit on a post, how long it counts any link, and the code point ranges it counts
#: once (twitter-text, version 3); every other character counts twice.
POST_LIMIT = 280
URL_LENGTH = 23
LIGHT_RANGES = ((0, 4351), (8192, 8205), (8208, 8223), (8242, 8247))


@dataclass(frozen=True)
class RecordHandle:
    """An X handle the record states for a credited name, with the file and words that
    state it: `quote`, its whitespace collapsed, must appear in `path`."""

    name: str
    handle: str
    path: str
    quote: str


#: The handles the record itself states with their source. Each is checked against its
#: file before use (`record_handles`), so a reworded record fails loudly, not silently.
RECORD_HANDLES: tuple[RecordHandle, ...] = (
    RecordHandle(
        name="Ahmed",
        handle="ManassehA06",
        path="packing/frontier/n-011.md",
        quote="whose author, Ahmed, posts on X as [@ManassehA06]",
    ),
)


class Handle(NamedTuple):
    """A credited name's X handle and where it came from."""

    name: str
    handle: str
    source: str


# ---------------------------------------------------------------------------------------
# Numbers


@dataclass(frozen=True)
class Span:
    """A bound as numbers: from `low` to `high`, with `high` itself excluded where the
    bound is cut decimals (`Stated.slack`), which stand for every number that starts so."""

    low: Fraction
    high: Fraction
    open_high: bool = False

    @classmethod
    def of_stated(cls, stated: Stated) -> Span:
        return cls(stated.value, stated.value + stated.slack, bool(stated.slack))

    @classmethod
    def of_case(cls, bound: Mapping[str, Any]) -> Span:
        low, high = span(bound)
        return cls(low, high)


def better(a: Span, b: Span, direction: str) -> bool:
    """Whether every number `a` may be is a strictly better bound than every number `b`
    may be: smaller for an upper bound, larger for a lower one."""
    if direction == UPPER:
        return a.high < b.low or (a.high == b.low and a.open_high)
    return a.low > b.high or (a.low == b.high and b.open_high)


def _ceil(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


def _floor(value: Fraction) -> int:
    return value.numerator // value.denominator


def _decimal(scaled: int, places: int) -> str:
    sign = "-" if scaled < 0 else ""
    whole, part = divmod(abs(scaled), 10**places)
    digits = f"{part:0{places}d}".rstrip("0") if places else ""
    return f"{sign}{whole}.{digits}" if digits else f"{sign}{whole}"


def shown(bound: Span, direction: str, previous: Span | None = None) -> str:
    """The bound as a line prints it: an upper bound rounded up and a lower bound rounded
    down, so the printed number is a true bound itself, at `PLACES` decimals, or more
    until it is still strictly better than `previous` where it is. A bound that only ties
    or trails `previous` no number of places makes better, so it is printed at `PLACES`.
    Exact where it ends sooner."""
    edge = bound.high if direction == UPPER else bound.low
    target = None
    if previous is not None and (
        previous.low > bound.high if direction == UPPER else bound.low > previous.high
    ):
        target = previous
    scaled, places = 0, PLACES
    for places in range(PLACES, (PLACES if target is None else MAX_PLACES) + 1):
        scale = 10**places
        scaled = _ceil(edge * scale) if direction == UPPER else _floor(edge * scale)
        printed = Fraction(scaled, scale)
        if target is None or better(Span(printed, printed), target, direction):
            break
    return _decimal(scaled, places)


def margin_text(margin: Fraction) -> str:
    """A positive margin to two significant figures, cut rather than rounded so it never
    claims more than the record holds: `1.0e-2`, `6.6e-4`."""
    exponent = 0
    while margin >= Fraction(10) ** (exponent + 1):
        exponent += 1
    while margin < Fraction(10) ** exponent:
        exponent -= 1
    tenths = _floor(margin * 10 / Fraction(10) ** exponent)
    return f"{tenths // 10}.{tenths % 10}e{exponent}"


# ---------------------------------------------------------------------------------------
# Standing at each count


class Rival(NamedTuple):
    """Another bound on record at one count and direction: a case record's, in one lane,
    or another entry's. `earlier` where it was on record before the entry was registered."""

    label: str
    bound: Span
    earlier: bool


@dataclass(frozen=True)
class Count:
    """One bound an entry states, and how it stands against everything else on record."""

    n: int
    direction: str
    bound: Span
    bettered_by: tuple[str, ...] = ()
    tied_with: tuple[str, ...] = ()
    previous: Span | None = None
    regularized_by: tuple[str, ...] = ()
    """Regularizations of the entry's own packing whose bound here is strictly better.
    They take nothing from it, but a line does not print a number they better."""

    @property
    def best(self) -> bool:
        """Nothing on record betters it, and nothing registered earlier equals it."""
        return not self.bettered_by and not self.tied_with

    @property
    def margin(self) -> Fraction | None:
        """How far it passes the best bound on record before it, at the least."""
        if self.previous is None:
            return None
        if self.direction == UPPER:
            gap = self.previous.low - self.bound.high
        else:
            gap = self.bound.low - self.previous.high
        return gap if gap > 0 else None


def assess(n: int, direction: str, bound: Span, rivals: Iterable[Rival]) -> Count:
    """How `bound` stands at `n` against `rivals`: what betters it, what earlier bound it
    only equals, and the best bound on record before it."""
    bettered: list[str] = []
    tied: list[str] = []
    before: list[Span] = []
    for rival in rivals:
        if better(rival.bound, bound, direction):
            bettered.append(rival.label)
        elif rival.earlier and not better(bound, rival.bound, direction):
            tied.append(rival.label)
        if rival.earlier:
            before.append(rival.bound)
    previous = None
    if before:
        if direction == UPPER:
            previous = min(before, key=lambda item: item.low)
        else:
            previous = max(before, key=lambda item: item.high)
    return Count(
        n,
        direction,
        bound,
        tuple(dict.fromkeys(bettered)),
        tuple(dict.fromkeys(tied)),
        previous,
    )


def _key(record: Mapping[str, Any]) -> tuple[str, int]:
    return str(record["registered"]), int(str(record["id"])[2:])


def rival_bounds(records: Records) -> dict[tuple[int, str], list[tuple[str, Span]]]:
    """Every bound each register entry states, by count and direction, in the directions
    its kind bounds (`check_standing.KIND_DIRECTIONS`)."""
    index: dict[tuple[int, str], list[tuple[str, Span]]] = {}
    for record in records.register.results:
        directions = KIND_DIRECTIONS.get(str(record["kind"]), ())
        for (n, direction), stated in stated_bounds(record).items():
            if direction in directions:
                index.setdefault((n, direction), []).append(
                    (str(record["id"]), Span.of_stated(stated))
                )
    return index


def own_bounds(record: Mapping[str, Any], records: Records) -> dict[tuple[int, str], Span]:
    """The bounds an entry states in the directions its kind bounds, and where it states
    none at a count, the case record's bound there that rests on it."""
    entry = str(record["id"])
    directions = KIND_DIRECTIONS.get(str(record["kind"]), ())
    found = {
        key: Span.of_stated(stated)
        for key, stated in stated_bounds(record).items()
        if key[1] in directions
    }
    for n in sorted(scope_values(dict(record["scope"]))):
        case = records.cases.get(n)
        if case is None:
            continue
        for direction in directions:
            if (n, direction) in found:
                continue
            for lane in ("verified", "reported"):
                held = case.get(f"{lane}_{direction}_bound")
                if held and entry in lane_holders(n, records, direction, [lane]):
                    found[(n, direction)] = Span.of_case(held)
                    break
    return found


def counts(
    record: Mapping[str, Any],
    records: Records,
    index: Mapping[tuple[int, str], Sequence[tuple[str, Span]]],
) -> list[Count]:
    """Each bound the entry states, held against the case record and every other entry.
    A regularization of the entry's own packing (`regularizes`) is no rival, whether as
    another entry or as the case record it holds."""
    entry, key = str(record["id"]), _key(record)
    assessed: list[Count] = []
    for (n, direction), bound in sorted(own_bounds(record, records).items()):
        rivals: list[Rival] = []
        regularized: list[str] = []
        case = records.cases.get(n) or {}
        for lane in ("verified", "reported"):
            held = case.get(f"{lane}_{direction}_bound")
            if not held or entry in (holders := lane_holders(n, records, direction, [lane])):
                continue
            label = ", ".join(sorted(holders)) or f"the n = {n} case record"
            if holders and all(regularizes(records.results[h], n, entry) for h in holders):
                if better(Span.of_case(held), bound, direction):
                    regularized.append(label)
                continue
            earlier = not holders or any(
                _key(records.results[holder]) < key for holder in holders
            )
            rivals.append(Rival(label, Span.of_case(held), earlier))
        for other, stated in index.get((n, direction), ()):
            if other == entry:
                continue
            if regularizes(records.results[other], n, entry):
                if better(stated, bound, direction):
                    regularized.append(other)
                continue
            rivals.append(Rival(other, stated, _key(records.results[other]) < key))
        count = assess(n, direction, bound, rivals)
        assessed.append(replace(count, regularized_by=tuple(dict.fromkeys(regularized))))
    return assessed


def regularizes(record: Mapping[str, Any], n: int, entry: str) -> bool:
    """Whether `record`'s certificate at `n` is a regularization of `entry`'s packing
    (`regularizations`): the same packing, so it does not better the packing's finder."""
    return any(
        int(item["n"]) == n and str(item["of"]) == entry
        for item in record.get("regularizations") or ()
    )


# ---------------------------------------------------------------------------------------
# Credit and handles


def credit_text(record: Mapping[str, Any], sources: Mapping[str, Mapping[str, Any]]) -> str:
    """The result's credit line as the register prints it, unescaped."""
    return credit_line(record, sources).replace(r"\|", "|")


def credit_parts(credit: str) -> tuple[list[str], list[str]]:
    """A credit line's finders, before `after`, and the lineage after it, each in the
    register's order and once: `Ahmed et al. after Levy, Daniel` is `Ahmed et al.`, then
    Levy and Daniel."""
    finders: list[str] = []
    lineage: list[str] = []
    for line in credit.split("; "):
        first, _, rest = line.partition(" after ")
        finders.extend(SEPARATORS.split(first)[::2])
        if rest:
            lineage.extend(SEPARATORS.split(rest)[::2])
    return list(dict.fromkeys(finders)), list(dict.fromkeys(lineage))


def primary_names(credit: str) -> list[str]:
    """The names a credit line credits first, before `after`, from each source's line."""
    return credit_parts(credit)[0]


def _bare(token: str) -> str:
    return token.removesuffix(ET_AL)


def people(tokens: Iterable[str]) -> list[str]:
    """Credit tokens less the project's owner, whom an announcement never credits: it is
    the owner's own post, and `after Levy` is this project's lineage, not a finding."""
    return [token for token in tokens if token and _bare(token) != PROJECT_AUTHOR]


@dataclass(frozen=True)
class Names:
    """How a line names a credited person: by an X handle where the evidence gives one,
    else by the full name the bibliography's `credited_names` or a contributor profile
    prints for the credited name, else as the register credits them."""

    handles: Mapping[str, Handle] = field(default_factory=dict[str, Handle])
    full: Mapping[str, str] = field(default_factory=dict[str, str])

    def show(self, token: str) -> str:
        name = _bare(token)
        suffix = token[len(name) :]
        if name in self.handles:
            return f"@{self.handles[name].handle}{suffix}"
        return self.full.get(name, name) + suffix


def full_names(credited: Mapping[str, str], profiles: Sequence[Profile] = ()) -> dict[str, str]:
    """Each credited name's full name, where the record gives exactly one: the
    bibliography's `credited_names` (`Francisco Couzo: Couzo`, a login in parentheses
    dropped), then a contributor profile's `real_name`."""
    found: dict[str, set[str]] = {}
    for full, name in credited.items():
        match = NAMED_LOGIN.match(full)
        found.setdefault(name, set()).add(match.group(1) if match else full)
    for profile in profiles:
        if profile.real_name:
            for name in profile.names:
                if name not in credited.values():
                    found.setdefault(name, set()).add(profile.real_name)
    return {name: next(iter(fulls)) for name, fulls in found.items() if len(fulls) == 1}


def frontmatter(text: str) -> str:
    """The YAML between a Markdown file's opening `---` lines, or nothing."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return ""
    for end, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "\n".join(lines[1:end])
    return ""


def _x_handle(link: Mapping[str, Any]) -> str | None:
    handle = link.get("handle")
    if handle:
        return str(handle).removeprefix("@")
    parsed = urlsplit(str(link.get("url", "")))
    path = parsed.path.strip("/")
    if parsed.hostname in {"x.com", "twitter.com", "www.x.com", "www.twitter.com"} and path:
        return path.split("/")[0]
    return None


@dataclass(frozen=True)
class Profile:
    """A contributor profile: the names it answers to, its real name where it gives one,
    its GitHub logins and X handles."""

    id: str
    path: str
    names: frozenset[str]
    github: tuple[str, ...] = ()
    twitter: tuple[str, ...] = ()
    real_name: str = ""


def load_profiles(directory: Path = CONTRIBUTORS) -> list[Profile]:
    """Every contributor profile in `directory`, which is absent before jlevy/squares#490."""
    if not directory.is_dir():
        return []
    profiles = []
    for path in sorted(directory.glob("*.md")):
        data = safe_load(frontmatter(path.read_text(encoding="utf-8"))) or {}
        person = data.get("contributor") if isinstance(data, Mapping) else None
        if not isinstance(person, Mapping):
            continue
        names = {str(person.get(key)) for key in ("id", "display_name", "real_name")}
        names.update(str(alias) for alias in person.get("aliases") or ())
        links = [link for link in person.get("links") or () if isinstance(link, Mapping)]
        github = [
            str(link.get("handle") or urlsplit(str(link["url"])).path.strip("/"))
            for link in links
            if link.get("kind") == "github"
        ]
        twitter = [
            h for link in links if link.get("kind") == "twitter" if (h := _x_handle(link))
        ]
        profiles.append(
            Profile(
                id=str(person["id"]),
                path=_relative(path),
                names=frozenset(name for name in names if name and name != "None"),
                github=tuple(github),
                twitter=tuple(twitter),
                real_name=str(person.get("real_name") or ""),
            )
        )
    return profiles


def _relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO).as_posix()
    except ValueError:
        return path.as_posix()


def record_handles(
    table: Sequence[RecordHandle] = RECORD_HANDLES, repo: Path = REPO
) -> dict[str, Handle]:
    """The handles the record states, each checked against the words of its file."""
    found: dict[str, Handle] = {}
    for item in table:
        text = " ".join((repo / item.path).read_text(encoding="utf-8").split())
        if item.quote not in text or f"@{item.handle}" not in item.quote:
            raise SystemExit(
                f"{item.path} no longer says {item.quote!r}: re-read the record before "
                f"using @{item.handle} for {item.name}"
            )
        found[item.name] = Handle(item.name, item.handle, f"{item.path}: “{item.quote}”")
    return found


Fetch = Callable[[str], Mapping[str, Any] | None]


def gh_user(login: str) -> Mapping[str, Any] | None:
    """A GitHub account's public profile through `gh api`, or None where it cannot be read."""
    shown_ = subprocess.run(
        ("gh", "api", f"users/{login}"), capture_output=True, text=True, check=False
    )
    if shown_.returncode:
        print(
            f"could not read GitHub profile {login}: {shown_.stderr.strip()}", file=sys.stderr
        )
        return None
    profile = json.loads(shown_.stdout)
    return profile if isinstance(profile, Mapping) else None


@dataclass
class GitHub:
    """What ties a GitHub login to a credited name, and the profiles read for it."""

    owner: str
    issues: Sequence[Mapping[str, Any]]
    credited_names: Mapping[str, str]
    primaries: Mapping[str, list[str]]
    """Each result id's first-credited names (`primary_names`)."""
    fetch: Fetch = gh_user
    read: dict[str, Mapping[str, Any] | None] = field(
        default_factory=dict[str, Mapping[str, Any] | None]
    )

    def profile(self, login: str) -> Mapping[str, Any] | None:
        if not LOGIN.match(login):
            return None
        if login not in self.read:
            self.read[login] = self.fetch(login)
        return self.read[login]

    def candidates(self) -> list[str]:
        """The logins the requests record knows, every issue's author, less its owner,
        whom an announcement never credits."""
        logins = (str(issue["author"]) for issue in self.issues)
        return list(dict.fromkeys(login for login in logins if login and login != self.owner))

    def by_issue(self) -> dict[str, tuple[str, list[int]]]:
        """Logins tied to one person by their issues: each issue whose every mapped result
        credits that one person first. The owner, who files for others, is never tied so."""
        found: dict[str, dict[str, list[int]]] = {}
        for issue in self.issues:
            login = str(issue["author"])
            ids = [
                str(entry)
                for result in issue.get("results") or ()
                for entry in result.get("register") or ()
            ]
            firsts = {tuple(self.primaries.get(entry, ())) for entry in ids}
            if login == self.owner or not ids or len(firsts) != 1:
                continue
            (first,) = firsts
            if len(first) == 1:
                found.setdefault(login, {}).setdefault(first[0], []).append(
                    int(issue["number"])
                )
        return {
            login: next(iter(names.items()))
            for login, names in found.items()
            if len(names) == 1
        }

    def logins(self, name: str, profiles: Sequence[Profile]) -> tuple[list[str], str]:
        """The logins tied to `name` by the first rule that ties any, and how; the rules
        run strongest first, and the ones that read profiles last."""
        rules: tuple[Callable[[], tuple[list[str], str]], ...] = (
            lambda: (
                [login for p in profiles if name in p.names for login in p.github],
                "its contributor profile's github link",
            ),
            lambda: (
                [
                    match.group(2)
                    for full, surname in self.credited_names.items()
                    if surname == name and (match := NAMED_LOGIN.match(full))
                ],
                "bibliography credited_names",
            ),
            lambda: (
                [login for login in self.candidates() if login.casefold() == name.casefold()],
                "a login that is the credited name",
            ),
            lambda: (
                [login for login in self.candidates() if self.declares(login, name)],
                "the name its GitHub profile declares, as bibliography credited_names maps it",
            ),
            lambda: self.by_issues(name),
        )
        for rule in rules:
            tied, how = rule()
            if tied:
                return tied, how
        return [], ""

    def declares(self, login: str, name: str) -> bool:
        """Whether `login`'s GitHub profile declares `name`, or a full name that the
        bibliography's `credited_names` credits as `name`."""
        declared = str((self.profile(login) or {}).get("name") or "")
        return bool(declared) and (
            declared == name or self.credited_names.get(declared) == name
        )

    def by_issues(self, name: str) -> tuple[list[str], str]:
        """The logins tied to `name` by their issues (`by_issue`), and which issues."""
        tied = [
            (login, numbers)
            for login, (person, numbers) in self.by_issue().items()
            if person == name
        ]
        issues = ", ".join(f"#{n}" for _, numbers in tied for n in numbers)
        how = f"author of {issues}, whose every mapped result credits {name} first"
        return [login for login, _ in tied], how


def resolve_handles(
    names: Iterable[str],
    profiles: Sequence[Profile],
    github: GitHub | None,
    stated: Mapping[str, Handle],
) -> tuple[dict[str, Handle], list[str]]:
    """Each credited name's handle from the evidence, in the module docstring's order,
    and the warnings met on the way: a name tied to two handles gets none, and the
    project's owner none at all."""
    handles: dict[str, Handle] = {}
    warnings: list[str] = []
    for name in dict.fromkeys(people(names)):
        matched = [p for p in profiles if name in p.names]
        found = sorted({h for p in matched for h in p.twitter})
        if len(found) == 1:
            sources = ", ".join(p.path for p in matched if p.twitter)
            handles[name] = Handle(name, found[0], f"{sources} (links kind twitter)")
            continue
        if len(found) > 1:
            warnings.append(f"{name}: contributor profiles give {found}; no handle used")
            continue
        if github is not None:
            logins, how = github.logins(name, profiles)
            declared = sorted(
                {
                    str(twitter)
                    for login in dict.fromkeys(logins)
                    if (twitter := (github.profile(login) or {}).get("twitter_username"))
                }
            )
            if len(declared) == 1:
                tied = ", ".join(dict.fromkeys(logins))
                handles[name] = Handle(
                    name,
                    declared[0],
                    f"GitHub profile of {tied} (twitter_username), tied to {name} by {how}",
                )
                continue
            if len(declared) > 1:
                warnings.append(f"{name}: GitHub profiles declare {declared}; no handle used")
                continue
        if name in stated:
            handles[name] = stated[name]
    return handles, warnings


# ---------------------------------------------------------------------------------------
# Lines


def _strict(record: Mapping[str, Any], direction: str) -> bool:
    """Whether the entry's words state its bound strictly (`s(40) > …`): the headline's
    where it states a bound, else the claim's, as `check_standing.stated_bounds` reads."""
    strict = r"<(?![=])" if direction == UPPER else r">(?![=])"
    pattern = re.compile(rf"s\((?:\d+|n)\)(?:, s\(\d+\))* {strict}")
    headline = str(record.get("headline") or "")
    text = (
        headline if re.search(r"s\((?:\d+|n)\)", headline) else str(record.get("claim") or "")
    )
    return bool(pattern.search(" ".join(text.split())))


def verified(record: Mapping[str, Any]) -> bool:
    return int(str(record["verification"])[1:]) >= VERIFIED_FROM


def tag(record: Mapping[str, Any]) -> str:
    """How far the result is checked, in a word: verified at `V3` and above, reported,
    and not yet verified, below."""
    return "(verified)" if verified(record) else "(reported)"


def result_link(result_id: str) -> str:
    return f"{SITE_URL}{RESULTS_PAGE}#{result_id.lower()}"


def margins(group: Sequence[Count]) -> str:
    """How far the bounds in `group` pass the previous bests, as one margin or a range;
    empty unless every bound in it has one."""
    texts = [margin_text(m) for c in group if (m := c.margin) is not None]
    if not texts or len(texts) < len(group):
        return ""
    ordered = sorted(set(texts), key=float)
    way = "below" if group[0].direction == UPPER else "above"
    best = "best" if len(group) == 1 else "bests"
    gap = ordered[0] if len(ordered) == 1 else f"{ordered[0]} to {ordered[-1]}"
    return f"{gap} {way} the previous {best}"


def statement(record: Mapping[str, Any], group: Sequence[Count], *, each: bool = True) -> str:
    """What the line says is bounded: one bound, one bound at several counts, with `each`
    each bound at up to `LISTED_COUNTS` counts (`s(155) ≤ 12.95243, s(156) ≤ 12.97918`),
    or the counts alone, their bounds elided (`s(n) ≤ … at n = 108, 127`). A bound that a
    regularization of the same packing betters is elided, since a smaller number than
    the entry's own is on record there."""
    direction = group[0].direction
    relation = RELATIONS[(direction, _strict(record, direction))]
    printed = {
        c.n: ELLIPSIS if c.regularized_by else shown(c.bound, direction, c.previous)
        for c in group
    }
    values = set(printed.values())
    if len(group) == 1:
        return f"s({group[0].n}) {relation} {values.pop()}"
    found = sorted(printed)
    if each and len(values) > 1 and ELLIPSIS not in values and len(found) <= LISTED_COUNTS:
        return ", ".join(f"s({n}) {relation} {printed[n]}" for n in found)
    cases = f"n = {compress(found)}"
    if len(found) > LISTED_COUNTS:
        cases = f"{len(found)} counts, n = {found[0]}{EN_DASH}{found[-1]}"
    value = values.pop() if len(values) == 1 else ELLIPSIS
    return f"s(n) {relation} {value} at {cases}"


def posted_length(line: str) -> int:
    """A line's length as X counts it (twitter-text, version 3): a link is 23, a character
    in its light ranges 1, and any other character 2, so `≤` and `≥` count twice."""
    length = 0
    for word in line.split(" "):
        if word.startswith(("https://", "http://")):
            length += URL_LENGTH
        else:
            length += sum(1 if _light(ord(char)) else 2 for char in word)
    return length + line.count(" ")


def _light(code: int) -> bool:
    return any(low <= code <= high for low, high in LIGHT_RANGES)


class Line(NamedTuple):
    """One announced result, or why it was left out."""

    id: str
    text: str
    left_out: str = ""


def plain(text: str) -> str:
    return text.replace("`", "")


def regularized(
    record: Mapping[str, Any],
    group: Sequence[Count],
    records: Records,
) -> list[str]:
    """Whose packings the entry's certificates at the counts in `group` regularize: the
    names those packings' own results credit first."""
    at = {c.n for c in group}
    names: list[str] = []
    for item in record.get("regularizations") or ():
        if int(item["n"]) in at:
            names.extend(
                primary_names(credit_text(records.results[str(item["of"])], records.sources))
            )
    return people(dict.fromkeys(names))


class Refinement(NamedTuple):
    """Whose packings an entry refines: each person as a credit token, with the words its
    headline names them by where it names them (`Ryan Xu`), and whether it says several."""

    people: tuple[tuple[str, str], ...]
    plural: bool


def refined(
    record: Mapping[str, Any], records: Records, at: Iterable[int] | None = None
) -> Refinement | None:
    """Whose packings the entry refines at the counts `at`, by default all its own, as its
    headline says: the person it names (`refinement of Ryan Xu's packing`) where its
    credit line credits them; else, where it names a request or a project (`refinements
    of SQUISH's Mondrian packings`), the first-credited of the entry its claim names first,
    at each count, among those whose headline names it too and whose scope holds the count
    (T-152's claim names T-151's). Only a person this entry's credit line credits is
    named; where none is, nothing."""
    match = REFINED.search(plain(str(record.get("headline") or "")))
    if match is None:
        return None
    owner, plural = match.group(1), match.group(2) == "packings"
    finders, lineage = credit_parts(credit_text(record, records.sources))
    credited = {_bare(token) for token in (*finders, *lineage)}
    if owner.split()[-1] in credited:
        return Refinement(((owner.split()[-1], owner),), plural)
    entry = str(record["id"])
    named = [
        other
        for other in dict.fromkeys(RESULT_ID.findall(str(record.get("claim") or "")))
        if other != entry
        and other in records.results
        and re.search(
            rf"{re.escape(owner)}['\u2019]s\b",
            plain(str(records.results[other].get("headline") or "")),
        )
    ]
    found: list[str] = []
    for n in sorted(set(at) if at is not None else scope_values(dict(record["scope"]))):
        source = next(
            (
                records.results[other]
                for other in named
                if n in scope_values(dict(records.results[other]["scope"]))
            ),
            None,
        )
        if source is not None:
            found.extend(primary_names(credit_text(source, records.sources)))
    people_ = [token for token in people(dict.fromkeys(found)) if _bare(token) in credited]
    return Refinement(tuple((token, "") for token in people_), plural) if people_ else None


def worked_on(
    record: Mapping[str, Any], group: Sequence[Count], records: Records, names: Names
) -> str:
    """Whose packing the entry regularizes at the listed counts (`regularizations`), or
    refines (`refined`), as the record says it: `regularizing Ryan Xu's packing`,
    `refining Nate Chaoweeraprasit's packings`."""
    finders = [names.show(token) for token in regularized(record, group, records)]
    if len(finders) == 1:
        return f"regularizing {finders[0]}'s packing"
    if finders:
        return f"regularizing packings by {listed(finders)}"
    refinement = refined(record, records, [c.n for c in group] or None)
    if refinement is None:
        return ""
    shown_ = [
        names.show(token)
        if _bare(token) in names.handles or _bare(token) in names.full or not written
        else written
        for token, written in refinement.people
    ]
    several = len(group) > 1 if group else refinement.plural
    if len(shown_) == 1:
        return f"refining {shown_[0]}'s {'packings' if several else 'packing'}"
    return f"refining packings by {listed(shown_)}"


def credit_phrase(
    record: Mapping[str, Any],
    group: Sequence[Count],
    records: Records,
    names: Names,
    *,
    lineage: bool = False,
) -> str:
    """Who the line credits: the result's finders, the names before `after` in its credit
    line, as `Names` shows them; whose packing it refines or regularizes; and with
    `lineage`, the names after `after`. Never the project's owner."""
    finders, after = credit_parts(credit_text(record, records.sources))
    phrase = listed([names.show(token) for token in people(finders)])
    chain = [names.show(token) for token in people(after)]
    if lineage and chain:
        phrase = f"{phrase} after {listed(chain)}" if phrase else f"after {listed(chain)}"
    work = worked_on(record, group, records, names)
    if work:
        phrase = f"{phrase}, {work}" if phrase else work
    return phrase


def credited_people(record: Mapping[str, Any], records: Records, *, lineage: bool) -> list[str]:
    """Every name a line about `record` may print, for handles to be found for."""
    finders, after = credit_parts(credit_text(record, records.sources))
    found = [*finders, *(after if lineage else ())]
    for item in record.get("regularizations") or ():
        found.extend(
            primary_names(credit_text(records.results[str(item["of"])], records.sources))
        )
    if refinement := refined(record, records):
        found.extend(token for token, _ in refinement.people)
    return list(dict.fromkeys(_bare(token) for token in people(found)))


def whom(verb: str, labels: Sequence[str], at: int | None = None) -> str:
    """What a `since` clause says betters, equals or supersedes a result: up to
    `SINCE_NAMED` labels by name, else how many results and whether case records, at how
    many counts where `at` says (`bettered at 14 counts by their case records`)."""
    if len(labels) <= SINCE_NAMED:
        return f"{verb} by {listed(labels)}"
    results = sorted(
        {
            entry
            for label in labels
            if not CASE_LABEL.match(label)
            for entry in label.split(", ")
        }
    )
    who = (results if len(results) <= SINCE_NAMED else [f"{len(results)} results"]) + (
        ["their case records"] if any(CASE_LABEL.match(label) for label in labels) else []
    )
    where = "" if at is None else f" at {at} {'count' if at == 1 else 'counts'}"
    return f"{verb}{where} by {listed(who)}"


def render_line(
    record: Mapping[str, Any],
    records: Records,
    index: Mapping[tuple[int, str], Sequence[tuple[str, Span]]],
    names: Names,
    *,
    keep_all: bool = False,
    lineage: bool = False,
    show_margins: bool = False,
) -> Line:
    """One result's line: what it bounds, how it stands and how far it is checked, who
    found it, and its row on the site; or, for a bound best known nowhere, why it is left
    out."""
    entry = str(record["id"])
    link = result_link(entry)

    def line(claim: str, group: Sequence[Count]) -> Line:
        credit = credit_phrase(record, group, records, names, lineage=lineage)
        return Line(entry, f"{claim}: {credit} {link}" if credit else f"{claim} {link}")

    if str(record["kind"]) not in BOUND_KINDS:
        return line(f"{plain(str(record['headline']))} {tag(record)}", [])
    assessed = counts(record, records, index)
    best = [c for c in assessed if c.best]
    since = ""
    if standing(record, records) == SUPERSEDED:
        since = whom("superseded", superseding(record, records) or ["the case records"])
    elif assessed and not best:
        bettered = sorted({who for c in assessed for who in c.bettered_by})
        tied = sorted({who for c in assessed for who in c.tied_with} - set(bettered))
        since = " and ".join(
            words
            for words in (
                whom("bettered", bettered, sum(1 for c in assessed if c.bettered_by))
                if bettered
                else "",
                whom(
                    "equalled first",
                    tied,
                    sum(1 for c in assessed if c.tied_with and not c.bettered_by),
                )
                if tied
                else "",
            )
            if words
        )
    if since and not keep_all:
        at = compress([c.n for c in assessed]) if assessed else "no count it states"
        return Line(entry, "", f"the best known at no count (n = {at}): {since}")
    group = assessed if since else best
    if not group:
        what = f"{plain(str(record['headline']))} {tag(record)}"
        return line(f"{what}, since {since}" if since else what, [])

    def stated(*, each: bool) -> Line:
        what = statement(record, group, each=each)
        if show_margins and not since and (gap := margins(group)):
            what += f" ({gap})"
        if since:
            return line(f"{what} {tag(record)}, since {since}", group)
        return line(f"{what}, {NEWS[group[0].direction]} {tag(record)}", group)

    full = stated(each=True)
    return full if len(before_link(full.text)) <= BRIEF_LIMIT else stated(each=False)


# ---------------------------------------------------------------------------------------
# Selection and the command


def select(
    records: Records,
    *,
    ids: Sequence[str] = (),
    since: str | None = None,
    min_significance: int = MIN_SIGNIFICANCE,
) -> tuple[list[Mapping[str, Any]], list[Line]]:
    """The results to announce, in register order, and those set aside by significance."""
    wanted = set(ids)
    unknown = sorted(wanted - set(records.results))
    if unknown:
        raise SystemExit(f"not in the register: {', '.join(unknown)}")
    chosen: list[Mapping[str, Any]] = []
    skipped: list[Line] = []
    for record in records.register.results:
        if (wanted and record["id"] not in wanted) or (
            since is not None and str(record["registered"]) < since
        ):
            continue
        score = int(record["significance"]["score"])
        if score < min_significance:
            skipped.append(
                Line(str(record["id"]), "", f"significance {score}, below {min_significance}")
            )
        else:
            chosen.append(record)
    return chosen, skipped


def header(day: date, count: int) -> str:
    noun = "result" if count == 1 else "results"
    return f"{day.day} {MONTHS[day.month - 1]} {day.year}: {count} new {noun}"


def announcement(
    records: Records,
    chosen: Sequence[Mapping[str, Any]],
    names: Names,
    *,
    day: date,
    keep_all: bool = False,
    lineage: bool = False,
    show_margins: bool = False,
) -> tuple[list[str], list[Line]]:
    """The announcement's lines, header first, and the results left out of it."""
    index = rival_bounds(records)
    rendered = [
        render_line(
            record,
            records,
            index,
            names,
            keep_all=keep_all,
            lineage=lineage,
            show_margins=show_margins,
        )
        for record in chosen
    ]
    lines = [line.text for line in rendered if line.text]
    left = [line for line in rendered if not line.text]
    return [header(day, len(lines)), *lines], left


def credited_names() -> dict[str, str]:
    """The bibliography's `credited_names`: each full name and the name credits print."""
    bibliography = safe_load(BIBLIOGRAPHY.read_text(encoding="utf-8"))
    return {str(k): str(v) for k, v in (bibliography.get("credited_names") or {}).items()}


def _github(records: Records, credited: Mapping[str, str], fetch: Fetch) -> GitHub:
    requests = safe_load(REQUESTS.read_text(encoding="utf-8"))
    return GitHub(
        owner=str(requests.get("owner") or ""),
        issues=list(requests.get("issues") or ()),
        credited_names=credited,
        primaries={
            entry: primary_names(credit_text(record, records.sources))
            for entry, record in records.results.items()
        },
        fetch=fetch,
    )


def block_fit(lines: Sequence[str]) -> str:
    """Whether the whole announcement fits one X post, as `posted_length` counts each line
    and one character each line break, and where it does not, whether each line fits one
    post of a thread."""
    length = sum(posted_length(line) for line in lines) + len(lines) - 1
    if length <= POST_LIMIT:
        return f"the announcement fits one X post: {length} of {POST_LIMIT} characters"
    over = [line for line in lines if posted_length(line) > POST_LIMIT]
    thread = "every line fits" if not over else f"{len(over)} lines do not fit"
    return (
        f"the announcement is {length} characters on X, over one post's {POST_LIMIT}; "
        f"as a thread of one line a post, {thread}"
    )


def before_link(line: str) -> str:
    """A line without its link, which is what `BRIEF_LIMIT` counts."""
    return line.rsplit(" ", 1)[0]


def main(argv: Sequence[str] | None = None, *, fetch: Fetch = gh_user) -> int:
    parser = argparse.ArgumentParser(
        prog="render_announcement",
        description="Render new results as an announcement, one short line per result.",
    )
    chosen_by = parser.add_mutually_exclusive_group(required=True)
    chosen_by.add_argument("--ids", nargs="+", metavar="T-NNN", help="the results to announce")
    chosen_by.add_argument(
        "--since",
        type=date.fromisoformat,
        metavar="YYYY-MM-DD",
        help="announce the results registered on or after this date",
    )
    parser.add_argument(
        "--min-significance",
        type=int,
        default=MIN_SIGNIFICANCE,
        help=f"leave out results scored below this (default {MIN_SIGNIFICANCE})",
    )
    parser.add_argument(
        "--github",
        action="store_true",
        help="read GitHub profiles' declared X handles through `gh api` (network)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        dest="keep_all",
        help="keep bounds that are the best known at no count, saying what betters them",
    )
    parser.add_argument(
        "--lineage",
        action="store_true",
        help="credit, after the finders, the work each result rests on (`after …`)",
    )
    parser.add_argument(
        "--margins",
        action="store_true",
        help="say how far each bound passes the previous best",
    )
    parser.add_argument(
        "--date",
        type=date.fromisoformat,
        default=None,
        metavar="YYYY-MM-DD",
        help="the header's date (default today)",
    )
    options = parser.parse_args(argv)
    records = load_records()
    since = options.since.isoformat() if options.since else None
    chosen, skipped = select(
        records, ids=options.ids or (), since=since, min_significance=options.min_significance
    )
    people = list(
        dict.fromkeys(
            name
            for record in chosen
            for name in credited_people(record, records, lineage=options.lineage)
        )
    )
    credited, profiles = credited_names(), load_profiles()
    github = _github(records, credited, fetch) if options.github else None
    handles, warnings = resolve_handles(people, profiles, github, record_handles())
    lines, left = announcement(
        records,
        chosen,
        Names(handles, full_names(credited, profiles)),
        day=options.date or datetime.now(UTC).date(),
        keep_all=options.keep_all,
        lineage=options.lineage,
        show_margins=options.margins,
    )
    print("\n".join(lines))
    for line in [*skipped, *left]:
        print(f"left out {line.id}: {line.left_out}", file=sys.stderr)
    for text in lines[1:]:
        entry = text.rsplit("#", 1)[-1].upper()
        if (length := len(before_link(text))) > BRIEF_LIMIT:
            print(
                f"warning: {entry}'s line is {length} characters before its link",
                file=sys.stderr,
            )
        if (length := posted_length(text)) > POST_LIMIT:
            print(f"warning: {entry}'s line is {length} characters on X", file=sys.stderr)
    print(block_fit(lines), file=sys.stderr)
    for handle in handles.values():
        print(f"@{handle.handle} for {handle.name}: {handle.source}", file=sys.stderr)
    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)
    unhandled = [name for name in people if name not in handles]
    if unhandled:
        print(f"no handle on record, printed by name: {', '.join(unhandled)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
