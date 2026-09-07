---
title: exp-127 — fixed collision-augmented H124 axis cover
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-127
  series: series-000
  title: Certify the whole near-axis H124 branch with one fixed collision region
  date: '2026-09-07'
  hypotheses: [H-124]
  tier: confirmatory
  subject:
    label: Fixed q=1939/500, T=110880/50803079, epsilon=1/500 and the original thirteen axis regions plus the proved Cstar S-center region
    engine: Independently source-bound exact closed-polygon endpoint-chain certificates
    engine_commit: 3bec06e2
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64, project Python3.14.7
    selftest_passed: true
  instance: {axis: n, point: 11, role: target}
  method:
    control: >-
      The retained generic cover instruments and original thirteen-region sources
      passed independent controls and reviews before exp125. Two independent
      analytical derivations now prove the fixed displacement and collision
      implication. The new producer and reader passed 41 and 16 unrelated synthetic
      controls; the explicit caller passed 33. Independent source reviews passed
      by11:22:21 UTC. No new scientific source was constructed during authoring.
    candidate: >-
      Exactly one complete near-axis obligation. Retain the old rectangle and all
      thirteen axis regions unchanged, appending the fixed Cstar region directly.
      Use all eight unnormalized support normals with epsilon times L1 penalty.
      No second dilation, changed mark, angle sample, radius refinement, alternate
      source, diagonal rerun or retry is admitted.
    runs_per_condition: 1
    interleaved: false
    operator: Session095 coordinator, BC255; max mathematical judgment
    commit: 3bec06e2
    dirty: false
    entry_point: packing/devtools/run_h124_cover.py
    command: >-
      /usr/bin/time -p env PYTHONPATH=src
      /Users/levy/wrk/github/squares/packing/.venv/bin/python3
      -m devtools.run_h124_cover --axis-collision --limit 5000 --timeout-seconds 120
    budget: >-
      One120-second complete scientific child, including imports, source construction,
      calculation and serialization. Only actual exit zero and a valid covered
      packet authorize one60-second independent child reader. Outer wrapper startup
      and teardown are measured separately, not asserted to have an external120-second
      kill. Do not invoke before Session095 begins11:49 UTC. Launch by12:05 and finish
      by12:09 UTC, otherwise preserve non-invocation. No retry or cap extension.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-127-h124-collision-augmented-axis-cover
  effort:
    timebox: One120-second scientific child; the nonpositive result did not authorize a reader
    wall_seconds: 0.25
    stopped_by: criterion
  results:
  - shape: determination
    role: outcome
    question: Does the fixed collision-augmented representation cover the complete near-axis center domain?
    outcome: criterion_missed
    checked_by: The sole producer exited zero and returned unresolved/no_chain. No independent reader was authorized or invoked; neither source agreement nor a geometric gap was independently certified.
  verdict:
    decision: unresolved
    primary_criterion: Complete independent source reconstruction and endpoint-chain verification of the fixed augmented axis cover, together with the retained diagonal certificate and reviewed continuous compatibility reduction.
    reason: The augmented sufficient cover returned no_chain. H124 and restricted H036 remain unresolved, with exp125's diagonal lemma retained. This ends the fixed representation's allocation without a retry, parameter sweep or diagonal rerun.
    commit: ddf545c9
---
# One Fixed Collision-augmented Axis Cover

The sole producer returned `unresolved` with `no_chain`. H124 and restricted H036 remain
unresolved. No independent reader ran, and this result supplies neither a geometric gap
nor a disjoint-square counterexample.
The fixed representation’s allocation is closed.

## Retained Outcome

The clean `3bec06e2` engine passed its push gate in 147.88 seconds and its isolated fast
handover gate in 169.33 seconds.
Protocol `ddf545c9` passed all 31 immutable record checks in 28.45 seconds after
independent protocol GO at 11:36:19 UTC. The new session had actually begun at 11:51:12
UTC. Full validation remained asynchronous and was not claimed as a passed gate or
substituted for any required admission.

The sole call completed by the observed 11:55:00 UTC boundary, before the original
launch and finish cutoffs, with actual exit zero.
External timing was 0.25 seconds wall, 0.21 user and 0.02 system; the child reported
about 0.122 seconds wall and 0.120 CPU. The envelope had the declared kind and source,
and its nested certificate reported `status=unresolved`, `stop_reason=no_chain` and no
slabs. The packet includes fourteen source polygons, including the constructed
eight-vertex collision region, but these producer-side contents have no independent
target replay.

Only `packet.json` and `producer.log` were created under the declared result directory.
No reader was authorized and no process was repeated.
The diagonal lemma from exp125 is unchanged.
Further diagnosis, a new representation or a parameter refinement needs separate
repricing; this outcome does not fund it.
The independent BC259 support review continues under its own original allocation.

## Retained Prospective Protocol

This protocol tests the remaining near-axis S branch of
[H124](../../../hypotheses/H-124-full-distinguished-square-compatibility.md).
It adds one proved collision region to the failed sufficient representation from
[exp125](exp-125-h124-complete-residual-cover.md); it does not repeat that experiment.
The independently certified diagonal-band result is retained without another call.

## Fixed Source and Admission

The [author proof](../results/agenda-026/bc-255-center-correlated-collision.md) and
[independent derivation](../results/agenda-026/bc-255-center-correlated-review.md)
define the source and prove its collision implication throughout the actual closed angle
bands. The new region is an S-center region: append it directly, without another
Minkowski sum with the S kernel.
Both independently implemented sources retain the old thirteen-region prefix and the
same full center rectangle.

Use the clean immutable `3bec06e2` checkout, with `packing/` as the working directory.
The independent source reviews, immutable push tier, independent protocol review and
committed prospective record checks must pass before the new source is constructed.
The full checkpoint gate is tracked separately; pending is not a claimed pass.
The sole call is held until Session095 starts at or after 11:49 UTC.

Independent protocol review passed at 11:36:19 UTC under `think-60tt` without any
scientific invocation.
The subsequent engine-pointer correction replaces `b38d0376`, whose push gate failed on
record and status-inventory issues.
A direct Git comparison confirmed that all seven new and reused source, caller and
generic cover modules are unchanged at `9d614fef`. Its subsequent gate found only a
stale narrative-round mutation anchor and that anchor’s self-test; `3bec06e2` corrects
the anchor from 82 to 83 while retaining the same mutation to 45. No scientific
constants, algorithms or admission predicates changed.
The final corrected immutable push must still pass before invocation.

Static limits are fourteen polygons, at most 68 vertices, at most 72 supporting lines
including rectangle walls, and at most 2,630 conservative x-events.
The instrument’s unchanged event/slab cap is 5,000; its unchanged packet cap is 2 MiB.
The fixed field is the positive embedding of square root of two.
Empty or degenerate Cstar, source mismatch or arithmetic refusal stops this attempt;
none permits dropping the region or changing the constants.

## One Producer and a Conditional Reader

Run the frontmatter command exactly once.
Retain its stdout as `packet.json` and stderr with external wall/user/system timing as
`producer.log` under the declared result path.
Record the actual tool exit code.
The child’s timeout covers its imports, source construction, calculation and
serialization; the external measurement includes the wrapper and is not itself a
separate operating-system timeout.

Only actual exit zero and a well-formed packet with envelope kind
`h124-closed-cover/v1`, source `h124:axis-collision-v1`, and nested `status=covered` and
`stop_reason=complete` authorize one reader:

```bash
/usr/bin/time -p env PYTHONPATH=src \
  /Users/levy/wrk/github/squares/packing/.venv/bin/python3 \
  -m devtools.run_h124_cover --axis-collision --limit 5000 --timeout-seconds 60 \
  --input /absolute/path/to/exp-127-h124-collision-augmented-axis-cover/packet.json
```

Acceptance requires actual exit zero, the exact same source label,
`status=verified_source_cover` and literal `cover_proved=true`. The nested independent
result must also report `status=verified_cover` and literal `cover_proved=true`. This
independently reconstructs the entire source and checks the full closed slab partition,
endpoint chains and boundary contacts.
Retain `replay.json` and `replay.log` only if that process is actually invoked.

A checked axis cover, the retained exp125 diagonal cover and the reviewed continuous
collision implications establish H124. Restricted H036 additionally uses H106, H123 and
the independently reviewed closed-core counting reduction.
Record that composition explicitly before accepting the restricted theorem.
No unrestricted bound follows.

## Stop and Retention Rules

Any nonpositive producer result ends this allocation.
A well-formed `unresolved` packet with `no_chain`, `event_limit` or `slab_limit` leaves
the sufficient cover unresolved; it is not a disjoint-square witness.
No reader is authorized.
A timeout, nonzero exit, malformed packet, arithmetic refusal, unexpected stop reason or
failed reader also ends the sequence, without a mathematical negative being inferred
from an operational failure.
No completed call is repeated.

Preserve partial or empty output on failure, labeled as such.
Do not invent a reader receipt, resume an expired sequence, extend the cutoff, change
epsilon or rerun the diagonal branch.
Remove the lease and record the scoped terminal verdict when this sequence ends.
The final-slice allocation reserves its checkpoint independently of whether this target
is admitted or successful.

Fresh upstream/open-branch inspection found no exp127 or Session095 in PR110 at
`0e1961e2`. This record allocates exp127 sequentially under `think-nk01`; it allocates
no new hypothesis, agenda, BC or exploration.
The work remains on integrated PR109.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
