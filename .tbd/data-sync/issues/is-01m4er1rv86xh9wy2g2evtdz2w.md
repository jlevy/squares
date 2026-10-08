---
type: is
id: is-01m4er1rv86xh9wy2g2evtdz2w
title: "PR461 B1: record structured refusals for deeply nested untrusted JSON"
kind: bug
status: open
priority: 2
version: 1
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
labels:
  - n-17
dependencies: []
parent_id: is-01m4eq9mdaejkedd1b09qqn09p
created_at: 2026-10-08T21:52:28.519Z
updated_at: 2026-10-08T21:52:28.519Z
---
Security review B at 091f75d585/base64: deeply nested 2407-byte descriptor can parse then RecursionError during deepcopy; nested submitted mathematical payload can raise during canonical iterencode. Validate shallow descriptor contract before deepcopy and translate depth errors narrowly at untrusted input boundaries; add tiny CLI controls, preserve guards and proof-scope. Review https://github.com/jlevy/squares/pull/461#pullrequestreview-5463259834. Sol sole addressing committer; root coordinates.
