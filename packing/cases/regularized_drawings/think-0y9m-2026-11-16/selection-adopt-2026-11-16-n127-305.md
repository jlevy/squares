| n | view | side - U | side - drawn | light / uneven / near-axis / classes / hues | house / stage sides | better on |
| --- | --- | --- | --- | --- | --- | --- |
| 127 | grid:adopt-2026-11-16-n127-305-grid-deg1 | 0 | 0 | 17 / 23 / 24 / 44 / 19 -> 1 / 2 / 0 / 18 / 18 | 107 / 227 -> 244 / 290 | light_axis, uneven_axis, near_axis, classes, hues, house_total, stage_total |
| 204 | grid:adopt-2026-11-16-n127-305-grid-deg5 | 0 | 0 | 15 / 47 / 9 / 35 / 19 -> 2 / 5 / 0 / 25 / 19 | 312 / 465 -> 409 / 491 | light_axis, uneven_axis, near_axis, classes, house_total, stage_total |
| 232 | grid:adopt-2026-11-16-n127-305-grid-deg05 | 0 | 0 | 8 / 37 / 4 / 29 / 19 -> 4 / 28 / 0 / 25 / 19 | 575 / 602 -> 598 / 608 | light_axis, uneven_axis, near_axis, classes, house_total, stage_total |
| 264 | grid:adopt-2026-11-16-n127-305-grid-deg1 | 0 | 0 | 37 / 96 / 25 / 65 / 19 -> 4 / 28 / 0 / 39 / 19 | 453 / 719 -> 697 / 723 | light_axis, uneven_axis, near_axis, classes, house_total, stage_total |
| 305 | grid:adopt-2026-11-16-n127-305-grid-deg05 | 0 | 0 | 72 / 100 / 47 / 109 / 19 -> 2 / 13 / 0 / 67 / 19 | 391 / 786 -> 787 / 869 | light_axis, uneven_axis, near_axis, classes, house_total, stage_total |

5 counts chosen; 0 with no adoptable view (the JSON report gives each candidate's reasons).

Register candidates (policy row 3; registered first, never admitted here):

| n | view | side - U |
| --- | --- | --- |
| 127 | evand:adopt-2026-11-16-n127-305-evand:solved | -1.22e-10 |
| 232 | evand:adopt-2026-11-16-n127-305-evand:solved | -4.02e-09 |
| 264 | evand:adopt-2026-11-16-n127-305-evand:solved | -1.91e-11 |
| 305 | evand:adopt-2026-11-16-n127-305-evand:solved | -1.91e-10 |

```bash
python -m devtools.regularize_evand layer --run-dir "$(mktemp -d)" --repo-root .. --grid-run /tmp/claude-0/-home-user-squares/0a01ddbe-91e2-5d1d-98f8-365093a10337/scratchpad/l187-runs/adopt-2026-11-16-n127-305-grid-deg05 --grid-counts 232 305
python -m devtools.regularize_evand layer --run-dir "$(mktemp -d)" --repo-root .. --grid-run /tmp/claude-0/-home-user-squares/0a01ddbe-91e2-5d1d-98f8-365093a10337/scratchpad/l187-runs/adopt-2026-11-16-n127-305-grid-deg1 --grid-counts 127 264
python -m devtools.regularize_evand layer --run-dir "$(mktemp -d)" --repo-root .. --grid-run /tmp/claude-0/-home-user-squares/0a01ddbe-91e2-5d1d-98f8-365093a10337/scratchpad/l187-runs/adopt-2026-11-16-n127-305-grid-deg5 --grid-counts 204
```
