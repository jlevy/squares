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
  target: "tests/test_overview.py tests/test_site_head.py tests/test_site_documents.py tests/test_repo_links.py; quick marker; four loadfile workers"
---
# Share complete immutable publications within one pytest invocation

Registered before candidate measurements.
Implementation was authorized just before this record was written; no candidate
measurement had been observed.
Status: pending bounded implementation and its review.

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

The baseline is the current 77152fb83 source with the common reviewed functional font
and CLI repairs. Capture those exact bytes before alternating the owned candidate files;
do not substitute a different rendered corpus or source revision between arms.
Retained hosted timings identify the candidate, not recoverable time or CPU attribution.

## Evidence

Raw receipts and source snapshots belong in the existing task closeout archive under
pr599-integration, outside disposable scratch.
The campaign report is generated from validated records after measurement; no outcome is
assigned before then.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
