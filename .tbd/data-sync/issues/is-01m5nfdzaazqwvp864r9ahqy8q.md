---
type: is
id: is-01m5nfdzaazqwvp864r9ahqy8q
title: "Triage the authors' new comments on #670, #675, #715, #719, #732 and #734 (23 October, after our replies)"
kind: task
status: closed
priority: 2
version: 5
delegate: c-triage-1023b
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-23T22:52:14.026Z
updated_at: 2026-10-24T08:26:48.584Z
started_at: 2026-10-23T22:52:20.825Z
closed_at: 2026-10-24T08:26:48.584Z
close_reason: "Triage complete; the authors' answers were taken into the record by #766 (5f8f005a3) and #769 (34eb8bb75); Couzo's 24 October comments are think-mdfr's."
resolution: null
duplicate_of: null
---

## Notes

2026-10-23 c-triage-1023b: read-only stage 1 triage of the authors' comments posted after our 23 October replies, against origin/main 64b316b6c. Nothing was committed, pushed or posted. Drafts are in the coordinator scratchpad at triage-1023b/reply-670.md, reply-715.md, reply-719.md (one paragraph), reply-732.md and reply-734.md.

Commands: `check_requests --github` from a sparse worktree of 64b316b6c listed 15 differences. `capture_kingbird_catalogue` showed 0 counts moved against the 5 October capture. The full `intake_sweep` reported 19 items with no owner, 5 resolved blockers and 2 closeable issues that are closed on GitHub but open in the record. Its regularization section was not read, because the sparse checkout left out the atlas index. Comparisons were exact, using Fraction arithmetic over Mishapolk's certified_bounds.json at f1ceee4, 34e59f3, c0bf150 and 7e82c64 against main's case records, source-coverage.yaml's current rows and the PR #574 claims. Results are in triage-1023b/*.tsv.

#670 (Couzo, 22:22:03Z): both review questions answered.
- Seed: the chain starts at Mishapolk/square-packing-records@70a033f certificates/square-204.cert, SHA-256 f0885fa8. That digest equals the T-186 packet's recorded digest for n204.cert and square-204.cert at that pin. Then n204.txt at 4e4c8ce, SHA-256 3e7c2456, which matches the author's statement. Then hop jobs 101216, 103222 and 105412, then a quarter turn.
- Measured here: n204.txt pairs with T-186's 204 packing under the identity, one to one, maximum centre distance 3.9e-12, at a side 2.78e-12 above T-186's exact side.
- Disposition: the author names T-186's lineage, so by attribution.md's chain rule T-226's credit becomes "Couzo after Polkovskyi, Ostashev, PingYou Ltd, Daniel, Levy". The short credit is unchanged. Rewrite the seed sentences in T-226's claim and notes. S3, V3/C3 and the first-report standing are unchanged, consistent with the 22 October measurement.
- The same chain should reach T-228 ([Couzo issue 675]), T-223 ([Couzo issue 678]: add Ostashev), T-225 ([Daniel regularized lists]: add Ostashev and PingYou Ltd), T-229 ([Mishapolk issue 719]: add Ostashev) and T-231 ([Mishapolk n204], on #753: add Ostashev and PingYou Ltd).
- Answer 1: verify_packing(bucket=True), closed box, wall contact only. This agrees with the replay; add it to T-226's notes.
- Record fixes: read_through; state closed and closed '2026-10-23' (GitHub closed it at 18:32:54Z through #747's "closes #670" wording, with no final comment); summary and n370, n452, n536 still say "current row" though #722 superseded them; mark the withdrawn awaiting_author question answered.
- Recommendation: leave #670 closed, post reply-670.md as its final comment after PR A merges, and do not reopen it. Reopening is an issue edit beyond what the runbook lists and would need the owner's word.

#675 (22:22:34Z): the same checker answer (88 boundary corner coordinates, no touching pairs). Record it in read_through and T-228's notes. Post nothing: we closed #675 with its final comment at 03:54:39Z, and reply-670 covers it.

#715 (22:16:52Z):
- 335: the 9 October certificate is the 8 October decimal packing, dilated by 1+1e-12 with three near-axis angles set to 0. Printed centres pack at the printed side with the certificate's rotations, and overshoot by 7.8e-16 with the binary64 angles. think-rx26 can now run both checks, under 1 CPU-minute for six counts plus a small converter. Owner question 2 decides how the record treats the row. Mishapolk's f1ceee4 335 lies 1.6e-12 below the row anyway.
- Above 1024: 1266, 1339 and 1568 refine de Winter's packings; 1061, 1413 and 1489 are Couzo's assemblies, and he asks for the credit "Couzo after de Winter's staircase/four-block constructions and Arslanov, Mustafin and Shangitbayev (2021)". For think-llit, and for the [Couzo issue 715] credit when those rows are recorded.
- Draft: reply-715.md. Combine it with #754's promised follow-up.

#719 (01:52:40Z): already read in #753 (draft, merges 24 October). Nothing new beyond the chain extension from Couzo's #670 answer, which reply-719.md adds to the coordinator's lane-719 draft.

#732 (20:35:12Z): new claims.
- f1ceee4c1dd69f97d8e50e6ddaf1a14084dceda7 has 138 certificates at 328 to 989, 18.9 MB, under MIT. All 138 lie below main's current row by more than the 12-place print, from 1.5e-12 at 924 to 8.59e-4 at 747.
- Rows they would supersede: 59 from #715, 47 from #732, 21 from #719, 9 from couzo-index, 1 from couzo-verified and 1 at 335 (couzo-extended).
- Disposition: a new import bead and PR C. Price: replay 10 to 20 CPU-minutes on two routes with six controls, ledger gather in minutes, packet about 19 MB.
- Credit split: the manifest calls all 138 refinements of Couzo topology; the comment asks for sole credit at 11 counts. Measure those 11 pose by pose; the question joins D5 (think-f2io).
- Theorems: not registered. No proof is given, and the corollary lists 11 (40.18 degrees) and 18 (24.3 degrees).
- Draft: reply-732.md.
- Later commits, no issue (needs a read):
  - 34e59f3 states T-229's sides exactly.
  - c0bf150's 51 in-corpus counts each lie above an earlier report: above PR #574's numerical rows at 49 counts by 3.9e-25 to 1.7e-24, and above his own 14 October certificates at 153 and 207.
  - 7e82c64's 303 lies above #755 (11:12:48Z).
  - None of these is recorded; the ledger confirms.

#734 (02:17:06Z): Mishapolk's support. No result; read in #753. Triage reply owed (reply-734.md). Owner question 1.

Other: #755 is handled by PR #757. #470 and #533 are other lanes' recording. chelokot/square-packing-archive and wand125/square-packing-tools have been watched only since 8c26340d9 added them to the site's other-projects list, so their old commits now show as unread. chelokot's are Bend proofs of s(1..9), s(5) and s(6)>=3 (needs a triage bead). wand125/square-packing-tools moved to wand125/square-packing (a read).

2026-10-24 coord-intake-1023: OWNER ANSWERS on the triage's two questions.
(1) #734: the owner selected "Not now". The proposal is recorded as on hold, and the reply says so (records PR A, think-t5hc).
(2) n335: the owner said "we should have clear defined process for this already, why are you asking? if it is replaced by another one, we could indicate that too". So it is not an owner question. Runbook stage 1, "Several Reports at One Count", decides it: the comparison reads a printed side as its exact side where a lane or the certificate gives one. PR C (#732's f1ceee4) runs think-rx26's exact check, keeps the 8 October print as a quote in the history, and records the supersession by Polkovskyi's lower 335. Lesson: before raising an owner question, check whether a stated rule already decides it. The process rules come first.
