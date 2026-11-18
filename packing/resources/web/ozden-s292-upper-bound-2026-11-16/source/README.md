# s(292) ≤ 17.590104218682

**This improves the published registry packing, but does NOT beat the cached Kaggle side-only leaderboard.** Our exact-rational side is 17.5901042186818346195918844579867374561574315…; the side-only entry is 17.589053943368 (Cats and boxes, 2026-10-29; cache 2026-11-09 20:52 UTC), smaller by 0.001050. The entry gives no packing and cannot be verified by us; the cache may be stale.

Credit: **Doğa Özden** ([@dogaozden](https://github.com/dogaozden), [live tracker](https://dogaozden.com/math/live/square-packing/)). Found, checked and posted by his AI research lab (Claude Sonnet 5.5 director `sonnear`, in a Sonnet-vs-Sol director experiment). This is an upper bound only, not an optimality, rigidity, or KKT claim.

## Certificate

`n-292-candidate.yaml` is a packing.squares:Witness/v2, corners with rational scalars, with 292 exact unit squares. Its `side` is the exact rational; rounded **up** at 12 decimals it is 17.590104218682. The JSON is the same witness. SHA-256 of the YAML: `90a0e30681821da567835ce1c9e81cf52aa899985587a953eafa0701b1829a8a`.

The prior verified registry record (jlevy/squares main @f9ddfeee, packing/frontier/n-292.md) is 17.5913781454976982, found by Nate Chaoweeraprasit (itsnaka), improved by Evan Daniel. Exact Fraction arithmetic shows our side is smaller by 0.00127392681586 (relative 7.242e-05). The best public Kaggle packing we know is 17.591378145514 (kirilltym; dataset fetched 2026-11-11 03:32 UTC), also larger, by about 0.001274.

## Geometry and provenance

Original AI-run design, **not a donor/transplant packing or public recovery**; no registry packing was used as a seed. Stage 1: a column-band designer (`cscan`/`coldp`: tilted squares stand in columns across a band along the diagonal at unit pitch, each column a stack of squares sliding on its own; axis-parallel squares on the two wall-anchored staircase lattices; an exact dynamic programme over the columns maximises the square count for a side fraction f and band angle 45°-delta) followed by one quench with Evan Daniel's ALM+SLP fq optimizer (`evand/square-packing`, search/packer; MIT). The director's own earlier designs (jobs s2h292b, s3h292a) seeded stage 2. Stage 2, a new operator written by the director (`segkick.py`): rigidly re-angle a contiguous segment of tilted squares, loosen, quench again with fq, and hill-climb a pool of such packings (mode `two`, 25,512 moves, 1,658 kept). The filed packing is hit `hit-n292-83-99956` of job s5k292t in batch s5 (rng 83), moves [(segment 10, +2.45°), (segment 9, +7.2°)], final decimal side 17.59010421868203977. The same batch's job s5k292a (single move: segment 15, +3.59°, rng 82) found 17.59010421868319085, 1.15e-12 higher; job s5k292e reached the same plateau. All 114 hit files from batch s5 below the record (114 distinct byte-for-byte poses, 28 of them below 17.5901043) are the same rigid basin, differing by about 1e-9 or less in the best cases. `hit-n292-83-99956.json` has the move metadata.

Matched up to the square's eight symmetries, 203 of 292 centres move by >0.001 vs the registry packing (115 by >0.05; largest move 0.996); 77 squares retilt by >1 degree; ours has 64 tilted squares, the old packing 49. The comparison image is in records/. Credit this improvement to Doğa Özden, the former record to its holders as the registry lists them, and the local optimizer to Evan Daniel. His MIT notice is preserved.

## Exact conversion and checks

1. The search pose was transcribed to decimal centre-angle form (binary64 round-trip strings). Independent `sqcheck.py` interval arithmetic certified it at its own side, with pair gap ≥2.02e-13 and wall gap ≥1.02e-13.
2. The registry's unmodified `packing-witness promote --strategy robust-rational` @f9ddfeee constructed exact rational unit-square corners. `center_dilation` is **1**, no dilation; translating the least corner coordinates to zero and taking the greatest corner extent as side reduced the reported side by about 2.0e-13. This is a representation/normalization adjustment, not the 0.00127 geometric improvement.
3. Registry `packing-witness verify` passed **all 42,486 pairs**, method exact-algebraic over Q; minimum wall clearance is zero.
4. The separately implemented `sqcheck.py` says **VALID exact-rational**, certified side ≤17.590104218681835. Exact Fraction arithmetic compares the candidate with the registry's exact rational, not rounded float sides.

`verify-292.txt` and `sqcheck-292.txt` are unmodified outputs on the repository witness; checks/ retains JSON reports from promotion and verification. `n-292-decimal-pose.yaml` is the source named by the witness; `certificate.replay` names this repository's candidate. Promotion and the registry verifier share code, so they are not independent of each other. sqcheck is independent. No proof-assistant check or outside human review is claimed.

Rerun in a clone of jlevy/squares @f9ddfeee:

```sh
cd squares/packing
uv run --frozen --no-dev --with sympy --with mpmath packing-witness verify /absolute/path/n-292-candidate.yaml
python3 /absolute/path/verifier/sqcheck.py /absolute/path/n-292-candidate.yaml
```

sqcheck needs mpmath, sympy and PyYAML. Witness/data/text: CC BY 4.0; code: MIT, as LICENSE.md. Search, checks and filing were AI-assisted throughout; the independent check code did not produce the packing.
