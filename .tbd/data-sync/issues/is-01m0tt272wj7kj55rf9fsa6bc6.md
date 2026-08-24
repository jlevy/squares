---
type: is
id: is-01m0tt272wj7kj55rf9fsa6bc6
title: Make packing agent-session records workflow-aware
kind: task
status: closed
priority: 1
version: 3
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
updated_at: 2026-08-24T22:08:32.287Z
closed_at: 2026-08-24T22:08:32.287Z
close_reason: Added the README selector, full synopsis entry and transition contracts, AgentSession/v2 phase history, migrated sessions 001-009, and generated workflow summaries.
resolution: null
duplicate_of: null
---
Evolve the agent-session contract without erasing the existing primary-focus concept. Record an entry workflow and an ordered phase history whose entries carry workflow, focus, objective, budget or clock, switch reason, outputs, checks, stop reason, and next action. Choose and document a backward-compatible migration for sessions 001-009. Extend the generated ledger so a reader can recover each session workflow sequence and aggregate the kinds of sessions completed. Acceptance: all session artifacts validate; legacy history is preserved; one active phase is enforceable; and the ledger is generated rather than hand-maintained.
