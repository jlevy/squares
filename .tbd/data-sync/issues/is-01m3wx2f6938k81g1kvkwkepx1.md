---
type: is
id: is-01m3wx2f6938k81g1kvkwkepx1
title: Gate the verified lane for a result by others on a replay here and a mapped review
kind: task
status: in_progress
priority: 1
version: 3
delegate: c-gates-1023
labels:
  - packing
  - result-import
dependencies: []
parent_id: is-01m3nrt5zy2g6dpegq1fbczpzg
hold: null
hold_until: null
created_at: 2026-10-01T23:33:54.505Z
updated_at: 2026-10-23T07:51:39.369Z
started_at: 2026-10-23T06:19:06.068Z
---
W7, trust boundary. packing/frontier/README.md says the verified lane takes a result by others only after a complete replay here and a review of its mathematics. Nothing enforces either: assurance.py admits any assurance: verified evidence, origin external included, and no check ties a verified-lane value to a review. T-056 and T-057 reached the verified lane with replay entries carrying neither audit_record nor external_review. Add the check with negative controls. Prerequisite for recording a source-run certificate as V3/C0 (owner decision 1 in the process review).

## Notes

2026-10-23 c-gates-1023 (PR #748): negative control first: a verified lower bound seeded on a recent result by others. sqpack.assurance.check_case_semantics (verified_here) already refused the producer's own machine run, but passed a published proof nobody here read and a replay here with no review, so a gate was added: check_results.verified_lane_review_problems requires, for a verified case bound on a result by others dated from 22 August 2026, a register entry citing that evidence and covering the count with a `reviews` entry, or a qualifying external_review / proof.audit_record naming a mapped review document. On main it refused T-086's 16 counts; review-2026-10-02-nagamochi-lemma1-karakus.md is now mapped in T-086's reviews (no rung moves). Commit 3a8572e44; tests test_a_verified_bound_by_others_with_no_mapped_review_is_refused (three seeded shapes) and test_a_mapped_review_on_the_entry_or_a_read_naming_one_lets_the_value_stand.
