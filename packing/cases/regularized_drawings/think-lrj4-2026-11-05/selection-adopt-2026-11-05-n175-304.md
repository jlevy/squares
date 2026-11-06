| n | view | side - U | side - drawn | light / uneven / near-axis / classes / hues | house / stage sides | better on |
| --- | --- | --- | --- | --- | --- | --- |
| 175 | evand:adopt-2026-11-05-n175-304-evand:same | 0 | 0 | 22 / 58 / 22 / 43 / 19 -> 8 / 19 / 0 / 3 / 3 | 292 / 422 -> 477 / 477 | light_axis, uneven_axis, near_axis, classes, hues, house_total, stage_total |
| 204 | evand:adopt-2026-11-05-n175-304-evand:same | 0 | 0 | 7 / 17 / 2 / 26 / 19 -> 7 / 14 / 0 / 19 / 19 | 510 / 531 -> 517 / 535 | uneven_axis, near_axis, classes, house_total, stage_total |
| 260 | grid:adopt-2026-11-05-n175-304-grid-deg05 | 0 | 0 | 26 / 59 / 14 / 39 / 19 -> 3 / 9 / 0 / 25 / 19 | 402 / 582 -> 556 / 634 | light_axis, uneven_axis, near_axis, classes, house_total, stage_total |
| 268 | evand:adopt-2026-11-05-n175-304-evand:same | 0 | 0 | 13 / 47 / 16 / 41 / 19 -> 0 / 0 / 0 / 12 / 12 | 547 / 636 -> 697 / 727 | light_axis, uneven_axis, near_axis, classes, hues, house_total, stage_total |
| 303 | grid:adopt-2026-11-05-n175-304-grid-deg5 | 0 | 0 | 1 / 4 / 1 / 54 / 19 -> 1 / 2 / 0 / 52 / 19 | 745 / 789 -> 756 / 798 | uneven_axis, near_axis, classes, house_total, stage_total |

5 counts chosen; 2 with no adoptable view (the JSON report gives each candidate's reasons).

```bash
copies="$(mktemp -d)"
mkdir "$copies/0" && cp -R /tmp/claude-0/-home-user-squares/0a01ddbe-91e2-5d1d-98f8-365093a10337/scratchpad/l51-regularize/adopt-2026-11-05-n175-304-evand "$copies/0/adopt-2026-11-05-n175-304-evand"
python -m devtools.regularize_evand reclassify --run-dir "$copies/0/adopt-2026-11-05-n175-304-evand" --refresh-bounds
python -m devtools.regularize_evand layer --run-dir "$copies/0/adopt-2026-11-05-n175-304-evand" --repo-root .. --exclude 293
python -m devtools.regularize_evand layer --run-dir "$(mktemp -d)" --repo-root .. --grid-run /tmp/claude-0/-home-user-squares/0a01ddbe-91e2-5d1d-98f8-365093a10337/scratchpad/l51-regularize/adopt-2026-11-05-n175-304-grid-deg05 --grid-counts 260
python -m devtools.regularize_evand layer --run-dir "$(mktemp -d)" --repo-root .. --grid-run /tmp/claude-0/-home-user-squares/0a01ddbe-91e2-5d1d-98f8-365093a10337/scratchpad/l51-regularize/adopt-2026-11-05-n175-304-grid-deg5 --grid-counts 303
```
