---
type: is
id: is-01m4jjgm8npn9zv9h0wcq2yp2y
title: Qualify squish custody replay controls under final checkpoint resource contention
kind: bug
status: in_progress
priority: 1
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4h9s465x7mphy1xxkmdyqc9
hold: null
hold_until: null
created_at: 2026-10-10T09:32:41.610Z
updated_at: 2026-10-10T09:35:43.582Z
started_at: 2026-10-10T09:35:43.581Z
---
Hda22 final broad pre-push normal lane exposed two existing 30-second custody replay control deadlines for squish_followup_packets and second_squish_followup_packets while other host validation schedulers were active. Retain failures, diagnose exact causes under a controlled focused run, preserve all custody assertions and existing acceptance limits, and qualify actual hosted slow-lane execution. Root owns tracking and publication; no timeout relaxation without measured evidence and review.
