---
type: is
id: is-01m2ayf0drt7y45xm38m8qt4q0
title: Separate BC329 operational preflight failures from invalid inputs
kind: bug
status: in_progress
priority: 1
version: 7
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
updated_at: 2026-09-12T15:25:35.095Z
---
Independent review of c516a592 reproduced that a transient source_manifest OSError is caught as invalid/preflight-invalid with exit 2. Define the preflight exception taxonomy so malformed or mismatched invocation evidence remains invalid while I/O, process-launch, Git execution, timeout, and other operational failures are retained as unresolved operational outcomes. Preserve exact failure provenance without permitting acceptance, add positive and negative controls for representative failures, and verify the outer reader/state machine cannot confuse them with scientific rejection. Re-run focused tests, Ruff, BasedPyright, formatting, and source-distinct review. No BC329 target may run before closure.

## Notes

Follow-up repair implemented in d6bbe20172d4048a9f156b1c3c4fcfe8f1b64014 on top of original repair 1a5a8565eb7d8a4ed5c8dfc1979a2d3af5c034fe (integrated as 2179b327). OSError while reading .python-version or uv.lock now becomes PacketOperationalError with concrete type and message, while TOML parse defects remain PacketError. The maintained run_worker probe faults the actual uv.lock Path.read_text boundary and observes return 1 with partial/preflight-failed/unresolved. Leave open for source-distinct re-review.
