---
type: is
id: is-01m0thvax1hetdk00p1g1hbkrp
title: Prevent excerpt-boundary artifacts from becoming false synopsis defects
kind: bug
status: closed
priority: 2
version: 4
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
delegate: unknown@spud10.local
labels:
  - packing
  - focus-process
dependencies: []
parent_id: is-01m0t3n7z9fj0p7wwt1kn4nzqk
hold: null
hold_until: null
created_at: 2026-08-24T18:52:12.063Z
updated_at: 2026-08-24T18:58:35.219Z
started_at: 2026-08-24T18:56:46.503Z
closed_at: 2026-08-24T18:58:35.210Z
close_reason: "D-184 fixed in 29d99b1: the overlapping-excerpt false positive is corrected in the log, and check_synopsis now counts each experiment exactly once in both tables; the duplicate-row mutation fires."
resolution: null
duplicate_of: null
---
D-184. A review command printed two overlapping synopsis ranges whose shared line was exp-024, and the duplicate display was initially mistaken for a duplicate source row. Correct the finding before commit, document the conservative validity error, and make the source checker count each experiment id exactly once in both roll-up and cost tables so future duplicate claims are adjudicated against the file. Acceptance: current source passes; an actual duplicated row fails; the false source criticism is retracted.
