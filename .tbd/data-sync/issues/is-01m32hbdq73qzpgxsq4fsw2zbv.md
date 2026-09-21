---
type: is
id: is-01m32hbdq73qzpgxsq4fsw2zbv
title: check_session_gate's verdict depends on which refs the clone happens to have fetched
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m32dvmtc77znp14556p7c5w2
created_at: 2026-09-21T17:48:49.767Z
updated_at: 2026-09-21T17:48:49.767Z
---
Found 2026-09-21 while validating on main.

packing-validate --records fails the step 'terminal sessions name the gate that certified them' in a clone that has fetched many refs, and passes in a fresh CI checkout of the same tree. Sessions 087, 088, 089, 090, 112, 113 (and earlier 133-135) declare gate commits from PRs that were historically squash- or rebase-merged. Those objects are absent from a shallow CI checkout, so the check reports them as uncheckable and passes. Fetch enough refs and the objects appear but are not ancestors of HEAD, so the same check fails.

So the verdict is a function of the operator's fetch history rather than of the tree. check_session_gate's own docstring draws the line deliberately -- 'a checkout that does not contain the commit is not evidence the commit was orphaned' -- and that reasoning is sound, but the consequence is a records tier that cannot be run cleanly by anyone with a full clone, which is every agent that has been working across branches.

This is adjacent to think-fqut (the stacked-merge rebase) and probably wants deciding together: a rebase or squash merge legitimately orphans a declared gate commit, and the check currently has only two readings, 'absent so uncheckable' and 'present so false'. A third is needed for 'present, not an ancestor, and known to have been orphaned by a recorded merge'.
