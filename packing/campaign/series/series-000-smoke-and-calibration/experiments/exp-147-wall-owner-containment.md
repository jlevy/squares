---
title: exp-147 — wall-owner component-containment expansion
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-147
  series: series-000
  title: Wall-owner component-containment expansion
  date: '2026-09-09'
  hypotheses:
  - H-145
  tier: exploratory
  subject:
    label: Sixteen wall-aware owner classes against two certified four-patch families
    engine: Exact rational polygon half-plane containment and union-of-products counting in devtools.wall_owner_containment
    assurance: verified
    method: exact-algebraic
    host_system: Darwin arm64; project Python 3.14; one process
    selftest_passed: true
    engine_commit: e72102e15897dc33e59fcd82818a7ca9174d3cd0
  instance:
    axis: n
    point: 11
    role: target
  method:
    control: Synthetic exact inclusion, malformed star refusal, cross-input baseline identities, deadline
      overrun refusal, D4 transport and the 175-impossible/31-covered/50-unresolved toy partition; Astra
      Max mathematical source review.
    candidate: Evaluate all 128 family/corner/class slots and count the union of the two products of accepted
      class sets, subtracting their intersection and the two covered baseline tuples.
    runs_per_condition: 1
    interleaved: false
    operator: GPT-6 Astra coordinator; implementation by GPT-5.6 Sol extra high; mathematical admission
      by GPT-6 Astra max
    entry_point: packing/devtools/wall_owner_containment.py
    command: cd packing && /opt/homebrew/bin/timeout --signal=TERM --kill-after=2s 120s .venv/bin/python3
      -m devtools.wall_owner_containment campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-143-four-owner-footprint-cover.json
      campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-146-wall-owner-footprints.json
      --replay-receipt campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-144-four-owner-endpoint-full-net-replay.json
      --coverage-receipt campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-145-independent-five-dot-union.json
      --expect-endpoint-blob cc66f06ddd3f7cc52d8a06d30a3920ba8e992c19 --expect-wall-blob e54fa98133db5f2135cae8875188f51b7db26e12
      --expect-wall-source 915758898a97c92793f51e62b7a6b17f846895ca --expect-replay-blob e445cca80d95c77226cdf324414ab269152e26d0
      --expect-coverage-blob 4688678bfd4e64d9cb345b48f065c1c82bebdea0 --expect-git-revision "$(git rev-parse
      HEAD)" --deadline-seconds 60 --output campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-147-wall-owner-containment.json
    budget: One 120-second external process with two-second termination grace; a 60-second cooperative
      clock starts after input loading. No tuning, retry, overwrite or resume. Launch by 15:53:07 UTC
      so the complete allowance fits before 15:55:09 UTC.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-147-wall-owner-containment.json
    commit: e72102e15897dc33e59fcd82818a7ca9174d3cd0
    dirty: false
  results:
  - shape: determination
    role: outcome
    question: Does complete valid component containment add a tuple beyond the two baselines?
    outcome: criterion_missed
    checked_by: 'All 128 exact relations completed: eight contained, 120 not contained. The two family
      products each contain one tuple, with no overlap; both are existing baselines.'
  verdict:
    decision: rejected
    primary_criterion: Complete all 128 logical relations validly and certify at least one distinct owner
      tuple beyond the two baseline tuples.
    reason: The complete exact matrix covers only the two baseline tuples, with zero new covered tuples.
      This refutes component-containment expansion for the frozen classes, not direct coverage by the
      five dots.
  effort:
    timebox: One 120-second external process and 60-second cooperative clock after input loading; no retry.
    wall_seconds: 40.88
    stopped_by: criterion
---
# Exp147: No New Tuple Inherits the Exclusion

**Rejected under its declared criterion.** The single run launched at 15:47:15 UTC from
clean published `e72102e15897dc33e59fcd82818a7ca9174d3cd0` and exited zero in 40.88
seconds. All 128 relations completed: eight containments and 120 exact failures.
Only the two baseline tuples are covered; 65,534 labels remain unresolved by this
method. No class is impossible.
Internal elapsed time was 33.43337650000467 seconds.
The result does not refute direct five-dot coverage or establish a feasible packing.
The next selected test is the fixed-dot witness bank and one surviving candidate.

**Prospective history, now discharged.** Publish the controlled adapter and this
protocol before one target invocation.
Capture the full published revision, clean Git state, UTC start, process exit and
elapsed seconds outside the repository before the clean-tree guard.
The four input blobs and exp146 constructor revision are fixed in the command above.

Accept only a complete valid 128-slot matrix whose union-of-products count adds at least
one tuple beyond (m1:j0)⁴ and (m2:j7)⁴. Reject this extension only if the complete valid
matrix adds none.
Missing receipts, malformed inputs, exceptions and partial or timed-out
runs remain unresolved.
An external kill may leave no JSON; retain its process log without manufacturing a
mathematical verdict.

There are two patch families, four corners and sixteen classes.
Each old certified patch must be contained in the corresponding new guaranteed wall
footprint. Use one family consistently across all four corners.
Count the union of the two products, subtract their overlap once, and exclude impossible
classes before counting.
The 65536 label combinations can overlap as physical cases.

The 120-second guard covers the whole process; the cooperative 60-second clock starts
after input loading and checks completion as well as intermediate slots.
Keep the internal and process timings separate.
No direction-by-direction covering rerun is needed to transfer the already admitted
certificates by symmetry and containment.

This adapter consumes the retained constructor and coverage evidence; it is not an
independent verifier for arbitrary upstream receipts.
Any gain is an additional sufficient condition for exclusion, not an exhaustive n11
proof or an automatic promotion of T-023. The
[source admission](../../../../cases/n11_five_dot_cover/wall-containment-source-admission.md)
states the remaining analytic premises.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
