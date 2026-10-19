"""Independent check of Evan Daniel's #639 exact forms, for the stage 4 review of T-193.

Written for the review; it shares no code with the source's ``verify_exact.py`` (which
its author read first) and decides each file again with other arithmetic:

- the count: ``n`` equals the count in the file name and the number of squares listed;
- the field: SymPy decides that ``f`` is squarefree and irreducible over Q and has
  exactly one real root in the file's ``t_interval`` (Sturm count); exact rational
  bisection then narrows that interval to width below ``10**-WIDTH_DIGITS``;
- the configuration: every centre, angle parameter and the side are enclosed at that
  root with mpmath interval arithmetic at ``PREC`` bits; each corner's four box margins
  and, for each pair not separated by circumscribed discs, the margins of the other
  square's corners against each side line of either square, are enclosed;
  an enclosure above 0 is a strict inequality, and one inside ``(-ZERO, ZERO)`` is
  accepted only if the margin is exactly 0 in K = Q[t]/f, decided by SymPy over Q with
  ``1 + u^2`` inverted modulo ``f``;
- the side: ``p(S) = 0`` in K exactly, ``p`` irreducible over Q (``factor_list``: one
  factor, multiplicity one, full degree) and squarefree, exactly one real root of ``p``
  in the file's side interval (Sturm count), and the enclosure of ``S(t*)`` inside it.

Controls (``--controls``) mutate the exact data by ``10**-30`` and must be refused: a
wall-touching square moved through its wall, a square of a touching pair moved into its
neighbour along the contact normal, and the side lowered in K.

Run from ``packing/`` with the project interpreter, ``python -I``, on copies of the
gzip files; it reads them as data and writes one JSON report.
"""

import argparse
import gzip
import json
import re
import sys
import time
from fractions import Fraction
from pathlib import Path

import sympy
from mpmath import iv
from sympy import QQ, Poly, Symbol

PREC = 1400
WIDTH_DIGITS = 260
ZERO = 1e-150
T = Symbol("t")
X = Symbol("x")


def fr(value):
    return Fraction(value)


def qpoly(coeffs):
    """A polynomial over Q from a low-to-high coefficient list."""
    items = [QQ(fr(c).numerator, fr(c).denominator) for c in reversed(coeffs)]
    return Poly.from_list(items or [QQ(0)], T, domain=QQ)


def ivq(value):
    q = fr(value)
    return iv.mpf(q.numerator) / iv.mpf(q.denominator)


def horner_iv(coeffs, tt):
    v = iv.mpf(0)
    for c in reversed(coeffs):
        v = v * tt + ivq(c)
    return v


def sign_at(coeffs, r):
    v = Fraction(0)
    for c in reversed(coeffs):
        v = v * r + c
    return (v > 0) - (v < 0)


def narrow(coeffs, lo, hi):
    """Exact bisection of a sign-change interval of the polynomial to width < 10^-WIDTH_DIGITS."""
    if lo == hi:
        if sign_at(coeffs, lo) != 0:
            raise ValueError("t interval is a point that is not a root of f")
        return lo, hi
    slo, shi = sign_at(coeffs, lo), sign_at(coeffs, hi)
    if slo * shi >= 0:
        raise ValueError("no strict sign change of f on the t interval")
    eps = Fraction(1, 10**WIDTH_DIGITS)
    while hi - lo >= eps:
        mid = (lo + hi) / 2
        sm = sign_at(coeffs, mid)
        if sm == 0:
            return mid, mid
        if sm == slo:
            lo = mid
        else:
            hi = mid
    return lo, hi


def kind(g):
    """'gt' if the enclosure is above 0, 'zero?' if inside (-ZERO, ZERO), else 'bad'."""
    if g.a > 0:
        return "gt"
    if abs(float(g.a)) < ZERO and abs(float(g.b)) < ZERO:
        return "zero?"
    return "bad"


class Refused(Exception):
    pass


class Field:
    """Exact arithmetic in Q[t]/f, elements as reduced SymPy polynomials."""

    def __init__(self, fcoeffs):
        self.f = qpoly(fcoeffs)
        self.inverses = {}

    def el(self, coeffs):
        return qpoly(coeffs).rem(self.f)

    def mul(self, a, b):
        return (a * b).rem(self.f)

    def cs(self, ucoeffs, m):
        key = tuple(str(c) for c in ucoeffs)
        if key not in self.inverses:
            u = self.el(ucoeffs)
            uu = self.mul(u, u)
            inv = (uu + 1).invert(self.f)
            self.inverses[key] = (self.mul(1 - uu, inv), self.mul(2 * u, inv))
        c, s = self.inverses[key]
        for _ in range(m % 4):
            c, s = -s, c
        return c, s


CORNERS = ((1, 1), (-1, 1), (-1, -1), (1, -1))


def check(data, name_n):
    started = time.process_time()
    iv.prec = PREC
    out = {"n": data["n"], "name_n": name_n, "squares_listed": len(data["squares"])}
    if data["n"] != name_n or len(data["squares"]) != name_n:
        raise Refused(f"count: n = {data['n']}, file name {name_n}, {len(data['squares'])} squares")
    n = name_n
    fco = [fr(c) for c in data["field"]["f"]]
    fpoly = qpoly(fco)
    out["field_degree"] = fpoly.degree()
    out["f_irreducible"] = bool(fpoly.is_irreducible)
    out["f_squarefree"] = sympy.gcd(fpoly, fpoly.diff(T)).degree() == 0
    ta, tb = (fr(c) for c in data["field"]["t_interval"])
    out["f_roots_in_t_interval"] = int(fpoly.count_roots(QQ(ta.numerator, ta.denominator), QQ(tb.numerator, tb.denominator)))
    lo, hi = narrow(fco, ta, tb)
    tt = iv.mpf([ivq(lo).a, ivq(hi).b])
    K = Field(fco)
    sq = []
    for q in data["squares"]:
        x, y, u = horner_iv(q["x"], tt), horner_iv(q["y"], tt), horner_iv(q["u"], tt)
        den = 1 + u * u
        c, s = (1 - u * u) / den, 2 * u / den
        for _ in range(q["m"] % 4):
            c, s = -s, c
        sq.append((x, y, c, s))
    side = horner_iv(data["S"]["in_K"], tt)

    exact = {}

    def ex(k):
        if k not in exact:
            q = data["squares"][k]
            c, s = K.cs(q["u"], q["m"])
            exact[k] = (K.el(q["x"]), K.el(q["y"]), c, s)
        return exact[k]

    side_exact = K.el(data["S"]["in_K"])
    half = QQ(1, 2)

    def corner_iv(k):
        x, y, c, s = sq[k]
        return [(x + (c * a - s * b) / 2, y + (s * a + c * b) / 2) for a, b in CORNERS]

    def corner_ex(k, idx):
        x, y, c, s = ex(k)
        a, b = CORNERS[idx]
        return (x + (c * a - s * b) * half, y + (s * a + c * b) * half)

    cor = [corner_iv(k) for k in range(n)]
    box = {"gt": 0, "identity": 0}
    least_box = None
    for k in range(n):
        for idx, (px, py) in enumerate(cor[k]):
            for wall, g in enumerate((px, side - px, py, side - py)):
                r = kind(g)
                if r == "gt":
                    box["gt"] += 1
                    v = float(g.a)
                    least_box = v if least_box is None else min(least_box, v)
                    continue
                if r == "zero?":
                    ex_x, ex_y = corner_ex(k, idx)
                    e = (ex_x, side_exact - ex_x, ex_y, side_exact - ex_y)[wall]
                    if e.is_zero:
                        box["identity"] += 1
                        continue
                raise Refused(f"square {k} corner {idx} wall {wall}: margin {float(g.a):.3g}..{float(g.b):.3g}")
    pairs = {"disc": 0, "strict": 0, "touching": 0, "identities": 0}
    least_gap = None
    least_gap_pair = None
    contacts = []
    mid = [(float(x.a), float(y.a)) for x, y, _, _ in sq]
    for i in range(n):
        for j in range(i + 1, n):
            dxf, dyf = mid[j][0] - mid[i][0], mid[j][1] - mid[i][1]
            if dxf * dxf + dyf * dyf > 2.25:
                dx, dy = sq[j][0] - sq[i][0], sq[j][1] - sq[i][1]
                if (dx * dx + dy * dy - 2).a >= 0:
                    pairs["disc"] += 1
                    continue
            best_strict = None
            touch = []
            for own, oth in ((i, j), (j, i)):
                ox, oy, c, s = sq[own]
                for nidx, (nx, ny) in enumerate(((c, s), (-s, c), (-c, -s), (s, -c))):
                    gs = [nx * (px - ox) + ny * (py - oy) - 0.5 for px, py in cor[oth]]
                    ks = [kind(g) for g in gs]
                    if all(r == "gt" for r in ks):
                        v = min(float(g.a) for g in gs)
                        best_strict = v if best_strict is None else max(best_strict, v)
                    elif all(r != "bad" for r in ks):
                        touch.append((own, oth, nidx, ks))
            if best_strict is not None:
                pairs["strict"] += 1
                if least_gap is None or best_strict < least_gap:
                    least_gap, least_gap_pair = best_strict, (i, j)
                continue
            for own, oth, nidx, ks in touch:
                ox, oy, c, s = ex(own)
                nx, ny = ((c, s), (-s, c), (-c, -s), (s, -c))[nidx]
                ok = True
                for idx, r in enumerate(ks):
                    if r == "zero?":
                        px, py = corner_ex(oth, idx)
                        e = (K.mul(nx, px - ox) + K.mul(ny, py - oy) - half).rem(K.f)
                        if not e.is_zero:
                            ok = False
                            break
                if ok:
                    pairs["touching"] += 1
                    pairs["identities"] += sum(1 for r in ks if r == "zero?")
                    contacts.append((own, oth, nidx, [idx for idx, r in enumerate(ks) if r == "zero?"]))
                    break
            else:
                raise Refused(f"pair ({i}, {j}): no separating side line proved")
    out["box"] = box
    out["least_strict_box_margin"] = least_box
    out["pairs"] = pairs
    out["least_strict_pair_gap"] = least_gap
    out["least_strict_pair"] = least_gap_pair
    # the side
    pco = [int(c) for c in data["S"]["poly"]]
    ppoly = Poly(list(reversed(pco)), X, domain="ZZ")
    acc = Poly(0, T, domain=QQ)
    for c in reversed(pco):
        acc = (K.mul(acc, side_exact) + QQ(c)).rem(K.f)
    if not acc.is_zero:
        raise Refused("p(S) is not 0 in K")
    out["p_of_S_zero_in_K"] = True
    content, factors = sympy.factor_list(ppoly)
    out["p_degree"] = ppoly.degree()
    out["p_factors"] = [[int(Poly(q, X).degree()), int(mult)] for q, mult in factors]
    out["p_irreducible"] = len(factors) == 1 and int(factors[0][1]) == 1 and int(Poly(factors[0][0], X).degree()) == ppoly.degree()
    out["p_squarefree"] = sympy.gcd(ppoly, ppoly.diff(X)).degree() == 0
    sa, sb = (fr(c) for c in data["S"]["interval"])
    out["p_roots_in_S_interval"] = int(ppoly.count_roots(QQ(sa.numerator, sa.denominator), QQ(sb.numerator, sb.denominator)))
    inside = (side - ivq(sa)).a >= 0 and (ivq(sb) - side).a >= 0
    if not inside:
        raise Refused("S(t*) not inside the side interval")
    out["S_in_interval"] = True
    out["S_enclosure_lo"] = iv.nstr(side.a, 80)
    out["S_enclosure_hi"] = iv.nstr(side.b, 80)
    out["S_enclosure_width"] = float(side.delta)
    out["contacts_sample"] = contacts[:3]
    out["cpu_seconds"] = round(time.process_time() - started, 2)
    return out, contacts


STEP = Fraction(1, 10**30)


def controls(data, name_n, contacts):
    """Three mutations by 1e-30, each of which must be refused."""
    results = []
    wall_touch = next(e for e in data["equations"] if e[0] == "W")
    k, wall = int(wall_touch[1]), str(wall_touch[3])
    coord, sign = {"L": ("x", -1), "R": ("x", 1), "B": ("y", -1), "T": ("y", 1)}[wall]
    d1 = json.loads(json.dumps(data))
    d1["squares"][k][coord][0] = str(fr(d1["squares"][k][coord][0]) + sign * STEP)
    results.append(("wall", f"square {k} moved 1e-30 through its {wall} wall", d1))
    own, oth, nidx, _ = contacts[0]
    d2 = json.loads(json.dumps(data))
    # move `oth` toward `own` along the contact normal, approximated by a rational
    nx_ny = _normal_approx(data, own, nidx)
    for coord_name, comp in zip(("x", "y"), nx_ny):
        d2["squares"][oth][coord_name][0] = str(fr(d2["squares"][oth][coord_name][0]) - STEP * comp)
    results.append(("contact", f"square {oth} moved 1e-30 into square {own} across their contact", d2))
    d3 = json.loads(json.dumps(data))
    d3["S"]["in_K"][0] = str(fr(d3["S"]["in_K"][0]) - STEP)
    results.append(("side", "the side lowered by 1e-30 in K", d3))
    out = []
    for label, what, mutated in results:
        try:
            check(mutated, name_n)
            out.append({"control": label, "mutation": what, "refused": False})
        except Refused as exc:
            out.append({"control": label, "mutation": what, "refused": True, "reason": str(exc)})
    return out


def _normal_approx(data, own, nidx):
    """The contact normal of square `own`, as rationals within 1e-20 (direction only)."""
    iv.prec = 200
    lo, hi = (fr(c) for c in data["field"]["t_interval"])
    tt = iv.mpf([ivq(lo).a, ivq(hi).b])
    u = horner_iv(data["squares"][own]["u"], tt)
    den = 1 + u * u
    c, s = (1 - u * u) / den, 2 * u / den
    for _ in range(data["squares"][own]["m"] % 4):
        c, s = -s, c
    nx, ny = ((c, s), (-s, c), (-c, -s), (s, -c))[nidx]
    iv.prec = PREC
    return Fraction(float(nx.a)).limit_denominator(10**12), Fraction(float(ny.a)).limit_denominator(10**12)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--controls", action="store_true")
    ap.add_argument("--json", required=True)
    args = ap.parse_args(argv)
    report = {"program": "independent_check.py", "prec_bits": PREC, "t_width_digits": WIDTH_DIGITS, "zero_band": ZERO,
              "sympy": sympy.__version__, "python": sys.version.split()[0], "rows": []}
    path_out = Path(args.json)
    if path_out.is_file():
        report = json.loads(path_out.read_text())
    done = {row["file"] for row in report["rows"]}
    status = 0
    for name in args.files:
        path = Path(name)
        if path.name in done:
            continue
        name_n = int(re.match(r"n-(\d+)\.minpoly\.json\.gz$", path.name).group(1))
        data = json.loads(gzip.decompress(path.read_bytes()).decode("utf-8"))
        wall0 = time.time()
        row = {"file": path.name}
        try:
            result, contacts = check(data, name_n)
            row.update(result)
            row["verdict"] = "packing"
            if args.controls:
                row["controls"] = controls(data, name_n, contacts)
        except Refused as exc:
            row["verdict"] = "refused"
            row["reason"] = str(exc)
            status = 1
        row["wall_seconds"] = round(time.time() - wall0, 1)
        report["rows"].append(row)
        path_out.write_text(json.dumps(report, indent=1))
        print(path.name, row["verdict"], row.get("pairs"), row.get("box"), "least box", row.get("least_strict_box_margin"),
              "least gap", row.get("least_strict_pair_gap"), "p irr", row.get("p_irreducible"),
              "ctl", [c["refused"] for c in row.get("controls", [])], f"{row['wall_seconds']} s", flush=True)
    return status


if __name__ == "__main__":
    sys.exit(main())
