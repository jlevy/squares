---
title: Validation Efficiency Campaign
date: 2026-09-06
---
# Validation Efficiency Campaign

This engineering campaign implements the
[W5 plan](../../../docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md).
It does not change scientific acceptance criteria.

## Protocol

The instrument is [`validation_timing.py`](../validation_timing.py), tested for passing,
failing, timed-out, and interrupted children.
Each trial writes start/end receipts, streamed output, and pytest JUnit with
setup/call/teardown durations.
Unmatched starts are incomplete observations.
Measurements use Python 3.14, one pytest process, `PACK_JOBS=1`, and one native thread,
unless the experiment explicitly varies them.
The cache regime is repeated execution in an existing environment with warm filesystem
caches; caches are not flushed.
Other agents may perform lightweight editing and checks.

The control is main `6b21d14b64c19003d597ed3c993c051b64336b0c` in
`/tmp/squares-validation-efficiency-control`, with the same certificate worker cap and
exhaustive duration instrumentation as the candidate.
Each receipt records its source revision, dirty diff digest, selected test source
hashes, host, command, and worker configuration.
The retained control patch reconstructs that control checkout.
The candidate patch reconstructs the affected mathematical sources; it is not a full
snapshot of every measurement-time working tree.
Unrelated documentation and timing tool edits continued as permitted above, so the
candidate’s whole-tree diff digest varies.
The
[implementation audit](../../../docs/project/reviews/review-2026-09-06-validation-efficiency-implementation.md)
checks the affected source reconstruction and states the limits of this evidence.

These twelve trials used the [retained original instrument](runs/instrument-v1.py.txt),
whose [digest record](runs/instrument-v1-source.json) documents its provenance limits.
After the trials, the maintained instrument was corrected to hash exact Git diff bytes
and untracked inputs.
The original receipts are unchanged; later improvements to the instrument do not
retroactively strengthen them.

For each candidate, alternate three control and candidate runs.
Every run must pass.
The exploratory screen requires at least a 15% reduction in median wall time and
nonoverlapping ranges.
Report median and range, not a confirmatory speedup claim.
For parallel scheduling, allocated worker-seconds must increase by no more than 25%;
these are an allocation proxy, not measured CPU. A separate written judgment decides
whether the simpler or faster implementation earns its complexity.

The [idea board](ideas.md) links each registered experiment.
Raw evidence lives in `runs/`; the report is generated from receipts and experiment
metadata.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
