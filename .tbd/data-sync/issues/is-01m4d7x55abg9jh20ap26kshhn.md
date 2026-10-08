---
type: is
id: is-01m4d7x55abg9jh20ap26kshhn
title: Read the catalogue source key once per full reconciliation
kind: bug
status: in_progress
priority: 1
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4cecqqmt13gys8265mpra32
hold: null
hold_until: null
created_at: 2026-10-08T07:51:05.641Z
updated_at: 2026-10-08T07:51:12.342Z
started_at: 2026-10-08T07:51:12.341Z
---
C15: Full hosted fast-C fails the original 12-second call budget in frontier transcription reconciliation (12.40 seconds). The test reloads and reparses the same source coverage YAML once for each of all324 cases while building the expected selected set, after the actual production reconciliation already ran. Read source key/catalogue inputs once within this fresh test invocation, retain the complete production comparison and all perturbed-record negatives; no budget or skip changes.
