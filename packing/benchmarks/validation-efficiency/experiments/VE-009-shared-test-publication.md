---
softschema:
  contract: squares.validation_efficiency:Experiment/v1
  schema: ../experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: VE-009
  title: Share complete immutable publications within one pytest invocation
  registered: "2026-10-14"
  tier: exploratory
  control_label: publication-local-control
  candidate_label: publication-shared-candidate
  minimum_samples: 3
  minimum_improvement: 0.15
  maximum_allocation_ratio: 1.25
  target:
    - tests/test_overview.py
    - tests/test_site_head.py
    - tests/test_site_documents.py
    - tests/test_repo_links.py
---
# Share complete immutable publications within one pytest invocation

Registered before candidate measurements.
Implementation was authorized just before this record was written; no candidate
measurement had been observed.
Status: withdrawn on design and maintenance grounds after both fresh 184-result semantic
oracles passed. No paired performance samples ran.

## Hypothesis and Frozen Criterion

Share complete immutable publications within one pytest invocation should remove
repeated work from the retained strict-checkpoint workload.
This is a hypothesis, not an established saving.
Alternate three control/candidate observations through the maintained validation-timing
instrument. Every observation must pass its full semantic oracle.
Require at least 15% reduction in median inclusive wall, nonoverlapping ranges and
allocated worker-seconds at most 1.25 times control.
Report median and range with a separate complexity judgment; a miss stays a miss.
No confirmatory speedup, full-shard admission or three-minute result follows.

## Semantic Guards

Retain all canonical pages, 324 case records, result bodies/documents, inlined variants
and the complete asset/support closure required by the four actual consumers.
Preserve direct patched and deterministic producer calls, explicit case subsets, fresh
per-consumer mutable mappings and private filesystem copies.
A fresh invocation rebuilds from current inputs.
Missing, corrupt, partial, escaped, linked or conflicting snapshot inputs must fail.
Enable sharing only when an opted-in consumer is actually selected for the shard; no
unnecessary all-shard prebuild.
Prove complete byte/asset equality and exactly one producer with three real workers
before comparing cost.

## Regime and Measurement

Control remains existing lazy process-local preparation.
Candidate controller preparation is part of the pytest wall and is recorded separately;
it never moves outside the measured command.
Allocation and selected identities remain fixed; no producer corpus or assertion
reduction. Record controller and worker allocation honestly.

Use existing Python 3.14 and the locked environment, warm filesystem caches, fresh
pytest processes and private fixtures, PACK_JOBS=1 and one native thread.
Retain exact source inputs, commands, allocation, raw output and JUnit through the
existing campaign instrument.
Other source edits may be light; no known heavy local measurement overlaps these
observations. Keep all original failures and incomplete observations.

The original semantic check used the 77152fb83 source with the common reviewed font and
CLI repairs. Main PR #602 subsequently expanded the corpus from 160 to 184 results.
The timing baseline is now the integration at `f13efcb7a`, preserving main `9b32da04d`
and its new results, plus the common functional repairs.
Record the final documentation baseline commit and exact source bytes before a fresh
corpus check and alternating the candidate files.
Keep that corpus and source fixed between arms.
Retained hosted timings identify the candidate, not recoverable time or CPU attribution.

## Evidence

Raw receipts and source snapshots belong in the existing task closeout archive under
pr599-integration, outside disposable scratch.
The campaign report is generated from validated records after measurement; no outcome is
assigned before then.

## Result and Withdrawal

The fresh main #602 corpus passed all 470 checks in both modes, without skips or
failures. The expected identities and all 2,707 frozen source inputs were unchanged.
These are single semantic observations, not registered performance samples:

- Local preparation: 110.380 seconds inclusive.
- Shared preparation: 149.098 seconds inclusive, including a 91.151-second serial
  controller barrier before the 54.70-second worker phase.

The independent patched and deterministic producer checks correctly remain fresh after
preparation. Their work still runs in workers.
Current cost packing places three consumers on one shard and the fourth on another, so
the combined cohort would not establish a benefit for either actual shard.

The coordinator accepted the author’s recommendation to withdraw the roughly 500 lines
of transport and lifecycle code on design and maintenance grounds.
No paired timings were started and no three-pair numerical verdict is claimed.
All five candidate files, the original 160-result oracle, both 184-result oracles and
their source/phase audits are retained in the closeout archive under
`ve009-publication-main602/`. The four tracked source files now match the pre-experiment
implementation; the new test module is archived and staged in Trash.
No CI opt-in was enabled and no criterion was relaxed.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
