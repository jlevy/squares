"""Exact premises of the continuous-angle claims, decided again in exact rationals.

For each claim this review covers (T-145's c6715, T-157's c6718, the c6718 control at
B = 3348/3359 and T-192's n = 28) it decides, with Python's ``fractions`` and nothing
of the source's code:

- the counting margin ``n tau - M > 0`` and the claim ``X = L / B``;
- ``L^2 > 2 B^2`` (so ``E(t) = L/2 - (B/2) W(t) > 0`` at every angle, ``W <= sqrt 2``);
- ``T^2 + 2T - 1 > 0`` (``T > tan(pi/8)``) and ``T <= 1/2``; ``eps^2 + 2 eps - 1 < 0``
  (``eps < sqrt 2 - 1``, so ``W`` increases on ``[0, eps]``);
- the near-axis side ``A``: the default ``floor(10^9 B / W(eps)) / 10^9``, ``0 < A <= B``,
  and the margin ``B - A W(eps) >= 0`` that makes the side-``A`` axis square lie inside
  every side-``B`` square at ``t <= eps`` (lemma C6), and ``B W(t) >= A`` on ``[0, eps]``
  (the side-``B`` centre domain lies inside the axis sweep's ``[L/2, L - A/2]^2``);
- the default root ranges: 86 ranges whose ends increase strictly from ``eps`` to ``T``,
  and the binary64 enclosure of every end, computed here by exact comparison, so that the
  outward-rounded roots cover ``[eps, T]`` with overlaps;
- the ``run_key`` the source's v4 build would print, recomputed from the parameters by the
  rule ``slab.rs`` states (SHA-256 of the compact JSON of the eleven named fields, keys in
  byte order as ``serde_json``'s default map writes them), and compared with the key in
  the source's retained n = 28 summaries when ``--n28-summaries`` names their directory.

It reads no candidate (``candidates.py`` decides the densities) and prints one JSON
receipt. Exit status 0 when every premise holds and every compared key matches.

Usage::

    python -I premises.py [--n28-summaries DIR] > premises.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path

EPS = F(1, 10**7)
LAST_T = F(83, 200)
V4_SOURCE = "619b3c00bd918b329b4141c24ee30b027af7f88b86bcf2886e3c18855a61c7f5"

CLAIMS = {
    "c6715 (T-145)": {"n": 40, "L": F(67, 10), "B": F(199529, 200000), "tau": F(4999, 5000), "M": F(3999, 100)},
    "c6718 (T-157)": {"n": 40, "L": F(67, 10), "B": F(3350, 3359), "tau": F(4999, 5000), "M": F(3999, 100)},
    "c6718_B3348 (control)": {"n": 40, "L": F(67, 10), "B": F(3348, 3359), "tau": F(4999, 5000), "M": F(3999, 100)},
    "n28 (T-192)": {"n": 28, "L": F(573351, 100000), "B": F(499, 500), "tau": F(1), "M": F(2799999, 100000)},
}


def w_of(t: F) -> F:
    """W(t) = cos theta + sin theta at t = tan(theta / 2)."""
    return (1 + 2 * t - t * t) / (1 + t * t)


def default_axis_side(b: F, eps: F) -> F:
    g = 10**9
    return F(math.floor(b / w_of(eps) * g), g)


def default_cuts(eps: F, last: F) -> list[F]:
    cuts = [F(1, 100000), F(1, 10000), F(1, 1000), F(1, 200)]
    cuts += [F(k, 200) for k in range(2, 83)]
    return [c for c in cuts if eps < c < last]


def enclose(q: F) -> tuple[float, float]:
    """The tightest binary64 interval [lo, hi] holding q, by exact comparison."""
    x = float(q)
    if F(x) == q:
        return x, x
    if F(x) < q:
        return x, math.nextafter(x, math.inf)
    return math.nextafter(x, -math.inf), x


def run_key(input_sha256: str, p: dict, cuts: list[F], max_nodes: int, source: str) -> str:
    key = {
        "input_sha256": input_sha256,
        "n": p["n"],
        "L": str(p["L"]),
        "source_sha256": source,
        "core": str(p["B"]),
        "threshold": str(p["tau"]),
        "eps": str(EPS),
        "last_t": str(LAST_T),
        "axis_core": str(p["A"]),
        "cuts": [str(c) for c in cuts],
        "max_nodes": max_nodes,
    }
    text = json.dumps(key, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(text.encode()).hexdigest()


def decide(name: str, p: dict) -> dict:
    n, L, B, tau, M = p["n"], p["L"], p["B"], p["tau"], p["M"]
    a = default_axis_side(B, EPS)
    p["A"] = a
    w_eps = w_of(EPS)
    cuts = default_cuts(EPS, LAST_T)
    ends = [EPS, *cuts, LAST_T]
    roots = list(zip(ends, ends[1:]))
    enclosed = [(enclose(lo)[0], enclose(hi)[1]) for lo, hi in roots]
    cover = all(F(lo) <= r[0] and r[1] <= F(hi) for (lo, hi), r in zip(enclosed, roots))
    overlap = all(enclosed[k][1] >= enclosed[k + 1][0] for k in range(len(enclosed) - 1))
    checks = {
        "counting margin n tau - M > 0": n * tau - M > 0,
        "0 < M < n (admission)": 0 < M < n,
        "L^2 > 2 B^2": L * L > 2 * B * B,
        "0 < eps < T <= 1/2": 0 < EPS < LAST_T <= F(1, 2),
        "T^2 + 2T - 1 > 0": LAST_T**2 + 2 * LAST_T - 1 > 0,
        "eps^2 + 2 eps - 1 < 0": EPS**2 + 2 * EPS - 1 < 0,
        "0 < A <= B": 0 < a <= B,
        "A W(eps) <= B": a * w_eps <= B,
        "B W(0) >= A, so B W(t) >= A on [0, eps]": B * w_of(F(0)) >= a,
        "86 roots, ends strictly increasing": len(roots) == 86 and all(x < y for x, y in roots),
        "outward enclosures cover each root": cover,
        "neighbouring enclosed roots overlap": overlap,
    }
    return {
        "claim": name,
        "n": n,
        "L": str(L),
        "B": str(B),
        "tau": str(tau),
        "M": str(M),
        "X = L/B": str(L / B),
        "X decimal": f"{float(L / B):.12f}",
        "counting_margin": str(n * tau - M),
        "A (default)": str(a),
        "axis_containment_margin B - A W(eps)": str(B - a * w_eps),
        "axis_containment_margin decimal": f"{float(B - a * w_eps):.4e}",
        "L^2 - 2 B^2": str(L * L - 2 * B * B),
        "first roots": [[str(lo), str(hi)] for lo, hi in roots[:5]],
        "last root": [str(roots[-1][0]), str(roots[-1][1])],
        "first enclosed root": [repr(enclosed[0][0]), repr(enclosed[0][1])],
        "last enclosed root": [repr(enclosed[-1][0]), repr(enclosed[-1][1])],
        "checks": checks,
        "all_hold": all(checks.values()),
        "_cuts": cuts,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n28-summaries", type=Path, default=None)
    args = parser.parse_args()
    receipt: dict[str, object] = {"eps": str(EPS), "T": str(LAST_T), "claims": []}
    ok = True
    for name, p in CLAIMS.items():
        result = decide(name, dict(p))
        ok = ok and bool(result["all_hold"])
        cuts = result.pop("_cuts")
        if name.startswith("n28") and args.n28_summaries is not None:
            compared = []
            for file, mass in (("summary.json", p["M"]), ("control-summary.json", p["M"] * F(985, 1000))):
                summary = json.loads((args.n28_summaries / file).read_text())
                prem = summary["premises"]
                q = dict(p, M=mass, A=default_axis_side(p["B"], EPS))
                key = run_key(prem["input_sha256"], q, cuts, 200_000_000, V4_SOURCE)
                fields = {
                    "A": prem["A"] == str(q["A"]),
                    "X": prem["X"] == str(p["L"] / p["B"]),
                    "mass": prem["mass"] == str(mass),
                    "counting_margin": prem["counting_margin"] == str(p["n"] * p["tau"] - mass),
                    "axis_containment_margin": prem["axis_containment_margin"]
                    == str(p["B"] - q["A"] * w_of(EPS)),
                    "source_sha256": summary["build"]["source_sha256"] == V4_SOURCE,
                    "run_key": summary["run_key"] == key,
                    "roots": summary["roots"] == len(cuts) + 1,
                }
                ok = ok and all(fields.values())
                compared.append({"file": file, "recomputed_run_key": key, "equal": fields})
            result["source_summaries"] = compared
        receipt["claims"].append(result)
    receipt["all_hold"] = ok
    json.dump(receipt, sys.stdout, indent=2)
    print()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
