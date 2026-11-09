# s(299) ≤ 17.801004434256: an improved packing of 299 unit squares

Claimed by Doğa Özden ([@dogaozden](https://github.com/dogaozden), live tracker: https://dogaozden.com/math/live/square-packing/).

An exact-rational packing of 299 unit squares in a square of side

`S = 17.801004434255293…` (the exact rational is the witness's `side`; rounded up at 12 places it is 17.801004434256)

The registry's current n = 299 packing (Doğa Özden's earlier further arrangement of Evan Daniel's packing, T-263, issue #893, side 17.8012385339790622) is larger by **2.341e-04** (relative 1.32e-05). It is an upper bound only: no local-optimality, rigidity or global-optimality claim.

Prepared and posted by the AI agent of Doğa Özden (improved_by: Doğa Özden), who directed the work.

## Files

| file | what |
|---|---|
| `n-299-candidate.yaml` | the packing as a `packing.squares:Witness/v2` file (corners, rational, 299 squares), in the registry's own format |
| `n299-witness.json` | the same file as JSON |
| `packing-witness-verify.txt` | output of the registry's `packing-witness verify` (jlevy/squares `main` @ 19b354a5), unmodified: `VERIFIED`, 44551 pairs |
| `sqcheck-output.txt` | output of `verifier/sqcheck.py`, our independent exact checker: `VALID`, exact rational |
| `verifier/` | `sqcheck.py` and its README |
| `records/n-299-candidate-diff.png` | candidate vs the registry packing |

SHA-256: `n-299-candidate.yaml` `dfb0ccf71474a276a52ce768cc38e799d30ff6373a22b8ae318f58f278025d9d`; `n299-witness.json` `e2f178e7586729e3aa7ba5ad9c44eb8a406dbd1ca069a98b20ff367174036929`.

## Rerun

```
cp n-299-candidate.yaml <squares>/packing/witnesses/known-best/zz-cand.yaml
cd <squares>/packing && uv run --frozen --no-dev --with sympy --with mpmath packing-witness verify witnesses/known-best/zz-cand.yaml
python3 verifier/sqcheck.py n-299-candidate.yaml      # needs mpmath, sympy, pyyaml
```

## How the exact coordinates were made

The search produced a decimal pose (centre and angle per square). The registry's own `packing-witness promote --strategy robust-rational` (jlevy/squares @ 19b354a5) turned it into these exact rational corners: every pair is separated by at least about 2e-13 and squares touching the walls touch them exactly (containment clearance 0). `sqcheck.py` also certified the decimal pose itself in interval arithmetic before promotion.

## What differs from the registry packing

Squares matched by assignment up to the symmetries of the square: 187 of 299 centres move by more than 1e-3, 14 by more than 0.05 (largest 0.642); 5 squares are re-tilted by more than 1° (largest 41.32°); the packing has 94 tilted squares against 85.

## Lineage, credit and AI assistance

Started from the registry's current n = 299 packing (Evan Daniel (found_by) and Doğa Özden (improved_by), as the record lists them; T-263, #893), taken from the regularized known-best atlas of jlevy/squares. Found by basin hopping (kick, rotate, swap and reinsert moves) over local minima computed by Evan Daniel's ALM+SLP quench code from [evand/square-packing](https://github.com/evand/square-packing) (`search/packer`, MIT, at bb4cc78e), compiled into our search (its MIT licence kept with it). Credit the improvement to Doğa Özden, the base packing to its holders as the record lists them, and the local optimizer to Evan Daniel.

The search was AI-assisted throughout (an AI agent wrote and ran the search and the checks); the checks above were run by code that did not produce the packing. Doğa directed the work.

The best public Kaggle per-puzzle side we found for 299 is 17.801238552749 (jazivxt), above ours.
