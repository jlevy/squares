"""Own re-derivation of the root admissions (premise ROOT_ADMISSION, PROOF.md P043-P046, P059-P060, P073-P080)
and of the distinct-parent profiles (P044-P046): for each of the eleven branches, the seventeen target regions,
converted with my own chart formula xi = e.(c - (U-L)(1,1)/2 - p_i) over my own enclosure of L, must lie in the
root box of the literal root file, and their direction sets must lie in the root arcs; the seventeen clipped
target centre regions must have diameter < 1 and be pairwise disjoint.

Usage: python3 -I admission_check.py SRC_ROOT
"""
import json
import os
import sys
from fractions import Fraction as Fr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geom_util import (U, C_CAP, RHO, poly, rect, ccw, clip_box, diam2, bbox, strictly_separated, contains, rot,
                       cmul, cconj, vcross, vdot, J, lift)
from root_box import enclosure

SRC = sys.argv[1]
CAP = os.path.join(SRC, "research/finishing-threshold-goal-20261007/clean-rerun-20261011/current-build-0122/capture/statements")
JOIN = os.path.join(SRC, "research/window-extension-20261008/bigbox/join")
R = Fr(4675530093604551, 10**15)
(tl, th), _, (Llo, Lhi) = enclosure()
assert Llo < Lhi < R < C_CAP < U
print("own L enclosure: [%s, %s] (width %.3e); R - Lhi = %.4e" % (float(Llo), float(Lhi), float(Lhi - Llo), float(R - Lhi)))
DELTA = (U - C_CAP) / 2
PHYS = (DELTA + Fr(1, 2), U - DELTA - Fr(1, 2))

# ---- reference chart (my own reading of SPEC 3.0 section 1)
pk = json.load(open(os.path.join(SRC, "upper-packing-certificate.json")))
assert Fr(pk["side"]) == R
p = {}; u = {}; v = {}
for k, s in enumerate(pk["squares"]):
    i = k + 1
    p[i] = (Fr(s["x"]), Fr(s["y"]))
    u[i] = rot(Fr(s["t"]))
    v[i] = (-u[i][1], u[i][0])
T0 = u[9][0] * (u[9][0] + 4 - R)
p[13] = (p[13][0] - T0 / 3 * v[13][0], p[13][1] - T0 / 3 * v[13][1])
axes = {i: ((u[i], v[i]) if i in (11, 13) else ((Fr(1), Fr(0)), (Fr(0), Fr(1)))) for i in p}


def chart_interval(i, P, clip=True):
    """interval of xi_(i,1), xi_(i,2) over the polygon P (frame coordinates) and L in [Llo, Lhi]"""
    out = []
    for k in (0, 1):
        vals = []
        for c in P:
            for L in (Llo, Lhi):
                q = (c[0] - (U - L) / 2 - p[i][0], c[1] - (U - L) / 2 - p[i][1])
                vals.append(vdot(axes[i][k], q))
        lo, hi = min(vals), max(vals)
        if clip and i not in (11, 13):
            lo = max(lo, Fr(1, 2) - p[i][k])          # every unit square in [0,L]^2 has centre >= 1/2
            hi = min(hi, Lhi - Fr(1, 2) - p[i][k])    # and centre <= L - 1/2
        out.append((lo, hi))
    return out


def load_cls(name, path=None):
    pth = path or os.path.join(CAP, name, "classes.json")
    d = json.load(open(pth))
    assert d["symmetry"] == "fixed" and [Fr(x) for x in d["frame"]["center"]] == [U / 2, U / 2]
    out = {}
    for c in d["classes"]:
        out[c["name"]] = (Fr(c["threshold"]), [(ccw(poly(s["centre"]["polygon"])), (Fr(s["angle_tan_half"][0]), Fr(s["angle_tan_half"][1]))) for s in c["slots"]])
    return out


def target_of(cls, label):
    """the unique threshold-0 class of a label (prefixes as the proof text names them)"""
    cands = [n for n, (thr, slots) in cls.items() if thr == 0 and any(n.startswith(pre + "label%d_" % label) for pre in ("PB_", "HULLW_", "QB_", "HULL_", "B_", "T_", "S_"))]
    assert len(cands) == 1, (label, list(cls))
    thr, slots = cls[cands[0]]
    assert len(slots) == 1
    return cands[0], slots[0]


def load_root(name):
    files = {"JQ": "JQ_exact_v1.json", "JPWS": "JPWS_exact_v4.json", "JPW13": "JPW13_exact_v2x.json", "JG": "JG_exact_v2.json",
             "JPA": "JPA_exact_v5.json", "JPG3m": "JPG3m_exact_v5.json", "JPG3p": "JPG3p_exact_v5.json", "JPG17m": "JPG17m_exact_v5.json",
             "JPG17p": "JPG17p_exact_v5.json", "JPG15m": "JPG15m_exact_v5.json", "JPG15p": "JPG15p_exact_v5.json"}
    d = json.load(open(os.path.join(JOIN, files[name])))
    assert Fr(d["Sref"]) == R and Fr(d["S_floor"]) == R and [Fr(x) for x in d["S"]] == [R, R] and d["labels"] == 17
    box = {int(i): [(Fr(a), Fr(b)) for a, b in bb] for i, bb in d["window"]["box"].items()}
    arc = {}
    for i, a in d["root_arc"].items():
        c = tuple(Fr(x) for x in a["c"]); lo = tuple(Fr(x) for x in a["lo"]); hi = tuple(Fr(x) for x in a["hi"])
        for g in (c, lo, hi):
            assert g[0] ** 2 + g[1] ** 2 == 1
        assert lo[0] > 0 and hi[0] > 0 and lo[1] <= hi[1]
        A = cmul(u[int(i)], cmul(c, lo)); B = cmul(u[int(i)], cmul(c, hi))   # direction a_i = R(psi) rho_i u_i
        arc[int(i)] = (A, B)
    return d, box, arc, files[name]


def in_arc(D, arc):
    """D (unit or not) lies on the counter-clockwise arc from A to B (arc shorter than pi)"""
    A, B = arc
    assert vcross(A, B) >= 0 or vdot(A, B) < 0  # arc of length <= pi
    return vcross(A, D) >= 0 and vcross(D, B) >= 0


def arc_margins(D, arc):
    A, B = arc
    return vcross(A, D), vcross(D, B)


def some_lift_in_arc(lo, hi, arc):
    """the closed tan-half interval [lo, hi] of ONE side direction: some quarter-turn lift of it lies in the arc"""
    found = []
    for k in range(4):
        D1, D2 = rot(lo), rot(hi)
        for _ in range(k):
            D1, D2 = cmul(D1, J), cmul(D2, J)
        if in_arc(D1, arc) and in_arc(D2, arc):
            found.append((k, min(arc_margins(D1, arc)[0], arc_margins(D2, arc)[1])))
    return found


RIGID = [1, 2, 5, 6, 7, 8, 10, 11, 12, 13, 14, 16]
LOOSE = [3, 4, 15, 17]
X0, X1, XW = Fr(-131, 250), Fr(4501, 5000), Fr(53, 100)
Y0, YC, Y13, Y1 = Fr(24137, 10000), Fr(129, 50), Fr(13, 5), Fr(29637, 10000)
G9LO, G9HI, KWHI = Fr(61301, 200000), Fr(591183, 1408817), Fr(44941, 100000)
GT = Fr(1, 20)
TW = Fr(31, 1000)
sel = json.load(open(os.path.join(SRC, "research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/runtime/SELECTED_ORIGINAL_MAP.json")))
SEL = {(r["root"], r["label"]): r for r in sel["rows"]}
M_hex = load_cls("L_3")["M"][1][0][0]


def spec(root):
    """label -> (polygon in the frame, direction spec, source)"""
    s = {}
    if root == "JQ":
        for j in RIGID + LOOSE:
            nm, (P, g) = target_of(load_cls("Q_%d" % j), j); s[j] = (P, ("slot", g), "Q_%d:%s" % (j, nm))
        s[9] = (rect(X0, XW, Y0, YC), ("wall",), "wall column y<=129/50")
    elif root == "JPWS":
        for j in RIGID:
            if j == 11:
                nm, (P, g) = target_of(load_cls("SL11_T020"), 11); s[11] = (P, ("slot", g), "SL11_T020:" + nm)
            else:
                nm, (P, g) = target_of(load_cls("PW_%d" % j), j); s[j] = (P, ("slot", g), "PW_%d:%s" % (j, nm))
        for j in LOOSE:
            nm, (P, g) = target_of(load_cls("Q_%d" % j), j); s[j] = (P, ("slot", g), "Q_%d:%s" % (j, nm))
        s[9] = (rect(X0, XW, YC, Y13), ("wall",), "wall column 129/50<=y<=13/5")
    elif root == "JPW13":
        for j in RIGID:
            nm, (P, g) = target_of(load_cls("PW_%d" % j), j); s[j] = (P, ("slot", g), "PW_%d:%s" % (j, nm))
        for j in LOOSE:
            nm, (P, g) = target_of(load_cls("L_%d" % j), j); s[j] = (P, ("slot", g), "L_%d:%s" % (j, nm))
        s[9] = (rect(X0, XW, Y13, Y1), ("wall",), "wall column y>=13/5")
    elif root == "JG":
        design = os.path.join(SRC, "local-research/claude-20261002/rerun-clean-20261011/design_classes/classes")
        for j in RIGID:
            if j in (7, 8):      # C7 and C8 are the unrun literal files (occupancy from E07A, P047)
                nm, (P, g) = target_of(load_cls(None, os.path.join(design, "C_L%02d.json" % j)), j); s[j] = (P, ("slot", g), "C_L%02d:%s" % (j, nm))
            else:
                nm, (P, g) = target_of(load_cls("C_%d" % j), j); s[j] = (P, ("slot", g), "C_%d:%s" % (j, nm))
        for j in (3, 15, 17):
            nm, (P, g) = target_of(load_cls("L_%d" % j), j); assert g == (-RHO, RHO); s[j] = (P, ("gate",), "L_%d:%s gated" % (j, nm))
        nm, (P, g) = target_of(load_cls("L_4"), 4); s[4] = (P, ("slot", g), "L_4:" + nm)
        s[9] = (rect(XW, X1, Y0, Y1), ("gate9",), "off-wall L9, gated")
    else:
        for j in RIGID:
            r = SEL[(root, j)]
            path = os.path.join(SRC, r["literal"]["file"])
            nm, (P, g) = target_of(load_cls(None, path), j); s[j] = (P, ("slot", g), os.path.basename(os.path.dirname(path)) + ":" + nm)
        d3 = d17 = d15 = ("free",)
        if root == "JPA":
            d9 = ("exit9",)
        else:
            d9 = ("gate9",)
            kind = {"m": ("below",), "p": ("above",)}[root[-1]]
            if root.startswith("JPG3"):
                d3 = kind
            elif root.startswith("JPG17"):
                d3 = ("gate",); d17 = kind
            else:
                d3 = ("gate",); d17 = ("gate",); d15 = kind
        for j, dk in ((3, d3), (17, d17), (15, d15)):
            nm, (P, g) = target_of(load_cls("L_%d" % j), j); assert g == (-RHO, RHO); s[j] = (P, dk, "L_%d:%s %s" % (j, nm, dk[0]))
        nm, (P, g) = target_of(load_cls("L_4"), 4); s[4] = (P, ("slot", g), "L_4:" + nm)
        s[9] = (rect(XW, X1, Y0, Y1), d9, "off-wall L9 " + d9[0])
    return s


def check_root(root):
    d, box, arc, fname = load_root(root)
    s = spec(root)
    worst = None; fails = []
    regions = {}
    for i in range(1, 18):
        P, dk, src = s[i]
        tr = chart_interval(i, P)
        if i == 9 and dk[0] == "gate9":
            # support bound: a square in x >= 0 whose side direction (g, s) is in the first quadrant has centre x >= (g+s)/2;
            # (g+s)/2 is concave in the angle, so its minimum over the gate arc is at an end
            smin = min(sum(rot(G9LO)) / 2, sum(rot(G9HI)) / 2)
            assert all(x > 0 for x in rot(G9LO)) and all(x > 0 for x in rot(G9HI))
            tr[0] = (max(tr[0][0], smin - p[9][0]), tr[0][1])
        margins = {}
        for k in (0, 1):
            assert tr[k][0] <= tr[k][1]
            margins["xi%d.lo" % (k + 1)] = tr[k][0] - box[i][k][0]
            margins["xi%d.hi" % (k + 1)] = box[i][k][1] - tr[k][1]
        A, B = arc[i]
        if dk[0] == "slot":
            lo, hi = dk[1]
            if (lo, hi) == (-RHO, RHO):
                dk = ("free",)
            else:
                if i == 12:
                    assert lo > -RHO and hi < 1
                    hi = min(hi, RHO)       # the label-12 parent is the marker occupant, whose representative is in [0, rho]
                found = some_lift_in_arc(lo, hi, (A, B))
                if not found:
                    margins["arc"] = Fr(-1)
                else:
                    margins["arc"] = max(m for _, m in found)
        if dk[0] == "free":
            margins["arc.free"] = -vdot(A, B)        # >= 0 iff the arc spans at least a quarter turn
        elif dk[0] == "gate":
            D1, D2 = rot(-GT), rot(GT)
            margins["arc"] = min(arc_margins(D1, (A, B))[0], arc_margins(D2, (A, B))[1]) if (in_arc(D1, (A, B)) and in_arc(D2, (A, B))) else Fr(-1)
        elif dk[0] == "below":
            D1, D2 = (Fr(1), Fr(-1)), rot(-GT)
            margins["arc"] = min(arc_margins(D1, (A, B))[0], arc_margins(D2, (A, B))[1]) if (in_arc(D1, (A, B)) and in_arc(D2, (A, B))) else Fr(-1)
        elif dk[0] == "above":
            D1, D2 = rot(GT), (Fr(1), Fr(1))
            margins["arc"] = min(arc_margins(D1, (A, B))[0], arc_margins(D2, (A, B))[1]) if (in_arc(D1, (A, B)) and in_arc(D2, (A, B))) else Fr(-1)
        elif dk[0] == "wall":
            D1, D2 = rot(-TW), rot(TW)
            margins["arc"] = min(arc_margins(D1, (A, B))[0], arc_margins(D2, (A, B))[1]) if (in_arc(D1, (A, B)) and in_arc(D2, (A, B))) else Fr(-1)
        elif dk[0] in ("gate9", "exit9"):
            lo, hi = (G9LO, G9HI) if dk[0] == "gate9" else (G9HI, KWHI)
            found = [f for f in some_lift_in_arc(lo, hi, (A, B)) if f[0] == 0]
            margins["arc"] = found[0][1] if found else Fr(-1)
        for k, val in margins.items():
            if val < 0:
                fails.append((i, k, float(val), src))
            if worst is None or val < worst[0]:
                worst = (val, i, k)
        regions[i] = clip_box(P, PHYS[0], PHYS[1], PHYS[0], PHYS[1])
    # distinct-parent profile: diameters and pairwise disjointness of the seventeen clipped centre regions
    prof_fail = []
    dmax = Fr(0)
    for i in range(1, 18):
        dd = diam2(regions[i])
        dmax = max(dmax, dd)
        if dd >= 1:
            prof_fail.append(("diameter", i, float(dd)))
    if root not in ("JQ", "JPWS", "JPW13") or True:
        dd = max(diam2([a, b]) for a in regions[12] + M_hex for b in regions[12] + M_hex)
        if dd >= 1:
            prof_fail.append(("diameter target12 u marker", 12, float(dd)))
    minsep = None
    for i in range(1, 18):
        for j in range(i + 1, 18):
            if not strictly_separated(regions[i], regions[j]):
                prof_fail.append(("overlap", i, j))
    print("== %s (%s): smallest admission margin %.6e at label %d (%s); %d admission failures; max clipped target diameter^2 %.4f; %d profile failures"
          % (root, fname, float(worst[0]), worst[1], worst[2], len(fails), float(dmax), len(prof_fail)))
    for f in fails:
        print("   ADMISSION FAIL", f)
    for f in prof_fail:
        print("   PROFILE FAIL", f)
    return not fails and not prof_fail


allok = True
for root in ["JQ", "JPWS", "JPW13", "JG", "JPA", "JPG3m", "JPG3p", "JPG17m", "JPG17p", "JPG15m", "JPG15p"]:
    allok &= check_root(root)
print("ALL ROOTS ADMITTED AND PROFILES DISTINCT:", allok)
