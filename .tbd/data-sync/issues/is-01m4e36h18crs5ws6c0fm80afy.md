---
type: is
id: is-01m4e36h18crs5ws6c0fm80afy
title: Review and validate the atlas site cleanups
kind: task
status: in_progress
priority: 2
version: 18
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-08T15:48:04.263Z
updated_at: 2026-10-09T04:44:15.321Z
started_at: 2026-10-08T15:49:07.449Z
---
Review source changes and exported atlas, run focused checks and the change-reachable gate, then commit/push a focused PR and confirm CI. Keep the site cleanup epic open for further requests.

## Notes

Final clean HEAD818c4c372c9abc5878e7ed755e1ee79fa19f1a1f, base3213d651b880d7768bce8506efaf75c2089aeb4f, data9c34421f. All exact user typography requirements now source/actualPDF verified:15shared body lines, uniform face/size/weight/spacing, two black plain final lines, right ink alignment; retained cards unchanged. Producer preflight R1 fixed in a7; independent source review at818 reports no open material findings and covers84non-bulk paths of96,12generated/deleted artifacts separately visually verified. Four review body drafts pending publication/trust/CI. Maintained export56.76s/postflightgreen; integrated preview92.16s,5677file checks,9assets+2aliases byte-equal, newmethods payload intact. Final PDF reopened in defaultPreview from verified569KBfile. Current full required --push against3213 is running;63completed edit checks all passed so far, reachable whole suite underway. No PR/push/final hosted or checkpoint pass claimed yet. Keep epic open; no GitHub merge authorized.
