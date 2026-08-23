---
type: is
id: is-01m0pnjppsajkthg7jgchw6awx
title: R1 applies to analysis code, not only pipeline components (from D-029)
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels: []
dependencies: []
parent_id: is-01m0n6nyzx5pnark7xve1dy52x
created_at: 2026-08-23T06:40:25.817Z
updated_at: 2026-08-23T06:40:25.817Z
---
D-029: an agent built a one-LP-solve probe, called it "the quench", and retracted a correct finding. sqpack.quench existed and would have disagreed on the first call.

The soundness postmortem's R1 says a component *accepting a configuration* is checked against code it does not share. The postmortem frames R1 around pipeline components; D-029 is evidence it applies to throwaway analysis code too, which is also where D-023 landed. Two defects now point at the same gap.

Decide and act on one of:

- Widen R1's wording in postmortem-2026-08-23-soundness-class.md to cover analysis and probes explicitly. It is a dated artifact, so this is a dated annotation, not a rewrite.
- Or add a rule to conventions.md section 8 -- "a probe that reproduces a pipeline stage is checked against that stage before its result is believed" -- and cross-reference R1.

Either way state where a one-off probe is supposed to live. tools/regression_test.py holds checks labelled by defect; tools/negctl.py holds mutations. Neither is the home for an exploratory measurement, and D-023 and D-029 are both partly about there not being one.
