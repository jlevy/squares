# G4 n=11 191/50 Seventeen-Direction Threshold-Atom Receipt

Status: **unresolved**. This is not a scientific freeze.
`candidate_created` is false.
The 181-net was not run (`--direction-steps 16`).

Session-139 G4 producer on `(n, L, B, net) = (11, 191/50, 9977/10000, 17
directions)` at `--grid-counts 10,14,18` with six atom rounds and eight row
rounds. Wall 32.4 s.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.produce_threshold_certificate \
  --n 11 --outer-side 191/50 --square-side 9977/10000 \
  --grid-counts 10,14,18 --direction-steps 16 --angle-limit 207107/500000 \
  --max-atom-rounds 6 --max-row-rounds 8 \
  --output-dir campaign/series/series-000-smoke-and-calibration/results/agenda-037/g4-n11-191-50-net17
```

## Covering

| Quantity | Value |
| --- | --- |
| Status | unresolved |
| Finished objective | `11.449456701` |
| Atom orbits | 48 |
| Rows | 459 |
| Sites / site orbits | 612 / 86 |
| Seconds | 32.431 |
| Covering below 11 | no |
| Seed stopped | round limit 8 reached |

On the 203 seed rows the atom loop dropped below 11 from `atoms-1` (`10.874023`)
through `atoms-5` (`9.636364`). Eight row rounds then restored mass, crossing 11
at `rows-2` (`11.146979`) and finishing at `11.449457` on 459 rows. Same shape as
the 9-direction 456-site run: threshold atoms overfit the seed rows; added
placement rows bring the covering back above 11.

Artifacts in this directory: `receipt.json`, `trajectory.json`, `atoms.json`,
`producer.log`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
