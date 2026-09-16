---
type: is
id: is-01m2k77cev2mj85dkb88nxedp8
title: Close the live workbench PR stack in dependency order
kind: task
status: in_progress
priority: 1
version: 14
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
updated_at: 2026-09-16T06:31:57.534Z
---
Merge #125, #155, #160, #171, #175, #178, #179, #181, and #180 strictly parent-first. Refresh each child from the exact parent, resolve only evidence-backed conflicts, require clean mergeability and exact-head fast/Page CI at each stopping point, and require a successful deferred checkpoint on the final cumulative leaf before completing the stack. Track the #179 nested-package selector fix and the #181 think-6o9n lifecycle explicitly; do not treat stale green checks as evidence.

## Notes

Merge pass authorized 2026-09-15. PR #175 merged to main as 05157c33 and PR #178 merged as 6e212693 through GitHub's stack-aware asynchronous endpoint, each at its exact reviewed green head. PR #179 final head e40970b1 is pushed with all blocking review fixes and exact hosted checks running. PR #183 became DIRTY after the no-JS merges and is being reconciled rather than merged on stale evidence. #185/#186 are also DIRTY; #186 still has failing wall-budget checks.
