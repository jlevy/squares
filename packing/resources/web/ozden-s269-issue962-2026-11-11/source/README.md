# s(269) ≤ 16.899469075856: an improved packing of 269 unit squares

Claimed by Doğa Özden ([@dogaozden](https://github.com/dogaozden), live tracker: https://dogaozden.com/math/live/square-packing/).

An exact-rational packing of 269 unit squares in a square of side

`S = 16.899469075855046…` (the exact rational is the witness's `side`; rounded up at 12 places it is 16.899469075856)

The registry's current n = 269 packing (our own packing (Doğa Özden, found_by; jlevy/squares#947), built from Nate Chaoweeraprasit's packing (itsnaka) improved by Evan Daniel and PingYou Ltd, T-290, side 16.9009945799513249) is larger by **1.526e-03** (relative 9.03e-05). **Leaderboard: our side does not beat the Kaggle per-puzzle leaderboard's side-only entry for n = 269 (16.889730079125, elegans, 2026-11-05; cache of 2026-11-09): it is above it by 9.74e-3. That entry is unpublished and unverifiable.** This improves our own #947 (registry T-290, 16.9009945799513249) by 1.5255e-3, and supersedes it. It is an upper bound only: no local-optimality, rigidity or global-optimality claim.

Prepared and posted by the AI agent of Doğa Özden (improved_by: Doğa Özden), who directed the work.

## Files

| file | what |
|---|---|
| `n-269-candidate.yaml` | the packing as a `packing.squares:Witness/v2` file (corners, rational, 269 squares), in the registry's own format |
| `n269-witness.json` | the same file as JSON |
| `n-269-decimal-pose.yaml` | the decimal pose (centre and angle per square) as the search found it; the witness's `source.path` |
| `packing-witness-verify.txt` | output of the registry's `packing-witness verify` (jlevy/squares `main` @ 0af33d85), unmodified: `VERIFIED`, 36046 pairs |
| `sqcheck-output.txt` | output of `verifier/sqcheck.py`, our independent exact checker: `VALID`, exact rational |
| `verifier/` | `sqcheck.py` and its README |
| `records/n-269-candidate-diff.png` | candidate vs the registry packing |
| `LICENSE-evand-square-packing.txt` | Evan Daniel's MIT notice (evand/square-packing), for his quench code |

SHA-256: `n-269-candidate.yaml` `54b408b2f1b45fc3d0a1330767c8740f0889eecb73f5fcf7888710526dbcc26b`; `n269-witness.json` `4b7ac2a7402037b047c04e239d239042228ae6c68f09cb917e09fa128f5b9cc0`.

## Rerun

```
cp n-269-candidate.yaml <squares>/packing/witnesses/known-best/zz-cand.yaml
cd <squares>/packing && uv run --frozen --no-dev --with sympy --with mpmath packing-witness verify witnesses/known-best/zz-cand.yaml
python3 verifier/sqcheck.py n-269-candidate.yaml      # needs mpmath, sympy, pyyaml
```

## How the exact coordinates were made

The search produced a decimal pose (centre and angle per square). The registry's own `packing-witness promote --strategy robust-rational` (jlevy/squares @ 0af33d85, `center_dilation: '1'`, no dilation) turned it into these exact rational corners. Every pair is separated by at least about 2e-13: that margin is the decimal pose's own, left by the final f64 repair scaling of Evan Daniel's quench (about 1e-13 relative), rounded to 36 digits. The promotion puts the packing's least corner coordinates at 0 and takes the side as its greatest corner coordinate, so the squares that set the left wall, the bottom wall and the side touch them exactly; other squares near a wall clear it by up to about 1e-12. The witness's `source.path` and `certificate.replay` name this repository's files. `sqcheck.py` also certified the decimal pose itself in interval arithmetic before promotion.

## What differs from the registry packing

Squares matched by assignment up to the symmetries of the square: 262 of 269 centres move by more than 1e-3, 124 by more than 0.05 (largest 1.456); 116 squares are re-tilted by more than 1° (largest 44.77°); the packing has 46 squares tilted by more than 0.5° against the record's 100.

## Lineage, credit and AI assistance

The registry's n = 269 packing is Doğa Özden (found_by; our issue #947), a packing found by transplanting Evan Daniel's n = 304 packing (T-290). Found by an AI-run band-design search (new for this filing; no transplant of a whole neighbouring packing is involved). Tilted squares taken from a registry packing of the same family are laid along the diagonal as a seed band; a simulated annealing in a reduced model then rearranges them (the tilted squares move freely without overlapping each other, the axis-parallel squares are confined to the two wall-anchored staircase lattices and are only present or absent, and the energy is the total penetration of the tilted squares into the lattice cells that must be kept to reach n squares); the resulting slightly overlapping n-square configuration is quenched once with Evan Daniel's ALM+SLP code from [evand/square-packing](https://github.com/evand/square-packing) (`search/packer`, MIT, built from bb4cc78e). This packing was built from tilted squares of three clusters of registry or own packings: the second cluster of tilted squares of the registry's n = 207 packing (`207b`), the cluster of the registry's n = 70 packing (`70a`; Ryan Xu, found_by; improved by Evan Daniel and PingYou Ltd), and the first cluster of our own n = 179 band packing (`179ha`, jlevy/squares#954), each reflected in the main diagonal of its box (symmetry 2; shifts (0, 0), (0, 0) and (3, 3), our band tool's `[207b, 2, 0, 0, 0]`, `[70a, 2, 0, 0, 0]`, `[179ha, 2, 3, 3, 0]`) and rotated to a lean of 2.55°, 45 tilted squares at band parameter 0.899, annealed at that side (2e7 moves, energy 0.0719) and quenched once to 16.899469084224 (job b1n269r2, trial at 4806 s). A random kick of that packing's coordinates (sigma 0.0031) and a second quench, 18 s later in the same job, gave 16.899469075879, and a further kick (sigma 0.0296) and quench, 3 s after that, gave the filed side 16.899469075855. The filed packing has 46 tilted squares (the record, our #947, has 100); 16 of them share the angle -42.88° (it is not one clean band). Credit the improvement to Doğa Özden, the band's source packing and the current record to their holders as the registry lists them, and the local optimizer to Evan Daniel. His MIT notice is kept in `LICENSE-evand-square-packing.txt`.

The search was AI-assisted throughout (an AI agent wrote and ran the search and the checks); the checks above were run by code that did not produce the packing. Doğa directed the work.

## Other public values

The best public Kaggle per-puzzle packing we found for 269 has side 16.901513582205 (kirilltym; dataset refreshed 2026-11-11 03:32Z), above ours. The Kaggle per-puzzle leaderboard (staff notebook inversion/squares-in-squares-per-puzzle-leaderboard; cache of 2026-11-09 20:52Z) lists a side-only entry for n = 269: **16.889730079125**, team elegans, 2026-11-05. It is unpublished and states no packing, so we cannot verify it and make no claim about it. **Ours does not beat it: it is above it by 9.74e-3** (our exact side 16.8994690758550465, claim 16.899469075856). The cache is from 2026-11-09 20:52Z. Ours is 1.53e-3 below the registry record (our own #947, T-290) and below the best public packing we know of (16.901513582205, kirilltym), so it is the best published packing with a certificate we know of, not the smallest side anyone has scored.
