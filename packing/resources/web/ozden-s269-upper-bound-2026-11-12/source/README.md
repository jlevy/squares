# s(269) ≤ 16.889730073596: an improved packing of 269 unit squares

Claimed by Doğa Özden ([@dogaozden](https://github.com/dogaozden), live tracker: https://dogaozden.com/math/live/square-packing/).

An exact-rational packing of 269 unit squares in a square of side

`S = 16.889730073595636…` (the exact rational is the witness's `side`; rounded up at 12 places it is 16.889730073596)

The registry's current n = 269 packing (our own packing (Doğa Özden, found_by; jlevy/squares#947), built from Nate Chaoweeraprasit's packing (itsnaka) improved by Evan Daniel and PingYou Ltd, T-290, side 16.9009945799513249) is larger by **1.126e-02** (relative 6.66e-04). **Leaderboard: our certified side is below the Kaggle per-puzzle leaderboard's side-only entry for n = 269 (16.889730079125, elegans, 2026-11-05; cache of 2026-11-09) by 5.53e-9. That entry is unpublished and unverifiable.** This improves our own #947 (registry T-290, 16.9009945799513249) by 1.1265e-2, and also our own, still open #962 (16.8994690758550465) by 9.74e-3; it supersedes both. It is an upper bound only: no local-optimality, rigidity or global-optimality claim.

Prepared and posted by the AI agent of Doğa Özden (improved_by: Doğa Özden), who directed the work.

## Files

| file | what |
|---|---|
| `n-269-candidate.yaml` | the packing as a `packing.squares:Witness/v2` file (corners, rational, 269 squares), in the registry's own format |
| `n269-witness.json` | the same file as JSON |
| `n-269-decimal-pose.yaml` | the decimal pose (centre and angle per square) as the search found it; the witness's `source.path` |
| `packing-witness-verify.txt` | output of the registry's `packing-witness verify` (jlevy/squares `main` @ 0352d755), unmodified: `VERIFIED`, 36046 pairs |
| `sqcheck-output.txt` | output of `verifier/sqcheck.py`, our independent exact checker: `VALID`, exact rational |
| `verifier/` | `sqcheck.py` and its README |
| `records/n-269-candidate-diff.png` | candidate vs the registry packing |
| `LICENSE-evand-square-packing.txt` | Evan Daniel's MIT notice (evand/square-packing), for his quench code |

SHA-256: `n-269-candidate.yaml` `35b1307a3a0dc2eb806ef064933c809a2f2b7eda73551bcc4ba6c411a307b5e6`; `n269-witness.json` `a1c4caab16d420112732566c45fd5910ba6713ce65ded0fcf8be6e6032c18ca3`.

## Rerun

```
cp n-269-candidate.yaml <squares>/packing/witnesses/known-best/zz-cand.yaml
cd <squares>/packing && uv run --frozen --no-dev --with sympy --with mpmath packing-witness verify witnesses/known-best/zz-cand.yaml
python3 verifier/sqcheck.py n-269-candidate.yaml      # needs mpmath, sympy, pyyaml
```

## How the exact coordinates were made

The search produced a decimal pose (centre and angle per square). The registry's own `packing-witness promote --strategy robust-rational` (jlevy/squares @ 0352d755, `center_dilation: '1'`, no dilation) turned it into these exact rational corners. Every pair is separated by at least about 2e-13: that margin is the decimal pose's own, left by the final f64 repair scaling of Evan Daniel's quench (about 1e-13 relative), rounded to 36 digits. The promotion puts the packing's least corner coordinates at 0 and takes the side as its greatest corner coordinate, so the squares that set the left wall, the bottom wall and the side touch them exactly; other squares near a wall clear it by up to about 1e-12. The witness's `source.path` and `certificate.replay` name this repository's files. `sqcheck.py` also certified the decimal pose itself in interval arithmetic before promotion.

## What differs from the registry packing

Squares matched by assignment up to the symmetries of the square: 261 of 269 centres move by more than 1e-3, 137 by more than 0.05 (largest 1.879); 121 squares are re-tilted by more than 1° (largest 44.4°); the packing has 45 squares tilted by more than 0.5° against the record's 100.

## Lineage, credit and AI assistance

The registry's n = 269 packing is Doğa Özden (found_by; our issue #947), a packing found by transplanting Evan Daniel's n = 304 packing (T-290). Found by an AI-run column-band designer, new for this filing; no donor packing is used. Tilted squares stand in columns across a band along the diagonal, at unit pitch along it, each column a stack of 1 to 3 squares sliding on its own; the axis-parallel squares sit on the two wall-anchored staircase lattices; for a side fraction f and a band angle of 45° minus delta, an exact dynamic programme over the columns maximises the number of squares (tolerance 0: a valid packing of that many squares at side k0 + f). The best design (nt tilted squares, column offset ox, diagonal variant) is quenched once with Evan Daniel's ALM+SLP code from [evand/square-packing](https://github.com/evand/square-packing) (`search/packer`, MIT, built from bb4cc78e), and random kicks of the packing's coordinates with a further quench follow. This packing was found from a designer packing with no registry packing as a seed: design f = 0.913469, band angle 42.8° (delta 2.2°), tolerance 0, 45 tilted squares, column offset 0.96875, diagonal variant 14, quenched once to 16.890507465412 (11 s into a local run of the cloud job b2h269's command line). Fq kicks of that packing then lowered it: a kick of sigma 0.0222 and a quench gave 16.889734433328, and a further kick of the best packings so far (sigma 0.001007) gave the filed side 16.889730073596, 5 s into the kick run. (The cloud job b2h269 itself reached 16.88973007359575 by a kick, sigma 0.0265, of a parent at 16.890507620785 at 210 s, but its pack file was lost to an infrastructure fault before it could be copied, so the filed packing is the local re-find, which has the same structure and a side 9e-14 higher.) The filed packing has 45 tilted squares (the registry record has 100): one band at about 42.1° and a small cluster of squares at about -44.9° at the upper-right end. Credit the improvement to Doğa Özden, the band's source packing and the current record to their holders as the registry lists them, and the local optimizer to Evan Daniel. His MIT notice is kept in `LICENSE-evand-square-packing.txt`.

The search was AI-assisted throughout (an AI agent wrote and ran the search and the checks); the checks above were run by code that did not produce the packing. Doğa directed the work.

## Other public values

The best public Kaggle per-puzzle packing we found for 269 has side 16.901513582205 (kirilltym; dataset refreshed 2026-11-11 03:32Z), above ours. The Kaggle per-puzzle leaderboard (staff notebook inversion/squares-in-squares-per-puzzle-leaderboard; cache of 2026-11-09 20:52Z) lists a side-only entry for n = 269: **16.889730079125**, team elegans, 2026-11-05. It is unpublished and states no packing, so we cannot verify it and make no claim about its method. **Our certified exact side is below it: 16.889730073595636 vs 16.889730079125, by 5.53e-9** (claim 16.889730073596). The cache is from 2026-11-09 20:52Z, so a later entry may be lower. Ours is also 1.13e-2 below the registry record (our own #947, T-290), 9.74e-3 below our own #962 (16.899469075856, T-296 in the registry's draft adoption PR #966), and 1.18e-2 below the best public packing we know of (16.901513582205, kirilltym): a published packing with a certificate whose side is below the leaderboard's side-only entry.
