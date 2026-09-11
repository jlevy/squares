---
type: is
id: is-01m29bhrhcs1zrcbfbhgwbb86n
title: Two descriptions of the workbench API, and they will drift
kind: chore
status: open
priority: 3
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m299tcsrh44b8n8m1c6jpgcb
created_at: 2026-09-11T23:06:25.195Z
updated_at: 2026-09-11T23:06:25.195Z
---
The type gate produced the same knowledge twice, in parallel:

- `probes/atlas-transitions.d.ts` -- 643 lines, ~30 named interfaces, string-literal unions read off the page's own whitelists, cross-checked key by key against the object the page exports (114 keys, all declared, nothing declared that is not there).
- a `WorkbenchApi` JSDoc typedef inside `assets/workbench.js`, written by the other lane for its own `window.atlasTransitions` handle.

They agree today -- the 114-key cross-check was re-run after both landed -- and they are in different type programs, so nothing makes them agree tomorrow.

The .d.ts is the fuller description and the one derived from the source, so it should be the single reference: have `workbench.js` point at it rather than restate it, or generate the typedef from it. Whatever the shape, add the key cross-check to `check_probes.py` or to the browser floor so a drift is a failure rather than a discovery.
