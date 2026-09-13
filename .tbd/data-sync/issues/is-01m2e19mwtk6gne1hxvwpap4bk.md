---
type: is
id: is-01m2e19mwtk6gne1hxvwpap4bk
title: "F6a: bind nested source, launch, and cleanup clocks to enclosing lifetimes"
kind: bug
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - calibration
  - admission
dependencies: []
parent_id: is-01m2dz5kzv8k9e1yq06017ngah
created_at: 2026-09-13T18:43:25.710Z
updated_at: 2026-09-13T18:43:33.325Z
---
At exact reader head 7e4d2487, full readback accepts source_loading_seconds 0.9 inside preflight 0.1, launch_seconds 1000000 before worker exit 1.05, and supervisor_cleanup_seconds 1000000 inside external lifetime 1.2. Enforce necessary nested and post-exit bounds with equality controls; do not sum overlapping durations. Evidence: docs/project/reviews/review-2026-09-13-n11-bc329-reader-rereview.md.
