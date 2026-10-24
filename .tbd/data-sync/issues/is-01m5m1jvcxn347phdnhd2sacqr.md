---
type: is
id: is-01m5m1jvcxn347phdnhd2sacqr
title: "Land #750 after T-231 to T-233: merge main, cut the explainer, re-pin"
kind: task
status: in_progress
priority: 2
version: 4
delegate: c-land-750-1023
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-23T09:30:59.357Z
updated_at: 2026-10-23T22:59:25.427Z
started_at: 2026-10-23T22:22:18.508Z
---
PR #750 (branch claude/intake-2026-10-23-lean-sources) registers T-234 to T-236 and cannot merge before T-231 (#753, for issue #719) and T-232, T-233 (#745) are on main: `check_results` requires contiguous register ids, and four register tests and one status test in shards A and B fail on that alone.

Once those land:

1. Merge origin/main into the branch (never rebase), re-render RESULTS.md, INVENTORY.md, STATUS.md, VERIFIERS.md, SYNOPSIS.md, the URL registry and the T-007 consumer audit, and re-run `release_pin --update`.
2. Cut the explainer's successor: it counts the register ("one of N results the framework has registered so far"), 233 on the branch and 230 on main on 23 October, so `check_release_impact` asks for an owning successor of v0.4.21 (or of whatever #753 and #745 cut). `cut_release vX --component paper:n11-lower-bounds-explainer --impact patch --scope "..."` after the merge, with the count measured by rendering twice from each tree, as the 5f8c45a47 cut did.
3. The other three papers (optimality review v0.1.11, threshold-bound review v0.1.4, methods survey v0.2.7) already have a fresh no-public-change record on the branch: rendered twice from each tree against main c1115c095, byte-identical. Re-measure only if their versions moved on main.

Hosted CI should then be green.

## Notes

2026-10-23, c-land-750-1023 (coordinator coord-intake-1023), branch claude/intake-2026-10-23-lean-sources, worktree /home/user/wt-gates.
Merged main 77aba4c02 (#747, #748, #751, #752, #761) at 3d134d640 and 64b316b6c (#762) at 73715631a, never rebased. Conflicts in evidence.yaml, bibliography.yaml and occurrences.yaml were both sides appending entries; resolved at entry granularity (result = exact union of both sides' entries, checked by parsing); release.py took main's pin; RESULTS.md, INVENTORY.md, VERIFIERS.md, STATUS.md re-rendered by their tools; site_urls --write and audit_t007_consumers --update left the auto-merge unchanged.
Re-pinned at dbef9b460 (DATA_REVISION 3d134d64). Explainer v0.4.22 cut at b16c36a4c: four renders into empty site dirs (two from this tree, two with main's version of every branch-modified file swapped in, release.py and tests aside; 55 files each): each tree's two renders byte-identical; explainer differs only in "one of 233 results" vs 230. cut_release rendered paper and PDF, 316 edition tests passed. Three other papers keep v0.1.11, v0.1.4, v0.2.7 (no-change record from c1115c095; check_release_impact did not ask again).
Local at 73715631a: packing-validate --records fails only check_results contiguity (144 s). Affected tests: 528 passed, 6 skipped, 7 failed (the six test_results_register and one test_result_status contiguity tests); test_overview 460 passed. #748's new record gates pass.
Remaining: once #753 and #745 merge, merge main again, re-cut the explainer (v0.4.22 is also cut by #753, #745, #757), re-pin. T-237: allocated to this lane, held unused for think-4o9c; #757 holds T-238 and assumes #750 holds T-237 -> gap unless renumbered or think-4o9c registers T-237 here (coordinator's call).
