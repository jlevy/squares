---
type: is
id: is-01m474b3danvrq5dr74c1hdzhv
title: "Answer #375 (evand exact optima of 48 records): acknowledgement, verdict reply from the lane, then the reply from main and the close"
kind: task
status: in_progress
priority: 2
version: 7
delegate: bold-ritchie-l7
labels:
  - result-import
dependencies: []
parent_id: is-01m482krnapg9vxqd91zjrg171
hold: null
hold_until: null
created_at: 2026-10-05T22:53:21.706Z
updated_at: 2026-10-31T12:10:48.661Z
started_at: 2026-10-31T11:31:48.792Z
---
Replies owed on jlevy/squares#375. Posted 2026-10-05: the stage-1 acknowledgement (https://github.com/jlevy/squares/issues/375#issuecomment-6004562871). Lane F (think-t6ok) posts a verdict reply once its records are committed, stating only what the branch's records say and that they are not merged. After the merge: the reply from main with the merged T-id and rungs (check_requests --draft 375), recorded in packing/campaign/result-requests.yaml, and the close when nothing the author asked for is queued.

## Notes

2026-10-10, records lane R4 of the 2026-10-10 intake pass (think-fvz4): Evan Daniel's comment https://github.com/jlevy/squares/issues/375#issuecomment-6101883016 (20:31:42Z) withdraws S' at n = 17 as a separate submission and asks that the exact form from #419, at evand/square-packing 8c47162cec22f02791abfbf7dedb8094de91189a (search/exact/minpoly/data/n-17.minpoly.json.gz), be the n = 17 object, with its bookkeeping on #419 and #405; upper bound only, no optimality, no improvement on the register's 4.67553009360455. On the intake branch (not yet on main), in packing/campaign/result-requests.yaml, #375's n17-certificate is not_registered and no longer queued (withdrawn by the author), a new result n17-exact-form-2026-10-10 is queued under think-x4v4 (held with the n = 17 intake, nothing at 8c47162 retained or replayed), read_through is 2026-10-10T20:31:42Z, and #419 and #405 carry a note of the pointer.

The stage 7 draft for #375 in think-mtwe's notes must drop or reword its n = 17 part. The line that needs to change: "**What remains.** The n = 17 certificate is still held for the n = 17 work, under `think-00e3`, as the [8 October follow-up](https://github.com/jlevy/squares/issues/375#issuecomment-6065914616) says. A geometry replay of T-129 is optional and would not change any selected bound. This issue stays open while the n = 17 certificate is held, and a reply follows each change in the record." Its header line, "Ledger: not closeable (n17 hold).", needs the same change. The draft should acknowledge the withdrawal and say the exact form stays held with the n = 17 intake, not imported or replayed here; `check_requests --report` now lists "n17-exact-form-2026-10-10: an acknowledgement; not yet imported" among the replies due on #375.


## Stage 7 draft from main at c6bf2d46f, 2026-10-11 — not posted (owner: leave as drafts)

Ledger: not closeable (`check_requests --report` at c6bf2d46f: certificates-105-130-status-2026-10-07 and certificate-292-status-2026-10-07 are open, as T-129 is recorded and not replayed; n17-exact-form-2026-10-10 is queued under think-x4v4). Replaces think-mtwe's 10 October draft for #375: the n = 17 paragraph and header are reworded as this bead's 10 October notes ask, acknowledging Evan Daniel's comment of 2026-10-10T20:31:42Z (https://github.com/jlevy/squares/issues/375#issuecomment-6101883016) that withdraws S' at n = 17 in favour of #419's exact form; `think-00e3` is no longer named, since the record now holds the n = 17 object under think-x4v4; links point at `results.html`. Raw `--draft 375` prints "nothing has been read or replayed here yet" for T-129 and glued numerals ("at105 and130 at7eef24f"); this text does not. No case ceiling moved.

@evand, thank you for the 7 October updates and for the 10 October note on n = 17. This follow-up covers only what they added; T-098 and T-101 are unchanged from the [6 October confirmation](https://github.com/jlevy/squares/issues/375#issuecomment-6023190825).

**What is recorded.** Your dated certificates at n = 105 and 130 (7eef24f) and at n = 292 (f58a017) are retained with their matching inputs and separate immutable pins, as **[T-129](https://jlevy.github.io/squares/results.html#t-129), V0/C0**, through [PR #463](https://github.com/jlevy/squares/pull/463). They stand at the sides they state: s(105) ≤ 10.806077865519704632682966…, s(130) ≤ 11.911187706535762355657987… and s(292) ≤ 17.597249391156465040647414…. Here they were parsed and their exact sides compared with the case records. No geometric replay was run and neither of your checkers was executed, so T-129 is recorded, not confirmed.

**Why they move no case.** A smaller certificate already confirmed here holds each of these counts: Ryan Xu's #432 certificate at n = 105 (T-125), Siddharth Gupta's #438 refinement at n = 130 (T-127) and Seth Rehwaldt's #425 refinement at n = 292 (T-117). The results table marks T-129 superseded by those three.

**The `verify_all.sh` correction** at cca7bf1 is retained separately, in [`packing/resources/web/evand-batch-wrapper-2026-10-07/`](https://github.com/jlevy/squares/blob/main/packing/resources/web/evand-batch-wrapper-2026-10-07/README.md), and linked from T-129. It corrects the wrapper and is not a new bound. Your re-run of the batch remains your report; no program of yours ran here for it. The older scripts and receipts behind T-098 and T-101 are unchanged.

**n = 17.** As you asked on 10 October, the rational certificate S' at n = 17 is withdrawn from this issue as a separate submission, and the record now takes the exact form of #419 at 8c47162 (`search/exact/minpoly/data/n-17.minpoly.json.gz`, with `verify_exact.py` and `lean/Sqpack/Exact/Batch/N17.lean`) as the n = 17 object. It is the register's packing at n = 17, John Bidwell's, and an upper bound only, so it states no new bound: neither S' nor S* improves the register's 4.67553009360455. The exact form is held with the n = 17 intake for integration with the n = 17 work; nothing at 8c47162 has been retained, replayed or recorded here yet, and none of your programs ran for it. The #419 and #405 entries note where you point its bookkeeping.

**What remains.** The n = 17 exact form stays held with the n = 17 intake until that work takes it up or declines it. A geometry replay of T-129 is optional and would not change any selected bound. This issue stays open while the n = 17 object is held and T-129 is recorded but not replayed, and a reply follows each change in the record.

---
_Generated by [Claude Code](https://claude.ai/code)_


2026-10-31 bold-ritchie-l7 (intake pass think-3guf, lane L7): posted the #375 follow-up from main 90b79dbe1 (Pages run 41196287332, verify-deployment passed): https://github.com/jlevy/squares/issues/375#issuecomment-6542830540. It names T-101 (V3/C3, current; 32 of the 77 counts' verified bounds still cite its exact replay) with E-evand-exact-ceilings-2026-10-05-exact-replay and -source-replay, both confirmed, and T-129 (V0/C0, recorded, superseded); the n = 17 exact form stays held under think-x4v4. Recorded on branch claude/bold-ritchie-xo28us-replies2. check_requests --report: no reply due; not closeable (T-129 has no named validation bead; n17-exact-form queued).

2026-10-31 bold-ritchie-l7: the reply record is draft PR #857 (https://github.com/jlevy/squares/pull/857), head f04af4801 after merging main a8deaf1b6 (#817); hosted CI green (59 checks: 31 success, 28 skipped). This bead stays open as the answer bead.
