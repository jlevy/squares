---
title: "H-299 \u2014 matched exact replay observations"
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-299
  kind: hypothesis
  claim: Boundary-level replay instrumentation preserves the full accepted centered exact result
    while exposing step costs, memo evictions and memory observations.
  lane: proof
  derived_from:
  - X-048
  criterion:
    shape: determination
    metric: matched_full_exact_replay_observations
    direction: criterion_met
    threshold: Both fresh same-object runs complete full exact centered replay with identical mathematical
      result identities and identical seed/node/cells byte digests. The PHASES receipt matches the
      NONE baseline and retains all16 step boundaries, memo-eviction observations and bounded RSS
      samples. Instrumentation never changes verification arithmetic, coverage or acceptance. This
      establishes a diagnostic control and observations, not speedup or a new geometric admission.
      Resource stops, changed inputs or semantic differences refuse equivalence.
  instrument: packing/devtools/profile_n17_exact_replay.py
  instrument_ready: true
  regime: 'Original accepted exp280 seed/node directory and exact same ordered cells and U; centered
    inner cap935106018721/200000000000 with unchanged48-vertex boundary policy. Run NONE first,
    then PHASES in a new process comparing the retained NONE receipt. Do not compare historical
    receipt bytes: the new explicitcellsfile has its own custody metadata. No exp284 geometry and
    no implicit CALLGRAPH run.'
  instance:
    axis: n
    point: 17
  priority: 1
  cost_estimate: NONE180s + PHASES180s scientific budgets; combined360s inside owned-group TERM370/KILL380
    allowing10s setup/serialization. One worker, sampled4096MiB PER live process with owned cleanup.
    Instrumentation overhead is measured and cannot establish gain. Input/output ceilings and cooperative
    checks in the frozen profiler; partial diagnostics retained.
  prereqs:
  - H-291
  replication: false
  notes: Author27 target-free controls PASS0.80s, Ruff/BasedPyright zero; source-only review by
    coordinator and independent integration controls before launch. Scientific target unrun before
    registration. Explicitcellsfile3590B is a deterministic metadata extraction from accepted exp280
    descriptor, preserving geometry/order/U; originSHA51c2a5bfaa550870aba4df8abc2ebb5aa23139dd7922e7c9bcf382b1a6989dfb.
  registered: '2026-10-07'
---
# Matched Exact Replay Observations

Original accepted exp280 seed/node directory and exact same ordered cells and U;
centered inner cap935106018721/200000000000 with unchanged48-vertex boundary policy.
Run NONE first, then PHASES in a new process comparing the retained NONE receipt.
Do not compare historical receipt bytes: the new explicitcellsfile has its own custody
metadata. No exp284 geometry and no implicit CALLGRAPH run.

Both fresh same-object runs complete full exact centered replay with identical
mathematical result identities and identical seed/node/cells byte digests.
The PHASES receipt matches the NONE baseline and retains all16 step boundaries,
memo-eviction observations and bounded RSS samples.
Instrumentation never changes verification arithmetic, coverage or acceptance.
This establishes a diagnostic control and observations, not speedup or a new geometric
admission. Resource stops, changed inputs or semantic differences refuse equivalence.

NONE180s + PHASES180s scientific budgets; combined360s inside owned-group
TERM370/KILL380 allowing10s setup/serialization.
One worker, sampled4096MiB PER live process with owned cleanup.
Instrumentation overhead is measured and cannot establish gain.
Input/output ceilings and cooperative checks in the frozen profiler; partial diagnostics
retained.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
