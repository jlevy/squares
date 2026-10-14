"""A213 -- the A211d stage table from a cProfile dump:  python stages213.py before.prof [after.prof ...]
Rows: cumulative seconds of the functions that delimit the stages (rebuild = MBox.rebuild and its parts, the clip
primitive, no-room, the role reach), plus the wall.  Same rows for the library build and the integer-space build."""
import os
import pstats
import sys

ROWS = [
    ("run_page (wall)", [("run211.py", "run_page")]),
    ("tree normalise (fixed point)", [("tree205.py", "normalise")]),
    ("  MBox.rebuild (library-level)", [("multibox.py", "rebuild")]),
    ("    pieces_poly", [("multibox.py", "pieces_poly"), ("polycore_int.py", "pieces_poly")]),
    ("      polycore.build (per piece / union)", [("polycore.py", "build"), ("polycore_fast.py", "build")]),
    ("        _clip / _clip_np", [("polycore.py", "_clip"), ("polycore_fast.py", "_clip_np")]),
    ("        _simplify / _simplify_np", [("polycore.py", "_simplify"), ("polycore_fast.py", "_simplify_np")]),
    ("      intersect_frac / intersect_h", [("multibox.py", "intersect_frac"), ("polycore_int.py", "intersect_h")]),
    ("      certify_verts", [("multibox.py", "certify_verts"), ("polycore_int.py", "certify_verts"), ("polycore_vec.py", "certify_verts")]),
    ("    axis_core_pieces", [("multibox.py", "axis_core_pieces"), ("polycore_int.py", "axis_core_pieces")]),
    ("    exactcore.exact_core", [("exactcore.py", "exact_core")]),
    ("    vertex_ok (all callers)", [("polycore.py", "vertex_ok"), ("polycore_int.py", "vertex_ok")]),
    ("    vertex_ok_h (integer kernel)", [("polycore_int.py", "vertex_ok_h")]),
    ("  _clip_rect_obstacle (library / integer space)", [("multibox.py", "_clip_rect_obstacle"), ("pinclip_int.py", "clip_rect_obstacle")]),
    ("    dead_poly -> dead_int (the exact test)", [("multibox.py", "dead_poly"), ("pinclip_int.py", "dead_int")]),
    ("    _dead_poly_f -> dead_f (the search twin)", [("multibox.py", "_dead_poly_f"), ("pinclip_int.py", "dead_f")]),
    ("    _m_lt_half + _m_lt_half_f (A131, now inlined)", [("pinclip.py", "_m_lt_half"), ("pinclip.py", "_m_lt_half_f")]),
    ("    _bisect_boundary (A131, reused verbatim)", [("pinclip.py", "_bisect_boundary")]),
    ("    IPair (the per (obstacle, bin) compile)", [("pinclip_int.py", "__init__")]),
    ("no-room leaf (noroom189)", [("noroom189.py", "noroom")]),
    ("role reach depth 0 (fastclip211.reach0)", [("fastclip211.py", "reach0")]),
    ("Fraction arithmetic (_mul + _add + _sub + gcd)", [("fractions.py", "_mul"), ("fractions.py", "_add"), ("fractions.py", "_sub"), ("~", "math.gcd")]),
]


def table(path):
    st = pstats.Stats(path).stats
    out = {}
    for name, keys in ROWS:
        ct = 0.0
        nc = 0
        for (f, _l, fn), (_cc, n, tt, c, _callers) in st.items():
            base = os.path.basename(f)
            for (kf, kfn) in keys:
                if kf == "~" and fn == "<built-in method %s>" % kfn and f == "~":
                    ct += tt
                    nc += n
                elif base == kf and fn == kfn:
                    ct += c
                    nc += n
        out[name] = (nc, ct)
    return out


def main():
    tabs = [(os.path.basename(p), table(p)) for p in sys.argv[1:]]
    w = max(len(r[0]) for r in ROWS)
    print("| stage / function | " + " | ".join("%s calls | %s s" % (n, n) for n, _t in tabs) + " |")
    print("|" + "---|" * (1 + 2 * len(tabs)))
    for name, _keys in ROWS:
        cells = []
        for _n, t in tabs:
            nc, ct = t[name]
            cells.append("%d | %.1f" % (nc, ct))
        print("| %s | %s |" % (name.ljust(w), " | ".join(cells)))


if __name__ == "__main__":
    main()
