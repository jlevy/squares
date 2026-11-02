"""The quantities of the quarter-power preprint (Q), as functions of its parameters.

Written for the strongest-tier review of 2 November 2026 from the text of Q
(squarepacker/k2-minus-c-quarter abbedcf, paper/paper.tex): Definitions 3.1, 3.2 and
3.6, Theorem 10.3 (the bound Psi of (10.3)), Proposition 11.2 (conditions (i)-(iii)),
Section 11.3 (c_infinity). Every quantity is an exact-rational interval from iv.py.
Nothing here is taken from the source's programs or from a maintained checker.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from iv import Iv, cos, log, root, rpow, sqrt

DELTA = Fraction(1, 10**5)
BBAR = Fraction(15, 10**7)
BW = Fraction("2.0002")
QSTAR = Fraction("0.32")
LAMBDA = 2 * DELTA + Fraction(2, 10**12)
F050001 = Fraction("0.50001")
F10001 = Fraction("1.0001")
F100002 = Fraction("1.00002")
F1000001 = Fraction("1.000001")


def A_exact(K: int) -> Iv:
    """A = 4 sqrt(K/Q*)/(2 - 3e-6) (Definition 3.6; [R, Lemma 4.13])."""
    return 4 * sqrt(Fraction(K) / QSTAR) / (2 - Fraction(3, 10**6))


def Ap_exact(K: int) -> Iv:
    """A' = A / cos(bbar) + 1e-8 (Definition 3.6)."""
    return A_exact(K) / cos(BBAR) + Fraction(1, 10**8)


def CL_exact(K: int) -> Fraction:
    """C_Lambda = 1 + 1185.6 delta^2 (K = 9) or 1 + 1712.6 delta^2 (K = 13)."""
    return 1 + (Fraction("1185.6") if K == 9 else Fraction("1712.6")) * DELTA**2


# The rounded constants used in every explicit computation (Section 11.1, Table 2).
BARS = {
    9: (Fraction("10.6067"), Fraction("10.6068"), Fraction("1.0000002")),
    13: (Fraction("12.7476"), Fraction("12.7476"), Fraction("1.0000002")),
}


@dataclass(frozen=True)
class Params:
    c0: Fraction
    c1: Fraction
    y0: Fraction
    eps: Fraction
    om0: Fraction

    @staticmethod
    def of(c0: str, c1: str, y0: str, eps: str, om0: str) -> Params:
        return Params(Fraction(c0), Fraction(c1), Fraction(y0), Fraction(eps), Fraction(om0))


PI_STAR = Params.of("0.3078", "0.2754", "42108000000", "5.8e-6", "1.7e-5")
PI_STAR_13 = Params.of("0.3674", "0.3012", "60000000000", "5e-6", "1.4e-5")


def constraints(p: Params, k: Fraction | None) -> dict[str, bool | None]:
    """(C0)-(C7), (Q1), (Q2) of Definition 3.2, exactly where they are rational."""
    c0, c1, y0, eps, om0 = p.c0, p.c1, p.y0, p.eps, p.om0
    out: dict[str, bool | None] = {}
    out["C0"] = c0 > 0 and c1 > 0 and y0.denominator == 1 and y0 > 0 and 0 < eps < 1 and om0 > 0
    out["C1"] = c0**2 <= BBAR**2 * y0
    out["C2"] = c1**4 <= Fraction(15, 10**7) ** 4 * y0**3
    out["C3"] = c1**4 < c0**4 * y0 * (1 - eps) ** 3
    out["C4"] = om0 < Fraction(1, 2)
    w0 = derived(p)["w0"]
    out["C5"] = True if w0.hi < Fraction(1, 2) else (False if w0.lo >= Fraction(1, 2) else None)
    amax = c0 / sqrt(y0)
    rhs = cos(2 * amax) / 2
    out["C6"] = True if DELTA <= rhs.lo else (False if DELTA > rhs.hi else None)
    out["C7"] = None if k is None else (y0 + 1 <= (1 - eps) * (Fraction(k) / 2 - 3))
    out["Q1"] = c0**2 <= Fraction(1, 10**6) * y0
    out["Q2"] = c1**4 <= Fraction(1, 10**16) * ((1 - eps) * y0) ** 3
    return out


def derived(p: Params) -> dict[str, Iv]:
    """The k-independent derived quantities of Definition 3.1."""
    c0, c1, y0, eps = p.c0, p.c1, p.y0, p.eps
    bstar = c1 / rpow((1 - eps) * y0, 3, 4)
    w0 = F050001 * c0**2 * (1 + F10001 / y0) + DELTA + F10001 * bstar + Fraction(1, 10**12)
    return {
        "alpha_y0": c0 / sqrt(y0),
        "betahat_y0": c1 / rpow(y0, 3, 4),
        "bstar": bstar,
        "w0": w0,
        "h0": 1 - 2 * w0,
    }


def invF(p: Params, bw: Fraction = BW) -> Iv:
    m = rpow(1 - p.eps, 3, 4)
    return 4 * m * (1 - m) / (3 * p.eps * (1 + bw / (p.eps * p.y0)))


def model(
    p: Params,
    k: Fraction | int,
    A: object,
    Ap: object,
    CL: object,
    cstar: Fraction = Fraction(1, 10),
    bw: Fraction = BW,
    wall_factor: Fraction = Fraction(1),
) -> dict[str, Iv]:
    """Psi_pi(k) of (10.3) and the quantities of Proposition 11.2 and Table 3.

    A, Ap, CL may be exact intervals or the rounded bars; `bw` and `wall_factor`
    serve the sensitivity record of Section 12.6 ((e) and (f))."""
    c0, c1, y0, eps, om0 = p.c0, p.c1, p.y0, p.eps, p.om0
    A, Ap, CL = Iv.of(A), Iv.of(Ap), Iv.of(CL)
    d = derived(p)
    h0 = d["h0"]
    iF = invF(p, bw)
    gamma = F100002 * (2 * c1 * A / sqrt(y0) + Fraction(4, 5) * c1**2 / DELTA / rpow(y0, 5, 4))
    cwall = 4 * c1 / (c0 * iF)
    kw = cwall * F1000001 * c0**2
    t1 = 1 / (om0 * rpow(y0, 3, 4))
    t2 = A / (2 * c1)
    t3 = 2 * c1 / (c0 * iF) * (Ap + d["alpha_y0"] * CL / DELTA)
    B = t1 + t2 + t3 + gamma
    kq = Fraction(k)
    y1 = kq / 2 - 3
    lH = 8 * h0 * (root((1 - eps) * y1, 4) - root(y0 + 1, 4))
    L = log(y1 / y0) + Fraction(2) / y0
    om_bound = F1000001 * c0**2 * L
    wall = wall_factor * cwall * om_bound
    numerator = (1 - om0) * lH - wall
    psi = numerator / B
    D1 = h0 * (1 - om0) * root(1 - eps, 4) / B - cstar / (4 * rpow(2, 3, 4))
    return {
        **d,
        "invF": iF,
        "Gamma": gamma,
        "Cwall": cwall,
        "KW": kw,
        "t1": t1,
        "t2": t2,
        "t3": t3,
        "B": B,
        "lH_bound": lH,
        "Omega_bound": om_bound,
        "wall": wall,
        "numerator": numerator,
        "Psi": psi,
        "rhs_i": cstar * root(kq, 4),
        "D1": D1,
        "iii_lhs": root(y1, 4) * D1,
        "iii_rhs": wall_factor * kw / (2 * B),
        "Psi_inf": 8 * rpow(2, -1, 4) * h0 * (1 - om0) * root(1 - eps, 4) / B,
        "eps_y0": Iv(eps * y0),
        "C7_lhs": Iv((1 - eps) * y1),
        "C3_lhs": c1 / rpow(1 - eps, 3, 4),
        "C3_rhs": c0 * root(y0, 4),
    }


def conditions(m: dict[str, Iv]) -> dict[str, bool | None]:
    """Conditions (i)-(iii) of Proposition 11.2, certified on intervals."""

    def ge(a: Iv, b: Iv) -> bool | None:
        if a.lo >= b.hi:
            return True
        if a.hi < b.lo:
            return False
        return None

    return {
        "i": ge(m["Psi"], m["rhs_i"]),
        "ii": True if m["D1"].lo > 0 else (False if m["D1"].hi <= 0 else None),
        "iii": ge(m["iii_lhs"], m["iii_rhs"]),
    }


def c_inf(A: object, Ap: object) -> Iv:
    """c_infinity of (11.4): 16 2^(-1/4) (1-lambda)^(5/4) / (5 5.0001^(1/4) sqrt(A A'))."""
    A, Ap = Iv.of(A), Iv.of(Ap)
    return 16 * rpow(2, -1, 4) * rpow(1 - LAMBDA, 5, 4) / (5 * root(Fraction("5.0001"), 4) * sqrt(A * Ap))


def c0_opt() -> Iv:
    return sqrt((1 - LAMBDA) / Fraction("5.0001"))
