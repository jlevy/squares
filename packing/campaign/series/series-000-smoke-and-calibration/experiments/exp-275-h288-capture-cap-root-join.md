---
title: "exp-275 \u2014 exact capture cap generation and fresh checker"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-275
  series: series-000
  title: Exact frozen numeric capture cap and fresh standalone root/side checker
  date: '2026-10-07'
  hypotheses:
  - H-288
  tier: confirmatory
  subject:
    label: Complete accepted root R, fixed capture cap935106018721/200000000000 and
      outer cap1169/250.
    engine: devtools.check_n17_capture_cap, source frozen by coordinator before target.
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64; external Python3.14.7/SymPy; separate generation/fresh-check
      processes; external scratch.
    selftest_passed: true
  instance:
    axis: n
    point: 17
    role: target
  method:
    control: 25 cap synthetic controls plus one mocked pilot side.lo regression passed1.11s;
      independent26controls passed2.87s; Ruff/BasedPyright zero. No accepted-root
      target read. Final provenance-only binding explicitly locates forcing.Dyadic
      class source; no arithmetic change.
    candidate: Frozen full-root side/cap criterion, independent monotone box and preserved
      outward consumer box, exact symbolic endpoint-layout/derivative join; no producer.
    runs_per_condition: 1
    interleaved: false
    operator: Sol coordinator registers/freezes/supervises exact generation and fresh
      standalone checker; Session184.
    entry_point: packing/devtools/check_n17_capture_cap.py
    command: 'From packing/ under root launch supervisor and required external scratch
      variables: external venv/bin/python -m devtools.check_n17_capture_cap --output
      campaign/series/series-000-smoke-and-calibration/results/exp-275-capture-cap-root-join/certificate.json;
      NEW process repeats with --certificate pointing to that receipt and --output
      .../replay.json. Both use identical frozen root path. Freeze exact arrays/interpreter/source/root
      identities before launch.'
    budget: 180s combined generation and fresh checker; fresh lease limited by remaining
      parent time; TERM180/KILL190 cleanup. No producer, new root search, cap tuning
      or object relabel. Preserve honest failed bounds/refusals/interruption.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-275-capture-cap-root-join
    commit: 3575c02a761d9ae439add4b19707575e3cfdbcf7
    dirty: false
  results:
  - shape: determination
    role: outcome
    question: Fresh accepted full root R and exact endpoint side/derivative identities;
      0<t_lo<=t_hi<1, positive denominator, negative derivative numerator; exact monotone
      [F(t_hi),F(t_lo)] and unchanged outward consumer side enclosure; fixed Uprime=935106018721/200000000000
      strictly above both upper endpoints with Uprime-minus-each-lower endpoint <=1e-12,
      and Uprime<=1169/250. Generation and new-process checker agree, cap_certified=true,
      all capture/leaf/global/relabel/producer flags false.
    outcome: criterion_met
    checked_by: Generation/freshchecker sciencepayloads agree; fullrootmonotone+consumer
      sidejoins andallstrictgapguards pass, cap_certified/verification_passed true.
      Maximumconsumerexcess about4.49048365992313e-13 displayonly; exactrationalcomparisons
      retained. No producer/capture/global/oldobjectrelabel.
  verdict:
    decision: accepted
    primary_criterion: Fresh accepted full root R and exact endpoint side/derivative
      identities; 0<t_lo<=t_hi<1, positive denominator, negative derivative numerator;
      exact monotone [F(t_hi),F(t_lo)] and unchanged outward consumer side enclosure;
      fixed Uprime=935106018721/200000000000 strictly above both upper endpoints with
      Uprime-minus-each-lower endpoint <=1e-12, and Uprime<=1169/250. Generation and
      new-process checker agree, cap_certified=true, all capture/leaf/global/relabel/producer
      flags false.
    reason: Generation/freshchecker sciencepayloads agree; fullrootmonotone+consumer
      sidejoins andallstrictgapguards pass, cap_certified/verification_passed true.
      Maximumconsumerexcess about4.49048365992313e-13 displayonly; exactrationalcomparisons
      retained. No producer/capture/global/oldobjectrelabel.
    needs_review: false
  effort:
    timebox: Combined180s TERM/KILL190, sampled4096MiB perownedprocess
    wall_seconds: 1.21
    stopped_by: criterion
---
# exp-275: Frozen Numeric Cap

Generation and a new-process checker share a single 180-second deadline, with TERM at
180 seconds and KILL at190. Fresh replay reconstructs the accepted root, symbolic side
and derivative identities, both exact enclosures and all fixed cap inequalities.
Stored pass flags alone are insufficient.

The accepted root domain is the independently checked inclusion interval, not a printed
decimal or bare midpoint.
Honest failure of the finite cap inequalities is inconclusive; changed constants,
malformed input or root/receipt mismatch is refused.
A deadline stop is incomplete and supplies no cap acceptance.

The arithmetic defect and minimal pilot correction are tracked in `think-p13m`. No old
None/U seed/node is relabelled or reused as numeric-cap evidence.
This instrument is a root/cap certificate only; H289’s new producer control remains a
separate target.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
