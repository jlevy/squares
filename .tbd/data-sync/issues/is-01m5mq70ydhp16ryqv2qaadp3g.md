---
type: is
id: is-01m5mq70ydhp16ryqv2qaadp3g
title: "PR #751 A4: records misstate what check_certificate_citations accepts"
kind: bug
status: in_progress
priority: 3
version: 2
delegate: c-review-thmc-1023
labels: []
dependencies: []
parent_id: is-01m5mq5vh52bze2e8j4eapg0bj
hold: null
hold_until: null
created_at: 2026-10-23T15:49:00.493Z
updated_at: 2026-10-23T15:49:17.033Z
started_at: 2026-10-23T15:49:17.033Z
---
Review A, finding A4 (Low), PR #751, https://github.com/jlevy/squares/pull/751#issuecomment-6368595518. evidence.yaml:43054-43055, verifiers.yaml:2659-2662, the review's lines 483-486 and think-7scz's paste instructions say the register entry is the record that cites the run's evidence. orphaned_evidence (packing/devtools/check_certificate_citations.py:185) counts case-record packing blocks, method-limit and beyond-horizon evidence; otherwise a 30-day deferral naming the register entry is needed.
