---
type: is
id: is-01m32dwbwvq4ptmcmqy6py0941
title: fold --check cannot see a hypothesis swap (PR 207 residual 2)
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m32dvmtc77znp14556p7c5w2
created_at: 2026-09-21T16:48:10.651Z
updated_at: 2026-09-21T16:48:10.651Z
---
container_differences does not compare variant or corner_clip while fold copies them through, so differences(clipped_fold, unclipped_fold) == [] and --check reports matches:true for retained bytes declaring a different hypothesis. Concrete on exp-220-n11-96-25-class-family.json:2011-2012, which carries both fields at top level. By M3's own argument those two fields say which problem the family is a ceiling for and belong in container_differences.
