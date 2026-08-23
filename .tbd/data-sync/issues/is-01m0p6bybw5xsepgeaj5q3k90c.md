---
type: is
id: is-01m0p6bybw5xsepgeaj5q3k90c
title: "PR #5 review F-6: exp-001 is a three-cell sweep recorded as a one-cell round"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m0p6bwcyve6zdv41ezr08e3g
created_at: 2026-08-23T02:14:35.643Z
updated_at: 2026-08-23T02:14:35.643Z
---
Measured n=10,11,12 in one artifact with instance point 11, so the ledger shows H-016 coverage as 'n: 10 11* 12' with two measured cells unstarred. Since an unfilled cell is a queue item, an unattended runner would re-run n=10 and n=12. Fix: split future sweep rounds one per cell, or declare a multi-cell form; annotate exp-001 either way.
