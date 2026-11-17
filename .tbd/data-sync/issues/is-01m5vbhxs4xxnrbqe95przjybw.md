---
type: is
id: is-01m5vbhxs4xxnrbqe95przjybw
title: Review Ryu's quarter-power and cube-root preprint chains, statement conventions and constants at the strongest tier (#414)
kind: task
status: closed
priority: 2
version: 5
delegate: bold-ritchie-l23
labels:
  - validation
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-26T05:39:55.812Z
updated_at: 2026-11-02T05:36:15.297Z
started_at: 2026-11-02T01:53:36.425Z
closed_at: 2026-11-02T05:36:15.297Z
close_reason: "#414 answered and closed: strongest-tier review accepted (#879, f54c74f6b); final comment issuecomment-6569593647 posted after deploy verified; recorded in https://github.com/jlevy/squares/pull/881 (7a4521582). Remaining: think-k3tk (Lemma 4.10 box labels)."
resolution: null
duplicate_of: null
---
The review #414's ask still needs: "Review the full preprint chain, statement conventions and numerical constants" of Sungjoon Ryu's quarter-power and cube-root deficiency preprints (squarepacker/k2-minus-c-quarter abbedcf, 5,471 TeX lines; squarepacker/k2-minus-c-cube-root 15045f9, 584 lines; both v1.0, retained in packing/resources/web/squarepacker-k2-minus-c-quarter-2026-10-07/ and squarepacker-k2-minus-c-cube-root-2026-10-07/). Opened on 26 October 2026 by w-imports-1026 to own the ask in place of think-6ptr, an in_progress lane bead under a delegate that is gone (codex@spud10.local, last update 18 October).

What is retained and done: the 8 October review (docs/project/reviews/review-2026-10-08-quarter-cube-proof-chains.md, PR #441) accepted both new chains at source-review scope, conditional on the imported v1.2 lemmas and the numerical premises; its addendum and cases/asymptotic/quarter_cube_constants.py decide 108 of 108 numerical predicates in interval arithmetic. The v1.2 dependency has its own review (review-2026-10-08-squarepacker-k2-minus-c-v12.md). Not done: an independent strongest-tier reading under today's stage 4 rule (result-import.md, "Who reviews, and when"), which writes its own findings before reading the 8 October review; Q's supplementary optimization and sensitivity tables, read as source claims and never executed; and the per-box labelling of v1.2's Lemma 4.10, which think-k3tk owns.

## Validation
- Claim: both preprints' theorems as the asymptotic register records them (frontier/asymptotic-waste-bounds.yaml), with their statement conventions (closed-set disjointness, the strict-packing equivalence) and constants.
- Run: a tbd-strong-max review sub-agent in its own worktree reads both TeX sources and the v1.2 dependency from the packets, re-derives the chains and the constants (running only code it writes), executes Q's supplementary tables, then compares its findings with the 8 October review; mapped under docs/project/reviews/ and answered on #414.
- Cost: about 6 to 10 hours of strongest-tier agent reading and writing; under 0.1 CPU-hours for the constants and tables. An estimate.
- Budget status: runnable; it needs a strong-tier lane, which the coordinator launches.
- Possible subset under the cap: not needed.
- Depends on: nothing; think-k3tk's per-box labelling stays a separate obligation the review names.
- Done when: the review is mapped, #414's ask in result-requests.yaml is marked done with its verdict, and the reply is posted.
- Machine note: none; reading only.

## Notes

2026-11-02, lane L25 (bold-ritchie-l25): #414's final comment is posted and the issue closed. Posted at 05:11:12Z, https://github.com/jlevy/squares/issues/414#issuecomment-6569593647, after #879 merged (f54c74f6b) and its Pages run 41391360284 passed verify-deployment (job 125105691468, 6,036 of 6,036 checks). Rendered with check_requests --draft 414 from that main and reconciled with think-u1kq's L23 draft; a stray pair of backticks the post put around the receipts link was removed at 05:11:46Z, and the comment then read back identical to the draft. check_requests --report on main gave #414 closeable with a final comment; closed as completed at 05:11:58Z. The reply (kind final, beads [think-k3tk]) and the close are recorded in packing/campaign/result-requests.yaml on draft PR #881 (claude/bold-ritchie-xo28us-l25, labels intake + S1). Not closed here: the coordinator closes this bead after #881 merges and check_bead_tree --before-close passes.

2026-11-02, lane L23 (bold-ritchie-l23): review done, draft PR #879 (claude/bold-ritchie-xo28us-l23), labels intake + S2. Verdict: accepted, both preprints, conditional on the v1.2 lemmas, and for Theorem A and C's Theorem 1.1 on v1.2 Lemma 4.10's box computation (think-k3tk). Eight notes F1-F8, no defect or gap. Q's supplementary Tables 4, 5 and Section 12.6 reproduce (118 of 118); all 108 predicates of quarter_cube_constants.py hold on the review's own intervals. #414's ask is done on the branch. Remaining for 'done when': merge, then post the reply drafted in think-u1kq's notes (stage 7). Not closed by the lane.
