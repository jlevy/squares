---
softschema:
  contract: squares.validation_efficiency:Experiment/v1
  schema: ../experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: VE-014
  title: Inline identical hot scalar and point witness schema shapes
  registered: "2026-10-14"
  tier: exploratory
  control_label: witness-refs-original-control
  candidate_label: witness-inline-candidate
  minimum_samples: 3
  minimum_improvement: 0.15
  maximum_allocation_ratio: 1.25
  target: tests/test_upper_bound_reports_574.py
---
# Inline identical hot scalar and point witness schema shapes

Registered before candidate implementation or timing.
Tracking: `think-vrof`.

One retained diagnostic of the PR574 comparison node attributes 14.461 seconds to
Witness/v2 schema validation, including 296,696 local reference resolutions.
Profiling overhead is unmeasured; this is not a baseline speed claim.
Replace hot acyclic scalar and point local references with identical YAML-aliased inline
shapes. Keep the public schema identity and definitions, the validator and every
constraint.

Before timing, prove expanded original and candidate constraints equal; retain supported
witness forms and malformed scalar/point controls, fresh schema/input mutation
detection, all 85 facts and exact comparisons, certificate reconstruction, custody,
register claims, receipt controls and native checker-input binding.
Do not cache verdicts or bypass validation.
Measure the complete PR574 module so both originally slow nodes and all its refusal
tests remain included.

Alternate three control/candidate pairs through the maintained validation-timing CLI,
using Python 3.14, one pytest process, one inner worker and one native thread.
Use a warm filesystem, fresh process and complete private fixture for every sample.
Include imports, rendering, setup, call and teardown in inclusive command wall time.
Use a 300-second command deadline and failed-only temporary retention on external
scratch. Every sample and independent oracle must pass.
Require at least 15% lower median wall, nonoverlapping ranges and allocated
worker-seconds at most 1.25 times control.
Retain all raw output, JUnit, source variants and native provenance receipts; a miss
remains a miss. Judge maintenance cost separately.
Timing ceilings, markers and selectors are unchanged.
This screen does not establish hosted shard timing or three-minute CI. No candidate
runtime observation had been taken at registration.

## Outcome — 2026-10-14

The independent correctness oracle and all six native observations passed.
Control inclusive wall seconds: 34.3984, 33.5600, 34.1032. Candidate inclusive wall
seconds: 29.4741, 30.0894, 29.7384. Medians are 34.1032 and 29.7384 seconds: a 12.80%
reduction, with nonoverlapping ranges and equal allocation.

The candidate misses the frozen 15% improvement requirement and is withdrawn.
Both schema and contract-test source files are restored to `6756bda8d`; complete
candidate variants, semantic oracles and all observations remain retained.
No timing criterion or validation constraint changed.

Each source variant ran in a fresh process; other candidate inputs remained fixed in
both arms, as recorded in the exact dirty-source receipts.
The generated report consumes the original native receipts and raw output without
rewriting their provenance.
These observations do not establish hosted shard timing or the three-minute objective.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
