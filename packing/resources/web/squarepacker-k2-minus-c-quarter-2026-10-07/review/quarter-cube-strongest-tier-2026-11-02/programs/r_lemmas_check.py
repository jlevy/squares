"""The finite check of [R, Lemma 4.9] and the numbers of [R, Lemmas 4.8-4.10, Prop. 4.5].

[R] is Ryu's k2-minus-c version 1.2 (squarepacker/k2-minus-c e16a5cf,
paper/paper.tex, retained in squarepacker-k2-minus-c-v12-2026-10-06). Theorem A13 of
the quarter-power preprint and Theorem 1.2 of the cube-root preprint rest on the
analytic Lemma 4.9 in place of the computer-assisted Lemma 4.10; its proof ends in a
finite check of angle conditions, "part of the accompanying script". This program
redoes that check from the text, on exact-rational intervals, and recomputes the
numerical claims of the proofs of Lemmas 4.8, 4.9 (parts (a)-(c)) and 4.10 and of
Proposition 4.5 that the two preprints inherit. It reads [R]'s text only; the source's
scripts were not read or run.

Usage: python -I r_lemmas_check.py OUT.json
"""

from __future__ import annotations

import itertools
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # run with python -I

from checks import Recorder
from iv import PI, Iv, arccos, arcsin, root, sin, sqrt

F = Fraction
DEG = PI / 180


def deg(x: Iv) -> Iv:
    return x / DEG


def main(out: Path) -> int:
    r = Recorder("r_lemmas_check.py")
    d = F(1, 10**4)
    s2 = sqrt(F(2))
    Lam = d + s2
    rho1 = sqrt((d + s2 / 2) ** 2 + F(1, 4))
    R0 = sqrt(Lam * Lam + F(1, 4))
    r.below("R4.8-R0", "[R] L605", "R0 = sqrt(Lambda^2 + 1/4) at d = 1e-4", R0, "1.5001")
    # Lemma 4.8(a): area argument.
    r.below("R4.8a-sq", "[R] L642", "(12/pi) Lambda + 4", 12 / PI * Lam + 4, "10")
    r.below("R4.8a-wall", "[R] L646", "(12/pi)(d + sqrt2/2) + 2", 12 / PI * (d + s2 / 2) + 2, "5")
    # Lemma 4.8(b).
    c0 = d + s2 / 2 - F(1, 2)
    r.below("R4.8b-c0", "[R] L659", "c0 = d + sqrt2/2 - 1/2", c0, "0.20721")
    phi = arccos(c0 / R0)
    area = R0 * R0 * (PI - phi) + c0 * sqrt(R0 * R0 - c0 * c0)
    per = 2 * R0 * (PI - phi) + 2 * sqrt(R0 * R0 - c0 * c0)
    r.below("R4.8b-area", "[R] L661", "area of D0", area, "4.155")
    r.below("R4.8b-per", "[R] L661", "perimeter of D0", per, "8.1")
    r.below("R4.8b-oler", "[R] L662", "(2/sqrt3) 4.155 + 8.1/2 + 1", 2 / sqrt(F(3)) * F("4.155") + F("8.1") / 2 + 1, "9.85")
    r.below("R4.8b-1.58", "[R] L665", "sqrt((d+sqrt2/2)^2 + 1/4) + d + sqrt2/2", rho1 + d + s2 / 2, "1.58")
    # Lemma 4.9.
    r.below("R4.9-rho1", "[R] L684", "rho1 at d = 1e-4", rho1, "0.86611")
    r.below("R4.9-rho1b", "[R] L684", "rho1", rho1, "0.8662")
    fL = 1 - 1 / (2 * Lam * Lam)
    r.fact("R4.9a-corners", "[R] L696", "on [1, Lambda]^2 the corner values of f are 1/2, Lambda/2, 1 - 1/(2 Lambda^2), "
           "the last the largest", (Lam / 2).hi < fL.lo and F(1, 2) < fL.lo)
    g0 = arccos(fL)
    r.above("R4.9-g0", "[R] L715", "gamma0 in degrees", deg(g0), "41.406")
    r.above("R4.9a-78", "[R] L701", "arccos(d + sqrt2/2 - 1/2) in degrees", deg(arccos(c0)), "78")
    r.fact("R4.9a-D5", "[R] L705", "pi < 5 gamma0, so D(r) <= 5", PI.hi < (5 * g0).lo)
    Rm = {2: rho1}
    for m in (3, 4, 5):
        cand = 1 / (2 * sin((m - 1) * g0 / 2))
        Rm[m] = cand if cand.hi <= rho1.lo else (rho1 if rho1.hi <= cand.lo else None)
        if Rm[m] is None:
            raise ArithmeticError(f"R_{m} undecided")
    r.below("R4.9b-R3", "[R] L715", "R3", Rm[3], "0.75598")
    r.below("R4.9b-R4", "[R] L715", "R4", Rm[4], "0.56571")
    r.below("R4.9b-R5", "[R] L715", "R5", Rm[5], "0.50396")

    def f(r1: Iv, r2: Iv) -> Iv:
        return (r1 * r1 + r2 * r2 - 1) / (2 * r1 * r2)

    gam: dict[tuple[int, int], Iv] = {}
    for a in range(2, 6):
        for b in range(2, 6):
            fab = f(Rm[a], Rm[b])
            if fab.lo < -1 or fab.hi > 1:
                raise ArithmeticError("f out of range")
            # arccos on [-1, 1] by symmetry: arccos(-x) = pi - arccos(x).
            if fab.lo >= 0:
                gam[(a, b)] = arccos(fab)
            elif fab.hi <= 0:
                gam[(a, b)] = PI - arccos(-fab)
            else:
                raise ArithmeticError("f straddles 0")
    r.above("R4.9b-g22", "[R] L715", "gamma(2,2) in degrees", deg(gam[(2, 2)]), "70.52")
    r.fact("R4.9b-g22-min", "[R] L715", "gamma(a,b) >= gamma(2,2) for all classes",
           all(gam[k].lo >= gam[(2, 2)].lo - F(1, 10**100) for k in gam))
    r.fact("R4.9b-n5", "[R] L716", "6 gamma(2,2) > 2 pi, so n <= 5", (6 * gam[(2, 2)]).lo > (2 * PI).hi)
    two_pi = 2 * PI
    worst_margin_15 = None
    sat14: list[tuple[int, ...]] = []
    undecided = 0
    n_seq = 0
    for n in (3, 4, 5):
        for seq in itertools.product((2, 3, 4, 5), repeat=n):
            n_seq += 1
            s = sum(seq)
            if s < 14:
                continue
            tot = Iv(0)
            for i in range(n):
                tot = tot + gam[(seq[i], seq[(i + 1) % n])]
            violates = tot.lo > two_pi.hi
            satisfies = tot.hi <= two_pi.lo
            if not (violates or satisfies):
                undecided += 1
            if s >= 15:
                if not violates:
                    worst_margin_15 = "FAIL"
                elif worst_margin_15 != "FAIL":
                    mg = deg(tot - two_pi)
                    worst_margin_15 = mg if worst_margin_15 is None or mg.lo < worst_margin_15.lo else worst_margin_15
            elif s == 14 and satisfies:
                sat14.append(seq)
    r.fact("R4.9b-undecided", "[R] L716-719", "every sequence with sum >= 14 is decided on intervals", undecided == 0)
    ok15 = isinstance(worst_margin_15, Iv) and worst_margin_15.lo > 25
    r.fact("R4.9b-15", "[R] L716-718", "every sequence with sum >= 15 violates the angle conditions by more than 25 degrees",
           ok15, worst_margin_15 if isinstance(worst_margin_15, Iv) else None)

    def canon(seq: tuple[int, ...]) -> tuple[int, ...]:
        rots = [seq[i:] + seq[:i] for i in range(len(seq))]
        return min(rots)

    classes = sorted({canon(sq) for sq in sat14})
    r.fact("R4.9b-14", "[R] L718-719", "the only sequences with sum 14 that satisfy them are the rotations of (5,2,5,2)",
           classes == [(2, 5, 2, 5)])
    tot5252 = gam[(5, 2)] * 2 + gam[(2, 5)] * 2
    t5 = deg(tot5252)
    r.fact("R4.9b-359", "[R] L718", "(5,2,5,2) uses about 359 degrees (to nearest), below 360",
           t5.lo >= F("358.5") and t5.hi < 360, t5)
    r.fact("R4.9b-n<=2", "[R] L713", "for n <= 2, sum of classes <= 10", 2 * 5 <= 10)
    # Part (c): two centres of class 5.
    g55 = gam[(5, 5)]
    r.above("R4.9c-g55", "[R] L725", "gamma(5,5) in degrees", deg(g55), "165.6")
    r.below("R4.9c-2R5", "[R] L725", "2 R5", 2 * Rm[5], "1.008")
    r.fact("R4.9c-2R5<L", "[R] L730", "2 R5 < Lambda", (2 * Rm[5]).hi < Lam.lo)
    psi = arcsin(Rm[5] * sin(PI - g55))
    r.below("R4.9c-psi", "[R] L727", "psi = arcsin(R5 sin(pi - gamma(5,5))) in degrees", deg(psi), "7.19")
    arc = 90 + deg(psi) - deg(g0)
    r.fact("R4.9c-arcs", "[R] L734", "90 + 7.19 - 41.406 < 2 gamma0", (F(90) + F("7.19") - F("41.406")) < (2 * deg(g0)).lo, arc)
    # Lemma 4.10: n <= 5 for centres in (1/2, rho1] at mutual distance >= 1.
    r.fact("R4.10-n", "[R] L752-753", "at most 5 centres within rho1 of p at mutual distance >= 1 "
           "(gamma(2,2) bounds the angle at p, as in Lemma 4.9(b))", (6 * gam[(2, 2)]).lo > (2 * PI).hi)

    # Proposition 4.5.
    eps1 = 2 * F(1, 10**5)
    eps0 = F(1, 10**4)

    def rho(h: Fraction) -> Iv:
        return sqrt(1 + Iv(h) * Iv(h))

    def Dh(h: Fraction) -> Iv:
        return F(1, 2) - (1 - Iv(h)) / (2 * rho(h))

    def chi(h: Fraction) -> Iv:
        return 1 + rho(h) / 2 - (1 + Iv(h)) / rho(h)

    r.below("R4.5-rho", "[R] L496", "rho_h at h = 1 + eps1", rho(1 + eps1), "1.415")
    r.below("R4.5d-rhoh/h", "[R] L496", "rho_h/h at h = 1 (the largest for h > 1)", rho(F(1)) / 1, "1.4143")
    r.below("R4.5f-D", "[R] L510", "D(0.344)", Dh(F("0.344")), "0.19")
    chis = max(chi(F("0.344")).hi, chi(1 + eps1).hi) + F("2.2") * eps1
    r.below("R4.5g-chi*", "[R] L555", "max(chi(0.344), chi(1.00002)) + 2.2 eps1", Iv(chis), "0.29295")
    # h_c: the positive root of h^3 + 3h - 2, inside [0.344, 1].
    r.fact("R4.5g-hc", "[R] L554", "h^3 + 3h - 2 changes sign once on [0.344, 1] (chi has one minimum there)",
           F("0.344") ** 3 + 3 * F("0.344") - 2 < 0 < 1 + 3 - 2)
    chi_star = Iv(F("0.29295"))
    b2 = (2 - chi_star) ** 2 / 9
    b3 = F(2, 3) * (1 - chi_star) ** 2
    r.above("R4.5g-b1", "[R] L557", "1/3", Iv(F(1, 3)), "0.3237")
    r.above("R4.5g-b2", "[R] L558", "(2 - chi*)^2/9 at chi* = 0.29295", b2, "0.3237")
    r.above("R4.5g-b3", "[R] L559", "(2/3)(1 - chi*)^2 at chi* = 0.29295", b3, "0.3237")
    beta1 = 3 * F("1.415") * eps1
    r.below("R4.5g-beta1", "[R] L560", "beta1 = 3 gamma* = 3 (1.415 eps1)", Iv(beta1), "8.5e-5")
    r.above("R4.5g-0.3235", "[R] L560", "0.3237 - 2.04 beta1", Iv(F("0.3237") - F("2.04") * beta1), "0.3235")
    r.above("R4.5g-Q*", "[R] L561", "0.3235 - 4 eps0", Iv(F("0.3235") - 4 * eps0), "0.32")
    r.above("R4.5g-0.38", "[R] L550", "(1 - 0.3812)^2", Iv((1 - F("0.3812")) ** 2), "0.38")
    r.above("R4.5g-0.38b", "[R] L551", "0.38 - 4 eps0", Iv(F("0.38") - 4 * eps0), "0.32")
    r.above("R4.5b-wall", "[R] L465", "(1 - 2 eps0)^2", Iv((1 - 2 * eps0) ** 2), "0.32")
    r.below("R4.5d-gamma*", "[R] L560", "1.5 gamma* in units of eps1 (< 2.13)", Iv(F("1.5") * F("1.415")), "2.13")
    r.below("R4.5f-1.1", "[R] L530", "1.1 eps1 < eps0", Iv(F("1.1") * eps1), str(eps0))
    r.below("R4.5f-1.8", "[R] L539", "1.8 eps1 < eps0", Iv(F("1.8") * eps1), str(eps0))

    rec = r.write(out, {"sequences_enumerated": n_seq, "sum14_satisfying_rotation_classes": [list(c) for c in classes],
                        "gamma_degrees": {f"{a}{b}": [float(deg(v).lo), float(deg(v).hi)] for (a, b), v in gam.items()}})
    print(f"r_lemmas_check: {rec['summary']}")
    print("not proved:", [row["id"] for row in r.rows if row["needed"] is not True])
    print("display false:", [row["id"] for row in r.rows if row.get("display") is False])
    print("worst margin (sum>=15), degrees:", float(worst_margin_15.lo) if isinstance(worst_margin_15, Iv) else worst_margin_15)
    print("sum-14 classes:", classes, "5252:", float(deg(tot5252).lo))
    return 0 if all(row["needed"] is True for row in r.rows) else 1


if __name__ == "__main__":
    raise SystemExit(main(Path(sys.argv[1])))
