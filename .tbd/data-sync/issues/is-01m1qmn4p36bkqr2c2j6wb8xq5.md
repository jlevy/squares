---
type: is
id: is-01m1qmn4p36bkqr2c2j6wb8xq5
title: "F5: the package README says the bound holds for no other n; monotonicity says otherwise"
kind: bug
status: in_progress
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m1qcc9devr6mz0m6erxswxjc
created_at: 2026-09-05T01:59:13.346Z
updated_at: 2026-09-05T02:07:01.216Z
---
F5 of PR 80, found unaddressed by the coverage audit: packing/cases/n11_fractional_certificate/thirdparty/README.md (line ~468) says the result is 'not a bound for any other n', which monotonicity makes false -- a packing of n+1 unit squares contains a packing of n, so s(n) >= 19/5 for every n >= 11 (trivially, since every n > 11 already carries a larger bound). PR 80's replacement wording is at git show 04127189:packing/cases/n11_fractional_certificate/thirdparty/README.md around line 471. Port the one clause; check packing/frontier/n-011.md and T-018's composition sentence in results.yaml for the same disclaimer.
