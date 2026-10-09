---
title: H-302 — Exact Replay Stage Attribution
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-302
  kind: hypothesis
  claim: Low-frequency stage observers preserve the accepted full exact replay while attributing inclusive/exclusive
    wall,CPU and calls.
  lane: proof
  derived_from:
  - X-048
  criterion:
    shape: determination
    metric: n17-stages-replay-observations
    direction: criterion_met
    threshold: One fresh STAGES run completes fullPASS_STALL, matches accepted exp290attempt2 NONE mathematicalresult
      and identical seed/node/cells bytes, and retains all16stepboundaries with explicitly nestedinclusive/exclusive
      wall/CPU/call attribution and an explicitlyunattributed residual. Temporaryhooks restore aftersuccess/failure,
      no pervertex/globaltrace or verificationarithmeticchange. Runtimeoverhead is diagnostic, not speedup
      or geometricadmission. Limits/custody/semanticmismatch are incomplete/refused.
  instrument: packing/devtools/profile_n17_exact_replay.py
  instrument_ready: true
  regime: Original accepted parent/witness/native objects only; prospective frozen source/command plan.
    STAGES matches acceptedNONEbaseline; allobservers outsideexactmathematicalpayload.
  instance:
    axis: n
    point: 17
  priority: 2
  cost_estimate: One worker; STAGES180s cooperative replaybudget,owned-group TERM190/KILL200 allowing10s
    setup/serialization;4096MiB sampled currentRSS PERliveprocess. Same originalnative/cells/input/output/sourcecaps
    asacceptedNONE/PHASES; fullsame-objectexactresult required. Timing underoverlaphostactivity neverestablishesgain.
  prereqs:
  - H-291
  - H-299
  replication: false
  notes: 'Author33targetfreecontrolsPASS1.10s,independentSol33PASS1.14s,Ruff/format/types0; controlledtoyfreshprocesssemanticparity
    andrestoration/failurecontrols. Standing/primitives sourceunchanged. AcceptedfullNONEbaseline fromexp290attempt2,
    nothistoricaldifferentcellspath. No actual STAGES target was read before registration. Exp294 accepted:
    full same-object payload/input equality and all16 observed boundaries, zero failed calls; coverage57.292715s,
    collisions10.218034s exclusive wall. Diagnostic only; no speedup or new geometric admission.'
  registered: '2026-10-07'
---
# Exact Replay Stage Attribution

Low-frequency stage observers preserve the accepted full exact replay while attributing
inclusive/exclusive wall,CPU and calls.

One fresh STAGES run completes fullPASS_STALL, matches accepted exp290attempt2 NONE
mathematicalresult and identical seed/node/cells bytes, and retains all16stepboundaries
with explicitly nestedinclusive/exclusive wall/CPU/call attribution and an
explicitlyunattributed residual.
Temporaryhooks restore aftersuccess/failure, no pervertex/globaltrace or
verificationarithmeticchange.
Runtimeoverhead is diagnostic, not speedup or geometricadmission.
Limits/custody/semanticmismatch are incomplete/refused.

One worker; STAGES180s cooperative replaybudget,owned-group TERM190/KILL200 allowing10s
setup/serialization;4096MiB sampled currentRSS PERliveprocess.
Same originalnative/cells/input/output/sourcecaps asacceptedNONE/PHASES;
fullsame-objectexactresult required.
Timing underoverlaphostactivity neverestablishesgain.

Author33targetfreecontrolsPASS1.10s,independentSol33PASS1.14s,Ruff/format/types0;
controlledtoyfreshprocesssemanticparity andrestoration/failurecontrols.
Standing/primitives sourceunchanged.
AcceptedfullNONEbaseline fromexp290attempt2, nothistoricaldifferentcellspath.
No actual STAGES target was read before registration.

Measured exp294 completes the registered diagnostic criterion.
Full replay payload and input bytes match NONE, and all 16 owner/count boundaries match
PHASES. Coverage is the largest measured stage; see the
[completed result](../series/series-000-smoke-and-calibration/results/exp-294-stages-exact-replay/README.md).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
