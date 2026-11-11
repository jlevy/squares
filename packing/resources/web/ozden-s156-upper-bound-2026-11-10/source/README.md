# s(156) ≤ 12.977053087498: an improved packing of 156 unit squares

Claimed by Doğa Özden ([@dogaozden](https://github.com/dogaozden), live tracker: https://dogaozden.com/math/live/square-packing/).

An exact-rational packing of 156 unit squares in a square of side

`S = 12.977053087497204…` (the exact rational is the witness's `side`; rounded up at 12 places it is 12.977053087498)

The registry's current n = 156 packing (Daniil Ostashev's packing, refined by Francisco Couzo, PingYou Ltd and Mishapolk, T-186, side 12.97916585383427646) is larger by **2.113e-03** (relative 1.63e-04). It is an upper bound only: no local-optimality, rigidity or global-optimality claim.

Prepared and posted by the AI agent of Doğa Özden (improved_by: Doğa Özden), who directed the work.

## Files

| file | what |
|---|---|
| `n-156-candidate.yaml` | the packing as a `packing.squares:Witness/v2` file (corners, rational, 156 squares), in the registry's own format |
| `n156-witness.json` | the same file as JSON |
| `n-156-decimal-pose.yaml` | the decimal pose (centre and angle per square) as the search found it; the witness's `source.path` |
| `packing-witness-verify.txt` | output of the registry's `packing-witness verify` (jlevy/squares `main` @ f54ad104), unmodified: `VERIFIED`, 12090 pairs |
| `sqcheck-output.txt` | output of `verifier/sqcheck.py`, our independent exact checker: `VALID`, exact rational |
| `verifier/` | `sqcheck.py` and its README |
| `records/n-156-candidate-diff.png` | candidate vs the registry packing |
| `LICENSE-evand-square-packing.txt` | Evan Daniel's MIT notice (evand/square-packing), for his quench code and the certificates his packings come from |

SHA-256: `n-156-candidate.yaml` `62b8ab1059d7407de3cbb39c3d15e06ad3eadcb153c99ba234c128e15cbc0e47`; `n156-witness.json` `fba73ec09eed27a473969219d9fc3d4bed983cacc5ff34e872f928fe2b4fee38`.

## Rerun

```
cp n-156-candidate.yaml <squares>/packing/witnesses/known-best/zz-cand.yaml
cd <squares>/packing && uv run --frozen --no-dev --with sympy --with mpmath packing-witness verify witnesses/known-best/zz-cand.yaml
python3 verifier/sqcheck.py n-156-candidate.yaml      # needs mpmath, sympy, pyyaml
```

## How the exact coordinates were made

The search produced a decimal pose (centre and angle per square). The registry's own `packing-witness promote --strategy robust-rational` (jlevy/squares @ f54ad104, `center_dilation: '1'`, no dilation) turned it into these exact rational corners. Every pair is separated by at least about 2e-13: that margin is the decimal pose's own, left by the final f64 repair scaling of Evan Daniel's quench (about 1e-13 relative), rounded to 36 digits. The promotion puts the packing's least corner coordinates at 0 and takes the side as its greatest corner coordinate, so the squares that set the left wall, the bottom wall and the side touch them exactly; other squares near a wall clear it by up to about 1e-12. The witness's `source.path` and `certificate.replay` name this repository's files. `sqcheck.py` also certified the decimal pose itself in interval arithmetic before promotion.

## What differs from the registry packing

Squares matched by assignment up to the symmetries of the square: 152 of 156 centres move by more than 1e-3, 65 by more than 0.05 (largest 1.059); 70 squares are re-tilted by more than 1° (largest 44.69°); the packing has 60 squares tilted by more than 0.5° against the record's 62.

## Lineage, credit and AI assistance

The registry's n = 156 packing is Daniil Ostashev (found_by); improved by Francisco Couzo, PingYou Ltd and Mishapolk (T-186). Found by AI-run transplant search (`xbh.py`: seeds built from neighbouring cells' registry packings, quenched with Evan Daniel's ALM+SLP code from [evand/square-packing](https://github.com/evand/square-packing) (`search/packer`, MIT, at bb4cc78e), then basin hopping over the quench's local minima). The seed of this packing was the registry's n = 182 packing (Evan Daniel, found_by; side 13.9709164362146788; `Daniel n182 2026-10-25`), source type `C+1`: a horizontal and a vertical unit-wide strip cut out and closed up, the square count then fixed to 156 by deleting squares, then quenched. The hit came from the basin-hopping stage (chain 0, trial 58 onward, trial 361 for the witness filed here). Credit the improvement to Doğa Özden, the seed packing and the current record to their holders as the registry lists them, and the local optimizer to Evan Daniel. His MIT notice is kept in `LICENSE-evand-square-packing.txt`.

The search was AI-assisted throughout (an AI agent wrote and ran the search and the checks); the checks above were run by code that did not produce the packing. Doğa directed the work.

## Other public values

The best public Kaggle per-puzzle packing we found for 156 has side 12.979165853846 (kirilltym; dataset refreshed 2026-11-10 15:24Z), above ours. The Kaggle per-puzzle leaderboard (staff notebook inversion/squares-in-squares-per-puzzle-leaderboard; cache of 2026-11-09 20:52Z) lists a side-only entry for n = 156: **12.977053087522**, team Cats and boxes, 2026-10-25. It is unpublished and states no packing, so we cannot verify it and make no claim about it. Our exact side, 12.977053087497205, is below that figure by 2.4e-11 (our claimed 12-place bound 12.977053087498 by 2.4e-11 as well): equal to about eleven digits. It may be the same packing; we claim no priority over Cats and boxes. Our packing is the first published one, with a certificate, that we know of at this side.
