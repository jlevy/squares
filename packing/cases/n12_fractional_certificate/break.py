# ruff: noqa
# Provenance: independent reviewer's break test, 2026-09-04; see independent_verify.py.
"""Task D: try to break the 77/20 certificate with three small perturbations."""
from fractions import Fraction as Fr
import sys, copy
sys.path.insert(0, "/tmp/claude-0/-home-user-squares/21ae3bfc-58a6-55fc-90e3-6e29d229a7f1/scratchpad/indep")
from verify import load, verify

base = "/home/user/squares/packing/cases/n12_fractional_certificate/"
orig = load(base + "certificate.json")
L = orig["L"]
IDX = 0
x0, y0, w0 = orig["atoms"][IDX]
print("perturbing atom #%d = (%s, %s, %s)\n" % (IDX, x0, y0, w0))

def clone(mut, tag):
    c = copy.deepcopy(orig); c["atoms"] = mut(list(c["atoms"])); c["id"] = orig["id"] + tag
    return c

def orbit(x, y):
    return {(x, y), (L-x, y), (x, L-y), (L-x, L-y), (y, x), (L-y, x), (y, L-x), (L-y, L-x)}

tests = [
    ("P1 weight -1/10000 on one atom",
     clone(lambda A: [(x, y, w - Fr(1,10000)) if i == IDX else (x, y, w)
                      for i, (x, y, w) in enumerate(A)], "+p1")),
    ("P2 drop one atom",
     clone(lambda A: [a for i, a in enumerate(A) if i != IDX], "+p2")),
    ("P3 shift one atom x by +1/1000",
     clone(lambda A: [(x + Fr(1,1000), y, w) if i == IDX else (x, y, w)
                      for i, (x, y, w) in enumerate(A)], "+p3")),
    ("P4 (bonus) weight -1/10000 on the WHOLE D4 orbit (keeps C0)",
     clone(lambda A: [(x, y, w - Fr(1,10000)) if (x, y) in orbit(x0, y0) else (x, y, w)
                      for (x, y, w) in A], "+p4")),
]
# ks: full net is slow here; C4 failure shows at k=0 already, but check the full net
# for any test whose C4 survives k=0.
for name, cert in tests:
    print("### " + name)
    ok, res = verify(cert, ks=None)
    fails = [k for k in ("C0","C1","C2","C3","C4") if not res[k]]
    print("    FAILING CONDITIONS: %s\n" % (", ".join(fails) if fails else "NONE (!!)"))
