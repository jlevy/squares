# n=19 97/20 T-020-Seeded Window-6 Lattice Covering Receipt

Status: **site set refuted, unconverged**. The side stays open.

Session-139 probe: BC-197 auto `(34, 45, 56)` unioned with T-020's 2260 atom
sites scaled from `24/5` to `97/20`, plus `--seed-windows 6`,
`(n, L, B, net) = (19, 97/20, 9977/10000, 181 directions)`.
Seed from the immutable `certificate-24-5.json`, not T-021's moving
`certificate.json`. Seed sites 2836 = 2260 T-020 plus 576 ceiling-window
lattice sites. The 900 s deadline stopped the row loop after 34 LP rounds
at `19.808958` (321 still violated). Crossed nineteen at round 5
(`19.114379`) and climbed. Remaining rows can only raise this value.
Adding sites can still lower it, so `97/20` is not barred for n=19.
T-020 at `24/5` is unchanged. T-021's n=20 certificate is untouched.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 19 --side 97/20 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 34,45,56 --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 900 \
  --seed-certificate cases/n20_fractional_certificate/certificate-24-5.json --seed-map scale \
  --seed-windows 6 \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-037/n19-97-20-t020-windows6-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-037/n19-97-20-t020-windows6-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-037/n19-97-20-t020-windows6-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n19-97-20-t020-windows6-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n19-97-20-t020-windows6.log
```

No freeze file: the 900 s deadline stopped the row loop after 34 rounds.
Wall 953.1 s.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `19.808958` |
| Sites / orbits / rows | 8865 / 1172 / 11546 |
| Seed sites | 2836 |
| LP rounds | 34 |
| Crossing | round 5 (`19.114379`) |
| Wall | 953.1 s |
| `least_covered` | 0.974389 |
| Converged | no (`violated == 321` at stop) |

`devtools.decide_certificate` was not run: the mass is not below 19.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
