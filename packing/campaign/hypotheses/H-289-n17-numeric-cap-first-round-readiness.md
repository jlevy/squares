---
title: H-289 — numeric-cap full17 first-round readiness
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-289
  kind: hypothesis
  claim: The repaired producer completes the first16 contracting-owner round from a new full17 numeric-cap
    cell seed, preserving all17 exact endpoint poses and exact states, and fresh resume-only replay
    re-admits the complete saved seed/node without new production.
  lane: proof
  derived_from:
  - X-048
  criterion:
    shape: determination
    metric: numeric_cap_full17_first_round_and_fresh_replay
    direction: criterion_met
    threshold: Accepted H288 full-root numeric cap935106018721/200000000000; new full17 cell seed
      at that numeric cap, exactly16 distinct complete contracting-owner round1 updates (square6 remains
      coarse), all17 exact endpoint poses retained after seed and each update (17 checks), exact producer/checker
      state agreement and complete round1 checkpoint. New-process resume --max-rounds1 re-admits the
      entire original17-owner seed and replays all16 steps/finalstate with identical contentIDs, unchanged
      round/update records and zero new producer updates. Fresh resume adds one all17-pose final-state
      endpoint check; it does not rerun all17 production checkpoint checks. No closure, convergence,
      terminal or census claim.
  instrument: packing/devtools/pilot_n17_capture.py and input-only check_n17_capture_checkpoint.py;
    corrected whole-root cap guard and dedicated synthetic17-owner/16-step fresh CLI resume control.
  instrument_ready: true
  regime: New full17 endpoint cells at checked fixed Uprime, no --box and no old checkpoint/None-U
    seed. bins32,maxlive64,minwidth2^-22,hull48,octagon,seedgrid0,maxrounds1; square6 remains coarse
    with all its full rows.
  instance:
    axis: n
    point: 17
  priority: 1
  cost_estimate: Production900s and fresh replay300s; currentRSS4096MiB cooperative guard and owned-process
    cleanup.
  prereqs:
  - H-288
  replication: false
  registered: '2026-10-07'
  notes: Actual H289 target unrun. H288 cap certificate is accepted; source readiness passed Astra
    mathematical and independent Sol mechanical review. Independent helper25 controls passed0.78s
    and freshCLI1 passed1.71s. Helper25+fresh CLI1 target-free controls passed26/1.76s; Ruff/types
    zero. Actual root/cap/frame input join is the first CONTROL phase of registered exp276, before
    production, not an unregistered readiness measurement. No real pilot root prevalidation.
---
# H-289: Numeric-Cap First-Round Readiness

Use a new full-17 wall seed at the cap accepted by H288. Existing None/U objects retain
their original custody and are not relabelled, resumed or substituted here.
A retained input control must bind exp238’s exact geometry-box midpoint and inclusion
bounds to the freshly accepted H288 root, prove the pilot’s outward 10^-40 t/beta boxes
contain the H288 inclusion domain, and require exact frozen cap equality plus the
corrected maximum-excess check against the pilot’s own `side.lo`. Neither matching Git
references nor overlapping side intervals establish this root join.

The repaired current producer updates the 16 contracting owners; square6 remains coarse
with its complete rows.
The endpoint check still covers all17 poses after the seed and each update, so a
complete first round requires17 checks.

Fresh replay uses only this run’s complete round1 checkpoint and `--max-rounds 1`. A
target-free n17/16-owner CLI control must prove that this executes zero new production,
re-admits all17 saved seed owners and replays all16 saved steps.
Fresh resume separately checks the all17-pose final state; it does not repeat the
production’s17 endpoint checkpoint checks.
A copied n11 count is insufficient.

Acceptance is first-round readiness, complete checkpoint custody and measured cost only.
There is no contraction threshold, convergence prediction, terminal predicate, exclusion
or census change. Resource stops before complete production/replay are incomplete;
endpoint loss, exact identity/state disagreement or refused replay are refused.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
