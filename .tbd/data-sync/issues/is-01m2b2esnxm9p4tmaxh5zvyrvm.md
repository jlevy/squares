---
type: is
id: is-01m2b2esnxm9p4tmaxh5zvyrvm
title: Classify BC329 packet-runner process-launch failures without losing evidence
kind: bug
status: closed
priority: 1
version: 7
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: Sol xhigh repair; source-distinct rereview; root integration
labels:
  - n11
  - tooling
dependencies:
  - type: blocks
    target: is-01m2as8hsq3d7dxy1z185zxeah
parent_id: is-01m2as8hsq3d7dxy1z185zxeah
created_at: 2026-09-12T15:05:59.729Z
updated_at: 2026-09-12T15:39:04.590Z
closed_at: 2026-09-12T15:39:04.590Z
close_reason: "Integrated repair d6bbe201 passed source-distinct behavior review on d924a4bf: uv.lock OSError stays operational with exit 1 and an unresolved receipt; normal, linked, common, separate, and symlinked Git administrative paths refuse before mutation; OSError and MemoryError launch failures return 1 with schema-valid launch-failed provenance. Focused controls, Ruff lint, and BasedPyright pass. The unrelated formatting drift from 8d21f58a remains on think-yiay; no scientific target ran."
resolution: null
duplicate_of: null
---
The source-distinct repair review reproduced that a non-OSError host failure from Popen is reported as supervisor-interrupted, drops the original message, and re-raises instead of producing a coherent operational terminal record. Define the allowed launch failure classes, preserve the concrete error, publish a schema-valid non-scientific disposition, reap any partially created process group, and retain adversarial controls for OSError and non-OSError launch failures. No BC329 target may run until this closes.

## Notes

Repair implemented in d6bbe20172d4048a9f156b1c3c4fcfe8f1b64014. Ordinary Exception failures from Popen, including the reproduced MemoryError, are recorded as launch-failed with the concrete type/message and return 1; OSError keeps its existing operational message. _SupervisorSignal and KeyboardInterrupt remain on cleanup-and-propagation paths. Maintained OSError, MemoryError, SIGTERM, and SIGHUP controls pass. Leave open for source-distinct re-review.
