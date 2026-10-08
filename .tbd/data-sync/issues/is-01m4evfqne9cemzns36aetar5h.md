---
type: is
id: is-01m4evfqne9cemzns36aetar5h
title: "n17 PR404 B1: reject colliding producer output paths"
kind: bug
status: in_progress
priority: 2
version: 2
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
delegate: sol-merge-engineering
labels:
  - n-17
dependencies: []
parent_id: is-01m4eq9mdaejkedd1b09qqn09p
hold: null
hold_until: null
created_at: 2026-10-08T22:52:31.789Z
updated_at: 2026-10-08T23:01:03.096Z
started_at: 2026-10-08T23:01:03.092Z
---
PR404 full review B1, pinned head 1d1691bf5e6e1115ad1597b5f72bbd12ad9b0b88.

The conditional-owned-hull producer accepts the same path for --output and
--child-output. It first publishes the child gzip and then overwrites it with the
JSON report, while returning success and retaining the obsolete child SHA.
Distinct paths pass the tiny control; colliding paths return exit 0 with BadGzipFile
and a digest mismatch when independently read.

Reject colliding resolved output paths before publishing either output, preserve
existing files on refusal, and add a small regression control. Consider existing
symlink/hardlink aliases consistently with the command's file publication contract.
Keep mathematical scope and original evidence unchanged.

Evidence: attic/n17-merge-readiness-20261008/pr404-tiny-review-controls.json.
