---
type: is
id: is-01m0vnvvcnsv5jh2pk96ywbz38
title: Make packing README layout check ignore cache-only migration remnants
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m0vnq7t0x9ydha20bpdxmjzk
created_at: 2026-08-25T05:21:37.673Z
updated_at: 2026-08-25T05:37:41.461Z
closed_at: 2026-08-25T05:37:41.461Z
close_reason: README inventory now ignores cache-only legacy directories without requiring Git metadata; regression passes in the long-lived checkout and the full 31-step gate.
resolution: null
duplicate_of: null
---
Post-PR23 packing-validate --fast fails in an existing checkout because devtools.check_readme inventories ROOT.iterdir() and treats ignored directories left by deleted tools/ and sqpack/ modules as durable content. Clean CI hides the failure. Reproduce with the canonical fast gate; fix the inventory to reflect Git-visible committed/untracked content, protect behavior, record the defect, and rerun validation.
