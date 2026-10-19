| n | view | side - U | side - drawn | light / uneven / near-axis / classes / hues | house / stage sides | better on |
| --- | --- | --- | --- | --- | --- | --- |
| 232 | grid:z7wn-b-deg05-1016 | 0 | 0 | 8 / 24 / 7 / 17 / 17 -> 4 / 20 / 0 / 14 / 14 | 620 / 700 -> 652 / 708 | light_axis, uneven_axis, near_axis, classes, hues, house_total, stage_total |
| 264 | grid:z7wn-b-deg05-1016 | 0 | 0 | 3 / 15 / 0 / 17 / 17 -> 3 / 15 / 0 / 17 / 17 | 703 / 709 -> 711 / 715 | house_total, stage_total |
| 271 | grid:z7wn-b-deg05-1016 | 0 | 0 | 6 / 12 / 1 / 24 / 19 -> 6 / 10 / 0 / 23 / 19 | 728 / 752 -> 738 / 754 | uneven_axis, near_axis, classes, house_total, stage_total |
| 302 | grid:z7wn-b-deg5-1016 | 0 | 0 | 6 / 26 / 11 / 40 / 19 -> 0 / 0 / 0 / 27 / 19 | 882 / 952 -> 960 / 962 | light_axis, uneven_axis, near_axis, classes, house_total, stage_total |

4 counts chosen; 4 with no adoptable view (the JSON report gives each candidate's reasons).

```bash
python -m devtools.regularize_evand layer --run-dir "$(mktemp -d)" --repo-root .. --grid-run /tmp/claude-0/-home-user/497b954f-f1d7-5565-9258-beec4cbe400c/scratchpad/laneS/runs/b/z7wn-b-deg05-1016 --grid-counts 232 264 271
python -m devtools.regularize_evand layer --run-dir "$(mktemp -d)" --repo-root .. --grid-run /tmp/claude-0/-home-user/497b954f-f1d7-5565-9258-beec4cbe400c/scratchpad/laneS/runs/b/z7wn-b-deg5-1016 --grid-counts 302
```
