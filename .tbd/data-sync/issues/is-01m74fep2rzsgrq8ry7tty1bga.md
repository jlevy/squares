---
type: is
id: is-01m74fep2rzsgrq8ry7tty1bga
title: "Import #941, #942: Joost de Winter's 31 lowered upper bounds for n between 413 and 989"
kind: task
status: in_progress
priority: 2
version: 5
delegate: bold-ritchie-l90
labels:
  - intake
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-11T04:56:55.639Z
updated_at: 2026-11-11T10:03:57.111Z
started_at: 2026-11-11T09:58:23.522Z
---
#941 (2026-11-10T13:30Z) fifteen lowered upper bounds n 413-910; #942 (14:41Z) sixteen n 632-989; JoostdeWinter. Beyond the atlas's 324, below the 1024 horizon: beyond-horizon rows. Precedent: Yim's 553-700 rows (PR #934). Starts after the Özden lane to stay within usage limits.

## Notes

2026-11-11 coordinator: JoostdeWinter/square-packing commits d3a020e, 71da0d5, a9486ed and a0c4fc8 (between the #939 pin 702c7af and the #946 pin c4e65d0, 9-10 November) add certificates at 37 new counts above 324 under above324/ and above324_refined/, with no issue of their own. Under the 14 October rule these are reports from their first commits. Triage them with #941/#942 (likely overlapping counts; compare report times and sides, keep each first report).

2026-11-11 L90 (bold-ritchie-l90), triage start. Branch claude/bold-ritchie-xo28us-l90 from main 8afdabe8f.
- Commits (UTC; push not read: the events API and the activity page both refuse this session, as for #934): d3a020e 2026-11-09T23:59:23Z adds above324/ with 9 certificates (413, 494, 539, 543, 547, 590, 809, 810, 867); 71da0d5 2026-11-10T06:15:17Z adds 6 more (738, 739, 753, 794, 851, 910) and touches no earlier certificate, so #941's 15 files at 71da0d5 are the blobs first committed there; a9486ed 14:39:52Z adds above324_refined/ with #942's 16 (1m26s before #942); a0c4fc8 15:37:44Z adds 597, 754, 864, 865, 869, 991.
- Surprise: a0c4fc8's six DO have a report: #942's addendum comment issuecomment-6772308414 at 2026-11-10T16:02:47Z claims all six at a0c4fc8. Following #763's practice (an issue's claims carry first_committed for certificates committed earlier), the comment is the report and a0c4fc8 its first commit; same verdicts either way unless something else reached those counts in 15:37-16:02Z (nothing found: no other issue in #939-#947 above 324).
- d3a020e's role: first publication of 9 of #941's certificates, 13.5 h before #941; no other report reached those counts in between (issues #943-#947 are below 324). Ledger: #941 claims carry first_committed d3a020e / 71da0d5.
- All 37 counts lie in 413..991: no count above 1024, nothing held for think-f2io.
