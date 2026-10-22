---
type: is
id: is-01m5gkk7zv20d0dtpje8t54xqx
title: "Stage 4: review and confirm Couzo's in-corpus #670, #672, #675 entries (T-226 to T-228)"
kind: task
status: open
priority: 2
version: 1
delegate: c-lane-t225-stage4
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m5frzavxzvcqht1tf2edbfxp
created_at: 2026-10-22T01:28:48.887Z
updated_at: 2026-10-22T01:28:48.887Z
---
Stage 4 for Francisco Couzo's in-corpus rows of issues 670, 672 and 675, registered at V0/C0 in the think-ql4v stage 4 pull request (branch claude/stoic-thompson-ku09fw) as T-226 (#670 at 204), T-227 (#672 at 227 and 229) and T-228 (#675 at 204); the ids are the branch's and may change in merge order. The 21 October review of T-225 measured #672's 227 certificate on its own checker for information only and does not cover these entries, so they stay at V0/C0 until a review covers them.

## Validation
- Claim: s(204) <= 45044217780850246618141/3041751595240000000000 (#670, franciscouzo/square-packing@23aff0c6, certificates/n204.cert, SHA-256 f317d0c0...bc73dc); s(227) <= 71427829379429597600111901507/4589408083628500000000000000 and s(229) <= 231170315041711399213831561/14771101209934000000000000 (#672, @af8cb795, certificates/n227.cert 65b03df8...8c17 and n229.cert 9ab667ec...609f); s(204) <= 101859759444979981360793459/6878398651426000000000000 (#675, @c6da0fc7, certificates/best/n204.cert 761af9ec...a97543). Checker: the two maintained exact routes (devtools.upper_bound_reports certify/check --replay) and a review's own.
- Run: from packing/, python -m devtools.upper_bound_reports PACKET check --replay for couzo-issue670-2026-10-17, couzo-issue672-2026-10-17 and couzo-issue675-2026-10-18 (receipts retained, 12 jobs); a stage 4 mathematical review (tbd-strong-max) of the four certificates with sharp controls at 1e-30, mapped under docs/project/reviews/.
- Cost: under 0.02 CPU-h for the replays (12 jobs, 44.1 route CPU seconds in the receipts of 22 October 2026); the review lane's own runs a few CPU-minutes.
- Budget status: runnable, under any cap; gated on a review lane.
- Possible subset under the cap: not needed.
- Depends on: the think-ql4v stage 4 pull request merging (packets, receipts, entries).
- Done when: the review is mapped and accepted with no blocking defect, confirming evidence entries added, and T-226, T-227 and T-228 raised to V3/C3 by check_results; T-227's raise then also lets the house rule weigh it at 227 behind T-225.
- Machine note: seconds of CPU; shares the machine with any gate.
