---
type: is
id: is-01m2e9w8x11jwcexv4rk6r6rs9
title: Diagnose and repair PR156 exact-head required-suite failure
kind: bug
status: open
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - ci
dependencies:
  - type: blocks
    target: is-01m2e0e4ct972w6eapcr8c3xjz
parent_id: is-01m2e0e4ct972w6eapcr8c3xjz
created_at: 2026-09-13T21:13:24.640Z
updated_at: 2026-09-13T21:14:53.190Z
---
On pushed PR156 draft 9c56e901, GitHub Actions run 34782594805 job 103792203850 failed step 5 (required pull-request behavioral lane) after 7m51s, causing packing-required failure. Retrieve and retain the exact failed log; distinguish source regression, test flake, and environment from evidence. Local full --push also failed its reachable step with unretained output, while a separate exact-head standalone rerun passed 5511/9/57 in 2002.14s. Repair the actual cause, rerun appropriate local push gate and current-head CI, update PR/body and think-4ovs. Do not mark PR ready on a partial pass.

## Notes

2026-09-13 21:13 UTC exact hosted log retrieved via escalated `gh run view 34782594805 --job 103792203850 --log-failed`, saved /private/tmp/pr156-suite-failed.log. The required suite failed on enforced duration, not a reported assertion: fast behavioral tests wall 436.29s, suite total 436.36s versus 275s tier ceiling (159%) and recorded 183.44s (2.38x, above 1.5x drift rule). It reports two test calls over 12s: test_read_fixed_core_calibration_profile.py::test_coherent_mathematical_and_operational_mutations_are_refused 28.02s, and ::test_exact_method_witness_agreement_and_closed_boundary 12.32s. Need profile/shorten or appropriately mark measured slow nodes with declared measurement in test_the_slow_marker_is_declared_only_by_measured_nodes, then restore suite-tier budget and rerun exact-head local/hosted checks. Do not simply increase ceiling without a justified new reference shape. Earlier full --push reachable failure still has no retained exact trace; local standalone reachable 5511 passed/9 skipped/57 deselected is separate evidence. PR156 remains draft.
