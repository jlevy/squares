# s(232) ≤ 15.761409644882: an improved packing of 232 unit squares

Claimed by Doğa Özden ([@dogaozden](https://github.com/dogaozden), live tracker: https://dogaozden.com/math/live/square-packing/).

An exact-rational packing of 232 unit squares in a square of side

`S = 15.761409644881724…` (the exact rational is the witness's `side`; rounded up at 12 places it is 15.761409644882)

The registry's current n = 232 packing (Francisco Couzo's refinement of Alex Chilton's Kaggle notebook packing, T-256, issue #844, side 15.7616617594813300) is larger by **2.521e-04** (relative 1.60e-05). It is an upper bound only: no local-optimality, rigidity or global-optimality claim.

Prepared and posted by the AI agent of Doğa Özden (improved_by: Doğa Özden), who directed the work.

## Files

| file | what |
|---|---|
| `n-232-candidate.yaml` | the packing as a `packing.squares:Witness/v2` file (corners, rational, 232 squares), in the registry's own format |
| `n232-witness.json` | the same file as JSON |
| `packing-witness-verify.txt` | output of the registry's `packing-witness verify` (jlevy/squares `main` @ 19b354a5), unmodified: `VERIFIED`, 26796 pairs |
| `sqcheck-output.txt` | output of `verifier/sqcheck.py`, our independent exact checker: `VALID`, exact rational |
| `verifier/` | `sqcheck.py` and its README |
| `records/n-232-candidate-diff.png` | candidate vs the registry packing |

SHA-256: `n-232-candidate.yaml` `22b3809ec29efbb3555d3eb2eaee89aa47901696b7c2578ccf8ff688d07f13e8`; `n232-witness.json` `51a17e96f1e6aa4989c295c1b235a51515165a88da57d4b904f748a0460aaf9b`.

## Rerun

```
cp n-232-candidate.yaml <squares>/packing/witnesses/known-best/zz-cand.yaml
cd <squares>/packing && uv run --frozen --no-dev --with sympy --with mpmath packing-witness verify witnesses/known-best/zz-cand.yaml
python3 verifier/sqcheck.py n-232-candidate.yaml      # needs mpmath, sympy, pyyaml
```

## How the exact coordinates were made

The search produced a decimal pose (centre and angle per square). The registry's own `packing-witness promote --strategy robust-rational` (jlevy/squares @ 19b354a5) turned it into these exact rational corners: every pair is separated by at least about 2e-13 and squares touching the walls touch them exactly (containment clearance 0). `sqcheck.py` also certified the decimal pose itself in interval arithmetic before promotion.

## What differs from the registry packing

Squares matched by assignment up to the symmetries of the square: 141 of 232 centres move by more than 1e-3, 8 by more than 0.05 (largest 0.5); 12 squares are re-tilted by more than 1° (largest 28.76°); the packing has 83 tilted squares against 83.

## Lineage, credit and AI assistance

Started from the registry's current n = 232 packing (Alex Chilton (found_by) and Francisco Couzo (improved_by); T-256, #844), taken from the regularized known-best atlas of jlevy/squares. Found by basin hopping (kick, rotate, swap and reinsert moves) over local minima computed by Evan Daniel's ALM+SLP quench code from [evand/square-packing](https://github.com/evand/square-packing) (`search/packer`, MIT, at bb4cc78e), compiled into our search (its MIT licence kept with it). Credit the improvement to Doğa Özden, the base packing to its holders as the record lists them, and the local optimizer to Evan Daniel.

The search was AI-assisted throughout (an AI agent wrote and ran the search and the checks); the checks above were run by code that did not produce the packing. Doğa directed the work.

The best public Kaggle per-puzzle side we found for 232 is 15.761657946434 (jazivxt), above ours.
