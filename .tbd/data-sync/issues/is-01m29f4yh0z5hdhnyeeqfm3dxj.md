---
type: is
id: is-01m29f4yh0z5hdhnyeeqfm3dxj
title: "P2: the branch has to reach main before anything publishes"
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m29f3zcv8kfcf70ra7fpkd1j
created_at: 2026-09-12T00:09:19.647Z
updated_at: 2026-09-12T00:09:19.647Z
---
The one strictly required step, and the only reason `/workbench/` is not live now.

Both gates in `pages.yml` are the same condition: the artifact upload (line 329) and the `deploy` job (line 490) are each `if: github.ref == 'refs/heads/main' && github.event_name != 'pull_request'`. A pull request BUILDS the page -- so a change that breaks the render fails review rather than the next deploy -- and deploys nothing.

State today: PR jlevy/squares#125, open, 94 commits ahead of `origin/main` (d507f5c7). Merging it publishes the workbench, because the path filter already names the workbench's inputs and a push to main that touches them triggers the workflow.

Before merging, it is worth having P1 in the same branch: a publish that fails on an undeclared Node is a worse first deploy than one that never started.

Depends on the Phase 6 chunks only as much as the owner wants it to. Nothing in the conversion blocks publishing -- the page is correct and gated today -- but think-g0lh's banner removal is the thing that changes what the published page CLAIMS, so see think-hvzh.
