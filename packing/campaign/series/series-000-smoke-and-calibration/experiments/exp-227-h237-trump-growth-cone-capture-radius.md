---
title: exp-227 — the growth-cone capture radius around Trump's n11 packing
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-227
  series: series-000
  title: The growth-cone capture radius around Trump's n11 packing
  date: '2026-09-23'
  hypotheses: [H-237]
  tier: confirmatory
  subject:
    label: >-
      Exact first-order growth g_b(d) on all 66 faces of the sup-norm sphere for each of
      exp-013's 128 derivative-distinct branches at Trump's labelled anchored pose, and
      the radius the growth route certifies under the BC-199 per-row remainder bounds
    engine: >-
      packing/cases/trump11/capture_radius.py: float LPs propose, exact far-normalised
      duals certify lower bounds, exact vertices pin minima; the BC-199 weighted
      modulus recomputed on the same faces as the control
    assurance: verified
    method: exact-algebraic
    host_system: macOS, Claude Session 156 lane; project Python 3.14.7
  instance: {axis: n, point: 11, role: target}
  method:
    control: >-
      The same code with the far-row normalisation replaced by weights 2/K_j reproduces
      BC-199's branch-0 weighted modulus to all 32 retained digits and both modulus
      classes on all 128 branches
    candidate: >-
      The growth-route radius. Confirm H-237 only with an explicit rational radius above
      rho = 808514697/200000000000, every inequality exact; reject as a bounded negative
      when the route's best certified radius is at most rho, naming the binding
      constant.
    runs_per_condition: 1
    interleaved: false
    operator: Claude Session 156, Fable extra-high lane
    entry_point: packing/cases/trump11/capture_radius.py
    command: >-
      cd packing && uv run --frozen --all-extras --group dev python -m
      cases.trump11.capture_radius --record
      campaign/series/series-000-smoke-and-calibration/results/agenda-042/exp-227-h237-growth-cone-and-route-radius.json
    budget: About four hours of derivation and exact LPs; the full record took 446 s.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-042/
  effort:
    timebox: Four hours
    wall_seconds: 446
    stopped_by: criterion
  results:
  - shape: determination
    role: outcome
    question: >-
      Does the growth-cone route certify side at least U on a sup-norm ball of radius
      greater than rho around Trump's pose?
    outcome: criterion_missed
    checked_by: >-
      An exhaustion lemma in the module docstring: under per-row remainder bounds
      |R_j| <= (K_j/2) t^2 a branch system is solvable at scale t exactly when
      t >= max_j -(2/K_j) a_j.d, so every such certificate is capped by the BC-199
      weighted modulus. The record checks the lemma's consequence on all 8,448 faces
      (route radius at most the modulus on every one); the least route radius is
      0.00402872 on branch 8, and on the binding face theta_10 = -1 of branch 0 the
      growth certificate equals the modulus exactly
  - shape: determination
    role: mechanism
    question: What is the exact minimum of the first-order growth over the whole direction sphere?
    outcome: criterion_met
    checked_by: >-
      Exact vertices pinned on every branch: g_min = 0.0517714532056682325..., attained
      on face theta_10 = -1 by 64 branches, the other 64 at 0.07443; all 66 faces
      positive on every branch, with 13 to 14 faces per branch first-order infeasible
      and certified by exact Farkas vectors
  verdict:
    decision: exhausted
    primary_criterion: >-
      An explicit rational radius above rho from the growth route with exact
      constants; at most rho is a bounded negative.
    reason: >-
      The route cannot exceed the BC-199 modulus by a proved lemma, and the exact
      computation confirms that on every face, so re-running under the per-row
      remainder model adds nothing. The binding constant is that model, not the growth
      minimum, which is 4.5 times kappa. Along the binding direction 36 of 42 rows do
      not recover at second order (exp-227 curvature record), so only a second-order
      exact isolation theorem, a named change of instrument, should reopen the radius.
    reopen_when: >-
      A second-order-exact isolation model: exact row Hessians with a certified cubic
      remainder and a face-wise enclosure of the nonconvex directional bound, replacing
      the per-row quadratic remainder model that caps this route.
---
# Exp-227: The Growth-Cone Capture Radius Around Trump’s Packing

[H-237](../../../hypotheses/H-237-n11-trump-angular-capture-radius.md) asked for a ball
around Trump’s packing larger than BC-240’s, from the exact growth of the side along
every direction.
The growth itself is healthy: its exact minimum over the whole sphere is
about $0.0518$ per unit of sup-norm displacement.
The radius is not, and the reason is structural.
Any certificate that bounds each row’s second-order remainder separately is capped by
BC-199’s weighted modulus, which is where $\rho$ came from, so this route can equal
$\rho$ and never beat it.

The useful by-product is the curvature record
([`exp-227-h237-directional-curvature-b0-4.json`](../results/agenda-042/exp-227-h237-directional-curvature-b0-4.json)):
along the binding direction most rows keep decreasing at second order, so the uniform
remainder model, not the geometry, is what stops at $0.004$. A second-order-exact
isolation theorem is the follow-up, as a W7 improvement of the radius tool.
X-046’s growth floor of $0.0057$ per radian also used a far-row constant; the corrected
uniform-ball floor is $\sigma\ge0.0111\,t$. A larger radius was always going to shorten
the H-112 ladder modestly, by about three refinement levels on each side of Trump’s box,
not tenfold.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
