---
title: "exp-242 — n17 common-core first-order stress"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-242
  series: series-000
  title: Exact common-core first-order stress at the n17 endpoint
  date: '2026-10-02'
  hypotheses:
  - H-258
  tier: confirmatory
  subject:
    label: The frozen H258 analytic force and torque allocation on the 58 common rows and 52 columns at the
      accepted H255 root box, H256 endpoint and H257 feature inventory.
    engine: devtools.check_n17_core_stress, with an independent review that rebuilt the certificate in
      separately written exact and outward-interval arithmetic
    assurance: verified
    method: exact-algebraic
    host_system: Linux x86_64 remote session container, project Python 3.14.7, sympy 1.14.0, one worker
    selftest_passed: true
    engine_commit: 2fbf8d2933e6a8f51268b87be111a5c03d9f95cf
  instance:
    axis: n
    point: 17
    role: target
  method:
    control: Synthetic controls that run before any input is read, in both runs. Nine mutations must fail
      the identity (tree-edge moment sign, swapped face rows, square-16 angle sign, omitted omega_12 term,
      exceptional-residual sign, force 15/16, normalization, a dropped row, a nonzero 9/11 weight). Load
      and row derivative checks against true partials and against the row builder. Dyadic containment,
      refusal and sign-disposition checks. Twelve tests, ruff and BasedPyright clean.
    candidate: The fixed H258 stress, with the 52 identities proved in QQ[t,b,S,mu,nu,rho] over eleven
      registered monic irreducible denominator factors, and 256-bit outward dyadic sign bounds over the
      H255 box, including a strict-sign guard on every factor the ring proof divides by.
    runs_per_condition: 2
    interleaved: false
    operator: Claude Session 167 coordinator; lane A1 built the instrument and run-001
    entry_point: packing/devtools/check_n17_core_stress.py
    command: 'From packing: .venv/bin/python3 -m devtools.check_n17_core_stress --controls-only, then the
      target command on the exp-237, exp-238 and exp-239 run-001 certificates. Exact lines in run-001 and
      run-002 command.txt.'
    budget: One 300-second single-worker target, 10 MiB per output, then independent review.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-242-n17-core-stress/run-002
    dirty: false
    commit: 2fbf8d2933e6a8f51268b87be111a5c03d9f95cf
  results:
  - shape: determination
    role: outcome
    question: Do all 52 normalized residuals vanish exactly at the H255 root, are all 58 weights nonnegative
      with the prescribed zeros, and are every denominator and normal-force guard strictly positive?
    outcome: criterion_met
    checked_by: Exact ring proof of all 52 columns, formal and fully substituted, with omega_12 and omega_16
      equal to the prescribed plus or minus gamma rho F2 / K terms; six exact zero weights (5-right and
      6-bottom wall pairs, 9/11 face) and 52 strictly positive, smallest 0.0060790 at 11/12 E+; fifteen
      guards and eleven denominator factors strictly signed on the box. The independent review reproduced
      every weight sign, the five oblique capacities and the identity at five rational points, and proved
      it again on a 135 by 11 grid beyond a computed degree bound.
  - shape: determination
    role: guard
    question: Do the frozen controls, provenance, resource limits and review hold?
    outcome: criterion_met
    checked_by: Controls passed before target reads in both runs; run-002 replays run-001 from a clean
      worktree at the engine commit with byte-identical outputs apart from timings; 30.3 s and 30.9 s
      target walls against 300 s; outputs under 46 KB; independent output review finds no blocking defect.
  verdict:
    decision: accepted
    primary_criterion: Exact A-transpose-lambda = K e-side identity at the certified root; weight lower bounds
      at least zero with no tolerance; strictly positive denominator and force guards; synthetic controls;
      independent mathematical, code and output review.
    reason: Every criterion item is met. This is first-order stationarity of the complete local model in both
      corner branches; it is not local minimality, rigidity or global optimality.
    needs_review: false
    commit: 2fbf8d2933e6a8f51268b87be111a5c03d9f95cf
  effort:
    timebox: 300 seconds; one worker
    wall_seconds: 30.3
    stopped_by: criterion
---
# exp-242: n17 Common-Core First-Order Stress

[H258](../../../hypotheses/H-258-n17-common-core-stress.md) fixes one deterministic dual
for both complete n17 first-order branches.
Session 165 stopped its instrument when `sympy.cancel` on 52 fully substituted rational
functions swelled past every time limit.
Session 167 rebuilt the identity proof in a polynomial ring with explicit denominators,
leaving the checked identities and the criterion unchanged.

## Runs

- **run-001.** Lane A1 ran the controls and the target from the session tree before the
  instrument was committed.
  Its SHA-256 `88ffe611…` equals the blob at `2fbf8d29`. The directory also holds the
  reproduction of the old stall, which exited 124 at 90 seconds.
- **run-002.** The coordinator replayed the same commands from a clean worktree at
  `2fbf8d29`. The certificate and controls are identical to run-001 apart from timings.

## Accepted Outcome

The [independent output review](../results/exp-242-n17-core-stress/output-review.md)
read the instrument against the frozen derivations and found no blocking defect.
It rebuilt the certificate in code sharing nothing with the producer; that code is
retained in [`audit/`](../results/exp-242-n17-core-stress/audit/). It recorded four
non-blocking notes:

- The exact-zero offsets of the three axis faces hold by construction of the layout
  rather than by a named check.
- `minimum_capacity_lower_bound` reads zero because it includes the zero-force 9/11
  face. The five oblique capacities’ minimum is $0.0098987$ (11→12).
- The receipt’s $\tau_{5,7}$ interval of $\pm2\times10^{-22}$ is a subtraction artefact.
  At the certified point square 5 is at the wall, so $\tau_{5,7}=0$ and $k=1/2$ exactly.
- The hypothesis record needed its readiness flag updated, which this session did.

The review also found that the criterion names an independent review, not a second
program, so the unfinished `audit_n17_core_stress.py` is not required.

The stress is nonnegative with the six prescribed zeros, so no negative-side first-order
direction exists in either corner branch.
[H-261](../../../hypotheses/H-261-n17-local-minimum-modulo-sliders.md), the local
minimum modulo the slider cone, takes this as its process prerequisite.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
