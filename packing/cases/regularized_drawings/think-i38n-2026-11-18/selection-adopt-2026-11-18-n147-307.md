| n | view | side - U | side - drawn | light / uneven / near-axis / classes / hues | house / stage sides | better on |
| --- | --- | --- | --- | --- | --- | --- |
| 147 | grid:adopt-2026-11-18-n147-307-grid-deg05 | 0 | 0 | 7 / 16 / 11 / 20 / 19 -> 1 / 6 / 0 / 10 / 10 | 320 / 389 -> 389 / 397 | light_axis, uneven_axis, near_axis, classes, hues, house_total, stage_total |
| 156 | grid:adopt-2026-11-18-n147-307-grid-deg05 | 0 | 0 | 5 / 9 / 1 / 19 / 19 -> 2 / 4 / 0 / 18 / 18 | 337 / 364 -> 356 / 366 | light_axis, uneven_axis, near_axis, classes, hues, house_total, stage_total |
| 180 | evand:adopt-2026-11-18-n147-307-evand:same | 0 | 0 | 17 / 34 / 9 / 25 / 19 -> 4 / 9 / 0 / 8 / 8 | 423 / 481 -> 513 / 515 | light_axis, uneven_axis, near_axis, classes, hues, house_total, stage_total |
| 210 | grid:adopt-2026-11-18-n147-307-grid-deg05 | 0 | 0 | 3 / 6 / 0 / 24 / 19 -> 3 / 6 / 0 / 24 / 19 | 500 / 544 -> 506 / 544 | house_total |
| 260 | grid:adopt-2026-11-18-n147-307-grid-deg05 | 0 | 0 | 9 / 28 / 3 / 29 / 19 -> 3 / 9 / 0 / 26 / 19 | 500 / 608 -> 596 / 638 | light_axis, uneven_axis, near_axis, classes, house_total, stage_total |
| 262 | evand:adopt-2026-11-18-n147-307-evand:same | 0 | 0 | 23 / 53 / 37 / 58 / 19 -> 0 / 0 / 0 / 2 / 2 | 489 / 712 -> 822 / 822 | light_axis, uneven_axis, near_axis, classes, hues, house_total, stage_total |
| 268 | grid:adopt-2026-11-18-n147-307-grid-deg05 | 0 | 0 | 28 / 104 / 41 / 65 / 19 -> 0 / 0 / 0 / 28 / 19 | 495 / 833 -> 834 / 846 | light_axis, uneven_axis, near_axis, classes, house_total, stage_total |
| 272 | evand:adopt-2026-11-18-n147-307-evand:same | 0 | 0 | 3 / 12 / 5 / 27 / 19 -> 2 / 5 / 2 / 23 / 19 | 667 / 741 -> 693 / 741 | light_axis, uneven_axis, near_axis, classes, house_total |
| 292 | grid:adopt-2026-11-18-n147-307-grid-deg05 | 0 | 0 | 107 / 120 / 109 / 85 / 19 -> 3 / 15 / 0 / 38 / 19 | 88 / 826 -> 846 / 870 | light_axis, uneven_axis, near_axis, classes, house_total, stage_total |
| 295 | grid:adopt-2026-11-18-n147-307-grid-deg05 | 0 | 0 | 83 / 93 / 126 / 165 / 19 -> 5 / 11 / 0 / 49 / 19 | 58 / 692 -> 815 / 897 | light_axis, uneven_axis, near_axis, classes, house_total, stage_total |
| 299 | grid:adopt-2026-11-18-n147-307-grid-deg05 | 0 | 0 | 18 / 40 / 20 / 49 / 19 -> 6 / 20 / 2 / 31 / 19 | 635 / 773 -> 775 / 817 | light_axis, uneven_axis, near_axis, classes, house_total, stage_total |

11 counts chosen; 2 with no adoptable view (the JSON report gives each candidate's reasons).

Register candidates (policy row 3; registered first, never admitted here):

| n | view | side - U |
| --- | --- | --- |
| 260 | evand:adopt-2026-11-18-n147-307-evand:solved | -1.01e-14 |
| 268 | evand:adopt-2026-11-18-n147-307-evand:solved | -1.63e-15 |
| 270 | evand:adopt-2026-11-18-n147-307-evand:solved | -5.73e-15 |
| 272 | evand:adopt-2026-11-18-n147-307-evand:solved | -3.86e-17 |
| 292 | evand:adopt-2026-11-18-n147-307-evand:solved | -1.03e-13 |
| 295 | evand:adopt-2026-11-18-n147-307-evand:solved | -4.16e-19 |
| 299 | evand:adopt-2026-11-18-n147-307-evand:solved | -6.20e-15 |
| 307 | evand:adopt-2026-11-18-n147-307-evand:solved | -1.34e-15 |

```bash
copies="$(mktemp -d)"
mkdir "$copies/0" && cp -R /tmp/claude-0/-home-user-squares/bd74155c-bf06-5d6c-a727-558842453a91/scratchpad/w3/runs/adopt-2026-11-18-n147-307-evand "$copies/0/adopt-2026-11-18-n147-307-evand"
python -m devtools.regularize_evand reclassify --run-dir "$copies/0/adopt-2026-11-18-n147-307-evand" --refresh-bounds
python -m devtools.regularize_evand layer --run-dir "$copies/0/adopt-2026-11-18-n147-307-evand" --repo-root ..
python -m devtools.regularize_evand layer --run-dir "$(mktemp -d)" --repo-root .. --grid-run /tmp/claude-0/-home-user-squares/bd74155c-bf06-5d6c-a727-558842453a91/scratchpad/w3/runs/adopt-2026-11-18-n147-307-grid-deg05 --grid-counts 147 156 210 260 268 292 295 299
```
