---
type: is
id: is-01m0r89wgt102y3wm7nfd235fj
title: "atlas_check's D-030 convergence guard is vacuous: it cannot fail"
kind: bug
status: closed
priority: 0
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0pqfp4rm5r4fy7ys6t03h0w
created_at: 2026-08-23T21:26:54.217Z
updated_at: 2026-08-23T22:51:22.227Z
closed_at: 2026-08-23T22:51:22.227Z
close_reason: "Fixed on codex/pr14-square-packing-review (PR #15) before this bead was filed; verified against that branch after stacking PR #16 on top of it. atlas_check.py now offers one genuinely non-converged observation and asserts offered_non_converged == 1, so the D-030 guard has a failure mode again. test.sh sets DEEP=1 under --strict with a guard that fails if it did not take. golden_basins.py assigns configs[identity] directly rather than via setdefault, so the verified pose matches the retained side, and it evaluates oracles before writing, atomically through a temporary. Independent convergence on the same fixes from two directions is the useful part of the result."
resolution: null
duplicate_of: null
---
Confirmed by re-derivation from merged main, 2026-08-23. Raised independently by the PR #15 review as part of F-17; this bead is the executable version.

tools/atlas_check.py offers every observation with converged=True (lines 112 and 122), then asserts:

    ok=offered_non_converged == 0 and offered == 6

Nothing in the check ever offers a non-converged observation, so the assertion tests the fixture rather than the store. It cannot fail. Its own comment at line 174 cites D-030 -- "the store faithfully recorded twelve non-converged stopping points" -- so the guard for this campaign's most serious defect has no failure mode.

FIX: the check must offer at least one genuinely non-converged observation and assert that the counter sees it, and at least one converged one, and assert the counter does NOT count that. Then watch it fail via negctl by mutating Atlas.add's `if not converged: self.non_converged += 1`.

THE GENERALISATION, which is the part worth keeping. This is the third instance of one mistake in this campaign: a tamper that replaced nothing (YAML escaped the surd), a tamper that replaced nothing (float rendering), and now an assertion whose inputs exclude the failing case. The rule that catches all three: an assertion has not been watched failing unless its INPUTS can produce the failing case. Add that sentence to the negative-control guidance, because "run negctl" did not catch this one -- negctl mutates source, and here the source was fine and the fixture was wrong.
