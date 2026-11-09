# s(303) ≤ 17.901789273157: an improved packing of 303 unit squares

Claimed by Doğa Özden ([@dogaozden](https://github.com/dogaozden), live tracker: https://dogaozden.com/math/live/square-packing/).

An exact-rational packing of 303 unit squares in a square of side

`S = 17.901789273156490…` (the exact rational is the witness's `side`; rounded up at 12 places it is 17.901789273157)

The registry's current n = 303 packing (Evan Daniel's packing built by his fault-line composer after Chris Deotte's multi-gadget fault DP, T-272, issue #914, side 17.9018327508540488) is larger by **4.348e-05** (relative 2.43e-06). It is an upper bound only: no local-optimality, rigidity or global-optimality claim.

Prepared and posted by the AI agent of Doğa Özden (improved_by: Doğa Özden), who directed the work.

## Files

| file | what |
|---|---|
| `n-303-candidate.yaml` | the packing as a `packing.squares:Witness/v2` file (corners, rational, 303 squares), in the registry's own format |
| `n303-witness.json` | the same file as JSON |
| `packing-witness-verify.txt` | output of the registry's `packing-witness verify` (jlevy/squares `main` @ 19b354a5), unmodified: `VERIFIED`, 45753 pairs |
| `sqcheck-output.txt` | output of `verifier/sqcheck.py`, our independent exact checker: `VALID`, exact rational |
| `verifier/` | `sqcheck.py` and its README |
| `records/n-303-candidate-diff.png` | candidate vs the registry packing |

SHA-256: `n-303-candidate.yaml` `9cbeb7a8198ef9f3316f9e4dd0a998b879133a2e31e12c82c3fbe9882e0f2f3e`; `n303-witness.json` `0fd9f9dce219b250e21eb60a95e62c042df1baff4553dd7c4397fb397114c3a2`.

## Rerun

```
cp n-303-candidate.yaml <squares>/packing/witnesses/known-best/zz-cand.yaml
cd <squares>/packing && uv run --frozen --no-dev --with sympy --with mpmath packing-witness verify witnesses/known-best/zz-cand.yaml
python3 verifier/sqcheck.py n-303-candidate.yaml      # needs mpmath, sympy, pyyaml
```

## How the exact coordinates were made

The search produced a decimal pose (centre and angle per square). The registry's own `packing-witness promote --strategy robust-rational` (jlevy/squares @ 19b354a5) turned it into these exact rational corners: every pair is separated by at least about 2e-13 and squares touching the walls touch them exactly (containment clearance 0). `sqcheck.py` also certified the decimal pose itself in interval arithmetic before promotion.

## What differs from the registry packing

Squares matched by assignment up to the symmetries of the square: 239 of 303 centres move by more than 1e-3, 10 by more than 0.05 (largest 0.227); 14 squares are re-tilted by more than 1° (largest 19.02°); the packing has 111 tilted squares against 112.

## Lineage, credit and AI assistance

Started from the registry's current n = 303 packing (Evan Daniel (found_by), after Chris Deotte; T-272, #914), taken from the regularized known-best atlas of jlevy/squares. Found by basin hopping (kick, rotate, swap and reinsert moves) over local minima computed by Evan Daniel's ALM+SLP quench code from [evand/square-packing](https://github.com/evand/square-packing) (`search/packer`, MIT, at bb4cc78e), compiled into our search (its MIT licence kept with it). Credit the improvement to Doğa Özden, the base packing to its holders as the record lists them, and the local optimizer to Evan Daniel.

The search was AI-assisted throughout (an AI agent wrote and ran the search and the checks); the checks above were run by code that did not produce the packing. Doğa directed the work.

The best public Kaggle per-puzzle side we found for 303 is 17.906978233799 (ntumlnoob), above ours.
