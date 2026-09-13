---
type: is
id: is-01m2e0e4ct972w6eapcr8c3xjz
title: Publish the PR156 draft checkpoint with exact local gates and final hosted CI
kind: task
status: in_progress
priority: 1
version: 21
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: codex@spud10.local
labels:
  - n11
dependencies:
  - type: blocks
    target: is-01m2csyyq4nzfqppqj639avs51
  - type: blocks
    target: is-01m2dzgknq7k2cj3ea91thkcmj
  - type: blocks
    target: is-01m2e0qcksvn1sygh0tn3kj11d
  - type: blocks
    target: is-01m2e9ggafpy2xvk0r0rgy1p8w
  - type: blocks
    target: is-01m2eddtqbpv11d9g5yk0s8cv0
  - type: blocks
    target: is-01m2edr5vf9vba530c9ntyd3t1
parent_id: is-01m2ctdap5jwdr8h4qb8dxwt8z
child_order_hints:
  - is-01m2e7adq6sc2j6mzgsx89sg8h
  - is-01m2e9w8x11jwcexv4rk6r6rs9
  - is-01m2ef7thnn45d82454wg91f6p
hold: null
hold_until: null
created_at: 2026-09-13T18:28:24.089Z
updated_at: 2026-09-13T23:07:30.884Z
started_at: 2026-09-13T18:35:26.795Z
---
Review and commit durable reviews, run-sheet status, records, and accepted source changes; reconcile origin/main with the merge-upstream shortcut; run required push gate; push PR156 as draft; update body with unique cost, exact head, admitted/refused contracts and remaining gates; wait for final hosted CI and sync beads. Do not mark ready while coordinator and run-sheet admission remain refused.

## Notes

2026-09-13 21:13 UTC correction to the CI handoff: exact job log /private/tmp/pr156-suite-failed.log was retrieved. The 9c hosted required suite failed the explicit time budget: 436.36s total vs 275s ceiling and 183.44s recorded reference (2.38x). Two test calls >12s were 28.02s coherent mathematical/operational mutations and 12.32s exact method witness/closed boundary, both in test_read_fixed_core_calibration_profile.py. The job reports no assertion failure; its only failed validation step is fast behavioral tests due elapsed time. See think-bpy8 for targeted fix. The other 9c required checks and Pages passed. PR body is being updated; PR stays draft/unready; no calibration profile or BC329 target ran.

2026-09-13 23:07 UTC publication checkpoint: origin/main f2e24e07 is merged into clean local PR156 head 2f8925b2 and verified already up to date by the merge-upstream shortcut. Pushed 2f8925b2 to PR #156; cost-first body updated with 57-file diff (+31868/-169), conservative 50-root/97-session selected usage subtotal and explicit exclusions, three local --push attempts, and pending hosted CI. Required run 34788680067 and Pages run 34788680064 are underway; gh pr checks --watch is active. Three calibration profiles and BC329 target unrun; PR remains draft. Local two-job reachable lane passed 1593/3 skipped once with missing Ruff/Pyright PATH; corrected environment passed floors but local process-group EPERM and nested timeout caused two test failures, each later passed in isolation. No single green local --push receipt.
