---
type: is
id: is-01m50x9t934x68scj1vqnwfd5c
title: Retain browser failure journals and add bounded manual diagnostics
kind: bug
status: in_progress
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m50kwed71nqmh914z0mh5103
hold: null
hold_until: null
created_at: 2026-10-15T23:10:34.774Z
updated_at: 2026-10-16T02:00:43.805Z
started_at: 2026-10-15T23:11:37.214Z
---
PR634 run38819302541 exposed900s frontend timeout and anonymous F. Native _run enables progress only for quick/slow marker strings; custom browser -k commands lack journals. Enable accurate browser phase/node journals and immediate failed trace retention without changing test selection, worker caps or hard limits. Extend existing dispatch-only browser diagnostic entry point with fixed120s known-node and180s forwarder-module observations, DEBUGP wire logs, required Chromium and retained artifacts. Preserve default font diagnostic and keep all new diagnostic work off ordinaryPR/push triggers. Diagnose actual Linux failure before another full-run iteration.

## Notes

2026-10-16 continuation: Maintained fixed-choice diagnostics and explicit browser progress now in PR634 heada85eb74a66c6e695faee8bc5e6c42a5cbb769a00. Linux diagnostics38823195740/38823480441 passed1/51 tests respectively, zero skips,25.871s/77.874s command wall; these observations do not identify original shared-process stall.35 diagnostic controls and19 existing controls passed; security/source review publication and ordinary current-head CI pending.

2026-10-16 final integration: formal stack635 now targets main ee9cec6e after intake632 and S1 replies626/625. News633 head e31ca7787b1e0838c07a195f71802b6ee7cf6788; CI634 head098009354b4191d774f56f659e0fa90706c1f2a4. Sitev0.7.12, inherited scientific pin e35725f0 and claim source6ba43f14. Separate T191/T192 S3 V0/C0 stories retain unchanged standing bounds; shared delivery keeps full audit/frozen provenance.63 focused tests passed17.60s after2 expected-red controls; sitecut111passed/15deselected90.99s; native70passed155.56s and Python types0errors170.71s before the two metadata-only rebases. Requests, claim generation and final publication/URL contracts rechecked (48.14s). Final current-head reviews and ordinaryCI are pending; do not close until merge/live verification. Prior8d/78df all4workflows passed with actual51forwarders/0skips and original900s shareddeadline. New metadata-churn followup think-m2fn; original causal stall and broader3min goal remain open.
