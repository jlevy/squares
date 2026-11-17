"""The L extension s(n + 2*floor(s) + 1) <= s(n) + 1 across every case record on main.

For each n with a recorded upper bound s(n) (verified, and separately reported), the
extension gives m = n + 2*floor(s(n)) + 1 squares in side s(n) + 1. This program compares
s(n) + 1 with the record at m, with the record's monotone closure at m, and then closes
the record under the extension and monotonicity, with and without #938's bound at 199.

Rational bounds compare exactly. Algebraic forms are evaluated by a small parser of their
own (numbers, + - * /, parentheses, sqrt, implicit products) at 60 digits; `root(...)`
forms by the midpoint of their stated isolating interval; anything else by its decimal
`value`. A comparison within 1e-25 that is not exact is reported as a close call.

Run: python -I -B l77_propagate.py FRONTIER_DIR CANDIDATE.yaml OUT.json
"""

from __future__ import annotations

import glob
import hashlib
import json
import os
import re
import sys
from fractions import Fraction as F

import mpmath
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import l77_checker as C  # noqa: E402

mpmath.mp.dps = 60
TOL = mpmath.mpf(10) ** -25

_TOK = re.compile(r"\s*(\d+(?:\.\d+)?|sqrt|[()+\-*/])")


def parse_expr(text: str) -> mpmath.mpf:
    toks = []
    pos = 0
    text = text.strip()
    while pos < len(text):
        m = _TOK.match(text, pos)
        if not m:
            raise ValueError(f"cannot parse {text!r} at {pos}")
        toks.append(m.group(1))
        pos = m.end()
    i = 0

    def peek() -> str | None:
        return toks[i] if i < len(toks) else None

    def take() -> str:
        nonlocal i
        t = toks[i]
        i += 1
        return t

    def expr() -> mpmath.mpf:
        v = term()
        while peek() in ("+", "-"):
            op = take()
            w = term()
            v = v + w if op == "+" else v - w
        return v

    def term() -> mpmath.mpf:
        v = unary()
        while True:
            t = peek()
            if t in ("*", "/"):
                take()
                w = unary()
                v = v * w if t == "*" else v / w
            elif t is not None and (t == "(" or t == "sqrt" or t[0].isdigit()):
                v = v * unary()
            else:
                return v

    def unary() -> mpmath.mpf:
        if peek() == "-":
            take()
            return -unary()
        return primary()

    def primary() -> mpmath.mpf:
        t = take()
        if t == "(":
            v = expr()
            assert take() == ")"
            return v
        if t == "sqrt":
            assert take() == "("
            v = expr()
            assert take() == ")"
            return mpmath.sqrt(v)
        if t[0].isdigit():
            return mpmath.mpf(t)
        raise ValueError(f"unexpected {t!r} in {text!r}")

    v = expr()
    if i != len(toks):
        raise ValueError(f"trailing tokens in {text!r}")
    return v


class Bound:
    """An upper bound: exact Fraction where the record is rational, else a 60-digit value."""

    def __init__(self, ub: dict):
        ef = ub.get("exact_form")
        val = ub.get("value")
        self.text = str(ef) if ef is not None else str(val)
        self.exact: F | None = None
        self.how = ""
        if ef is not None and re.fullmatch(r"-?\d+(/\d+)?", str(ef)):
            self.exact = F(*C.parse_scalar(str(ef)))
            self.v = mpmath.mpf(self.exact.numerator) / self.exact.denominator
            self.how = "rational"
        elif ef is not None and str(ef).startswith("root("):
            nums = re.findall(r"(\d+\.\d+)", str(ef))
            if len(nums) >= 2:
                self.v = (mpmath.mpf(nums[-2]) + mpmath.mpf(nums[-1])) / 2
                self.how = "root interval midpoint"
            else:
                self.v = mpmath.mpf(str(val))
                self.how = "decimal value"
        elif ef is not None:
            self.v = parse_expr(str(ef))
            self.how = "algebraic form"
        else:
            self.v = mpmath.mpf(str(val))
            self.how = "decimal value"
        if val is not None and self.how != "decimal value":
            # the printed value must agree with the evaluated form to its own digits
            digits = len(str(val).split(".")[1]) if "." in str(val) else 0
            assert abs(self.v - mpmath.mpf(str(val))) <= mpmath.mpf(10) ** (-digits + 1), (self.text, val)

    def floor(self) -> int:
        if self.exact is not None:
            return self.exact.numerator // self.exact.denominator
        f = int(mpmath.floor(self.v))
        assert TOL < self.v - f < 1 - TOL, f"floor too close to call: {self.text}"
        return f


def cmp(a_exact: F | None, a_v, b: Bound) -> tuple[str, float]:
    """Compare a candidate bound a with the record b: improves, equal or not."""
    if a_exact is not None and b.exact is not None:
        d = b.exact - a_exact
        return ("improves" if d > 0 else "equal" if d == 0 else "no"), float(d)
    d = b.v - a_v
    if abs(d) <= TOL:
        return "equal-to-60-digits", float(d)
    return ("improves" if d > 0 else "no"), float(d)


def main() -> int:
    frontier, cand, out = sys.argv[1:4]
    recs_v: dict[int, Bound] = {}
    recs_r: dict[int, Bound] = {}
    digests = hashlib.sha256()
    for path in sorted(glob.glob(os.path.join(frontier, "n-*.md"))):
        raw = open(path, "rb").read()
        digests.update(raw)
        d = yaml.safe_load(raw.decode().split("---", 2)[1])["packing"]
        n = int(d["n"])
        recs_v[n] = Bound(d["verified_upper_bound"])
        recs_r[n] = Bound(d["reported_upper_bound"])
    N = max(recs_v)
    w = C.read_witness(cand)
    S199 = F(*w["side"])

    def closure_min(recs: dict[int, Bound]) -> dict[int, tuple[F | None, mpmath.mpf]]:
        """Monotone closure U(n) = min over m >= n of rec(m)."""
        U: dict[int, tuple[F | None, mpmath.mpf]] = {}
        cur = None
        for n in range(N, 0, -1):
            b = recs[n]
            if cur is None or b.v < cur[1]:
                cur = (b.exact, b.v)
            U[n] = cur
        return U

    res: dict = {
        "program": "l77_propagate.py",
        "program_sha256": hashlib.sha256(open(__file__, "rb").read()).hexdigest(),
        "case_records": len(recs_v),
        "case_records_sha256_concatenated": digests.hexdigest(),
        "max_n": N,
        "forms": {k: sum(1 for b in recs_v.values() if b.how == k) for k in
                  ("rational", "algebraic form", "root interval midpoint", "decimal value")},
    }
    for label, recs in (("verified", recs_v), ("reported", recs_r)):
        U = closure_min(recs)
        rows = []
        for n in sorted(recs):
            b = recs[n]
            fl = b.floor()
            m = n + 2 * fl + 1
            t_exact = b.exact + 1 if b.exact is not None else None
            t_v = b.v + 1
            row = {"n": n, "s": float(b.v), "floor": fl, "m": m, "s_plus_1": float(t_v)}
            if m <= N:
                c1, d1 = cmp(t_exact, t_v, recs[m])
                row.update(record_m=float(recs[m].v), vs_record=c1, record_minus=d1)
                ue, uv = U[m]
                if ue is not None and t_exact is not None:
                    du = ue - t_exact
                    c2 = "improves" if du > 0 else "equal" if du == 0 else "no"
                    du = float(du)
                else:
                    du_m = uv - t_v
                    c2 = "equal-to-60-digits" if abs(du_m) <= TOL else ("improves" if du_m > 0 else "no")
                    du = float(du_m)
                row.update(closure_m=float(uv), vs_closure=c2, closure_minus=du)
            else:
                row.update(vs_record="beyond register")
            rows.append(row)
        res[label] = {
            "rows_in_range": sum(1 for r in rows if r["m"] <= N),
            "improves_record": [r for r in rows if r.get("vs_record") == "improves"],
            "improves_closure": [r for r in rows if r.get("vs_closure") == "improves"],
            "equal_record": [[r["n"], r["m"]] for r in rows if str(r.get("vs_record", "")).startswith("equal")],
            "closest_misses": sorted(
                [[r["n"], r["m"], r["record_minus"]] for r in rows if r.get("vs_record") == "no"],
                key=lambda x: -x[2])[:12],
            "rows": rows,
        }
    # close the verified record under the extension and monotonicity, without and with #938
    def close(extra: dict[int, F]) -> dict[int, mpmath.mpf]:
        b = {n: recs_v[n].v for n in recs_v}
        ex = {n: recs_v[n].exact for n in recs_v}
        for n, v in extra.items():
            b[n] = mpmath.mpf(v.numerator) / v.denominator
            ex[n] = v
        changed = True
        rounds = 0
        while changed:
            changed = False
            rounds += 1
            for n in range(1, N + 1):
                fl = ex[n].numerator // ex[n].denominator if ex[n] is not None else int(mpmath.floor(b[n]))
                m = n + 2 * fl + 1
                if m <= N and b[n] + 1 < b[m] - TOL:
                    b[m] = b[n] + 1
                    ex[m] = ex[n] + 1 if ex[n] is not None else None
                    changed = True
            for n in range(N - 1, 0, -1):
                if b[n + 1] < b[n] - TOL:
                    b[n] = b[n + 1]
                    ex[n] = ex[n + 1]
                    changed = True
        return {n: b[n] for n in b}, rounds

    base, r0 = close({})
    withnew, r1 = close({199: S199})
    res["closure_without_938"] = {
        "rounds": r0,
        "below_record": [[n, float(recs_v[n].v), float(base[n]), float(recs_v[n].v - base[n])]
                         for n in range(1, N + 1) if base[n] < recs_v[n].v - TOL],
    }
    res["closure_with_938"] = {
        "rounds": r1,
        "below_record": [[n, float(recs_v[n].v), float(withnew[n]), float(recs_v[n].v - withnew[n])]
                         for n in range(1, N + 1) if withnew[n] < recs_v[n].v - TOL],
    }
    s199 = mpmath.mpf(S199.numerator) / S199.denominator
    res["monotone_around_199"] = {
        "S199_new": float(s199),
        "record_198": [recs_v[198].text, float(recs_v[198].v)],
        "record_198_reported": [recs_r[198].text, float(recs_r[198].v)],
        "record_200": [recs_v[200].text, float(recs_v[200].v)],
        "record_200_reported": [recs_r[200].text, float(recs_r[200].v)],
        "n_below_199_with_record_above_new": [n for n in range(1, 199) if recs_v[n].v > s199],
        "n_above_199_with_record_below_new": [n for n in range(200, N + 1) if recs_v[n].v < s199],
        "n_above_199_with_reported_below_new": [n for n in range(200, N + 1) if recs_r[n].v < s199],
        "extension_from_199": {
            "m": 199 + 2 * 14 + 1,
            "bound": float(s199 + 1),
            "record_m": float(recs_v[199 + 29].v),
            "record_m_text": recs_v[228].text,
        },
        "record_172": [recs_v[172].text[:40] + "…", float(recs_v[172].v)],
    }
    with open(out, "w") as fh:
        json.dump(res, fh, indent=1)
        fh.write("\n")
    short = {k: v for k, v in res.items() if k not in ("verified", "reported")}
    for label in ("verified", "reported"):
        short[label] = {k: v for k, v in res[label].items() if k != "rows"}
    print(json.dumps(short, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
