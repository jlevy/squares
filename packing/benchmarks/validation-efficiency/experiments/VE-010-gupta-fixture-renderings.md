---
softschema:
  contract: squares.validation_efficiency:Experiment/v1
  schema: ../experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: VE-010
  title: Batch admitted Gupta rendering within each private fixture
  registered: "2026-10-14"
  tier: exploratory
  control_label: gupta-original-control
  candidate_label: gupta-production-and-fixture-candidate
  minimum_samples: 3
  minimum_improvement: 0.15
  maximum_allocation_ratio: 1.25
  target: tests/test_confirm_gupta_records.py::test_late_case_or_registry_refuses_the_entire_write_plan[result-scope]
---
# Batch Admitted Gupta Rendering Within Each Private Fixture

Registered before this variant’s source change or timing.
Operator: Astra subagent news_security_c. Status: rejected and withdrawn; the retained
CLI cohort misses the frozen range-separation criterion.
The coordinator owns campaign indexes and source disposition.
VE-008 and VE-009 are separate experiments.

## Hypothesis and Criterion

[VE-007](VE-007-gupta-invocation-facts.md) missed its frozen 15% inclusive-wall
threshold: its median reduction was 11.97%. That verdict is unchanged.
Its private-proposal fixture still calls the public `register.section` once per selected
case, admitting the complete seventeen-case fact roster fourteen times per fixture
invocation.

Use the freshly admitting `case_renderings(confirmed=False)` once per function-scoped
fixture and check its late-input guard after preparation.
Retain every private input copy, fourteen selected case bodies, all seventeen source
facts, actual history/house checks, and every mutation/assertion.
No module/global cache or work outside fixture setup is introduced.
Compare every one of its fourteen section/bound pairs byte-for-byte with the existing
freshly admitting public wrappers before timing.

The candidate combines VE-007’s two production modules with this fixture batching.
Control is the original production modules and original complete test module at
`77152fb83a85d80aa50d773ecf1a4a062cfe0eaa`. The exact timed node above and its assertion
remain unchanged.
This experiment measures the combined delta, not the isolated effect of
fixture batching.

Alternate three control/candidate pairs through maintained
`benchmarks.validation_timing.run_sample`. Every observation must pass; require at least
15% reduction in median inclusive wall, nonoverlapping ranges, and allocated
worker-seconds at most 1.25 times control.
Use serial Python 3.14 pytest, `PACK_JOBS=1`, native-thread limits one, warm filesystem
and the existing environment.
Each sample has a fresh process and complete private fixture.
Preserve setup/call/teardown and total wall, exact source snapshots, all failures, and a
fixed 180-second command timeout.
There is no confirmed-speedup, whole-CI, or three-minute-loop claim.

Root documentation/font edits are outside the owned inputs; known heavy validation is
held until this comparison finishes.
Bounded semantic checks cover the fresh wrappers, late fact/pin mutations, full positive
output and unchanged refusal node before accepting any timing.
Complexity is judged separately after applying the numerical criterion.

## Evidence

Raw receipts, exact control/candidate source snapshots and the thin driver calling the
maintained instrument live in
`/Users/levy/wrk/github/squares/.codex/regularization-closeout-evidence-2026-10-13/pr599-integration/ve010-gupta/`.
No timings had been taken for this variant at registration.

## Result and Withdrawal

The original thin-driver cohort passed all six tests and showed a numerical median
reduction from 9.9090 to 7.8679 seconds (20.60%), with separated ranges.
It used the primary Python 3.14.7 build from August 5 with Clang 21. Its incomplete
receipt metadata prevents full campaign acceptance; no pooling with a different
interpreter is valid.

A separate repeat used the maintained CLI, registered arm labels and complete provenance
with the existing external Python 3.14.7 build from August 25 with Clang 22. All six
functional observations passed.
The generated arithmetic comparison is:

- Control: 10.66 (9.08-10.96), n=3 seconds.
- Candidate: 7.24 (7.17-11.67), n=3 seconds.
- Verdict: **No detectable effect: ranges overlap or candidate is slower.**

The 11.6740-second candidate remains in the data without selective retry or exclusion.
The [generated report](../report.md) uses the original CLI receipts and JUnit; the
original thin-driver receipts remain in the external archive separately.

Semantic preservation and independent static review do not establish performance
acceptance or an integrated gate pass.
The author recommended withdrawal on complexity grounds, and the coordinator accepted
it. All three routine source files now equal the pre-experiment version.
No threshold, marker, ceiling or scientific acceptance rule changed.
Exact candidate source snapshots and both interpreter cohorts are retained.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
