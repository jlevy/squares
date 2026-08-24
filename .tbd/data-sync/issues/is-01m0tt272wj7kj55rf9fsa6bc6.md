---
type: is
id: is-01m0tt272wj7kj55rf9fsa6bc6
title: Make packing agent-session records workflow-aware
kind: task
status: open
priority: 1
version: 2
spec_path: explorations/packing/campaign/schemas/agent-session.schema.yaml
labels:
  - packing
  - documentation
  - focus-process
  - workflow-entry-points
dependencies:
  - type: blocks
    target: is-01m0tt27gkgew93b6xzza03emd
parent_id: is-01m0r7tkdt35ged6b10gaf9wa0
created_at: 2026-08-24T21:15:46.139Z
updated_at: 2026-08-24T21:15:46.578Z
---
Evolve the agent-session contract without erasing the existing primary-focus concept. Record an entry workflow and an ordered phase history whose entries carry workflow, focus, objective, budget or clock, switch reason, outputs, checks, stop reason, and next action. Choose and document a backward-compatible migration for sessions 001-009. Extend the generated ledger so a reader can recover each session workflow sequence and aggregate the kinds of sessions completed. Acceptance: all session artifacts validate; legacy history is preserved; one active phase is enforceable; and the ledger is generated rather than hand-maintained.
