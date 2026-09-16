---
type: is
id: is-01m1sgmedjqvwszgcd4n0h6460
title: "BC-218: run the gate as parallel GitHub Actions jobs, not one sequential runner"
kind: task
status: closed
priority: 0
version: 3
labels: []
dependencies: []
created_at: 2026-09-05T19:27:25.098Z
updated_at: 2026-09-16T00:20:29.059Z
closed_at: 2026-09-16T00:20:29.056Z
close_reason: |
  Landed. The gate has run as five concurrent pull-request jobs in .github/workflows/packing-validation.yml since 2026-09-06, with packing-required waiting on all five. The tier calibration it owned now lives in packing/devtools/gate-budgets.yaml, re-recorded from seven hosted runs on 2026-09-15 under think-z121.
resolution: null
duplicate_of: null
---

## Notes

2026-09-15 (think-z121): closing as landed. BC-218's parallel gate shipped on 2026-09-06; `.github/workflows/packing-validation.yml` has run the pull-request surface as five concurrent jobs (`validate`, `frontend`, `geometry`, `suite`, `sweeps`) ever since, with `packing-required` waiting on all five, rather than one sequential runner. The tier calibration this bead was named as owning is now the register's: a recorded cost per tier at a declared reference shape in `packing/devtools/gate-budgets.yaml`, re-measured on 2026-09-15 under think-z121 from seven hosted pull-request runs (`checks` 145.53 s, `frontend` 76.66 s, `geometry` 102.73 s, `sweeps` 119.72 s), and an empty record for a pull-request tier now fails `devtools.check_gate_budgets`. The per-test contention this split was meant to remove is gone with it -- see think-fckk, closed the same day.
