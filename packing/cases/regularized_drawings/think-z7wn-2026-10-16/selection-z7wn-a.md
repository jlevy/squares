| n | view | side - U | side - drawn | light / uneven / near-axis / classes / hues | house / stage sides | better on |
| --- | --- | --- | --- | --- | --- | --- |
| 129 | evand:z7wn-a-1016:same | 0 | 0 | 0 / 0 / 0 / 23 / 19 -> 0 / 0 / 0 / 12 / 12 | 362 / 366 -> 372 / 378 | classes, hues, house_total, stage_total |
| 146 | evand:z7wn-a-1016:same | 0 | 0 | 5 / 20 / 6 / 16 / 16 -> 1 / 0 / 0 / 5 / 5 | 347 / 372 -> 400 / 410 | light_axis, uneven_axis, near_axis, classes, hues, house_total, stage_total |
| 154 | grid:z7wn-a-deg5-1016 | 0 | 0 | 12 / 27 / 2 / 15 / 15 -> 4 / 9 / 0 / 12 / 12 | 374 / 402 -> 419 / 423 | light_axis, uneven_axis, near_axis, classes, hues, house_total, stage_total |
| 156 | grid:z7wn-a-deg05-1016 | 0 | 0 | 2 / 8 / 4 / 19 / 19 -> 2 / 4 / 0 / 15 / 15 | 328 / 376 -> 356 / 376 | uneven_axis, near_axis, classes, hues, house_total |
| 175 | evand:z7wn-a-1016:same | 0 | 0 | 4 / 15 / 1 / 18 / 18 -> 4 / 15 / 0 / 3 / 3 | 478 / 482 -> 502 / 502 | near_axis, classes, hues, house_total, stage_total |
| 204 | evand:z7wn-a-1016:same | 0 | 0 | 4 / 19 / 0 / 17 / 17 -> 4 / 19 / 0 / 5 / 5 | 556 / 572 -> 580 / 580 | classes, hues, house_total, stage_total |

6 counts chosen; 2 with no adoptable view (the JSON report gives each candidate's reasons).

```bash
python -m devtools.regularize_evand layer --run-dir /tmp/claude-0/-home-user/497b954f-f1d7-5565-9258-beec4cbe400c/scratchpad/laneJ/runs/z7wn-a-1016 --repo-root ..
python -m devtools.regularize_evand layer --run-dir "$(mktemp -d)" --repo-root .. --grid-run /tmp/claude-0/-home-user/497b954f-f1d7-5565-9258-beec4cbe400c/scratchpad/laneJ/runs/z7wn-a-deg05-1016 --grid-counts 156
python -m devtools.regularize_evand layer --run-dir "$(mktemp -d)" --repo-root .. --grid-run /tmp/claude-0/-home-user/497b954f-f1d7-5565-9258-beec4cbe400c/scratchpad/laneJ/runs/z7wn-a-deg5-1016 --grid-counts 154
```
