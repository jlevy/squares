---
type: is
id: is-01m1t71bf6rqbsd14afyvp2b7y
title: Reconcile PR 89 after the next origin/main advance
kind: task
status: closed
priority: 1
version: 5
labels:
  - upstream
dependencies:
  - type: blocks
    target: is-01m1t71bsncn7adg02er2hyk6d
parent_id: is-01m1t5yjssbd51cnnw2zwkqah6
child_order_hints:
  - is-01m1t769sq46m6hkgfpj3j7z2c
created_at: 2026-09-06T01:58:56.741Z
updated_at: 2026-09-06T02:46:37.715Z
closed_at: 2026-09-06T02:46:37.714Z
close_reason: "Integrated the audited PR #87 head directly at merge commit 3fecaf23, recorded the overlap disposition and superseding manifest, rebuilt shared views, and passed the merged edit gate; upstream no longer blocks commissioning."
resolution: null
duplicate_of: null
---
When PR #87 or another relevant upstream change reaches main, run the merge-upstream shortcut, record the old/new bases and overlap disposition, regenerate affected shared views, and preserve manager launch gates.
