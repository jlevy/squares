---
type: is
id: is-01m0vj2qwwqvw4h0anbydgathr
title: "PR #23 review R19: Remove the cross-layer private certificate import"
kind: bug
status: closed
priority: 3
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
delegate: codex@spud10
labels:
  - engineering-maturity
  - pr-review
  - pr-23
dependencies: []
parent_id: is-01m0vj13yefxcxhhew81ewfpvq
hold: null
hold_until: null
created_at: 2026-08-25T04:15:29.179Z
updated_at: 2026-08-25T04:44:41.694Z
started_at: 2026-08-25T04:16:15.565Z
closed_at: 2026-08-25T04:44:41.693Z
close_reason: "Completed in 69e65eb: canonical_graph_certificate is a public research API and the devtool no longer imports a private package member."
resolution: null
duplicate_of: null
---
PR 23 review R19. Files: explorations/packing/devtools/check_canonical.py and src/sqpack/research/canonical.py. Promote the certificate operation to a supported public API or move the assertion beside package tests.
