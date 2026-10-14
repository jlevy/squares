"""A241 -- `classes178` with the MERGED census installed, exactly as A238's load238.patch_classes does
it, but without pulling in A211's whole page loader (this attempt never builds a tree page).

A178's `classes178` knows only A53's name_to_slots.json (k5 / k6 / trump5 / corners4), so the k <= 4
protected classes and A55's k3_00 / k4_* are invisible to it.  This installs the merged table over the
module's cache and `pins_of` -- ADDED entries only, never a changed one (asserted).  Read-only on A178.
"""
import json
import os
import sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
A241 = os.path.abspath(os.path.join(HERE, ".."))
ROOT = os.path.abspath(os.path.join(A241, "..", ".."))
ATT = os.path.join(ROOT, "attempts")
N2S = [os.path.join(ATT, "A53-simple-strata", "results", "name_to_slots.json"),
       os.path.join(ATT, "A55-k4-sweep", "results", "name_to_slots.json")]
TIER84 = os.path.join(ATT, "A84-protected-trees", "results", "tier84_classes.json")
_CL = None


def raw_slots():
    raw = {}
    for f in N2S:
        if os.path.exists(f):
            for k, v in json.load(open(f, encoding="utf-8")).items():
                raw.setdefault(k, [[float(a), float(b)] for a, b in v])
    if os.path.exists(TIER84):
        for k, d in json.load(open(TIER84, encoding="utf-8")).items():
            pts = [[float(Fr(a)), float(Fr(b))] for a, b in (d.get("pins") or [])]
            if not pts:
                continue
            old = raw.get(k)
            if old is not None:
                assert sorted(map(tuple, old)) == sorted(map(tuple, pts)), \
                    "A241: tier84 disagrees with name_to_slots on %s" % k
            raw[k] = pts
    return raw


def classes():
    """the patched `classes178` module."""
    global _CL
    if _CL is None:
        sys.path.insert(0, os.path.join(ATT, "A178-gallery-geometry", "code"))
        import classes178 as CL                                                 # noqa: E402
        raw = raw_slots()
        CL._N2S = {k: tuple(sorted((round(a, 5), round(b, 5)) for a, b in v)) for k, v in raw.items()}
        CL.pins_of = lambda cls: [tuple(p) for p in raw[cls]]
        CL._SB = None                                                           # always re-read the scoreboard
        _CL = CL
    return _CL
