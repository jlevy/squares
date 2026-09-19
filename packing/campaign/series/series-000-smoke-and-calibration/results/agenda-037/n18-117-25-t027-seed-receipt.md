# n=18 117/25 T-027-Seeded Covering Receipt

Status: **site set refuted, unconverged**. Locked at 18. The side stays open.

Session-139 probe: BC-191 auto `(32, 43, 54)` unioned with T-027's 769 atom
sites scaled from `467/100` to `117/25`,
`(n, L, B, net) = (18, 117/25, 9977/10000, 181 directions)`.
The T-019 seed at the same side converged with exact mass `18.000043`.
T-027's own atoms, which certified `467/100`, sat at `18.000000` from
round 7 through the 60-round limit (465 still violated) on 6549 sites /
868 orbits. Remaining rows can only raise this value. Adding sites can
still lower it, so `117/25` is not barred. T-027 at `467/100` is
unchanged.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 18 --side 117/25 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 32,43,54 --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 900 \
  --seed-certificate cases/n18_fractional_certificate/certificate.json --seed-map scale \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-037/n18-117-25-t027-seed-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n18-117-25-t027-seed-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n18-117-25-t027-seed.log
```

`--freeze` was not requested. The 60-round limit stopped the row loop;
no column-generation round ran. Wall 819.5 s.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `18.000000` |
| Sites / orbits / rows | 6549 / 868 / 19241 |
| Seed sites | 769 |
| LP rounds | 60 |
| Crossing | round 7 (`18.000000`) |
| Wall | 819.5 s |
| `least_covered` | 0.970596 |
| Converged | no (`violated == 465` at stop) |

`devtools.decide_certificate` was not run: the mass is not below 18.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
