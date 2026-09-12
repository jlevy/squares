---
type: is
id: is-01m2ayf0drt7y45xm38m8qt4q0
title: Separate BC329 operational preflight failures from invalid inputs
kind: bug
status: in_progress
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - tooling
dependencies:
  - type: blocks
    target: is-01m2as8hsq3d7dxy1z185zxeah
  - type: blocks
    target: is-01m2app5e71qnp9z5vfp9vppbp
parent_id: is-01m2as8hsq3d7dxy1z185zxeah
created_at: 2026-09-12T13:56:12.343Z
updated_at: 2026-09-12T14:06:29.227Z
---
Independent review of c516a592 reproduced that a transient source_manifest OSError is caught as invalid/preflight-invalid with exit 2. Define the preflight exception taxonomy so malformed or mismatched invocation evidence remains invalid while I/O, process-launch, Git execution, timeout, and other operational failures are retained as unresolved operational outcomes. Preserve exact failure provenance without permitting acceptance, add positive and negative controls for representative failures, and verify the outer reader/state machine cannot confuse them with scientific rejection. Re-run focused tests, Ruff, BasedPyright, formatting, and source-distinct review. No BC329 target may run before closure.
