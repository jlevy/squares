---
type: is
id: is-01m479rwhyavp3petjgt9qr2y7
title: "n = 17 integration: retain the R070/R071 CI artifacts and job logs before they expire (December 2026)"
kind: task
status: open
priority: 1
version: 5
labels:
  - result-import
dependencies: []
parent_id: is-01m46g51s5a06f0r0qsqy5tte3
created_at: 2026-10-06T00:28:16.318Z
updated_at: 2026-10-09T06:05:56.424Z
---
Held out of jlevy/squares#369 because the owner holds n = 17 for integration with the n = 17 branches. Lane G (think-cdzc) prepared commit 8b9788ee2 on the local branch claude/ecstatic-pascal-pothtx-archive: r070-global.zip (77,412 B), r070-geometry.zip (159,985 B), r071-bound.zip (212,890 B), each matching the SHA-256 the packet's run records state, plus the four job logs, into packing/resources/web/n17-guzhou-r071-2026-09-30/receipts/ci/artifacts/; r071-geometry (3,288,383 B) pinned by digest only. The GitHub Actions artifacts expire around 2026-12-29: re-fetch them (now reachable through the API) during the n = 17 integration and update that packet's README and the n = 17 evidence notes that say they could not be fetched.

## Notes

2026-10-06 (later): waits on the owner's n = 17 hold (think-x4v4), not on #369. Lane G's artifact commit 8b9788ee2 exists only on the ephemeral local branch claude/ecstatic-pascal-pothtx-archive; the CI artifacts stay downloadable until December 2026.

blocked_on: think-x4v4
