#!/usr/bin/env python3
"""Every algebraic step of Kevin Fang's Theorem A note (v0.2), decided symbolically.

Stage 4 mathematical review of issue #797, lane c-review-797-math, 25 October 2026.
Written from the note alone (note/main.tex, SHA-256 f6f26d7b...1152) before its author
read any program of the source or the maintained cases/asymptotic/fang_theorem_a.py.

Each check is an identity or a polynomial inequality that the proof uses for every k,
decided by sympy (exact rational arithmetic, no floating point). An identity is checked
by simplifying the difference of its two sides to 0; an inequality by an explicit
factorisation or sum of terms whose sign is evident, and sampled exactly as a guard.
The receipt lists every check with its outcome. Run:

    python3 -I fang_a_identities.py --out identities.json

Exit status 0 when every check holds.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

import sympy as sp

b, t, k, u, v, y, L, F, i, R = sp.symbols("b t k u v y L F i R", real=True)
x = sp.symbols("x", positive=True)  # x = sqrt(2k)

CHECKS: list[dict[str, object]] = []


def record(name: str, where: str, ok: bool, detail: str = "") -> None:
    CHECKS.append({"check": name, "note": where, "holds": bool(ok), "detail": detail})


def zero(expr: sp.Expr) -> bool:
    return sp.simplify(sp.together(sp.expand(expr))) == 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    # Section 2: the band, with c, s from t = tan(theta/2).
    c = (1 - t**2) / (1 + t**2)
    s = 2 * t / (1 + t**2)
    tan = s / c
    tau = c / s
    sec = 1 / c
    W = b * c + s
    h = b * s + c
    eta = b / 2 - tau

    record("c^2 + s^2 = 1", "S2, l.66", zero(c**2 + s**2 - 1))
    t0 = 1 / b
    at0 = {t: t0}
    record("c0 = (b^2-1)/(b^2+1)", "S2, l.70", zero(c.subs(at0) - (b**2 - 1) / (b**2 + 1)))
    record("s0 = 2b/(b^2+1)", "S2, l.70", zero(s.subs(at0) - 2 * b / (b**2 + 1)))
    record("tau0 = (b^2-1)/(2b)", "S2, l.70", zero(tau.subs(at0) - (b**2 - 1) / (2 * b)))
    record("W0 = b", "S2, l.70", zero(W.subs(at0) - b))
    record("h0 = (3b^2-1)/(b^2+1)", "S2, l.70", zero(h.subs(at0) - (3 * b**2 - 1) / (b**2 + 1)))
    record("3 - h0 = 4/(b^2+1) > 0", "S2, l.70", zero(3 - h.subs(at0) - 4 / (b**2 + 1)))
    # W < b for t > 1/b: the note argues by dW/dtheta = c - b s; here W - b in closed form.
    record(
        "W - b = 2t(1 - bt)/(1+t^2), so W < b for every t > 1/b",
        "S2, l.70",
        zero(W - b - 2 * t * (1 - b * t) / (1 + t**2)),
        "a direct form of the note's derivative argument",
    )
    th = sp.symbols("theta", real=True)
    Wth = b * sp.cos(th) + sp.sin(th)
    record("dW/dtheta = c - b s", "S2, l.70", zero(sp.diff(Wth, th) - (sp.cos(th) - b * sp.sin(th))))

    # (R1), (R2), (E1): a point of row j in row 0's frame (u, v).
    X = s + u * c - v * s
    Y = y + u * s + v * c
    record("(R1) X - s = uc - vs", "S2, l.74", zero(X - s - (u * c - v * s)))
    record("(R1) X - s = -s at (u,v)=(0,1) and = bc at (b,0)", "S2, l.74",
           zero((X - s).subs({u: 0, v: 1}) + s) and zero((X - s).subs({u: b, v: 0}) - b * c))
    # Shift (0, sec): change in u = (0, sec).(c, s), change in v = (0, sec).(-s, c).
    record("(R2) the shift (0, sec) moves v by 1", "S2, l.74", zero(sec * c - 1))
    record("(R2) the shift (0, sec) moves u by tan", "S2, l.74", zero(sec * s - tan))
    record("(R3) highest point of a row is y + h (u=b, v=1)", "S2, l.74", zero(Y.subs({u: b, v: 1}) - y - h))
    record("(E1) Y - y - (X - s)T = v c + v s^2/c = v/c", "S2, l.76",
           zero(Y - y - (X - s) * tan - (v * c + v * s**2 / c)) and zero(v * c + v * s**2 / c - v / c))
    record("(E1) Y - y - (s - X)/T = u s + u c^2/s = u/s", "S2, l.76",
           zero(Y - y - (s - X) / tan - (u * s + u * c**2 / s)) and zero(u * s + u * c**2 / s - u / s))
    # (E2): l(a_i) = i + 1 when a_i = s + (i + 1 - y) tau >= s.
    a_i = s + (i + 1 - y) * tau
    record("(E2) l(a_i) = y + (a_i - s)T = i + 1", "S2, l.78", zero(y + (a_i - s) * tan - (i + 1)))
    # (E3): the rotation about (W/2, L/2) maps row j to a row of lift y1 + (R-1-j) sec.
    y0, j = sp.symbols("y0 j", real=True)
    Xj = s + u * c - v * s
    Yj = y0 + j * sec + u * s + v * c
    up, vp = b - u, 1 - v
    y1 = L - y0 - (R - 1) * sec - h
    record("(E3) rotated row j has X = s + u'c - v's with u'=b-u, v'=1-v", "S2, l.80",
           zero((W - Xj) - (s + up * c - vp * s)))
    record("(E3) rotated row j has Y = y1 + (R-1-j)sec + u's + v'c", "S2, l.80",
           zero((L - Yj) - (y1 + (R - 1 - j) * sec + up * s + vp * c)))

    # Section 3: the count identity behind (1).
    kk, bb, SS, C1, C2 = sp.symbols("k b S C1 C2", real=True)
    waste = kk**2 - ((kk - bb) ** 2 + C1 + C2)
    rhs1 = bb * (kk - SS) + (bb * SS - C1) + (bb * (kk - bb) - C2)
    record("(1) k^2 - [(k-b)^2 + C(S) + C(k-b)] equals the right side of (1)", "S3, l.94-96",
           zero(waste - rhs1))

    # Section 4: the closeness conditions at t0.
    delta_b = sp.Rational(1, 2) + 1 / (2 * b) - 2 * b / (b**2 + 1)
    record("W0 - s0 - tau0 = (b-1)/2 + delta_b", "S4, l.108",
           zero((W - s - tau).subs(at0) - (b - 1) / 2 - delta_b))
    # delta_b > 0 iff b^3 - 3b^2 + b + 1 > 0 (multiply by 2b(b^2+1) > 0).
    record("2b(b^2+1) delta_b = b^3 - 3b^2 + b + 1 = (b-1)(b^2-2b-1)", "S4, l.108",
           zero(2 * b * (b**2 + 1) * delta_b - (b**3 - 3 * b**2 + b + 1))
           and zero(b**3 - 3 * b**2 + b + 1 - (b - 1) * (b**2 - 2 * b - 1)),
           "for b >= 3: b - 1 >= 2 and b^2 - 2b - 1 = (b-1)^2 - 2 >= 2, so delta_b > 0")
    record("delta_b < 1 for b >= 1 (delta_b < 1/2 + 1/(2b) <= 1)", "S4, l.108",
           zero(sp.Rational(1, 2) + 1 / (2 * b) - delta_b - 2 * b / (b**2 + 1)))
    record("eta0 = 1/(2b)", "S4, l.101", zero(eta.subs(at0) - 1 / (2 * b)))
    record("2 tau0 - b c0 = (b^2-1)/(b(b^2+1))", "S4, l.108",
           zero((2 * tau - b * c).subs(at0) - (b**2 - 1) / (b * (b**2 + 1))))

    # Lemma 2.
    record("s + (1 - sec) tau = c(1-c)/s", "Lemma 2, l.120", zero(s + (1 - sec) * tau - c * (1 - c) / s))
    z = W - s - 2 * tau + y * tau
    record("W - a_0(y) = z + tau and W - a_1(y) = z", "Lemma 2, l.122",
           zero(W - (s + (1 - y) * tau) - (z + tau)) and zero(W - (s + (2 - y) * tau) - z))
    record("tau = (b-1)/2 + 1/2 - eta", "Lemma 2, l.122", zero(tau - ((b - 1) / 2 + sp.Rational(1, 2) - eta)))
    # The floor pairing: z = n + f, 0 <= f < 1, 0 <= eta < 1/2.
    n_, f_, e_ = sp.symbols("n f e", real=True)
    zz = n_ + f_
    # case f < 1/2 + e: floor(z) + floor(z + 1/2 - e) = 2n, and 2n - (2z - 1 - 2e) = 1 + 2e - 2f.
    record("floor pairing, case f < 1/2+eta: 2n - (2z-1-2eta) = 1 + 2eta - 2f > 0", "Lemma 2, l.122",
           zero(2 * n_ - (2 * zz - 1 - 2 * e_) - (1 + 2 * e_ - 2 * f_)))
    record("floor pairing, case f >= 1/2+eta: (2n+1) - (2z-1) = 2 - 2f > 0", "Lemma 2, l.122",
           zero(2 * n_ + 1 - (2 * zz - 1) - (2 - 2 * f_)))
    # Exhaustive exact guard of the floor pairing on a rational grid with every tie.
    bad = 0
    grid = [Fraction(p, 240) for p in range(0, 240)]
    etas = [Fraction(p, 240) for p in range(0, 120)]
    for e in etas:
        for f in grid + [Fraction(1, 2) + e, Fraction(1, 2) + e - Fraction(1, 10**30)]:
            if not 0 <= f < 1:
                continue
            for n in (-3, 0, 5):
                zv = n + f
                lhs = (zv.numerator // zv.denominator) + ((zv + Fraction(1, 2) - e).numerator
                                                          // (zv + Fraction(1, 2) - e).denominator)
                if not lhs > 2 * zv - 1 - 2 * e:
                    bad += 1
    record("floor pairing on 240 x 120 rational grid (with f = 1/2+eta and just below)",
           "Lemma 2, l.122", bad == 0, f"{bad} failures")

    # Lemma 3.
    Rr = 1 + c * (L - h - F)
    record("bR = b + bc(L - h - F) when F = L - (R-1)sec - h", "Lemma 3, l.136",
           zero(b * Rr - (b + b * c * (L - h - F))) and zero(L - (Rr - 1) * sec - h - F))
    Bs, Cs, Hs, Ws, Ss, Ts, Es, Ls, Fs = sp.symbols("b c h W s tau eta L F", real=True)
    zF = Ws - Ss - 2 * Ts + Fs * Ts
    C_lower = Bs * (1 + Cs * (Ls - Hs - Fs)) + (Bs - 1) / 2 + ((Bs - 1) / 2 + 2 * zF - 1 - 2 * Es)
    rhs2 = Bs * Ls * (1 - Cs) + Bs * Cs * Hs - 2 * Bs + 2 - 2 * (Ws - Ss - 2 * Ts) + 2 * Es
    record("Lemma 3: bL - C_lower - RHS(2) = F(bc - 2tau), as a polynomial identity",
           "Lemma 3, l.130-136", zero(Bs * Ls - C_lower - rhs2 - Fs * (Bs * Cs - 2 * Ts)),
           "so (c) 2tau - bc >= 0 and F >= 0 give bL - C(L) < RHS(2)")
    RHS2_t = b * L * (1 - c) + b * c * h - 2 * b + 2 - 2 * (W - s - 2 * tau) + 2 * eta
    kappa = (7 * b**4 + 1) / (b * (b**2 + 1) ** 2)
    record("RHS(2) at t0 = 2bL/(b^2+1) + b + 2 - kappa_b", "Lemma 3, l.132",
           zero(RHS2_t.subs(at0) - (2 * b * L / (b**2 + 1) + b + 2 - kappa)))
    record("1 - c0 = 2/(b^2+1)", "Lemma 3, l.136", zero(1 - c.subs(at0) - 2 / (b**2 + 1)))
    record("b c0 h0 = 3b - b(10b^2+2)/(b^2+1)^2", "Lemma 3, l.136",
           zero((b * c * h).subs(at0) - (3 * b - b * (10 * b**2 + 2) / (b**2 + 1) ** 2)))
    record("W0 - s0 - 2tau0 = -(b^2-1)/(b(b^2+1))", "Lemma 3, l.136",
           zero((W - s - 2 * tau).subs(at0) + (b**2 - 1) / (b * (b**2 + 1))))

    # Section 5.
    S_t = k - b + W
    H_t = b * (k - S_t) + RHS2_t.subs(L, S_t) + RHS2_t.subs(L, k - b)
    Bk = 4 * k * b / (b**2 + 1) + 2 * b + 2 + 2 / (b**2 + 1) - 2 * kappa
    record("H(t0) = B(k) (H is a rational function of t, continuous at t0)", "S5, l.143-145",
           zero(H_t.subs(at0) - Bk))
    record("S(t0) = k", "S5, l.143", zero(S_t.subs(at0) - k))
    record("4k/b - 4kb/(b^2+1) = 4k/(b(b^2+1)) > 0", "S5, l.147",
           zero(4 * k / b - 4 * k * b / (b**2 + 1) - 4 * k / (b * (b**2 + 1))))
    record("4k/b + 2b = 4 sqrt(2k) + (2/b)(b - sqrt(2k))^2, with x = sqrt(2k)", "S5, l.147",
           zero(4 * (x**2 / 2) / b + 2 * b - 4 * x - 2 / b * (b - x) ** 2))
    record("B(k) = 4x + (2/b)(b-x)^2 + 2 + 2/(b^2+1) - 2 kappa_b - 4k/(b(b^2+1)), x = sqrt(2k)",
           "S5, l.147-149",
           zero(Bk.subs(k, x**2 / 2) - (4 * x + 2 / b * (b - x) ** 2 + 2 + 2 / (b**2 + 1)
                                        - 2 * kappa - 4 * (x**2 / 2) / (b * (b**2 + 1)))),
           "with (b-x)^2 <= 1: B(k) <= 4x + 2 - 2(kappa - 1/b - 1/(b^2+1)) - 4k/(b(b^2+1))")
    poly = sp.expand(b * (b**2 + 1) ** 2 * (kappa - 1 / b - 1 / (b**2 + 1)))
    record("b(b^2+1)^2 (kappa - 1/b - 1/(b^2+1)) = 6b^4 - b^3 - 2b^2 - b", "S5, l.151",
           zero(poly - (6 * b**4 - b**3 - 2 * b**2 - b)))
    record("6b^4 - b^3 - 2b^2 - b = b(b-1)(6b^2+5b+3) + 2b > 0 for b >= 1", "S5, l.151",
           zero(6 * b**4 - b**3 - 2 * b**2 - b - (b * (b - 1) * (6 * b**2 + 5 * b + 3) + 2 * b)))
    record("k - sqrt(2k) - 1 >= 3 iff (k-2)(k-8) >= 0 (k >= 4)", "S5, l.141",
           zero((k - 4) ** 2 - 2 * k - (k - 2) * (k - 8)))

    # The sharpness remark: 4 sqrt(2k) + 2 - 4b at k = (b^2 - b + 8)/2.
    m = sp.symbols("m", positive=True)  # m = 1/b
    expr = 4 * sp.sqrt(1 - m + 8 * m**2) / m + 2 - 4 / m  # 4 sqrt(b^2 - b + 8) + 2 - 4b
    ser = sp.series(expr, m, 0, 3).removeO()
    record("4 sqrt(2k) + 2 - 4b = 31/(2b) + O(b^-2) at k = (b^2-b+8)/2", "Remark, l.154",
           zero(sp.expand(ser) - (sp.Rational(31, 2) * m + sp.expand(ser).coeff(m, 2) * m**2)),
           f"series in 1/b: {sp.expand(ser)}")

    # Controls: mutated identities that the same test must refuse.
    controls = {
        "kappa with 7b^4 - 1 in place of 7b^4 + 1": zero(
            RHS2_t.subs(at0) - (2 * b * L / (b**2 + 1) + b + 2 - (7 * b**4 - 1) / (b * (b**2 + 1) ** 2))),
        "Lemma 3 with the F term's sign flipped": zero(
            Bs * Ls - C_lower - rhs2 + Fs * (Bs * Cs - 2 * Ts)),
        "W0 = b - 1/b": zero(W.subs(at0) - (b - 1 / b)),
        "6b^4 - b^3 - 2b^2 + b in place of ... - b": zero(poly - (6 * b**4 - b**3 - 2 * b**2 + b)),
    }
    control_rows = [{"control": name, "refused": not held} for name, held in controls.items()]

    ok = all(item["holds"] for item in CHECKS) and all(row["refused"] for row in control_rows)
    receipt = {
        "program": Path(__file__).name,
        "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "python": sys.version.split()[0],
        "sympy": sp.__version__,
        "checks": CHECKS,
        "controls": control_rows,
        "all_hold": ok,
        "count": len(CHECKS),
    }
    for row in control_rows:
        print(("refused " if row["refused"] else "ACCEPTED") + f"  control: {row['control']}")
    args.out.write_text(json.dumps(receipt, indent=1) + "\n")
    for item in CHECKS:
        print(("ok  " if item["holds"] else "FAIL") + f"  {item['check']}  [{item['note']}]")
    print(f"{sum(1 for c in CHECKS if c['holds'])}/{len(CHECKS)} hold")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
