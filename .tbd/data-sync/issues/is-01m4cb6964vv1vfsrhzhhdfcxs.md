---
type: is
id: is-01m4cb6964vv1vfsrhzhhdfcxs
title: "PR #427 A1 — High: the sweeps checkout omits the newly required source packet."
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m4cb68shtz5h0braprdqj1qb
created_at: 2026-10-07T23:29:15.972Z
updated_at: 2026-10-07T23:29:15.972Z
---
Review https://github.com/jlevy/squares/pull/427#pullrequestreview-5449633758 head83748.

**A1 — High: the sweeps checkout omits the newly required source packet.**
`.github/workflows/packing-validation.yml:1314` lists the original and first-update
SQUISH packets but not `squish-422-second-update-2026-10-07`. The changed source
selection in `packing/devtools/build_known_best_atlas.py` therefore works in a full
checkout but fails in the actual sweeps checkout.
CI run `37701514884`, job `113066270977`, records
`build_known_best_atlas --check --sample` failing at n=88 with “retains no facts for
this case.” This is an input-availability defect, not a numerical refusal.

**Fix:** include the new pinned packet in the sweeps sparse checkout and update its
paired module-boundary contract.
Validate the effective sparse checkout and rerun the affected sweeps job.
