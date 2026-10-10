---
type: is
id: is-01m4jr7mpcvv3wqm8280bt2x19
title: Keep website publication and frontend validation within their contracts
kind: bug
status: in_progress
priority: 1
version: 13
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels:
  - website
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-10T11:12:38.602Z
updated_at: 2026-10-10T16:00:49.174Z
started_at: 2026-10-10T11:13:19.000Z
---
Resolve PR 462 publication and frontend findings without relaxing existing contracts. Preserve script inventory refusal, native MathML readiness, stable Atlas geometry, 300 ms startup assertions, all browser checks and current effective PR hard ceiling. Retained fixes cover non-inherited Headroom clearance, concurrent browser-lane startup, canonical render setup and Atlas host reuse. Final hosted gates must pass before closure; full pre-merge checkpoint remains think-xio5.

## Notes

Final head f489084511a56b130e6d86fc46a8260f4fb530bb is committed with normal hooks and pushed to draft PR 462. Astra approved startup batching and reduced-motion corrections. Wrapper geometry now disables inherited KPress micro-transitions just as existing tile geometry does. Matched control failed immediate layout before the fix; four focused targets pass afterward with no active wrapper transitions or changed boxes. All assertions, wait policies, content and budgets retained. Startup batching removes repeated 848/832-element restyles; traced script time 201.429 to 169.435 ms, diagnostic only. Required pre-push recorded 4658 passed, 35 skipped and one stale selector oracle failure, plus unavailable tool PATH and strict probe typing failures; those were corrected. Exact oracle passed, strict probe typecheck passed, all five selected final floor steps passed in 99.19 seconds. The aggregate was not rerun after narrow corrections; full checkpoint remains think-xio5. Hosted final Packing38065629234/frontend114252561386 and Certificate38065629233 are in progress. Strict paper startup checks pass all four theme/width combinations below unchanged 300 ms: optimality259/226/256/252, threshold164/163/171/178 ms. Close only after all exact-final-head required CI passes.
