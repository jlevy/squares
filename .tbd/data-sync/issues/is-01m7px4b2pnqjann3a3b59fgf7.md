---
type: is
id: is-01m7px4b2pnqjann3a3b59fgf7
title: "Adopt T-331 at 268, T-332 at 270 and #1031's result at 299 on 19 November 2026 (the day after #1009 moved all three), and regularize them"
kind: task
status: open
priority: 1
version: 1
labels:
  - regularization
  - validation
  - intake
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
created_at: 2026-11-18T08:42:16.533Z
updated_at: 2026-11-18T08:42:16.533Z
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
