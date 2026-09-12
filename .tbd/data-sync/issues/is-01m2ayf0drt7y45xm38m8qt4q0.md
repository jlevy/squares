---
type: is
id: is-01m2ayf0drt7y45xm38m8qt4q0
title: Separate BC329 operational preflight failures from invalid inputs
kind: bug
status: in_progress
priority: 1
version: 5
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
updated_at: 2026-09-12T14:33:17.950Z
---
Independent review of c516a592 reproduced that a transient source_manifest OSError is caught as invalid/preflight-invalid with exit 2. Define the preflight exception taxonomy so malformed or mismatched invocation evidence remains invalid while I/O, process-launch, Git execution, timeout, and other operational failures are retained as unresolved operational outcomes. Preserve exact failure provenance without permitting acceptance, add positive and negative controls for representative failures, and verify the outer reader/state machine cannot confuse them with scientific rejection. Re-run focused tests, Ruff, BasedPyright, formatting, and source-distinct review. No BC329 target may run before closure.

## Notes

Repair committed as 1a5a8565eb7d8a4ed5c8dfc1979a2d3af5c034fe. Malformed or mismatched evidence remains invalid with exit 2; I/O, Git execution, import, process-launch, and unexpected host failures retain partial/preflight-failed/unresolved receipts with exact exception provenance and exit 1. Reader controls reject the preflight schema as scientific evidence. Validation: 98 fixed-core tests passed in 11.40 s; repository Ruff and BasedPyright reported zero findings; packing-validate --edit passed in 55.66 s. Keep open pending source-distinct review. BC329 was not registered or run.
