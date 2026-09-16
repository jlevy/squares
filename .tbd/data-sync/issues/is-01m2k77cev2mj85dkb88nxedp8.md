---
type: is
id: is-01m2k77cev2mj85dkb88nxedp8
title: Close the live workbench PR stack in dependency order
kind: task
status: in_progress
priority: 1
version: 13
labels: []
dependencies: []
parent_id: is-01m2h2zv3xg1w4gdy1svjsv1tx
child_order_hints:
  - is-01m2kd6659g8r7svfx9mkb83sf
  - is-01m2m5zjmj7dsycs1x6yxwcwwt
  - is-01m2m6xx00sabcq5zqkrneavd0
  - is-01m2m6y4gw224dgrwf37bgqnhd
  - is-01m2mab5h55dh53sd1gtw5prjh
created_at: 2026-09-15T19:03:15.162Z
updated_at: 2026-09-16T05:16:59.299Z
---
Merge #125, #155, #160, #171, #175, #178, #179, #181, and #180 strictly parent-first. Refresh each child from the exact parent, resolve only evidence-backed conflicts, require clean mergeability and exact-head fast/Page CI at each stopping point, and require a successful deferred checkpoint on the final cumulative leaf before completing the stack. Track the #179 nested-package selector fix and the #181 think-6o9n lifecycle explicitly; do not treat stale green checks as evidence.

## Notes

2026-09-15/16 checkpoint: #125 merged as 0ac0e063; #155 as 031de58d;
#160 as 11783761; #171 as 21a68102.

#175 reached 3d8ef13c with deterministic whole-module quick sharding, corrected
quick-test scope, hosted baselines of 150.54s and 119.54s, and 6,111 accounted
quick tests. A concurrent follow-up advanced it to 582d384a to validate
sqpack.probes.applied sources. Review found that commit failed open for legal
source= calls and for unknown or mixed wrapper sources. The reviewed amendment
e4d96b6f makes a recognized applied call safe only when its source is provably
loader-backed; 67 focused tests, Ruff, formatting, and diff checks pass. Its
full pre-push gate is running before any push.

The descendants were propagated concurrently through #178 5e3c00f0, #179
1c42b6ce, #181 def1e133, and #180 8ea979b8, but those heads become stale if the
#175 amendment moves the parent. Continue strictly parent-first from the exact
final #175 SHA and require fresh exact-head Packing, Page, mergeability, and
final cumulative deferred evidence before the async stack merge. Never reuse
stale green checks.

The open-PR inventory also found overlapping CI PRs #183, #185, and #186.
Their reconciliation is tracked as child think-97we: preserve #183's parallel
Pages architecture after fixing and remeasuring its workbench checkout; port
only #185's independently valuable fixture, liveness, typecheck, and per-file
cost work while keeping suite-a/suite-b; preserve #186's wall-measurement
framework after Python 3.14 and final-topology rewiring. Do not merge the three
branches wholesale.

PR #182 remains the post-stack Route S certification boundary. It must integrate
the final main, preserve the admitted receipt, pass exact-head fast and deferred
gates, repair the two stale synopsis statements, and merge before any H-163
target access.
