| n | view | side - U | side - drawn | light / uneven / near-axis / classes / hues | house / stage sides | better on |
| --- | --- | --- | --- | --- | --- | --- |
| 175 | evand:3c-1016:same | 0 | 0 | 8 / 19 / 0 / 17 / 17 -> 4 / 15 / 0 / 3 / 3 | 466 / 474 -> 502 / 502 | light_axis, uneven_axis, classes, hues, house_total, stage_total |
| 232 | evand:3c-1016:same | 0 | 0 | 6 / 25 / 0 / 10 / 10 -> 4 / 22 / 0 / 3 / 3 | 698 / 702 -> 756 / 756 | light_axis, uneven_axis, classes, hues, house_total, stage_total |
| 264 | grid:3c-deg05-1016 | 0 | 0 | 5 / 20 / 0 / 17 / 17 -> 5 / 20 / 0 / 17 / 17 | 695 / 701 -> 705 / 709 | house_total, stage_total |

3 counts chosen; 0 with no adoptable view (the JSON report gives each candidate's reasons).

```bash
copies="$(mktemp -d)"
mkdir "$copies/0" && cp -R /tmp/claude-0/-home-user/497b954f-f1d7-5565-9258-beec4cbe400c/scratchpad/laneB/RUNS/3c-1016 "$copies/0/3c-1016"
python -m devtools.regularize_evand reclassify --run-dir "$copies/0/3c-1016" --refresh-bounds
python -m devtools.regularize_evand layer --run-dir "$copies/0/3c-1016" --repo-root ..
python -m devtools.regularize_evand layer --run-dir "$(mktemp -d)" --repo-root .. --grid-run /tmp/claude-0/-home-user/497b954f-f1d7-5565-9258-beec4cbe400c/scratchpad/laneB/RUNS/3c-deg05-1016 --grid-counts 264
```
