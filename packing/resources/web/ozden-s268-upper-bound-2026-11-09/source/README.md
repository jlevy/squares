# s(268) ≤ 16.872469897837: an improved packing of 268 unit squares

Claimed by Doğa Özden ([@dogaozden](https://github.com/dogaozden), live tracker: https://dogaozden.com/math/live/square-packing/).

An exact-rational packing of 268 unit squares in a square of side

`S = 16.872469897836212…` (the exact rational is the witness's `side`; rounded up at 12 places it is 16.872469897837)

The registry's current n = 268 packing (Evan Daniel's packing built by his fault-line composer after Chris Deotte's multi-gadget fault DP, T-270, issue #914, side 16.8724995181350307) is larger by **2.962e-05** (relative 1.76e-06). It is an upper bound only: no local-optimality, rigidity or global-optimality claim.

Prepared and posted by the AI agent of Doğa Özden (improved_by: Doğa Özden), who directed the work.

## Files

| file | what |
|---|---|
| `n-268-candidate.yaml` | the packing as a `packing.squares:Witness/v2` file (corners, rational, 268 squares), in the registry's own format |
| `n268-witness.json` | the same file as JSON |
| `packing-witness-verify.txt` | output of the registry's `packing-witness verify` (jlevy/squares `main` @ 19b354a5), unmodified: `VERIFIED`, 35778 pairs |
| `sqcheck-output.txt` | output of `verifier/sqcheck.py`, our independent exact checker: `VALID`, exact rational |
| `verifier/` | `sqcheck.py` and its README |
| `records/n-268-candidate-diff.png` | candidate vs the registry packing |

SHA-256: `n-268-candidate.yaml` `74c0e5d4927ec57468f0cae71636ba46833230ceea4d1dd0cd5ddc1ed76421b3`; `n268-witness.json` `fcd07b9ff77e7e9be86fcf78eebee721bcfd1c4e5d6ffa2c8164847a4dd0d180`.

## Rerun

```
cp n-268-candidate.yaml <squares>/packing/witnesses/known-best/zz-cand.yaml
cd <squares>/packing && uv run --frozen --no-dev --with sympy --with mpmath packing-witness verify witnesses/known-best/zz-cand.yaml
python3 verifier/sqcheck.py n-268-candidate.yaml      # needs mpmath, sympy, pyyaml
```

## How the exact coordinates were made

The search produced a decimal pose (centre and angle per square). The registry's own `packing-witness promote --strategy robust-rational` (jlevy/squares @ 19b354a5) turned it into these exact rational corners: every pair is separated by at least about 2e-13 and squares touching the walls touch them exactly (containment clearance 0). `sqcheck.py` also certified the decimal pose itself in interval arithmetic before promotion.

## What differs from the registry packing

Squares matched by assignment up to the symmetries of the square: 122 of 268 centres move by more than 1e-3, 11 by more than 0.05 (largest 0.274); 3 squares are re-tilted by more than 1° (largest 2.14°); the packing has 99 tilted squares against 99.

## Lineage, credit and AI assistance

Started from the registry's current n = 268 packing (Evan Daniel (found_by), after Chris Deotte; T-270, #914), taken from the regularized known-best atlas of jlevy/squares. Found by basin hopping (kick, rotate, swap and reinsert moves) over local minima computed by Evan Daniel's ALM+SLP quench code from [evand/square-packing](https://github.com/evand/square-packing) (`search/packer`, MIT, at bb4cc78e), compiled into our search (its MIT licence kept with it). Credit the improvement to Doğa Özden, the base packing to its holders as the record lists them, and the local optimizer to Evan Daniel.

The search was AI-assisted throughout (an AI agent wrote and ran the search and the checks); the checks above were run by code that did not produce the packing. Doğa directed the work.

The best public Kaggle per-puzzle side we found for 268 is 16.874361715873 (ntumlnoob), above ours.
