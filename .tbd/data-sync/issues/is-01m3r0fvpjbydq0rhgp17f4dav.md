---
type: is
id: is-01m3r0fvpjbydq0rhgp17f4dav
title: Repair public case-438 near-audit final-state digest binding
kind: bug
status: open
priority: 0
version: 3
spec_path: docs/project/reviews/review-2026-09-29-n11-optimality-census-contract.md
labels:
  - n11
dependencies: []
parent_id: is-01m3qw8b5q2xgjp85cxx24134c
created_at: 2026-09-30T01:57:26.850Z
updated_at: 2026-10-03T17:15:09.376Z
---
At pinned f9e0de7, B7 near1024-independent-audit.json (decoded SHA4a93b7c8) reports source SHA491afdaa and final_state_sha256 81002706..., but canonical SHA-256 of final_state in that exact verified near-refined1024-240.json is a6d45c0c.... audit_capture_portable.py line408 claims to compute this digest from the raw source, and audit_complete_capture438.py line158 requires equality. Fixed RUN_ALL replay_candidate.py lines272-281 compares fresh geometry digest against historical B7; composition retains historical B7, so the public fresh-replay route would reject even if geometric replay succeeds. Investigate normalization/rebinding, regenerate and source-bind the audit/composition receipts, and separately validate actual source ancestry/geometry. This is a public certificate-binding defect, not a packing counterexample or theorem refutation.

## Notes

2026-10-03: Upstream main's integration of the n = 11 adversarial review (docs/project/reviews/review-2026-10-03-n11-gpt6-pro-review-integration.md, finding C3) dispositions the publisher's four stale digests as Upstream (bead think-nnrx on main). They are the publisher's release, not this project's. The paper discloses the stale bindings and the composer that checks the joins, and the old-to-new table is in the validation guide's replay section. That matches Session 168's recommendation for ceremony slice 6: keep refusing the stale near-audit final_state digest rather than accept it with a report. Lane E1's slice-6 change (bind_near, CAPTURE_CHECKER_SHA removal) was denied by the permission classifier, is not landed, and is not recommended. Awaiting the owner's confirmation.
