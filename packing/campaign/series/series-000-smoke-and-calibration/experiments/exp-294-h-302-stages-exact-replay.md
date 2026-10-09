---
title: exp-294 — Exact Replay Stage Attribution
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-294
  series: series-000
  title: Exact Replay Stage Attribution
  date: '2026-10-07'
  hypotheses:
  - H-302
  tier: confirmatory
  subject:
    label: Original accepted exp280samecanonical seed/node/cells; full16-stepstandingreplay withSTAGES
    engine: Unchanged exactreplay with low-frequency STAGES observers
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64; external Python3.14.7/gmpy2==2.3.1
    selftest_passed: true
  instance:
    axis: n
    point: 17
    role: target
  method:
    operator: Sol coordinator registers/freezes/supervises/disposes in Session185.
    control: Author33targetfreecontrolsPASS1.10s,independentSol33PASS1.14s,Ruff/format/types0; controlledtoyfreshprocesssemanticparity
      andrestoration/failurecontrols. Standing/primitives sourceunchanged. AcceptedfullNONEbaseline fromexp290attempt2,
      nothistoricaldifferentcellspath. NoactualSTAGES target read.
    candidate: Original accepted parent/witness/native objects only; prospective frozen source/command
      plan. STAGES matches acceptedNONEbaseline; allobservers outsideexactmathematicalpayload.
    runs_per_condition: 1
    interleaved: false
    entry_point: packing/devtools/profile_n17_exact_replay.py
    command: Frozen argv arrays in execution-manifest.json; originalinputbytes and selectedcriterion remainunchanged
      afterregistration.
    budget: One worker; STAGES180s cooperative replaybudget,owned-group TERM190/KILL200 allowing10s setup/serialization;4096MiB
      sampled currentRSS PERliveprocess. Same originalnative/cells/input/output/sourcecaps asacceptedNONE/PHASES;
      fullsame-objectexactresult required. Timing underoverlaphostactivity neverestablishesgain.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-294-stages-exact-replay
    commit: 0f7b96c7a7457c19445de7366d4c77224f7d917f
    dirty: false
  results:
  - shape: determination
    role: outcome
    question: Does STAGES preserve the complete same-object exact replay and retain all16 step observations?
    outcome: criterion_met
    checked_by: COMPLETE full PASS_STALL; independent mechanical audit recomputes identical full mathematical
      payload and inputbyte digests against NONE, all16 owner/count boundaries against PHASES, zero failed
      observed calls and exact exclusive-plus-residual clock accounting.
  verdict:
    decision: accepted
    primary_criterion: One fresh STAGES run completes fullPASS_STALL, matches accepted exp290attempt2
      NONE mathematicalresult and identical seed/node/cells bytes, and retains all16stepboundaries with
      explicitly nestedinclusive/exclusive wall/CPU/call attribution and an explicitlyunattributed residual.
      Temporaryhooks restore aftersuccess/failure, no pervertex/globaltrace or verificationarithmeticchange.
      Runtimeoverhead is diagnostic, not speedup or geometricadmission. Limits/custody/semanticmismatch
      are incomplete/refused.
    reason: Fresh full STAGES replay matches accepted NONE mathematical/input identities and all16 PHASES
      step boundaries. Coverage is the largest measured stage:57.292715s exclusive wall; collisions10.218034s.
      Diagnostic only; no speedup, exp284 explanation or geometric admission.
    needs_review: false
  effort:
    stopped_by: criterion
    timebox: One worker; STAGES180s cooperative replaybudget,owned-group TERM190/KILL200 allowing10s setup/serialization;4096MiB
      sampled currentRSS PERliveprocess. Same originalnative/cells/input/output/sourcecaps asacceptedNONE/PHASES;
      fullsame-objectexactresult required. Timing underoverlaphostactivity neverestablishesgain.
    wall_seconds: 108.620915
---
# Exact Replay Stage Attribution

One fresh STAGES run completes fullPASS_STALL, matches accepted exp290attempt2 NONE
mathematicalresult and identical seed/node/cells bytes, and retains all16stepboundaries
with explicitly nestedinclusive/exclusive wall/CPU/call attribution and an
explicitlyunattributed residual.
Temporaryhooks restore aftersuccess/failure, no pervertex/globaltrace or
verificationarithmeticchange.
Runtimeoverhead is diagnostic, not speedup or geometricadmission.
Limits/custody/semanticmismatch are incomplete/refused.

Author33targetfreecontrolsPASS1.10s,independentSol33PASS1.14s,Ruff/format/types0;
controlledtoyfreshprocesssemanticparity andrestoration/failurecontrols.
Standing/primitives sourceunchanged.
AcceptedfullNONEbaseline fromexp290attempt2, nothistoricaldifferentcellspath.
No actual STAGES target was read before registration.

One worker; STAGES180s cooperative replaybudget,owned-group TERM190/KILL200 allowing10s
setup/serialization;4096MiB sampled currentRSS PERliveprocess.
Same originalnative/cells/input/output/sourcecaps asacceptedNONE/PHASES;
fullsame-objectexactresult required.
Timing underoverlaphostactivity neverestablishesgain.

## Measured Outcome

The completed full `PASS_STALL` replay matches the accepted NONE mathematical payload
and all three input byte digests.
All 16 owner/count boundaries match PHASES, with no failed observed calls.
The replay took 108.237456s wall and 104.257205s CPU; outer supervision took 108.620915s
with normal exit and complete cleanup.

`check_cover` used 57.292715s exclusive wall, `check_step` outside observed nested
stages used 23.232524s, `check_collisions` used 10.218034s, and final-state comparison
used 10.255051s. The unattributed residual was 0.224548s wall.
These observations justify finer coverage attribution before selecting an optimization;
they do not establish a speedup or explain the unaccepted exp284 timeout.

The [mechanical summary](../results/exp-294-stages-exact-replay/mechanical-summary.json)
retains complete stage wall/CPU/call totals, custody checks and resource observations.
The [result README](../results/exp-294-stages-exact-replay/README.md) states the
diagnostic scope.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
