"""A211f -- the per-stage table of a run's cProfile, in A211d/A211e's own rows, so two runs can be compared.

    python profstage211.py <file.prof> [<file.prof> ...]

Each row is the CUMULATIVE time of one named function (the stage's entry point), summed over every code object with
that (file basename, function name) -- the same numbers A211d and A211e reported by hand.
"""
import pstats
import sys

ROWS = [
    ("coarse fixed point", [("coarse211.py", "coarse_fixpoint")]),
    ("  ... normalise (page)", [("coarse211.py", "normalise")]),
    ("no-room leaf (A189)", [("tree209.py", "noroom_at")]),
    ("  ... build_node [outer]", [("noroom189.py", "build_node"), ("noroommemo211.py", "build_memo")]),
    ("  ... bisect_free [outer]", [("noroom189.py", "bisect_free"), ("noroommemo211.py", "bisect_memo")]),
    ("  ... lane", [("multibox.py", "lane")]),
    ("option table (build_options)", [("tree205b.py", "build_options"), ("tree206.py", "build_options")]),
    ("  ... ROLE-REACH", [("coarse211.py", "role_reach")]),
    ("MBox.rebuild (K') [outer]", [("multibox.py", "rebuild"), ("mbpatch178.py", "rebuild"), ("fastclip211.py", "rebuild_memo"),
                           ("coarse211.py", "grid_rebuild")]),
    ("  ... pieces_poly", [("multibox.py", "pieces_poly"), ("polycore_int.py", "pieces_poly")]),
    ("  ... union_pc", [("multibox.py", "union_pc")]),
    ("  ... polycore.build", [("polycore.py", "build"), ("polycore_int.py", "build"), ("polycore_fast.py", "build")]),
    ("_clip_rect_obstacle [outer]", [("multibox.py", "_clip_rect_obstacle"), ("fastclip211.py", "clip_memo")]),
    ("start load (INHERIT)", [("startload211.py", "load")]),
    ("leaf rules (CC / basin / NS)", [("tree211.py", "leaf_rules")]),
]


def cum(st, keys, outer=False):
    """the CUMULATIVE seconds of a stage.  `outer`: the entries are WRAPPERS of one another (a memo around the
    library function), so their cumulative times nest -- take the largest instead of the sum."""
    vals = {}
    for (fn, _ln, name), (_cc, _nc, _tt, ct, _cl) in st.stats.items():
        base = fn.replace("\\", "/").rsplit("/", 1)[-1]
        if (base, name) in keys:
            vals[(base, name)] = vals.get((base, name), 0.0) + ct
    if not vals:
        return 0.0
    return max(vals.values()) if outer else sum(vals.values())


def main(paths):
    S = [(p, pstats.Stats(p)) for p in paths]
    tot = [s.total_tt for _p, s in S]
    print("%-32s %s" % ("stage", "  ".join("%12s" % p.rsplit("/", 1)[-1].rsplit("\\", 1)[-1][:12] for p, _ in S)))
    print("%-32s %s" % ("TOTAL (s)", "  ".join("%12.1f" % t for t in tot)))
    for label, keys in ROWS:
        ks = set(keys)
        vals = [cum(s, ks, outer="[outer]" in label) for _p, s in S]
        if not any(v > 0.05 for v in vals):
            continue
        print("%-32s %s" % (label, "  ".join("%8.1f %4.1f%%" % (v, 100.0 * v / t if t else 0) for v, t in zip(vals, tot))))


if __name__ == "__main__":
    main(sys.argv[1:])
