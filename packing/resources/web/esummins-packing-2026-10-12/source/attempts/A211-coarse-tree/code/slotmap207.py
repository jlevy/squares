"""A207 -- the map (page class S, forced slot p) -> (extension class T = S u {p}, the D4 element g with g(pins(S) u {c_p}) =
name_to_slots[T], the index of g(c_p) among T's slots).  Computed from A178 classes178 (read-only) and A53's class table;
the basin (r_c, t_r) is D4-invariant (an l-inf box around the centre, a symmetric tilt interval), so only the centre moves."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "attempts", "A178-gallery-geometry", "code"))
import classes178 as CL                                        # noqa: E402  READ-ONLY (A178)

S0 = CL.S0
D4 = [("id", lambda x, y: (x, y)), ("x->s-x", lambda x, y: (S0 - x, y)), ("y->s-y", lambda x, y: (x, S0 - y)),
      ("rot180", lambda x, y: (S0 - x, S0 - y)), ("swap", lambda x, y: (y, x)), ("(s-y,x)", lambda x, y: (S0 - y, x)),
      ("(y,s-x)", lambda x, y: (y, S0 - x)), ("(s-y,s-x)", lambda x, y: (S0 - y, S0 - x))]
_TAB = None


def table():
    global _TAB
    if _TAB is None:
        _TAB = json.load(open(CL.NAME_TO_SLOTS, encoding="utf-8"))
    return _TAB


def slot_map(cls):
    """{cell: dict(ext, g, centre (page frame), cert_centre, idx, corner, i, j, status)} over the USABLE forced cells of cls."""
    pins = CL.pins_of(cls)
    out = {}
    for r in CL.forced_cells(cls):
        if not r["usable"]:
            continue
        c = CL.slot_centre(r["corner"], r["i"], r["j"])
        ext = r["extension"]
        target = set((round(a, 5), round(b, 5)) for a, b in table()[ext])
        for nm, f in D4:
            im = set((round(a, 5), round(b, 5)) for a, b in (f(x, y) for x, y in pins + [c]))
            if im == target:
                gc = f(*c)
                idx = [k for k, (a, b) in enumerate(table()[ext]) if abs(a - gc[0]) < 1e-5 and abs(b - gc[1]) < 1e-5][0]
                out[r["cell"]] = dict(ext=ext, g=nm, centre=(c[0], c[1]), cert_centre=(gc[0], gc[1]), idx=idx, corner=r["corner"], i=r["i"], j=r["j"], status=r["status"])
                break
        else:
            raise ValueError("%s %s: no D4 image of the pins + slot is the census frame of %s" % (cls, r["cell"], ext))
    return out


def all_slots(classes=("k5_16", "k5_11", "trump5")):
    out = []
    for cls in classes:
        for cell, d in slot_map(cls).items():
            out.append(dict(d, cls=cls, cell=cell))
    return out


if __name__ == "__main__":
    for d in all_slots():
        print("%-7s %-8s -> %s core %d via %-9s cert centre %s   [%s]" % (d["cls"], d["cell"], d["ext"], d["idx"], d["g"], d["cert_centre"], (d["status"] or "")[:50]))
