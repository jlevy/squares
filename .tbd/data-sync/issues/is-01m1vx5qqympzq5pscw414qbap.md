---
type: is
id: is-01m1vx5qqympzq5pscw414qbap
title: Fix suite-wide invalidation for repository-relative packing configuration paths
kind: bug
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md
labels: []
dependencies: []
parent_id: is-01m1vrrktbrd2scnaqfe40eby4
created_at: 2026-09-06T17:45:03.485Z
updated_at: 2026-09-06T19:06:59.864Z
---
Actual packing/pyproject.toml, packing/uv.lock, packing/tests/conftest.py and packing/.python-version bypass SUITE_WIDE because its names are packing-relative. Public selector probe chose 23–27 of 163 test files instead of all. Add actual repository-relative paths and regression fixtures before any exhaustive family selection rollout. Four failing baseline cases verified; candidate prepared and being integrated.

## Notes

Repository-relative configuration invalidation fix remains in PR98. Integration with main c14451f5 exposed another selector omission: newly added dilation_corollary and decide_certificate paths did not select exact verification because other steps claimed them. Both failing regression cases now pass in full and fast selection universes; two declared input paths added. Bounded merged checks157, limit-record checks10 and selector/artifact checks7 passed; full integrated fast and final hosted checkpoint remain pending.
