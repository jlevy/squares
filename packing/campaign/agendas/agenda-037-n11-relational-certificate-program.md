---
title: agenda-037 — n11 relational-certificate program
softschema:
  contract: packing.squares:ExperimentAgenda/v1
  schema: ../schemas/agenda.schema.yaml
  envelope: agenda
  status: enforced
agenda:
  id: agenda-037
  title: N11 Relational-Certificate Program
  updated: '2026-09-18'
  status: active
  objective: >-
    Pursue n=11 results beyond the one-body ceiling L* = 38200/9977 through certificates
    that price relations between squares, starting from the overnight route slate in
    X-037. Calibrate the certificate machinery at the solved cases n=6 and n=10 under
    H-216, keep Route F1 / H-217 blocked until the new reader, sites-1 checkpoint,
    and convergence tool exist, and leave M2, M4, M5, M6, and M8 retired.
  items:
  - id: BC-356
    purpose: research
    owner_focus: insight
    instances: [6, 10, 11]
    state: complete
    priority: 0
    question: >-
      Which mechanisms could give a significant n=11 result beyond the one-body ceiling,
      how do they survive an independent adversarial review, and what do the cheapest
      decisive measurements say overnight?
    budget: >-
      One overnight program on 2026-09-17: four read-only review lanes, a Fable max
      ideation pass, an independent Fable max adversarial review, and two execution
      lanes (M1 and M7) of about 105 minutes, with no hypothesis registration and no
      bound claim.
    entry: >-
      BC-347’s route audit and BC-343’s Route S admission are on main at 035d84c6, the
      2026-09-14 owner holds stand, and the owner asked for a creative, significant n=11
      route.
    exit: >-
      A durable exploration report ranks the mechanisms, records the adversarial
      verdicts and the overnight measurements at their scope, and names every
      disposition and owner decision.
    bead: think-4woh
    depends_on: [BC-347]
    next_evidence: >-
      The five X-037 decisions are resolved; H-216 and H-217 are registered. BC-357
      closes the n=6 bracket under H-216.
    workflows: [factual-review, insight-iteration, review-planning-oversight]
    program: n11-strategy-reset
    artifacts:
    - packing/campaign/explorations/X-037-n11-overnight-review-and-route-slate.md
    - packing/campaign/agent-sessions/session-138-n11-overnight-review.md
    parallel_group: n11-overnight-review
    outcomes:
    - scope: >-
        The state audit, mechanism scan, machinery inventory, registry table, and the
        ranked M1–M8 slate with independent adversarial verdicts.
      classification: achieved
      result: >-
        X-037 records the four lanes, eight ranked mechanisms, and the adversarial
        verdicts: keep M7, keep M1 with changes as Route F1, keep M3 as a kill test,
        and retire M2, M4, M5, M6, and M8. Lane D’s twelve record inconsistencies are
        listed for later filing and were not fixed.
      evidence:
      - packing/campaign/explorations/X-037-n11-overnight-review-and-route-slate.md
      disposition: retire-success
      follow_up: null
    - scope: >-
        M1 clique and majority atoms at 153/40, B = 9977/10000, 181-direction net, on
        fixed catalogues and by column generation over the pose net.
      classification: inconclusive
      result: >-
        All 44 heavy cliques of the A6 64-family are budget-one threshold atoms (the
        3/2 cliques need 4-of-7). Each fixed support is exhausted below 11 (9, 54/5,
        76/7, 296/27), but column generation rebuilt a mass-11 family after every cut.
        The rows-complete LP could not run, and neither terminal state was reached.
        No covering value and no bound.
      evidence:
      - packing/campaign/explorations/X-037-n11-overnight-review-and-route-slate.md
      disposition: continue
      follow_up: think-gyzw
    - scope: >-
        M7 helper-free point certificates at n=6 (299/100) and n=10 (37/10), B =
        9977/10000, 181-direction net.
      classification: inconclusive
      result: >-
        n=10 at 37/10 is foreclosed exactly by a B-scaled integer ceiling family. The
        n=6 covering value at 299/100 lies in [83/14 exact, 6.006571 float]. The
        two-route gate accepts s(6) ≥ 297/100 and s(10) ≥ 73/20, 92/25, and 737/200,
        all weaker than the proved values. No helper necessity is shown.
      evidence:
      - packing/campaign/explorations/X-037-n11-overnight-review-and-route-slate.md
      disposition: continue
      follow_up: think-qqzs
  - id: BC-357
    purpose: measurement_validation
    owner_focus: correctness
    instances: [6, 10]
    state: in_progress
    priority: 1
    question: >-
      Does a helper-free point-atom certificate exist for n=6 at side 299/100 with
      B = 9977/10000 on the 181-direction net, and how far do point certificates reach
      at n=10 with B in (0.99808, 0.99885]?
    hypotheses: [H-216]
    budget: >-
      One block of two to three hours on the stock drivers: freeze and polish at 299/100,
      then either an exact ceiling family of total at least 6 or a rows-complete covering
      below 6 decided by both gate routes. An n-parameterised threshold producer (about
      2–3 h) follows for the threshold language at n=6 and is not H-216's instrument.
    entry: >-
      BC-356 is complete. H-216 is registered. G1, G2, G3, and G5 are on main.
    exit: >-
      Either a frozen point-atom covering below 6 on a named site set that both
      decide_certificate routes accept, which confirms H-216, or an exact depth-one
      family of total at least 6 that both ceiling readers accept, which refutes it.
      Or a recorded stall with its exact bracket and tooling receipts.
    bead: think-qqzs
    depends_on: [BC-356]
    next_evidence: >-
      Session 139 froze covering total 76027/12500 = 6.08216 (does not confirm) and
      polished a depth-one family of exact total 76/13 that both
      independent_ceiling_reader and verify_ceiling accept as depth <= 1 and reject
      on K3 (does not kill). A second named site set on grids 18/24/29/34 froze
      covering 151931/25000 = 6.07724 (does not confirm). H-216 stays open. Confirm
      still needs covering < 6 on a named site set that both decide_certificate
      routes accept. Not an n=11 result. Exit the chase at 08:33Z.
    workflows: [pipeline-improvement, research-loop]
    program: n11-strategy-reset
    artifacts:
    - packing/campaign/explorations/X-037-n11-overnight-review-and-route-slate.md
    - packing/campaign/hypotheses/H-216-point-certificate-at-n6-299-100.md
    - packing/campaign/agent-sessions/session-139-n11-overnight-research.md
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-037/h216-n6-299-100-covering.json
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-037/h216-n6-299-100-family.json
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-037/h216-n6-299-100-run.json
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-037/h216-n6-299-100-family-polished.json
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-037/h216-n6-299-100-independent.json
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-037/h216-n6-299-100-verify-ceiling.json
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-037/h216-n6-299-100-receipt.md
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-037/h216-n6-299-100-sites2-covering.json
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-037/h216-n6-299-100-sites2-receipt.md
    parallel_group: solved-case-calibration
    note: >-
      Calibration only, under H-216. Certificates at n=6 and n=10 are weaker than the
      proved values and are not new results; the question is whether helpers are
      necessary at a solved case.
  - id: BC-358
    purpose: research
    owner_focus: insight
    instances: [11]
    state: blocked
    priority: 1
    question: >-
      Is the rows-complete covering LP with weighted-majority, k-of-S, and floor atoms
      on arrangement-vertex sites below 11 at 153/40 (B = 9977/10000, 181-direction
      net)?
    hypotheses: [H-217]
    budget: >-
      Tooling first (checkpointed column generation with an independent reader, about a
      day), then a convergence run of several checkpointed hours.
    entry: >-
      X-037 admits the atom classes. The sites-1 checkpoint is retained or regenerated
      under think-3xbr, the column-generation loop is a guarded tool under think-gyzw,
      and think-g3j7 lands a new reader for those classes without mutating T-025 or
      T-026.
    exit: >-
      Either a depth-one mass-11 family feasible for every admitted majority, k-of-S,
      and floor atom on its own vertices, which kills the route at this scope, or a
      frozen certificate of total budget strictly below 11 and least charge at least 1
      that both routes of decide_threshold_certificate, or of the think-g3j7 successor,
      accept.
    bead: think-gyzw
    depends_on: []
    blocked_on: >-
      think-g3j7 must land a new reader for weighted-majority and floor atoms without
      mutating T-025/T-026 verify_claim.py. Also the unretained sites-1 checkpoint
      (think-3xbr) and the missing convergence tool (think-gyzw).
    next_evidence: >-
      Session 139 landed packing/src/sqpack/fractional/relational.py and
      packing/devtools/decide_relational_certificate.py without mutating T-025/T-026
      verify_claim.py. Remaining: retain or regenerate the sites-1 checkpoint
      (think-3xbr), then the guarded colgen tool (think-gyzw). Do not close
      think-g3j7 or think-gyzw.
    workflows: [pipeline-improvement, research-loop]
    program: n11-strategy-reset
    artifacts:
    - packing/campaign/explorations/X-037-n11-overnight-review-and-route-slate.md
    parallel_group: route-f1-relational-atoms
    note: >-
      This is Route F1 from the BC-347 audit, widened by the overnight adversarial
      review and registered as H-217.
  - id: BC-359
    purpose: research
    owner_focus: insight
    instances: [11]
    state: tentative
    priority: 2
    question: >-
      Is the integral piercing number of the T-018 site set at side 3.80 on a
      37-direction net at most 11, as a Memo II-style exact-ownership proof would need?
    budget: >-
      About a day: a set-cover integer program over event cells, then certification of
      any 11-point winner with cases/green17/interval_audit.py.
    entry: >-
      A planning block selects it over BC-357 and BC-358. No owner decision is needed
      for the kill test itself.
    exit: >-
      A certified piercing number of 12 or more kills M3. An exactly certified
      11-point set opens a hand-proof project that needs its own planning.
    bead: think-k4vb
    depends_on: [BC-356]
    next_evidence: >-
      The integer program’s optimum on the coarse net, with the winner decided exactly
      at full angle.
    workflows: [research-loop]
    program: n11-strategy-reset
    artifacts:
    - packing/campaign/explorations/X-037-n11-overnight-review-and-route-slate.md
    parallel_group: m3-kill-test
    note: >-
      An 11-point set cannot be D4-symmetric, so no existing D4 producer can look for
      one; the continuous-angle verifier exists.
  - id: BC-360
    purpose: research
    owner_focus: insight
    instances: [11]
    state: stopped
    priority: 4
    question: >-
      Should mechanisms M2, M4, M5, M6, and M8 from the overnight slate run as lanes?
    budget: >-
      None. Retired by the independent adversarial review in BC-356 without a
      measurement.
    entry: >-
      The adversarial review of M1–M8 is complete.
    exit: >-
      Each retired mechanism has a recorded reason and a reopening condition.
    bead: think-4woh
    depends_on: [BC-356]
    next_evidence: >-
      None; reopen a mechanism only when its stated reopening condition holds.
    workflows: [review-planning-oversight]
    program: n11-strategy-reset
    artifacts:
    - packing/campaign/explorations/X-037-n11-overnight-review-and-route-slate.md
    parallel_group: retired-overnight-mechanisms
    outcomes:
    - scope: >-
        M2, the trace-conflict graph with Lovász theta or the exact independence number,
        as a lane for this program.
      classification: bounded-negative
      result: >-
        Retired for feasibility. Theta needs an SDP solver and an exact PSD certificate
        (15–27 h), and alpha on the retained supports is trivially 10 or 9. It survives
        as a record note: M1, M8, and M2 relax one integer set-packing object. Resolved
        2026-09-18: SDP is not admitted; theta without exact PSD is at most V1 and
        cannot support a bound. Reopen only with an exact PSD route that can reach C3.
      evidence:
      - packing/campaign/explorations/X-037-n11-overnight-review-and-route-slate.md
      disposition: retire-negative
      follow_up: null
    - scope: M4, a slot-cover hand proof from a few named clique slots, at side 3.82.
      classification: bounded-negative
      result: >-
        Retired at 3.82. The fractional bound in a sub-language is already 10.967, and a
        hand-sized point cover is dead above 3.789. It could return only as exposition
        at 3.80 behind a catalogue LP.
      evidence:
      - packing/campaign/explorations/X-037-n11-overnight-review-and-route-slate.md
      disposition: retire-negative
      follow_up: null
    - scope: M5, weighted Bentz moving covers for closing Route A’s roots continuously.
      classification: bounded-negative
      result: >-
        Retired as a category error. Bentz moves the cover for a fixed packing, while
        Route A’s anchor parameter is a property of the packing, so no ownership path
        crosses it. The weighted lemma could be a note in X-027.
      evidence:
      - packing/campaign/explorations/X-037-n11-overnight-review-and-route-slate.md
      disposition: retire-negative
      follow_up: null
    - scope: M6, LP-relaxation rounding as an n=11 proof route.
      classification: bounded-negative
      result: >-
        Retired as a proof route; its ν*(U) diagnostic is ill-posed as stated. Resolved
        2026-09-18: no Route D search hypothesis. Reopen only with a criterion that can
        be wrong, Trump’s packing as the exact control, and an instrument, named before
        a run.
      evidence:
      - packing/campaign/explorations/X-037-n11-overnight-review-and-route-slate.md
      disposition: retire-negative
      follow_up: null
    - scope: M8, odd-cycle rank-two ring atoms, for this program block.
      classification: bounded-negative
      result: >-
        Retired for this block. A rank-two ring needs a geometric conflict certificate
        without common points, the same missing piece as M1’s kernel cliques. Revisit
        only after that certificate exists.
      evidence:
      - packing/campaign/explorations/X-037-n11-overnight-review-and-route-slate.md
      disposition: retire-negative
      follow_up: null
---
# N11 Relational-Certificate Program

This agenda carries the queue that came out of the 2026-09-17 overnight review
([X-037](../explorations/X-037-n11-overnight-review-and-route-slate.md),
[session-138](../agent-sessions/session-138-n11-overnight-review.md)). The overnight
program moved no bound.
The 2026-09-18 addition to X-037 resolves the five owner decisions and registers
[H-216](../hypotheses/H-216-point-certificate-at-n6-299-100.md) and
[H-217](../hypotheses/H-217-route-f1-majority-floor-at-153-40.md).

## Relation to Agenda-036

[agenda-036](agenda-036-n11-strategy-reset-roadmap.md) stays the controller for the
strategy reset. This agenda continues BC-347’s route audit with a new mechanism slate,
and its cells share agenda-036’s `n11-strategy-reset` program.
BC-343, Route S under `think-ufmk`, remains open there; session 139 registered `exp-161`
and has not run a target.
BC-358 is Route F1 from BC-347’s audit, widened by tonight’s adversarial review.
Agenda-036 was not edited, because an open pull request also edits it.

## Queue

- **BC-356 (complete).** The overnight review, the adversarial verdicts, and the M1 and
  M7 measurements at their stated scope.
  The five owner decisions are resolved in X-037.
- **BC-357 (in progress).** M7 calibration under `think-qqzs` / H-216: close the n=6
  bracket at 299/100. G1, G2, G3, and G5 are on main.
  G4 remains on this bead and is not H-216’s instrument.
- **BC-358 (blocked).** Route F1 / H-217 at 153/40. The language is admitted.
  The cell waits on the `think-g3j7` reader, the `sites-1` checkpoint (`think-3xbr`),
  and a guarded convergence tool (`think-gyzw`).
- **BC-359 (tentative).** The M3 kill test under `think-k4vb`.
- **BC-360 (stopped).** M2, M4, M5, M6, and M8, retired with reasons.
  SDP is not admitted.
  No Route D search hypothesis.

`exp-161` is registered for Route S in agenda-036 and has not run a target.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
