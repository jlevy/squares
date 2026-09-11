---
type: is
id: is-01m2945bnpzyf0jkgv9w3mcjcv
title: smoke_styles.py asserts behaviour three revisions old
kind: bug
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-11T20:57:18.773Z
updated_at: 2026-09-11T20:57:18.773Z
---
`smoke_styles.py` reports six failures against the current page, identical before and after Phase 6B's lint pass, so pre-existing and not caused by it: the page does not start in the tween, the `p` key reaches no style, and the view is not held at n's scale mid-move.

At least the first is the instrument being stale rather than the page being wrong: revision 14 made the tween Animate's, so entering Pack -- which is where the page opens -- coerces the style to the physics and says so under the select. An instrument asserting the page starts in the tween is asserting a rule that was deliberately changed.

Work out which of the six are stale expectations and which are real, then either update the assertions with the revision that changed them or fix the page. An instrument that fails for known reasons teaches everyone to ignore it, which is worse than not having it.
