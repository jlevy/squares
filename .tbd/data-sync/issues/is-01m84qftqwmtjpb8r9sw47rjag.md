---
type: is
id: is-01m84qftqwmtjpb8r9sw47rjag
title: Refresh the GitHub homepage atlas image from the deployed site
kind: task
status: closed
priority: 2
version: 4
delegate: codex-readme-atlas-20261123
labels:
  - documentation
dependencies: []
hold: null
hold_until: null
created_at: 2026-11-23T17:33:03.611Z
updated_at: 2026-11-23T18:10:59.096Z
started_at: 2026-11-23T17:33:04.435Z
closed_at: 2026-11-23T18:10:59.080Z
close_reason: "PR #1101 merged after both required gates and two reviews. Verified GitHub main serves the byte-identical updated 324-case image."
resolution: null
duplicate_of: null
---
The README links a 324-case atlas PNG last captured on 11 October. Use the maintained measure_atlas_views readme capture against the live atlas after the reviewed 127/305 delivery, verify all 324 tiles, review and merge the single image update, and confirm GitHub serves it.

## Notes

Opened draft #1101 at 10a42c40c21e657cbe840e5508f6b731fb349c5e against main 65d677ee. The maintained live capture waited for all 324 cases and wrote a verified 2652 × 1696 indexed PNG at normal pixel density under the memory guard. The two independent reviews of the one-file revision approved. Await full hosted gates and verify GitHub serves the image after merge.
