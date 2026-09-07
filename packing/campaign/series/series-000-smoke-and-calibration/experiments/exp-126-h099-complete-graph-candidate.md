---
title: exp-126 — complete graph certificate for the fixed mass56/5 candidate
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-126
  series: series-000
  title: Independently certify complete a.e. depth for the unchanged exp113 weights
  date: '2026-09-07'
  hypotheses: [H-099]
  tier: confirmatory
  subject:
    label: Fixed exact Trump D4 support and unchanged exp113 rational orbit weights of total mass56/5
    engine: Source-bound conservative interior-overlap graph and complete weighted-clique certificate
    engine_commit: 7daa7c55
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64, project Python3.14.7
    selftest_passed: true
  instance: {axis: n, point: 11, role: target}
  method:
    control: >-
      Independently reviewed source-free graph and geometry instruments. All five
      BC243 scientific controls passed under think-b9i7: overlapping half-weight
      acceptance, original and uniform mass-eleven source acceptance, strict
      positive-area perturbed-source rejection and genuine overweight-clique
      nonacceptance. All ten producer/reader exits zero;18.65 seconds wall total.
    candidate: >-
      The accepted exp113 parent packet, full sixty-square D4 support and exact
      orbit weights1,0,2/5,1/10,0,1/10,3/10,0. No new placement, weight, LP,
      necessary row, symmetry, heuristic or alternative certificate is selected.
    runs_per_condition: 1
    interleaved: false
    operator: Session094 coordinator, BC243; max mathematical judgment
    commit: 7daa7c55
    dirty: false
    entry_point: packing/devtools/run_full_size_density_graph.py
    command: >-
      /usr/bin/time -p env PYTHONPATH=src
      /Users/levy/wrk/github/squares/packing/.venv/bin/python3
      -m devtools.run_full_size_density_graph
      --candidate campaign/series/series-000-smoke-and-calibration/results/exp-113-h-099-trump-support-screen/packet.json
      --node-limit 10000 --timeout-seconds 60
    budget: >-
      Exactly one producer with a60-second complete scientific-child cap. Only actual exit zero and a
      complete matching proved_graph_bound packet authorize one independent
      reader with the same60-second scientific-child cap. Outer wrapper startup and
      teardown are measured separately in the external process timing.
      Every other result stops without a reader or retry. Preserve10000
      graph nodes and all existing geometry/arithmetic/input caps. Launch by11:12
      UTC and finish by11:15 UTC, or retain non-invocation. No cap extension.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-126-h099-complete-graph-candidate
  effort:
    timebox: One60-second scientific child; no independent reader was authorized or invoked
    wall_seconds: 4.49
    stopped_by: criterion
  results:
  - shape: determination
    role: outcome
    question: Does the complete conservative graph bound certify the unchanged mass56/5 candidate?
    outcome: criterion_missed
    checked_by: Sole producer actual exit zero with unresolved/overweight_clique; it reports36 retained positive vertices,630 pairs and a five-vertex clique of weight6/5. The protocol did not authorize an independent reader, so this is not independently checked geometric infeasibility.
  verdict:
    decision: unresolved
    primary_criterion: Complete independently source-bound a.e.-depth at most one for the fixed contained family, with exact mass56/5 greater than eleven.
    reason: The conservative graph contains a reported overweight clique, so this sufficient depth certificate failed. No common geometric interior was certified and no independent target reader ran. H099 and its fixed-support bracket remain unresolved and unchanged.
    commit: a3ce0b9c
---
# One Complete Fixed-Candidate Graph Test

The sole producer returned `unresolved` with `overweight_clique`. H099 remains
unresolved; an overweight clique in the conservative graph does not establish common
geometric interior. The fixed-support bracket remains [11,56/5].

## Retained Outcome

Protocol `a3ce0b9c` and its durable-document map correction `5195f903` were committed
before invocation. The latter passed all 31 immutable record checks in 24.33 seconds.
The engine remained the clean `7daa7c55` checkout that had already passed full/push
validation and all five scientific controls. The producer launched at the observed
11:11:15 UTC boundary, before the original 11:12 cutoff, and returned actual exit zero.
External timing was 4.49 seconds wall, 4.45 user and 0.03 system.

The retained packet reports sixty source squares, 36 positive-weight graph vertices and
630 pair tests. Its adapter status is `unresolved`; the graph certificate status and
stop reason are both `overweight_clique`. It reports local graph vertices [1,2,7,9,10]
with weight 6/5. These are indices in the retained positive-vertex graph, not original
packing labels. No independent target replay or geometric common-interior check was
authorized by this nonpositive result.

The producer and external timing are retained under the declared result directory.
No reader files were created and no process was repeated. This experiment does not
refute H099, establish that the fixed weights are geometrically invalid, or alter any
packing bound. Any higher-order geometric obligation needs separate repricing; it does
not follow automatically from this failed sufficient certificate.

## Retained Prospective Protocol

This is a new complete sufficient certificate for the unchanged exp113 candidate, not
another LP solve, pair screen or arrangement retry.
The graph retains every possible interior overlap and all unknown pairs.
A complete clique-weight upper bound of one therefore proves a.e. depth at most one.
An overweight clique is not a geometric counterexample: pairwise intersection need not
imply common interior.

## Admission and Commands

Use clean immutable engine `7daa7c55`, with its `packing/` as the working directory.
Its full gate passed in1623.67 seconds and push tier passed45/45 in153.55 seconds.
The five independently replayed scientific controls are retained in the
[BC243 assessment](../results/agenda-026/bc-243-graph-depth-assessment.md#reviewed-allocation-outcome).
Commit this protocol and pass independent protocol review and record checks before
constructing the candidate source.

Independent max protocol review passed at11:03:16 UTC, after142 seconds of static
review. The frozen caller’s60-second timeout covers the complete scientific child,
including imports, source construction, checking and serialization.
The outer wrapper has separately measured startup/teardown overhead; no separate
external60-second kill is claimed.
The original launch and finish cutoffs still apply to the entire sequence.

The relative `--candidate` path in the declared command resolves inside that immutable
engine. Both routes bind the entire accepted parent support and fixed rational weights;
the independent reader reconstructs them separately.
Zero-weight placements remain in the source identity and containment checks, even though
they need not enter the clique search.
There are sixty source placements; all source members must be accounted for.

Retain producer stdout as `packet.json`, stderr and external timing as `producer.log`,
and actual exit. Require absent output paths before launch.
Only actual exit zero, `version=1`, source `exp-113-candidate-v1`, matching side and
full source, and nested adapter `status=proved_graph_bound` with complete graph
`proved_upper_bound` authorize one independent replay:

```bash
/usr/bin/time -p env PYTHONPATH=src \
  /Users/levy/wrk/github/squares/packing/.venv/bin/python3 \
  -m devtools.run_full_size_density_graph \
  --candidate campaign/series/series-000-smoke-and-calibration/results/exp-113-h-099-trump-support-screen/packet.json \
  --node-limit 10000 --timeout-seconds 60 \
  --input /absolute/path/to/exp-126-h099-complete-graph-candidate/packet.json
```

Retain replay stdout as `replay.json` and stderr/timing as `replay.log`. Acceptance
requires actual exit zero, matching source, `status=verified_density_bound`, literal
`bound_proved=true`, exact mass string `"56/5"`, independent containment and complete
sixty-square source binding.
Its nested geometry result must be `verified_depth_bound` with literal
`bound_proved=true`, and its complete graph replay must be `verified_upper_bound` with
literal `bound_proved=true`. Missing source members, unreplayed nonedges or branches,
malformed output, or a failed reader prohibit acceptance.

## Scoped Verdict and Stop

A passing independent replay accepts H099. Together with exp113’s retained finite-row
upper certificate, it establishes that the supremum on this exact fixed D4 support is
56/5. Through the reviewed weak-duality contract it rules out a mass-eleven area density
at the exact Trump side.
It does not rule out below-Trump density, prove Trump optimal, or improve the
unrestricted unit-square packing lower bound.

Every nonpositive producer result is unresolved and stops this experiment without a
reader. In particular an overweight clique is a graph obstruction only, not a strict
positive-area overlap witness or a rejection of H099. Node exhaustion, timeout,
arithmetic refusal, malformed output or incomplete evidence are also unresolved.
No second candidate, budget extension, changed support or changed weights follow
automatically.
Keep partial or empty stdout if a process fails, and do not manufacture an
uninvoked reader receipt.
Remove the lease and retain the verdict when the sequence ends.

Fresh upstream/open-PR inspection at10:58 UTC found no exp126 in PR110 at `1b7ed623`.
This record allocates exp126 sequentially; H099 is unchanged and no new hypothesis,
session, agenda, BC or exploration ID is allocated.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
