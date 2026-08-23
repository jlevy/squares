---
type: is
id: is-01m0p6bybw5xsepgeaj5q3k90c
title: "PR #5 review F-6: exp-001 is a three-cell sweep recorded as a one-cell round"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m0p6bwcyve6zdv41ezr08e3g
created_at: 2026-08-23T02:14:35.643Z
updated_at: 2026-08-23T02:23:19.787Z
closed_at: 2026-08-23T02:23:19.786Z
close_reason: "FIXED. exp-001 annotated; the re-run is split one round per cell (exp-002 n=10, exp-003 n=11, exp-004 n=12) as the contract intends. H-016 now shows coverage 'n: 10* 11* 12*' with all cells filled. Also fixed a latent bug this exposed: status_of ranked accepted above rejected, so n=12 passing would have reported a refuted swept claim as confirmed. Rejected now outranks accepted, with the reasoning recorded in the code."
---
Measured n=10,11,12 in one artifact with instance point 11, so the ledger shows H-016 coverage as 'n: 10 11* 12' with two measured cells unstarred. Since an unfilled cell is a queue item, an unattended runner would re-run n=10 and n=12. Fix: split future sweep rounds one per cell, or declare a multi-cell form; annotate exp-001 either way.
