---
type: is
id: is-01m1qcnpbkcj1npasye0hzg9pd
title: "thirdparty/verify.py and falsify.py: preconditions, typed errors, and two things to write down"
kind: task
status: in_progress
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m1qcc9devr6mz0m6erxswxjc
created_at: 2026-09-04T23:39:42.835Z
updated_at: 2026-09-05T00:53:23.422Z
---
Port the P1-P4 preconditions (nonnegativity among them), typed load errors, and singleton/empty domain handling. Two policy points to state rather than slip in: (1) a B-square that does not fit the container (2h >= L) no longer raises, so an all-vacuous Condition 5 accepts -- sound, since a unit square containing such a B-square does not fit either, but acceptance on vacuity in a checker whose value was refusing what it cannot handle; write the soundness note beside it. (2) decide() folds declaration mismatches into failures under a comment saying it keeps them separate; fix the comment or the behaviour. falsify.py's per-mutation oracles are hard-coded to the 19/5 file while the usage line advertises any certificate; refuse a non-shipped path explicitly.
