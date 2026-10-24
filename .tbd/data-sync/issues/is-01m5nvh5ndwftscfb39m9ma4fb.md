---
type: is
id: is-01m5nvh5ndwftscfb39m9ma4fb
title: "PR #745 follow-up review B"
kind: task
status: closed
priority: 2
version: 4
delegate: c-rev-745b-1024
labels: []
dependencies: []
parent_id: is-01m5mzwrp4a8f1drb54we5z1tq
hold: null
hold_until: null
created_at: 2026-10-24T02:23:41.741Z
updated_at: 2026-10-24T04:50:19.628Z
started_at: 2026-10-24T02:23:48.359Z
closed_at: 2026-10-24T04:50:19.622Z
close_reason: "#745 merged at af9c9e850 (head 6eaa7111e; reviews A 6372288301 and B 6379074892 with dispositions 6376964172 and 6379460703; deep gate 40050481868; CI green)"
resolution: null
duplicate_of: null
---

## Notes

2026-10-24 c-rev-745b-1024 (follow-up review lane of coord-intake-1023): Review B (follow-up, round 2) posted as a PR comment at head d8138ad5f, base 0bbb0a2c4: https://github.com/jlevy/squares/pull/745#issuecomment-6379074892

Verdict: merge-ready once two edits are made, neither of which changes the tree (so dispatch 40050481868 still certifies d8138ad5f). No Blocker or High.

Review A's dispositions: A1 (High), A2, A3, A5, A6, A7 and A8 hold. A4 does not hold: the PR body's 24 October News rewording says "verified" for T-233 again (B2).

Findings:
- B1 (Medium): the four whole fine-net sweeps stack on one xdist worker under `--dist load`, which sends consecutive chunks. On 40050481868 all four ran on gw2 (span 1676 s); gw0, gw1 and gw3 sat idle 548 to 575 s. The Step's 1800 s cap is the lane's only hard limit, since the deep-gate walls are reporting-only. A full stack on the slower class (40033801674) would end near 1850 s, a kill. post-merge slow-lane on main runs the same Step. think-tcsl's n26 receipt adds a fifth whole sweep automatically.
  - Not a merge blocker, if the beads are fixed first: give think-o8to a body, raise it to P1, and order think-tcsl after it.
  - Smallest code fix: SLOW_SUITE_BUDGET_SECONDS = 2400 for the slow step (validate.py:263, :5036-5040; test_validation_cli.py:3181-3186).
- B2 (Medium): the News details say "complete replays here verified each certificate", and think-eth9's stage 7 draft says "All four certificates verified". Use "passed" (A4's wording). These are PR body and bead-note edits only.
- B3 (Low): the seven-count evidence entry E-wand125-fine-net-lower-bounds-446-report and its blocker at n-019:133, n-020:107 and n-026:106 still say capture, controls and review are pending for the same certificates. This can ride think-tcsl's records change.
- B4 (Low, suggestion): _slow_marked misses aliased mark spellings (`from pytest import mark as mk`, getattr). This predates the PR, and no such spelling is in the tree.

Tests at d8138ad5f, nice -n 2, -n 2:
- census PR lane: 176 passed (60.5 s);
- slow-registry tests: 9 passed;
- test_deep_gate_workflow.py: 14 passed;
- check_gate_budgets: passes;
- collect -m slow on the census file: exactly the 4 whole nodes;
- independent A1 negative control (old and new _slow_marked from git): reproduces 73 identical entries plus the census file;
- the four papers re-rendered from this tree and from a 0bbb0a2c4 export (method validated byte-identical at HEAD): 67 of 69 files identical; the explainer differs only in v0.4.23, 231 -> 233 and its history entry;
- News draft: NEWS_DRAFT_VALIDATES in memory.

Main is at da117ad0b (#764, after #758). merge-tree is clean, and #764 touches no DATA_PATHS.
