---
softschema:
  contract: squares.validation_efficiency:Experiment/v1
  schema: ../experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: VE-013
  title: Read each Gupta claim bound once for its two fields
  registered: "2026-10-14"
  tier: exploratory
  control_label: gupta-bound-original-control
  candidate_label: gupta-bound-pair-candidate
  minimum_samples: 3
  minimum_improvement: 0.15
  maximum_allocation_ratio: 1.25
  target: tests/test_gupta_adoption.py::test_register_outputs_schema_valid_complete_selected_and_withdrawn_inventory
---
# Read each Gupta claim bound once for its two fields

Registered before candidate implementation or timing.
Tracking: `think-dmz9`.

Each of 17 claims currently calls reported_bound twice to obtain two fields from the
same admitted certificate.
The unchanged node runs registration twice, making 68 full roster admissions for claims
alone. Compute the bound once per row and read both fields from that result.
Leave coverage readers, acquisition checks, schemas, inventory and public freshness
unchanged; introduce no batch API or cache.

Before timing, compare complete ordered claims and generated registry bytes against the
control, including both fields for all 17 cases, all 14 selected and 3 withdrawn cases,
withdrawal choices, artifact sentinel and evidence fields.
Retain second-registration byte stability and late-original/acquisition-pin refusals.
A valid read followed by an input mutation must cause the next public read to refuse.

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
Control inclusive wall seconds: 6.3567, 6.8027, 6.3872. Candidate inclusive wall
seconds: 5.0223, 5.0223, 5.0469. Medians are 6.3872 and 5.0223 seconds: a 21.37%
reduction, with nonoverlapping ranges and equal allocation.

The candidate passes this exploratory screen.
VE-015 independently passes the same criterion after withdrawal of the schema candidate
used in both arms here.
No new cache or admission API is introduced.

Each source variant ran in a fresh process; other candidate inputs remained fixed in
both arms, as recorded in the exact dirty-source receipts.
The generated report consumes the original native receipts and raw output without
rewriting their provenance.
These observations do not establish hosted shard timing or the three-minute objective.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
