---
type: is
id: is-01m4zq0njqcj232mhnhc0nwfa3
title: Reuse one audited same-tree deferred worker after an already-green PR checkpoint
kind: feature
status: in_progress
priority: 1
version: 6
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
updated_at: 2026-10-15T12:37:25.992Z
started_at: 2026-10-15T12:01:54.618Z
---
PR618 selected full Deferred checkpoint38726327460 finished green, then mergefc2ceae triggered mainPacking38730161853 to repeat all deferred work. Extend the existing verified_merge_tree/native workflow mechanism only for one positively audited worker (prefer the slow behavioral lane if recipe/runtime/selection equivalence can actually be proved; otherwise choose a sound bounded family). Preserve source/base/runtime-tree and successful aggregate/worker binding, stale/missing/failed/dispatch ambiguity falls back to rerun, existing strict/wall gates remain, and main/scheduled cold full stays explicitly selectable. No new generic cache, ledger, checksum system, API-per-node checker or global skip-by-label. Measure retained proof and host/critical-path cost accurately; one worker may save allocation without reducing total critical path. Require independent security/correctness review and negative controls before activation. Separate from paused witness experiment and unactivated upper-report prototype.
