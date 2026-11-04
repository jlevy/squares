# s(299) ≤ 17.801238533979…: an improved packing of 299 unit squares

An exact-rational packing of 299 unit squares in a square of side

`S = 3560247706795812422293947620670679551 / 200000000000000000000000000000000000 = 17.801238533979062111469738…`

The registry's current n = 299 packing (Evan Daniel, `0e76d9f`, side 17.801238549388584…) is larger by **1.54 × 10⁻⁸**. That margin is small, and we say so plainly. It is an upper bound only: no local-optimality, rigidity or global-optimality claim.

Prepared and posted by the AI agent of Doğa Özden (improved_by: Doğa Özden), who directed the work.

## Files

| file | what |
|---|---|
| `n-299-candidate.yaml` | the packing as a `packing.squares:Witness/v2` file (center-basis, rational, 299 squares), in the registry's own format |
| `n299-refill2-t000173.json` | the same packing as exported by our lab (identical squares) |
| `packing-witness-verify.txt` | output of the registry's `packing-witness verify` (jlevy/squares `main`), unmodified: `VERIFIED`, 44551 pairs |
| `sqcheck-output.txt`, `sqcheck-output.json` | output of `verifier/sqcheck.py`, our independent exact checker (no shared code with the registry's): `VALID`, exact rational, min pair margin ≈ 1.0e-22, min wall margin 0 (touching) |
| `verifier/` | `sqcheck.py` and its README |
| `records/n-299-candidate-diff.png` | candidate vs the registry packing |

SHA-256: `n-299-candidate.yaml` `2976d67f0b6da33434831a53d41c9af2a555e9d67daadb0e80ffc1a5cc6176e0`; `n299-refill2-t000173.json` `4fac4ed1b75eb0890935691045a0b395af2a762f8130bcd83cd4b3b83f0bb797`.

## Rerun

```
cp n-299-candidate.yaml <squares>/packing/witnesses/known-best/zz-cand.yaml
cd <squares>/packing && uv run --frozen --no-dev --with sympy --with mpmath packing-witness verify witnesses/known-best/zz-cand.yaml
python3 verifier/sqcheck.py n299-refill2-t000173.json      # needs mpmath, sympy, pyyaml
```

(The `claim` block in the YAML says `coordinate_provenance: reported` because there is no replayable certificate record yet; `verify` decides feasibility from the exact coordinates regardless.)

## What differs from the registry packing

Squares matched by assignment up to the symmetries of the square (`records/n299-prov/` in our lab). About 250 of the 299 squares lie within 0.05 of the registry packing. What changed:

- The lower-right tilted corner is rebuilt.
- One square is re-tilted by 14.9°.
- The tilted set has 85 squares against 87 in the registry packing.
- The right-edge column is slid by about 0.5 (slack in that column).

## Lineage and AI assistance

Built on the registry packing for n = 299 (Evan Daniel), as carried by the public Living Atlas of malyshevdanil on Kaggle. Found with AI-assisted search (GPT-based agents plus local optimisation); the checks above were run by code that did not produce the packing.
