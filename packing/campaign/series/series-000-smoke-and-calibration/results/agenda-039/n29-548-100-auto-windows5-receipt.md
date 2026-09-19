# n=29 548/100 Seedless Auto Window-5 Covering Receipt

Status: **site set still open**. Covering converged below 29. `declare_least_cell_mass`
accepted. `decide_certificate` refused the interval route. T-030 was not offered.

Session-141 exp-171: seedless auto grids plus `--seed-windows 5`,
`(n, L, B, net) = (29, 548/100, 9977/10000, 181 directions)`. Auto resolved to
`(39, 53, 65)`. Seed sites 625 (windows only). The row loop converged at LP
round 52 (violated 0) at `26.040745` on 9145 sites / 1230 orbits. Freeze mass
`52081879/2000000 = 26.0409395`. 1329 atoms. Never crossed 29.

Declare accepted least cell mass `4000013/4000000`.
Decide interval: `accepted=False`, enclosure
`(398409/400000, 4000013/4000000)`, 4,960,181 boxes, 272 stalled (65 s).
Condition 5 refused. The enclosure has width. Exact route did not run.
`EXIT:1`. Not `RETAINABLE`.

This is the first first-party covering row at n=29, and the first Nagamochi
freeze with mass `< n`. A freeze that the interval route refuses is not a
verified floor. Do not more-wall this set. Nagamochi `1 + sqrt(20)` stands.
H-220 stays unconfirmed.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 29 --side 548/100 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts auto --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 1200 \
  --seed-windows 5 \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-039/n29-548-100-auto-windows5-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-039/n29-548-100-auto-windows5-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-039/n29-548-100-auto-windows5-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-039/n29-548-100-auto-windows5-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-039/n29-548-100-auto-windows5.log
```

Covering wall 1068.7 s. Declare ~45 s (`11:45:12Z`–`11:45:57Z`). Decide 66 s
(`11:51:17Z`–`11:52:23Z`).

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `26.040745` |
| Freeze mass | `52081879/2000000` = 26.0409395 |
| Sites / orbits / rows | 9145 / 1230 / 14722 |
| Seed sites | 625 |
| Auto grids | `(39, 53, 65)` |
| LP rounds | 52 |
| Atoms | 1329 |
| Crossing | none |
| Wall | 1068.7 s |
| `least_covered` | 1 |
| Converged | yes (`violated == 0`) |

## Decide

| Quantity | Value |
| --- | --- |
| Declare | accepted; least `4000013/4000000` |
| Interval | refused; 272 stalled; Condition 5 |
| Enclosure | `(398409/400000, 4000013/4000000)` |
| Boxes | 4,960,181 |
| Exact | not run |
| Verdict | not `RETAINABLE` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
