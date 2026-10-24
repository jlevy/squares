| n | view | side - U | side - drawn | light / uneven / near-axis / classes / hues | house / stage sides | better on |
| --- | --- | --- | --- | --- | --- | --- |
| 268 | grid:adopt-2026-10-25-n268-303-grid-deg05 | 0 | 0 | 20 / 37 / 6 / 14 / 14 -> 5 / 19 / 0 / 9 / 9 | 676 / 729 -> 751 / 753 | light_axis, uneven_axis, near_axis, classes, hues, house_total, stage_total |
| 303 | grid:adopt-2026-10-25-n268-303-grid-deg05 | 0 | 0 | 14 / 28 / 8 / 27 / 19 -> 0 / 0 / 0 / 19 / 19 | 736 / 904 -> 848 / 904 | light_axis, uneven_axis, near_axis, classes, house_total |

2 counts chosen; 0 with no adoptable view (the JSON report gives each candidate's reasons).

Register candidates (policy row 3; registered first, never admitted here):

| n | view | side - U |
| --- | --- | --- |
| 268 | evand:adopt-2026-10-25-n268-303-evand:solved | -4.48e-12 |
| 303 | evand:adopt-2026-10-25-n268-303-evand:solved | -3.63e-12 |

```bash
python -m devtools.regularize_evand layer --run-dir "$(mktemp -d)" --repo-root .. --grid-run $RUNS/adopt-2026-10-25-n268-303-grid-deg05 --grid-counts 268 303
```
