---
type: is
id: is-01m4er1rv86xh9wy2g2evtdz2w
title: "PR461 B1: record structured refusals for deeply nested untrusted JSON"
kind: bug
status: closed
priority: 2
version: 3
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
delegate: claude-code@spud10.local
labels:
  - n-17
dependencies: []
parent_id: is-01m4eq9mdaejkedd1b09qqn09p
hold: null
hold_until: null
created_at: 2026-10-08T21:52:28.519Z
updated_at: 2026-10-08T22:32:07.206Z
started_at: 2026-10-08T21:54:45.784Z
closed_at: 2026-10-08T22:32:07.203Z
close_reason: "Fixed at reviewed5ad3d9c7, propagated with identical repair blobs to published55842c441. Whole49 controls PASS; static clean; independent Sol verification. Marked B1 disposition: https://github.com/jlevy/squares/pull/461#issuecomment-6070356717 . Original scientific receipts unchanged. Current-head CI/full checkpoint remains separately open underthink-0m0x."
resolution: null
duplicate_of: null
---
Security review B at 091f75d585/base64: deeply nested 2407-byte descriptor can parse then RecursionError during deepcopy; nested submitted mathematical payload can raise during canonical iterencode. Validate shallow descriptor contract before deepcopy and translate depth errors narrowly at untrusted input boundaries; add tiny CLI controls, preserve guards and proof-scope. Review https://github.com/jlevy/squares/pull/461#pullrequestreview-5463259834. Sol sole addressing committer; root coordinates.
