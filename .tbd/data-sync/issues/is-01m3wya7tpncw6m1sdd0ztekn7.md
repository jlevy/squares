---
type: is
id: is-01m3wya7tpncw6m1sdd0ztekn7
title: "Import Daniel: the s(32) no-fold run and the checker provenance answer (#238)"
kind: task
status: closed
priority: 2
version: 8
spec_path: docs/project/specs/active/plan-2026-10-01-result-import-first-application.md
delegate: claude-code@vm
labels:
  - packing
  - result-import
dependencies: []
parent_id: is-01m3wvgebtkjqb3km59h7768zx
hold: null
hold_until: null
created_at: 2026-10-01T23:55:37.681Z
updated_at: 2026-10-05T03:21:59.448Z
started_at: 2026-10-05T03:21:47.656Z
closed_at: 2026-10-05T03:21:59.447Z
close_reason: "Done, checked 2026-10-05 in the intake triage (think-nkzt). #292 merged on 2026-10-03, so T-051 is on main. The evidence update is on main: zmx2 --full --pair-points --sym-atoms was replayed over all 28,800 roots with every census equal to the source's (E-n032-evand-zmx2-full-sym-replay, with the report E-n032-evand-zmx2-full-sym-report). T-051's composition was rewritten on what the two checkers share, including the 1 October provenance answer. The 2 October review found no blocking defect. #238 got its final reply on 2026-10-03 (issuecomment-5972353213), which corrects the 29 September reply, and was closed the same day. Daniel's ask is recorded as done. The s(21) and s(45) re-sweeps are think-l6la and think-mx3k."
resolution: null
duplicate_of: null
---
Result import process, an evidence update to T-051 with no new entry: retain zmx2_full_sym from 2bf33bc3 in the 2026-10-01 packet, replay zmx2 cert --full --pair-points --sym-atoms (11,592 CPU-s at the source), rewrite the composition and limitations on what the two checkers share, answer the comment of 2026-10-01 and correct the stale statements of the 29 September reply. The s(21), s(45) re-sweeps restart from nothing (think-l6la, think-mx3k).

## Notes

2026-10-01: stages 2 and 3 are in draft PR jlevy/squares#292 (branch claude/import-2026-10-01-requests, commit 2b7191461), stacked on #290. Stage 4 not started. The T-id is provisional until #292 is on main; quote it to no author before then.

2026-10-02 (stage 4, PR #298): zmx2.rs 92a4cfe8 retained in packing/resources/web/evand-zmx2-sym-atoms-2026-09-30/ (review finding F1); --full --pair-points --sym-atoms replay running locally, resumed from its root log after a container restart; partial census identical to the source so far. Review docs/project/reviews/review-2026-10-02-evand-s32-no-fold-run.md: Lemma A proved in the source and correct; no blocking defect.
