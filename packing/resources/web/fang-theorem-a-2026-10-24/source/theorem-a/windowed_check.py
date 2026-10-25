#!/usr/bin/env python3
"""Run ../verify.py --strict and ../tools/verify_cert_daniel.py, unchanged, on overlapping 4 x 4 windows.

Standalone, stdlib only. Both checkers test every pair of squares, O(n^2), which is slow at
n ~ 10^4 to 10^5. Two unit squares whose centres are more than sqrt(2) apart in x or in y cannot
overlap, and both checkers accept such pairs by their own disc test (|dc|^2 > 2) without a
separating-axis test. Every other pair has |dx|, |dy| <= sqrt(2) < 2, so with m = floor(min x / 2),
l = floor(min y / 2) both centres lie in the window [2m, 2m + 4] x [2l, 2l + 4]. Each square goes to
every window holding its centre (exact rational test), each window is checked by the unmodified
verify() of each checker against the full side S (walls included), and the certificate is valid
iff every window is.

    python3 windowed_check.py certs/k101.cert [more.cert ...]    # exit 0 iff all valid under both
"""
import importlib.util
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


OURS = _load("verify", os.path.join(HERE, "..", "verify.py"))
DANIEL = _load("verify_cert_daniel", os.path.join(HERE, "..", "tools", "verify_cert_daniel.py"))


def windows(points):
    out = defaultdict(list)
    for i, (x, y) in enumerate(points):
        fx, fy = x.numerator // (2 * x.denominator), y.numerator // (2 * y.denominator)
        ms = [m for m in (fx - 2, fx - 1, fx) if 2 * m <= x <= 2 * m + 4]
        ls = [l for l in (fy - 2, fy - 1, fy) if 2 * l <= y <= 2 * l + 4]
        for m in ms:
            for l in ls:
                out[(m, l)].append(i)
    return out


def check(path):
    n, S, sq = OURS.load(path)
    win = windows([(q.x, q.y) for q in sq])
    assert len({i for idx in win.values() for i in idx}) == n
    ok_o = all(OURS.verify(len(idx), S, [sq[i] for i in idx], strict=True)[0] for idx in win.values())
    n2, S2, sq2 = DANIEL.parse(path)
    assert (n2, S2) == (n, S)
    ok_d = all(DANIEL.verify(len(idx), S2, [sq2[i] for i in idx], verbose=False)[0] for idx in win.values())
    return ok_o, ok_d, n, S, len(win)


def main(paths):
    bad = 0
    for p in paths:
        ok_o, ok_d, n, S, nw = check(p)
        bad += not (ok_o and ok_d)
        print(f"{p}: n = {n}, S = {float(S):.12f}, windows = {nw}, verify.py --strict {'VALID' if ok_o else 'INVALID'}, "
              f"verify_cert_daniel.py {'VALID' if ok_d else 'INVALID'}", flush=True)
    print(f"{len(paths) - bad}/{len(paths)} valid under both checkers")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
