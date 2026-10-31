| n | view | side - U | side - drawn | light / uneven / near-axis / classes / hues | house / stage sides | better on |
| --- | --- | --- | --- | --- | --- | --- |
| 130 | grid:adopt-2026-10-31-n130-307-grid-deg5 | 0 | 0 | 4 / 22 / 0 / 16 / 16 -> 2 / 4 / 0 / 15 / 15 | 321 / 348 -> 346 / 352 | light_axis, uneven_axis, classes, hues, house_total, stage_total |
| 172 | grid:adopt-2026-10-31-n130-307-grid-deg5 | 0 | 0 | 0 / 11 / 7 / 29 / 20 -> 0 / 0 / 0 / 21 / 20 | 426 / 492 -> 467 / 505 | uneven_axis, near_axis, classes, house_total, stage_total |
| 204 | grid:adopt-2026-10-31-n130-307-grid-deg5 | 0 | 0 | 13 / 66 / 3 / 29 / 19 -> 3 / 4 / 0 / 22 / 19 | 374 / 496 -> 489 / 515 | light_axis, uneven_axis, near_axis, classes, house_total, stage_total |
| 232 | grid:adopt-2026-10-31-n130-307-grid-deg1 | 0 | 0 | 9 / 25 / 1 / 20 / 19 -> 9 / 22 / 0 / 18 / 18 | 525 / 569 -> 534 / 572 | uneven_axis, near_axis, classes, hues, house_total, stage_total |
| 260 | grid:adopt-2026-10-31-n130-307-grid-deg05 | 0 | 0 | 14 / 69 / 6 / 32 / 19 -> 3 / 37 / 0 / 26 / 19 | 510 / 606 -> 582 / 630 | light_axis, uneven_axis, near_axis, classes, house_total, stage_total |
| 293 | grid:adopt-2026-10-31-n130-307-grid-deg05 | 0 | 0 | 16 / 109 / 6 / 32 / 19 -> 5 / 78 / 0 / 26 / 19 | 589 / 685 -> 669 / 709 | light_axis, uneven_axis, near_axis, classes, house_total, stage_total |

6 counts chosen; 2 with no adoptable view (the JSON report gives each candidate's reasons).

Register candidates (policy row 3; registered first, never admitted here):

| n | view | side - U |
| --- | --- | --- |
| 130 | evand:adopt-2026-10-31-n130-307-evand:solved | -2.50e-13 |
| 307 | evand:adopt-2026-10-31-n130-307-evand:solved | -3.75e-12 |

```bash
python -m devtools.regularize_evand layer --run-dir "$(mktemp -d)" --repo-root .. --grid-run /tmp/claude-0/-home-user-squares/0a01ddbe-91e2-5d1d-98f8-365093a10337/scratchpad/regularize/adopt-2026-10-31-n130-307-grid-deg05 --grid-counts 260 293
python -m devtools.regularize_evand layer --run-dir "$(mktemp -d)" --repo-root .. --grid-run /tmp/claude-0/-home-user-squares/0a01ddbe-91e2-5d1d-98f8-365093a10337/scratchpad/regularize/adopt-2026-10-31-n130-307-grid-deg1 --grid-counts 232
python -m devtools.regularize_evand layer --run-dir "$(mktemp -d)" --repo-root .. --grid-run /tmp/claude-0/-home-user-squares/0a01ddbe-91e2-5d1d-98f8-365093a10337/scratchpad/regularize/adopt-2026-10-31-n130-307-grid-deg5 --grid-counts 130 172 204
```
