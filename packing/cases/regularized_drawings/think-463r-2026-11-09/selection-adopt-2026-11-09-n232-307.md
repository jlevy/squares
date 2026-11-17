| n | view | side - U | side - drawn | light / uneven / near-axis / classes / hues | house / stage sides | better on |
| --- | --- | --- | --- | --- | --- | --- |
| 232 | grid:adopt-2026-11-09-n232-307-grid-deg05 | 0 | 0 | 18 / 86 / 9 / 36 / 19 -> 4 / 14 / 0 / 27 / 19 | 395 / 550 -> 538 / 572 | light_axis, uneven_axis, near_axis, classes, house_total, stage_total |
| 268 | grid:adopt-2026-11-09-n232-307-grid-deg5 | 0 | 0 | 11 / 77 / 12 / 40 / 19 -> 0 / 0 / 0 / 27 / 19 | 492 / 677 -> 653 / 723 | light_axis, uneven_axis, near_axis, classes, house_total, stage_total |
| 299 | grid:adopt-2026-11-09-n232-307-grid-deg1 | 0 | 0 | 28 / 57 / 22 / 52 / 19 -> 5 / 11 / 1 / 29 / 19 | 586 / 739 -> 771 / 829 | light_axis, uneven_axis, near_axis, classes, house_total, stage_total |
| 303 | grid:adopt-2026-11-09-n232-307-grid-deg05 | 0 | 0 | 61 / 137 / 19 / 59 / 19 -> 0 / 0 / 0 / 40 / 19 | 374 / 769 -> 734 / 814 | light_axis, uneven_axis, near_axis, classes, house_total, stage_total |

4 counts chosen; 1 with no adoptable view (the JSON report gives each candidate's reasons).

Register candidates (policy row 3; registered first, never admitted here):

| n | view | side - U |
| --- | --- | --- |
| 232 | evand:adopt-2026-11-09-n232-307-evand:solved | -3.37e-12 |
| 268 | evand:adopt-2026-11-09-n232-307-evand:solved | -3.30e-12 |
| 299 | evand:adopt-2026-11-09-n232-307-evand:solved | -3.53e-12 |
| 303 | evand:adopt-2026-11-09-n232-307-evand:solved | -3.48e-12 |
| 307 | evand:adopt-2026-11-09-n232-307-evand:solved | -3.48e-12 |

```bash
python -m devtools.regularize_evand layer --run-dir "$(mktemp -d)" --repo-root .. --grid-run /tmp/claude-0/-home-user-squares/0a01ddbe-91e2-5d1d-98f8-365093a10337/scratchpad/l63/runs/adopt-2026-11-09-n232-307-grid-deg05 --grid-counts 232 303
python -m devtools.regularize_evand layer --run-dir "$(mktemp -d)" --repo-root .. --grid-run /tmp/claude-0/-home-user-squares/0a01ddbe-91e2-5d1d-98f8-365093a10337/scratchpad/l63/runs/adopt-2026-11-09-n232-307-grid-deg1 --grid-counts 299
python -m devtools.regularize_evand layer --run-dir "$(mktemp -d)" --repo-root .. --grid-run /tmp/claude-0/-home-user-squares/0a01ddbe-91e2-5d1d-98f8-365093a10337/scratchpad/l63/runs/adopt-2026-11-09-n232-307-grid-deg5 --grid-counts 268
```
