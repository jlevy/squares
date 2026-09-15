---
type: is
id: is-01m29f4zbw0vv3xj1xbe95narx
title: Wire post-deployment checks for the packaged workbench
kind: task
status: open
priority: 3
version: 5
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
  - workbench-phase-4
dependencies:
  - type: blocks
    target: is-01m2cm03rtrjcg98ejb9y56jn6
parent_id: is-01m29f3zcv8kfcf70ra7fpkd1j
created_at: 2026-09-12T00:09:20.507Z
updated_at: 2026-09-15T02:41:47.776Z
---
Implement the post-deploy workbench check before the phase-4 release checkpoint. Verify /squares/workbench/ returns the expected deployed source/build identity and can start its public app API, with project-relative navigation and required static assets. Extend the existing published-site mechanism; do not assume the future API keeps window.atlasTransitions or add repository-integrity checksums. Test against a served package artifact and negative wrong/stale/missing artifact controls. The actual live deployment receipt is recorded by think-tn6s after authorized release, so this implementation task does not depend on the deployment it enables.

## Notes

2026-09-14, PR #160 review lane D-tools (D90, bead think-g1ry, closed at 2782c27e): `check_published_site` retries transient answers (unreachable, 404, 408, 429, 5xx) after 2, 4, 8 and 16 s, and `verify-deployment` installs the headless shell its cache key holds. The published page now carries a `default-src 'none'` CSP (D56, 269fefcc), which a post-deploy check could assert. A deployed receipt is still owed.
