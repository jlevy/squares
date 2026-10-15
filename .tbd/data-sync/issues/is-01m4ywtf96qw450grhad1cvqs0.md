---
type: is
id: is-01m4ywtf96qw450grhad1cvqs0
title: "PR #612 A10: algebraic_against never reaches its 4000-place ceiling; refusal untested"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m4ywspmt47ny1en5jnen7c09
created_at: 2026-10-15T04:23:43.142Z
updated_at: 2026-10-15T04:52:31.573Z
closed_at: 2026-10-15T04:52:31.573Z
close_reason: "fixed in 98df478e2: last refinement is to the ceiling; test fails before and passes after"
resolution: null
duplicate_of: null
---
Nit. upper_bound_reports.py ALGEBRAIC_PLACES loop and its ReportError. Review: https://github.com/jlevy/squares/pull/612#issuecomment-6184278979
