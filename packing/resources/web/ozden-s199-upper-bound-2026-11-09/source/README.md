# s(199) ≤ 14.614689853287: an improved packing of 199 unit squares (issue #935's packing plus an L of 27 grid squares)

Claimed by Doğa Özden ([@dogaozden](https://github.com/dogaozden), live tracker: https://dogaozden.com/math/live/square-packing/).

An exact-rational packing of 199 unit squares in a square of side

`S = 14.614689853286215…` (the exact rational is the witness's `side`; rounded up at 12 places it is 14.614689853287)

The registry's current n = 199 packing (Nate Chaoweeraprasit's, rational refinement by Siddharth Gupta; side 14.6175721735928069) is larger by **2.882e-03** (relative 1.97e-04). It is an upper bound only: no local-optimality, rigidity or global-optimality claim.

**What this is, plainly.** It is our exact n = 172 packing (jlevy/squares issue #935, side S₁₇₂ = 13.6146898532862153…, adopted by the registry as T-282) with an L of 27 axis-aligned unit grid squares added along two walls. The side is exactly S₁₇₂ + 1 in rational arithmetic. Nothing was searched or optimized at n = 199: the improvement is inherited from #935 through the construction s(n + 2⌊s⌋ + 1) ≤ s(n) + 1 (here ⌊S₁₇₂⌋ = 13, 172 + 27 = 199).

Prepared and posted by the AI agent of Doğa Özden (improved_by: Doğa Özden), who directed the work.

## The construction

Place the n = 172 packing, unchanged, in the lower-left square [0, S₁₇₂]² of the new square [0, S₁₇₂ + 1]². Add 14 unit squares `[a, a+1] × [S₁₇₂, S₁₇₂+1]`, a = 0…13, along the top wall (14 < S₁₇₂ + 1 fits), and 13 unit squares `[S₁₇₂, S₁₇₂+1] × [b, b+1]`, b = 0…12, along the right wall (13 < S₁₇₂ fits, so they stay below the top row). Every old square lies in [0, S₁₇₂]², so the L touches the old packing only along the lines x = S₁₇₂ and y = S₁₇₂. The drawing is `records/n-199-packing.png` (the 27 grid squares in orange).

## Files

| file | what |
|---|---|
| `n-199-candidate.yaml` | the packing as a `packing.squares:Witness/v2` file (corners, rational, 199 squares), in the registry's own format. Squares 1–172 are the exact n = 172 witness of #935 (the same rational corners); 173–186 are the top row, 187–199 the right column |
| `n199-witness.json` | the same file as JSON |
| `n-199-decimal-pose.yaml` | the decimal pose: the #935 search pose (decimal centre and angle per square, side 13.614689853286418) with the 27 grid squares at decimal centres; the witness's `source.path` |
| `packing-witness-verify.txt` | output of the registry's `packing-witness verify` (jlevy/squares `main` @ 200f2ebc), unmodified: `VERIFIED`, 19701 pairs |
| `sqcheck-output.txt` | output of `verifier/sqcheck.py`, our independent exact checker: `VALID`, exact rational (candidate), then the interval certificate of the decimal pose |
| `verifier/` | `sqcheck.py` and its README |
| `records/n-199-packing.png`, `.svg` | the packing; the L in orange |
| `LICENSE-evand-square-packing.txt` | Evan Daniel's MIT notice (evand/square-packing), for his base packing's certificate and his quench code, from which the n = 172 packing descends |

SHA-256: `n-199-candidate.yaml` `8a85b4c3536757a77fd51e2a0e361de1ecef36b38d59ed3111611672e6a78aca`; `n199-witness.json` `88d20ae206367d2029b05221d4a9975c86f8a71ffd51ac065aeebf168f4a6cb8`.

## Rerun

```
cp n-199-candidate.yaml <squares>/packing/witnesses/known-best/zz-cand.yaml
cd <squares>/packing && uv run --frozen --no-dev --with sympy --with mpmath packing-witness verify witnesses/known-best/zz-cand.yaml
python3 verifier/sqcheck.py n-199-candidate.yaml      # needs mpmath, sympy, pyyaml
python3 verifier/sqcheck.py n-199-decimal-pose.yaml
```

## About the margins

The 172 packing's pair gaps are about 2e-13 or more (the decimal pose's own, from Evan Daniel's quench repair scaling; see #935). The grid squares touch each other, the walls and the old packing's bounding square exactly, as in any grid packing, so the exact minimum pair gap of this witness is 0 (the registry's verify reports `minimum_best_pair_gap` 0). Non-overlap of interiors is what is verified, in exact rational arithmetic. For the decimal pose, `sqcheck` needs a dilation of 1e-24 to certify the touching squares in interval arithmetic; it says so in its output.

## Lineage, credit and AI assistance

The packing of squares 1–172 is the one filed in #935: it starts from the registry's n = 172 packing (Evan Daniel, T-257, #845, taken from the regularized known-best atlas of jlevy/squares), found by basin hopping over local minima computed by Evan Daniel's ALM+SLP quench code from [evand/square-packing](https://github.com/evand/square-packing) (`search/packer`, MIT, at bb4cc78e), built unmodified into our search. His MIT notice is kept in `LICENSE-evand-square-packing.txt`. Credit the improvement to Doğa Özden, the base packing to its holders as the record lists them, and the local optimizer to Evan Daniel. The L of 27 grid squares is the standard row-and-column extension.

The work was AI-assisted throughout (an AI agent wrote and ran the search and the checks); the checks above were run by code that did not produce the packing. Doğa directed the work.

The best public Kaggle per-puzzle side we found for 199 is 14.617572173606 (kirilltym, dataset kmmmvs/squares-in-squares-best-packings, refreshed 2026-11-09 20:30Z), above ours.
