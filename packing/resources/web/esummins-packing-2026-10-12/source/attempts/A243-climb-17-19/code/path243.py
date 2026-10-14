"""A243 -- the import path, enforced (A238's rule): [A243/code, A211/code (the LIVE k5 toolkit), ...].  A212's frozen
copies are never on the path.  fix() is idempotent; check() asserts every shared module came from A211."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ATT = os.path.join(ROOT, "attempts")
A211 = os.path.join(ATT, "A211-coarse-tree", "code")
A212 = os.path.join(ATT, "A212-trump5-tree", "code")
SHARED = ("tree211", "tree206", "tree209", "coarse211", "leaves211", "poly204", "load211", "stage209", "run211")


def fix():
    while A212 in sys.path:
        sys.path.remove(A212)
    for p in (A211, HERE):
        while p in sys.path:
            sys.path.remove(p)
        sys.path.insert(0, p)
    return sys.path


def check():
    bad = []
    for name in SHARED:
        m = sys.modules.get(name)
        if m is not None and os.path.dirname(os.path.abspath(m.__file__)) != A211:
            bad.append((name, m.__file__))
    return bad


fix()
