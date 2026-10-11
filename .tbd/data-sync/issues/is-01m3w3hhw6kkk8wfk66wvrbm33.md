---
type: is
id: is-01m3w3hhw6kkk8wfk66wvrbm33
title: "Review 'Standing' on the results table: a workflow status (recorded, reviewed, confirmed, incomplete) in place of the present values"
kind: feature
status: closed
priority: 1
version: 7
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T16:07:45.798Z
updated_at: 2026-10-01T22:18:23.997Z
closed_at: 2026-10-01T22:18:23.993Z
close_reason: "jlevy/squares#277 merged 2026-10-01 (main 3cbbfd1c2): a derived workflow status (recorded, reviewed, confirmed, incomplete) in place of Standing; superseded its own mark; an activity mark (in analysis) on T-046, T-048, T-055. Provisional for the owner: where confirmed begins (C2), drawing 'confirmed' on most rows, the activity's shape, which activities to record."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: 'another bigger issue, let's also review the "Standing" setting on the results chart. it seems like it isn't very well thought through or useful in its current form with the data. perhaps it could be simplified to reflect the actual workflows, e.g. "recorded" to mean we've recorded the result, "reviewed", "confirmed" if this project has confirmed it, and "incomplete" if it's still a placeholder or has some other notable omissions or issues'. Scope: (1) what Standing is today: its values (current best; current best, reported; superseded; second certificate; reported; the nine non-bounds), how each is derived, how many results carry each, and what a reader can and cannot do with it; (2) a proposal: a status that follows the project's workflow, with the owner's four values as the starting vocabulary, each defined by a predicate over the record (registered; review record present; confirmed by this project per the C ladder; placeholder or with recorded omissions), derived and checked, not hand-set; how it relates to the V and C rungs (no duplication), to 'superseded' (the owner asked on the same day that superseded mark every result no longer the best: keep it as its own mark), to kind (think-69j0) and to the 'not fully assessed' tag (think-d04u, the same field); (3) implement on the branch with the schema, checker, register views, site chip and filter; (4) the classification table for the owner. Same agent as think-d04u.

## Notes

Proposal implemented on jlevy/squares#277 (c0b537b8c, main 5b3da156f merged): status derived by result_status.py, never stored: recorded (C0) 3, reviewed (C1) 4, confirmed (C2+) 56, incomplete (an open defect on record) 2 (T-058, T-059), of 65. Superseded is its own mark, asked only of a bound kind (26 marked). 'Second certificate' is the kind simplification; 'reported' is the status recorded. An optional hand-recorded activity field (in-analysis | waiting, party, what, since, link), entered on T-046, T-048, T-055. Owner decisions: the vocabulary; confirmed from C2 or C3; whether to draw 'confirmed' on 56 rows; activity as a mark (A, built) or as statuses (B); which activities to record; an omissions list; homepage default; T-065's credit and significance.
