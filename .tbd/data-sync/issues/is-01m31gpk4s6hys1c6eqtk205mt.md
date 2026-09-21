---
type: is
id: is-01m31gpk4s6hys1c6eqtk205mt
title: Retained-patch control is marked slow on a false justification
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m31gn7263sfhfbq8xfabkh3p
created_at: 2026-09-21T08:18:12.759Z
updated_at: 2026-09-21T08:18:12.759Z
---
PR 209 re-review, new Low/Medium. test_every_retained_patch_applies_to_its_declared_base is marked slow, justified in tests/test_module_boundaries.py and the commit message as 'It needs the base commit, so it belongs in the lane that checks out with fetch-depth: 0.' Not a discriminator: suite-a and suite-b carry the quick lane on every PR and both check out with fetch-depth: 0 (.github/workflows/packing-validation.yml:424 and :465), as does validate (:57). At ~3.3s it is far under the 12s quick ceiling. Net effect: slow-lane and deferred-slow-lane are skipping, so the control has never executed in CI on either PR. OR-13 says a fast check belongs on the PR surface. The review asked for a records-tier control.
