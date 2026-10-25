---
type: is
id: is-01m5rr1szcsazmt86mavzs7555
title: "Import #806: Evan Daniel's s(182) <= 13.970916436215 (evand d99925d), 3.17e-3 below the register"
kind: task
status: in_progress
priority: 1
version: 12
delegate: c-import-806-1025
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
child_order_hints:
  - is-01m5rs5zgh67xp4p355jr8s3ak
  - is-01m5s1x1wf05920w6vejww2ecm
hold: null
hold_until: null
created_at: 2026-10-25T05:20:35.819Z
updated_at: 2026-10-25T08:46:11.402Z
started_at: 2026-10-25T05:20:59.792Z
---
New 2026-10-25 issue https://github.com/jlevy/squares/issues/806 (evand, 04:16:24Z): s(182) <= 13.970916436215, the exact side of search/packer/candidates/s182-1024.cert at evand/square-packing d99925d1 (with .exact.txt KKT point, .input.txt, .json, _regularized.cert), 3.17e-3 below the register's 13.974090713122 (Couzo). In the case corpus (n <= 324): a register entry, stage 4 review and adoption under the house rule. Side-only Kaggle entries (Subramanya N, 2026-10-24 18:41 UTC, matching to 1.6e-11) are not reports. Also owns the read of evand/square-packing's 28 commits past the last read (head d99925d12982). Stage 1 triage read-only first.

## Notes

2026-10-25 stage 1 triage (c-triage-2lzo-1025, read-only, main bb756e193):
- Pin: evand/square-packing d99925d1298262c4ddb81c95abbb6f45adca8d3d (committed 04:11:15Z, pushed 04:16:05Z in 3c335fe..d99925d; #806 opened 04:16:24Z). s182-1024.cert 30648 B sha256 9e12e0a4...fe97 and _regularized.cert 30526 B f1ec415a...fabf match the issue's table; .exact.txt 3ed2a8a8..., .input.txt e79897cb..., .json e5491852... (issue gives no digests for these).
- Quick check: side = header = 13970916436214678735385725854133/10^30, rounds up to 13.970916436215; 3.174277e-3 below T-174 (house, both lanes); side - S_exact = 1.40e-19. One positive job on both maintained routes (kernel.run_case + validate_job): both accept, 16471 pairs, wall clearance 5e-21, pair gap ~1e-20; 4.03 CPU-s (exact_verify 2.39, independent 1.64), 4.11 s wall.
- Identity (devtools.measure_identity): vs T-174/house witness/T-098: no symmetry one to one; assignment 44 > 0.1, 79 > 1e-2, largest 0.813; 74 turned; 16 tilts reversed; no tilt angle shared. vs source input: one to one, largest 2.55e-7. vs source regularized view: same side, moves exactly its 43 flat + 6 rattler squares, 5 > 0.1 (largest 0.381).
- Report order at 182: T-056, T-098 (#375), #476, T-174 (PR #574, house), #593 (not recorded) all >= 13.97409071312...; Kaggle side-only Chavan 13.9727613470647 and Subramanya N 13.9709164362306 are no reports (no packing; the latter 1.59e-11 above). Couzo 1c17153 (head) holds T-174's side. Ledger draft upper-bounds-issue806-20261025 (scratch): #806 recorded, new packing continuing T-188; check OK.
- 28 commits: only d99925d holds a certificate; the rest are packer code, docs, deletions and private-store experiment notes (store bests only above 324, values private). Nothing else to import.
- Next free T: T-243 (unless #804 registers first in report order). Draft S3.
- Drafts: scratchpad/triage-806/drafts/ (result-requests-806.yaml validated by check_requests --record; intake-watch-read.yaml validated against schema; import-plan-806.yaml; ack-806.md; upper-bounds-issue806-20261025/).

2026-10-25 ~06:10Z coord-intake-1024 on c-triage-2lzo-1025's report: #806's certificate is the only report below the house at 182 (3.174e-3 below T-174), a new arrangement (44 squares beyond 0.1), accepted on both routes at triage; the 28 evand commits hold nothing else to import. Plan: records lane c-import-806-1025 (wt-806, branch claude/intake-2026-10-25-issue806-n182) registers T-243 at V0/C0; stage 4 review c-review-806-math (think-meci, wt-rev806) runs in parallel; if accepted before the records are green, the same PR maps V3/C3 and adopts at 182 (25 Oct: 182 has not moved today), else a second PR. No owner question.

2026-10-25 records lane (c-import-806-1025, stages 2 and 3, worktree /home/user/wt-806, branch claude/intake-2026-10-25-issue806-n182 from main bb756e193):
- Draft PR #814 (https://github.com/jlevy/squares/pull/814), labels intake and S3; head 76eb2dd52 (records f8cca02c3, release 406ebec29, re-pin 76eb2dd52).
- T-243 at V0/C0, S3 draft; E-evand-n182-certificate-report; coverage source evand-n182-2026-10-25; key [Daniel n182 2026-10-25] (Daniel after Ostashev, Couzo, Levy; builds-on-project) with five contributor spans; reader [Daniel n182 2026-10-25] in upper_bound_reports.HOUSES; activity and unfinished_confirmations name the stage 4 review (think-meci).
- Packet: 10 retained files (the 8-file s182-1024 set, 167,915 B, plus LICENSE and CREDITS.md), the two checkers pinned identical_to the n183 packet. Replay: 3 jobs, 98,826 pairs, 11.53 route CPU-s; walls 5e-21, pairs >= 9.99e-21; sharp controls all 11 as expected (45 CPU-s); identity reproduces the triage's receipt pair for pair.
- Ledger upper-bounds-issue806-20261025: recorded, new packing. #806 requests entry triage: done, register T-243; evand watch read through d99925d with no bead.
- Release: explainer v0.4.28 (243 results); no-change record for the other three papers (51 files byte-identical at link revision f8cca02c); DATA_REVISION f8cca02c. stamp_landed --apply changed nothing.
- Local: records tier exit 0, edit tier exit 0, 906 + 116 + 25 tests passed. Waiting on: hosted CI, then the review (think-meci) for V3/C3 and adoption at 182 (on the coordinator's word).

2026-10-25 records lane, stage 4 mapping and adoption (c-import-806-1025, on coord-intake-1024's word): review think-meci accepted (no blocking or major; M-1, M-2 minor; N-1 to N-8), copied byte for byte and mapped; T-243 at V3/C3, S3 confirmed; credit "Evan Daniel, from an L-cut of Francisco Couzo's 211 packing (T-188), an arrangement of Daniil Ostashev's design (T-175)"; adopted at 182 in the pass of 25 October; regularized: Evan Daniel's regularizer view drawn (the source's own s182-1024_regularized.cert to 1.9e-19); N-8 rigidity derived again (square 5 translates 0.033032; 49 of 182 squares move). PR #814.

Question rule (runbook stage 7, Close a Settled Issue): all four review questions are informational and none goes under awaiting_author. Q1 (the start's credit) is settled here: the issue's own start side, 14.993549626299, is T-188's (T-175's is 14.99369...), and the review's measurement places the start at T-188 (square 141: 0.015 from T-188, 0.442 from T-175), so no answer could falsify what the record asserts. Q2 (the cut, the store's copy) is measured (the 29 removed squares are T-188's right column and top row); which copy the store held changes no credit, since the packing is the same. Q3 (enclosure of the KKT point) and Q4 (format line) change nothing the record asserts. The triage's question on Subramanya N's packing is informational too.

DRAFT import reply for #806 (post after PR #814 merges and the deploy is verified; replaces drafts/ack-806.md):
---
Thank you, Evan. Your certificate is now in the record as [T-243](https://squaremath.org/results.html#t-243), and the case at 182 has adopted it as its best packing.

**What we pinned.** evand/square-packing at `d99925d1298262c4ddb81c95abbb6f45adca8d3d`. The eight files of the `s182-1024` set, with the licence and credits, are kept in the packet `evand-n182-2026-10-25`, and the two SHA-256 digests in your table match.

**What we checked.** The certificate's side is its header's, 13970916436214678735385725854133/10^30, and it rounds up to your 13.970916436215: 3.17e-3 below the previous best packing at 182 and below every report there. Both of this repository's exact routes accept it, and refuse its controls, including controls taken to exact contact and 10^-30 past it. An independent review ([review of 25 October](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-25-evand-n182.md)) decided it again with a clean-room checker, by separating axes and by exact clipped areas with fourteen sharp controls, and accepted it for finite feasibility. So T-243 stands at V3/C3: confirmed, independently re-implemented, by a Claude agent, a system family your commit also names. Measured pose by pose, no symmetry pairs it one to one with the previous best packing (44 squares beyond 0.1), so it is a new arrangement, as you say.

**Credit.** Evan Daniel, from an L-cut of Francisco Couzo's 211 packing (T-188), an arrangement of Daniil Ostashev's design (T-175). The start side in your issue, 14.993549626299, is T-188's, and the review found the 29 squares your 182 do not use are exactly T-188's right column and top row; where T-188 differs from Ostashev's own 211 packing, your certificate follows T-188.

**What the record states.** The upper bound only, as an upper bound: your commit title's "=" is not carried. Your KKT, local-minimum and flat-motion statements are recorded as your numerical report at 80 digits. The Kaggle side-only values are not reports, and the record does not call your side the first at this value; "the first public packing at that side" is accurate as far as we know.

**The drawing.** Both of the project's strong regularizers ran on the new house. The drawing now shown is the regularizer's view at the same side, which is your own `s182-1024_regularized.cert`, square for square.

Some questions, none of which holds anything open:

1. May the record keep crediting the start as Francisco Couzo's 211 arrangement (T-188) of Daniil Ostashev's design (T-175)?
2. Was the L the right column and the top row of the store's 211 packing in its own orientation, 15 and 15 squares sharing the corner, as measured? Did the store hold T-188's certificate poses or a binary64 copy of them?
3. Do you plan an interval or exact enclosure of the KKT point, or an argument along the 43 flat motions?
4. Would you add the corner formula and the box [0, S]^2 to your certificates' format line? The rotation sense matters: read the other way, 80 pairs overlap.
5. Do you know whether Subramanya N has published a packing at 13.9709164362306?

---
_Generated by [Claude Code](https://claude.ai/code)_
---
2026-10-25 08:15Z records lane: PR #814 head a473471df (draft, intake + S3), hosted green (Packing validation 40174785773, Certificate page 40174785646; packing-required and pages-required pass, 31 checks). Main merged once (886dddce6, #808). DATA_REVISION 6f6896bb; landings 182 -> T-243 2026-10-25. Must merge before 2026-10-26T00:00Z (the pass is dated 25 October); if main moves first, merge it with a merge commit, re-run stamp_landed --apply, re-measure the three papers (devtools renders, 51 files) and re-pin.

2026-10-25 coord-intake-1024: #814 MERGED as 46e355582 at 08:45:49Z (review A issuecomment-6395409285, dispositions issuecomment-6395553196, head 90dabab55, CI green 40177028092/40177028091). T-243 V3/C3, the house at 182 in the pass of 25 October. After the deploy: post the import reply (draft in these notes) and record it with the S3 News (PR body draft) in the next records change.
