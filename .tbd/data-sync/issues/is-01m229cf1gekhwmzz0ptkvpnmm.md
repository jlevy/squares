---
type: is
id: is-01m229cf1gekhwmzz0ptkvpnmm
title: Test that a force law holds known optima still
kind: task
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-07-known-best-atlas-video.md
labels:
  - packing
dependencies: []
parent_id: is-01m1z68hzazv9yjs9k7cddmf82
created_at: 2026-09-09T05:13:53.455Z
updated_at: 2026-10-13T00:54:40.546Z
closed_at: 2026-10-13T00:54:40.546Z
close_reason: Duplicate of think-eq0n (same force-law stationarity test, X-025 C0d, filed an hour later under the video epic); consolidated per the owner's decision of 2026-10-13.
resolution: duplicate
duplicate_of: is-01m225psj2z0sx407k1ma5a4sp
---
A force law worth using must hold a known optimum stationary. That is a necessary condition needing no discovery, so it is a better first test of the law than whether it finds good answers, and it does not fit to a test set the way tuning on known answers does. Method: load each retained packing, run the physics, measure drift. The repository supplies the answer key, and the test is two-sided because of it. The translation-escape screen reports that most screened records have at least one movable square, so drift is not automatically a failure: on a record with no movable square, which includes the perfect squares and n = 5, 11, 28, 40, the law must hold every square exactly and any drift is a defect in the law; on a record with rattlers, only squares the screen already identifies as free may move, and the container side must not grow. Verify the screen's counts from packing/atlas/known-best/translation-escape-screen.json rather than trusting this description. Owner's idea, framed in packing/campaign/explorations/X-025-hunting-by-hand-and-the-move-set-threads.md.
