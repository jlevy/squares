"""Are the source's built boards mu_k (verification/boards/box<k>.txt) equal, as measures, to mu_k built here from
the family file by the paper's Definition 3?  (review of #973, L144)
usage: python -I boards_vs_family.py FAMILY BOX10 BOX12 ...
"""
import json
import os
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from k2m5_cover import read_board, read_family, family_pieces, build_mu, key_of, add  # noqa: E402

om, nu = family_pieces(*read_family(sys.argv[1]))
out = {}
for path in sys.argv[2:]:
    b = read_board(path)
    k = int(b["side"])
    m = {}
    for x0, y0, x1, y1, w in b["segs"]:
        add(m, key_of(x0, y0, x1, y1), F(w, b["wden"]))
    mk, leb = build_mu(om, nu, k)
    p = b["polys"][0]
    xs, ys = p[2::2], p[3::2]
    rect_ok = (min(xs), max(xs)) == leb and (min(ys), max(ys)) == leb and F(p[1], b["wden"]) == F((leb[1] - leb[0]) ** 2, 100)
    out[os.path.basename(path)] = dict(k=k, equal=m == mk, rect_ok=rect_ok, pieces=len(m))
print(json.dumps(out))
