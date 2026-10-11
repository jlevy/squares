---
type: is
id: is-01m4m588mffw9ac4ssy5qa9hhd
title: Reconcile final website contracts and URL registry after recency cleanup
kind: task
status: in_progress
priority: 1
version: 8
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
child_order_hints:
  - is-01m4m5cazc8r1phkrxezd8w47v
  - is-01m4m5zp4crkv9ywx7hd793jks
  - is-01m4m61h43ajxan7q3kn2b3n4n
  - is-01m4m6xh7z5y890je82kt3s9nf
  - is-01m4m6yg8cnpm1pz0jsg77jv2n
hold: null
hold_until: null
created_at: 2026-10-11T00:19:24.942Z
updated_at: 2026-10-11T00:57:53.607Z
started_at: 2026-10-11T00:19:34.475Z
---
Current-head CI found two obsolete result-panel star assertions and generated URL registry drift. Preserve all math, geometry, citations and historic aliases while updating the assertions for red recency and regenerating the register with its maintained producer. Verify affected tests and current/historic URL contract before the final fix push.

## Notes

Stabilization e047478b8 includes all mapped CI repairs: expired measurement waiver replaced without changing90s ceiling; URL dates regenerated; stale user-intent oracles repaired. Overview302passes+repairedtarget1pass; Headroom17pass with actual startup-race regression; gray z-layer3pass. Final hosted validation38100002326 and matching checkpoint38099999269 running.
