---
type: is
id: is-01m1z6h6tzja2ej4phez6gpftw
title: Align validation documentation with the 324-case tiers
kind: bug
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-09-08T00:26:19.844Z
updated_at: 2026-09-08T00:26:19.844Z
---
Documentation follow-up found while integrating upstream main 2869652618a09d183b8fba3b4237577b402d2f6b (PR #111) into PR #117. Leave this separate from the publication changes.

In development.md, the validation table still reports the suite tier at a 205-second ceiling and a 102.8-second four-sample mean. The authoritative packing/devtools/gate-budgets.yaml now declares a 260-second ceiling and a 162.62-second baseline from the first hosted 324-case run, 34133437296. Update the table and nearby baseline prose: only geometry retains the old four-reading mean; suite has one new hosted reading, and checks/fast/sweeps had their obsolete baselines cleared after their workloads changed.

In .github/workflows/deep-gate.yml, the comment beside the exact-complement contract says a seventh deferral added tomorrow must update the workflow, but seven deferrals already exist. Change that ordinal to eighth.

Acceptance: the documentation and workflow comment accurately describe the existing configuration. Do not change timing thresholds, test selection, or the fixed v0.2.4 publication version. Searches for the specific baseline, suite-baseline documentation, and deferral ordinal found no existing matching bead.
