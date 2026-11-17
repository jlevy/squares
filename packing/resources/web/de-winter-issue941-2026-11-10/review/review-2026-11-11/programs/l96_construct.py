"""Hold #941's construction statements to the certificates, exactly.

L96 review program. Usage: python -I -B l96_construct.py OUT_JSON ABOVE324_DIR
Statements (#941 table and the files' second comment lines):
  539 = 494 plus a border of 45 axis-aligned squares, 590 = 543 + 47, 794 = 739 + 55,
  851 = 794 + 57, 867 = 810 + 57, 910 = 851 + 59; 809 = 810 with one square removed.
For each: the parent's squares appear in the child unchanged (as a multiset of exact
(x, y, t)), the rest number as stated and have t = 0, and the side grows by exactly 1
(border) or not at all (removal). Where the border squares lie is reported.
It decides no packing: each child was decided in full by l96_check.py.
"""

import json
import os
import sys
from collections import Counter
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import l96_read as R  # noqa: E402

BORDERS = [(539, 494, 45), (590, 543, 47), (794, 739, 55), (851, 794, 57), (867, 810, 57), (910, 851, 59)]


def load(d, n):
    with open(os.path.join(d, f"n{n:04d}.cert"), "rb") as fh:
        c = R.read_cert(fh.read())
    return F(*c["side"]), [tuple(F(*v) for v in t) for t in c["squares"]], c["comments"]


def main():
    out_path, d = sys.argv[1:3]
    res = []
    for child, parent, k in BORDERS:
        sc, tc, cc = load(d, child)
        sp, tp, _ = load(d, parent)
        extra = Counter(tc) - Counter(tp)
        missing = Counter(tp) - Counter(tc)
        ex = list(extra.elements())
        item = {
            "child": child,
            "parent": parent,
            "stated_border": k,
            "comment": cc[1] if len(cc) > 1 else None,
            "parent_squares_all_in_child_unchanged": not missing,
            "extra_squares": len(ex),
            "extra_all_axis_aligned": all(t == 0 for _, _, t in ex),
            "side_is_parent_plus_1": sc == sp + 1,
            "parent_order_preserved_as_prefix": tc[: len(tp)] == tp,
        }
        if ex:
            right = [s for s in ex if s[0] > sp]
            top = [s for s in ex if s[1] > sp]
            item["extra_in_column_x_gt_parent_side"] = len(right)
            item["extra_in_row_y_gt_parent_side"] = len(top)
            item["extra_x_values"] = sorted({str(s[0]) for s in right})
            item["extra_y_values"] = sorted({str(s[1]) for s in top})
            item["parent_side_floor"] = int(sp)
            item["l_border_capacity_floor(S)+floor(S+1)"] = int(sp) + int(sp + 1)
        item["as_stated"] = (
            not missing and len(ex) == k and item["extra_all_axis_aligned"] and item["side_is_parent_plus_1"]
        )
        res.append(item)
    s810, t810, _ = load(d, 810)
    s809, t809, c809 = load(d, 809)
    gone = Counter(t810) - Counter(t809)
    added = Counter(t809) - Counter(t810)
    removed = list(gone.elements())
    res.append(
        {
            "child": 809,
            "parent": 810,
            "comment": c809[1] if len(c809) > 1 else None,
            "removed": [[t810.index(r) + 1, str(float(r[0])), str(float(r[1])), str(r[2])] for r in removed],
            "added": len(list(added.elements())),
            "same_side": s809 == s810,
            "as_stated": len(removed) == 1 and not added and s809 == s810,
        }
    )
    out = {"statements": res, "result": "AS_STATED" if all(r["as_stated"] for r in res) else "NOT_AS_STATED"}
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    for r in res:
        print({k: v for k, v in r.items() if k not in ("extra_x_values", "extra_y_values", "comment")})
    print(out["result"])


if __name__ == "__main__":
    main()
