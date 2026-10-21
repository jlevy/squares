| n | view | side - U | side - drawn | light / uneven / near-axis / classes / hues | house / stage sides | better on |
| --- | --- | --- | --- | --- | --- | --- |
| 155 | grid:adopt-2026-10-19-n155-271-grid-0.5 | 0 | 0 | 1 / 6 / 1 / 21 / 19 -> 1 / 3 / 0 / 20 / 19 | 350 / 380 -> 362 / 380 | uneven_axis, near_axis, classes, house_total |
| 236 | evand:adopt-2026-10-19-n155-271-evand:same | 0 | 0 | 9 / 16 / 3 / 19 / 19 -> 1 / 2 / 0 / 6 / 6 | 692 / 719 -> 736 / 736 | light_axis, uneven_axis, near_axis, classes, hues, house_total, stage_total |
| 271 | evand:adopt-2026-10-19-n155-271-evand:same | 0 | 0 | 7 / 14 / 2 / 25 / 19 -> 7 / 12 / 0 / 21 / 19 | 728 / 754 -> 738 / 758 | uneven_axis, near_axis, classes, house_total, stage_total |

3 counts chosen; 1 with no adoptable view (the JSON report gives each candidate's reasons).

```bash
copies="$(mktemp -d)"
mkdir "$copies/0" && cp -R /tmp/claude-0/-home-user-squares/b1f8ff4e-5e49-561e-aa0f-a76f1a5fe076/scratchpad/lnew/runs/adopt-2026-10-19-n155-271-evand "$copies/0/adopt-2026-10-19-n155-271-evand"
python -m devtools.regularize_evand reclassify --run-dir "$copies/0/adopt-2026-10-19-n155-271-evand" --refresh-bounds
python -m devtools.regularize_evand layer --run-dir "$copies/0/adopt-2026-10-19-n155-271-evand" --repo-root .. --exclude 155
python -m devtools.regularize_evand layer --run-dir "$(mktemp -d)" --repo-root .. --grid-run /tmp/claude-0/-home-user-squares/b1f8ff4e-5e49-561e-aa0f-a76f1a5fe076/scratchpad/lnew/runs/adopt-2026-10-19-n155-271-grid-0.5 --grid-counts 155
```
