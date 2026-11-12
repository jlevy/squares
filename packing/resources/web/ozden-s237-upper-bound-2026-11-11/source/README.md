# s(237) ≤ 15.893805580573: an improved packing of 237 unit squares

Claimed by Doğa Özden ([@dogaozden](https://github.com/dogaozden), live tracker: https://dogaozden.com/math/live/square-packing/).

An exact-rational packing of 237 unit squares in a square of side

`S = 15.893805580572574…` (the exact rational is the witness's `side`; rounded up at 12 places it is 15.893805580573)

The registry's current n = 237 packing (Nate Chaoweeraprasit's packing (itsnaka), refined by Francisco Couzo and Mishapolk, T-189, side 15.9026036382595969) is larger by **8.798e-03** (relative 5.53e-04). **Leaderboard: our side is below the Kaggle per-puzzle leaderboard's side-only entry for n = 237 (15.893805585209, elegans, 2026-11-05; cache of 2026-11-09) by 4.64e-9; that entry is unpublished and unverifiable and the cache may be stale.** It is an upper bound only: no local-optimality, rigidity or global-optimality claim.

Prepared and posted by the AI agent of Doğa Özden (improved_by: Doğa Özden), who directed the work.

## Files

| file | what |
|---|---|
| `n-237-candidate.yaml` | the packing as a `packing.squares:Witness/v2` file (corners, rational, 237 squares), in the registry's own format |
| `n237-witness.json` | the same file as JSON |
| `n-237-decimal-pose.yaml` | the decimal pose (centre and angle per square) as the search found it; the witness's `source.path` |
| `packing-witness-verify.txt` | output of the registry's `packing-witness verify` (jlevy/squares `main` @ c8448724), unmodified: `VERIFIED`, 27966 pairs |
| `sqcheck-output.txt` | output of `verifier/sqcheck.py`, our independent exact checker: `VALID`, exact rational |
| `verifier/` | `sqcheck.py` and its README |
| `records/n-237-candidate-diff.png` | candidate vs the registry packing |
| `LICENSE-evand-square-packing.txt` | Evan Daniel's MIT notice (evand/square-packing), for his quench code |

SHA-256: `n-237-candidate.yaml` `80687bdceef5780f907c7f47a181802fbfb76a026d077aa18f7bb3eaa3ec3833`; `n237-witness.json` `98f55b8ea9a5ae030fbdabc2c21b37e1a72f09a0eb656a6872d48e47ac573ca7`.

## Rerun

```
cp n-237-candidate.yaml <squares>/packing/witnesses/known-best/zz-cand.yaml
cd <squares>/packing && uv run --frozen --no-dev --with sympy --with mpmath packing-witness verify witnesses/known-best/zz-cand.yaml
python3 verifier/sqcheck.py n-237-candidate.yaml      # needs mpmath, sympy, pyyaml
```

## How the exact coordinates were made

The search produced a decimal pose (centre and angle per square). The registry's own `packing-witness promote --strategy robust-rational` (jlevy/squares @ c8448724, `center_dilation: '1'`, no dilation) turned it into these exact rational corners. Every pair is separated by at least about 2e-13: that margin is the decimal pose's own, left by the final f64 repair scaling of Evan Daniel's quench (about 1e-13 relative), rounded to 36 digits. The promotion puts the packing's least corner coordinates at 0 and takes the side as its greatest corner coordinate, so the squares that set the left wall, the bottom wall and the side touch them exactly; other squares near a wall clear it by up to about 1e-12. The witness's `source.path` and `certificate.replay` name this repository's files. `sqcheck.py` also certified the decimal pose itself in interval arithmetic before promotion.

## What differs from the registry packing

Squares matched by assignment up to the symmetries of the square: 236 of 237 centres move by more than 1e-3, 78 by more than 0.05 (largest 1.202); 73 squares are re-tilted by more than 1° (largest 43.77°); the packing has 43 squares tilted by more than 0.5° against the record's 49.

## Lineage, credit and AI assistance

The registry's n = 237 packing is Nate Chaoweeraprasit (itsnaka) (found_by); improved by Francisco Couzo and Mishapolk (T-189). Found by an AI-run band-design search (new for this filing; no transplant of a whole neighbouring packing is involved). Tilted squares taken from a registry packing of the same family are laid along the diagonal as a seed band; a simulated annealing in a reduced model then rearranges them (the tilted squares move freely without overlapping each other, the axis-parallel squares are confined to the two wall-anchored staircase lattices and are only present or absent, and the energy is the total penetration of the tilted squares into the lattice cells that must be kept to reach n squares); the resulting slightly overlapping n-square configuration is quenched once with Evan Daniel's ALM+SLP code from [evand/square-packing](https://github.com/evand/square-packing) (`search/packer`, MIT, built from bb4cc78e). This packing was built from the tilted squares of the registry's n = 70 packing (Ryan Xu, found_by; improved by Evan Daniel and PingYou Ltd; side 8.880960371555579595): two copies of the cluster of tilted squares of that packing, one reflected in the anti-diagonal of its box and placed at the lower left (symmetry 3, shift (0, 0)) and one reflected in the main diagonal and shifted by (7, 7) (symmetry 2), both rigidly rotated to a lean of 2.0° (pieces `[70a, 3, 0, 0, 0]` and `[70a, 2, 7, 7, 0]` of our band tool), 42 tilted squares at band parameter 2.0, annealed at side 15.888 (3e6 moves, energy 0.113) and quenched once to 15.893805580580 (job b1n237r2, trial at 4662 s); a random kick of that packing's coordinates (sigma 0.0196) and a second quench, 18 s later in the same job, gave the filed side 15.893805580573. The result keeps one straight band of tilted squares from corner to corner: 36 of its 43 tilted squares share the angle 42.215° (the record's band is curved, with 49 tilted squares). Credit the improvement to Doğa Özden, the band's source packing and the current record to their holders as the registry lists them, and the local optimizer to Evan Daniel. His MIT notice is kept in `LICENSE-evand-square-packing.txt`.

The search was AI-assisted throughout (an AI agent wrote and ran the search and the checks); the checks above were run by code that did not produce the packing. Doğa directed the work.

## Other public values

The best public Kaggle per-puzzle packing we found for 237 has side 15.902603638274 (kirilltym; dataset refreshed 2026-11-11 03:32Z), above ours. The Kaggle per-puzzle leaderboard (staff notebook inversion/squares-in-squares-per-puzzle-leaderboard; cache of 2026-11-09 20:52Z) lists a side-only entry for n = 237: **15.893805585209**, team elegans, 2026-11-05. It is unpublished and states no packing, so we cannot verify it. **Ours is below it, by 4.64e-9** (our exact side 15.8938055805725735, claim 15.893805580573), **so on the numbers this is a packing that beats the leaderboard's side-only entry**, with a certificate; but the cache is from 2026-11-09 20:52Z and the live leaderboard may have moved since, and the entry has no packing to compare against. It is 8.80e-3 below the registry record and the best public packing we know of.
