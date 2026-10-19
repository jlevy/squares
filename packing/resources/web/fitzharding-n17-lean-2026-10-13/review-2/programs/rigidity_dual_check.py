"""Independent recomputation of the 93-box local-rigidity dual certificate.

Reads, as text only:
  x/Sq17Lean/LocalRigidityMatrixData.lean   (bounds : Fin 430 -> Interval, codes : 4x52x45)
  x/Sq17Lean/LocalRigidityWeightData.lean   (93 AffineWeightCertificate 52 3, lo/hi boxes)
  Sq17Lean/LocalRigidityResidualMetadata.lean (mid, target per box)
  Sq17Lean/LocalRigidityResidualSupport.lean (support sets)
  Sq17Lean/LocalRigidityWeightCoverData.lean (owner, first, global bounds)
and re-implements, with exact Fractions:
  AffineWeightCertificate.check   (nonnegativity on the box, curvature mass)
  sparseResidualCheck             (interval L1 residual budget <= 1/4)
  the box cover of the slider box for every signed direction
  the final inequality q <= q/4 + 6e5 q^2 at radius 1e-7.
It also recomputes the budget with the *dense* (non-sparse) sum as a cross-check,
and reports the worst budget over the 93 boxes.
"""
import re
import sys
from fractions import Fraction as F
from pathlib import Path

src = Path(sys.argv[1])
xsrc = Path(sys.argv[2])


def frac(s):
    s = s.strip().strip("()")
    if "/" in s:
        a, b = s.split("/")
        return F(int(a.strip("() ")), int(b.strip("() ")))
    return F(int(s))


def fracs(s):
    return [frac(m) for m in re.findall(r"\(?-?\d+(?:/\d+)?\)?", s)]


# ---------- matrix data ----------
md = (xsrc / "Sq17Lean/LocalRigidityMatrixData.lean").read_text()
bline = re.search(r"^def bounds : Fin 430 → Interval := !\[(.*)\]$", md, re.M).group(1)
bounds = [(frac(a), frac(b)) for a, b in re.findall(r"⟨\(?(-?\d+(?:/\d+)?)\)?,\(?(-?\d+(?:/\d+)?)\)?⟩", bline)]
assert len(bounds) == 430, len(bounds)
cline = re.search(r"^def codes : Fin 4 → Fin 52 → Fin 45 → Fin 430 := (.*)$", md, re.M).group(1)
rows = re.findall(r"!\[([0-9,]+)\]", cline)
assert len(rows) == 4 * 52, len(rows)
codes = [[[int(x) for x in rows[k * 52 + i].split(",")] for i in range(52)] for k in range(4)]
assert all(len(r) == 45 for k in codes for r in k)
B = [[[bounds[codes[k][i][j]] for j in range(45)] for i in range(52)] for k in range(4)]
print("matrix bounds parsed: 4 x 52 x 45; distinct value codes used:", len({c for k in codes for r in k for c in r}))
# sanity: codes 0 means value v0 = 0
assert bounds[0] == (F(0), F(0))

# ---------- weight data ----------
wd = (xsrc / "Sq17Lean/LocalRigidityWeightData.lean").read_text()
boxes = {}
for m in re.finditer(r"def box(\d+) : AffineWeightCertificate 52 3 := \{(.*?)\n\}", wd, re.S):
    i = int(m.group(1))
    body = m.group(2)
    half = fracs(re.search(r"half := !\[([^\]]*)\]", body).group(1))
    base = fracs(re.search(r"base := !\[([^\]]*)\]", body).group(1))
    slope_block = re.search(r"slope := !\[(.*?)\]\]", body, re.S).group(1) + "]"
    slope = [fracs(r) for r in re.findall(r"!\[([^\]]*)\]", slope_block)]
    cm = re.search(r"curvature := fun i => if i\.val < (\d+) then (\d+) else (\d+)", body)
    if cm:
        n_, a_, b_ = (int(x) for x in cm.groups())
        curv = [F(a_) if r < n_ else F(b_) for r in range(52)]
    else:
        curv = fracs(re.search(r"curvature := !\[([^\]]*)\]", body).group(1))
    mass = frac(re.search(r"mass := (\(?-?\d+(?:/\d+)?\)?)", body).group(1))
    if not (len(half) == 3 and len(base) == 52 and len(slope) == 3 and all(len(s) == 52 for s in slope) and len(curv) == 52):
        raise SystemExit(f"parse shape box {i}: half {len(half)} base {len(base)} slope {[len(s) for s in slope]} curv {len(curv)}")
    boxes[i] = dict(half=half, base=base, slope=slope, curv=curv, mass=mass)
assert len(boxes) == 93, len(boxes)
lo = {int(m.group(1)): fracs(m.group(2)) for m in re.finditer(r"def lo(\d+) : Fin 3 → ℚ := !\[([^\]]*)\]", wd)}
hi = {int(m.group(1)): fracs(m.group(2)) for m in re.finditer(r"def hi(\d+) : Fin 3 → ℚ := !\[([^\]]*)\]", wd)}
print("weight boxes parsed:", len(boxes))

# ---------- residual metadata ----------
rm = (src / "Sq17Lean/LocalRigidityResidualMetadata.lean").read_text()
mid = {int(m.group(1)): fracs(m.group(2)) for m in re.finditer(r"def mid(\d+) : Fin 3 → ℚ := !\[([^\]]*)\]", rm)}
target = {}
for m in re.finditer(r"def target(\d+) : Fin 45 → ℚ := fun j => if j\.val = (\d+) then (-?1) else 0", rm):
    target[int(m.group(1))] = (int(m.group(2)), int(m.group(3)))
assert len(mid) == 93 and len(target) == 93
rs = (src / "Sq17Lean/LocalRigidityResidualSupport.lean").read_text()
sline = re.search(r"def support : LocalMatrixSupport := (.*)$", rs, re.M).group(1)
sets = re.findall(r"\{([0-9,]*)\}", sline)
assert len(sets) == 4 * 45, len(sets)
support = [[set(int(x) for x in sets[k * 45 + j].split(",") if x) for j in range(45)] for k in range(4)]
wc = (src / "Sq17Lean/LocalRigidityWeightCoverData.lean").read_text()
owner = [int(x) for x in re.search(r"def owner : Fin 93 → Fin 90 := !\[([^\]]*)\]", wc).group(1).split(",")]
first = [int(x) for x in re.search(r"def first : Fin 90 → Fin 93 := !\[([^\]]*)\]", wc).group(1).split(",")]
gl = fracs(re.search(r"def globalLower : Fin 3 → ℚ := !\[([^\]]*)\]", wc).group(1))
gu = fracs(re.search(r"def globalUpper : Fin 3 → ℚ := !\[([^\]]*)\]", wc).group(1))
names = re.search(r'def directionNames : Fin 90 → String := !\[([^\]]*)\]', wc).group(1)
names = [n.strip().strip('"') for n in names.split(",")]
print("owner/first/direction names parsed:", len(owner), len(first), len(names))

# ---------- support soundness: codes outside support are 0 ----------
viol = 0
for k in range(4):
    for j in range(45):
        for i in range(52):
            if i not in support[k][j] and codes[k][i][j] != 0:
                viol += 1
print("support covers every nonzero code:", viol == 0)


# ---------- interval arithmetic exactly as the Lean definitions ----------
def iadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


def imul(a, b):
    p = [a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1]]
    return (min(p), max(p))


def iscale(q, a):
    return imul((q, q), a)


def iabs(a):
    return max(abs(a[0]), abs(a[1]))


def sparse_dot(k, q, j, use_support=True):
    idx = support[k][j] if use_support else range(52)
    lo_ = F(0)
    hi_ = F(0)
    for i in idx:
        s = iscale(q[i], B[k][i][j])
        lo_ += s[0]
        hi_ += s[1]
    return (lo_, hi_)


def center_dot(q, mid_, j, use_support=True):
    r = sparse_dot(0, q, j, use_support)
    for k in range(3):
        r = iadd(r, iscale(mid_[k], sparse_dot(k + 1, q, j, use_support)))
    return r


def residual_budget(i, use_support=True):
    c = boxes[i]
    m = mid[i]
    tj, ts = target[i]
    const = []
    for j in range(45):
        a = center_dot(c["base"], m, j, use_support)
        t = F(ts) if j == tj else F(0)
        const.append(iadd(a, (t, t)))
    lin = [[iadd(center_dot(c["slope"][k], m, j, use_support), sparse_dot(k + 1, c["base"], j, use_support)) for j in range(45)] for k in range(3)]
    quad = [[[sparse_dot(l + 1, c["slope"][k], j, use_support) for j in range(45)] for l in range(3)] for k in range(3)]
    H = c["half"]
    budget = sum(iabs(x) for x in const)
    budget += sum(H[k] * sum(iabs(x) for x in lin[k]) for k in range(3))
    budget += sum(H[k] * H[l] * sum(iabs(x) for x in quad[k][l]) for k in range(3) for l in range(3))
    return budget


def weight_check(i):
    c = boxes[i]
    ok = all(h >= 0 for h in c["half"])
    ok &= all(sum(c["half"][k] * abs(c["slope"][k][r]) for k in range(3)) <= c["base"][r] for r in range(52))
    mass_lhs = sum(c["base"][r] * c["curv"][r] for r in range(52)) + sum(c["half"][k] * abs(sum(c["slope"][k][r] * c["curv"][r] for r in range(52))) for k in range(3))
    ok &= mass_lhs <= c["mass"] and c["mass"] >= 0
    return ok, mass_lhs


worst = F(0)
worst_i = None
all_ok = True
mass_max = F(0)
for i in range(93):
    ok, ml = weight_check(i)
    bud = residual_budget(i)
    # consistency of mid with lo/hi, half with (hi-lo)/2
    assert all(mid[i][k] == (lo[i][k] + hi[i][k]) / 2 for k in range(3)), i
    assert all(boxes[i]["half"][k] == (hi[i][k] - lo[i][k]) / 2 for k in range(3)), i
    assert all(boxes[i]["curv"][r] >= 1 for r in range(52)), i
    assert boxes[i]["mass"] <= 12000, i
    # target matches owner direction
    d = owner[i]
    col = d // 2 if False else None
    all_ok &= ok and bud <= F(1, 4)
    mass_max = max(mass_max, boxes[i]["mass"])
    if bud > worst:
        worst, worst_i = bud, i
print("all 93 weight checks pass:", all_ok)
print("worst residual budget over 93 boxes = %.6f (box %d, direction %s); bound 1/4" % (float(worst), worst_i, names[owner[worst_i]]))
print("max mass over boxes =", mass_max, " (<= 12000; used as 1200000/100)")
# dense cross-check for a few boxes
for i in (0, 55, 56, 92):
    assert residual_budget(i, use_support=False) == residual_budget(i, True)
print("dense == sparse budget on boxes 0,55,56,92: True")

# ---------- cover of the slider box for each of the 90 signed directions ----------
# ordinary directions: first j has global box; direction 55 has boxes 55..58 splitting z
cover_ok = True
for d in range(90):
    bs = [i for i in range(93) if owner[i] == d]
    if d != 55:
        cover_ok &= len(bs) == 1 and lo[bs[0]] == gl and hi[bs[0]] == gu
    else:
        zs = sorted((lo[i][2], hi[i][2]) for i in bs)
        cover_ok &= all(lo[i][0] == gl[0] and hi[i][0] == gu[0] and lo[i][1] == gl[1] and hi[i][1] == gu[1] for i in bs)
        cover_ok &= zs[0][0] == gl[2] and zs[-1][1] == gu[2] and all(zs[t][1] == zs[t + 1][0] for t in range(len(zs) - 1))
        print("direction 55 (%s) z-splits:" % names[55], [(str(a), str(b)) for a, b in zs])
print("93 boxes cover the slider box for all 90 signed directions:", cover_ok)
# targets agree with owner direction: direction 2j = +coordinate j, 2j+1 = -coordinate j
tgt_ok = all(target[i] == (owner[i] // 2, 1 if owner[i] % 2 == 0 else -1) for i in range(93))
print("targets are the signed unit coordinate of the owner direction:", tgt_ok)
# final scalar inequality
q = F(1, 10**7)
print("q/4 + 600000 q^2 < q at q = 1e-7:", F(1, 4) * q + 600000 * q * q < q, " (margin factor %.3f)" % float((F(1, 4) * q + 600000 * q * q) / q))
