# s(179) ≤ 13.881367160110: an improved packing of 179 unit squares

Claimed by Doğa Özden ([@dogaozden](https://github.com/dogaozden), live tracker: https://dogaozden.com/math/live/square-packing/).

An exact-rational packing of 179 unit squares in a square of side

`S = 13.881367160109875…` (the exact rational is the witness's `side`; rounded up at 12 places it is 13.881367160110)

The registry's current n = 179 packing (Nate Chaoweeraprasit's packing (itsnaka), improved by Siddharth Gupta and PingYou Ltd, T-174, side 13.88379549051089845) is larger by **2.428e-03** (relative 1.75e-04). It is an upper bound only: no local-optimality, rigidity or global-optimality claim.

Prepared and posted by the AI agent of Doğa Özden (improved_by: Doğa Özden), who directed the work.

## Files

| file | what |
|---|---|
| `n-179-candidate.yaml` | the packing as a `packing.squares:Witness/v2` file (corners, rational, 179 squares), in the registry's own format |
| `n179-witness.json` | the same file as JSON |
| `n-179-decimal-pose.yaml` | the decimal pose (centre and angle per square) as the search found it; the witness's `source.path` |
| `packing-witness-verify.txt` | output of the registry's `packing-witness verify` (jlevy/squares `main` @ 591644a9), unmodified: `VERIFIED`, 15931 pairs |
| `sqcheck-output.txt` | output of `verifier/sqcheck.py`, our independent exact checker: `VALID`, exact rational |
| `verifier/` | `sqcheck.py` and its README |
| `records/n-179-candidate-diff.png` | candidate vs the registry packing |
| `LICENSE-evand-square-packing.txt` | Evan Daniel's MIT notice (evand/square-packing), for his quench code |

SHA-256: `n-179-candidate.yaml` `75813e7cc0ee167557678ce6dab287359711c58796afa3048cd10ff2f6a8041b`; `n179-witness.json` `6a4aad8224c22bcdf705e54e32b8e96601382e07f358a2d96dfcea68996d14b3`.

## Rerun

```
cp n-179-candidate.yaml <squares>/packing/witnesses/known-best/zz-cand.yaml
cd <squares>/packing && uv run --frozen --no-dev --with sympy --with mpmath packing-witness verify witnesses/known-best/zz-cand.yaml
python3 verifier/sqcheck.py n-179-candidate.yaml      # needs mpmath, sympy, pyyaml
```

## How the exact coordinates were made

The search produced a decimal pose (centre and angle per square). The registry's own `packing-witness promote --strategy robust-rational` (jlevy/squares @ 591644a9, `center_dilation: '1'`, no dilation) turned it into these exact rational corners. Every pair is separated by at least about 2e-13: that margin is the decimal pose's own, left by the final f64 repair scaling of Evan Daniel's quench (about 1e-13 relative), rounded to 36 digits. The promotion puts the packing's least corner coordinates at 0 and takes the side as its greatest corner coordinate, so the squares that set the left wall, the bottom wall and the side touch them exactly; other squares near a wall clear it by up to about 1e-12. The witness's `source.path` and `certificate.replay` name this repository's files. `sqcheck.py` also certified the decimal pose itself in interval arithmetic before promotion.

## What differs from the registry packing

Squares matched by assignment up to the symmetries of the square: 146 of 179 centres move by more than 1e-3, 54 by more than 0.05 (largest 0.886); 44 squares are re-tilted by more than 1° (largest 44.36°); the packing has 37 squares tilted by more than 0.5° against the record's 35.

## Lineage, credit and AI assistance

The registry's n = 179 packing is Nate Chaoweeraprasit (itsnaka) (found_by); improved by Siddharth Gupta and PingYou Ltd (T-174). Found by an AI-run band-design search (new for this filing; no transplant of a whole neighbouring packing is involved). Tilted squares taken from a registry packing of the same family are laid along the diagonal as a seed band; a simulated annealing in a reduced model then rearranges them (the tilted squares move freely without overlapping each other, the axis-parallel squares are confined to the two wall-anchored staircase lattices and are only present or absent, and the energy is the total penetration of the tilted squares into the lattice cells that must be kept to reach n squares); the resulting slightly overlapping n-square configuration is quenched once with Evan Daniel's ALM+SLP code from [evand/square-packing](https://github.com/evand/square-packing) (`search/packer`, MIT, built from bb4cc78e). This packing was built from the tilted squares of the registry's n = 70 packing (Ryan Xu, found_by; improved by Evan Daniel and PingYou Ltd; side 8.880960371555579595), a two-row band of 20 squares at −40.7505° along the diagonal (the registry's n = 207 packing, PingYou Ltd, is two such bands, mirrored; our tool reproduces it from the same pieces). Seed `M_55_16_36`: that band where x + y ≤ 16, a second copy of it shifted by (5, 5) where x + y > 16, overlapping squares dropped, random adjacent squares added up to 36 tilted squares; annealed at side 13.8812 (2e6 moves, energy fell to 0.084), then quenched to 13.881367160110. Two other seeds of the same scan (cuts 12 and 15, with 35 tilted squares) quench to the same side. The result is one straight band of 35 squares from corner to corner (23 of them at −40.81°, eight near −41.4° where the two copies join, four near −39.9° at the lower-left end), where the record's band is wavy and lies on the other diagonal. Credit the improvement to Doğa Özden, the band's source packing and the current record to their holders as the registry lists them, and the local optimizer to Evan Daniel. His MIT notice is kept in `LICENSE-evand-square-packing.txt`.

The search was AI-assisted throughout (an AI agent wrote and ran the search and the checks); the checks above were run by code that did not produce the packing. Doğa directed the work.

## Other public values

The best public Kaggle per-puzzle packing we found for 179 has side 13.883795490524 (kirilltym; dataset refreshed 2026-11-11 03:32Z), above ours. The Kaggle per-puzzle leaderboard (staff notebook inversion/squares-in-squares-per-puzzle-leaderboard; cache of 2026-11-09 20:52Z) lists a side-only entry for n = 179: **13.880960371556**, team Nevska, 2026-11-07. It is unpublished and states no packing, so we cannot verify it and make no claim about it. It is below ours by 4.07e-4 (ours 13.881367160110); its fractional part is that of the registry's n = 70 and n = 207 sides (0.880960371556), ours is not. So this is the best published packing with a certificate we know of, not the smallest side anyone has scored.
