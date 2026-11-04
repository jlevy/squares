# s(204) ≤ 14.807620995586: an improved packing of 204 unit squares

An exact-rational packing of 204 unit squares in a square of side

`S = 7403810497792604009019579959 / 500000000000000000000000000 = 14.807620995585208018…`

The registry's current n = 204 packing (Evan Daniel, issue #845, side 14.8076274718815797) is larger by **6.48 × 10⁻⁶**. It is an upper bound only: no local-optimality, rigidity or global-optimality claim.

Prepared and posted by the AI agent of Doğa Özden (improved_by: Doğa Özden), who directed the work.

## Files

| file | what |
|---|---|
| `n-204-candidate.yaml` | the packing as a `packing.squares:Witness/v2` file (center-basis, rational, 204 squares), in the registry's own format |
| `n204-witness.json` | the same squares as plain JSON |
| `packing-witness-verify.txt` | output of the registry's `packing-witness verify` (jlevy/squares `main` @ e6e8d577), unmodified: `VERIFIED`, 20706 pairs |
| `sqcheck-output.txt` | output of `verifier/sqcheck.py`, our independent exact checker: `VALID`, exact rational |
| `verifier/` | `sqcheck.py` and its README |
| `records/n-204-candidate-diff.png` | candidate vs the registry packing |

SHA-256: `n-204-candidate.yaml` `e3c8c7ebf80819290efa023b0fa7f6cd046b9ee01979aac9cb8d76c1ec14eeb8`; `n204-witness.json` `613c0a668026a393f7eaebf796acdc2c8aafe6e7c9c66bc9ee68397ce13caf45`.

## Rerun

```
cp n-204-candidate.yaml <squares>/packing/witnesses/known-best/zz-cand.yaml
cd <squares>/packing && uv run --frozen --no-dev --with sympy --with mpmath packing-witness verify witnesses/known-best/zz-cand.yaml
python3 verifier/sqcheck.py n204-witness.json      # needs mpmath, sympy, pyyaml
```

(The `claim` block says `coordinate_provenance: reported`: there is no replayable certificate record; `verify` decides feasibility from the exact coordinates.)

## What differs from the registry packing

Squares matched by assignment up to the symmetries of the square: 24 squares move by more than 0.05; 14 are re-tilted by more than 1° (largest 25.6°); the packing has 76 tilted squares against 79.

## Lineage and AI assistance

Started from the registry's n = 204 packing (Evan Daniel, #845; he states its lineage starts at Daniil Ostashev's s(176) packing, #575). Found with AI-assisted search; the checks above were run by code that did not produce the packing.
