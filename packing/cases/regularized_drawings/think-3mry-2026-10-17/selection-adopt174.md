| n | view | side - U | side - drawn | light / uneven / near-axis / classes / hues | house / stage sides | better on |
| --- | --- | --- | --- | --- | --- | --- |
| 105 | grid:adopt174-deg05-1017 | 0 | 0 | 7 / 14 / 5 / 16 / 16 -> 6 / 7 / 0 / 11 / 11 | 199 / 240 -> 226 / 248 | light_axis, uneven_axis, near_axis, classes, hues, house_total, stage_total |
| 131 | grid:adopt174-deg05-1017 | 0 | 0 | 7 / 21 / 0 / 14 / 14 -> 7 / 21 / 0 / 14 / 14 | 280 / 294 -> 284 / 296 | house_total, stage_total |
| 172 | evand:adopt174-1017:same | 0 | 0 | 0 / 0 / 0 / 6 / 6 -> 0 / 0 / 0 / 6 / 6 | 480 / 566 -> 480 / 570 | stage_total |
| 181 | grid:adopt174-deg05-1017 | 0 | 0 | 2 / 4 / 0 / 18 / 18 -> 2 / 4 / 0 / 18 / 18 | 450 / 478 -> 452 / 478 | house_total |
| 206 | grid:adopt174-deg05-1017 | 0 | 0 | 25 / 58 / 33 / 41 / 19 -> 0 / 0 / 0 / 8 / 8 | 416 / 585 -> 661 / 667 | light_axis, uneven_axis, near_axis, classes, hues, house_total, stage_total |
| 238 | grid:adopt174-deg5-1017 | 0 | 0 | 7 / 15 / 0 / 14 / 14 -> 7 / 15 / 0 / 13 / 13 | 654 / 662 -> 656 / 664 | classes, hues, house_total, stage_total |
| 239 | grid:adopt174-deg05-1017 | 0 | 0 | 7 / 17 / 1 / 20 / 19 -> 7 / 16 / 0 / 19 / 19 | 596 / 619 -> 603 / 623 | uneven_axis, near_axis, classes, house_total, stage_total |
| 270 | grid:adopt174-deg05-1017 | 0 | 0 | 4 / 9 / 0 / 21 / 19 -> 4 / 9 / 0 / 21 / 19 | 734 / 750 -> 738 / 752 | house_total, stage_total |
| 305 | grid:adopt174-deg5-1017 | 0 | 0 | 2 / 7 / 1 / 26 / 19 -> 2 / 7 / 1 / 25 / 19 | 814 / 836 -> 824 / 842 | classes, house_total, stage_total |
| 307 | grid:adopt174-deg05-1017 | 0 | 0 | 7 / 14 / 0 / 27 / 19 -> 7 / 14 / 0 / 27 / 19 | 764 / 812 -> 768 / 812 | house_total |

10 counts chosen; 25 with no adoptable view (the JSON report gives each candidate's reasons).

```bash
copies="$(mktemp -d)"
mkdir "$copies/0" && cp -R /tmp/claude-0/-home-user/497b954f-f1d7-5565-9258-beec4cbe400c/scratchpad/laneT/runs/adopt174-1017 "$copies/0/adopt174-1017"
python -m devtools.regularize_evand reclassify --run-dir "$copies/0/adopt174-1017" --refresh-bounds
python -m devtools.regularize_evand layer --run-dir "$copies/0/adopt174-1017" --repo-root .. --exclude 68
python -m devtools.regularize_evand layer --run-dir "$(mktemp -d)" --repo-root .. --grid-run /tmp/claude-0/-home-user/497b954f-f1d7-5565-9258-beec4cbe400c/scratchpad/laneT/runs/adopt174-deg05-1017 --grid-counts 105 131 181 206 239 270 307
python -m devtools.regularize_evand layer --run-dir "$(mktemp -d)" --repo-root .. --grid-run /tmp/claude-0/-home-user/497b954f-f1d7-5565-9258-beec4cbe400c/scratchpad/laneT/runs/adopt174-deg5-1017 --grid-counts 238 305
```
