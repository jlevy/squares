---
type: is
id: is-01m4zq0njqcj232mhnhc0nwfa3
title: Reuse one audited same-tree deferred worker after an already-green PR checkpoint
kind: feature
status: closed
priority: 1
version: 7
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4xkf4v65pthd9zbd7a5a3qv
child_order_hints:
  - is-01m4zrde9aa1104xe4yekwvtpq
  - is-01m4zs1d6rdqasgbagzvkaes56
  - is-01m4zs1dnx2rk5tn9zkeyf49ws
  - is-01m4zs2fv9hfmsbpjdkxb47p94
hold: null
hold_until: null
created_at: 2026-10-15T12:01:29.168Z
updated_at: 2026-10-15T12:50:15.463Z
started_at: 2026-10-15T12:01:54.618Z
closed_at: 2026-10-15T12:50:15.462Z
close_reason: Retired before activation after independent source-provenance review. GitHub metadata identifies PR HEAD but cannot authenticate which merged workflow/source executed after associations disappear. Exact six-file candidate is preserved and reverse-apply verified in deferred-worker-reuse/retired-final.patch at basefc2; 88 passing focused tests do not close E1. D1/D2/E2 fixes remain prototype evidence only, with no production speed claim. All six source paths restored; no new proof framework. Separate live fast-proof issue is actively fixed under think-3d1m.
resolution: null
duplicate_of: null
---
PR618 selected full Deferred checkpoint38726327460 finished green, then mergefc2ceae triggered mainPacking38730161853 to repeat all deferred work. Extend the existing verified_merge_tree/native workflow mechanism only for one positively audited worker (prefer the slow behavioral lane if recipe/runtime/selection equivalence can actually be proved; otherwise choose a sound bounded family). Preserve source/base/runtime-tree and successful aggregate/worker binding, stale/missing/failed/dispatch ambiguity falls back to rerun, existing strict/wall gates remain, and main/scheduled cold full stays explicitly selectable. No new generic cache, ledger, checksum system, API-per-node checker or global skip-by-label. Measure retained proof and host/critical-path cost accurately; one worker may save allocation without reducing total critical path. Require independent security/correctness review and negative controls before activation. Separate from paused witness experiment and unactivated upper-report prototype.
