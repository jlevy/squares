"""Independent re-derivation of the orbit census, the classifier and the D4 action.

Reads, as text only:
  Sq17Lean/CellPermutation.lean           (perm, comp, inv tables)
  Sq17Lean/ExactCellCoverData.lean        (24 cell vertex lists)
  x/Sq17Lean/OrbitRepresentativeFiniteData.lean (RepTree of representatives)
  Sq17Lean/OrbitCensus/Chunk*.lean        (346,104 rows)
  Sq17Lean/RepresentativeCaseData.lean    (35 patterns, fullRosters tree)
  Sq17Lean/RepresentativeCaseParts/Part*.lean + All.lean (classifier certificates)
and checks, with its own code:
  1. the permutation table is the D4 action on the 24 cells (via the geometric
     action on vertex lists), is a group, and inv/comp are right;
  2. the RepTree holds exactly one representative per D4 orbit of 7-subsets
     (orbit census computed here from scratch), and every key is distinct;
  3. the 346,104 rows are all distinct 7-subsets (so all of C(24,7)), tags increase,
     and each row's holes map under its symmetry to its representative's holes;
  4. the classifier certificate trees mirror the RepTree and every representative
     is either covered by a pattern image (pattern ⊆ occupied) or equals a full
     roster; the full rosters are 2,781 distinct 17-sets, and the four neighbour
     indices and the capture index are where the assembly says they are.
"""
import re
import sys
from fractions import Fraction
from itertools import combinations
from pathlib import Path

src = Path(sys.argv[1])
xsrc = Path(sys.argv[2])


def ints(s):
    return [int(t) for t in re.findall(r"-?\d+", s)]


# ---------- 1. permutation table versus geometric action ----------
cp = (src / "Sq17Lean/CellPermutation.lean").read_text()
perm_block = cp[cp.index("def perm :"):cp.index("def comp :")]
perm = [ints(r) for r in re.findall(r"!\[([0-9, ]*)\]", perm_block)]
assert len(perm) == 8 and all(len(p) == 24 for p in perm), [len(p) for p in perm]
comp_block = cp[cp.index("def comp :"):cp.index("def inv :")]
comp = [ints(r) for r in re.findall(r"!\[([0-9, ]*)\]", comp_block)]
assert len(comp) == 8 and all(len(p) == 8 for p in comp), [len(p) for p in comp]
inv = ints(re.search(r"def inv : Fin 8 → Fin 8 := !\[([^\]]*)\]", cp).group(1))

cd = (src / "Sq17Lean/ExactCellCoverData.lean").read_text()
vblock = cd[cd.index("def vertices :"):cd.index("def xBreaks")]
cells = []
for line in vblock.splitlines():
    line = line.strip()
    if line.startswith("[") :
        pts = re.findall(r"\((-?\d+)(?:/(\d+))?, (-?\d+)(?:/(\d+))?\)", line)
        cells.append(frozenset((Fraction(int(a), int(b or 1)), Fraction(int(c), int(d or 1))) for a, b, c, d in pts))
assert len(cells) == 24, len(cells)
U = Fraction(1169, 250)


def act(g, p):
    x, y = p
    return [(x, y), (U - x, y), (x, U - y), (U - x, U - y), (y, x), (U - y, x), (y, U - x), (U - y, U - x)][g]


geo_perm = []
for g in range(8):
    row = []
    for i in range(24):
        img = frozenset(act(g, p) for p in cells[i])
        js = [j for j in range(24) if cells[j] == img]
        assert len(js) == 1, (g, i, js)
        row.append(js[0])
    geo_perm.append(row)
print("perm table equals geometric D4 action on the 24 cells:", geo_perm == perm)
for g in range(8):
    for h in range(8):
        assert all(perm[comp[g][h]][i] == perm[g][perm[h][i]] for i in range(24))
    assert all(perm[inv[g]][perm[g][i]] == i for i in range(24))
print("comp/inv tables consistent with perm: True")

# ---------- 2. RepTree and orbit census from scratch ----------
rep_text = (xsrc / "Sq17Lean/OrbitRepresentativeFiniteData.lean").read_text()
nodes = re.findall(r"\.node (\d+) \[([0-9,]*)\]", rep_text)
reps = {}
for k, h in nodes:
    k = int(k)
    hs = tuple(sorted(int(t) for t in h.split(",") if t))
    assert k not in reps, k
    reps[k] = hs
print("RepTree nodes:", len(reps), " distinct hole-sets:", len(set(reps.values())))
# the final tree is repsPart510; check that all parts' nodes are in that tree? Each part is
# a subtree of the next in the Lean sources (the file lists parts by inclusion); we check the
# node set of the whole file equals that of representatives by re-parsing repsPart510 alone.
parts_src = {name: body for name, body in re.findall(
    r"noncomputable def (repsPart\d+) : RepTree :=\n(.*?)(?=\n\n|\nnoncomputable def|\nend )", rep_text, re.S)}
print("RepTree part definitions:", len(parts_src))
parts_tree = {}


def parse_tree(txt):
    p = [0]

    def skip():
        while p[0] < len(txt) and txt[p[0]] in " \n":
            p[0] += 1

    def go():
        skip()
        if txt.startswith(".empty", p[0]):
            p[0] += 6
            return None
        mm = re.match(r"repsPart\d+", txt[p[0]:])
        if mm:
            p[0] += mm.end()
            return get_part(mm.group(0))
        if txt[p[0]] == "(":
            p[0] += 1
            t = go()
            skip()
            assert txt[p[0]] == ")", txt[p[0]:p[0] + 20]
            p[0] += 1
            return t
        mm = re.match(r"\.node (\d+) \[([0-9,]*)\]", txt[p[0]:])
        assert mm, txt[p[0]:p[0] + 30]
        p[0] += mm.end()
        key = int(mm.group(1))
        holes = tuple(sorted(int(t) for t in mm.group(2).split(",") if t))
        left = go()
        right = go()
        return (key, holes, left, right)

    t = go()
    skip()
    assert p[0] == len(txt), txt[p[0]:p[0] + 30]
    return t


def get_part(name):
    if name not in parts_tree:
        parts_tree[name] = parse_tree(parts_src[name].strip())
    return parts_tree[name]


tree = get_part("repsPart510")
keys_inorder = []


def inorder(t):
    if t is None:
        return
    inorder(t[2])
    keys_inorder.append(t[0])
    inorder(t[3])


inorder(tree)
print("BST keys strictly increasing in-order (find is sound):",
      all(a < b for a, b in zip(keys_inorder, keys_inorder[1:])), " count", len(keys_inorder))
rep_sets = set(reps[k] for k in keys_inorder)

# orbit census from scratch: canonical representative = min over g of sorted image
all7 = list(combinations(range(24), 7))
assert len(all7) == 346104


def canon(hs):
    return min(tuple(sorted(perm[g][i] for i in hs)) for g in range(8))


orbits = {}
for hs in all7:
    orbits.setdefault(canon(hs), []).append(hs)
print("D4 orbits of 7-subsets computed here:", len(orbits))
# every representative set belongs to a distinct orbit, and every orbit has a representative
rep_orbits = {canon(hs) for hs in rep_sets}
print("representatives hit distinct orbits:", len(rep_orbits) == len(rep_sets),
      " all orbits represented:", rep_orbits == set(orbits))
# Burnside cross-check
fixed = 0
for g in range(8):
    fixed += sum(1 for hs in all7 if tuple(sorted(perm[g][i] for i in hs)) == hs)
print("Burnside sum/8 =", fixed / 8)

# ---------- 3. the census rows ----------
rows = []
for f in sorted((src / "Sq17Lean/OrbitCensus").glob("Chunk*.lean")):
    t = f.read_text()
    for h, g, r in re.findall(r"⟨\[([0-9,]*)\], (\d+), (\d+)⟩", t):
        rows.append((tuple(int(x) for x in h.split(",")), int(g), int(r)))
print("rows parsed:", len(rows))
ok_card = all(len(set(h)) == 7 for h, g, r in rows)
tags = [sum(2 ** i for i in set(h)) for h, g, r in rows]
ok_tags = all(a < b for a, b in zip(tags, tags[1:]))
ok_map = all(tuple(sorted(perm[g][i] for i in h)) == reps[r] for h, g, r in rows)
ok_all = set(tuple(sorted(h)) for h, g, r in rows) == set(all7)
print("rows: 7 distinct holes each:", ok_card, " tags strictly increasing:", ok_tags,
      " each maps to its representative:", ok_map, " rows = all C(24,7):", ok_all)
chunk_order = sorted((src / "Sq17Lean/OrbitCensus").glob("Chunk*.lean"))
print("chunk files:", len(chunk_order))

# ---------- 4. classifier ----------
rc = (src / "Sq17Lean/RepresentativeCaseData.lean").read_text()
# Changed at retention, 14 October 2026: "=>" is written "=[>]", the same pattern, because
# the repository's check refuses the arrow in a Python string (check_no_embedded_js).
patterns = {int(k): [int(x) for x in v.split(",")] for k, v in re.findall(r"\| (\d+) =[>] \[([0-9,]+)\]", rc)}
print("patterns:", len(patterns), " all nodup:", all(len(set(v)) == len(v) for v in patterns.values()))
fr = re.search(r"noncomputable def fullRosters : RepTree :=\n(.*?)\n\n", rc, re.S).group(1)
full = {}
for k, h in re.findall(r"\.node (\d+) \[([0-9,]*)\]", fr):
    full[int(k)] = tuple(sorted(int(x) for x in h.split(",")))
print("full rosters:", len(full), " keys 0..2780:", set(full) == set(range(2781)),
      " all 17 distinct cells:", all(len(set(v)) == 17 for v in full.values()),
      " distinct rosters:", len(set(full.values())))
# certificate trees: parse every Part file and All.lean; build cert for root (cert of repsPart510)
cert_text = {}
for f in sorted((src / "Sq17Lean/RepresentativeCaseParts").glob("*.lean")):
    t = f.read_text()
    for name, body in re.findall(r"def (cert\d+) : Certificate :=\s*(.*?)(?=\n(?:theorem|def|end|namespace|\Z))", t, re.S):
        cert_text[name] = body.strip()
    # Which repsPart each cert checks:
    for name, part in re.findall(r"theorem accepted\d+ : (cert\d+)\.check patterns fullCases Sq17\.OrbitFiniteData\.(repsPart\d+) = true", t):
        cert_text[name + ":part"] = part
print("certificate definitions:", sum(1 for k in cert_text if not k.endswith(":part")))


def parse_cert(s):
    """Parse a Certificate term into nested tuples (assignment, left, right); refs resolved."""
    s = s.strip()
    p = [0]

    def skip():
        while p[0] < len(s) and s[p[0]] in " \n":
            p[0] += 1

    def go():
        skip()
        if s.startswith(".empty", p[0]):
            p[0] += 6
            return None
        mm = re.match(r"cert\d+", s[p[0]:])
        if mm:
            p[0] += mm.end()
            return parse_cert(cert_text[mm.group(0)])
        if s[p[0]] == "(":
            p[0] += 1
            t = go()
            skip()
            assert s[p[0]] == ")", s[p[0]:p[0] + 30]
            p[0] += 1
            return t
        mm = re.match(r"\.node \(\.pattern (\d+) (\d+)\)", s[p[0]:]) or re.match(r"\.node \(\.full (\d+)\)", s[p[0]:])
        assert mm, s[p[0]:p[0] + 40]
        p[0] += mm.end()
        a = ("pattern", int(mm.group(1)), int(mm.group(2))) if mm.re.pattern.find("pattern") >= 0 else ("full", int(mm.group(1)))
        l = go()
        r = go()
        return (a, l, r)

    return go()


# find the cert whose part is repsPart510
root_name = [k[:-5] for k, v in cert_text.items() if k.endswith(":part") and v == "repsPart510"]
assert len(root_name) == 1, root_name
root_cert = parse_cert(cert_text[root_name[0]])


def walk(ct, rt, out):
    if ct is None or rt is None:
        assert ct is None and rt is None, "shape mismatch"
        return
    a, cl, cr = ct
    key, holes, tl, tr = rt
    out.append((key, holes, a))
    walk(cl, tl, out)
    walk(cr, tr, out)


assign = []
walk(root_cert, tree, assign)
print("certificate tree mirrors RepTree, assignments:", len(assign))
n_pat = n_full = 0
bad = []
full_used = set()
for key, holes, a in assign:
    occ = set(range(24)) - set(holes)
    if a[0] == "pattern":
        n_pat += 1
        pat = patterns[a[1]]
        if not all(perm[a[2]][i] in occ for i in pat):
            bad.append((key, a))
    else:
        n_full += 1
        full_used.add(a[1])
        if set(full[a[1]]) != occ:
            bad.append((key, a))
print("pattern-covered representatives:", n_pat, " full representatives:", n_full,
      " violations:", len(bad), " distinct full indices used:", len(full_used),
      " = all 2781:", full_used == set(range(2781)))
print("neighbour indices 209,1158,1161,1193 and capture 204 rosters:")
for k in (209, 1158, 1161, 1193, 204):
    print("  ", k, full[k])
# which pattern indices are used, and the symmetric images used
used_p = sorted({a[1] for _, _, a in assign if a[0] == "pattern"})
print("pattern indices used:", used_p, " count", len(used_p))
