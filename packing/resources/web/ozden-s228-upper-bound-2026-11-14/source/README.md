# s(228) ≤ 15.600801734812

**This improves the published registry packing, but does NOT beat the cached Kaggle side-only leaderboard.** Our exact-rational side is 15.6008017348117538028514559173910014808630264…; the side-only entry is 15.596043116646 (square1000, 2026-10-29; cache 2026-11-09 20:52 UTC), smaller by 0.004758618166. The entry gives no packing and cannot be verified by us; the cache may be stale.

Credit: **Doğa Özden** ([@dogaozden](https://github.com/dogaozden), [live tracker](https://dogaozden.com/math/live/square-packing/)). Found, checked and posted by his AI research lab (Sol near1 director, gpt-6.1-sol). This is an upper bound only, not an optimality, rigidity, or KKT claim.

## Certificate

`n-228-candidate.yaml` is a packing.squares:Witness/v2, corners with rational scalars, with 228 exact unit squares. Its `side` is the exact rational; rounded **up** at 12 decimals it is 15.600801734812. The JSON is the same witness. SHA-256 of the YAML: `4dc2075f5fb06bb7a1ca68aabd8eebd0d326c16c5f408151876a165d2246b747`.

The prior verified registry record (jlevy/squares main @fa980f8e, packing/frontier/n-228.md) is 15.60460147572967429, found by Francisco Couzo and improved by PingYou Ltd, 2026-10-13. Exact Fraction arithmetic shows our side is smaller by 0.00379974091792 (relative 0.0002435). The best public Kaggle packing we know is 15.604601475744 (kirilltym; dataset fetched 2026-11-11 03:32 UTC), also larger by about 0.003799740932.

## Geometry and provenance

This is a freshly generated column-band design, **not a donor/transplant packing or public recovery**. Axis-parallel squares occupy two wall-anchored staircase/corner domains, and tilted squares form finite-width stacks across a diagonal band. The near1 director extended the column designer's corner domains, seam handling, and optional piecewise angle/phase proposals. Its finite-memory DP generates proposals; no assertion of globally maximal counts for general-angle junctions is made. Each selected pose must pass full emitted-count and far-overlap checks, then one quench with Evan Daniel's ALM+SLP fq optimizer (`evand/square-packing`, search/packer; MIT, source built from bb4cc78e). No random kicks or donor poses were used for this hit.

The filed hit is `hit-n228-114-0.txt`, kind design, from finite228 in batch nf141744: f=0.596543, delta=1 degree, tolerance=0.03, count=228, nt=48, column offset ox=0.026742, variant=1, corner layout `t:4,4`; final decimal side 15.60080173481195764, at search time 121 seconds. These are proposal parameters, not a claim that the final quenched squares retain that angle. The final pose has 50 squares tilted by more than 0.5 degrees. The independently harvested copy from verify228 in batch n31114181447 is byte-identical (SHA-256 `18dad468007e8fb8058104772dcfc5887c48bf0baa2789c5bcbee03f1cf2bfe5`). `hit-n228-114-0.json` records the design metadata.

Matched up to the square's eight symmetries, all 228 centres move by >0.001 vs the registry packing (93 by >0.05; largest move 0.940); 59 squares retilt by >1 degree; the old packing has 51 tilted squares. The comparison image is in records/. Credit this improvement to Doğa Özden, the former record to Francisco Couzo and PingYou Ltd, and the local optimizer to Evan Daniel. His MIT notice is preserved.

## Exact conversion and checks

1. The search pose was transcribed to decimal centre-angle form (binary64 round-trip strings). Independent `sqcheck.py` interval arithmetic certified it at its own side, with pair gap ≥2.02e-13 and wall gap ≥1.01e-13.
2. The registry's unmodified `packing-witness promote --strategy robust-rational` @fa980f8e constructed exact rational unit-square corners. `center_dilation` is **1**, no dilation; translating the least corner coordinates to zero and taking the greatest corner extent as side reduced the reported side by about 2.04e-13. This is a representation/normalization adjustment, not the 0.0038 geometric improvement.
3. Registry `packing-witness verify` passed **all 25,878 pairs**, method exact-algebraic over Q. Minimum best pair gap is exactly 101/500000000000000; minimum wall clearance is zero.
4. The separately implemented `sqcheck.py` says **VALID exact-rational**, certified side ≤15.600801734811754. Exact Fraction arithmetic compares the candidate with the registry's exact rational, not rounded float sides.

`verify-228.txt` and `sqcheck-228.txt` are unmodified outputs on the repository witness; checks/ retains JSON reports from promotion and verification. `n-228-decimal-pose.yaml` is the source named by the witness; `certificate.replay` names this repository's candidate. Promotion and the registry verifier share code, so they are not independent of each other. sqcheck is independent. No proof-assistant check or outside human review is claimed.

Rerun in a clone of jlevy/squares @fa980f8e:

```sh
cd squares/packing
uv run --frozen --no-dev --with sympy --with mpmath packing-witness verify /absolute/path/n-228-candidate.yaml
python3 /absolute/path/verifier/sqcheck.py /absolute/path/n-228-candidate.yaml
```

sqcheck needs mpmath, sympy and PyYAML. Witness/data/text: CC BY 4.0; code: MIT, as LICENSE.md. Search, checks and filing were AI-assisted throughout; the independent check code did not produce the packing.
