---
title: "exp-249 — the first certified n17 sub-pattern exclusions"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-249
  series: series-000
  title: Two flagged sub-patterns certified infeasible at cap 1169/250 by two independent provers, and admitted
  date: '2026-10-02'
  hypotheses:
  - H-267
  tier: confirmatory
  subject:
    label: Pattern W7 (corner-SW, side-N0, side-W0, side-W1, side-W2, interior-SW, interior-W) by the
      ownership-induction kernel, and pattern A (interior-SW, interior-NW, interior-W, interior-S, interior-N,
      interior-SE) by the interval branch and bound, on the unique-state 24-cell cover at U = 1169/250.
    engine: devtools.check_n17_subpattern --check-saved (the kernel's checker alone) and
      devtools.pilot_n17_subpattern_bb, each certificate re-checked in full by an independent verifier in
      separate exact code
    assurance: verified
    method: exact-algebraic
    host_system: Linux x86_64 remote session container, project Python 3.14.7, one worker per run
    selftest_passed: true
    engine_commit: 15df68ab1ee179601bf9707163d6143213976c34
  instance:
    axis: n
    point: 17
    role: target
  method:
    control: The kernel's falsifiers stall at W7's settings (the endpoint's own west-wall arity-7 sub-pattern,
      and W7 without side-N0, which follows W7's cascade through round 3); the branch and bound certifies no
      control (three endpoint sub-patterns and a placed class, each witness path passing). The W7 review's
      mutation suite refuses 25 of 26 unsound variants and ends the 26th incomplete; the A review's verifier
      rejects 12 of 16 mutant certificates at the right check and all 9 doctored kinds, two sign mutants
      failing safe.
    candidate: W7's saved seed and node (8949a798, 2d516d00) re-certified with the producer never imported;
      A certified again with a certificate written by --save-certificate (manifest 340492bd).
    runs_per_condition: 1
    interleaved: false
    operator: Claude Session 168; lanes K2 and P2 built the provers, lanes R3 and R4 reviewed them, the
      coordinator ran both from a clean worktree
    entry_point: packing/devtools/check_n17_subpattern.py
    command: 'From packing: .venv/bin/python3 -m devtools.check_n17_subpattern --check-saved
      campaign/explorations/X048-session-168-pilots/certificates/W7 --output FILE (run-001);
      .venv/bin/python3 -m devtools.pilot_n17_subpattern_bb --receipt
      campaign/explorations/X048-session-168-pilots/receipts/selector-arity6-seed1.json --index 0
      --split-ratio 0.25 --save-certificate DIR --output FILE (run-002). Exact lines in each run''s
      command.txt.'
    budget: Thirty minutes per run on one worker.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-249-n17-first-certified-sub-patterns
    dirty: false
    commit: 15df68ab1ee179601bf9707163d6143213976c34
  results:
  - shape: determination
    role: outcome
    question: Is W7 infeasible at U, by a certificate the kernel's checker accepts alone and an independent
      verifier re-proves in full?
    outcome: criterion_met
    checked_by: run-001 returns PASS_SAVED_CLOSED on 58 steps and 3,712 rows with 7,752 collision regions,
      closure all_parent_poses_forbidden for side-N0 at step 57. The review's verifier re-proves all 3,712
      rows (3,324 in full, 388 empty), all 7,752 regions by 30,952,184 exact facet inequalities and every
      coverage by an area argument. Transfer 133,152 states and 16,701 orbits, recounted independently.
  - shape: determination
    role: outcome
    question: Is A infeasible at U, by a branch-and-bound certificate an independent verifier re-proves in
      full?
    outcome: criterion_met
    checked_by: run-002 certifies A in 41,598 nodes and 21,215 leaves at depth 31 with no Farkas failure, and
      writes a certificate byte-identical to the one reviewed. The review's verifier re-proves all 41,598
      nodes in exact rationals, the tree's coverage of the root, the piece and pair-split coverage and every
      trigonometric enclosure. Transfer 110,448 states and 13,897 orbits, recounted independently.
  - shape: determination
    role: guard
    question: Do the certified exclusions leave at most 10^4 orbits, H-267's threshold?
    outcome: criterion_missed
    checked_by: With both admitted, census_n17_certified counts 139,976 states and 17,690 orbits, the
      endpoint surviving. Two of the 44 flagged classes are certified; H-267's criterion is decided at arity
      seven, so this is a measurement of progress, not a refutation.
  verdict:
    decision: unresolved
    primary_criterion: The certified residue is at most 10^4 orbits with every certificate independently
      checked; rejected if it exceeds 10^4 at arity seven or a certificate excludes the endpoint state.
    reason: Both certificates are sound and admitted, and the endpoint survives, but 2 of 44 flagged classes
      leave 17,690 orbits. A was certified by an interval branch and bound, which H-267's claim does not
      name among its instruments; the independent review admits it as an equivalent certificate, and that is
      a recorded deviation in the instrument, not in the threshold.
    needs_review: false
    commit: 15df68ab1ee179601bf9707163d6143213976c34
  effort:
    timebox: 1800 seconds per run; one worker
    wall_seconds: 2055.6
    stopped_by: criterion
---
# exp-249: The First Certified n17 Sub-Pattern Exclusions

[H-267](../../../hypotheses/H-267-n17-isolated-sub-pattern-residue.md) asks whether
certified forbidden sub-patterns of arity at most seven bring the n17 census on the
unique-state cover to at most $10^4$ orbits.
Its heuristic selector flags 44 classes.
This experiment records the first two that are certified, by two provers that share no
code.

## What Is Certified

No 7 unit squares with centres in W7’s cells, and no 6 with centres in A’s, fit inside
$[0,1169/250]^2$ with disjoint interiors.
W7 is a chain along the west wall, closed by the
[kernel adapted from n11](../../../explorations/X048-session-168-pilots/README.md): its
west wall pins first, and side-N0 then loses every pose to collision.
A is a crowd of interior cells, closed by the interval branch and bound.
Each prover stalls or times out on the other’s pattern.

Both certificates are retained by hash in
[`certificates/`](../../../explorations/X048-session-168-pilots/certificates/), and each
was re-proved in full by an independent verifier written in separate exact code:
[the W7 review](../../../../../docs/project/reviews/review-2026-10-02-n17-w7-closure.md)
and
[the branch-and-bound review](../../../../../docs/project/reviews/review-2026-10-02-n17-branch-and-bound-certifier.md).
Their scripts and logs are under
[`audit-W7/`](../results/exp-249-n17-first-certified-sub-patterns/audit-W7/) and
[`audit-A/`](../results/exp-249-n17-first-certified-sub-patterns/audit-A/). A’s claim
rests on that certificate check: the review found that the witness-path controls miss
some unsound relaxations, while the verifier rejects them.

## What It Changes

The
[certified-census ledger](../../../explorations/X048-session-168-pilots/certified-sub-patterns.yaml)
now admits both, and
[`census.json`](../results/exp-249-n17-first-certified-sub-patterns/census.json) counts
139,976 surviving states and 17,690 orbits, down from 346,104 and 43,593, with the
endpoint’s state surviving.
The selector’s float penetrations ($1.1\times10^{-2}$ for W7, $1.49\times10^{-2}$ for A)
are search results, not margins: the reviews’ own searches came closer, to about
$9\times10^{-3}$.

H-267 stays undecided.
Forty-two flagged classes remain, and the kernel stalls on the next three it tried.
The
[residue process review](../../../../../docs/project/reviews/review-2026-10-02-n17-residue-process.md)
plans what comes after them.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
