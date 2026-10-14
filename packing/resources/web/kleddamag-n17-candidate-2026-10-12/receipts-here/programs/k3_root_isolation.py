"""K3 independent exact root isolation for the #557 statement (Kleddamag, s(17) = L).

Written for lane K3 without reading the author's endpoint programs. Reads STATEMENT.md
literally, parses F and G with SymPy, and decides with exact rational interval
arithmetic (fractions.Fraction only):

1. Krawczyk test on the statement's box [t0 +- 1e-12] x [b0 +- 1e-12]: K(B) inside int(B)
   proves exactly one simultaneous zero of (F, G) in B.
2. Exact Newton refinement and a second Krawczyk test on a radius-1e-45 box that lies in B,
   so the refined box holds the same unique zero.
3. Denominator 1 + 2t - t^2 > 0 on the refined box, and an outward enclosure of
   L = (6 + 4t)/(1 + 2t - t^2), compared with the statement's 20-place bounds, the
   record's 34-place ceiling and the 16-place rational witness side.
4. A second route with SymPy: Res_b(F, G) squarefree, Sturm count of its real roots in
   the t-range of B equals 1.
5. Control: F with its t coefficient changed by 1 must fail the Krawczyk test on B.
6. Comparison of F and G with the record's exp-237 chart polynomials.

Usage: python k3_root_isolation.py STATEMENT.md EXP237_CERTIFICATE.json [N017_PAGE.md]
7. With the n-017 page: the catalogue degree-18 polynomial vanishes at L exactly (the
   minimal polynomial of t* divides its lift under S = (6+4t)/(1+2t-t^2)).
Prints one JSON object; exit 0 only if every check holds.
"""

import json
import re
import sys
from fractions import Fraction as Q

import sympy
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

T, B = sympy.symbols("t b")
TRANSFORMS = standard_transformations + (implicit_multiplication_application, convert_xor)

STATEMENT_LO = Q("4.67553009360455095163")
STATEMENT_HI = Q("4.67553009360455095164")
RECORD_CEILING = Q("4.6755300936045509516342148538535054")
WITNESS_SIDE = Q(4675530093604551, 10**15)

Poly2 = dict[tuple[int, int], Q]
Interval = tuple[Q, Q]


def parse_statement(text: str) -> tuple[Q, Q, Poly2, Poly2]:
    t0 = re.search(r"\$t_0=(\d+)/10\^\{(\d+)\}\$", text)
    b0 = re.search(r"\$b_0=(\d+)/10\^\{(\d+)\}\$", text)
    f = re.search(r"\$F\(t,b\)=(.+?)\$", text)
    g = re.search(r"\$G\(t,b\)=(.+?)\$", text)
    if not (t0 and b0 and f and g):
        raise ValueError("statement did not parse")
    tq = Q(int(t0.group(1)), 10 ** int(t0.group(2)))
    bq = Q(int(b0.group(1)), 10 ** int(b0.group(2)))
    polys = []
    for m in (f, g):
        expr = parse_expr(m.group(1), local_dict={"t": T, "b": B}, transformations=TRANSFORMS)
        poly = sympy.Poly(sympy.expand(expr), T, B)
        polys.append({k: Q(int(v.p), int(v.q)) for k, v in poly.as_dict().items()})
    return tq, bq, polys[0], polys[1]


def deriv(p: Poly2, var: int) -> Poly2:
    out: Poly2 = {}
    for (i, j), c in p.items():
        e = (i, j)[var]
        if e:
            key = (i - 1, j) if var == 0 else (i, j - 1)
            out[key] = out.get(key, Q(0)) + c * e
    return out


def ev(p: Poly2, t: Q, b: Q) -> Q:
    return sum((c * t**i * b**j for (i, j), c in p.items()), Q(0))


def ev_box(p: Poly2, ti: Interval, bi: Interval) -> Interval:
    """Outward enclosure; requires both intervals strictly positive (monotone powers)."""
    if ti[0] <= 0 or bi[0] <= 0:
        raise ValueError("box must be positive")
    lo = hi = Q(0)
    for (i, j), c in p.items():
        mlo = ti[0] ** i * bi[0] ** j
        mhi = ti[1] ** i * bi[1] ** j
        if c > 0:
            lo += c * mlo
            hi += c * mhi
        else:
            lo += c * mhi
            hi += c * mlo
    return lo, hi


def imul(a: Interval, b: Interval) -> Interval:
    products = (a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1])
    return min(products), max(products)


def krawczyk(f: Poly2, g: Poly2, mt: Q, mb: Q, r: Q) -> dict:
    jac = [[deriv(f, 0), deriv(f, 1)], [deriv(g, 0), deriv(g, 1)]]
    jm = [[ev(jac[i][k], mt, mb) for k in range(2)] for i in range(2)]
    det = jm[0][0] * jm[1][1] - jm[0][1] * jm[1][0]
    if det == 0:
        return {"passed": False, "reason": "singular midpoint Jacobian"}
    y = [[jm[1][1] / det, -jm[0][1] / det], [-jm[1][0] / det, jm[0][0] / det]]
    fm = [ev(f, mt, mb), ev(g, mt, mb)]
    tbox, bbox = (mt - r, mt + r), (mb - r, mb + r)
    jb = [[ev_box(jac[i][k], tbox, bbox) for k in range(2)] for i in range(2)]
    radius = (-r, r)
    mid = (mt, mb)
    kbox = []
    for i in range(2):
        centre = mid[i] - (y[i][0] * fm[0] + y[i][1] * fm[1])
        lo = hi = centre
        for k in range(2):
            # (I - Y J(B))_{ik}, as an interval
            elo = ehi = Q(1 if i == k else 0)
            for m in range(2):
                part = imul((y[i][m], y[i][m]), jb[m][k])
                elo -= part[1]
                ehi -= part[0]
            term = imul((elo, ehi), radius)
            lo += term[0]
            hi += term[1]
        kbox.append((lo, hi))
    inside = all(mid[i] - r < kbox[i][0] and kbox[i][1] < mid[i] + r for i in range(2))
    margin = min(
        min(kbox[i][0] - (mid[i] - r), (mid[i] + r) - kbox[i][1]) / r for i in range(2)
    )
    return {"passed": inside, "kbox": kbox, "relative_margin": float(margin)}


def newton(f: Poly2, g: Poly2, t: Q, b: Q, steps: int, digits: int) -> tuple[Q, Q]:
    jac = [[deriv(f, 0), deriv(f, 1)], [deriv(g, 0), deriv(g, 1)]]
    scale = 10**digits
    for _ in range(steps):
        a, bb, c, d = (ev(jac[i][k], t, b) for i in range(2) for k in range(2))
        det = a * d - bb * c
        fv, gv = ev(f, t, b), ev(g, t, b)
        t, b = t - (d * fv - bb * gv) / det, b - (-c * fv + a * gv) / det
        t = Q(round(t * scale), scale)
        b = Q(round(b * scale), scale)
    return t, b


def l_enclosure(ti: Interval) -> tuple[Interval, Interval]:
    # 1 + 2t - t^2 is increasing for t < 1; the box lies in (0, 1).
    if not (0 < ti[0] and ti[1] < 1):
        raise ValueError("t range outside (0,1)")
    den = (1 + 2 * ti[0] - ti[0] ** 2, 1 + 2 * ti[1] - ti[1] ** 2)
    num = (6 + 4 * ti[0], 6 + 4 * ti[1])
    return den, (num[0] / den[1], num[1] / den[0])


def main() -> int:
    statement = open(sys.argv[1], encoding="utf-8").read()
    record = json.load(open(sys.argv[2], encoding="utf-8"))
    t0, b0, f, g = parse_statement(statement)
    r = Q(1, 10**12)
    out: dict = {"t0": str(t0), "b0": str(b0), "radius": "1/10^12"}

    rec_polys = [
        {(int(i), int(j)): Q(c) for i, j, c in poly} for poly in record["polynomials"]
    ]
    rec_mid = [Q(x) for x in record["box"]["midpoint"]]
    out["matches_record_exp237"] = {
        "F": rec_polys[0] == f,
        "G": rec_polys[1] == g,
        "midpoint": rec_mid == [t0, b0],
        "radius": Q(record["box"]["radius"]) == r,
    }

    k1 = krawczyk(f, g, t0, b0, r)
    out["krawczyk_statement_box"] = {"passed": k1["passed"], "relative_margin": k1["relative_margin"]}

    tn, bn = newton(f, g, t0, b0, steps=8, digits=120)
    rho = Q(1, 10**45)
    in_box = abs(tn - t0) + rho < r and abs(bn - b0) + rho < r
    k2 = krawczyk(f, g, tn, bn, rho)
    out["krawczyk_refined_box"] = {
        "radius": "1/10^45",
        "inside_statement_box": in_box,
        "passed": k2["passed"],
        "relative_margin": k2["relative_margin"],
        "t_mid_60": f"{float(tn):.17g}",
    }
    tk = k2["kbox"][0]
    den, lint = l_enclosure((tk[0], tk[1]))
    out["denominator_positive"] = den[0] > 0
    out["L_enclosure_width"] = float(lint[1] - lint[0])
    out["L_40_digits"] = str(sympy.Float(sympy.Rational(lint[0].numerator, lint[0].denominator), 45))
    out["statement_bounds_hold"] = STATEMENT_LO < lint[0] and lint[1] < STATEMENT_HI
    out["record_ceiling_ge_L"] = lint[1] <= RECORD_CEILING
    out["record_ceiling_minus_L_lower"] = float(RECORD_CEILING - lint[1])
    out["witness_side_minus_L_lower"] = float(WITNESS_SIDE - lint[1])
    out["witness_side_gt_L"] = lint[1] < WITNESS_SIDE

    # Second route: resultant and Sturm count in the t-range of the statement box.
    fp = sympy.Poly(sum(sympy.Rational(c.numerator, c.denominator) * T**i * B**j for (i, j), c in f.items()), B)
    gp = sympy.Poly(sum(sympy.Rational(c.numerator, c.denominator) * T**i * B**j for (i, j), c in g.items()), B)
    res = sympy.Poly(sympy.resultant(fp.as_expr(), gp.as_expr(), B), T)
    sqf = sympy.Poly(sympy.quo(res, sympy.gcd(res, res.diff(T))), T)
    lo_t = sympy.Rational((t0 - r).numerator, (t0 - r).denominator)
    hi_t = sympy.Rational((t0 + r).numerator, (t0 + r).denominator)
    out["resultant"] = {
        "degree": res.degree(),
        "squarefree_degree": sqf.degree(),
        "real_roots_in_t_range": int(sqf.count_roots(lo_t, hi_t)),
        "nonzero_at_endpoints": bool(sqf.eval(lo_t) != 0 and sqf.eval(hi_t) != 0),
    }

    # Exact identity: the catalogue degree-18 polynomial P (n-017.md) vanishes at L.
    # Factor Res_b(F,G) over Q, take the unique factor with a root in the t-range, and
    # test that it divides den^18 * P((6+4t)/den) exactly.
    if len(sys.argv) > 3:
        page = open(sys.argv[3], encoding="utf-8").read()
        m = re.search(r"minimal_polynomial: (.+)=0", page)
        s = sympy.Symbol("s")
        cat = sympy.Poly(
            parse_expr(
                m.group(1).replace("^{", "^(").replace("}", ")"),
                local_dict={"s": s},
                transformations=TRANSFORMS,
            ),
            s,
        )
        factors = [fac for fac, _ in sympy.factor_list(res.as_expr(), T)[1]]
        hits = [sympy.Poly(fac, T) for fac in factors if sympy.Poly(fac, T).count_roots(lo_t, hi_t) > 0]
        den_t = 1 + 2 * T - T**2
        lifted = sympy.Poly(
            sympy.expand(sum(c * (6 + 4 * T) ** k * den_t ** (18 - k) for (k,), c in cat.as_dict().items())),
            T,
        )
        out["catalogue_identity"] = {
            "catalogue_degree": cat.degree(),
            "t_factors_with_root_in_box": [h.degree() for h in hits],
            "min_poly_t_degree": hits[0].degree() if len(hits) == 1 else None,
            "divides_lifted_catalogue": len(hits) == 1 and lifted.rem(hits[0]).is_zero,
            "catalogue_irreducible_over_Q": len(sympy.factor_list(cat.as_expr(), s)[1]) == 1
            and sympy.factor_list(cat.as_expr(), s)[1][0][1] == 1,
        }

    # Control: change the coefficient of t in F by 1.
    fc = dict(f)
    fc[(1, 0)] = fc.get((1, 0), Q(0)) + 1
    kc = krawczyk(fc, g, t0, b0, r)
    out["control_perturbed_F_passed"] = kc["passed"]

    ok = (
        all(out["matches_record_exp237"].values())
        and k1["passed"]
        and in_box
        and k2["passed"]
        and out["denominator_positive"]
        and out["statement_bounds_hold"]
        and out["record_ceiling_ge_L"]
        and out["witness_side_gt_L"]
        and out["resultant"]["real_roots_in_t_range"] == 1
        and not kc["passed"]
        and ("catalogue_identity" not in out or out["catalogue_identity"]["divides_lifted_catalogue"])
    )
    out["result"] = "PROVED" if ok else "NOT PROVED"
    print(json.dumps(out, indent=1, default=str))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
