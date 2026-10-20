"""The polynomials alone of #639's exact forms: for the counts the full check did not decide.

For each file: ``f`` squarefree and irreducible over Q with one real root in its
``t_interval``; ``p`` irreducible over Q (``factor_list``: one factor, multiplicity one,
full degree) and squarefree, with one real root in its side interval; and ``p(S) = 0`` in
Q[t]/f, with ``S`` the side's field element. It decides nothing about the configuration.
Run from ``packing/`` with the project interpreter, ``python -I``; prints JSON lines.
"""

import gzip
import json
import sys
from fractions import Fraction
from pathlib import Path

import sympy
from sympy import QQ, Poly, Symbol

T, X = Symbol("t"), Symbol("x")


def qq(value):
    q = Fraction(value)
    return QQ(q.numerator, q.denominator)


def main():
    for name in sys.argv[1:]:
        data = json.loads(gzip.decompress(Path(name).read_bytes()).decode("utf-8"))
        f = Poly.from_list([qq(c) for c in reversed(data["field"]["f"])], T, domain=QQ)
        ta, tb = (qq(c) for c in data["field"]["t_interval"])
        p = Poly([int(c) for c in reversed(data["S"]["poly"])], X, domain="ZZ")
        sa, sb = (qq(c) for c in data["S"]["interval"])
        side = Poly.from_list([qq(c) for c in reversed(data["S"]["in_K"])], T, domain=QQ).rem(f)
        acc = Poly(0, T, domain=QQ)
        for c in reversed(data["S"]["poly"]):
            acc = (acc * side + QQ(int(c))).rem(f)
        _content, factors = sympy.factor_list(p)
        print(json.dumps({
            "file": Path(name).name,
            "n": data["n"],
            "squares": len(data["squares"]),
            "f_degree": f.degree(),
            "f_irreducible": bool(f.is_irreducible),
            "f_squarefree": sympy.gcd(f, f.diff(T)).degree() == 0,
            "f_roots_in_t_interval": int(f.count_roots(ta, tb)),
            "p_degree": p.degree(),
            "p_factors": [[int(Poly(q, X).degree()), int(m)] for q, m in factors],
            "p_squarefree": sympy.gcd(p, p.diff(X)).degree() == 0,
            "p_roots_in_S_interval": int(p.count_roots(sa, sb)),
            "p_of_S_zero_in_K": acc.is_zero,
        }), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
