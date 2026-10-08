---
type: is
id: is-01m4evfr32r0w8vjd6b22n55sb
title: "n17 PR404 B2: retain structured refusal for malformed input boundaries"
kind: bug
status: closed
priority: 2
version: 4
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
delegate: sol-merge-engineering
labels:
  - n-17
dependencies: []
parent_id: is-01m4eq9mdaejkedd1b09qqn09p
hold: null
hold_until: null
created_at: 2026-10-08T22:52:32.225Z
updated_at: 2026-10-08T23:45:17.061Z
started_at: 2026-10-08T23:01:03.110Z
closed_at: 2026-10-08T23:45:17.061Z
close_reason: Implemented B1/B2 boundary fixes at 0a8b46e1357a3891604a5a3d7f1e8c5ed80230a1, integrated 18e3a6f4f20f534e80074131d4947c633cca5ef3, with 366 retained target-free affected controls and verified PR404 B disposition. Closing only these findings; current required CI/full checkpoint remain under think-0m0x.
resolution: null
duplicate_of: null
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

## Notes

Implemented scope: iterative finite-value traversal preserves valid metadata without recursive descent; full-square validates the exact flat schema and string INPUTS paths/hashes before shallow adaptation. Guard-conditioned ownership, n11 corner-cardinality, incircle projection/disk and two-center regional adapters use shallow schema adaptation before inherited intake, avoiding traversal of unknown nested fields. Conditional child-stream reads normalize truncated gzip EOF only at the submitted decoder boundary; unrelated programming failures propagate. Envelope-windows registry I/O centrally maps CalledProcessError/YAMLError to ValueError and TimeoutExpired to finite.IncompleteError, chaining original causes. Tiny valid/refused, unknown-nested-field, initial/final EOF, git/YAML and programming-error controls cover these boundaries. No global JSON-depth cap or broad exception catch was added.

Implemented in PR404 repair commit 0a8b46e1357a3891604a5a3d7f1e8c5ed80230a1, integrated head 18e3a6f4f20f534e80074131d4947c633cca5ef3; original reviewed head 1d1691bf5e6e1115ad1597b5f72bbd12ad9b0b88. Verified B disposition: https://github.com/jlevy/squares/pull/404#issuecomment-6071219969.

Retained combined B1/B2 batch: 366 target-free affected controls PASS across ten modules, 0 deselections, summed pytest 23.94s / process 26.673s. A subsequent test-style-only adapter check passed 6 controls with 46 deselections and is excluded from the 366 total. Ruff/format and BasedPyright over 15 owned repair paths were clean. Evidence: attic/n17-merge-readiness-20261008/pr404-b1b2-tests-final.json, pr404-b1b2-static-final.json, pr404-b1b2-final-checks.json and pr404-b1b2-repair-handoff.md.

Closing only the implemented finding scope. Retained local controls do not establish a full checkpoint or current required CI; A1 remains open under think-0m0x. Mathematical criteria, bounds, admissions, original research receipts and persistent resource caps are unchanged. No new tests/builds were run for this bookkeeping.
