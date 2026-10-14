"""Compare Kleddamag's n = 17 candidate statement with this repository's exact n17 record.

Run from anywhere with the project interpreter (Python 3.14), isolated:

    packing/.venv/bin/python3 -I compare_statement.py REPO_ROOT EDITION_ROOT OUT.json

REPO_ROOT is a checkout of jlevy/squares; EDITION_ROOT the clone of
Kleddamag/the-seventeenth-square-candidate at 653b9589d. The edition is read as data only:
STATEMENT.md is parsed by a small polynomial parser written here (no eval), and the
edition's upper-packing-certificate.json is only hashed. Nothing in the edition is
imported or executed.

What it decides, all in exact rational arithmetic:

1. STATEMENT.md has the SHA-256 the edition's manifest gives it.
2. Its F and G equal, coefficient for coefficient, the two chart polynomials this
   repository derived independently (`devtools.check_n17_root_certificate.n17_polynomials`)
   and froze in the exp-237 root certificate.
3. Its (t0, b0) and radius 10^-12 equal the exp-237 box midpoint and radius exactly, so its
   isolating rectangle is our certified box; exp-237's contraction proves a unique root
   there, so (t*, b*) is our H-255 root.
4. Its side map (6 + 4t)/(1 + 2t - t^2) is ours (`check_n17_catalogue_polynomial`), and our
   tight inclusion of t* gives an outward enclosure of L strictly inside the statement's
   20-place enclosure and inside the exp-245 width-1e-40 enclosure of S*.
5. L is strictly below n-017's verified upper bound (the exact_form ceiling), within 1e-16
   of it (in fact within about 1.04e-22), and agrees with the catalogue's printed decimal.
6. The edition's upper-packing-certificate.json is byte-identical to the rational seed this
   repository retained on 2026-09-21 and built the certified endpoint from.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from fractions import Fraction as Q
from pathlib import Path

Poly = dict[tuple[int, int], int]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# --- a small exact parser for the statement's polynomials (no eval) ---------------------

TOKEN = re.compile(r"\s*(?:(\d+)|([tb])|(\^)|([()+\-]))")


def tokens(text: str) -> list[str]:
    out: list[str] = []
    pos = 0
    text = text.replace("{", "").replace("}", "")
    while pos < len(text):
        m = TOKEN.match(text, pos)
        if not m or m.end() == pos:
            raise ValueError(f"unexpected text at {pos}: {text[pos:pos + 20]!r}")
        out.append(next(g for g in m.groups() if g is not None))
        pos = m.end()
    return out


def p_add(a: Poly, b: Poly, sign: int = 1) -> Poly:
    r = dict(a)
    for k, v in b.items():
        r[k] = r.get(k, 0) + sign * v
    return {k: v for k, v in r.items() if v}


def p_mul(a: Poly, b: Poly) -> Poly:
    r: Poly = {}
    for (i, j), x in a.items():
        for (k, l), y in b.items():
            r[i + k, j + l] = r.get((i + k, j + l), 0) + x * y
    return {k: v for k, v in r.items() if v}


def p_pow(a: Poly, n: int) -> Poly:
    r: Poly = {(0, 0): 1}
    for _ in range(n):
        r = p_mul(r, a)
    return r


class Parser:
    def __init__(self, text: str) -> None:
        self.t = tokens(text)
        self.i = 0

    def peek(self) -> str | None:
        return self.t[self.i] if self.i < len(self.t) else None

    def take(self) -> str:
        tok = self.t[self.i]
        self.i += 1
        return tok

    def expr(self) -> Poly:
        sign = 1
        if self.peek() in ("+", "-"):
            sign = -1 if self.take() == "-" else 1
        acc = p_mul({(0, 0): sign}, self.term())
        while self.peek() in ("+", "-"):
            s = -1 if self.take() == "-" else 1
            acc = p_add(acc, self.term(), s)
        return acc

    def term(self) -> Poly:
        acc = self.factor()
        while self.peek() is not None and self.peek() not in ("+", "-", ")"):
            acc = p_mul(acc, self.factor())
        return acc

    def factor(self) -> Poly:
        tok = self.take()
        if tok.isdigit():
            base: Poly = {(0, 0): int(tok)}
        elif tok == "t":
            base = {(1, 0): 1}
        elif tok == "b":
            base = {(0, 1): 1}
        elif tok == "(":
            base = self.expr()
            if self.take() != ")":
                raise ValueError("unbalanced parenthesis")
        else:
            raise ValueError(f"unexpected token {tok!r}")
        if self.peek() == "^":
            self.take()
            base = p_pow(base, int(self.take()))
        return base

    def parse(self) -> Poly:
        value = self.expr()
        if self.peek() is not None:
            raise ValueError(f"trailing tokens from {self.i}")
        return value


def statement_facts(text: str) -> dict[str, object]:
    def grab(pattern: str) -> str:
        m = re.search(pattern, text)
        if not m:
            raise ValueError(f"statement lacks {pattern}")
        return m.group(1)

    t0 = Q(int(grab(r"t_0=(\d+)/10\^\{60\}")), 10**60)
    b0 = Q(int(grab(r"b_0=(\d+)/10\^\{60\}")), 10**60)
    f = Parser(grab(r"F\(t,b\)=([^$]+)\$")).parse()
    g = Parser(grab(r"G\(t,b\)=([^$]+)\$")).parse()
    rect = grab(r"rectangle \$\[t_0-10\^\{-(\d+)\},t_0\+10")
    if rect != grab(r"\[b_0-10\^\{-(\d+)\},b_0\+10"):
        raise ValueError("the two rectangle radii differ")
    if "L=(6+4t_*)/(1+2t_*-t_*^2)" not in text:
        raise ValueError("the side map is not the one expected")
    m = re.search(r"\$(\d+\.\d+)<L<(\d+\.\d+)\$", text)
    if not m:
        raise ValueError("statement lacks the L enclosure")
    return {
        "t0": t0,
        "b0": b0,
        "F": f,
        "G": g,
        "radius": Q(1, 10 ** int(rect)),
        "L_lower": Q(m.group(1)),
        "L_upper": Q(m.group(2)),
        "L_lower_text": m.group(1),
        "L_upper_text": m.group(2),
    }


def side(t: Q) -> Q:
    return (6 + 4 * t) / (1 + 2 * t - t * t)


def terms(p: Poly) -> list[list[object]]:
    return [[i, j, str(c)] for (i, j), c in sorted(p.items())]


def as_poly(rows: list[list[object]]) -> Poly:
    return {(int(r[0]), int(r[1])): int(str(r[2])) for r in rows}


def decimal(q: Q, digits: int) -> str:
    """q to `digits` places, truncated toward zero, for display only."""
    scaled = q.numerator * 10**digits // q.denominator
    s = str(scaled).rjust(digits + 1, "0")
    return f"{s[:-digits]}.{s[-digits:]}"


def main() -> int:
    repo, edition, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    sys.path.insert(0, str(repo / "packing"))
    from devtools.check_n17_catalogue_polynomial import side_interval  # noqa: PLC0415
    from devtools.check_n17_root_certificate import (  # noqa: PLC0415
        SOURCE_PATH,
        SOURCE_SHA256,
        n17_polynomials,
    )
    from sqpack.yamlio import load_yaml  # noqa: PLC0415

    results = repo / "packing/campaign/series/series-000-smoke-and-calibration/results"
    cert_path = results / "exp-237-n17-polynomial-root/run-001/certificate.json"
    checker_path = results / "exp-237-n17-polynomial-root/run-001/checker.json"
    s245_path = results / "exp-245-n17-catalogue-polynomial/run-001/receipt.json"
    case_path = repo / "packing/frontier/n-017.md"

    statement_path = edition / "STATEMENT.md"
    manifest = dict(
        reversed(line.split("  ", 1))
        for line in (edition / "MANIFEST.sha256").read_text(encoding="utf-8").splitlines()
    )
    st_sha = sha256(statement_path)
    facts = statement_facts(statement_path.read_text(encoding="utf-8"))
    checks: dict[str, bool] = {}
    checks["statement_sha256_matches_manifest"] = st_sha == manifest["STATEMENT.md"]

    # 2. polynomials
    ours_formula = n17_polynomials()
    cert = json.loads(cert_path.read_text(encoding="utf-8"))
    ours_cert = tuple(as_poly(p) for p in cert["polynomials"])
    checks["F_equals_our_first_chart_polynomial"] = facts["F"] == ours_formula[0] == ours_cert[0]
    checks["G_equals_our_second_chart_polynomial"] = facts["G"] == ours_formula[1] == ours_cert[1]

    # 3. the isolating rectangle is our certified box
    mid = tuple(Q(x) for x in cert["box"]["midpoint"])
    radius = Q(cert["box"]["radius"])
    checks["t0_b0_equal_exp237_box_midpoint"] = (facts["t0"], facts["b0"]) == mid
    checks["rectangle_radius_equals_exp237_radius"] = facts["radius"] == radius
    checker = json.loads(checker_path.read_text(encoding="utf-8"))
    checks["exp237_certificate_and_checker_passed"] = (
        bool(cert["criterion_passed"]) and not cert["failures"] and checker["verification_passed"] is True
    )
    incl = [Q(x) for x in cert["inclusion_bounds"]]
    checks["exp237_inclusion_strictly_inside_box"] = all(x < radius for x in incl)
    q_norm = Q(cert["q"])
    checks["exp237_contraction_norm_below_one"] = q_norm < 1

    # 4. L: our tight t* inclusion mapped through the same side formula
    t_lo, t_hi = mid[0] - incl[0], mid[0] + incl[0]
    k_lo = min(1 + 2 * t - t * t for t in (t_lo, t_hi))
    checks["side_denominator_positive_on_tight_t_range"] = k_lo > 0
    s_lo, s_hi = side(t_hi), side(t_lo)  # S is decreasing on the range (checked by side_interval)
    side_interval(t_lo, t_hi, digits=60)  # raises unless K > 0 and S' < 0 at both ends
    checks["L_enclosure_strictly_inside_statement_enclosure"] = (
        facts["L_lower"] < s_lo and s_hi < facts["L_upper"]
    )
    s245 = json.loads(s245_path.read_text(encoding="utf-8"))
    e_lo, e_hi = (Q(x) for x in s245["root_enclosure"])
    checks["exp245_S_star_enclosure_inside_tight_L_enclosure"] = s_lo <= e_lo and e_hi <= s_hi
    checks["exp245_S_star_enclosure_inside_statement_enclosure"] = (
        facts["L_lower"] < e_lo and e_hi < facts["L_upper"]
    )
    checks["exp245_verdict_identical_and_irreducible"] = (
        s245["verdict"] == "identical up to a rational unit and irreducible over Q"
        and bool(s245["criterion_passed"])
    )

    # 5. against the case record
    text = case_path.read_text(encoding="utf-8")
    front = text.split("---", 2)[1]
    case = load_yaml(front)["packing"]
    vub = case["verified_upper_bound"]
    ceiling = Q(vub["exact_form"])
    checks["verified_upper_value_is_exact_form"] = Q(vub["value"]) == ceiling
    lo_l = max(e_lo, s_lo)
    hi_l = min(e_hi, s_hi)
    checks["L_strictly_below_verified_ceiling"] = hi_l < ceiling
    checks["ceiling_minus_L_below_1e-16"] = ceiling - lo_l < Q(1, 10**16)
    reported = Q(case["reported_upper_bound"]["value"])
    checks["catalogue_decimal_within_1e-15_of_L"] = max(abs(reported - lo_l), abs(reported - hi_l)) < Q(
        1, 10**15
    )
    rlb = Q(case["reported_lower_bound"]["exact_form"])
    vlb = Q(case["verified_lower_bound"]["exact_form"])
    checks["L_above_record_lower_bounds"] = rlb < lo_l and vlb < lo_l

    # 6. the rational seed
    seed_ours = repo / SOURCE_PATH
    seed_theirs = edition / "upper-packing-certificate.json"
    checks["edition_seed_identical_to_retained_seed"] = (
        sha256(seed_theirs) == sha256(seed_ours) == SOURCE_SHA256
    )

    receipt = {
        "schema": "k17-statement-comparison/v1",
        "inputs": {
            "edition_statement": {"path": "STATEMENT.md", "sha256": st_sha},
            "edition_seed": {
                "path": "upper-packing-certificate.json",
                "sha256": sha256(seed_theirs),
            },
            "exp237_certificate": {
                "path": str(cert_path.relative_to(repo)),
                "sha256": sha256(cert_path),
            },
            "exp237_checker": {
                "path": str(checker_path.relative_to(repo)),
                "sha256": sha256(checker_path),
            },
            "exp245_receipt": {"path": str(s245_path.relative_to(repo)), "sha256": sha256(s245_path)},
            "case_record": {"path": str(case_path.relative_to(repo)), "sha256": sha256(case_path)},
            "retained_seed": {"path": SOURCE_PATH, "sha256": sha256(seed_ours)},
            "comparison_program_sha256": sha256(Path(__file__)),
        },
        "statement": {
            "t0": str(facts["t0"]),
            "b0": str(facts["b0"]),
            "radius": str(facts["radius"]),
            "F": terms(facts["F"]),
            "G": terms(facts["G"]),
            "side_map": "L = (6 + 4t*)/(1 + 2t* - t*^2)",
            "L_enclosure": [facts["L_lower_text"], facts["L_upper_text"]],
        },
        "ours": {
            "exp237_contraction_norm_q_below": decimal(q_norm, 12),
            "exp237_inclusion_bounds_below": [f"{float(x):.6e}" for x in incl],
            "tight_t_range_decimal": [decimal(t_lo, 40), decimal(t_hi, 40)],
            "L_outward_from_tight_t_range": [decimal(s_lo, 40), decimal(s_hi, 40)],
            "L_width_from_tight_t_range": f"{float(s_hi - s_lo):.3e}",
            "exp245_S_star_enclosure": [decimal(e_lo, 45), decimal(e_hi, 45)],
            "exp245_S_star_enclosure_width": f"{float(e_hi - e_lo):.3e}",
            "exp237_checker_verification_passed": checker["verification_passed"],
        },
        "record": {
            "verified_upper_bound_value": vub["value"],
            "verified_upper_bound_exact_form": vub["exact_form"],
            "verified_upper_bound_evidence": vub["evidence"],
            "ceiling_minus_L_upper": f"{float(ceiling - hi_l):.6e}",
            "ceiling_minus_L_lower": f"{float(ceiling - lo_l):.6e}",
            "reported_upper_bound_value": case["reported_upper_bound"]["value"],
            "catalogue_decimal_minus_L": f"{float(reported - lo_l):.6e}",
            "reported_lower_bound": case["reported_lower_bound"]["exact_form"],
            "verified_lower_bound": case["verified_lower_bound"]["exact_form"],
            "gap_L_minus_verified_lower": f"{float(lo_l - vlb):.12f}",
        },
        "checks": checks,
        "verdict": "AGREES" if all(checks.values()) else "DIFFERS",
    }
    out.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verdict": receipt["verdict"], "failed": [k for k, v in checks.items() if not v]}))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
