---
type: is
id: is-01m4wds22twm2dtqwtsvkh1d9a
title: Keep the ladder diagram inside its clipping track with both gutters
kind: bug
status: closed
priority: 1
version: 3
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4wcjctchxg9qv8jp0za5g13
hold: null
hold_until: null
created_at: 2026-10-14T05:22:19.353Z
updated_at: 2026-10-14T07:21:25.583Z
started_at: 2026-10-14T05:22:31.894Z
closed_at: 2026-10-14T07:21:25.583Z
close_reason: Fixed, independently reviewed, and merged in regularization stack main9f48ccc80cee8dcf94c7cadbcaded01408f94fa2; exact-head Packing and Pages CI pass. Deployment tracked by parent think-azzv.
resolution: null
duplicate_of: null
---
The pre-push ladder tests measured left gutters of 3, 5 and 5.5 px at widths 768, 716 and 715, below the unchanged 7.5 px assertion. The implemented cleanup fixes the clipping-track layout rather than relaxing the gutter floor. Relevant strong-lane validation: the ladder/layout group passed within the 149 browser-test batch. Preserve readability and clipping checks at narrow and wide widths. Keep in progress until the final gate and merge.
