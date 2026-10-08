---
type: is
id: is-01m4d7x55abg9jh20ap26kshhn
title: Read the catalogue source key once per full reconciliation
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m4cecqqmt13gys8265mpra32
created_at: 2026-10-08T07:51:05.641Z
updated_at: 2026-10-08T07:51:05.641Z
---
C15: Full hosted fast-C fails the original 12-second call budget in frontier transcription reconciliation (12.40 seconds). The test reloads and reparses the same source coverage YAML once for each of all324 cases while building the expected selected set, after the actual production reconciliation already ran. Read source key/catalogue inputs once within this fresh test invocation, retain the complete production comparison and all perturbed-record negatives; no budget or skip changes.
