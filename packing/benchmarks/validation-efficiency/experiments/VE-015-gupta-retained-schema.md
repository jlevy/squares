---
softschema:
  contract: squares.validation_efficiency:Experiment/v1
  schema: ../experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: VE-015
  title: Repeat Gupta bound-pair timing with the retained witness schema
  registered: "2026-10-14"
  tier: exploratory
  control_label: gupta-retained-schema-control
  candidate_label: gupta-retained-schema-candidate
  minimum_samples: 3
  minimum_improvement: 0.15
  maximum_allocation_ratio: 1.25
  target: tests/test_gupta_adoption.py::test_register_outputs_schema_valid_complete_selected_and_withdrawn_inventory
---
# Repeat Gupta Timing with the Retained Schema

Registered before observations in this regime.
Tracking: `think-dmz9`.

VE-013 passed its frozen screen while both arms used the VE-014 schema candidate.
VE-014 subsequently missed its own screen and was withdrawn.
Source inspection found that the Gupta fixture setup admits historical houses through
Witness/v2, so those inclusive timings do not establish performance with the final
retained schema. Keep the earlier measurements unchanged and repeat the same hypothesis
and acceptance rule with the original schema fixed in both arms.
The tally fixture does not consume Witness/v2; its independent result does not require
this replication.

Change only whether each Gupta claim obtains its two fields from one or two fresh bound
reads. Preserve the original complete inventory/schema/idempotence test and all 17 rows.
Before timing, rerun the independent complete ordered claims and fresh-input refusal
controls under the retained schema.
Prior control/candidate registry-byte equality and saved-original schema-equivalence
evidence remain supporting evidence.

Alternate three control/candidate pairs through the maintained validation-timing CLI,
using Python 3.14, one pytest process, one inner worker and one native thread, warm
filesystem and a fresh complete private fixture in each process.
Include imports, setup, call and teardown in wall time; use a 300-second deadline and
external scratch with failed-only retention.
Every sample and oracle must pass.
Require at least 15% lower median inclusive wall, nonoverlapping ranges and allocated
worker-seconds at most 1.25 times control.
Preserve all native receipts, output, JUnit and exact source variants.
Keep every failure or miss.
No cap, marker, selector or scientific assertion changes.
This remains an exploratory comparison, not a hosted-speedup claim.

No observations in this regime have been taken at registration.

## Outcome — 2026-10-14

The final-schema independent claims, inventory and freshness batch passed all four
cases. All six native observations passed with the retained original witness schema.
Control inclusive wall seconds: 7.3009, 6.8210, 6.5802. Candidate inclusive wall
seconds: 5.2100, 5.2204, 5.3227. Medians are 6.8210 and 5.2204 seconds: a 23.46%
reduction, with nonoverlapping ranges and equal allocation.

The candidate passes the unchanged exploratory screen and is retained.
The original inventory test and complete ordered claims remain; each public read still
admits fresh inputs.
VE-013 retains its earlier distinct schema regime.
Source variants, all native receipts, raw output and JUnit remain unchanged in the
evidence record. No hosted wall improvement or three-minute CI result is established by
these local observations.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
