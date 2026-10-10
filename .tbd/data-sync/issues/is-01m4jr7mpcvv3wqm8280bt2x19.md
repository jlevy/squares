---
type: is
id: is-01m4jr7mpcvv3wqm8280bt2x19
title: Keep website publication and frontend validation within their contracts
kind: bug
status: in_progress
priority: 1
version: 12
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels:
  - website
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-10T11:12:38.602Z
updated_at: 2026-10-10T15:20:36.949Z
started_at: 2026-10-10T11:13:19.000Z
---
Resolve PR 462 publication and frontend findings without relaxing existing contracts. Preserve script inventory refusal, native MathML readiness, stable Atlas geometry, 300 ms startup assertions, all browser checks and current effective PR hard ceiling. Retained fixes cover non-inherited Headroom clearance, concurrent browser-lane startup, canonical render setup and Atlas host reuse. Final hosted gates must pass before closure; full pre-merge checkpoint remains think-xio5.

## Notes

Final startup fix 16beeb1bdf8c196c66bd32cef5b531d7a91259b4 is committed with normal hooks and pushed to draft PR 462. Astra approved four files. Atlas startup now measures geometry before visibility/placement writes; the matched trace removes repeated 848/832-element restyles, script time 201.429 to 169.435 ms. Untraced longest tasks 178/174/173 to 162/154/155 ms; full content, 282 readable math hosts and CLS zero retained. New fail-closed trace regression rejects the original and passes the fix. Two full frontend controls each passed 406 site tests, four HTTP cases and 56 floor tests. Reducing site workers worsened wall 186.93 to 242.88 seconds and was discarded; no budgets or allocation changed. Pre-push: all 65 prerequisites passed; 4552 tests passed, 35 skipped, one existing concurrent subprocess-timeout failure; exact serial control passed in 5.22 seconds. Prior cf6 hosted 415.57 seconds and three 300 ms HTTP failures remain recorded in PR body. Final exact-head CI now runs Packing38063108404/frontend114245208963 and Certificate38063108313. Close only after all final required checks pass; full pre-merge checkpoint remains think-xio5.
