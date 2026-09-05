---
type: is
id: is-01m1qmn533spag4avtvsckss5y
title: "F41: check_rung_figures must refuse to fall back to a historical rung when the live certificate is missing"
kind: task
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m1qcc9devr6mz0m6erxswxjc
created_at: 2026-09-05T01:59:13.762Z
updated_at: 2026-09-05T02:38:31.077Z
closed_at: 2026-09-05T02:38:31.077Z
close_reason: "Ported as 6c7f8ce8: check_rung_figures refuses a missing live certificate.json by naming the expected path instead of falling back to a historical rung; retained_pointer_problems tested."
resolution: null
duplicate_of: null
---
F41 of PR 80, deferred without an owner by commit 75e04e9f: check_rung_figures.pick_retained falls back to the first resolved certificate when a result's live certificate.json is missing (check_rung_figures.py ~line 227), so a missing live certificate could silently select a historical rung. Port PR 80's control: require exactly one live certificate for a certificate-bearing result, drop the historical fallback, and add the two tests 75e04e9f named (pick_retained refusing to fall back; two moving pointers). The margin half of F41 needs nothing: margin = n - mass already uses the declared target.
