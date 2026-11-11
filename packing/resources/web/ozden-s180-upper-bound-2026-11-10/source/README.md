# s(180) ≤ 13.915618502791: an improved packing of 180 unit squares

Claimed by Doğa Özden ([@dogaozden](https://github.com/dogaozden), live tracker: https://dogaozden.com/math/live/square-packing/).

An exact-rational packing of 180 unit squares in a square of side

`S = 13.915618502790025…` (the exact rational is the witness's `side`; rounded up at 12 places it is 13.915618502791)

The registry's current n = 180 packing (Nate Chaoweeraprasit's packing (itsnaka), refined by Siddharth Gupta, Francisco Couzo and PingYou Ltd, T-174, side 13.91699352247783249) is larger by **1.375e-03** (relative 9.88e-05). It is an upper bound only: no local-optimality, rigidity or global-optimality claim.

Prepared and posted by the AI agent of Doğa Özden (improved_by: Doğa Özden), who directed the work.

## Files

| file | what |
|---|---|
| `n-180-candidate.yaml` | the packing as a `packing.squares:Witness/v2` file (corners, rational, 180 squares), in the registry's own format |
| `n180-witness.json` | the same file as JSON |
| `n-180-decimal-pose.yaml` | the decimal pose (centre and angle per square) as the search found it; the witness's `source.path` |
| `packing-witness-verify.txt` | output of the registry's `packing-witness verify` (jlevy/squares `main` @ f54ad104), unmodified: `VERIFIED`, 16110 pairs |
| `sqcheck-output.txt` | output of `verifier/sqcheck.py`, our independent exact checker: `VALID`, exact rational |
| `verifier/` | `sqcheck.py` and its README |
| `records/n-180-candidate-diff.png` | candidate vs the registry packing |
| `LICENSE-evand-square-packing.txt` | Evan Daniel's MIT notice (evand/square-packing), for his quench code and the certificates his packings come from |

SHA-256: `n-180-candidate.yaml` `91447bf157126c4c62edcc6751b10892fd1cb1e0006de9a82e5020809e6676f9`; `n180-witness.json` `7ab902b0dbd3c68bf797fe396cb62c630a66edfe09c8fe57a0e7e8ae1498754d`.

## Rerun

```
cp n-180-candidate.yaml <squares>/packing/witnesses/known-best/zz-cand.yaml
cd <squares>/packing && uv run --frozen --no-dev --with sympy --with mpmath packing-witness verify witnesses/known-best/zz-cand.yaml
python3 verifier/sqcheck.py n-180-candidate.yaml      # needs mpmath, sympy, pyyaml
```

## How the exact coordinates were made

The search produced a decimal pose (centre and angle per square). The registry's own `packing-witness promote --strategy robust-rational` (jlevy/squares @ f54ad104, `center_dilation: '1'`, no dilation) turned it into these exact rational corners. Every pair is separated by at least about 2e-13: that margin is the decimal pose's own, left by the final f64 repair scaling of Evan Daniel's quench (about 1e-13 relative), rounded to 36 digits. The promotion puts the packing's least corner coordinates at 0 and takes the side as its greatest corner coordinate, so the squares that set the left wall, the bottom wall and the side touch them exactly; other squares near a wall clear it by up to about 1e-12. The witness's `source.path` and `certificate.replay` name this repository's files. `sqcheck.py` also certified the decimal pose itself in interval arithmetic before promotion.

## What differs from the registry packing

Squares matched by assignment up to the symmetries of the square: 162 of 180 centres move by more than 1e-3, 49 by more than 0.05 (largest 0.91); 49 squares are re-tilted by more than 1° (largest 44.68°); the packing has 40 squares tilted by more than 0.5° against the record's 44.

## Lineage, credit and AI assistance

The registry's n = 180 packing is Nate Chaoweeraprasit (itsnaka) (found_by); improved by Siddharth Gupta, Francisco Couzo and PingYou Ltd (T-174). Found by AI-run transplant search (`xbh.py`: seeds built from neighbouring cells' registry packings, quenched with Evan Daniel's ALM+SLP code from [evand/square-packing](https://github.com/evand/square-packing) (`search/packer`, MIT, at bb4cc78e), then basin hopping over the quench's local minima). The seed of this packing was the registry's n = 154 packing (Evan Daniel, found_by, improved by Francisco Couzo; side 12.9211009407616806; `Daniel n154 sweep 2026-10-20`), source type `L-1`: an L of axis-aligned grid squares added along two walls (one of the four corners), the square count then fixed to 180 by deleting or inserting squares, then quenched. The hit came from the basin-hopping stage (chain 2, trial 1281, move `kick`). Credit the improvement to Doğa Özden, the seed packing and the current record to their holders as the registry lists them, and the local optimizer to Evan Daniel. His MIT notice is kept in `LICENSE-evand-square-packing.txt`.

The search was AI-assisted throughout (an AI agent wrote and ran the search and the checks); the checks above were run by code that did not produce the packing. Doğa directed the work.

## Other public values

The best public Kaggle per-puzzle packing we found for 180 has side 13.916993522491 (kirilltym; dataset refreshed 2026-11-10 15:24Z), above ours. The Kaggle per-puzzle leaderboard (cache of 2026-11-09 20:52Z) lists a side-only entry for n = 180: 13.916993522478, team webmaking, 2026-10-27. That figure is the registry's side to 12 digits; ours is below it by 1.375e-3. So ours is below the leaderboard side as well as below every published packing we know of.
