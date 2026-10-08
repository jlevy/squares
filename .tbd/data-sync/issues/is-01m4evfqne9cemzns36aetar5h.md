---
type: is
id: is-01m4evfqne9cemzns36aetar5h
title: "n17 PR404 B1: reject colliding producer output paths"
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
created_at: 2026-10-08T22:52:31.789Z
updated_at: 2026-10-08T23:45:17.050Z
started_at: 2026-10-08T23:01:03.092Z
closed_at: 2026-10-08T23:45:17.049Z
close_reason: Implemented B1/B2 boundary fixes at 0a8b46e1357a3891604a5a3d7f1e8c5ed80230a1, integrated 18e3a6f4f20f534e80074131d4947c633cca5ef3, with 366 retained target-free affected controls and verified PR404 B disposition. Closing only these findings; current required CI/full checkpoint remain under think-0m0x.
resolution: null
duplicate_of: null
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

## Notes

Implemented scope: refuse report/child-output aliases before checker import, scientific reads or output writes. Same, resolved, symlink and hardlink aliases preserve existing files on refusal; distinct paths retain the correct child digest. The producer module contributed 39 controls to the combined batch. Broader input/output alias hypotheses are outside this finding.

Implemented in PR404 repair commit 0a8b46e1357a3891604a5a3d7f1e8c5ed80230a1, integrated head 18e3a6f4f20f534e80074131d4947c633cca5ef3; original reviewed head 1d1691bf5e6e1115ad1597b5f72bbd12ad9b0b88. Verified B disposition: https://github.com/jlevy/squares/pull/404#issuecomment-6071219969.

Retained combined B1/B2 batch: 366 target-free affected controls PASS across ten modules, 0 deselections, summed pytest 23.94s / process 26.673s. A subsequent test-style-only adapter check passed 6 controls with 46 deselections and is excluded from the 366 total. Ruff/format and BasedPyright over 15 owned repair paths were clean. Evidence: attic/n17-merge-readiness-20261008/pr404-b1b2-tests-final.json, pr404-b1b2-static-final.json, pr404-b1b2-final-checks.json and pr404-b1b2-repair-handoff.md.

Closing only the implemented finding scope. Retained local controls do not establish a full checkpoint or current required CI; A1 remains open under think-0m0x. Mathematical criteria, bounds, admissions, original research receipts and persistent resource caps are unchanged. No new tests/builds were run for this bookkeeping.
