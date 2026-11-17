# s(172) ≤ 13.614689853287: an improved packing of 172 unit squares

Claimed by Doğa Özden ([@dogaozden](https://github.com/dogaozden), live tracker: https://dogaozden.com/math/live/square-packing/).

An exact-rational packing of 172 unit squares in a square of side

`S = 13.614689853286215…` (the exact rational is the witness's `side`; rounded up at 12 places it is 13.614689853287)

The registry's current n = 172 packing (Evan Daniel's packing, T-257, issue #845, side 13.6179356983814155) is larger by **3.246e-03** (relative 2.38e-04). It is an upper bound only: no local-optimality, rigidity or global-optimality claim.

Prepared and posted by the AI agent of Doğa Özden (improved_by: Doğa Özden), who directed the work.

## Files

| file | what |
|---|---|
| `n-172-candidate.yaml` | the packing as a `packing.squares:Witness/v2` file (corners, rational, 172 squares), in the registry's own format |
| `n172-witness.json` | the same file as JSON |
| `n-172-decimal-pose.yaml` | the decimal pose (centre and angle per square) as the search found it; the witness's `source.path` |
| `packing-witness-verify.txt` | output of the registry's `packing-witness verify` (jlevy/squares `main` @ ef1af493), unmodified: `VERIFIED`, 14706 pairs |
| `sqcheck-output.txt` | output of `verifier/sqcheck.py`, our independent exact checker: `VALID`, exact rational |
| `verifier/` | `sqcheck.py` and its README |
| `records/n-172-candidate-diff.png` | candidate vs the registry packing |
| `LICENSE-evand-square-packing.txt` | Evan Daniel's MIT notice (evand/square-packing), for his base packing's certificate and his quench code |

SHA-256: `n-172-candidate.yaml` `0df5ae7936950b9a1fe06832cb8f8bdc21dbae9e0d009c6b87302a14c452b2af`; `n172-witness.json` `311a83339e86d503954c8f423b0c6e0ca3c2c5bfb6e80c37d53ec064667aa2bf`.

## Rerun

```
cp n-172-candidate.yaml <squares>/packing/witnesses/known-best/zz-cand.yaml
cd <squares>/packing && uv run --frozen --no-dev --with sympy --with mpmath packing-witness verify witnesses/known-best/zz-cand.yaml
python3 verifier/sqcheck.py n-172-candidate.yaml      # needs mpmath, sympy, pyyaml
```

## How the exact coordinates were made

The search produced a decimal pose (centre and angle per square). The registry's own `packing-witness promote --strategy robust-rational` (jlevy/squares @ ef1af493, `center_dilation: '1'`, no dilation) turned it into these exact rational corners. Every pair is separated by at least about 2e-13: that margin is the decimal pose's own, left by the final f64 repair scaling of Evan Daniel's quench (about 1e-13 relative), rounded to 36 digits. The promotion puts the packing's least corner coordinates at 0 and takes the side as its greatest corner coordinate, so the squares that set the left wall, the bottom wall and the side touch them exactly; other squares near a wall clear it by up to about 1e-12. The witness's `source.path` and `certificate.replay` name this repository's files. `sqcheck.py` also certified the decimal pose itself in interval arithmetic before promotion.

## What differs from the registry packing

Squares matched by assignment up to the symmetries of the square: 168 of 172 centres move by more than 1e-3, 37 by more than 0.05 (largest 0.668); 15 squares are re-tilted by more than 1° (largest 44.61°); the packing has 49 squares tilted by more than 0.5° against the record's 49.

## Lineage, credit and AI assistance

Started from the registry's current n = 172 packing (Evan Daniel (found_by); T-257, #845), taken from the regularized known-best atlas of jlevy/squares. Found by basin hopping (kick, rotate, swap and reinsert moves) over local minima computed by Evan Daniel's ALM+SLP quench code from [evand/square-packing](https://github.com/evand/square-packing) (`search/packer`, MIT, at bb4cc78e), built unmodified into our search. The base packing comes from Evan Daniel's MIT-licensed certificate; his MIT notice is kept in `LICENSE-evand-square-packing.txt`. Credit the improvement to Doğa Özden, the base packing to its holders as the record lists them, and the local optimizer to Evan Daniel.

The search was AI-assisted throughout (an AI agent wrote and ran the search and the checks); the checks above were run by code that did not produce the packing. Doğa directed the work.

The best public Kaggle per-puzzle side we found for 172 is 13.617935700905 (jazivxt), above ours.
