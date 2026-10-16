"""Independent check of the property the nine capture-to-hull native facts of sq19 certify.

`Sq19.Capture.Region.{S3442,S3435,S3438}.{sq_ok,wall_ok}` and
`Sq19.Capture.Region.S3435P0.{sq_ok,wall_ok,top_ok}` assert that each capture
target (an angle interval and a polygon of integer half-planes for the centre),
moved by the frame shift, lies in the matching box of the local hull problem
`Hull.prob`. This program reads Capture/Region.lean and Endgame/HullData.lean as
data and decides each assertion in exact rational arithmetic. `sq_check`,
`wall_check` and their mirror and top forms transcribe the source's `sqCheck`
and `wallCheck` (Capture/ToHull.lean:52-59, and ToHullMirror.lean) line for
line; only the source's `impliedOK` is replaced: a half-plane bound is implied
when the maximum of its functional over the target polygon (by vertex
enumeration, after checking that every target polygon is bounded and nonempty)
is within it. So the program is independent of the source in evaluation, not in
formulation, and it decides the property the facts certify, not the value the
source's Boolean `sqCheck ... = true` takes. It also places Wainwright's
configuration (this project's witness) in the hull box.

    python -I check_region.py SQ19_DIR WITNESS_YAML [--json OUT]

Standard library only.
"""

import argparse
import json
import re
import sys
from fractions import Fraction as F
from itertools import combinations

PI_LO = F(314159265358979323846, 10**20) - F(1, 10**20)
PI_HI = F(314159265358979323847, 10**20)
NUM = r"-?\d+(?:/\d+)?"


def parse_targets(text, name):
    body = text.split(f"def {name}.targets : Array Target := #[", 1)[1].split("\n\ndef ", 1)[0]
    out = []
    for m in re.finditer(rf"⟨\(({NUM}) : Rat\), \(({NUM}) : Rat\), \[(.*?)\]⟩", body):
        cons = [tuple(int(x) for x in c) for c in re.findall(r"⟨(-?\d+), (-?\d+), (-?\d+)⟩", m.group(3))]
        out.append((F(m.group(1)), F(m.group(2)), cons))
    return out


def parse_def(text, name, kind="ℚ"):
    m = re.search(rf"def {re.escape(name)} : {kind} := \(({NUM}) : Rat\)", text)
    return F(m.group(1))


def parse_vec(text, name):
    m = re.search(rf"def {re.escape(name)} : Fin 9 → ℕ := !\[([0-9, ]+)\]", text)
    return [int(x) for x in m.group(1).split(",")]


def parse_hull(text):
    body = text.split("def prob : Prob := ⟨[", 1)[1].split("]⟩", 1)[0]
    sqs = []
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("⟨"):
            continue
        s, m = (int(x) for x in re.match(r"⟨(\d+), (\d+),", line).groups())
        q = [F(x) for x in re.findall(rf"\(({NUM}) : ℚ\)", line)]
        assert len(q) == 8, line[:80]
        sqs.append({"s": s, "m": m, "rx": q[0], "ry": q[1], "a": (q[2], q[3]), "x": (q[4], q[5]), "y": (q[6], q[7])})
    return sqs


def vertices(cons):
    """Vertices of {z : a z1 + b z2 <= c for all (a, b, c)}, exact."""
    pts = []
    for (a1, b1, c1), (a2, b2, c2) in combinations(cons, 2):
        det = a1 * b2 - a2 * b1
        if det == 0:
            continue
        x, y = F(c1 * b2 - c2 * b1, det), F(a1 * c2 - a2 * c1, det)
        if all(a * x + b * y <= c for a, b, c in cons):
            pts.append((x, y))
    return pts


def bounded(cons):
    """The polygon's recession cone {d : a d1 + b d2 <= 0 for all (a, b, c)} is {0}.

    A nonzero cone that is not the whole plane has a nonzero boundary ray, and a
    boundary ray lies on some line a d1 + b d2 = 0, so it is +-(-b, a) for some
    constraint; testing those directions decides boundedness exactly.
    """
    dirs = [(s * -b, s * a) for a, b, _ in cons for s in (1, -1) if (a, b) != (0, 0)]
    return bool(dirs) and not any(all(a * u + b * v <= 0 for a, b, _ in cons) for u, v in dirs)


def implied(cons, a, b, c):
    """Every point of the polygon, checked bounded and nonempty, satisfies a x + b y <= c."""
    vs = vertices(cons)
    if not vs or not bounded(cons):
        raise ValueError("empty or unbounded target polygon")
    return max(a * x + b * y for x, y in vs) <= c


def ge_x(r):
    return (-1, 0, -r)


def le_x(r):
    return (1, 0, r)


def ge_y(r):
    return (0, -1, -r)


def le_y(r):
    return (0, 1, r)


def sq_check(t, k, q, A, Amin):
    lo, hi, cons = t
    ang = q["a"][0] <= lo + k * PI_LO / 2 - q["m"] * PI_HI / 4 and hi + k * PI_HI / 2 - q["m"] * PI_LO / 4 <= q["a"][1]
    return ang and all(implied(cons, *h) for h in (
        ge_x(q["rx"] + q["x"][0] + A), le_x(q["rx"] + q["x"][1] + Amin),
        ge_y(q["ry"] + q["y"][0] + A), le_y(q["ry"] + q["y"][1] + Amin)))


def sq_check_mirror(t, k, q, Dlo, Dhi):
    lo, hi, cons = t
    ang = q["a"][0] <= -hi + k * PI_LO / 2 - q["m"] * PI_HI / 4 and -lo + k * PI_HI / 2 - q["m"] * PI_LO / 4 <= q["a"][1]
    return ang and all(implied(cons, *h) for h in (
        le_y(Dlo - q["rx"] - q["x"][0]), ge_y(Dhi - q["rx"] - q["x"][1]),
        le_x(Dlo - q["ry"] - q["y"][0]), ge_x(Dhi - q["ry"] - q["y"][1])))


def wall_check(t, Xw, Phi, A):
    lo, hi, cons = t
    return implied(cons, *le_x(Xw)) and -Phi <= lo and hi <= Phi and 0 <= Phi and Xw - F(1, 2) + Phi**2 / 4 <= A


def top_check(t, Y0, Phi, Dlo):
    lo, hi, cons = t
    return implied(cons, *ge_y(Y0)) and -Phi <= lo and hi <= Phi and 0 <= Phi and Dlo <= Y0 + F(1, 2) - Phi**2 / 4


def read_witness(path):
    text = open(path, encoding="utf-8").read()
    return {int(m.group(1)): (F(m.group(2)), F(m.group(3)), F(m.group(4))) for m in re.finditer(
        r"- id: (\d+)\n\s+center:\n\s+- '([^']+)'\n\s+- '([^']+)'\n\s+angle: '([^']+)'", text)}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("sq19")
    ap.add_argument("witness")
    ap.add_argument("--json")
    a = ap.parse_args()
    reg = open(a.sq19 + "/Sq19Lean/Capture/Region.lean", encoding="utf-8").read()
    hull = parse_hull(open(a.sq19 + "/Sq19Lean/Endgame/HullData.lean", encoding="utf-8").read())
    res, ok = {"hull_squares": [q["s"] for q in hull]}, True
    print(f"Hull.prob: {len(hull)} squares, record numbers {[q['s'] for q in hull]}")
    # Vertex enumeration decides implication only on a bounded, nonempty polygon.
    polys = [cons for st in ("S3442", "S3435", "S3438", "S3435P0") for _, _, cons in parse_targets(reg, st)]
    poly_ok = all(vertices(cons) and bounded(cons) for cons in polys)
    res["target_polygons"], res["target_polygons_bounded_nonempty"] = len(polys), poly_ok
    ok &= poly_ok
    print(f"{'PASS' if poly_ok else 'FAIL'}  all {len(polys)} target polygons are bounded and nonempty")
    for st in ("S3442", "S3435", "S3438"):
        T = parse_targets(reg, st)
        own, kq = parse_vec(reg, f"{st}.own"), parse_vec(reg, f"{st}.kq")
        A, Amin = parse_def(reg, f"{st}.A"), parse_def(reg, f"{st}.Amin")
        Xw, Phi = parse_def(reg, f"{st}.Xw"), parse_def(reg, f"{st}.Phi")
        sq_ok = all(sq_check(T[own[i]], kq[i], hull[i], A, Amin) for i in range(9))
        w_ok = wall_check(T[own[0]], Xw, Phi, A)
        axis = all(x == 0 or y == 0 for _, _, cons in T for x, y, _ in cons)
        res[st] = {"targets": len(T), "sq_ok": sq_ok, "wall_ok": w_ok, "axis_aligned_targets": axis}
        ok &= sq_ok and w_ok and len(T) == 19
        print(f"{'PASS' if sq_ok else 'FAIL'}  Region.{st}.sq_ok   ({len(T)} targets)")
        print(f"{'PASS' if w_ok else 'FAIL'}  Region.{st}.wall_ok")
    st = "S3435P0"
    T = parse_targets(reg, st)
    own, kq = parse_vec(reg, f"{st}.own"), parse_vec(reg, f"{st}.kq")
    A, Xw, Phi = parse_def(reg, f"{st}.A"), parse_def(reg, f"{st}.Xw"), parse_def(reg, f"{st}.Phi")
    Y0, Phi2 = parse_def(reg, f"{st}.Y0"), parse_def(reg, f"{st}.Phi2")
    Dlo, Dhi = parse_def(reg, f"{st}.Dlo"), parse_def(reg, f"{st}.Dhi")
    sq_ok = all(sq_check_mirror(T[own[i]], kq[i], hull[i], Dlo, Dhi) for i in range(9))
    w_ok, t_ok = wall_check(T[2], Xw, Phi, A), top_check(T[0], Y0, Phi2, Dlo)
    ok &= sq_ok and w_ok and t_ok and len(T) == 19
    res[st] = {"targets": len(T), "sq_ok": sq_ok, "wall_ok": w_ok, "top_ok": t_ok}
    for n, v in (("sq_ok", sq_ok), ("wall_ok", w_ok), ("top_ok", t_ok)):
        print(f"{'PASS' if v else 'FAIL'}  Region.{st}.{n}")
    # Wainwright's configuration in the hull box H.
    wit = read_witness(a.witness)
    margins = []
    for q in hull:
        x, y, ang = wit[q["s"]]
        dx, dy = x - q["rx"], y - q["ry"]
        theta = 0 if (ang - 45 * q["m"]) == 0 else None
        inside = theta == 0 and q["x"][0] <= dx <= q["x"][1] and q["y"][0] <= dy <= q["y"][1] and q["a"][0] <= 0 <= q["a"][1]
        margins.append(min(dx - q["x"][0], q["x"][1] - dx, dy - q["y"][0], q["y"][1] - dy, -q["a"][0], q["a"][1]))
        ok &= inside
    res["wainwright_in_H_min_margin"] = float(min(margins))
    print(f"{'PASS' if min(margins) > 0 else 'FAIL'}  Wainwright's configuration lies in H (min margin {float(min(margins)):.3g})")
    res["all_checks_pass"] = ok
    print("PASS" if ok else "FAIL")
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(res, f, indent=1)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
