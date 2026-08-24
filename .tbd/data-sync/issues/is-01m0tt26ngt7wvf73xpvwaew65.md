---
type: is
id: is-01m0tt26ngt7wvf73xpvwaew65
title: Define workflow entry and transition contracts in the packing synopsis
kind: task
status: open
priority: 1
version: 2
spec_path: explorations/packing/SYNOPSIS.md
labels:
  - packing
  - documentation
  - focus-process
  - workflow-entry-points
dependencies:
  - type: blocks
    target: is-01m0tt27gkgew93b6xzza03emd
parent_id: is-01m0r7tkdt35ged6b10gaf9wa0
created_at: 2026-08-24T21:15:45.712Z
updated_at: 2026-08-24T21:15:46.578Z
---
Add the operational detail behind W1-W6 near the synopsis opening. For each workflow state entry evidence, scope, permitted work, required artifacts, completion or stop rule, and next handoff. Define orchestrator transitions: one active workflow phase at a time; checkpoint the old phase; record the reason, evidence, and new contract; reset the slice clock; and allow a user request to trigger the boundary. Clarify that W6 owns disciplined time-bounded hypothesis execution while W1 enriches the knowledge base. Acceptance: mixed sessions remain reconstructable, workflow switches are deliberate, and the campaign runbook remains the sole owner of W6 mechanics.
