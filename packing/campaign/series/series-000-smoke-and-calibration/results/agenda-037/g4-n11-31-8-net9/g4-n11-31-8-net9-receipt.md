# G4 n=11 31/8 Nine-Direction Threshold-Atom Receipt

Status: **unresolved**. This is not a scientific freeze.
`candidate_created` is false.
The 181-net was not run (`--direction-steps 8`).

Session-139 G4 producer on `(n, L, B, net) = (11, 31/8, 9977/10000, 9
directions)` at `--grid-counts 8,12,16`. Same round budget as the completed
`191/50` net9 run. Exited 0 in 3.8 s.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.produce_threshold_certificate \
  --n 11 --outer-side 31/8 --square-side 9977/10000 \
  --grid-counts 8,12,16 --direction-steps 8 --angle-limit 207107/500000 \
  --max-atom-rounds 4 --max-row-rounds 2 \
  --output-dir campaign/series/series-000-smoke-and-calibration/results/agenda-037/g4-n11-31-8-net9
```

## Covering

| Quantity | Value |
| --- | --- |
| Status | unresolved |
| Finished objective | `14.000000000` |
| Atom orbits | 32 |
| Rows | 156 |
| Sites / site orbits | 456 / 65 |
| Seconds | 3.849 |
| Covering below 11 | no |
| Seed stopped | round limit 8 reached |

The finished covering is not below 11. On the seed rows the atom loop did drop below
11 (`atoms-1` `10.666667`, `atoms-2` `10.500000`, `atoms-3` `10.172414`). The two row
rounds then restored mass to `11.909091` (138 rows) and `14.000000` (156 rows).
That dip is a covering of the seed rows only. Same overfit shape as `191/50` net9,
with a larger restore.

Artifacts in this directory: `receipt.json`, `trajectory.json`, `atoms.json`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
