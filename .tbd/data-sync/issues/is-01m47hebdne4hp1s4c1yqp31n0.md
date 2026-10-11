---
type: is
id: is-01m47hebdne4hp1s4c1yqp31n0
title: "Import wand125 #366: mixed_n18_L4704 (s(18) >= 588/125, 832-node net) and mixed_n19_L48229 (s(19) >= 48229/10000) at 65e408c"
kind: task
status: closed
priority: 1
version: 6
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m47hea1vkqx8h5wzdzcyqs5k
hold: null
hold_until: null
created_at: 2026-10-06T02:42:19.701Z
updated_at: 2026-10-06T07:19:34.170Z
started_at: 2026-10-06T02:45:53.733Z
closed_at: 2026-10-06T07:19:34.169Z
close_reason: "T-099 and T-100 merged at V3/C3 in #381 (ebf23276); #366 replied and closed. Full n=18 source replay follow-up filed separately."
resolution: null
duplicate_of: null
---

## Notes

2026-10-06 06:10Z: T-099 and T-100 exited at V3/C3 by sqverify-fast (8b0215c5b); n = 18 verified 588/125, n = 19 verified 48229/10000. #366's n18-4704 and n19-48229 mapped in result-requests.yaml.

Follow-up left running, not waited for: the complete replay of mixed_n18_L4704's bundle by its own driver, process group 8378, started 2026-10-06T03:28:44Z at two workers (about 370 of 832 nodes at 06:10Z; ETA roughly 11:00-13:00Z). Its receipts land in /tmp/claude-0/-home-user-squares/1fb2d4ab-96d0-5b24-9e36-157598bdbf06/scratchpad/r2/full-n18-receipts/ and full-n18.done. To finish: copy run.meta and run.stdout into packing/resources/web/wand125-mixed-bounds-finer-net-2026-10-06/receipts/n18-L4704/full/ (beside the committed processes.json, ASSERTS_ON), run devtools.audit_wand125_declared_net compare --certificate n18-L4704 --shipped .../full-n18/shipped/n18-L4.704-proof-bundle --fresh .../full-n18/run/n18-L4.704-proof-bundle --meta <that run.meta>, then add E-n018-wand125-mixed-4704-source-replay (draft at scratchpad/r2/exit/evidence-n18-replay.yaml) to T-099's evidence: a reproduction with the producer's code beside the rung. Kill with kill -TERM -- -8378 if not wanted.
