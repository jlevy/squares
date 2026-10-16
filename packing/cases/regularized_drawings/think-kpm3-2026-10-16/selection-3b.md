| n | view | side - U | side - drawn | light / uneven / near-axis / classes / hues | house / stage sides | better on |
| --- | --- | --- | --- | --- | --- | --- |
| 153 | evand:3b-1016:same | 0 | 0 | 20 / 52 / 13 / 35 / 19 -> 0 / 0 / 0 / 10 / 10 | 283 / 400 -> 462 / 462 | light_axis, uneven_axis, near_axis, classes, hues, house_total, stage_total |
| 154 | grid:3b-deg5-1016 | 0 | 0 | 19 / 34 / 2 / 15 / 15 -> 4 / 9 / 0 / 12 / 12 | 356 / 390 -> 419 / 423 | light_axis, uneven_axis, near_axis, classes, hues, house_total, stage_total |
| 207 | evand:3b-1016:same | 0 | 0 | 0 / 0 / 1 / 5 / 5 -> 0 / 0 / 0 / 3 / 3 | 654 / 662 -> 662 / 662 | near_axis, classes, hues, house_total |
| 211 | evand:3b-1016:same | 0 | 0 | 2 / 12 / 6 / 30 / 19 -> 2 / 9 / 3 / 20 / 19 | 496 / 534 -> 524 / 549 | uneven_axis, near_axis, classes, house_total, stage_total |
| 237 | evand:3b-1016:same | 0 | 0 | 4 / 9 / 1 / 20 / 19 -> 4 / 8 / 0 / 18 / 18 | 678 / 682 -> 686 / 686 | uneven_axis, near_axis, classes, hues, house_total, stage_total |
| 241 | evand:3b-1016:solved | 0 | 0 | 0 / 0 / 0 / 27 / 19 -> 0 / 0 / 0 / 27 / 19 | 608 / 634 -> 610 / 636 | house_total, stage_total |
| 302 | evand:3b-1016:solved | 0 | 0 | 6 / 26 / 11 / 40 / 19 -> 0 / 0 / 0 / 14 / 14 | 882 / 952 -> 978 / 978 | light_axis, uneven_axis, near_axis, classes, hues, house_total, stage_total |

7 counts chosen; 1 with no adoptable view (the JSON report gives each candidate's reasons).

Register candidates (policy row 3; registered first, never admitted here):

| n | view | side - U |
| --- | --- | --- |
| 153 | evand:3b-1016:solved | -1.57e-14 |
| 207 | evand:3b-1016:solved | -2.42e-12 |

```bash
python -m devtools.regularize_evand layer --run-dir /tmp/claude-0/-home-user/497b954f-f1d7-5565-9258-beec4cbe400c/scratchpad/laneB/RUNS/3b-1016 --repo-root ..
python -m devtools.regularize_evand layer --run-dir "$(mktemp -d)" --repo-root .. --grid-run /tmp/claude-0/-home-user/497b954f-f1d7-5565-9258-beec4cbe400c/scratchpad/laneB/RUNS/3b-deg5-1016 --grid-counts 154
```
