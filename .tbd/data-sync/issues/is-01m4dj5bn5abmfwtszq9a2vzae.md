---
type: is
id: is-01m4dj5bn5abmfwtszq9a2vzae
title: Avoid repeated manifest and count work within one census invocation
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-10-06-exact-side-values.md
labels: []
dependencies: []
parent_id: is-01m4dfhweng71qgnvs6ngvdbap
created_at: 2026-10-08T10:50:20.196Z
updated_at: 2026-10-08T10:50:20.196Z
---
Read-only attempt-2 triage of full checkpoint 37756689659 at a0ca63461 found repeated work in the 14.63-second census-ledger control (12-second ceiling). certificate_data calls hosted_data.require for each of 200 object records; require reparses/revalidates the same manifest after load_ledger already loaded it, yielding 201 parses per successful census. Reuse a validated manifest only within one invocation while preserving every object presence, size, digest and namespace check. Do not introduce a global path-only cache: existing controls add, corrupt and remove objects between calls. The ledger has 58 admitted entries; when selector_receipts is empty, reuse the same admitted-mask count for the three identical projection fields while preserving distinct per-entry marginal counts.

Begin with a preregistered bounded comparison on adequate external storage and the same runner shape, retain cold and mutation controls, and measure savings before claiming them. No fix, benchmark, or profile was performed in this delivery. Source/input paths are unchanged from a910a0e6 to a0ca6346; no host cause is established. Preserve both full-checkpoint attempts and unchanged timing ceilings. Files: packing/devtools/census_n17_certified.py; packing/src/sqpack/hosted_data.py; packing/tests/test_census_n17_certified.py. Ownership of a future patch should be explicit and isolated from other ongoing n17 work.
