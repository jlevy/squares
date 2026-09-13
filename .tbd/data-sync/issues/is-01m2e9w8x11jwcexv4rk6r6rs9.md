---
type: is
id: is-01m2e9w8x11jwcexv4rk6r6rs9
title: Diagnose and repair PR156 exact-head required-suite failure
kind: bug
status: in_progress
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - ci
dependencies:
  - type: blocks
    target: is-01m2e0e4ct972w6eapcr8c3xjz
parent_id: is-01m2e0e4ct972w6eapcr8c3xjz
created_at: 2026-09-13T21:13:24.640Z
updated_at: 2026-09-13T22:17:35.826Z
---
On pushed PR156 draft 9c56e901, GitHub Actions run 34782594805 job 103792203850 failed step 5 (required pull-request behavioral lane) after 7m51s, causing packing-required failure. Retrieve and retain the exact failed log; distinguish source regression, test flake, and environment from evidence. Local full --push also failed its reachable step with unretained output, while a separate exact-head standalone rerun passed 5511/9/57 in 2002.14s. Repair the actual cause, rerun appropriate local push gate and current-head CI, update PR/body and think-4ovs. Do not mark PR ready on a partial pass.

## Notes

2026-09-13 21:13 UTC exact hosted log retrieved via escalated `gh run view 34782594805 --job 103792203850 --log-failed`, saved /private/tmp/pr156-suite-failed.log. The required suite failed on enforced duration, not a reported assertion: fast behavioral tests wall 436.29s, suite total 436.36s versus 275s tier ceiling (159%) and recorded 183.44s (2.38x, above 1.5x drift rule). It reports two test calls over 12s: test_read_fixed_core_calibration_profile.py::test_coherent_mathematical_and_operational_mutations_are_refused 28.02s, and ::test_exact_method_witness_agreement_and_closed_boundary 12.32s. Need profile/shorten or appropriately mark measured slow nodes with declared measurement in test_the_slow_marker_is_declared_only_by_measured_nodes, then restore suite-tier budget and rerun exact-head local/hosted checks. Do not simply increase ceiling without a justified new reference shape. Earlier full --push reachable failure still has no retained exact trace; local standalone reachable 5511 passed/9 skipped/57 deselected is separate evidence. PR156 remains draft.

2026-09-13 local isolated remediation: branch codex/pr156-suite-timing from exact published PR156 head 9c56e901; clean candidate commit 21e9cdee84f5b1baea6d1e7dfa99b04d113f5cec. Baseline source/file: 112 profile tests passed in 239.13s locally; call time 236.17s, including 188.49s in eight functions, every parametrization at least 2.69s. A cProfile of one accepted admission put 5.22/6.49s read_profile time in _read_rows and 3.01s in pure exact _charge. A production cache trial was reverted because it did not remove enough aggregate cost. Final patch changes only eight slow decorators and their measured declaration in test_the_slow_marker_is_declared_only_by_measured_nodes; full accepted profile read remains quick. The slow lane still runs in full checkpoints, and devtools.reachable_tests --since 9c56e901 selected the changed profile test file (narrow 39), so --push still reaches all moved cases.

Post-change focused quick profile plus registry: 67 passed, 46 deselected in 54.55s. Focused slow profile: 46 passed in 91.05s at -n 4, minimum call 3.66s above the 1s floor. Records tier 32/74 passed in 50.05s; edit tier 45/74 passed in 172.35s. Local --suite with PYTHON_CPU_COUNT=4, --jobs 1 --inner-jobs 1 took 202.75s, inside the 275s ceiling and 1.11x the 183.44s reference; no quick call reached the 12s backstop. Its pytest verdict was locally red for host setup only: 5,327 passed, 9 skipped, 5 failed (forkserver and two loopback socket binds denied by sandbox, two uv-cache permission failures) and 4 known-best-atlas collection errors because macOS dyld did not find Cairo. Exact log: /private/tmp/pr156-suite-uncontended.log; source head was clean after commit. No assertion in the changed profile file failed.

This is a local candidate, not a green PR. PR156 remains draft at 9c56e901 and auto-retargeted to main after PR148/149 merged at f2e24e07. Parent think-4ovs must integrate the commit, run exact combined-head --push and hosted required checks, then update PR/body; no push, PR edit, merge, or green-CI claim was made in this slice.
