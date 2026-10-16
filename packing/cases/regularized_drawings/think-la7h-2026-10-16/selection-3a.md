| n | view | side - U | side - drawn | light / uneven / near-axis / classes / hues | house / stage sides | better on |
| --- | --- | --- | --- | --- | --- | --- |
| 105 | grid:3a-rerun-deg05-1016 | 0 | 0 | 7 / 14 / 5 / 16 / 16 -> 6 / 7 / 0 / 11 / 11 | 199 / 240 -> 226 / 248 | light_axis, uneven_axis, near_axis, classes, hues, house_total, stage_total |
| 129 | evand:3a-rerun-1016:same | 0 | 0 | 0 / 0 / 0 / 23 / 19 -> 0 / 0 / 0 / 13 / 13 | 362 / 366 -> 370 / 376 | classes, hues, house_total, stage_total |
| 146 | evand:3a-rerun-1016:same | 0 | 0 | 3 / 5 / 1 / 12 / 12 -> 1 / 0 / 0 / 6 / 6 | 367 / 388 -> 402 / 410 | light_axis, uneven_axis, near_axis, classes, hues, house_total, stage_total |
| 156 | grid:3a-rerun-deg05-1016 | 0 | 0 | 2 / 8 / 4 / 19 / 19 -> 2 / 4 / 0 / 15 / 15 | 328 / 376 -> 356 / 376 | uneven_axis, near_axis, classes, hues, house_total |
| 271 | grid:3a-rerun-deg05-1016 | 0 | 0 | 6 / 12 / 1 / 24 / 19 -> 6 / 10 / 0 / 23 / 19 | 728 / 752 -> 738 / 754 | uneven_axis, near_axis, classes, house_total, stage_total |

5 counts chosen; 4 with no adoptable view (the JSON report gives each candidate's reasons).

```bash
python -m devtools.regularize_evand layer --run-dir /tmp/claude-0/-home-user/497b954f-f1d7-5565-9258-beec4cbe400c/scratchpad/laneI/rerun/runs/3a-rerun-1016 --repo-root ..
python -m devtools.regularize_evand layer --run-dir "$(mktemp -d)" --repo-root .. --grid-run /tmp/claude-0/-home-user/497b954f-f1d7-5565-9258-beec4cbe400c/scratchpad/laneI/rerun/runs/3a-rerun-deg05-1016 --grid-counts 105 156 271
```
