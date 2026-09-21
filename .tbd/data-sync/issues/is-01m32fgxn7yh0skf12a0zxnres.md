---
type: is
id: is-01m32fgxn7yh0skf12a0zxnres
title: "Efficiency block (W5): the deep gate costs 45 minutes of wall and is 1.38x its own declared price"
kind: epic
status: open
priority: 1
version: 2
labels: []
dependencies: []
child_order_hints:
  - is-01m32g52666n96w3fwjqsysbw6
created_at: 2026-09-21T17:16:52.770Z
updated_at: 2026-09-21T17:27:52.770Z
---
OR-12 opens an efficiency block by measuring the gate. Measured 2026-09-21 on two complete deep-gate runs of PR 208, both at the same tree.

Run 35579234418 (started 08:41:41Z, completed):
  exhaustive-tier      2674s  (44m34s)   <-- gates the wall
  deferred-steps       2469s  (41m09s)
  deferred-slow-lane    999s  (16m39s)
  screen                909s  (15m09s)
  deep-gate-required      4s
Run 35627075872 (started 16:40:10Z): screen 902s, deferred-slow-lane 993s, both others still running past 36 minutes. Same shape.

Wall per run is about 45 minutes, set entirely by exhaustive-tier.

THE DRIFT. .github/workflows/deep-gate.yml:5,26 and packing/tests/test_deep_gate_workflow.py:182 price the exhaustive tier at 1943.05s, the figure test_the_pull_request_surface_defers_only_what_was_measured used to refuse promotion into --fast. The job actually costs 2674s: 1.376x the declared price. Under the 1.5x that fails a local tier, but the CI job is not clocked by any drift rule at all, so nothing noticed. deferred-steps at 2469s is in the same position.

WHY IT BIT TODAY. The deep gate is a pre-merge gate by label, so its wall is on the merge path. It ran twice on PR 208 -- about 90 minutes -- and the first run was spent on a head that was then force-restored, so half of it was wasted outright. OR-14 says a development cycle is never artificially slow.

CANDIDATE WORK, none measured yet:
- Clock the four CI jobs under a drift rule the way local tiers are clocked, so 1.38x is reported rather than invisible.
- Ask why exhaustive-tier costs 2674s of wall for 1943.05s of declared step time: is the 731s difference setup, serialisation, or a step that grew since the price was recorded?
- exhaustive-tier and deferred-steps overlap heavily in wall; check whether deferred-steps is re-running what exhaustive-tier already decided.
- Decide whether a label-gated 45-minute gate belongs on the merge path at all, or whether it should run once per stack tip rather than per pull request.

Entry conditions are met and the block is overdue: the last session declaring workflow: efficiency-loop is Session 131 (BC-340, 2026-09-14); 17 terminal blocks have closed since, against OR-12's ceiling of eight. Sessions 139 and 141 scheduled a W5 and neither declared one; counting 141 generously still gives 7.
