---
type: is
id: is-01m0tvc0vjy9yw4v41bjy6hgbw
title: Normalize packing campaign and work-unit vocabulary
kind: task
status: closed
priority: 1
version: 6
spec_path: explorations/packing/SYNOPSIS.md
delegate: codex@spud10
labels:
  - packing
  - documentation
  - focus-process
  - terminology
dependencies:
  - type: blocks
    target: is-01m0tt2681m25t6zve37pb002d
  - type: blocks
    target: is-01m0tt26ngt7wvf73xpvwaew65
  - type: blocks
    target: is-01m0tt272wj7kj55rf9fsa6bc6
parent_id: is-01m0r7tkdt35ged6b10gaf9wa0
hold: null
hold_until: null
created_at: 2026-08-24T21:38:36.017Z
updated_at: 2026-08-24T22:08:31.498Z
started_at: 2026-08-24T21:38:43.035Z
closed_at: 2026-08-24T22:08:31.498Z
close_reason: Defined the canonical W1-W6 taxonomy and normalized campaign, series, session, phase, slice, experiment, round, run, result, and ledger vocabulary in the synopsis, with compact README orientation and enforced schema agreement.
resolution: null
duplicate_of: null
---
Define exploration, campaign, series, session, workflow phase, slice, hypothesis, experiment, result, and ledger so each term has one meaning and one owning document. Reconcile the existing packing README, synopsis, campaign runbook, session guide/schema, conventions, agent instructions, and generated views. Acceptance: the README gives the short orientation; the synopsis owns the conceptual model; campaign/session runbooks own procedure; experiment means one durable measured round rather than a whole agent session; campaign, series, and session are not used interchangeably; and automated checks catch taxonomy drift where practical.
