| n | view | side - U | side - drawn | light / uneven / near-axis / classes / hues | house / stage sides | better on |
| --- | --- | --- | --- | --- | --- | --- |
| 102 | grid:mbdw-2026-10-26-grid-deg05 | -3.19e-61 | 0 | 4 / 11 / 2 / 4 / 4 -> 2 / 4 / 0 / 3 / 3 | 254 / 272 -> 268 / 272 | light_axis, uneven_axis, near_axis, classes, hues, house_total |
| 123 | grid:mbdw-2026-10-26-grid-deg05 | -4.27e-62 | 0 | 3 / 30 / 2 / 5 / 5 -> 1 / 16 / 0 / 3 / 3 | 305 / 312 -> 325 / 329 | light_axis, uneven_axis, near_axis, classes, hues, house_total, stage_total |
| 153 | grid:mbdw-2026-10-26-grid-deg05 | -3.25e-61 | 0 | 0 / 0 / 0 / 3 / 3 -> 0 / 0 / 0 / 3 / 3 | 446 / 446 -> 474 / 474 | house_total, stage_total |
| 207 | grid:mbdw-2026-10-26-grid-deg05 | +1.92e-61 | 0 | 0 / 0 / 0 / 3 / 3 -> 0 / 0 / 0 / 3 / 3 | 640 / 640 -> 662 / 662 | house_total, stage_total |
| 258 | grid:mbdw-2026-10-26-grid-deg05 | +4.32e-62 | 0 | 1 / 3 / 1 / 5 / 5 -> 1 / 2 / 0 / 4 / 4 | 763 / 766 -> 766 / 766 | uneven_axis, near_axis, classes, hues, house_total |
| 259 | grid:mbdw-2026-10-26-grid-deg05 | -4.27e-62 | 0 | 111 / 163 / 26 / 44 / 19 -> 4 / 20 / 0 / 20 / 19 | 264 / 678 -> 777 / 787 | light_axis, uneven_axis, near_axis, classes, house_total, stage_total |
| 302 | grid:mbdw-2026-10-26-grid-deg5 | -2.98e-61 | 0 | 142 / 204 / 29 / 56 / 19 -> 0 / 0 / 0 / 27 / 19 | 284 / 948 -> 960 / 962 | light_axis, uneven_axis, near_axis, classes, house_total, stage_total |

7 counts chosen; 0 with no adoptable view (the JSON report gives each candidate's reasons).

```bash
python -m devtools.regularize_evand layer --run-dir "$(mktemp -d)" --repo-root .. --grid-run $RUNS/mbdw-2026-10-26-grid-deg05 --grid-counts 102 123 153 207 258 259
python -m devtools.regularize_evand layer --run-dir "$(mktemp -d)" --repo-root .. --grid-run $RUNS/mbdw-2026-10-26-grid-deg5 --grid-counts 302
```
