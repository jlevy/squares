---
type: is
id: is-01m53ek3ff79x09e0bq00v9kcd
title: "Adopt T-174 at its 38 staged rational counts under the house rule, regularizing each in the adoption's PR (#660 A1; 12 more go to T-193 via #658/think-ot5c)"
kind: task
status: closed
priority: 2
version: 20
delegate: user-eb-adopt-174
labels:
  - regularization
  - validation
  - result-import
dependencies: []
parent_id: is-01m51hyxstsa9ptekd2ss26ksn
child_order_hints:
  - is-01m57j9xsga57szgfah5ex2bcd
  - is-01m59jbf3zmjznc12k8g2b5cwk
  - is-01m59mmjskde34b97g9npmhdb6
  - is-01m5a4zqkgk1vqa1q1n1ncbdec
hold: null
hold_until: null
created_at: 2026-10-16T22:51:13.774Z
updated_at: 2026-10-23T05:32:40.717Z
started_at: 2026-10-17T06:39:00.754Z
closed_at: 2026-10-23T05:32:40.717Z
close_reason: "Tracker audit 2026-10-23 (c-audit-c-1023, think-lrg9), checked by coord-intake-1023: DONE. #665 merged 2026-10-19 (adopt T-174 at 37 rational counts); 236 adopted to T-218 by #692; the T-193 twelve sit under think-ot5c; select_houses.PENDING_ADOPTION names think-3mry nowhere"
resolution: null
duplicate_of: null
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

user-eb-adopt-174 (lane T, 2026-10-17): claimed; worktree /home/user/squares/.claude/worktrees/adopt-t174, branch claude/intake-2026-10-17-adopt-t174 from origin/main 804eff369. Reading tools; next: wire T-174 into upper_bound_houses/adopt_houses and write the 50 houses.

user-eb-adopt-174: adopt_houses wrote the 50 records (d86dbb35b, pushed); draft PR #665 (intake, S2). Running build_known_best_atlas --update --n <50> --jobs 2; next: custody, axis views, default drawings, strong generators.

Scope corrected to 38 counts (coordinator, 17 Oct). #658 (8f46741ad) re-points 88, 102, 123, 126, 199, 258, 259, 266, 267, 292, 295 and 301 to T-193, which is smaller there; they are staged under think-ot5c until the algebraic writer exists. #658 lands first.

user-eb-adopt-174: coordinator scope change received: adopt T-174 at 38 counts only; 88, 102, 123, 126, 199, 258, 259, 266, 267, 292, 295, 301 go to T-193 via #658 (staged under think-ot5c there). No strong runs had started on any count. Reworking the branch (d86dbb35b adopted 50) to 38.

user-eb-adopt-174: 38 adopted and pushed (a867e9353 houses, e4de583c4 custody, 1b3cda963 axis views+states). 36 pending; strong runs started 07:45Z in scratch runs/adopt174-{deg05,deg1,deg5}-1017 and adopt174-1017 (2 processes). Next: regularize_select --workers 2, layer, settle, evidence.

user-eb-adopt-174: coordinator took 236 out too (issue 659). Branch now adopts T-174 at 37 (head 9f17533aa); 236 and the T-193 twelve stay staged under think-3mry until #658/#659 land. Strong runs restarted 07:50Z on the 35 pending (aborted 236-inclusive runs kept uncommitted in scratch aborted/).

user-eb-adopt-174 08:2xZ: head 1e55a4ba0 pushed (records views, bound citations, family census, check_standing staged-count fix, ABOVE_U -110/297, MAX_PLACES 72 for 68). Strong runs in progress (evand ~17/35, grid0.5 ~20/35). Papers render byte-identical to main at 804eff36 (provisional). Site edition not cut (coordinator cuts at merge).

user-eb-adopt-174 11:03Z: strong runs done on the 35 pending (evand 6,947+2,183 CPU-s incl. 206 rerun at 1800 s timeout, still no view; grid 0.5/1/5 4,388/4,469/4,456 CPU-s). regularize_select --workers 2 running.

user-eb-adopt-174 17:40Z after container restart: scratch runs intact and complete (evand 35+1, grid 3x35, selection 12:23Z); admission 738ee1b96; renderings+default drawings 8a5f8fdfd. Next: strong runs on 103 and 261 (regular as published) so all 37 are selected; settle the 25 no-better counts; retain evidence; validate.
