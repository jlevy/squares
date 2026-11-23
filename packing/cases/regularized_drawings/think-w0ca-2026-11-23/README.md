# Drawing runs for the T-343 adoption at 264

The 23 November 2026 intake pass replaced T-308 with
[T-343](../../../frontier/RESULTS.md), Doğa Özden’s refinement of Tomáš Kodaj and
JoeGun’s packing.
The exact side rounds up to $16.7721683050405464$ at 16 decimal places.
These four runs used the T-343 house witness under the
[house drawing rule](../../../campaign/result-import.md#adopt-a-house-then-regularize-it).

| Run | Outcome |
| --- | --- |
| Grid-slack, 0.5° | The view passes both exact routes at the exact house side. It has seven light squares, 28 uneven squares, zero near-axis squares and 26 angle classes. |
| Grid-slack, 1° | The selector drew this view at the exact house side. It passes both exact routes, with six light squares, 28 uneven squares, zero near-axis squares and 25 angle classes. |
| Grid-slack, 5° | Its exact view matches the 1° view byte for byte. Both exact routes pass. |
| Evan Daniel’s driver at `675a5ea` | No view. The ordinary solve gives `not jammed` in the driver’s smooth-contact solve. Its `force-kkt` and `dps-100` retries report `solve failed`. |
| [Selection](selection-n264.md) | The 1° view passes row 10. The selected side equals the registered upper bound exactly. The selector found no register candidate. |

The axis view of T-343 measured by the selector had 15 light squares, 47 uneven squares,
four near-axis squares, 30 classes and 19 hues.
The selected view retains all 19 hues and improves the full-side totals from 650 to 707
on the house measure and 721 to 741 on the stage measure.
Square matching is one-to-one and the contact comparison found no regressions against
the new house. Against the previously published T-308 drawing, light squares rise from
four to six, uneven squares stay at 28, near-axis squares stay at zero, and full sides
rise from 697 to 707 (house) and 723 to 741 (stage).
The flip rule again chooses a quarter-turn clockwise from the quadrants, with no
reflection.

The solver’s status is a report about its smooth-contact model.
Feasibility comes from the
[original exact certificate](../../../resources/web/ozden-s264-upper-bound-2026-11-23/README.md).

The grid reports record 90.99, 90.36 and 116.43 elapsed seconds.
The Evan Daniel receipt records 15.85 CPU-seconds and 18.82 wall-seconds with one
worker. The four-way selection took 70.79 seconds under the memory guard.
The guard interrupted the first 1° attempt when the Mac’s VM and swap reserve fell below
its cutoff. The retained 1° report and summary are from its completed second attempt.

The grid driver writes a per-count report and view.
Each grid `run.json` is a derived summary in the maintained
`regularize_grid_slack.run_block` shape.
Its time fields both come from the report’s elapsed time.
The compressed reports and views retain their uncompressed bytes.
The [selection JSON](selection-n264.json) changes the checkout and run paths to
repository-relative paths.
In the selection table’s command, `RUNS` stands for the original run directory or a copy
with the reports uncompressed.

## Compressed Files

| Path | Origin | Git blob of uncompressed bytes | SHA-256 of uncompressed bytes |
| --- | --- | --- | --- |
| `adopt-2026-11-23-n264-evand/n-264/report.json.gz` | receipt | `57247745dd873e47c313c396086a1af5ec2d0f54` | `47797cd768d79122c24798154e0dc77c97dd12c9a21e7a54ff9dd6d5d58d7a12` |
| `adopt-2026-11-23-n264-grid-deg05/n-264/report.json.gz` | receipt | `cc7ac6d675b61388f046c87ea7dcc094142e165b` | `0e65d6a7a613e89271738bbf36fb55b91e1167ff7d7a3d6c4e91c44ca9149214` |
| `adopt-2026-11-23-n264-grid-deg05/n-264/view.yaml.gz` | receipt | `9297217ee425958f5926c3278c985c2f28b990c8` | `f3e58f1f4253517a52f10e996bec3fd6d35e3676d4539a5d1a3c1315a407bdcf` |
| `adopt-2026-11-23-n264-grid-deg1/n-264/report.json.gz` | receipt | `a610fa10fec4500fa5fd77db0efdc9646406fd86` | `38b7638c3c5e3ce2fd3865649f1552835dc32aebe98067d7d4b5582e1696b184` |
| `adopt-2026-11-23-n264-grid-deg1/n-264/view.yaml.gz` | receipt | `1b772cd5cce3279ba3bcf57c00700673d8da33b3` | `ea92780fe1d48eb698351a0254795ebda3baf694d1d8ec9d4ae742727d6896f5` |
| `adopt-2026-11-23-n264-grid-deg5/n-264/report.json.gz` | receipt | `5e9844df3a303b401f341a8f71fbc085f2277b1e` | `0e110663e115fc6ad53bfa064a379b716d685ad7d529d8caa54de3fdefdd72f3` |
| `adopt-2026-11-23-n264-grid-deg5/n-264/view.yaml.gz` | receipt | `1b772cd5cce3279ba3bcf57c00700673d8da33b3` | `ea92780fe1d48eb698351a0254795ebda3baf694d1d8ec9d4ae742727d6896f5` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
