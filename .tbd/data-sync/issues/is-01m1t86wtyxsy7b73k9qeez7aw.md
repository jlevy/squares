---
type: is
id: is-01m1t86wtyxsy7b73k9qeez7aw
title: Correct exp-060 lower-bound display direction
kind: bug
status: closed
priority: 0
version: 2
labels: []
dependencies: []
parent_id: is-01m1t71acqhj675pskphwcyvst
created_at: 2026-09-06T02:19:26.941Z
updated_at: 2026-09-06T02:46:36.728Z
closed_at: 2026-09-06T02:46:36.727Z
close_reason: Corrected exp-060's upward-rounded lower-bound displays to exact fractions or downward-safe decimals, regenerated owned views, and passed numeric/document validation in 1ed5265a and 3fecaf23.
resolution: null
duplicate_of: null
---
The exp-060 source and generated synopsis display 3.82 and 3.85 lower bounds rounded upward. Replace them with exact fractions or downward-safe decimals, preserve the result's evidential status, and regenerate all owned views.
