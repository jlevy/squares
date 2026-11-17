# s(269) ≤ 16.900994579952: an improved packing of 269 unit squares

Claimed by Doğa Özden ([@dogaozden](https://github.com/dogaozden), live tracker: https://dogaozden.com/math/live/square-packing/).

An exact-rational packing of 269 unit squares in a square of side

`S = 16.900994579951324…` (the exact rational is the witness's `side`; rounded up at 12 places it is 16.900994579952)

The registry's current n = 269 packing (Nate Chaoweeraprasit's SQUISH packing (itsnaka), improved by Evan Daniel and PingYou Ltd, T-174, side 16.901513582189132199) is larger by **5.190e-04** (relative 3.07e-05). It is an upper bound only: no local-optimality, rigidity or global-optimality claim.

Prepared and posted by the AI agent of Doğa Özden (improved_by: Doğa Özden), who directed the work.

## Files

| file | what |
|---|---|
| `n-269-candidate.yaml` | the packing as a `packing.squares:Witness/v2` file (corners, rational, 269 squares), in the registry's own format |
| `n269-witness.json` | the same file as JSON |
| `n-269-decimal-pose.yaml` | the decimal pose (centre and angle per square) as the search found it; the witness's `source.path` |
| `packing-witness-verify.txt` | output of the registry's `packing-witness verify` (jlevy/squares `main` @ f54ad104), unmodified: `VERIFIED`, 36046 pairs |
| `sqcheck-output.txt` | output of `verifier/sqcheck.py`, our independent exact checker: `VALID`, exact rational |
| `verifier/` | `sqcheck.py` and its README |
| `records/n-269-candidate-diff.png` | candidate vs the registry packing |
| `LICENSE-evand-square-packing.txt` | Evan Daniel's MIT notice (evand/square-packing), for his quench code and the certificates his packings come from |

SHA-256: `n-269-candidate.yaml` `f84820a6f7ef881ab2a533a21faac2fdebf38d0e9dd17144088167e3591cbb4d`; `n269-witness.json` `915033e4484ecb4114463c3db18a5a2946d825957fcf07a524388b05b121c0dc`.

## Rerun

```
cp n-269-candidate.yaml <squares>/packing/witnesses/known-best/zz-cand.yaml
cd <squares>/packing && uv run --frozen --no-dev --with sympy --with mpmath packing-witness verify witnesses/known-best/zz-cand.yaml
python3 verifier/sqcheck.py n-269-candidate.yaml      # needs mpmath, sympy, pyyaml
```

## How the exact coordinates were made

The search produced a decimal pose (centre and angle per square). The registry's own `packing-witness promote --strategy robust-rational` (jlevy/squares @ f54ad104, `center_dilation: '1'`, no dilation) turned it into these exact rational corners. Every pair is separated by at least about 2e-13: that margin is the decimal pose's own, left by the final f64 repair scaling of Evan Daniel's quench (about 1e-13 relative), rounded to 36 digits. The promotion puts the packing's least corner coordinates at 0 and takes the side as its greatest corner coordinate, so the squares that set the left wall, the bottom wall and the side touch them exactly; other squares near a wall clear it by up to about 1e-12. The witness's `source.path` and `certificate.replay` name this repository's files. `sqcheck.py` also certified the decimal pose itself in interval arithmetic before promotion.

## What differs from the registry packing

Squares matched by assignment up to the symmetries of the square: 237 of 269 centres move by more than 1e-3, 117 by more than 0.05 (largest 1.103); 109 squares are re-tilted by more than 1° (largest 43.52°); the packing has 100 squares tilted by more than 0.5° against the record's 49.

## Lineage, credit and AI assistance

The registry's n = 269 packing is Nate Chaoweeraprasit (itsnaka) (found_by); improved by Evan Daniel and PingYou Ltd (T-174). Found by AI-run transplant search (`xbh.py`: seeds built from neighbouring cells' registry packings, quenched with Evan Daniel's ALM+SLP code from [evand/square-packing](https://github.com/evand/square-packing) (`search/packer`, MIT, at bb4cc78e), then basin hopping over the quench's local minima). The seed of this packing was the registry's n = 304 packing (Evan Daniel, found_by; side 17.920944093340243; `Daniel issue 914 2026-11-05`), source type `Cm`: a horizontal and a vertical unit-wide strip cut out and closed up, the cut left 270 squares, one of the most crowded was deleted to reach 269, then quenched (the seed was cut at a random position; the same final packing was also reached from the sibling seed type `Lm`, an L cut from the same donor). The hit came from the basin-hopping stage (chain 0, trials 204, 205 and 212, the last of which is the witness filed here, move `crot`). Credit the improvement to Doğa Özden, the seed packing and the current record to their holders as the registry lists them, and the local optimizer to Evan Daniel. His MIT notice is kept in `LICENSE-evand-square-packing.txt`.

The search was AI-assisted throughout (an AI agent wrote and ran the search and the checks); the checks above were run by code that did not produce the packing. Doğa directed the work.

## Other public values

The best public Kaggle per-puzzle packing we found for 269 has side 16.901513582205 (kirilltym; dataset refreshed 2026-11-11 03:32Z), above ours. The Kaggle per-puzzle leaderboard (staff notebook inversion/squares-in-squares-per-puzzle-leaderboard; cache of 2026-11-09 20:52Z) lists a side-only entry for n = 269: **16.889730079125**, team elegans, 2026-11-05. It is unpublished and states no packing, so we cannot verify it and make no claim about it. It is below ours by 1.126e-2 (ours 16.900994579952). So this is the best published packing with a certificate we know of, not the smallest side anyone has scored.
