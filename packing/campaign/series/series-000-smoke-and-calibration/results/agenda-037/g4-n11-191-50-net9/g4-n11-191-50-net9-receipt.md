# G4 n=11 191/50 Nine-Direction Threshold-Atom Receipt

Status: **unresolved**. This is not a scientific freeze.
`candidate_created` is false.
The 181-net was not run (`--direction-steps 8`).

Session-139 G4 producer on `(n, L, B, net) = (11, 191/50, 9977/10000, 9
directions)` at `--grid-counts 8,12,16`. First attempt logged within the 120 s watchdog
and exited 0 in 12.2 s. No retry.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.produce_threshold_certificate \
  --n 11 --outer-side 191/50 --square-side 9977/10000 \
  --grid-counts 8,12,16 --direction-steps 8 --angle-limit 207107/500000 \
  --max-atom-rounds 4 --max-row-rounds 2 \
  --output-dir campaign/series/series-000-smoke-and-calibration/results/agenda-037/g4-n11-191-50-net9
```

## Covering

| Quantity | Value |
| --- | --- |
| Status | unresolved |
| Finished objective | `11.610187542` |
| Atom orbits | 30 |
| Rows | 155 |
| Sites / site orbits | 456 / 65 |
| Seconds | 12.152 |
| Covering below 11 | no |
| Seed stopped | round limit 8 reached |

The finished covering is not below 11. On the 119 seed rows the atom loop did drop below
11 (`atoms-1` `10.649351`, `atoms-2` `10.279720`, `atoms-3` `9.968931`). The two row
rounds then restored mass to `11.299091` (137 rows) and `11.610188` (155 rows).
That dip is a covering of the seed rows only.

Artifacts in this directory: `receipt.json`, `trajectory.json`, `atoms.json`,
`producer.log`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
