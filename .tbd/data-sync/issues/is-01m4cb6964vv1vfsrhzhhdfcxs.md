---
type: is
id: is-01m4cb6964vv1vfsrhzhhdfcxs
title: "PR #427 A1 — High: the sweeps checkout omits the newly required source packet."
kind: bug
status: closed
priority: 1
version: 3
delegate: codex@17e132e9b179
labels: []
dependencies: []
parent_id: is-01m4cb68shtz5h0braprdqj1qb
hold: null
hold_until: null
created_at: 2026-10-07T23:29:15.972Z
updated_at: 2026-10-08T00:20:40.416Z
started_at: 2026-10-08T00:20:29.708Z
closed_at: 2026-10-08T00:20:40.416Z
close_reason: Source fixes9ff422a/6c615115 at f1d7 are independently reviewed E/F/G/H with0newfindings and hosted final-head CI30SUCCESS26documentedSKIP. Focused379+190+3+11owner checks passed; selected broad assertions completed with original capability failure retained and unchanged supported profiler/heavy completions. Actual broad allowance1800 is unchanged. These source findings are fixed; parent422 intake/confirmation/deployment remain open until atomic stack merge and publication.
resolution: null
duplicate_of: null
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
