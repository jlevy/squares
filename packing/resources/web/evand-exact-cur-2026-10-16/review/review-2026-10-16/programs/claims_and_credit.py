"""The claim map and the pose measurement of T-193, for its stage 4 review.

For each of T-193's sixteen counts:

- the side: S* is the one real root of ``p`` in the file's side interval (Sturm count,
  ``independent_check.py``); exact rational bisection encloses it to width below
  ``10**-170``;
- the claim: each bound T-193's claim prints, ``s(n) <= d…`` at 40 places, is held to
  that enclosure: a correct cut has ``d <= S* < d + 10**-40`` (result-import.md: the
  decimals stand for every number that starts so); the closed forms at 126 and 295 are
  checked to be roots of ``p`` inside the interval;
- the standing sides: every member ``gather`` froze at the count in the ledger's
  ``starts.yaml`` (the case's lanes and the pending register entries) is compared
  exactly: S* is below a member when the enclosure's top is below its ``low``;
- the pose: T-193's configuration, evaluated at the field's root, is paired with the
  packing its ``regularizations`` item names (T-174's or T-186's derived fact), with
  ``devtools.check_half_angle_area.arrangement_gap`` and ``unmoved``, which decide
  nothing.

Run from ``packing/`` with the project interpreter; it reads the exact forms, the
register, the ledger and the facts as data and prints one JSON report.
"""

import gzip
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

import mpmath  # noqa: E402
import sympy  # noqa: E402
import yaml  # noqa: E402

from devtools import check_half_angle_area as area  # noqa: E402

COUNTS = (88, 102, 123, 126, 175, 199, 204, 232, 258, 259, 266, 267, 292, 295, 301, 302)
PACKET = Path("resources/web/evand-exact-cur-2026-10-16/source/search/exact/cur/data")
LEDGER = Path("campaign/issue-intake/upper-bounds-20261016/starts.yaml")
FACTS = {
    "T-174": Path("resources/web/pingyou-pr574-certificates-2026-10-13/facts"),
    "T-186": Path("resources/web/mishapolk-kkt-refinements-2026-10-14/facts"),
}
WIDTH = Fraction(1, 10**170)
CLOSED = {126: "15/2 + 3*sqrt(2)", 295: "22*(1 + sqrt(2))/3"}


def peval(coeffs, r):
    v = Fraction(0)
    for c in reversed(coeffs):
        v = v * r + c
    return v


def enclose(coeffs, lo, hi):
    slo = peval(coeffs, lo) > 0
    if (peval(coeffs, hi) > 0) == slo:
        raise SystemExit("no sign change of p on its interval")
    while hi - lo >= WIDTH:
        mid = (lo + hi) / 2
        v = peval(coeffs, mid)
        if v == 0:
            return mid, mid
        if (v > 0) == slo:
            lo = mid
        else:
            hi = mid
    return lo, hi


def poses(data):
    """Centres and (cos, sin) at the field's root, as exact binary rationals within 1e-100."""
    mpmath.mp.prec = 800
    f = [Fraction(c) for c in data["field"]["f"]]
    lo, hi = (Fraction(c) for c in data["field"]["t_interval"])
    lo, hi = enclose(f, lo, hi)
    t = (lo + hi) / 2

    def at(coeffs):
        v = mpmath.mpf(0)
        for c in reversed(coeffs):
            q = Fraction(c)
            v = v * mpmath.mpf(t.numerator) / mpmath.mpf(t.denominator) + mpmath.mpf(q.numerator) / mpmath.mpf(q.denominator)
        man, exp = v.man_exp if v != 0 else (0, 0)
        return Fraction(int(man)) * (Fraction(2) ** int(exp))

    placed = []
    for q in data["squares"]:
        u = at(q["u"])
        c, s = (1 - u * u) / (1 + u * u), 2 * u / (1 + u * u)
        for _ in range(q["m"] % 4):
            c, s = -s, c
        placed.append((at(q["x"]), at(q["y"]), c, s))
    return at(data["S"]["in_K"]), tuple(placed)


def moved_squares(data, mine, other, k):
    """Squares of the exact form whose nearest centre in ``other`` (under symmetry k) is
    more than 1e-3 away, with how many contact equations of the form name each and
    whether a coordinate of it is pinned: a diagnostic in binary64, deciding nothing."""
    mapped = [area.symmetric(other[0], square, k) for square in other[1]]
    far = [(float(u), float(v)) for u, v, _a, _b in mapped]
    contacts = [0] * len(mine[1])
    for e in data["equations"]:
        contacts[int(e[1])] += 1
        if e[0] == "C":
            contacts[int(e[3])] += 1
    pinned = {int(key[1:]) for key in data.get("pins", {})}
    out = []
    for i, (x, y, _c, _s) in enumerate(mine[1]):
        fx, fy = float(x), float(y)
        d = min(((fx - u) ** 2 + (fy - v) ** 2) ** 0.5 for u, v in far)
        if d > 1e-3:
            out.append([i, round(d, 4), contacts[i], i in pinned])
    return out


def claim_prints(register):
    entry = next(e for e in register["results"] if e.get("id") == "T-193")
    prints = {}
    for m in re.finditer(r"s\((\d+)\) <= (?:([^=,]+?) = )?([0-9]+\.[0-9]+)…", entry["claim"]):
        prints[int(m.group(1))] = (m.group(2), m.group(3))
    regs = {item["n"]: item["of"] for item in entry["regularizations"]}
    return prints, regs


def main():
    register = yaml.load(Path("frontier/results.yaml").read_text(encoding="utf-8"), Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))
    prints, regs = claim_prints(register)
    starts = {row["n"]: row["members"] for row in yaml.safe_load(LEDGER.read_text(encoding="utf-8"))["counts"]}
    pinned = Path(sys.argv[1])
    rows = []
    for n in COUNTS:
        path = PACKET / f"n-{n}.minpoly.json.gz"
        if not path.is_file():
            path = pinned / f"n-{n}.minpoly.json.gz"
        data = json.loads(gzip.decompress(path.read_bytes()).decode("utf-8"))
        p = [Fraction(int(c)) for c in data["S"]["poly"]]
        sa, sb = (Fraction(c) for c in data["S"]["interval"])
        lo, hi = enclose(p, sa, sb)
        row = {"n": n, "S_star_60": str(mpmath.mpf(lo.numerator) / lo.denominator)[:62]}
        closed, digits = prints[n]
        d = Fraction(digits)
        places = len(digits.split(".")[1])
        row["printed_places"] = places
        row["cut_correct"] = d <= lo and hi < d + Fraction(1, 10**places)
        if n in CLOSED:
            x = sympy.Symbol("x")
            form = sympy.sympify(CLOSED[n])
            pp = sum(int(c) * x**i for i, c in enumerate(data["S"]["poly"]))
            row["closed_form"] = closed
            row["closed_form_root_of_p"] = sympy.simplify(pp.subs(x, form)) == 0
            # p has one real root in [Sa, Sb], so a root of p in [Sa, Sb] is S*; decided by intervals
            mpmath.iv.prec = 600
            r2 = mpmath.iv.sqrt(2)
            value = {126: mpmath.iv.mpf(15) / 2 + 3 * r2, 295: 22 * (1 + r2) / 3}[n]
            a = mpmath.iv.mpf(sa.numerator) / sa.denominator
            b = mpmath.iv.mpf(sb.numerator) / sb.denominator
            row["closed_form_in_side_interval"] = bool((value - a).a > 0 and (b - value).a > 0)
        below = []
        for member in starts[n]:
            low = Fraction(member["low"])
            below.append({"label": member["label"], "below": hi < low, "gap_at_least": f"{float(low - hi):.3e}"})
        row["standing"] = below
        of = regs[n]
        fact = FACTS[of] / f"n-{n:03d}.yaml.gz"
        text = gzip.decompress(fact.read_bytes()).decode("utf-8")
        try:
            other = area.read_fact(text, n)
        except area.AreaRouteError:
            other = area.read_fact(text, n, labelled=True)
        mine = poses(data)
        row["of"] = of
        row["of_side_minus_S_star_at_least"] = f"{float(other[0] - hi):.3e}"
        kept = area.unmoved(mine, other)
        row["unmoved_vs_of"] = {k: kept[k] for k in kept if k in ("symmetry", "within", "one_to_one")}
        row["moved_squares"] = moved_squares(data, mine, other, kept["symmetry"])
        try:
            gap = area.arrangement_gap(mine, other)
        except area.AreaRouteError as exc:
            row["pose_vs_of"] = {"none": str(exc)}
            rows.append(row)
            print(json.dumps(row), flush=True)
            continue
        row["pose_vs_of"] = {
            "symmetry": gap["symmetry"],
            "largest_displacement": str(gap["largest_displacement"])[:14],
            "largest_orientation_sine": gap["largest_orientation_sine"],
            "moved_beyond": gap["moved_beyond"],
        }
        rows.append(row)
        print(json.dumps(row), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
