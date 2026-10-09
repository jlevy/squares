---
title: "H-281 \u2014 n11 repaired-producer first-round readiness and fresh replay"
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-281
  kind: hypothesis
  claim: The repaired producer completes one certified eleven-owner round on the pinned n11 case-438 cell
    state, preserving the exact endpoint after every update, and a fresh resume-only invocation re-admits
    its saved seed and replays the complete node without any new production or state disagreement.
  lane: proof
  derived_from:
  - X-048
  criterion:
    shape: determination
    metric: complete_n11_first_round_endpoint_and_fresh_replay
    direction: criterion_met
    threshold: Complete round 1 with exactly eleven distinct owner updates; exact endpoint retained after
      seed and every update; producer/checker state agreement; complete saved checkpoint and node; fresh
      seed admission and all eleven saved steps replayed with final_state_agrees=true, identical seed/node
      identities, unchanged round/update records and zero new production.
  instrument: packing/devtools/pilot_n17_capture.py with the repaired hull producer, native current-RSS
    guard, pinned n11 frame and exact trump11 endpoint; actual CLI resume regression in packing/tests/test_pilot_n17_capture.py.
  instrument_ready: true
  regime: One process on macOS arm64 with Python 3.14.7 and gmpy2==2.3.1. Pinned sixteen-cell cover, case
    438 owners [0, 1, 2, 3, 4, 8, 9, 10, 11, 13, 15], U=387708359002281417731/10^20, L=191/50, B=L/U.
    No box cut or prior checkpoint in production. bins 32, max-live 64, min-width 2^-22, octagon core,
    hull-limit 48, seed-grid 0, max-rounds 1. Fresh replay resumes the complete round 1 checkpoint with
    max-rounds 1, so no round 2 is produced. Source and all scientific parameters are frozen before launch.
  instance:
    axis: n
    point: 11
  priority: 1
  cost_estimate: 'First-round cost is unknown and is the measurement: scheduling ceilings 900 seconds
    production and 300 seconds fresh replay, 4096 MiB cooperative current-RSS limit on each process; no
    extrapolated multi-hour estimate.'
  prereqs: []
  replication: false
  registered: '2026-10-07'
  notes: 'Readiness/cost only, no first-round contraction threshold. Exact input, endpoint or replay refusal
    refuses acceptance; resource interruption is incomplete. Top-level PASS_PILOT_MEASURED alone is insufficient.
    Retain E0, E1 as maxima of all eleven owners'' x/y two-sided extents, their ratio, row counts, wall/CPU,
    current and lifetime-peak RSS, objects and replay work. This does not decide R9''s later 15-round
    contraction discriminator or infer n17 capture. Continuation needs a separately registered budget
    informed by measured production, replay and memory cost. Accepted exp268: complete first11-owner round
    and fresh zero-production replay551.28s combined shell, endpoint12checks held; readiness/cost only.
    Original exp265 startup failure preserved.'
---
# H-281: n11 First-Round Producer Control

This is the known-case control for the repaired producer.
It tests a complete checked round from the actual cells and exact replay; it imposes no
contraction threshold on that first round.
Astra approved the scientific discriminator, and the coordinator owns the registration,
resource ceilings and launch.

The endpoint is the exact `cases.trump11.packing` construction over the verified
`pose_tool.root_interval()` bracket, mapped to its eleven owner cells by the retained
pose-inclusion receipt.
The pinned mask-0 loader admits the field packet, audit, cover and D4 bindings before
constructing the frame.
The pose receipt bytes are additionally frozen by exp-265; its loader checks the status
and roles rather than a built-in digest.

The later R9 control remains separate: at completed round 15, $E_{15}/E_0<0.5$ supports
producer readiness, $E_{15}/E_0>0.9$ refuses n17 interpretation, and the closed interval
$[0.5, 0.9]$ is inconclusive.
Missing round 15 is incomplete.
No later-round result is claimed here.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
