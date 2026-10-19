"""Exact check of the endpoint packing in sq19's EndpointPacking.lean.

Reads the nineteen `noncomputable def S<k> := sq cx cy ux uy` lines as data (it
never runs Lean or the source's generator), and decides in exact arithmetic over
Q(sqrt 2) that each square is a unit square, lies in [0, side19]^2 with
side19 = 3 + 4 sqrt(2)/3, and that every pair is weakly separated by one of the
four edge normals (so the interiors are disjoint). It then compares the squares,
in order, with this project's known-best witness for n = 19.

    python -I check_endpoint.py SQ19_DIR WITNESS_YAML [--json OUT]

Standard library only.
"""

import argparse
import json
import re
import sys
from fractions import Fraction as F
from itertools import combinations


class QS:
    """a + b sqrt(2) with rational a, b."""

    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a, self.b = F(a), F(b)

    def __add__(self, o):
        o = lift(o)
        return QS(self.a + o.a, self.b + o.b)

    __radd__ = __add__

    def __neg__(self):
        return QS(-self.a, -self.b)

    def __sub__(self, o):
        return self + (-lift(o))

    def __rsub__(self, o):
        return lift(o) - self

    def __mul__(self, o):
        o = lift(o)
        return QS(self.a * o.a + 2 * self.b * o.b, self.a * o.b + self.b * o.a)

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = lift(o)
        n = o.a * o.a - 2 * o.b * o.b  # nonzero for o != 0 since sqrt 2 is irrational
        if n == 0:
            raise ZeroDivisionError
        return self * QS(o.a / n, -o.b / n)

    def sign(self):
        a, b = self.a, self.b
        if a >= 0 and b >= 0:
            return 0 if a == 0 and b == 0 else 1
        if a <= 0 and b <= 0:
            return -1
        # opposite signs: compare a^2 with 2 b^2
        d = a * a - 2 * b * b
        return (1 if a > 0 else -1) if d > 0 else (-1 if a > 0 else 1)

    def __le__(self, o):
        return (self - o).sign() <= 0

    def __lt__(self, o):
        return (self - o).sign() < 0

    def __eq__(self, o):
        return (self - o).sign() == 0

    def __hash__(self):
        return hash((self.a, self.b))

    def __float__(self):
        return float(self.a) + float(self.b) * 2**0.5

    def __repr__(self):
        return f"{self.a} + {self.b}*sqrt2"


def lift(x):
    return x if isinstance(x, QS) else QS(x)


SQRT2 = QS(0, 1)

# ---------------------------------------------------------------- parsing

TOK = re.compile(r"\s*(Real\.sqrt|\d+|[()+\-*/:]|ℝ)")


def tokenize(s):
    out, i = [], 0
    while i < len(s):
        if s[i].isspace():
            i += 1
            continue
        m = TOK.match(s, i)
        if not m:
            raise ValueError(f"unexpected text at {s[i:i + 20]!r}")
        out.append(m.group(1))
        i = m.end()
    return out


class Parser:
    def __init__(self, toks):
        self.t, self.i = toks, 0

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else None

    def take(self, want=None):
        tok = self.peek()
        if want is not None and tok != want:
            raise ValueError(f"expected {want!r}, got {tok!r}")
        self.i += 1
        return tok

    def atom(self):
        """An argument of `sq`: a number or a parenthesised expression."""
        tok = self.peek()
        if tok == "(":
            self.take("(")
            v = self.expr()
            if self.peek() == ":":
                self.take(":")
                self.take("ℝ")
            self.take(")")
            return v
        if tok == "Real.sqrt":
            self.take()
            n = self.take()
            if n != "2":
                raise ValueError("only sqrt 2 is expected")
            return SQRT2
        if tok == "-":
            self.take()
            return -self.atom()
        if tok is not None and tok.isdigit():
            self.take()
            return QS(int(tok))
        raise ValueError(f"unexpected token {tok!r}")

    def term(self):
        v = self.atom()
        while self.peek() in ("*", "/"):
            op = self.take()
            w = self.atom()
            v = v * w if op == "*" else v / w
        return v

    def expr(self):
        v = self.term()
        while self.peek() in ("+", "-"):
            op = self.take()
            w = self.term()
            v = v + w if op == "+" else v - w
        return v


DEF = re.compile(r"^noncomputable def S(\d+) : Set \(ℝ × ℝ\) := sq (.*)$")


def read_squares(path):
    sq = {}
    for line in open(path, encoding="utf-8"):
        m = DEF.match(line.strip())
        if m:
            p = Parser(tokenize(m.group(2)))
            args = [p.atom() for _ in range(4)]
            if p.peek() is not None:
                raise ValueError(f"trailing tokens in S{m.group(1)}")
            sq[int(m.group(1))] = args
    if sorted(sq) != list(range(19)):
        raise ValueError(f"expected S0..S18, found {sorted(sq)}")
    return [sq[k] for k in range(19)]


def read_side(path):
    for line in open(path, encoding="utf-8"):
        if line.startswith("noncomputable def side19"):
            p = Parser(tokenize(line.split(":=", 1)[1]))
            return p.expr()
    raise ValueError("side19 not found")


# ---------------------------------------------------------------- geometry


def vertices(cx, cy, ux, uy):
    h = F(1, 2)
    out = []
    for s, t in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        out.append((cx + s * h * ux - t * h * uy, cy + s * h * uy + t * h * ux))
    return out


def separated(A, B):
    """Some edge normal of A or B weakly separates them; returns (axis, gap) or None."""
    best = None
    for ux, uy in ((A[2], A[3]), (-A[3], A[2]), (B[2], B[3]), (-B[3], B[2])):
        pa = [x * ux + y * uy for x, y in vertices(*A)]
        pb = [x * ux + y * uy for x, y in vertices(*B)]
        for gap in (min(pb) - max(pa), min(pa) - max(pb)):
            if gap.sign() >= 0 and (best is None or best[1] < gap):
                best = ((ux, uy), gap)
    return best


def read_witness(path):
    """The squares of a packing.squares Witness/v2 YAML, by a line scan."""
    text = open(path, encoding="utf-8").read()
    out = []
    for m in re.finditer(
        r"- id: (\d+)\n\s+center:\n\s+- '([^']+)'\n\s+- '([^']+)'\n\s+angle: '([^']+)'", text
    ):
        out.append((int(m.group(1)), F(m.group(2)), F(m.group(3)), F(m.group(4))))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("sq19")
    ap.add_argument("witness")
    ap.add_argument("--json")
    a = ap.parse_args()
    squares = read_squares(f"{a.sq19}/Sq19Lean/EndpointPacking.lean")
    side = read_side(f"{a.sq19}/Sq19Lean/Basic.lean")
    assert side == QS(3, F(4, 3)), side
    ok = True
    res = {"side19": repr(side), "side19_float": float(side), "squares": [], "pairs": {}}
    for k, (cx, cy, ux, uy) in enumerate(squares):
        unit = (ux * ux + uy * uy) == QS(1)
        vs = vertices(cx, cy, ux, uy)
        clear = min(min(x, y, side - x, side - y) for x, y in vs)
        inside = clear.sign() >= 0
        ok &= unit and inside
        ang = 0 if uy == QS(0) else 45
        res["squares"].append(
            {"k": k, "centre": [float(cx), float(cy)], "angle_deg": ang, "unit": unit,
             "containment_clearance": float(clear), "inside": inside}
        )
    touching = 0
    for i, j in combinations(range(19), 2):
        s = separated(squares[i], squares[j])
        if s is None:
            ok = False
            res["pairs"][f"{i}-{j}"] = "NOT SEPARATED"
        elif s[1].sign() == 0:
            touching += 1
    res["pairs_tested"] = 171
    res["pairs_touching_on_best_axis"] = touching
    # Compare with this project's known-best witness, in order.
    wit = read_witness(a.witness)
    diffs = []
    for k, (cx, cy, ux, uy) in enumerate(squares):
        wid, wx, wy, wang = wit[k]
        ang = 0 if uy == QS(0) else 45
        diffs.append(max(abs(float(cx) - float(wx)), abs(float(cy) - float(wy)), abs(ang - float(wang))))
    res["witness_squares"] = len(wit)
    res["witness_same_order_max_abs_diff"] = max(diffs)
    res["witness_ids_in_order"] = [w[0] for w in wit] == list(range(1, 20))
    res["all_checks_pass"] = ok
    print(f"side19 = {side} = {float(side):.15f}")
    print(f"19 squares: unit {all(s['unit'] for s in res['squares'])}, "
          f"inside [0, side19]^2 {all(s['inside'] for s in res['squares'])}, "
          f"min clearance {min(s['containment_clearance'] for s in res['squares']):.3g}")
    print(f"171 pairs weakly separated by an edge normal: {ok}; "
          f"{touching} pairs touch on their best axis")
    print(f"project witness: {len(wit)} squares, same order, max |diff| {max(diffs):.3g}")
    print("PASS" if ok else "FAIL")
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(res, f, indent=1)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
