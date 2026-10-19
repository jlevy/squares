#!/usr/bin/env python3
"""Independent recomputation of the 2026-10-14 intake ledger's verdicts from primary data.

Reads (nothing from ledger.yaml or ledger.json except for the final comparison and the
provenance audit, which are the objects under review):

- each lane's claims.json and algebraic-claims.json: from the packet under
  `packing/resources/web/<packet>/acquisition/` where `main` carries it, and otherwise from
  `PINNED/lanes/<lane>/<packet>/`, the bytes the lane's branch commit holds (the README's
  "Lane Records Read" table names the commits);
- `packing/frontier/n-NNN.md`, `source-coverage.yaml` and `results.yaml`;
- `PINNED/github/issue-N.json`, `pr-574.json`, `edits-N.json` (gh, read-only) for report
  times;
- `PINNED/upstream/*`, certificate headers fetched at the pinned upstream commits through
  the GitHub contents API;
- a hand transcription table (TRANSCRIBED) quoting where each print was read.

The walk is written from the owner's rule and the README's stated semantics, not from the
module under review. Differences from devtools.intake_ledger are deliberate and listed in
the output: the start is the SET of both case lanes (reported and verified), closed forms
with sqrt and polynomial roots are evaluated as rigorous intervals, the binary64 span is
half an ulp plus half a unit, and exact sides the lanes' READMEs or the PR's own files state
are used where the ledger used a print.

From `packing/`, with the project interpreter::

    python campaign/issue-intake/upper-bounds-20261014/review/recompute.py PINNED
"""

from __future__ import annotations

import json
import math
import random
import re
import sys
from dataclasses import dataclass, field
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

import mpmath as mp
import yaml
from mpmath.libmp import to_rational

#: The repository root: this file is packing/campaign/issue-intake/<directory>/review/.
REPO = Path(__file__).resolve().parents[5]
PACKING = REPO / "packing"
PACKETS = PACKING / "resources/web"
LEDGER_DIR = PACKING / "campaign/issue-intake/upper-bounds-20261014"
FRONTIER = PACKING / "frontier"
HORIZON = 324
mp.mp.dps = 90
IV: Any = mp.iv
IV.dps = 90


def lane_record(scr: Path, lane: str, packet: str, record: str) -> dict[str, Any]:
    """A lane's claim record: the packet on `main` where it is there, else the pinned bytes."""
    on_main = PACKETS / packet / "acquisition" / record
    path = on_main if on_main.is_file() else scr / "lanes" / lane / packet / record
    return json.loads(path.read_text(encoding="utf-8"))


# ------------------------------------------------------------------ spans and relations


@dataclass(frozen=True)
class Span:
    low: Fraction
    high: Fraction
    open_low: bool = False
    open_high: bool = False

    @property
    def exact(self) -> bool:
        return self.low == self.high and not self.open_low and not self.open_high


def point(v: Fraction) -> Span:
    return Span(v, v)


def below(a: Span, b: Span) -> bool:
    return a.high < b.low or (a.high == b.low and (a.open_high or b.open_low))


def rel(a: Span, b: Span) -> str:
    if below(a, b):
        return "below"
    if below(b, a):
        return "above"
    if a.exact and b.exact and a.low == b.low:
        return "equal"
    return "undecided"


def unit(printed: str) -> Fraction:
    return Fraction(1, 10 ** len(printed.partition(".")[2]))


def decimal(printed: str) -> Fraction:
    return Fraction(Decimal(printed))


def print_span(printed: str, rounding: str, *, wide_binary64: bool = False) -> Span:
    """My reading of what a print can stand for. up: (p-u, p]; cut: [p, p+u);
    nearest/unstated: [p-u, p+u]; binary64: p +- (ulp/2 + u/2) under the correctly-rounded
    model (the ledger's ulp + u with wide_binary64)."""
    if rounding == "exact":
        return point(Fraction(printed))
    p, u = decimal(printed), unit(printed)
    if rounding == "up":
        return Span(p - u, p, open_low=True)
    if rounding == "cut":
        return Span(p, p + u, open_high=True)
    if rounding == "binary64":
        ulp = Fraction(math.ulp(float(p)))
        slack = ulp + u if wide_binary64 else ulp / 2 + u / 2
        return Span(p - slack, p + slack)
    return Span(p - u, p + u)


def mpf_fraction(x: Any) -> Fraction:
    n, d = to_rational(mp.mpf(x)._mpf_)
    return Fraction(int(n), int(d))


# ------------------------------------------------------------------ closed forms


_TOKEN = re.compile(r"\s*(?:(\d+\.\d+|\d+)|(sqrt)|([-+*/()]))")


def closed_form_interval(form: str) -> Span | None:
    """A rigorous enclosure of a closed form such as `2 + (1/2)sqrt(2)`, `(16+5*sqrt(2))/3`,
    `7 - (1/2)sqrt(2) + sqrt(1 + sqrt(2))`, `6 + 4 sqrt(2)`, `15 + (28/41)`, or a plain p/q.
    None where the form is not of that shape (a polynomial root, say)."""
    if not form or "root(" in form or "floor" in form:
        return None
    tokens: list[tuple[str, str]] = []
    pos = 0
    while pos < len(form):
        m = _TOKEN.match(form, pos)
        if not m or m.end() == pos:
            if form[pos:].strip() == "":
                break
            return None
        pos = m.end()
        if m.group(1):
            tokens.append(("num", m.group(1)))
        elif m.group(2):
            tokens.append(("sqrt", "sqrt"))
        else:
            tokens.append(("op", m.group(3)))
    # implicit multiplication: num|')' followed by '('|sqrt|num
    out: list[tuple[str, str]] = []
    for t in tokens:
        if (
            out
            and (out[-1][0] == "num" or out[-1] == ("op", ")"))
            and (t[0] in ("num", "sqrt") or t == ("op", "("))
        ):
            out.append(("op", "*"))
        out.append(t)
    tokens = out
    i = 0

    def peek() -> tuple[str, str] | None:
        return tokens[i] if i < len(tokens) else None

    def take() -> tuple[str, str]:
        nonlocal i
        t = tokens[i]
        i += 1
        return t

    def expr() -> Any:
        v = term()
        while peek() in (("op", "+"), ("op", "-")):
            op = take()[1]
            w = term()
            v = v + w if op == "+" else v - w
        return v

    def term() -> Any:
        v = factor()
        while peek() in (("op", "*"), ("op", "/")):
            op = take()[1]
            w = factor()
            v = v * w if op == "*" else v / w
        return v

    def factor() -> Any:
        t = take()
        if t == ("op", "-"):
            return -factor()
        if t == ("op", "("):
            v = expr()
            assert take() == ("op", ")")
            return v
        if t[0] == "sqrt":
            assert take() == ("op", "(")
            v = expr()
            assert take() == ("op", ")")
            return IV.sqrt(v)
        if t[0] == "num":
            if "sqrt" not in form:
                return Fraction(Decimal(t[1])) if "." in t[1] else Fraction(int(t[1]))
            if "." in t[1]:
                return IV.mpf(t[1])
            return IV.mpf(int(t[1]))
        raise ValueError(form)

    try:
        v = expr()
    except AssertionError, ValueError, IndexError:
        return None
    if i != len(tokens):
        return None
    if isinstance(v, Fraction):
        return point(v)
    return Span(mpf_fraction(v.a), mpf_fraction(v.b))


def polynomial_coefficients(text: str) -> list[int]:
    """Integer coefficients, highest degree first, of a polynomial in s.

    The polynomial is written as `s^8 - 20s^7 + ... - 6865`.
    """
    coeffs: dict[int, int] = {}
    for m in re.finditer(r"([+-]?)(\d*)s(?:\^(\d+))?|([+-]?\d+)(?![\ds^])", text):
        if m.group(4) is not None and m.group(2) is None:
            coeffs[0] = coeffs.get(0, 0) + int(m.group(4))
            continue
        if m.group(0) and "s" in m.group(0):
            sign = -1 if m.group(1) == "-" else 1
            c = int(m.group(2)) if m.group(2) else 1
            e = int(m.group(3)) if m.group(3) else 1
            coeffs[e] = coeffs.get(e, 0) + sign * c
    tail = re.search(r"([+-]\d+)$", text)
    if tail:
        coeffs[0] = int(tail.group(1))
    degree = max(coeffs)
    return [coeffs.get(e, 0) for e in range(degree, -1, -1)]


def polynomial_root_interval(poly_text: str, near: str) -> Span:
    """A rigorous enclosure of the real root of an integer polynomial in s nearest `near`,
    by an exact sign change at rational endpoints around a high-precision root."""
    text = poly_text.split("=", maxsplit=1)[0].replace(" ", "")
    cs = polynomial_coefficients(text)
    coeffs: dict[int, int] = {}
    for m in re.finditer(r"([+-]?)(\d*)s(?:\^(\d+))?|([+-]?\d+)(?![\ds^])", text):
        if m.group(4) is not None and m.group(2) is None:
            coeffs[0] = coeffs.get(0, 0) + int(m.group(4))
            continue
        if m.group(0) and "s" in m.group(0):
            sign = -1 if m.group(1) == "-" else 1
            c = int(m.group(2)) if m.group(2) else 1
            e = int(m.group(3)) if m.group(3) else 1
            coeffs[e] = coeffs.get(e, 0) + sign * c
    # the constant term: the trailing signed integer not followed by s
    tail = re.search(r"([+-]\d+)$", text)
    if tail:
        coeffs[0] = int(tail.group(1))

    def value_at(x: Fraction) -> Fraction:
        acc = Fraction(0)
        for c in cs:
            acc = acc * x + c
        return acc

    r = mp.findroot(lambda s: mp.polyval(cs, s), mp.mpf(near))
    centre = mpf_fraction(r)
    for k in range(120, 20, -5):
        eps = Fraction(1, 10**k)
        lo, hi = centre - eps, centre + eps
        if value_at(lo) * value_at(hi) < 0:
            return Span(lo, hi)
    raise ValueError("no sign change around the root")


# ------------------------------------------------------------------ the record at main


def case(n: int) -> dict[str, Any]:
    text = (FRONTIER / f"n-{n:03d}.md").read_text(encoding="utf-8")
    return yaml.safe_load(text.split("---\n")[1])["packing"]


@dataclass
class Side:
    label: str
    span: Span
    value: Fraction  # for display and "difference" only
    time: str = ""
    first_committed: str = ""
    kind: str = "record"
    note: str = ""


def lane_side(lane: str, bound: dict[str, Any], poly: str = "") -> Side:
    value = str(bound["value"])
    form = bound.get("exact_form")
    label = f"{lane} lane"
    if form:
        form = str(form)
        if re.fullmatch(r"\d+/\d+", form):
            v = Fraction(form)
            return Side(label, point(v), v, note=f"exact {form[:40]}")
        if form.startswith("root("):
            poly = str(bound.get("minimal_polynomial") or poly or "")
            span = polynomial_root_interval(poly, value)
            return Side(label, span, decimal(value), note="polynomial root enclosure")
        span = closed_form_interval(form)
        if span is not None:
            return Side(label, span, decimal(value), note=f"closed form {form}")
    return Side(label, print_span(value, "unstated"), decimal(value), note=f"print {value} +-u")


_STATED = re.compile(r"s\((\d+)\)(?:, s\(\d+\))* (?:<=|≤) (\d+(?:/\d+|\.\d+)?)(…|\.\.\.)?")


def pending_bounds(counts: set[int]) -> dict[int, list[Side]]:
    """Register entries whose words state an upper bound at a ledger count that lies decidably
    below both case lanes: pending adoption by definition. Read from results.yaml at main."""
    register = yaml.safe_load((FRONTIER / "results.yaml").read_text(encoding="utf-8"))
    found: dict[int, list[Side]] = {}
    for entry in register["results"]:
        text = " ".join(str(entry.get("headline") or "").split())
        stated = {}
        for m in _STATED.finditer(text):
            stated[int(m.group(1))] = (m.group(2), bool(m.group(3)))
        if not stated:
            text = " ".join(str(entry.get("claim") or "").split())
            for m in _STATED.finditer(text):
                stated.setdefault(int(m.group(1)), (m.group(2), bool(m.group(3))))
        for n, (v, cut) in stated.items():
            if n not in counts or n > HORIZON:
                continue
            span = (
                print_span(v, "cut")
                if cut
                else (point(Fraction(v)) if "/" in v else point(decimal(v)))
            )
            c = case(n)
            poly = str(c["reported_upper_bound"].get("minimal_polynomial") or "")
            lanes = [
                lane_side("reported", c["reported_upper_bound"], poly),
                lane_side("verified", c["verified_upper_bound"], poly),
            ]
            if all(below(span, s.span) for s in lanes):
                found.setdefault(n, []).append(
                    Side(
                        f"register {entry['id']} pending",
                        span,
                        span.low,
                        kind="register",
                        note=f"stated {v}{'…' if cut else ''}",
                    )
                )
    return found


def starts(counts: list[int]) -> dict[int, list[Side]]:
    coverage = yaml.safe_load((FRONTIER / "source-coverage.yaml").read_text(encoding="utf-8"))
    beyond: dict[int, dict[str, Any]] = {}
    for row in coverage["beyond_horizon_claims"]:
        if row.get("disposition") == "superseded":
            continue
        assert row["n"] not in beyond, row["n"]
        beyond[row["n"]] = row
    pending = pending_bounds(set(counts))
    result: dict[int, list[Side]] = {}
    for n in counts:
        if n <= HORIZON:
            c = case(n)
            poly = str(c["reported_upper_bound"].get("minimal_polynomial") or "")
            members = [
                lane_side("reported", c["reported_upper_bound"], poly),
                lane_side("verified", c["verified_upper_bound"], poly),
                *pending.get(n, []),
            ]
            # keep the minimal elements: drop a member decidably above another
            members = [
                m
                for m in members
                if not any(below(o.span, m.span) for o in members if o is not m)
            ]
            result[n] = members
        elif n in beyond:
            row = beyond[n]
            v = str(row["value"])
            result[n] = [
                Side(
                    f"beyond-horizon row {row['source_id']}",
                    print_span(v, "unstated"),
                    decimal(v),
                )
            ]
        else:
            g = Fraction(__import__("math").isqrt(n - 1) + 1)
            result[n] = [Side("the grid", point(g), g)]
    return result


# ------------------------------------------------------------------ reports and claims


def gh_issue(scr: Path, n: int) -> dict[str, Any]:
    return json.loads((scr / "github" / f"issue-{n}.json").read_text(encoding="utf-8"))


def comment_time(scr: Path, issue: int, comment_id: int) -> str:
    for c in gh_issue(scr, issue)["comments"]:
        if c["url"].endswith(f"#issuecomment-{comment_id}") or str(c.get("id", "")).endswith(
            str(comment_id)
        ):
            return c["createdAt"]
    raise KeyError(comment_id)


# edits that added or replaced a claim: (report, n) -> GraphQL editedAt, with the comment
# time beside it
EDIT_TIMES = {
    ("#564", 302): ("2026-10-12T22:16:43Z", "2026-10-12T22:17:00Z"),
    ("#566", 146): ("2026-10-12T23:41:36Z", "2026-10-12T23:41:41Z"),
    ("#567", 261): ("2026-10-12T23:45:35Z", "2026-10-12T23:45:41Z"),
    ("#575", 304): ("2026-10-13T04:13:29Z", "2026-10-13T04:13:31Z"),
}

LANES = {
    ("couzo", "couzo-certificates-2026-10-12", "claims.json"): lambda _row: "#561",
    ("couzo", "couzo-certificates-2026-10-13", "claims.json"): lambda row: (
        "#583"
        if row["printed_in"].endswith("/583")
        else "#586"
        if row["printed_in"].endswith("/586")
        else {
            "2026-10-12T21:31:43Z": "franciscouzo/square-packing@93570ef",
            "2026-10-13T13:53:57Z": "franciscouzo/square-packing@4596670",
            "2026-10-13T17:30:53Z": "franciscouzo/square-packing@b85dee2",
        }[row["first_committed"]]
    ),
    ("mishapolk", "mishapolk-exact-certificates-2026-10-12", "claims.json"): lambda _row: (
        "#573"
    ),
    ("mishapolk", "mishapolk-records-2026-10-14", "claims.json"): lambda _row: "#593",
    ("ostashev", "dostashev-compositions-2026-10-12", "claims.json"): lambda _row: "#562",
    ("ostashev", "dostashev-merged-bands-2026-10-13", "claims.json"): lambda _row: "#575",
    ("ostashev", "evand-compositions-2026-10-13", "claims.json"): lambda _row: "#584",
    ("ostashev", "evand-fresh-compositions-2026-10-14", "claims.json"): lambda _row: "#596",
    ("pingyou", "pingyou-n105-refinement-2026-10-12", "claims.json"): lambda _row: "#568",
    ("pingyou", "pingyou-n146-refinement-2026-10-12", "claims.json"): lambda _row: "#566",
    ("pingyou", "pingyou-n153-refinement-2026-10-12", "claims.json"): lambda _row: (
        "#504 comment 6133737268"
    ),
    ("pingyou", "pingyou-n207-refinement-2026-10-12", "claims.json"): lambda _row: (
        "#503 comment 6133755143"
    ),
    ("pingyou", "pingyou-n261-refinement-2026-10-12", "claims.json"): lambda _row: "#567",
    ("pingyou", "pingyou-n272-refinement-2026-10-12", "claims.json"): lambda _row: "#569",
    ("pingyou", "pingyou-n302-certificate-2026-10-12", "claims.json"): lambda _row: "#564",
    ("pr574", "pingyou-pr574-certificates-2026-10-13", "claims.json"): lambda _row: "PR #574",
    ("pr574", "pingyou-pr574-certificates-2026-10-13", "algebraic-claims.json"): lambda _row: (
        "PR #574"
    ),
}
# the lane's 00:29:11Z for the N153/N302 commit is GitHub's a006c4525 at 01:29:11Z
# (02:29:11+01:00)
TIME_FIX = {"2026-10-13T00:29:11Z": "2026-10-13T01:29:11Z"}


def cert_side(scr: Path, name: str) -> Fraction:
    """The side line of a fetched upstream certificate.

    It is `n S` in the evand format and `s S` in sqcert.
    """
    for line in (scr / "upstream" / name).read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if len(parts) == 2 and parts[0] == "s":
            return Fraction(parts[1])
        if len(parts) == 2 and parts[0].isdigit() and "/" in parts[1]:
            return Fraction(parts[1])
    raise ValueError(name)


#: What `read_pinned` reads from the PINNED directory `main` is given: PR #574 and its
#: commits' times, each report's time, the pull request's head rows, and the transcribed
#: claims (report, n, span, display value, first_committed, where read).
PR: dict[str, Any] = {}
PR_COMMITS: set[str] = set()
REPORT_TIMES: dict[str, str] = {}
PR_HEAD: dict[int, dict[str, Any]] = {}
TRANSCRIBED: list[tuple[str, int, Span, Fraction, str, str]] = []


def read_pinned(scr: Path) -> None:
    """Fill the reads above from ``scr``; `main` calls it once, before anything else."""
    PR.update(json.loads((scr / "github/pr-574.json").read_text(encoding="utf-8")))
    PR_COMMITS.update(c["committedDate"] for c in PR["commits"])

    for n in (
        528,
        529,
        552,
        561,
        562,
        564,
        566,
        567,
        568,
        569,
        570,
        573,
        575,
        582,
        583,
        584,
        586,
        589,
        593,
        596,
    ):
        REPORT_TIMES[f"#{n}"] = gh_issue(scr, n)["createdAt"]
    REPORT_TIMES["#504 comment 6133737268"] = comment_time(scr, 504, 6133737268)
    REPORT_TIMES["#503 comment 6133755143"] = comment_time(scr, 503, 6133755143)
    REPORT_TIMES["PR #574"] = PR["createdAt"]
    # publications: the committer date of the named commit, as fetched from GitHub (see
    # the review)
    REPORT_TIMES["TheSnakeFang/squarepack-certs@e646c47"] = "2026-10-12T19:06:24Z"
    REPORT_TIMES["TheSnakeFang/squarepack-certs@c284cd0"] = "2026-10-13T00:05:31Z"
    REPORT_TIMES["franciscouzo/square-packing@93570ef"] = "2026-10-12T21:31:43Z"
    REPORT_TIMES["franciscouzo/square-packing@4596670"] = "2026-10-13T13:53:57Z"
    REPORT_TIMES["franciscouzo/square-packing@b85dee2"] = "2026-10-13T17:30:53Z"

    PR_HEAD.update(
        {
            row["n"]: row
            for row in json.loads(
                (scr / "upstream/pr574-head-numerical-claims.json").read_text(encoding="utf-8")
            )["rows"]
        }
    )

    # (report, n, span, display value, first_committed, where read)
    for n, fc in (
        (155, "2026-10-11T13:21:30Z"),
        (156, "2026-10-11T13:21:30Z"),
        (175, "2026-10-12T03:05:21Z"),
        (211, "2026-10-11T13:21:30Z"),
        (232, "2026-10-12T03:05:21Z"),
        (264, "2026-10-12T03:05:21Z"),
    ):
        s = cert_side(scr, f"dostashev-a8db6ff-n0{n}.sqcert")
        TRANSCRIBED.append(
            (
                "#528",
                n,
                point(s),
                s,
                fc,
                (
                    f"records/n0{n}.sqcert s line at dostashev/square-packing@a8db6ff "
                    "(issue #528 names the commit)"
                ),
            )
        )
    TRANSCRIBED.append(
        (
            "#529",
            102,
            print_span("10.605828696455852", "unstated"),
            decimal("10.605828696455852"),
            "2026-10-12T04:23:19Z",
            "issue #529: 'n = 102, s = 10.605828696455852' (decimal poses, no exact side)",
        )
    )
    s552 = Fraction(12922566401934059503377267965457, 10**30)
    TRANSCRIBED.append(
        (
            "#552",
            154,
            point(s552),
            s552,
            "2026-10-12T13:58:36Z",
            "issue #552: S' = 12922566401934059503377267965457 / 10^30",
        )
    )
    s154 = cert_side(scr, "franciscouzo_square-packing@4596670-n154.cert")
    TRANSCRIBED.append(
        (
            "#570",
            154,
            point(s154),
            s154,
            "",
            (
                "certificates/n154.cert at franciscouzo/square-packing@4596670, SHA-256 "
                "5335cb3b... as #570 states"
            ),
        )
    )
    TRANSCRIBED.append(
        (
            "#570",
            379,
            print_span("19.953542593650", "up"),
            decimal("19.953542593650"),
            "",
            (
                "issue #570 table, 'rounded upward to 12 decimal places'; the pinned 1b31bc9 "
                "is not served"
            ),
        )
    )
    for n in (154, 211, 241, 339, 379, 380, 382):
        s = cert_side(scr, f"franciscouzo_square-packing@4596670-n{n}.cert")
        TRANSCRIBED.append(
            (
                "#583",
                n,
                point(s),
                s,
                "",
                (
                    f"certificates/n{n}.cert header at franciscouzo/square-packing@4596670 "
                    "(the pin #583 names)"
                ),
            )
        )
    s582 = Fraction(19985624661051481, 10**15)
    TRANSCRIBED.append(
        ("#582", 381, point(s582), s582, "", "issue #582: 19985624661051481/1000000000000000")
    )
    TRANSCRIBED.append(
        (
            "#589",
            381,
            point(s582),
            s582,
            "",
            "issue #589: the same certificate as #582 (SHA-256 03650573...)",
        )
    )
    for n, name in (
        (380, "TheSnakeFang_squarepack-certs@e646c47-n0380.cert"),
        (381, "TheSnakeFang_squarepack-certs@e646c47-n0381.cert"),
    ):
        s = cert_side(scr, name)
        TRANSCRIBED.append(
            (
                "TheSnakeFang/squarepack-certs@e646c47",
                n,
                point(s),
                s,
                "2026-10-12T19:06:24Z",
                f"n0{n}/n0{n}.cert header at e646c47",
            )
        )
    s = cert_side(scr, "TheSnakeFang_squarepack-certs@c284cd0-n0382.cert")
    TRANSCRIBED.append(
        (
            "TheSnakeFang/squarepack-certs@c284cd0",
            382,
            point(s),
            s,
            "2026-10-13T00:05:31Z",
            "n0382/n0382.cert header at c284cd0",
        )
    )
    for n in (11, 17, 29):
        s = Fraction(PR_HEAD[n]["side_exact"])
        TRANSCRIBED.append(
            (
                "PR #574",
                n,
                point(s),
                s,
                "2026-10-13T00:24:05Z",
                (
                    f"side_exact of row n={n} in the pull request's numerical claims.json "
                    "at its head 4c319c24a"
                ),
            )
        )
    s593_51 = cert_side(scr, "mishapolk-46f638c-n51.cert")
    TRANSCRIBED.append(
        (
            "#593",
            51,
            point(s593_51),
            s593_51,
            "2026-10-13T21:38:13Z",
            (
                "certificates/n51.cert header at Mishapolk/square-packing-records@46f638c "
                "(SHA-256 e066f65f..., as the lane README states)"
            ),
        )
    )


def claims(scr: Path) -> dict[int, list[Side]]:
    by_count: dict[int, list[Side]] = {}
    for (lane, packet, record), owner in LANES.items():
        data = lane_record(scr, lane, packet, record)
        for row in data["results"]:
            n = int(row["n"])
            report = owner(row)
            committed = str(row["first_committed"])
            fc = TIME_FIX.get(committed, committed)
            if "exact_side" in row:
                v = Fraction(row["exact_side"])
                span = point(v)
                note = "lane exact"
            else:
                # an algebraic side printed at 40 places by the lane; rounding unstated
                span = print_span(row["side_decimal"], "unstated")
                v = decimal(row["side_decimal"])
                note = f"algebraic degree {row['degree']}, lane print +-1e-40"
            time = REPORT_TIMES[report]
            if report == "PR #574" and fc > time:
                assert fc in PR_COMMITS, fc
                time = fc
            if report.startswith(("franciscouzo/", "TheSnakeFang/")):
                time = fc
            by_count.setdefault(n, []).append(
                Side(report, span, v, time, fc, kind="claim", note=note)
            )
    for report, n, span, v, fc, where in TRANSCRIBED:
        time = REPORT_TIMES[report]
        if report == "PR #574" and fc > time:
            time = fc
        if report.startswith(("franciscouzo/", "TheSnakeFang/")):
            time = fc
        by_count.setdefault(n, []).append(
            Side(report, span, v, time, fc, kind="claim", note=f"transcribed: {where}")
        )
    for (report, n), (edited, _comment) in EDIT_TIMES.items():
        for side in by_count[n]:
            if side.label == report:
                side.time = edited
    return by_count


# ------------------------------------------------------------------ the walk


@dataclass
class Step:
    side: Side
    verdict: str
    against: list[Side] = field(default_factory=list)


def walk(start: list[Side], entries: list[Side]) -> tuple[list[Step], list[Side]]:
    standing = list(start)
    steps = []
    for side in sorted(entries, key=lambda s: (s.time, s.label)):
        rels = [(m, rel(side.span, m.span)) for m in standing]
        if all(r == "below" for _, r in rels):
            steps.append(Step(side, "recorded", [m for m, _ in rels]))
            standing = [side]
        elif any(r in ("above", "equal") for _, r in rels):
            steps.append(
                Step(side, "not recorded", [m for m, r in rels if r in ("above", "equal")])
            )
        else:
            steps.append(Step(side, "undecided", [m for m, r in rels if r == "undecided"]))
            standing = [m for m, r in rels if r != "below"] + [side]
    return steps, standing


# ------------------------------------------------------------------ comparison with the ledger


def main() -> None:
    scr = Path(sys.argv[1])
    read_pinned(scr)
    s593_51 = cert_side(scr, "mishapolk-46f638c-n51.cert")
    ledger_json = json.loads((LEDGER_DIR / "ledger.json").read_text(encoding="utf-8"))
    ledger_counts = {c["n"]: c for c in ledger_json["counts"]}
    counts = sorted(ledger_counts)
    by_count = claims(scr)
    start = starts(counts)
    missing = sorted(set(by_count) ^ set(counts))
    print(
        f"counts in ledger: {len(counts)}; counts I built: {len(by_count)}; symmetric "
        f"difference: {missing}"
    )

    agree = disagree = 0
    rows = []
    disagreements = []
    consistent_equal = []
    for n in counts:
        steps, _standing = walk(start[n], by_count.get(n, []))
        mine = {s.side.label: s for s in steps}
        for step in ledger_counts[n]["steps"]:
            label = step["report"]
            m = mine.get(label)
            if m is None:
                rows.append((n, label, step["verdict"], "MISSING", False))
                disagree += 1
                disagreements.append((n, label, step["verdict"], "missing in my claim set", ""))
                continue
            ok = m.verdict == step["verdict"]
            note = ""
            if (
                not ok
                and step["verdict"] == "not recorded"
                and step["reason"] == "equal"
                and m.verdict == "undecided"
            ):
                # my interval cannot prove equality of an algebraic side with a closed form
                note = "equal-by-lane vs undecided-by-interval"
                consistent_equal.append((n, label))
                ok = True
            rows.append((n, label, step["verdict"], m.verdict, ok, note))
            if ok:
                agree += 1
            else:
                disagree += 1
                against = [a.label for a in m.against]
                detail = (
                    f"mine: {m.verdict} against {against}; side "
                    f"{m.side.span.low!s:.60} note={m.side.note}"
                )
                disagreements.append(
                    (
                        n,
                        label,
                        step["verdict"]
                        + " ("
                        + step["reason"]
                        + ": "
                        + ", ".join(step["decided_against"])
                        + ")",
                        m.verdict,
                        detail,
                    )
                )
        extra = [
            s
            for s in steps
            if s.side.label not in {st["report"] for st in ledger_counts[n]["steps"]}
        ]
        rows.extend(
            (n, s.side.label, "ABSENT", s.verdict, False, "claim the ledger does not list")
            for s in extra
        )
    print(
        f"\nsteps compared: {agree + disagree}; agree: {agree}; disagree: {disagree}; of the "
        f"agreements {len(consistent_equal)} are equal-by-lane vs undecided-by-interval "
        "(listed as consistent)"
    )
    print("\n## Disagreements")
    for d in disagreements:
        print(" ", d)

    print("\n## Verdict table (n, report, ledger, mine, agree, note)")
    for r in rows:
        print(" ", r)

    # ---- sensitivity: reported lane only (the ledger's start), the lane's uncorrected time,
    # the comment times
    print("\n## Sensitivity")
    changed = []
    for n in counts:
        if n > HORIZON:
            continue
        c = case(n)
        pend = pending_bounds({n}).get(n, [])
        rep_only = [
            lane_side(
                "reported",
                c["reported_upper_bound"],
                str(c["reported_upper_bound"].get("minimal_polynomial") or ""),
            ),
            *pend,
        ]
        rep_only = [
            m
            for m in rep_only
            if not any(below(o.span, m.span) for o in rep_only if o is not m)
        ]
        a, _ = walk(rep_only, by_count.get(n, []))
        b, _ = walk(start[n], by_count.get(n, []))
        for x, y in zip(a, b, strict=True):
            if x.verdict != y.verdict:
                changed.append(
                    (
                        n,
                        x.side.label,
                        "reported-lane-only: " + x.verdict,
                        "both lanes: " + y.verdict,
                    )
                )
    print(" verdicts that change when the verified lane joins the start:", changed or "none")

    # ---- the special comparisons
    print("\n## Special comparisons")
    c11 = case(11)
    root = polynomial_root_interval(
        str(c11["reported_upper_bound"]["minimal_polynomial"]),
        str(c11["verified_upper_bound"]["value"]),
    )
    pr11 = Fraction(PR_HEAD[11]["side_exact"])
    poly11 = str(c11["reported_upper_bound"]["minimal_polynomial"])
    text = poly11.split("=", maxsplit=1)[0].replace(" ", "")
    cs11 = polynomial_coefficients(text)

    def value_at_11(x: Fraction) -> Fraction:
        acc = Fraction(0)
        for c in cs11:
            acc = acc * x + c
        return acc

    sign_at_pr = (value_at_11(pr11) > 0) - (value_at_11(pr11) < 0)
    sign_right = (value_at_11(root.high) > 0) - (value_at_11(root.high) < 0)
    side_of_root = "above" if sign_at_pr == sign_right else "below"
    print(
        f" n=11: root(P_trump11) enclosed with width {float(root.high - root.low):.1e}; PR "
        f"#574 exact side - root.high = {float(pr11 - root.high):.3e}; exact sign test: "
        f"P(side) has the sign of P(root+eps) -> the side is {side_of_root} the root; "
        f"|side - "
        f"root| < {float(abs(pr11 - root.high)) + float(root.high - root.low):.1e}"
    )
    for k in (70, 80, 100, 120, 150, 200, 300):
        eps = Fraction(1, 10**k)
        lo, hi = pr11 - eps, pr11 + eps
        if value_at_11(lo) * value_at_11(hi) < 0:
            print(
                f"       the root lies within 1e-{k} of the PR's side (sign change across "
                f"[side-1e-{k}, side+1e-{k}])"
            )
            break
    else:
        print(
            "       the root is not within 1e-300 of the PR's side on either side? (no sign "
            "change found)"
        )
    print(
        f"       PR #574 40-place print: {PR_HEAD[11]['safe_upper_bound_40_decimals']} ; root "
        f"to 45 places: {mp.nstr(mp.mpf(root.low.numerator) / root.low.denominator, 46)}"
    )
    cf51 = closed_form_interval("(16+5*sqrt(2))/3")
    assert cf51 is not None
    print(
        " n=51: (16+5*sqrt(2))/3 in "
        f"[{mp.nstr(mp.mpf(cf51.low.numerator) / cf51.low.denominator, 40)}, ...] ; #593 "
        f"exact side {s593_51} - closed form = {float(s593_51 - cf51.high):.3e} -> "
        f"{rel(point(s593_51), cf51)}"
    )
    print(f"       ratio S/closed - 1 = {float(s593_51 / cf51.high - 1):.3e}")
    c17 = case(17)
    v17 = Fraction(str(c17["verified_upper_bound"]["exact_form"]))
    pr17 = Fraction(PR_HEAD[17]["side_exact"])
    print(
        f" n=17: PR #574 exact - verified exact = {float(pr17 - v17):.3e} -> "
        f"{rel(point(pr17), point(v17))}; vs reported print "
        f"{c17['reported_upper_bound']['value']} +-1e-14 -> "
        f"{rel(point(pr17), print_span(str(c17['reported_upper_bound']['value']), 'unstated'))}"
    )
    c29 = case(29)
    v29 = Fraction(str(c29["verified_upper_bound"]["exact_form"]))
    pr29 = Fraction(PR_HEAD[29]["side_exact"])
    print(
        f" n=29: PR #574 exact - verified exact form = {float(pr29 - v29):.3e} -> "
        f"{rel(point(pr29), point(v29))}; verified value print "
        f"{c29['verified_upper_bound']['value']} - exact form = "
        f"{float(decimal(str(c29['verified_upper_bound']['value'])) - v29):.3e}"
    )

    # ---- binary64 prints of #593 against the exact sides
    print("\n## #593 prints (16 places, binary64) against the exact sides from the lane")
    issue593 = gh_issue(scr, 593)["body"]
    prints = {
        int(m.group(1)): m.group(2)
        for m in re.finditer(r"\|\s*\*\*(\d+)\*\*\s*\|\s*(\d+\.\d+)\s*\|", issue593)
    }
    data = json.loads(
        (scr / "lanes/mishapolk/mishapolk-records-2026-10-14/claims.json").read_text(
            encoding="utf-8"
        )
    )
    worst_tight = worst_wide = 0.0
    outside_tight = []
    for row in data["results"]:
        n = int(row["n"])
        p = prints.get(n)
        if p is None:
            continue
        exact = Fraction(row["exact_side"])
        d = abs(exact - decimal(p))
        ulp = Fraction(math.ulp(float(decimal(p))))
        u = unit(p)
        tight = ulp / 2 + u / 2
        wide = ulp + u
        worst_tight = max(worst_tight, float(d / tight))
        worst_wide = max(worst_wide, float(d / wide))
        if d > tight:
            outside_tight.append((n, p, float(d), float(tight)))
    print(
        f" {len(prints)} prints parsed from the issue; max |exact-print|/(ulp/2+u/2) = "
        f"{worst_tight:.3f}; max |exact-print|/(ulp+u) = {worst_wide:.3f}; prints outside the "
        f"tight span: {outside_tight or 'none'}"
    )
    p51 = prints[51]
    print(
        f" n=51 print {p51}: exact - print = {float(s593_51 - decimal(p51)):.3e}; ulp = "
        f"{math.ulp(float(decimal(p51))):.3e}"
    )

    # ---- provenance audit of every lane-backed claim in ledger.yaml
    print("\n## Provenance audit of ledger.yaml claims against the lane rows and my time table")
    ledger_yaml = yaml.safe_load((LEDGER_DIR / "ledger.yaml").read_text(encoding="utf-8"))
    lane_rows: dict[tuple[str, int, str], dict[str, Any]] = {}
    for (lane, packet, record), owner in LANES.items():
        data = lane_record(scr, lane, packet, record)
        for row in data["results"]:
            lane_rows[(owner(row), int(row["n"]), record)] = row
    problems = []
    checked = 0
    all_claims = []
    for report in ledger_yaml["reports"]:
        for cl in report["claims"]:
            all_claims.append((report["report"], cl))
            key_a = (report["report"], cl["n"], "claims.json")
            key_b = (report["report"], cl["n"], "algebraic-claims.json")
            row = (
                lane_rows.get(key_a)
                if "exact" in cl or key_b not in lane_rows
                else lane_rows.get(key_b)
            )
            if row is None:
                continue
            checked += 1
            where = f"{report['report']} n={cl['n']}"
            if "exact_side" in row:
                if Fraction(row["exact_side"]) != Fraction(cl.get("exact", "0")):
                    problems.append(
                        f"{where}: exact differs from the lane "
                        f"({cl.get('exact', '<none>')[:30]} vs {row['exact_side'][:30]})"
                    )
                offered = str(row["offered_side"])
                if "/" in offered:
                    if Fraction(offered) != Fraction(cl.get("exact", "0")):
                        problems.append(
                            f"{where}: lane offered fraction {offered[:30]} differs from the "
                            "ledger's exact"
                        )
                elif cl["printed"] != offered:
                    problems.append(
                        f"{where}: printed {cl['printed']} vs lane offered {offered}"
                    )
            else:
                if cl["printed"] != row["side_decimal"]:
                    problems.append(
                        f"{where}: printed {cl['printed']} vs lane side_decimal "
                        f"{row['side_decimal']}"
                    )
                rr = cl.get("record_relation")
                if rr and rr["relation"] != row["case"]["reported_relation"]:
                    problems.append(
                        f"{where}: record_relation {rr['relation']} vs lane "
                        f"{row['case']['reported_relation']}"
                    )
            committed = str(row["first_committed"])
            fc = TIME_FIX.get(committed, committed)
            if cl.get("first_committed") != fc:
                problems.append(
                    f"{where}: first_committed {cl.get('first_committed')} vs lane "
                    f"{row['first_committed']} (corrected {fc})"
                )
            expected_time = REPORT_TIMES[report["report"]]
            if report["report"] == "PR #574" and fc > expected_time:
                expected_time = fc
            if report["report"].startswith(("franciscouzo/", "TheSnakeFang/")):
                expected_time = fc
            if (report["report"], cl["n"]) in EDIT_TIMES:
                expected_time = EDIT_TIMES[(report["report"], cl["n"])][1]
            actual = cl.get("reported_at", report["reported_at"])
            if actual != expected_time:
                problems.append(f"{where}: reported_at {actual} vs expected {expected_time}")
    print(f" lane-backed claims checked: {checked}; problems: {len(problems)}")
    for p in problems:
        print("  ", p)
    # transcribed claims against my own transcription
    print("\n## Transcribed claims against my own sources")
    mine_t = {(r, n): (span, where) for r, n, span, _v, _fc, where in TRANSCRIBED}
    for report in ledger_yaml["reports"]:
        for cl in report["claims"]:
            key = (report["report"], cl["n"])
            if key in mine_t:
                span, where = mine_t[key]
                theirs = (
                    point(Fraction(cl["exact"]))
                    if "exact" in cl
                    else print_span(cl["printed"], cl["rounding"])
                )
                same = theirs == span
                shown = (
                    "exact " + cl["exact"][:24] + "..."
                    if "exact" in cl
                    else cl["printed"] + " (" + cl["rounding"] + ")"
                )
                ends = (
                    float(theirs.low),
                    float(theirs.high),
                    float(span.low),
                    float(span.high),
                )
                print(
                    f"  {report['report']} n={cl['n']}: ledger {shown} | mine {where[:70]} | "
                    f"{'SAME' if same else 'DIFFERENT: ' + repr(ends)}"
                )

    # ---- the random provenance sample
    print("\n## Random sample of 15 claims (seed 20261014) for the provenance table")
    times = {r["report"]: r["reported_at"] for r in ledger_yaml["reports"]}
    random.seed(20261014)
    for report, cl in random.sample(all_claims, 15):
        print(
            f"  {report} n={cl['n']}: printed={cl['printed']} rounding={cl['rounding']} "
            f"exact={'yes (' + cl['exact'][:20] + '...)' if 'exact' in cl else 'no'} "
            f"exact_from={str(cl.get('exact_from', ''))[:90]} "
            f"first_committed={cl.get('first_committed')} "
            f"reported_at={cl.get('reported_at', '<report: ' + times[report] + '>')}"
        )


if __name__ == "__main__":
    main()
