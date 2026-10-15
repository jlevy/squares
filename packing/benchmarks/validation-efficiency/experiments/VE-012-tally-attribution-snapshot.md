---
softschema:
  contract: squares.validation_efficiency:Experiment/v1
  schema: ../experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: VE-012
  title: Read project attribution inputs once per test invocation
  registered: "2026-10-14"
  tier: exploratory
  control_label: tally-original-control
  candidate_label: tally-snapshot-candidate
  minimum_samples: 3
  minimum_improvement: 0.15
  maximum_allocation_ratio: 1.25
  target: tests/test_site_project_tallies.py::test_a_tally_link_selects_exactly_its_projects_rows
---
# Read project attribution inputs once per test invocation

Registered before candidate implementation or timing.
Tracking: `think-abys`.

The exact node independently computes attribution for 45 projects.
Its helper reads and parses the same two YAML files for each project: 90 reads and 90
parses. This static count is not a timing result.
Compute the same complete ordered attribution map once within each test invocation,
using the same independent rules and fresh inputs.
Do not reuse the production project-source-key implementation or move rendering into
setup. The cold results renderer remains within the measured command.

Before timing, compare all 45 complete ordered result-ID lists against the original
helper, including shared and empty projects.
Retain slug uniqueness, facets, defaults, hidden rows, ordering and the complete
rendered HTML assertions.
Prove a new invocation observes changed inputs.
The adjacent browser test and its interactions are unchanged.

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
Control inclusive wall seconds: 7.9320, 7.5804, 7.6249. Candidate inclusive wall
seconds: 5.8616, 5.8184, 5.9462. Medians are 7.6249 and 5.8616 seconds: a 23.13%
reduction, with nonoverlapping ranges and equal allocation.

The candidate passes the exploratory screen and is retained: the bounded change removes
repeated reads without a new cache or admission API.

Each source variant ran in a fresh process; other candidate inputs remained fixed in
both arms, as recorded in the exact dirty-source receipts.
The generated report consumes the original native receipts and raw output without
rewriting their provenance.
These observations do not establish hosted shard timing or the three-minute objective.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
