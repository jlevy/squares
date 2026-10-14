"""Independent exact checks of the literal facts the proof text uses in sections 3-6.

Usage: python3 -I literal_checks.py SRC_ROOT
Every number is an exact rational. Each check prints OK/FAIL and the value found.
"""
import json
import os
import re
import sys
from fractions import Fraction as Fr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geom_util import (U, C_CAP, RHO, poly, rect, ccw, mirror_x, d4_image, D4, clip_box, diam2, bbox,
                       strictly_separated, point_in, contains, rot, cmul, cconj, vcross, vdot, lift)

SRC = sys.argv[1]
CAP = os.path.join(SRC, "research/finishing-threshold-goal-20261007/clean-rerun-20261011/current-build-0122/capture/statements")
fails = []


def same_poly(P, Q):
    return sorted(P) == sorted(Q)



def check(cond, text):
    print(("OK   " if cond else "FAIL ") + text)
    if not cond:
        fails.append(text)


def load_cls(name, path=None):
    p = path or os.path.join(CAP, name, "classes.json")
    with open(p, "r", encoding="utf-8") as fh:
        d = json.load(fh)
    out = {"symmetry": d["symmetry"], "bound": Fr(d["bound"]), "classes": {}}
    for c in d["classes"]:
        slots = []
        for s in c["slots"]:
            slots.append((ccw(poly(s["centre"]["polygon"])), (Fr(s["angle_tan_half"][0]), Fr(s["angle_tan_half"][1]))))
        out["classes"][c["name"]] = (Fr(c["threshold"]), slots)
    return out


def slot_images(slots, symmetry):
    """all (polygon, gate) images of the slots under the file's symmetry (as the checker reads a class)"""
    out = []
    for P, (lo, hi) in slots:
        if symmetry == "fixed":
            out.append((P, (lo, hi)))
        elif symmetry == "mirror_x":
            out.append((P, (lo, hi)))
            out.append((mirror_x(P), (-hi, -lo)))
        elif symmetry == "orbit":
            for k, g in enumerate(D4):
                det = g[0][0] * g[1][1] - g[0][1] * g[1][0]
                out.append((d4_image(P, g), (lo, hi) if det == 1 else (-hi, -lo)))
    return out


DELTA = (U - C_CAP) / 2
PHYS = (DELTA + Fr(1, 2), U - DELTA - Fr(1, 2))     # physical centre box in the frame, side C
print("delta =", DELTA, " physical centre box", PHYS)
check(PHYS == (Fr(1000469, 2000000), Fr(8351531, 2000000)), "physical centre box equals [1000469/2000000, 8351531/2000000] (P054)")

# ---- rho > tan(pi/8)
check(RHO * RHO + 2 * RHO - 1 > 0, "rho^2 + 2 rho - 1 = %s > 0, so 2 atan(rho) > pi/4 (P040, P050)" % (RHO * RHO + 2 * RHO - 1))

# ---- marker hexagon
L3 = load_cls("L_3")
M_hex = L3["classes"]["M"][1][0][0]
x0, x1, y0, y1 = bbox(M_hex)
check((x1 - x0) ** 2 + (y1 - y0) ** 2 == Fr(493, 1250), "marker hexagon bounding-box diameter^2 = %s (= 493/1250 claimed, P040)" % ((x1 - x0) ** 2 + (y1 - y0) ** 2))
check(diam2(M_hex) < 1, "marker hexagon diameter^2 = %s < 1" % diam2(M_hex))
check(x0 + x1 == U, "marker hexagon x-range symmetric about U/2 (reflection-invariant, P040/P047)")
check(mirror_x(M_hex) == M_hex or sorted(mirror_x(M_hex)) == sorted(M_hex), "marker hexagon is invariant under x -> U - x as a point set")
HALF_GATE = L3["classes"]["M"][1][0][1]
check(HALF_GATE == (Fr(0), RHO), "L_3's marker M is the half-marker: gate [0, rho]")

# ---- FRAME files
F0506 = load_cls("FRAME_0506"); F1114 = load_cls("FRAME_1114"); F0917 = load_cls("FRAME_0917"); FM = load_cls("FRAME_MARKER")
for name, F in (("FRAME_0506", F0506), ("FRAME_1114", F1114), ("FRAME_0917", F0917)):
    check(F["symmetry"] == "mirror_x", name + " symmetry mirror_x")
check(F0506["bound"] == Fr(137, 8) and F1114["bound"] == Fr(137, 8) and F0917["bound"] == Fr(145, 8), "frame bounds 137/8, 137/8, 145/8 (P039)")
check(FM["symmetry"] == "orbit" and FM["bound"] == 17 and list(FM["classes"].values())[0][0] == 0, "FRAME_MARKER: orbit symmetry, bound 17, threshold 0 (P039)")
check(FM["classes"]["marker_orbit_exempt"][1][0][0] == M_hex and FM["classes"]["marker_orbit_exempt"][1][0][1] == (-RHO, RHO), "FRAME_MARKER class is the hexagon with all directions")


def union_images(F, cname):
    thr, slots = F["classes"][cname]
    return thr, slot_images(slots, F["symmetry"])


def all_disjoint(A, B):
    return all(strictly_separated(P, Q) for P, _ in A for Q, _ in B)


# FRAME_0506: high M (BOX) vs low T_side-W0, with mirror images
thrM, highs = union_images(F0506, "M"); thrT, lows = union_images(F0506, "T_side-W0")
check(thrM == Fr(5, 4) and thrT == Fr(7, 8), "FRAME_0506 thresholds 5/4 (BOX) and 7/8 (W0/E0)")
check(all(g == (-RHO, RHO) for _, g in highs + lows), "FRAME_0506 all gates are all-direction [-rho, rho]")
check(all_disjoint(highs, lows), "FRAME_0506: high union and low union strictly disjoint (q = 0 in P041)")
check(contains(F0506["classes"]["M"][1][0][0], M_hex), "FRAME_0506 BOX contains the marker hexagon (so the marker occupant counts in m)")
bonus0506 = [P for P, _ in lows]
# FRAME_1114
thrM, highs1114 = union_images(F1114, "M"); thrT, lows1114 = union_images(F1114, "T_interior-W")
check(thrM == Fr(5, 4) and thrT == Fr(7, 8), "FRAME_1114 thresholds 5/4 (HEX) and 7/8 (IW/IE)")
check(all_disjoint(highs1114, lows1114), "FRAME_1114: high union and low union strictly disjoint")
check(F1114["classes"]["M"][1][0][0] == M_hex, "FRAME_1114 HEX equals the marker hexagon")
bonus1114 = [P for P, _ in lows1114]
# FRAME_0917
thrH, hex0917 = union_images(F0917, "M"); thrV, V = union_images(F0917, "T_region17")
thrB1, B1114 = union_images(F0917, "BONUS_1114"); thrB0, B0506 = union_images(F0917, "BONUS_0506")
check((thrH, thrB1, thrB0, thrV) == (Fr(5, 4), Fr(5, 4), Fr(5, 4), Fr(7, 8)), "FRAME_0917 thresholds: HEX, BONUS_1114, BONUS_0506 at 5/4; L9/L17 union at 7/8")
check(sorted(P for P, _ in B0506) == sorted(bonus0506), "BONUS_0506 (with mirror) equals FRAME_0506's low union (with mirror) as polygons")
check(sorted(P for P, _ in B1114) == sorted(bonus1114), "BONUS_1114 (with mirror) equals FRAME_1114's low union (with mirror) as polygons")
check(F0917["classes"]["M"][1][0][0] == M_hex, "FRAME_0917 HEX equals the marker hexagon")
highs0917 = hex0917 + B1114 + B0506
check(all_disjoint(hex0917, B1114) and all_disjoint(hex0917, B0506) and all_disjoint(B1114, B0506), "FRAME_0917: HEX, BONUS_1114, BONUS_0506 pairwise strictly disjoint (h >= 1+2+2)")
check(all_disjoint(highs0917, V), "FRAME_0917: high union strictly disjoint from V = L9 u L17 (12 separations claimed)")
L17 = F0917["classes"]["T_region17"][1][0][0]
L9 = mirror_x(L17)
check(same_poly(L9, rect(Fr(-131, 250), Fr(4501, 5000), Fr(24137, 10000), Fr(29637, 10000))), "L9 = mirror of T_region17 = [-131/250,4501/5000]x[24137/10000,29637/10000] (P042)")
check(strictly_separated(L9, L17), "L9 and L17 strictly disjoint")
for nm, P in (("L9", L9), ("L17", L17)):
    Q = clip_box(P, PHYS[0], PHYS[1], PHYS[0], PHYS[1])
    check(diam2(Q) <= Fr(11566501, 25000000) and diam2(Q) < 1, "%s clipped to the physical box: diameter^2 = %s <= 11566501/25000000 < 1" % (nm, diam2(Q)))
# counting consequences (pure arithmetic)
check(all(17 + Fr(m, 4) - Fr(t, 8) >= Fr(137, 8) for m in range(1, 18) for t in range(0, 2 * m)), "17 + m/4 - t/8 < 137/8 with m >= 1 forces t >= 2m (P041)")
check(all(17 + Fr(h, 4) - Fr(N, 8) >= Fr(145, 8) for h in range(5, 18) for N in range(0, 2)), "17 + h/4 - N/8 < 145/8 with h >= 5 forces N >= 2 (P041)")
check(all(17 + Fr(h, 4) - Fr(2, 8) >= Fr(145, 8) for h in range(6, 18)) and 17 + Fr(5, 4) - Fr(2, 8) < Fr(145, 8), "with N = 2 the same inequality forces h = 5 exactly (P041)")

# ---- KEY_W
KW = load_cls("KEY_W")
check(KW["bound"] == 20 and KW["classes"]["M"] [0] == 4 and KW["classes"]["M"][1][0][1] == (Fr(0), RHO), "KEY_W: bound 20, half-marker at threshold 4")
lowname = [k for k in KW["classes"] if k != "M"][0]
thr, kslots = KW["classes"][lowname]
check(thr == 0 and len(kslots) == 3, "KEY_W low union: threshold 0, three slots")
s1, s2, s3 = kslots
check(same_poly(s1[0], L9) and s1[1] == (Fr(30651, 100000), Fr(44941, 100000)), "KEY_W slot 1 = L9 x [30651/100000, 44941/100000] (P049)")
check(all(bbox(s[0])[1] <= Fr(53, 100) for s in (s2, s3)), "KEY_W slots 2, 3 are wall slots (x <= 53/100): off-wall only slot 1 can hold the L9 parent")
lo, hi = s1[1]
check(lift(lo, 1) > 1 and lift(hi, -1) < 0, "only the identity lift of slot 1's gate meets the canonical theta9 in [0, pi/2): +pi/2 lift starts above tan-half 1, -pi/2 lift ends below 0")
check(Fr(61301, 200000) < lo and lo - Fr(61301, 200000) == Fr(1, 200000), "lower exit end 61301/200000 is below the KEY_W gate by exactly 1/200000 (P053)")
check(hi < 1, "high atom t9 > 44941/100000 excluded; 44941/100000 < 1")
# the gate from the T9 trigger slot
PS = load_cls("CLASS_PS_L01_T09")
T9 = [k for k in PS["classes"] if k.startswith("T9")][0]
tP, tg = PS["classes"][T9][1][0]
check(tP == rect(Fr(53, 100), Fr(4501, 5000), Fr(24137, 10000), Fr(29637, 10000)) and tg == (Fr(-408817, 1000000), Fr(61301, 200000)), "T9 trigger slot: off-wall L9 part x [-408817/1000000, 61301/200000]")
check(lift(tg[0], 1) == Fr(591183, 1408817), "+pi/2 lift of -408817/1000000 is exactly 591183/1408817: the open gate is (61301/200000, 591183/1408817) (P052)")
check(Fr(591183, 1408817) < Fr(44941, 100000), "gate upper end 591183/1408817 < 44941/100000: JPA interval nonempty")
# C escape arcs
C1 = load_cls("C_1")
Xn = [k for k in C1["classes"] if k.startswith("X_")][0]
xslots = C1["classes"][Xn][1]
check(len(xslots) == 9, "C_1 escape union X has 9 slots")
a1 = [s for s in xslots if same_poly(s[0], L9)]
check(sorted(s[1] for s in a1) == sorted([(Fr(0), Fr(613, 2000)), (Fr(-5803, 14197), Fr(0))]), "X: the two angular exits on the whole L9: [0,613/2000] and [-5803/14197,0]")
check(Fr(61301, 200000) - Fr(613, 2000) == Fr(1, 200000), "lower exit gap: 61301/200000 - 613/2000 = 1/200000 (P057)")
check(lift(Fr(-5803, 14197), 1) == Fr(4197, 10000) and Fr(4197, 10000) - Fr(591183, 1408817) > 0, "upper quarter-turn gap: lift(-5803/14197) = 4197/10000; minus 591183/1408817 = %s > 0 (P057 prints 974949/14197000000; equal? %s)" % (Fr(4197, 10000) - Fr(591183, 1408817), Fr(4197, 10000) - Fr(591183, 1408817) == Fr(974949, 14197000000)))
AQ_X = [s for s in xslots if s[0] == rect(Fr(-131, 250), Fr(53, 100), Fr(24137, 10000), Fr(13, 5))]
check(len(AQ_X) == 1 and AQ_X[0][1] == (Fr(613, 2000), Fr(4197, 10000)), "X: the recut AQ wall-pose slot [613/2000, 4197/10000] (P055/PROOF_BRIDGE_V2 note)")
coarse3 = rect(Fr(129, 100), Fr(2993, 1500), Fr(-1, 2), Fr(1411, 1000))
coarse15 = rect(Fr(19953, 10000), Fr(26807, 10000), Fr(1623, 500), Fr(26, 5))
coarse17 = rect(Fr(3775331, 1000000), Fr(5199531, 1000000), Fr(24137, 10000), Fr(29637, 10000))
arms = [s for s in xslots if s[0] in (coarse3, coarse15, coarse17)]
check(len(arms) == 6 and all(s[1] in ((Fr(1, 20), RHO), (-RHO, Fr(-1, 20))) for s in arms), "X: six signed ungated arms [1/20,rho], [-rho,-1/20] on the whole coarse regions 3, 15, 17")
# all C files share the same X union and the 10 C files have M threshold 4, target threshold 0, bound 20
for nm in ("C_1", "C_2", "C_5", "C_6", "C_10", "C_11", "C_12", "C_13", "C_14", "C_16"):
    Cf = load_cls(nm)
    xs = [k for k in Cf["classes"] if k.startswith("X_")][0]
    check(Cf["classes"][xs][1] == xslots and Cf["bound"] == 20 and Cf["classes"]["M"][0] == 4
          and all(Cf["classes"][k][0] == 0 for k in Cf["classes"] if k != "M"), "%s: same X union, bound 20, M threshold 4, other classes threshold 0" % nm)

# ---- L files, AQ, S_k
Lfiles = {k: load_cls("L_%d" % k) for k in (3, 4, 15, 17)}
AQ = rect(Fr(-131, 250), Fr(53, 100), Fr(24137, 10000), Fr(13, 5))
S = {}
for k, Lf in Lfiles.items():
    aq = [n for n in Lf["classes"] if n.startswith("AQ")][0]
    sk = [n for n in Lf["classes"] if n.startswith("S_")][0]
    check(Lf["classes"][aq][1][0] == (AQ, (-RHO, RHO)) and Lf["classes"][aq][0] == 0, "L_%d: AQ = [-131/250,53/100]x[24137/10000,13/5], all directions, threshold 0" % k)
    check(Lf["bound"] == 20 and Lf["classes"]["M"][0] == 4 and Lf["classes"]["M"][1][0][1] == (Fr(0), RHO), "L_%d: bound 20, half-marker threshold 4" % k)
    P, g = Lf["classes"][sk][1][0]
    check(g == (-RHO, RHO) and Lf["classes"][sk][0] == 0, "L_%d: S_%d all directions, threshold 0" % (k, k))
    S[k] = P
check(contains(L9, AQ) and bbox(AQ)[1] == Fr(53, 100), "AQ is contained in L9 and has x <= 53/100 (empty off-wall, P054)")
WC = PS["classes"]["WC_label9_wall_column_exempt"][1][0][0]
check(WC == rect(Fr(-131, 250), Fr(53, 100), Fr(24137, 10000), Fr(29637, 10000)) and contains(L9, WC), "WC = wall column part of L9 (x <= 53/100): empty off-wall")
claimed = {3: Fr(1097067164761, 4 * 10**12), 15: Fr(799624844761, 4 * 10**12), 17: Fr(1059571044761, 4 * 10**12)}
Sclip = {}
for k in (3, 15, 17):
    Q = clip_box(S[k], PHYS[0], PHYS[1], PHYS[0], PHYS[1])
    Sclip[k] = Q
    check(diam2(Q) == claimed[k] and diam2(Q) < 1, "S_%d clipped diameter^2 = %s (claimed %s) < 1 (P054)" % (k, diam2(Q), claimed[k]))
Sclip[4] = clip_box(S[4], PHYS[0], PHYS[1], PHYS[0], PHYS[1])
check(diam2(Sclip[4]) < 1, "S_4 clipped diameter^2 = %s < 1" % diam2(Sclip[4]))
for a in (3, 15, 17):
    for b in (3, 15, 17):
        if a < b:
            check(strictly_separated(S[a], S[b]), "S_%d and S_%d disjoint" % (a, b))
    check(strictly_separated(S[a], M_hex) and strictly_separated(S[a], L9), "S_%d disjoint from the marker and from L9" % a)
check(contains(L17, S[17]), "S17 lies in the frame region L17 (P054)")
coarse = {3: coarse3, 15: coarse15, 17: coarse17}
for k in (3, 15, 17):
    check(contains(clip_box(coarse[k], PHYS[0], PHYS[1], PHYS[0], PHYS[1]), Sclip[k]), "clipped S_%d lies in clipped coarse region %d (P055)" % (k, k))
c17 = clip_box(coarse17, PHYS[0], PHYS[1], PHYS[0], PHYS[1])
check(diam2(c17) == Fr(1851391155161, 4 * 10**12) and diam2(c17) < 1, "clipped coarse 17 diameter^2 = %s (claimed 1851391155161/4e12) < 1" % diam2(c17))
check(contains(c17, clip_box(L17, PHYS[0], PHYS[1], PHYS[0], PHYS[1])), "clipped frame L17 lies in clipped coarse 17 (P055)")
check(bbox(L17)[0] - bbox(coarse17)[0] == Fr(469, 1000000), "coarse 17 differs from frame L17 by -469/1000000 in x (P055)")

# ---- coarse capacity quartic (P065-P066): own derivation and own positivity proof
def quartic(w, H):
    return [1 - w, 1 - 2 * H, Fr(4), -1 - 2 * H, 1 + w]


def bernstein_coeffs(power, a, b):
    """Bernstein coefficients of a degree-4 polynomial (power basis) on [a, b]."""
    from math import comb
    n = 4
    # substitute u = a + (b-a) s: coefficients in s
    h = b - a
    cs = [Fr(0)] * (n + 1)
    for k, pk in enumerate(power):
        # (a + h s)^k = sum_j C(k,j) a^(k-j) h^j s^j
        for j in range(k + 1):
            cs[j] += pk * comb(k, j) * a ** (k - j) * h ** j
    # power basis in s -> Bernstein basis on [0,1]: b_i = sum_{j<=i} C(i,j)/C(n,j) c_j
    return [sum(comb(i, j) * cs[j] / comb(n, j) for j in range(i + 1)) for i in range(n + 1)]


for k, (w, H, claimed_min) in {3: (Fr(529, 750), Fr(2821531, 2000000), Fr(634043429, 125829120000)),
                               15: (Fr(3427, 5000), Fr(2859531, 2000000), Fr(43535731167, 8388608000000))}.items():
    reg = coarse[k]
    xa, xb, ya, yb = bbox(reg)
    if k == 3:
        check(xb - xa == w and yb - DELTA == H, "region 3: w = width = %s, H = top - delta = %s (P066)" % (xb - xa, yb - DELTA))
    else:
        check(xb - xa == w and (U - DELTA) - ya == H, "region 15: w = width = %s, H = (U - delta) - bottom = %s (P066)" % (xb - xa, (U - DELTA) - ya))
    P = quartic(w, H)
    # own symbolic check of the quartic identity: (1+u^2)^2 [1 - a w - b H + b (a+b)/2] with a=(1-u^2)/(1+u^2), b=2u/(1+u^2)
    import random
    okid = True
    for _ in range(20):
        u = Fr(random.randint(0, 1000), 1000)
        a = (1 - u * u) / (1 + u * u); b = 2 * u / (1 + u * u)
        lhs = (1 + u * u) ** 2 * (1 - a * w - b * H + b * (a + b) / 2)
        rhs = sum(P[i] * u ** i for i in range(5))
        okid &= (lhs == rhs)
    check(okid, "region %d: quartic identity (1+u^2)^2 [1 - aw - bH + b(a+b)/2] = P(u) holds (random exact tests)" % k)
    mins = []
    N = 128
    allpos = True
    for i in range(N):
        bc = bernstein_coeffs(P, Fr(i, N), Fr(i + 1, N))
        allpos &= all(c > 0 for c in bc)
        mins.append(min(bc))
    check(allpos, "region %d: all Bernstein coefficients on 128 subintervals positive; minimum %s (claimed %s)" % (k, min(mins), claimed_min))
    check(min(mins) == claimed_min, "region %d: minimum Bernstein coefficient equals the claimed value" % k)
    # Sturm-free sanity: evaluate on a fine grid too
    check(all(sum(P[i] * Fr(j, 4096) ** i for i in range(5)) > 0 for j in range(4097)), "region %d: P > 0 on a grid of 4097 points of [0,1]" % k)

# ---- wall lemma (run_adm.py lines 17-18, KNOWN_ISSUES item 1): own derivation
tw = Fr(31, 1000)
check((1 + 2 * tw - tw * tw) * 50 > 53 * (1 + tw * tw), "cos|theta|+sin|theta| at |theta| = 2 atan(31/1000) exceeds 53/50: a square in x >= 0 with centre x < 53/100 has |theta| < 2 atan(31/1000)")
# monotonicity: cos t + sin t increases on [0, pi/4]; so support (cos+sin)/2 <= x < 53/100 bounds |theta| from above
# ---- support cut for gated label 9 (P079)
pk = json.load(open(os.path.join(SRC, "upper-packing-certificate.json")))
p9x = Fr(pk["squares"][8]["x"])
vals = []
for t in (Fr(61301, 200000), Fr(591183, 1408817)):
    g, s = rot(t)
    vals.append((g + s) / 2 - p9x)
check(min(vals) > Fr(-9897, 10**6), "gated label 9: min over the gate ends of (cos+sin)/2 - p9x = %s > -9897/10^6 (P079)" % float(min(vals)))
# concavity of cos+sin on [0, pi/2] -> minimum at an endpoint of the arc: (cos+sin)'' = -(cos+sin) < 0 there

# ---- E07A and C7/C8 transfer (P047)
E = load_cls("E07A")
check(E["bound"] == 20 and E["classes"]["M"][0] == 4 and E["classes"]["M"][1][0] == (M_hex, (-RHO, RHO)), "E07A: all-direction marker hexagon at threshold 4, bound 20")
t7n = [k for k in E["classes"] if k != "M"][0]
T7, g7 = E["classes"][t7n][1][0]
design = os.path.join(SRC, "local-research/claude-20261002/rerun-clean-20261011/design_classes/classes")
C7 = load_cls(None, os.path.join(design, "C_L07.json")); C8 = load_cls(None, os.path.join(design, "C_L08.json"))
T7c, g7c = C7["classes"]["T_label7_exempt"][1][0]; T8c, g8c = C8["classes"]["T_label8_exempt"][1][0]
check(T7 == T7c and g7 == g7c == (Fr(-751411, 10**7), Fr(751411, 10**7)), "literal C7 target equals the E07A target, gate +-751411/10^7")
T7r = mirror_x(T7)
check(contains(T8c, T7r) and g8c == g7c, "reflected C7 target lies inside the literal C8 target with the same symmetric gate")
check(bbox(T8c)[1] - bbox(T7r)[1] == Fr(3, 125), "C8 upper x end exceeds the reflected target by 3/125")
check(bbox(T8c)[0] - bbox(T7c)[1] == Fr(8189, 2500) and Fr(8189, 2500) > 1, "C7 and C8 x-projections separated by 8189/2500 > 1: distinct parents")
check(E["classes"]["M"][1][0][0] == M_hex, "E07A marker is the hexagon (reflection-invariant)")

# ---- C12 unions (P045, P078)
C12 = load_cls("C_12")
T12 = C12["classes"]["T_label12_exempt"][1][0][0]
d = diam2(ccw(M_hex + T12)) if False else max(diam2([p, q]) for p in M_hex + T12 for q in M_hex + T12)
check(d < Fr(3953, 10000), "JG: diameter^2 of marker hexagon u C12 target = %s < 3953/10000 (P078)" % float(d))
others = {}
others["PS PB12"] = load_cls("CLASS_PS_L12_T09")["classes"]["PB_label12_exempt"][1][0][0]
others["Q12 QB12"] = load_cls("Q_12")["classes"]["QB_label12_exempt"][1][0][0]
others["PW12 HULL12"] = load_cls("PW_12")["classes"]["HULL_label12_exempt"][1][0][0]
for nm, T in others.items():
    dd = max(diam2([p, q]) for p in M_hex + T for q in M_hex + T)
    check(dd <= Fr(9437, 31250), "%s: diameter^2 of marker u target12 = %s <= 9437/31250 (P045)" % (nm, float(dd)))

# ---- wall triggers (P050)
rigidQ = [1, 2, 5, 6, 7, 8, 10, 11, 12, 13, 14, 16]
for j in rigidQ:
    Qf = load_cls("Q_%d" % j)
    n = [k for k in Qf["classes"] if k.startswith("AQ")][0]
    P, g = Qf["classes"][n][1][0]
    check(P == rect(Fr(-131, 250), Fr(53, 100), Fr(24137, 10000), Fr(129, 50)) and g == (-RHO, RHO) and Qf["classes"][n][0] == 4 and Qf["bound"] == 23, "Q_%d trigger = wall column below the cut, all directions, threshold 4, bound 23" % j)
for j in (3, 4, 15, 17):
    Qf = load_cls("Q_%d" % j)
    n = [k for k in Qf["classes"] if k.startswith("AQ")][0]
    P, g = Qf["classes"][n][1][0]
    check(P == AQ and g == (-RHO, RHO) and Qf["classes"][n][0] == 4, "Q_%d trigger = AQ (y up to 13/5), all directions, threshold 4" % j)
for j in rigidQ:
    Pf = load_cls("PW_%d" % j)
    n = [k for k in Pf["classes"] if k.startswith("W_")][0]
    P, g = Pf["classes"][n][1][0]
    check(P == rect(Fr(-131, 250), Fr(53, 100), Fr(129, 50), Fr(29637, 10000)) and g == (-RHO, RHO) and Pf["classes"][n][0] == 4 and Pf["bound"] == 23, "PW_%d trigger = wall column above the cut, all directions, threshold 4, bound 23" % j)
SL = load_cls("SL11_T020")
n = [k for k in SL["classes"] if k.startswith("SLAB")][0]
check(SL["classes"][n][1][0] == (rect(Fr(-131, 250), Fr(53, 100), Fr(129, 50), Fr(13, 5)), (-RHO, RHO)) and SL["classes"][n][0] == 4 and SL["bound"] == 23, "SL11_T020 trigger = slab [129/50, 13/5] of the wall column, threshold 4, bound 23")

# ---- PS/PSS files: structure for the 4/4/0 and bound-23 arguments (P033, P062-P069)
import glob
for p in sorted(glob.glob(os.path.join(CAP, "CLASS_*"))):
    nm = os.path.basename(p)
    Cf = load_cls(nm)
    high = [k for k, v in Cf["classes"].items() if v[0] > 1]
    low = [k for k, v in Cf["classes"].items() if v[0] < 1]
    other = [k for k, v in Cf["classes"].items() if v[0] == 1]
    ok = (Cf["bound"] == 23 and len(high) == 2 and "M" in high and all(Cf["classes"][k][0] == 4 for k in high)
          and len(low) == 2 and all(Cf["classes"][k][0] == 0 for k in low) and any(k.startswith("WC") for k in low) and not other
          and Cf["classes"]["M"][1][0][1] == (Fr(0), RHO))
    wc = [k for k in low if k.startswith("WC")][0]
    ok &= Cf["classes"][wc][1][0] == (WC, (-RHO, RHO))
    check(ok, "%s: bound 23; high = M (half marker) and one trigger at 4; low = target and WC at 0" % nm)
# signed label-6 files
for nm, arm in (("CLASS_PS_L06_T17_ENDm_H4T4", (-RHO, Fr(-1, 20))), ("CLASS_PS_L06_T17_ENDp_H4T4", (Fr(1, 20), RHO))):
    Cf = load_cls(nm)
    tn = [k for k in Cf["classes"] if k.startswith("T17")][0]
    check(Cf["classes"][tn][1] == [(coarse17, arm)], "%s: trigger arm %s on the whole coarse 17 (P069)" % (nm, arm))

# ---- case partition (P051-P058): own enumeration on the product atoms
cuts = {"x9": [Fr(53, 100)], "y9": [Fr(129, 50), Fr(13, 5)], "t9": [Fr(0), Fr(61301, 200000), Fr(591183, 1408817), Fr(44941, 100000), Fr(1)],
        "tau3": [Fr(-1, 20), Fr(1, 20)], "tau17": [Fr(-1, 20), Fr(1, 20)], "tau15": [Fr(-1, 20), Fr(1, 20)]}


def atoms(vals):
    pts = sorted(vals)
    out = [pts[0] - 1]
    for i, x in enumerate(pts):
        out.append(x)
        if i + 1 < len(pts):
            out.append((x + pts[i + 1]) / 2)
    out.append(pts[-1] + 1)
    return out


def case(x9, y9, t9, tau3, tau17, tau15):
    if x9 <= Fr(53, 100):
        return "JQ" if y9 <= Fr(129, 50) else ("JPWS" if y9 <= Fr(13, 5) else "JPW13")
    if not (0 <= t9 < 1):
        return "outside t9 domain"
    if t9 <= Fr(61301, 200000):
        return "JPB(excluded by KEY_W)"
    if t9 >= Fr(591183, 1408817):
        return "JPA" if t9 <= Fr(44941, 100000) else "high9(excluded by KEY_W)"
    for k, tau in (("3", tau3), ("17", tau17), ("15", tau15)):
        if tau <= Fr(-1, 20):
            return "JPG%sm" % k
        if tau >= Fr(1, 20):
            return "JPG%sp" % k
    return "JG"


# exhaustiveness and disjointness: 'case' is a function (total on the domain), so each point has exactly one case;
# what the proof needs is that the eleven predicates of EXACT_ENDPOINT_AND_CASES.json are these cases. Compare literally.
ec = json.load(open(os.path.join(SRC, "research/finishing-threshold-goal-20261007/current-author-20261012t/second-order-20261010/theorem/EXACT_ENDPOINT_AND_CASES.json")))
preds = {b["root"]: b["predicate"] for b in ec["branches"] + ec["excluded_branches"]}
import itertools
names = ["x9", "y9", "t9", "tau3", "tau17", "tau15"]

# Changed at retention, 14 October 2026: the lane evaluated each predicate with eval() on
# the text of EXACT_ENDPOINT_AND_CASES.json, which executes text from the source. The
# record never executes upstream text, so holds() parses the one form those predicates
# take -- clauses joined by " and ", each a chain of names and rationals compared by <,
# <=, > or >= -- and refuses anything else. Its replay on the declared pin is kept in
# ../logs/literal_checks.log; equivalence to the lane's unretained eval line is not established.
_OPS = {"<": lambda a, b: a < b, "<=": lambda a, b: a <= b, ">": lambda a, b: a > b, ">=": lambda a, b: a >= b}


def _operand(token, env):
    if token in names:
        return env[token]
    if not re.fullmatch(r"-?\d+(?:/\d+)?", token):
        raise ValueError("not a name or a rational: %r" % token)
    return Fr(token)


def holds(pred, env):
    for clause in pred.split(" and "):
        tokens = clause.split()
        if len(tokens) < 3 or len(tokens) % 2 == 0 or any(t not in _OPS for t in tokens[1::2]):
            raise ValueError("not a chain of comparisons: %r" % clause)
        values = [_operand(t, env) for t in tokens[0::2]]
        if not all(_OPS[op](a, b) for a, b, op in zip(values, values[1:], tokens[1::2])):
            return False
    return True

grid = [atoms(cuts[n]) for n in names]
count = 0; mism = 0
for pt in itertools.product(*grid):
    env = dict(zip(names, pt))
    if not (0 <= env["t9"] < 1):
        continue
    if not all(-Fr(1, 2) <= env[k] <= Fr(1, 2) for k in ("tau3", "tau17", "tau15")):
        pass
    mine = case(*pt)
    hits = [r for r, pred in preds.items() if holds(pred, env)]
    count += 1
    want = {"JPB(excluded by KEY_W)": "JPB", "high9(excluded by KEY_W)": "REMOVED_HIGH9"}.get(mine, mine)
    if hits != [want]:
        mism += 1
check(mism == 0, "case partition: on all %d product atoms exactly one of the 13 literal predicates holds and it is the case of my own decision function" % count)

print()
print("FAILURES:", len(fails))
for f in fails:
    print("  -", f)
