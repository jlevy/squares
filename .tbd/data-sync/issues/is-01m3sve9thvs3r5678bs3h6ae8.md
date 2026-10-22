---
type: is
id: is-01m3sve9thvs3r5678bs3h6ae8
title: Promote measured canonical Rust multiplication with preserved exact controls
kind: task
status: in_progress
priority: 1
version: 6
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
delegate: codex-canonical-mul-20261019-01a14e4c
labels: []
dependencies: []
parent_id: is-01m3rcka78kmcccpetknr2mswh
child_order_hints:
  - is-01m58s1w7z9abmjrqzj8kj887s
  - is-01m58shfawc7mp4fc4j27vcwwj
  - is-01m59havhefsk1728hmt9ybfcq
hold: null
hold_until: null
created_at: 2026-09-30T19:07:41.776Z
updated_at: 2026-10-22T09:24:15.205Z
started_at: 2026-10-19T00:26:20.926Z
---
The source-reviewed canonical helper passed the fixed-kernel ablation and think-ss4a bounded whole-verifier experiment: external 1000-node Rust child CPU median -14.49%, invocation wall median -17.85%, exact normalized reports identical in all12 runs. Review a narrow production-default promotion of the existing helper, preserve differential210-polygon/10-refusal/analytic201/external-capped controls and the reference path, and remove redundant experimental scaffolding only if retained receipts remain reproducible. Keep this separate from remaining GCD/allocation/library diagnosis and full external certificate acceptance; the timed external case remains INCONCLUSIVE. Report review and validation on a PR; no blanket Rust/Python or full-proof performance claim.

## Notes

2026-10-22 coordinator recovery:
The narrow canonical multiplication promotion is qualified and merged in PR679 as e952755bcad005738785ab8bab0d0b7176f34fed. Independent recovery review confirmed A1-A3 dispositions, reviews B-F, final ordinary/deferred source identity, and successful actual-merge full Packing run39221529063 and Pages run39221529174. Keep this task open because stopped historical Session187 still declares certification_pending: think-1ozu. No certification of the unpublished local timing/release tree or external capped certificate is inferred.
