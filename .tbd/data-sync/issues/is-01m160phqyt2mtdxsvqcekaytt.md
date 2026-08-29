---
type: is
id: is-01m160phqyt2mtdxsvqcekaytt
title: "Block 6: reachability-scoped verification"
kind: task
status: closed
priority: 0
version: 3
labels: []
dependencies: []
created_at: 2026-08-29T05:43:22.621Z
updated_at: 2026-08-29T16:43:04.363Z
closed_at: 2026-08-29T16:43:04.363Z
close_reason: Superseded by think-c46d (BC-075), which asks the prior question. BC-062 assumed the gate's tiers were right and only their routing was wrong; the measurements since say otherwise, and a selector bolted onto the wrong tiers makes the wrong thing faster. The reachability-scoped selector survives inside BC-075 as one candidate mechanism.
resolution: null
duplicate_of: null
---
agenda-006 BC-062, advancing BC-051. A verification selector that runs only the steps a change can reach, with a control proving it cannot under-run, measured against the fast-gate baseline.

Renumbered: previously said BC-058, which agenda-006 reassigned to the chirality block. The agenda is authoritative.
