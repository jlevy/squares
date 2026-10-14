---
softschema:
  contract: squares.validation_efficiency:Experiment/v1
  schema: ../experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: VE-011
  title: Copy complete guarded native receipts through their JSON representation
  registered: "2026-10-14"
  tier: exploratory
  control_label: guarded-copy-original-control
  candidate_label: guarded-copy-json-candidate
  minimum_samples: 3
  minimum_improvement: 0.15
  maximum_allocation_ratio: 1.25
  target: tests/test_negative_controls.py::test_second_squish_consumers_survive_native_worker_boundaries[house-reads]
---
# Copy Complete Guarded Native Receipts

Registered before candidate implementation or measurements.
Tracking: `think-4p86`. The maintained native diagnostic admitted all nine historical
houses and both owner refusals.
Its profile attributes 2.2382 seconds to four deep copies and 0.0424 seconds to their
input guards. Profiling adds overhead and excludes snapshot preparation; these values
establish neither a speedup nor a gate pass.

Serialize the complete admitted receipt once as ordered integer-key/row pairs, then
decode a fresh private copy for each guarded return.
Compare the complete decoded value with the existing recursive type-and-order oracle
before reuse. Preserve every actual admission, case, schema/history check,
byte/custody/namespace guard, refusal and nested mutation-isolation requirement.
Refuse lossy or nonfinite representations.
Change only the test helper; production admission is unchanged.

Before accepting this candidate, pass all existing premise mutations, real native house
reads and fresh nested-copy controls.
Alternate three original/candidate pairs of the exact node above through the maintained
validation-timing CLI, using registered arm labels, Python 3.14, one pytest process, one
inner worker, one native thread, warm filesystem and a fresh complete private fixture in
each process. Include snapshot, imports, setup, call and teardown in wall.
Set a 180-second command deadline and retain failed-only temporary output on external
scratch.

Every sample must pass.
Require at least 15% lower median inclusive wall, nonoverlapping ranges and allocated
worker-seconds at most 1.25 times control.
Retain raw output, JUnit, start/end receipts and exact frozen source variants outside
disposable scratch. A miss remains a miss.
Judge code complexity separately; make no whole-shard, confirmed-speedup or three-minute
CI claim. Timing ceilings and markers are unchanged.

No candidate runtime observation has been taken.
C owns the host measurement budget; this slice is limited to source work until that
budget is released.

## Result and Withdrawal

The separate native positive oracle and all six registered observations passed the real
nine-house checks and both owner refusals.
Exact source guards passed before and after every observation; the candidate was
restored in `finally` before disposition.

- Control inclusive wall: 39.1359, 50.0571, 37.3616 seconds; median 39.1359 seconds.
- Candidate inclusive wall: 62.6207, 34.5586, 37.6866 seconds; median 37.6866 seconds.

The median reduction is 3.70%, below the frozen 15% criterion, and ranges overlap.
The slower 62.6207-second candidate remains in the data.
Private-fixture setup is included; the diagnostic profile’s deep-copy cost does not
replace inclusive evidence.

The coordinator withdrew the helper change and its five new copy controls.
The existing nine premise guards and native tests are unchanged.
The generated report includes the original six native CLI receipts and their raw
JUnit/output files without rewriting provenance.
The separate oracle, both complete source variants and withdrawal record remain in the
closeout archive under `ve011-guarded-admission/`. No ceiling, selector, criterion or
scientific rule changed.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
