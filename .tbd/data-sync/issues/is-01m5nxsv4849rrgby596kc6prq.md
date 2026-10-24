---
type: is
id: is-01m5nxsv4849rrgby596kc6prq
title: "PR #759 follow-up review B"
kind: task
status: in_progress
priority: 2
version: 4
delegate: c-rev-759b-1024
labels: []
dependencies: []
parent_id: is-01m5nstg2vqmhpdnwnyhhb0vjj
child_order_hints:
  - is-01m5nzgj08fzxw206jet0qkgzq
hold: null
hold_until: null
created_at: 2026-10-24T03:03:23.016Z
updated_at: 2026-10-24T03:33:15.911Z
started_at: 2026-10-24T03:03:42.013Z
---

## Notes

2026-10-24 c-rev-759b-1024: review B (follow-up, round 2) of PR #759 published at head 3f9383d31, base da117ad0b: https://github.com/jlevy/squares/pull/759#issuecomment-6379328505
Verdict: changes requested before merge, B1 (High). A1 holds for all 28 shared-merge groups (d3860c97a as the plan states), not for carried PRs.
- B1 (High): rule 4 (plan :480-483) takes a carried PR's change as M^1..M; wrong when GitHub's mergeCommit is the PR's head (#258, #298, fast-forwarded) or merges main into its branch (#336). Real case: #298 (baseRefOid c307f646f) registers T-070..T-079 and raises 11; the rule gives all 14 registrations and 7 raises of 47569ad50 to #292. Fix: measure from the base side (M^1 when M^2 is the head, else GitHub baseRefOid, added to the fetch); refuse equal heads (#258/#249, T-061) for the reviewed backfill; fixtures for both shapes. :502-504 also says T-094..T-100 came from #362 (they came from #362, #369, #381).
- B2 (Medium): per-layer split ignores ADOPTED; d167d4b86 adopts T-195 at 29 (#661).
- B3-B9 (Low): raise-of-new-id text and the untested filter clause; S1/S2 recording past the trip point; trip scope named by function; fidelity at :1250, :880-881, :561-564; time frames ("that day", "30 days of room"); stacks vs "everything written by the tool"; stale 117/40 and stage 7 line numbers. B10 suggestion: cite why Phase 2 sits with the intake session.
A2-A18 dispositions hold (A9 decline justified), with the residues above. Checks at 3f9383d31: check_documentation (2,207 docs), check_synopsis, check_pr_description pass; merge-tree onto 14b14f2d1 clean; CI 16 pass, 41 skip, 0 fail. Scripts: scratchpad/review-759b/rule_check.py, filter_check.py, baseoid_check.py, pair_diff.py; lane's layers.py, carried.py, shape.py re-run read-only with matching output.
