---
type: is
id: is-01m7px4b2pnqjann3a3b59fgf7
title: "Adopt T-331 at 268, T-332 at 270 and #1031's result at 299 on 19 November 2026 (the day after #1009 moved all three), and regularize them"
kind: task
status: in_progress
priority: 1
version: 6
delegate: c2-imports
labels:
  - regularization
  - validation
  - intake
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
hold: null
hold_until: null
created_at: 2026-11-18T08:42:16.533Z
updated_at: 2026-11-20T17:07:58.459Z
started_at: 2026-11-20T07:02:59.266Z
---
The pass's adoption of 19 November 2026 (UTC) under the house rule, in one pull request: Joost de Winter's T-331 at 268 (issue 1021), T-332 at 270 (issue 1022) and #1031's result at 299 (think-10mx), each a validated, reviewed packing below the house, which cannot be adopted on 18 November because #1009's pass (think-i38n) already moved 268, 270 and 299 that day and a day's archive holds one prior state a count (upper_bound_houses.LATER_PASSES; the precedent of 268 on 25 and 26 October, T-240 then T-242). Each count is staged in select_houses.PENDING_ADOPTION ("next pull request") under this bead by its registering PR: think-gqzz's for 268 and 270, think-10mx's for 299.

Steps (result-import.md, "Adopt a House, Then Regularize It"): add each packet to upper_bound_houses._sources and each count to ADOPTED and LATER_PASSES["2026-11-19"]; the coverage entry; RESULTS and CREDITS prose in adopt_houses; adopt_houses; take the three counts off PENDING_ADOPTION; build_known_best_atlas --update, regularize_axis_components --update-atlas --n 268 270 299, default_drawings --update; both strong generators on each pending count (grid-slack at 0.5, 1 and 5 degrees and Evan Daniel's driver) into run directories adopt_houses names; regularize_select and the layer commands; settle or admit; render and record; the derived records (custody, bound citations, escape screen, censuses, the contributor census, tables, case verifiers, landings); then the stage 7 replies on #1021, #1022 and #1031 say the adoption.

## Validation
- Claim: T-331 at 268, T-332 at 270 and #1031's result at 299 become the houses, each regularized on its new witness.
- Run: adopt_houses for the three counts; both strong generators and the selection at 268, 270 and 299.
- Cost: 5 to 25 CPU-minutes a count by the runbook's receipts, 15 to 75 for the three, under the owner's 40 CPU-hours an item; an estimate.
- Budget status: queued; runs on 19 November after think-gqzz's and think-10mx's registrations merge.
- Depends on: the registering PRs for think-gqzz and think-10mx merged.
- Done when: the three counts are adopted and regularized, select_houses --check, default_drawings --check-state --base-ref origin/main and flip_regularization --check pass, and the PR is merged.
- Machine note: at most two cores on the shared host.

## Notes

2026-11-20T11:30Z c2-imports: the pass moved to 20 November (the 19th passed with no PR). On claude/intake-2026-11-20-import-1021: adopt_houses wrote T-331 at 268 and T-332 at 270 at 07:40Z and T-333 at 299 at 08:57Z (after #1036 merged and was mapped); LATER_PASSES["2026-11-20"] = {268, 270, 299}; T-320, T-321, T-325 keep no house; select_houses PENDING_ADOPTION entries for 268/270 dropped. Strong runs (retained under packing/cases/regularized_drawings/think-78aj-2026-11-20/): 268 decided no better (grid-slack no view; driver solve 1.69e-19 above the side, row 4), 270 grid-slack 0.5-degree view drawn (driver's KKT solve 4.56e-18 below T-332's side held at row 3, think-4z8z), 299 grid-slack 5-degree view drawn (driver timed out). About 3,060 CPU-s in all. Run dirs renamed to -grid-deg05/1/5 after the first layer wrote a dotted run id the index schema refuses (adopt_houses prints -grid-0.5). Derived records, closed-form layer, test pins done; stamps and pin wait for #1024's merge, then retain_history on main's 20 November archive per same-day-pass.md.

2026-11-20T12:45Z c2-imports: draft PR #1048 (claude/intake-2026-11-20-import-1021), head 484e392ced, main a9e5261a2 merged; T-331 (268), T-332 (270), T-333 (299) provisional after #1024's T-328 to T-330; all three adopted and regularized in the pass of 20 November; stamps and pin at c3aa6d5773/484e392ced, to be redone after #1024 merges (retain_history on main's 20 November archive). Local: records and edit tiers green but the expected contiguity gap; hosted CI running.

2026-11-20T17:10Z c2-imports: PR #1048 green on main 7a3b186a2 (head abdeb73873; packing-required run 44777222780, pages-required run 44777222634), labels intake and S3. Final merge after #1024: archive combined with adopt_houses.retain_history (127, 268, 270, 299), LATER_PASSES unioned, SCREEN_FINDINGS n=1..324 (126, 2985, 302, 7449), paper comparison re-measured (explainer register count 333 vs 330 only), stamps unchanged (2026-11-20), DATA_REVISION re-pinned to 64a48c24. Not merged; stage 7 replies remain (the coordinator's).
