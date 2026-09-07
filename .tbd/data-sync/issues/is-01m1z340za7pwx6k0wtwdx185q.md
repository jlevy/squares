---
type: is
id: is-01m1z340za7pwx6k0wtwdx185q
title: Report actual quench stop diagnostics in historical regression failures
kind: task
status: open
priority: 2
version: 1
spec_path: packing/campaign/agendas/agenda-027-compatibility-and-restricted-families.md
labels: []
dependencies: []
parent_id: is-01m1z2grw8sr01t7ynft3hrnz9
created_at: 2026-09-07T23:26:42.153Z
updated_at: 2026-09-07T23:26:42.153Z
---
Bounded W7 maintenance implementation, no scientific claim: fix misleading four-turn label for4*pi, retain convergence/stop reason/side gap/solve counts/closure counts in D019/D168 failures, distinguish a budget stop before claiming an absent closure path. Preserve all existing pass/fail obligations, tolerance values,60-second caps and closure requirement. Add synthetic classification/diagnostic regression controls with TDD. Existing eight real controls already passed in serialized34.50s diagnostic. High agent owns only check_regressions.py and a focused test module; root owns docs/beads/integration. Eight-minute implementation bound followed by independent review.
