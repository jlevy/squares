---
type: is
id: is-01m2e19p36hn9ks8b2er46jw3m
title: "F7: require the calibration execution revision to be a Git commit object"
kind: bug
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - calibration
  - admission
dependencies: []
parent_id: is-01m2b884a8xfyybgtpfr4rdwgv
created_at: 2026-09-13T18:43:26.949Z
updated_at: 2026-09-13T18:43:26.949Z
---
At exact reader head 7e4d2487, full readback accepts the execution commit tree OID as source and invocation revision when supplied as the expected revision. Require Git object type commit, preserving F1 complete source manifest and reader/execution revision distinction. Evidence: docs/project/reviews/review-2026-09-13-n11-bc329-reader-rereview.md.
