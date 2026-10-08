---
type: is
id: is-01m4e2d5gyj7m218hm9f5g01xd
title: "PR #395: verify merged Pages rollout end to end"
kind: task
status: in_progress
priority: 1
version: 5
delegate: codex-pr395-site-review
labels:
  - pages
  - verification
dependencies: []
child_order_hints:
  - is-01m4e37ersbgmvw7ana72wd5an
  - is-01m4edxmfwe4ey36yag3yg9zz6
  - is-01m4edy0gkgv91t6evhbzeyk58
hold: null
hold_until: null
created_at: 2026-10-08T15:34:13.277Z
updated_at: 2026-10-08T18:55:39.537Z
started_at: 2026-10-08T15:38:21.259Z
---
Verify the user-authorized merged PR #395 rollout at 91378153846b718a6626167c70b790b5761ec4cf. Require exact-merge Packing full105, Pages producers/publication, actual deploy and registry-driven verify-deployment success; independently check live static/no-JavaScript content, SEO and historical URL behavior plus HTTPS, gzip, cache headers, sitemap and unknown-path 404. Root owns mutations and records; use task external storage, preserve unique evidence, and do not claim owner Search Console account acceptance without a supplied token/property.
