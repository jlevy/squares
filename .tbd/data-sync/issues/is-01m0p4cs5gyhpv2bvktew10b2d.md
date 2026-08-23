---
type: is
id: is-01m0p4cs5gyhpv2bvktew10b2d
title: Reconcile sqsearch with the sqpack-core architecture
kind: task
status: open
priority: 3
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0p4cr8nk338kqtbksaf63f9
created_at: 2026-08-23T01:40:05.935Z
updated_at: 2026-08-23T02:05:15.208Z
---
RESOLVED by measurement, kept for the record and for the one open sub-decision. The pipeline was priced: annealer move 0.025us, ctypes call 0.52us, JSONL round-trip 18.3us, LP quench 1283us, exact verify 129000us. Transport speed decides nothing - at candidate granularity ctypes is 0.04% of a quench and JSONL 1.4%. Decision: sqsearch stays a native binary behind a JSONL seam (no rewrite); PyO3 deferred indefinitely because the certificate must serialize to JSON anyway for Lean; a cdylib+ctypes seam is the escalation if quench-in-loop is ever needed. Numba rejected: equal speed to Rust but pins numpy<2.5 and has opaque typing errors, the worst failure mode unattended. Recorded in the plan spec under 'Stack and boundaries'. Remaining open: whether sqpack-core eventually absorbs sqsearch's geometry, which Phase 5 decides.
