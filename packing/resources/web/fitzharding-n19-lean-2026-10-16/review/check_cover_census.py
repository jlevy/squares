"""Independent re-evaluation of sq19's cover, orbit, route and census-coverage data.

Reads the retained Lean sources as data (never runs Lean or the source's tools)
and decides in exact rational arithmetic:

1. cells: the 25 cells of Census/Cells.lean equal Cover/CoverData.lean's, are
   convex, lie in the centre box [1/2, 2193/500]^2, have pairwise disjoint
   interiors and areas summing to the box's, so they tile (cover) the box;
2. symmetry: each of the eight frame symmetries maps every cell's vertex set onto
   the vertex set of `perm g i`, in all three copies of the table;
3. capacity data: interior cells have squared diameter <= 15488/15625 < 1, and the
   wall-cell bounding boxes, moved by `trans`, fit the corner and side windows
   (`wallCheck`); the declared boxes contain the cells;
4. native fact `Sq19.Cover.orbit_check`: every 19-cell set is mapped by some
   symmetry onto a census mask; the census list has one mask per D4 orbit;
5. native facts `CensusRoute.route_checked` and `captureIndex_checked`, and the
   indices of the survivor and capture masks;
6. the 38 survivor images are the D4 images of the seven survivors;
7. census coverage at the combinatorial level: every 19-cell mask other than the
   38 survivor images contains a symmetry image of one of the 269 certified
   patterns, reading each pattern's cell set from its name `P<hex>` in
   expected/axioms.txt (an assumption: the rosters themselves are in the release
   archives, not retained).

    python -I check_cover_census.py SQ19_DIR [--json OUT]

Standard library only.
"""

import argparse
import gzip
import json
import re
import sys
from fractions import Fraction as F
from itertools import combinations

U = F(2443, 500)
LO, HI = F(1, 2), F(2193, 500)
GB = [(False, False, False), (False, True, False), (False, False, True), (False, True, True),
      (True, False, False), (True, True, False), (True, False, True), (True, True, True)]


def rat(s):
    return F(s.replace(" ", ""))


def parse_vertex_block(text, start_marker):
    """The `![ [...], ... ]` vertex table after `start_marker`, one list per cell."""
    i = text.index(start_marker)
    j = text.index("![", i)
    body, depth, k = [], 0, j + 2
    while True:
        c = text[k]
        if c == "[":
            depth += 1
        elif c == "]":
            if depth == 0:
                break
            depth -= 1
        body.append(c)
        k += 1
    cells = []
    for line in "".join(body).splitlines():
        line = line.split("--")[0].strip()
        if not line.startswith("["):
            continue
        pts = re.findall(r"\(([^,()]+),\s*([^()]+?)\)", line)
        cells.append([(rat(a), rat(b)) for a, b in pts])
    return cells


def parse_perm(text, marker):
    i = text.index(marker)
    rows = re.findall(r"!?\[([0-9, ]+)\]", text[i:i + 2000])
    return [[int(x) for x in r.split(",")] for r in rows[:8]]


def act(sw, fx, fy, v):
    x, y = (v[1], v[0]) if sw else v
    return (U - x if fx else x, U - y if fy else y)


def area2(poly):
    return sum(poly[k][0] * poly[(k + 1) % len(poly)][1] - poly[(k + 1) % len(poly)][0] * poly[k][1]
               for k in range(len(poly)))


def convex_ccw(poly):
    n = len(poly)
    for k in range(n):
        a, b, c = poly[k], poly[(k + 1) % n], poly[(k + 2) % n]
        if (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0]) < 0:
            return False
    return area2(poly) > 0


def normals(poly):
    n = len(poly)
    return [(poly[(k + 1) % n][1] - poly[k][1], poly[k][0] - poly[(k + 1) % n][0]) for k in range(n)]


def interiors_disjoint(P, Q):
    for nx, ny in normals(P) + normals(Q):
        pp = [nx * x + ny * y for x, y in P]
        qq = [nx * x + ny * y for x, y in Q]
        if max(pp) <= min(qq) or max(qq) <= min(pp):
            return True
    return False


def img_box(sw, fx, fy, b):
    xl, xh, yl, yh = b
    if sw:
        xl, xh, yl, yh = yl, yh, xl, xh
    if fx:
        xl, xh = U - xh, U - xl
    if fy:
        yl, yh = U - yh, U - yl
    return (xl, xh, yl, yh)


def bits(m):
    return [c for c in range(25) if m >> c & 1]


def apply_perm(p, m):
    out = 0
    for c in bits(m):
        out |= 1 << p[c]
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("sq19")
    ap.add_argument("--json")
    a = ap.parse_args()
    S = a.sq19 + "/Sq19Lean/"
    cells_txt = open(S + "Census/Cells.lean", encoding="utf-8").read()
    cover_txt = open(S + "Cover/CoverData.lean", encoding="utf-8").read()
    orbit_txt = open(S + "Cover/OrbitData.lean", encoding="utf-8").read()
    route_txt = open(S + "Assembly/CensusRouteData.lean", encoding="utf-8").read()
    cap_txt = open(S + "Cover/Capacity.lean", encoding="utf-8").read()
    res, ok = {}, True

    def check(name, cond, detail=None):
        nonlocal ok
        ok &= bool(cond)
        res[name] = {"pass": bool(cond)} | ({"detail": detail} if detail is not None else {})
        print(f"{'PASS' if cond else 'FAIL'}  {name}" + (f": {detail}" if detail is not None else ""))

    # 1. cells
    V = parse_vertex_block(cells_txt, "def vertices")
    V2 = parse_vertex_block(cover_txt, "def vertices")
    check("cells: 25 cells, Census and Cover copies equal", len(V) == 25 and V == V2)
    check("cells: convex and counterclockwise", all(convex_ccw(p) for p in V))
    check("cells: inside the centre box [1/2, 2193/500]^2",
          all(LO <= x <= HI and LO <= y <= HI for p in V for x, y in p))
    bad = [(i, j) for i, j in combinations(range(25), 2) if not interiors_disjoint(V[i], V[j])]
    check("cells: pairwise disjoint interiors", not bad, bad or None)
    total = sum(area2(p) for p in V) / 2
    check("cells: areas sum to the box area, so they tile the box", total == (HI - LO) ** 2,
          f"{total} vs {(HI - LO) ** 2}")

    # 2. symmetry tables
    P_census = parse_perm(cells_txt, "def perm")
    P_cover = parse_perm(orbit_txt, "def perm")
    P_rows = parse_perm(orbit_txt, "def permRows")
    check("perm: the three tables are equal", P_census == P_cover == P_rows)
    vok = all(sorted(act(*GB[g], v) for v in V[i]) == sorted(V[P_cover[g][i]])
              for g in range(8) for i in range(25))
    check("perm: g maps the vertex set of cell i onto that of cell perm g i", vok)
    check("perm: each row a permutation", all(sorted(r) == list(range(25)) for r in P_cover))

    # 3. capacity data
    diam = max(max((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 for p in V[i] for q in V[i]) for i in range(16, 25))
    check("capacity: interior cells' squared diameter <= 15488/15625 < 1", diam <= F(15488, 15625),
          f"max {diam} = {float(diam):.6f}")
    bb = re.findall(r"\(([0-9/]+), ([0-9/]+), ([0-9/]+), ([0-9/]+)\)",
                    cap_txt[cap_txt.index("def bbox"):cap_txt.index("def inBoxQ")])
    bbox = [tuple(rat(x) for x in t) for t in bb]
    check("capacity: declared bounding boxes contain their cells", len(bbox) == 25 and all(
        bbox[i][0] <= x <= bbox[i][1] and bbox[i][2] <= y <= bbox[i][3] for i in range(25) for x, y in V[i]))
    tr = re.findall(r"\((true|false),(true|false),(true|false)\)",
                    cap_txt[cap_txt.index("def trans"):cap_txt.index("def sideStart")].replace(" ", ""))
    trans = [tuple(t == "true" for t in x) for x in tr]
    ss_txt = cap_txt[cap_txt.index("def sideStart"):cap_txt.index("def wallCheck")]
    side_start = [rat(x) for x in re.findall(r"[0-9]+/[0-9]+|\b0\b", ss_txt.split(":=", 1)[1])]
    wall = []
    for i in range(16):
        B = img_box(*trans[i], bbox[i])
        if i < 4:
            wall.append(B[1] <= F(27, 20) and B[3] <= F(27, 20))
        else:
            wall.append(side_start[i] <= B[0] and B[1] <= side_start[i] + F(7287, 10000) and B[3] <= F(1387, 1000))
    check("capacity: wallCheck holds for the 16 wall cells", len(trans) == 16 and len(side_start) == 16 and all(wall))

    # 4. orbit check (native fact Sq19.Cover.orbit_check)
    hexs = orbit_txt.split('def censusHex : String := "', 1)[1].split('"', 1)[0]
    census = [int(w, 16) for w in hexs.split()]
    cset = set(census)
    check("census: 22475 masks, distinct, each 19 of 25 cells",
          len(census) == 22475 and len(cset) == len(census) and all(m < 1 << 25 and m.bit_count() == 19 for m in census))
    tables = [[[0] * 32 for _ in range(5)] for _ in range(8)]
    for g in range(8):
        for ch in range(5):
            for v in range(32):
                out = 0
                for b in range(5):
                    if v >> b & 1:
                        out |= 1 << P_cover[g][5 * ch + b]
                tables[g][ch][v] = out

    def img(g, m):
        t = tables[g]
        return t[0][m & 31] | t[1][m >> 5 & 31] | t[2][m >> 10 & 31] | t[3][m >> 15 & 31] | t[4][m >> 20 & 31]

    full = (1 << 25) - 1
    misses, reps_per_orbit, nsets = 0, {}, 0
    for comp in combinations(range(25), 6):
        m = full
        for c in comp:
            m &= ~(1 << c)
        nsets += 1
        orbit = {img(g, m) for g in range(8)}
        hit = orbit & cset
        if not hit:
            misses += 1
        key = min(orbit)
        reps_per_orbit[key] = len(hit)
    check("orbit_check: every 19-cell set reaches a census mask", misses == 0 and nsets == 177100,
          f"{nsets} sets, {misses} misses")
    check("orbit: one census mask per D4 orbit", len(reps_per_orbit) == 22475 and set(reps_per_orbit.values()) == {1},
          f"{len(reps_per_orbit)} orbits")

    # 5. route (native facts route_checked, captureIndex_checked)
    def hexlist(name):
        body = route_txt.split(f"def {name} : List ℕ := [", 1)[1].split("]", 1)[0]
        return [int(x, 16) for x in re.findall(r"0x([0-9a-f]+)", body)]

    surv_imgs, tree, capture = hexlist("survivorImages"), hexlist("treeMasks"), hexlist("captureMasks")
    exc_raw = route_txt.split('def exceptionsRaw : String := "', 1)[1].split('"', 1)[0]
    exceptions = [int(w) for w in exc_raw.split(" ") if w.isdigit()]

    def excluded(m):
        return m < 1 << 25 and m.bit_count() == 19 and m not in surv_imgs and m not in exceptions

    check("route_checked: every census mask is Excluded, a tree mask or a capture mask",
          all(excluded(m) or m in tree or m in capture for m in census))
    check("captureIndex_checked: capture masks sit only at indices 3435, 3438, 3442",
          all(k in (3435, 3438, 3442) for k, m in enumerate(census) if m in capture))
    idx = {m: k for k, m in enumerate(census)}
    check("indices: tree masks at 1, 2, 5423, 5453; capture masks at 3435, 3438, 3442",
          [idx.get(m) for m in tree] == [1, 2, 5423, 5453] and [idx.get(m) for m in capture] == [3435, 3438, 3442],
          {"tree": [idx.get(m) for m in tree], "capture": [idx.get(m) for m in capture]})
    check("exceptions: the list is empty", exceptions == [])

    # 6. survivor images
    imgs7 = {img(g, m) for m in tree + capture for g in range(8)}
    check("survivorImages: the D4 images of the seven survivors", set(surv_imgs) == imgs7 and len(surv_imgs) == 38,
          f"{len(surv_imgs)} listed, {len(imgs7)} images")

    # 7. census coverage from the 269 pattern names
    ax = gzip.open(a.sq19 + "/expected/axioms.txt.gz", "rt", encoding="utf-8").read().split()
    pats = sorted({int(x.split(".")[2][1:], 16) for x in ax if x.startswith("Sq19.Census.P")})
    gen = open(a.sq19 + "/expected/generated-sources.sha256", encoding="utf-8").read()
    files_ok = all(f"Sq19Lean/Census/Pat/P{p:07x}.lean" in gen and f"Sq19Lean/Census/Pat/P{p:07x}Data.lean" in gen
                   for p in pats)
    check("patterns: 269 names, each with its two generated modules listed", len(pats) == 269 and files_ok)
    images = sorted({img(g, p) for p in pats for g in range(8)})
    avoid = [0] * 25  # avoid[c]: bitset over images that do not use cell c
    for k, im in enumerate(images):
        for c in range(25):
            if not im >> c & 1:
                avoid[c] |= 1 << k
    uncovered, surv_hit = [], []
    sset = set(surv_imgs)
    for comp in combinations(range(25), 6):
        s = avoid[comp[0]] & avoid[comp[1]] & avoid[comp[2]] & avoid[comp[3]] & avoid[comp[4]] & avoid[comp[5]]
        m = full & ~sum(1 << c for c in comp)
        if m in sset:
            if s:
                surv_hit.append(m)
        elif not s:
            uncovered.append(m)
    check("coverage: every non-survivor 19-cell mask contains an image of a pattern (names as rosters)",
          not uncovered, f"{len(uncovered)} uncovered of {177100 - len(sset)}")
    res["survivor_images_containing_a_pattern_image"] = len(surv_hit)
    print(f"note  survivor images that contain a pattern image: {len(surv_hit)} (0 means the census is tight)")
    sizes = {}
    for p in pats:
        sizes[p.bit_count()] = sizes.get(p.bit_count(), 0) + 1
    res["pattern_sizes"] = dict(sorted(sizes.items()))
    res["all_checks_pass"] = ok
    print("PASS" if ok else "FAIL")
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(res, f, indent=1)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
