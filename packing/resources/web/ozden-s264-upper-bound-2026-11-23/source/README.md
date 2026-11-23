# s(264) ≤ 16.772168305041

**This improves the registry packing, but does NOT beat the cached Kaggle side-only leaderboard.** Our exact-rational side is 16.772168305040546396263…; the side-only entry is 16.770288527750 (Cats and boxes, 2026-10-28 00:02 UTC; leaderboard cache 2026-11-09 20:52 UTC), smaller by 0.001880. That entry gives no packing and we cannot verify it; the cache may be stale. Our side is smaller than the best public Kaggle packing we know (16.774735132404, kirilltym) and smaller than GeiserX's published 16.772843152678 (the layout whose exact certificate is jlevy/squares #1037) by 6.75e-4.

Credit: **Doğa Özden** ([@dogaozden](https://github.com/dogaozden), [live tracker](https://dogaozden.com/math/live/square-packing/)). Found, checked and posted by his AI research lab (Claude agents, directed by him). This is an upper bound only, not an optimality, rigidity, or KKT claim.

## Certificate

`n-264-candidate.yaml` is a packing.squares:Witness/v2, corners with rational scalars, with 264 exact unit squares. Its `side` is the exact rational; rounded **up** at 12 decimals it is 16.772168305041. The JSON is the same witness. SHA-256 of the YAML: `e79b705387160903c31dd287575407c6ef8b2b6e89b6374bcd0a2d71b2939e25`.

The prior verified registry record (jlevy/squares main @b8bea996e, packing/frontier/n-264.md) is 16.7738075980019989: the packing was found by Tomáš Kodaj and its upper bound lowered by JoeGun (issue #1001). Exact Fraction arithmetic shows our side is smaller by 0.00163929296145 (relative 9.773e-05).

## Geometry and provenance

**This is a perturbation of the registry packing, not an independent design.** The seed was the registry's own n = 264 packing (witnesses/known-best/n-264.yaml). Stage 1: every square's centre and angle was kicked by Gaussian noise (sigma 0.08 on x, y and angle). Stage 2: `jam`, a new overlap-energy annealer written by our lab (Rust; energy = sum of squared pair penetration depths and wall excess at a fixed box side just below the record, single-square Metropolis moves of x, y and angle with an adaptive step, geometric temperature schedule, greedy tail), relaxed the kicked state to zero overlap at a box side slightly under the record's. Stage 3: one quench with Evan Daniel's ALM+SLP fq optimizer (`evand/square-packing`, search/packer; MIT), then three small kick-and-requench polishes. The filed packing is the best of 232 such trials on this count (job j42, tag r264-k0.08); two other trials found nearby lower sides (16.772211708 at sigma 0.12, 16.773178042 at sigma 0.12), and most trials return to the registry basin at its own side.

Matched up to the square's eight symmetries, 251 of 264 centres move by >0.001 vs the registry packing (21 by >0.05; largest move 0.553); 60 squares retilt by >1 degree (largest 28.49°); ours has 74 tilted squares, the registry packing 72. The comparison image is in records/. Credit this improvement to Doğa Özden, the former record to its holders as the registry lists them, and the local optimizer to Evan Daniel. His MIT notice is preserved.

## Exact conversion and checks

1. The search pose was transcribed to decimal centre-angle form (binary64 round-trip strings). Independent `sqcheck.py` interval arithmetic certified it at its own side, with pair gap ≥2.88e-13 and wall gap ≥1.72e-13.
2. The registry's unmodified `packing-witness promote --strategy robust-rational` @b8bea996e constructed exact rational unit-square corners. `center_dilation` is **1**, no dilation; translating the least corner coordinates to zero and taking the greatest corner extent as side reduced the reported side by about 3.5e-13. This is a representation/normalization adjustment, not the 0.00164 geometric improvement.
3. Registry `packing-witness verify` passed **all 34,716 pairs**, method exact-algebraic over Q; minimum wall clearance is zero.
4. The separately implemented `sqcheck.py` says **VALID exact-rational**, certified side ≤16.772168305040547. Exact Fraction arithmetic compares the candidate with the registry's exact rational, not rounded float sides.

`verify-264.txt` and `sqcheck-264.txt` are unmodified outputs on the repository witness; checks/ retains JSON reports from promotion and verification. `n-264-decimal-pose.yaml` is the source named by the witness; `certificate.replay` names this repository's candidate. `hit-n264-r264-k0.08-16.772168305041.txt` is the search output. Promotion and the registry verifier share code, so they are not independent of each other. sqcheck is independent. No proof-assistant check or outside human review is claimed.

Rerun in a clone of jlevy/squares @b8bea996e:

```sh
cd squares/packing
uv run --frozen --no-dev --with sympy --with mpmath packing-witness verify /absolute/path/n-264-candidate.yaml
python3 /absolute/path/verifier/sqcheck.py /absolute/path/n-264-candidate.yaml
```

sqcheck needs mpmath, sympy and PyYAML. Witness/data/text: CC BY 4.0; code: MIT, as LICENSE.md. Search, checks and filing were AI-assisted throughout; the independent check code did not produce the packing.
