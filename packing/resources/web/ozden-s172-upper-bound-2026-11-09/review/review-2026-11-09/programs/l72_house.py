"""Read a rational centre-basis Witness/v2 file as exact corners (lane L72, bead think-qqyg).

For the house witnesses under packing/witnesses/known-best/ and the regularized views under
packing/atlas/known-best/regularized/ (gzip). The YAML goes through the frozen reader's
generic conversion (l72_reader.yaml_tree: every scalar a string, aliases, tags and duplicate
keys refused); this module then requires representation center-basis, rational scalars, the
lower-left origin, and for every square a rational centre and a basis [c, s] with
c^2 + s^2 = 1 exactly. Corners are built exactly: u = (c, s), f = perp(u),
p0 = centre - u/2 - f/2, p1 = p0 + u, p2 = p0 + u + f, p3 = p0 + f (counterclockwise).
Returns the integer layout l72_check.decide_data takes.
"""

import gzip
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fractions import Fraction  # noqa: E402

import l72_reader as reader  # noqa: E402


class HouseError(Exception):
    pass


def _rat(text, what):
    m = reader.RAT_RE.match(text) if isinstance(text, str) else None
    if not m:
        raise HouseError(f"{what}: {str(text)[:50]!r} is not an integer or p/q")
    return Fraction(int(m.group(1)), int(m.group(2)) if m.group(2) else 1)


def read_center_basis(path):
    with open(path, "rb") as fh:
        data = fh.read()
    if path.endswith(".gz"):
        data = gzip.decompress(data)
    tree = reader.yaml_tree(data.decode("utf-8"))
    w = tree.get("witness")
    if not isinstance(w, dict):
        raise HouseError("no witness mapping")
    if w.get("representation") != "center-basis":
        raise HouseError(f"representation {w.get('representation')!r}")
    if w.get("scalar") != {"kind": "rational"}:
        raise HouseError("scalars are not rational")
    coords = w.get("coordinates", {})
    if coords.get("origin") != "lower-left" or coords.get("axes") != "x-right-y-up":
        raise HouseError("coordinates are not lower-left, x-right-y-up")
    if w.get("square_size") != "1":
        raise HouseError("square_size is not '1'")
    n = int(w["n"])
    side = _rat(w["side"], "side")
    squares = w["squares"]
    if len(squares) != n:
        raise HouseError(f"{len(squares)} squares where n is {n}")
    ids, corners, centres, bases = [], [], [], []
    for k, sq in enumerate(squares):
        sid = int(sq["id"])
        cx, cy = (_rat(v, f"square {k} centre") for v in sq["center"])
        c, s = (_rat(v, f"square {k} basis") for v in sq["basis"])
        if c * c + s * s != 1:
            raise HouseError(f"square {sid}: basis is not a unit vector")
        u = (c, s)
        f = (-s, c)
        p0 = (cx - u[0] / 2 - f[0] / 2, cy - u[1] / 2 - f[1] / 2)
        P = [p0, (p0[0] + u[0], p0[1] + u[1]), (p0[0] + u[0] + f[0], p0[1] + u[1] + f[1]), (p0[0] + f[0], p0[1] + f[1])]
        ids.append(sid)
        corners.append(tuple((x.numerator, x.denominator, y.numerator, y.denominator) for x, y in P))
        centres.append((cx, cy))
        bases.append((c, s))
    if len(set(ids)) != n:
        raise HouseError("repeated square id")
    return {
        "n": n,
        "side": (side.numerator, side.denominator),
        "ids": ids,
        "corners": corners,
        "centres": centres,
        "bases": bases,
        "witness_id": w.get("id"),
        "meta": {"witness_id": w.get("id"), "schema": tree.get("softschema", {}).get("schema")},
    }
