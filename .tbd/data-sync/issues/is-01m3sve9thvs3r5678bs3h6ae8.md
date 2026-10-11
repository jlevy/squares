---
type: is
id: is-01m3sve9thvs3r5678bs3h6ae8
title: Promote measured canonical Rust multiplication with preserved exact controls
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3rcka78kmcccpetknr2mswh
created_at: 2026-09-30T19:07:41.776Z
updated_at: 2026-09-30T19:07:41.776Z
---
The source-reviewed canonical helper passed the fixed-kernel ablation and think-ss4a bounded whole-verifier experiment: external 1000-node Rust child CPU median -14.49%, invocation wall median -17.85%, exact normalized reports identical in all12 runs. Review a narrow production-default promotion of the existing helper, preserve differential210-polygon/10-refusal/analytic201/external-capped controls and the reference path, and remove redundant experimental scaffolding only if retained receipts remain reproducible. Keep this separate from remaining GCD/allocation/library diagnosis and full external certificate acceptance; the timed external case remains INCONCLUSIVE. Report review and validation on a PR; no blanket Rust/Python or full-proof performance claim.
