---
type: is
id: is-01m45eydp87yaa6hyzn07pqkjd
title: "PR #347 B4 (Medium): disclose the frontier register change 4c060f233 and get it read by the register's reader"
kind: task
status: open
priority: 1
version: 3
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
delegate: null
labels: []
dependencies: []
parent_id: is-01m45ex3dssa31jvkkz9bzpc6e
hold: null
hold_until: null
created_at: 2026-10-05T07:20:11.719Z
updated_at: 2026-10-05T07:27:33.137Z
started_at: 2026-10-05T07:27:29.545Z
---
Review B finding B4 on jlevy/squares#347 (https://github.com/jlevy/squares/pull/347#pullrequestreview-5411026138), at head 9d2f05582. 4c060f233 adds E-n017-catalogue-polynomial-identity (packing/frontier/evidence.yaml:82) and V-n17-catalogue-polynomial, annotates T-065 (results.yaml:5771) and rewrites four passages of n-017.md; it is the data commit behind the DATA_REVISION re-pin. The reviewer found its evidential status consistent (derived-structure, verified, same-implementation, external review informally-verified; bound, rungs and open status unchanged). The body claims nothing about it and no reviewer of the PR has read it. Fix: list it under Results and Changes by Purpose, and have the register's usual reader check it before merge. The register work itself is think-yjgk (delivered in 4c060f233, closes when #347 merges).

## Notes

2026-10-05 07:40 UTC (bead bookkeeper). Disclosure half done in the #347 body edited at 06:45:54 UTC: Results and Dispositions (H-265 row: 'This PR updates n-017.md, T-065 and the evidence register to match (think-yjgk)') and Changes by Purpose ('Frontier record (think-yjgk)' row naming E-n017-catalogue-polynomial-identity and V-n17-catalogue-polynomial). Remaining: the register's usual reader checks 4c060f233 before merge, and the dispositions reply says so.
