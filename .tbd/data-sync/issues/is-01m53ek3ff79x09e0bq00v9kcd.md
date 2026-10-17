---
type: is
id: is-01m53ek3ff79x09e0bq00v9kcd
title: "Adopt T-174's 50 rational houses staged under the house rule, regularizing each in the adoption's PR (#660 A1; 60 before #657 moved 10 below T-174)"
kind: task
status: open
priority: 2
version: 4
labels:
  - regularization
  - validation
  - result-import
dependencies: []
parent_id: is-01m51hyxstsa9ptekd2ss26ksn
created_at: 2026-10-16T22:51:13.774Z
updated_at: 2026-10-17T02:51:49.736Z
---
The house rule (packing/campaign/result-import.md, "The House Rule"; the owner, 16 October 2026) makes T-174 (PR #574's PingYou certificates) the house at 63 counts on main. PR #660 stages them in `select_houses.PENDING_ADOPTION`: the 60 rational ones under this bead, staged as `next pull request`, and the three algebraic ones (70, 153, 207) under think-ot5c (the writer), staged as `no writer`. This bead's pull request adopts the 60, regularizes every count it re-houses in that same pull request, and takes each count off `PENDING_ADOPTION`. Opened by #660's addressing pass for its review A1 (the staged adoption had sat under the policy lane's own bead, think-sa5r).

## Validation
- Claim: T-174's exact rational sides at 60 counts, each below its case and confirmed (V3/C3 with an accepted review), and the witnesses `upper_bound_houses` rebuilds from the retained packet. `select_houses --all --check` lists them as staged under this bead.
- Run: `python -m devtools.adopt_houses` (write), then the commands it prints: `build_known_best_atlas --update`, `regularize_axis_components --update-atlas`, `default_drawings --update`, grid-slack at 0.5, 1 and 5 degrees and Evan Daniel's driver on each pending count, `regularize_select`, `layer` and the render step. Then `adopt_houses --check`, `select_houses --check` and `default_drawings --check-state`.
- Cost: 12.0 CPU-h, from 60 counts at the 3a batch's 0.2 CPU-h a count (think-la7h's receipts). The runbook's range, 5 to 25 CPU-minutes a count, gives 5 to 25 CPU-h.
- Budget status: runnable once #660, #657 and #658 have merged. It is within the 40 CPU-h item cap (think-ve84; think-lh7d), so the runs go in the adoption's pull request.
- Possible subset under the cap: not needed.
- Depends on:
  - #660 merged.
  - #657, which re-houses 129, 146, 156, 175, 176, 204, 232, 264, 271 and 303; those come off `PENDING_ADOPTION` in whichever of #657 and #660 merges second.
  - #658, whose T-193 reader re-points 88, 102, 123, 126, 199, 258, 259, 266, 267, 292, 295 and 301 to T-193 under think-ot5c. That leaves 38 rational counts here on the stack.
  - The worker snapshot cap (`run_negative_controls.SNAPSHOT_MAX_BYTES`, 216 MiB with 13.6 MB of headroom), measured and raised in the adoption's pull request where its witnesses need it.
  - The witnesses go into Git under OR-18's stored reading: 23.25 MB in a checkout, 3.51 MB stored.
- Done when:
  - the counts are off `PENDING_ADOPTION`, and their case records and coverage rows name T-174;
  - every count the pull request re-houses reads `regularized`, `decided-no-better` or `exempt` in `default-drawings.json`, and each one `PENDING_ALLOWED` named before is off the list;
  - after the last staged count (with think-ot5c's), `LIFTED`, the recorded view's pre-rule branch and `RULE_PASSES_FROM` are deleted, and `adopt_houses --refresh` runs under the house rule.
- Machine note: 4 shared cores, at most 2 workers. That is about 6 hours of wall at 2 workers. It cannot share the machine with a gate's wall measurement.

## Notes

Count corrected to 50: #657 (c593e2bfd) moved 129, 146, 156, 175, 176, 204, 232, 264, 271 and 303 below T-174, so 50 rational counts remain staged under this bead (#660 at f76706d17).
