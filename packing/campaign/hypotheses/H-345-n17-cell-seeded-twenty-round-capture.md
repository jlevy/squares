---
title: H-345 — twenty rounds of the repaired capture producer from the family's cells move something
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-345
  kind: hypothesis
  claim: >-
    A 20-round run of the n17 capture producer from the family's occupancy state seeded
    on its own cells at cap U' = 935106018721/200000000000 (the exp-276 path: centred
    walls, hull allowance 48, the hull-pull repair at 2^-18, all 17 owners), with fresh
    replay of every round, reduces at least one owner's orientation range or at least
    one wall-fed one-sided position extent by at least 10 per cent of its round-1 value
    by round 20, while retaining all 17 endpoint poses after every update.
  lane: proof
  derived_from: [X-052]
  criterion:
    shape: determination
    metric: >-
      The scorer's per-round orientation range and one-sided and two-sided position
      extents for every owner, relative to round 1; the endpoint-retention check after
      every update; wall time per round and live rows; separate outcomes for the
      contraction threshold, a verified fixed point, a timeout and unresolved progress.
    direction: >-
      Confirm when some owner's orientation range or wall-fed position extent falls by
      at least 10 per cent by round 20 with every endpoint pose retained. No such
      movement after 20 completed, replayed rounds refutes this contraction-budget
      claim for the specified configuration. It neither proves a fixed point nor rules
      out the kernel architecture: slower continuing contraction can miss the threshold.
      A timeout before round 20 is censored and unresolved. Require an exact invariant
      or fixed-point proof before making a structural claim. A lost endpoint pose
      invalidates the control and prevents a contraction verdict.
    threshold: at least one owner, at least 10 per cent, by round 20; 17 of 17 endpoint poses retained.
  instrument: >-
    devtools/pilot_n17_capture.py with --max-rounds 20 on the exp-276 configuration
    (full 17-owner seed, centred cap, hull limit 48), from a clean worktree at a commit
    containing 917163641; devtools/check_n17_capture_checkpoint.py for the fresh replay;
    devtools/score_n17_capture.py for the reading.
  instrument_ready: true
  regime: >-
    n = 17; the family's state; cap U'; the cells of the H-266 cover in the U frame as
    the seed; the repaired producer; rows growing with refinement as exp-276 measured
    (544 seed rows, 1,024 after round 1, 176 s for the round).
  instance: {axis: n, point: 17}
  priority: 1
  cost_estimate: >-
    5 to 20 CPU-hours (rounds grow with the live rows; exp-276's round 1 took 176 s);
    about 4 agent-hours including the reading; run after H-337 or beside it.
  prereqs: [H-289, H-337]
  replication: false
  registered: '2026-10-09'
  notes: >-
    X-052's direction 3, the n17 analogue of the n11 proof's root node, which contracted
    from its cells in 14 rounds and has never been run to a verdict at n17: exp-276,
    exp-277 and exp-280 completed one round and left every owner's orientation interval
    whole. Every contraction reading in the record comes from 1/1024-box seeds, which
    assume the hard part. R9's box-set reading rests on corner-to-edge facts
    homogeneous in the box radius from a symmetric seed; from the cells the seed is
    asymmetric (eleven squares on walls) and the question is empirical and costs hours.
    Correction of 9 October following review C4: the twenty-round threshold is a
    bounded operational trial. It cannot confirm R9's fixed-point interpretation or
    establish architectural failure without an additional exact invariant or
    fixed-point proof.
---
# H-345: Run the Engine From Where the Proof Starts

**Mechanism.** The pairwise ownership induction is the capture engine of the n = 11
proof, and at n = 17 it has been run from the actual starting point for one round.
Whether it contracts from an asymmetric cell seed with eleven squares on walls is a
question about the dynamics of that starting domain.
Twenty rounds measure the registered contraction threshold; they do not decide eventual
contraction.

**Falsifier.** No owner’s orientation range or wall-fed position extent moves by ten per
cent in twenty rounds.

**Expected information.** Whether this configuration contracts by the declared amount in
twenty rounds, and its per-round progress and cost.
H-337 supplies a separate check of the producer implementation.

**Limits.** A pass measures contraction from the cells; reaching the terminal region,
seven to twelve bisections away in every coordinate, remains a separate obligation.
A failed threshold does not rule out slower contraction or another kernel configuration.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
