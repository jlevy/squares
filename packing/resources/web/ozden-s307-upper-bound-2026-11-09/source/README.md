# s(307) ≤ 17.979230960388: an improved packing of 307 unit squares

Claimed by Doğa Özden ([@dogaozden](https://github.com/dogaozden), live tracker: https://dogaozden.com/math/live/square-packing/).

An exact-rational packing of 307 unit squares in a square of side

`S = 17.979230960387362…` (the exact rational is the witness's `side`; rounded up at 12 places it is 17.979230960388)

The registry's current n = 307 packing (Francisco Couzo's refinement of ntumlnoob's Kaggle notebook packing, T-256, issue #844, side 17.9792512836880252) is larger by **2.032e-05** (relative 1.13e-06). It is an upper bound only: no local-optimality, rigidity or global-optimality claim.

Prepared and posted by the AI agent of Doğa Özden (improved_by: Doğa Özden), who directed the work.

## Files

| file | what |
|---|---|
| `n-307-candidate.yaml` | the packing as a `packing.squares:Witness/v2` file (corners, rational, 307 squares), in the registry's own format |
| `n307-witness.json` | the same file as JSON |
| `packing-witness-verify.txt` | output of the registry's `packing-witness verify` (jlevy/squares `main` @ 19b354a5), unmodified: `VERIFIED`, 46971 pairs |
| `sqcheck-output.txt` | output of `verifier/sqcheck.py`, our independent exact checker: `VALID`, exact rational |
| `verifier/` | `sqcheck.py` and its README |
| `records/n-307-candidate-diff.png` | candidate vs the registry packing |

SHA-256: `n-307-candidate.yaml` `cb78adf88737718e4efe855bf5870879eef90ad30c386728d2ba64bb7f4e81e8`; `n307-witness.json` `612e97b1220ff5016e88c57d19293047da18d2e7775a8f99b0974cda1a6c706c`.

## Rerun

```
cp n-307-candidate.yaml <squares>/packing/witnesses/known-best/zz-cand.yaml
cd <squares>/packing && uv run --frozen --no-dev --with sympy --with mpmath packing-witness verify witnesses/known-best/zz-cand.yaml
python3 verifier/sqcheck.py n-307-candidate.yaml      # needs mpmath, sympy, pyyaml
```

## How the exact coordinates were made

The search produced a decimal pose (centre and angle per square). The registry's own `packing-witness promote --strategy robust-rational` (jlevy/squares @ 19b354a5) turned it into these exact rational corners: every pair is separated by at least about 2e-13 and squares touching the walls touch them exactly (containment clearance 0). `sqcheck.py` also certified the decimal pose itself in interval arithmetic before promotion.

## What differs from the registry packing

Squares matched by assignment up to the symmetries of the square: 45 of 307 centres move by more than 1e-3, 7 by more than 0.05 (largest 0.2); 6 squares are re-tilted by more than 1° (largest 25.23°); the packing has 112 tilted squares against 108.

## Lineage, credit and AI assistance

Started from the registry's current n = 307 packing (ntumlnoob (found_by) and Francisco Couzo (improved_by); T-256, #844), taken from the regularized known-best atlas of jlevy/squares. Found by basin hopping (kick, rotate, swap and reinsert moves) over local minima computed by Evan Daniel's ALM+SLP quench code from [evand/square-packing](https://github.com/evand/square-packing) (`search/packer`, MIT, at bb4cc78e), compiled into our search (its MIT licence kept with it). Credit the improvement to Doğa Özden, the base packing to its holders as the record lists them, and the local optimizer to Evan Daniel.

The search was AI-assisted throughout (an AI agent wrote and ran the search and the checks); the checks above were run by code that did not produce the packing. Doğa directed the work.

The best public Kaggle per-puzzle side we found for 307 is 17.979249693611 (mufasasimon), above ours.
