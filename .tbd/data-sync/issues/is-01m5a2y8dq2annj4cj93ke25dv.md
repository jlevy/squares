---
type: is
id: is-01m5a2y8dq2annj4cj93ke25dv
title: Reconcile full house refresh with later lower-bound writer layers
kind: bug
status: open
priority: 2
version: 3
delegate: codex-665-adoption-reconcile
labels: []
dependencies: []
parent_id: is-01m59jbf3zmjznc12k8g2b5cwk
hold: null
hold_until: null
created_at: 2026-10-19T12:42:17.399Z
updated_at: 2026-10-19T13:09:34.773Z
started_at: 2026-10-19T13:09:29.912Z
---
PR #665 C1 repair exposed historical full --refresh replacing n108 T216 evidence and lower-bound prose from an older upper-adoption replay. C1 adds opening-only refresh plus fail-closed lower-lane detection and preflight of all records before writes. Follow-up: implement an explicit ownership-aware merge for full evidence/history refresh with later lower additions, preserving four T216 evidence entries, lower introduction, exact lower 531/50, and all other later-writer content. Keep fail-closed protection until meaningful regression tests prove the reconciliation. Retained rejected refresh patch and n108 output: root .codex/intake-resume-20261019/665-review-C1-preparation/. No numeric or archive changes authorized by this follow-up alone.
