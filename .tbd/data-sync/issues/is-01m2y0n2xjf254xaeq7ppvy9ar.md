---
type: is
id: is-01m2y0n2xjf254xaeq7ppvy9ar
title: "PR200-201 review R4: correct verified labels on float-only experiments"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m2y07hq7kkss9qh386q3h912
created_at: 2026-09-19T23:40:02.864Z
updated_at: 2026-09-19T23:40:02.864Z
---
exp162 and exp164-170/172-178 subject assurance=verified and method=exact-algebraic overstate float64 HiGHS probes that produced no accepted certificate. Match Experiment/v2: numerically-checked, numerical-f64, actual precision/tolerance and scope. Keep successful T028-030 certificates separate and retain exact assurance only where an exact obligation was discharged.
