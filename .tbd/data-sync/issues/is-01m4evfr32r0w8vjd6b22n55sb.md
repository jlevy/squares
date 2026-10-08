---
type: is
id: is-01m4evfr32r0w8vjd6b22n55sb
title: "n17 PR404 B2: retain structured refusal for malformed input boundaries"
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
created_at: 2026-10-08T22:52:32.225Z
updated_at: 2026-10-08T23:01:03.110Z
started_at: 2026-10-08T23:01:03.110Z
---
PR404 full review B2, pinned head 1d1691bf5e6e1115ad1597b5f72bbd12ad9b0b88.

Tiny malformed inputs escape the documented structured refusal boundary:
run_registered_phases accepts a 2,412-byte nested-array manifest into finite_tree,
whose recursive walk raises uncaught RecursionError; full-square partner coupling
deepcopies a 2,467-byte valid-schema descriptor with an unused nested-array field
before validating its flat descriptor roles; conditional hull verification lets a
checksum-matching truncated child gzip raise uncaught EOFError.

Validate flat descriptor shape before copying, translate recursion failures only
at submitted-input traversal boundaries, and translate truncated gzip at the
stream decoder boundary. Preserve propagation of unrelated programming errors.
Add target-free controls for each demonstrated boundary and ordinary valid/refused
controls. Generic CPython 3.14 JSON decoder recursion was NOT reproduced.

Evidence: attic/n17-merge-readiness-20261008/pr404-tiny-review-controls.json and
pr404-tiny-deepcopy-controls.json.
