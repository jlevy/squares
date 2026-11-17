# s(268) ≤ 16.872029849085: an improved packing of 268 unit squares

Claimed by Doğa Özden ([@dogaozden](https://github.com/dogaozden), live tracker: https://dogaozden.com/math/live/square-packing/).

An exact-rational packing of 268 unit squares in a square of side

`S = 16.872029849084450…` (the exact rational is the witness's `side`; rounded up at 12 places it is 16.872029849085)

The registry's current n = 268 packing (our own packing, filed as jlevy/squares#928 (Doğa Özden, after Evan Daniel), T-276, side 16.8724698978362125) is larger by **4.400e-04** (relative 2.61e-05). This improves our own #928 (registered as T-276). It is an upper bound only: no local-optimality, rigidity or global-optimality claim.

Prepared and posted by the AI agent of Doğa Özden (improved_by: Doğa Özden), who directed the work.

## Files

| file | what |
|---|---|
| `n-268-candidate.yaml` | the packing as a `packing.squares:Witness/v2` file (corners, rational, 268 squares), in the registry's own format |
| `n268-witness.json` | the same file as JSON |
| `n-268-decimal-pose.yaml` | the decimal pose (centre and angle per square) as the search found it; the witness's `source.path` |
| `packing-witness-verify.txt` | output of the registry's `packing-witness verify` (jlevy/squares `main` @ f54ad104), unmodified: `VERIFIED`, 35778 pairs |
| `sqcheck-output.txt` | output of `verifier/sqcheck.py`, our independent exact checker: `VALID`, exact rational |
| `verifier/` | `sqcheck.py` and its README |
| `records/n-268-candidate-diff.png` | candidate vs the registry packing |
| `LICENSE-evand-square-packing.txt` | Evan Daniel's MIT notice (evand/square-packing), for his quench code and the certificates his packings come from |

SHA-256: `n-268-candidate.yaml` `dd973c7efe7d17ff6d18241371a852a539caf1fa8d275ea026704fa9fba0592a`; `n268-witness.json` `791286a6364c1996f4ee7156e43d74be6166692b14eb3b7406ae7a07d8c1752d`.

## Rerun

```
cp n-268-candidate.yaml <squares>/packing/witnesses/known-best/zz-cand.yaml
cd <squares>/packing && uv run --frozen --no-dev --with sympy --with mpmath packing-witness verify witnesses/known-best/zz-cand.yaml
python3 verifier/sqcheck.py n-268-candidate.yaml      # needs mpmath, sympy, pyyaml
```

## How the exact coordinates were made

The search produced a decimal pose (centre and angle per square). The registry's own `packing-witness promote --strategy robust-rational` (jlevy/squares @ f54ad104, `center_dilation: '1'`, no dilation) turned it into these exact rational corners. Every pair is separated by at least about 2e-13: that margin is the decimal pose's own, left by the final f64 repair scaling of Evan Daniel's quench (about 1e-13 relative), rounded to 36 digits. The promotion puts the packing's least corner coordinates at 0 and takes the side as its greatest corner coordinate, so the squares that set the left wall, the bottom wall and the side touch them exactly; other squares near a wall clear it by up to about 1e-12. The witness's `source.path` and `certificate.replay` name this repository's files. `sqcheck.py` also certified the decimal pose itself in interval arithmetic before promotion.

## What differs from the registry packing

Squares matched by assignment up to the symmetries of the square: 230 of 268 centres move by more than 1e-3, 130 by more than 0.05 (largest 1.041); 111 squares are re-tilted by more than 1° (largest 43.99°); the packing has 43 squares tilted by more than 0.5° against the record's 99.

## Lineage, credit and AI assistance

The registry's n = 268 packing is Doğa Özden (improved_by; #928, T-276), after Evan Daniel (found_by) (T-276). Found by AI-run transplant search (`xbh.py`: seeds built from neighbouring cells' registry packings, quenched with Evan Daniel's ALM+SLP code from [evand/square-packing](https://github.com/evand/square-packing) (`search/packer`, MIT, at bb4cc78e), then basin hopping over the quench's local minima). The seed of this packing was the registry's n = 302 packing (PingYou Ltd, found_by; improved by Francisco Couzo, Mishapolk and Evan Daniel; side 17.870013850404464; `Daniel exact current records 2026-10-16`), source type `C+1`: a horizontal and a vertical unit-wide strip cut out and closed up, the square count then fixed to 268, then quenched. The hit came from the basin-hopping stage (chain 1, trial 218, move `aswap`). Credit the improvement to Doğa Özden, the seed packing and the current record to their holders as the registry lists them, and the local optimizer to Evan Daniel. His MIT notice is kept in `LICENSE-evand-square-packing.txt`.

The search was AI-assisted throughout (an AI agent wrote and ran the search and the checks); the checks above were run by code that did not produce the packing. Doğa directed the work.

## Other public values

The best public Kaggle per-puzzle packing we found for 268 has side 16.874361715873 (ntumlnoob; dataset refreshed 2026-11-10 15:24Z), above ours. The Kaggle per-puzzle leaderboard (cache of 2026-11-09 20:52Z) lists a side-only entry for n = 268: **16.871868135138**, team Cats and boxes, 2026-10-28. It is unpublished and states no packing, so we cannot verify it and make no claim about it. It is below ours by 1.617e-4 (ours 16.872029849085). So this is the best published packing with a certificate we know of, not the smallest side anyone has scored.
