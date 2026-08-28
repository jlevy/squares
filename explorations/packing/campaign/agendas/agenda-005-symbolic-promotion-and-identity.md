---
title: agenda-005 — build the missing middle, and decide what the map counts
softschema:
  contract: packing.squares:ExperimentAgenda/v1
  schema: ../schemas/agenda.schema.yaml
  envelope: agenda
  status: enforced
agenda:
  id: agenda-005
  title: Build the missing middle of the promotion pipeline, and decide what the map counts
  updated: '2026-08-28'
  status: active
  objective: >-
    Three programs, run as one agenda because they compete for the same clock and must not
    be confused with each other. The first builds the unbuilt middle of the symbolic
    promotion route so an exact entry can be derived rather than inherited. The second
    removes the numeric floor that keeps that route usable only on someone else's
    high-precision data. The third resolves what the atlas counts, because a census over
    endpoint keys cannot saturate. None unblocks another.
  items:
  - id: BC-042
    purpose: tool_validation
    owner_focus: correctness
    instances: [11, 29]
    state: ready
    priority: 0
    question: >-
      Can the already-measured n = 29 contact structure be frozen as a durable artifact,
      and can the same extraction reproduce the known n = 11 structure?
    hypotheses: []
    budget: one W7 pipeline-improvement slice of at most 60 minutes
    entry: >-
      a numerical pose with a declared precision and tolerance, and the n = 11 contact
      structure available from the literature as a known answer
    exit: >-
      A retained contact-structure artifact for n = 29 carrying its 89 incidences and the
      measured separation, plus the same extraction reproducing the n = 11 structure as a
      known answer. Any incidence the extraction cannot decide is a typed refusal.
    bead: think-zmh8
    depends_on: []
    workflows: [pipeline-improvement]
    next_evidence: >-
      Corrected by measurement in X-004. This was first scoped as inference under an
      ambiguity risk, which misapplied D-021's 1e-11 float-LP floor to a source that is
      not that solver's output. The retained reconstruction already separates contact from
      non-contact by about ninety-nine orders of magnitude: the worst touching margin is
      -4.05e-101 against a smallest strict separation of 3.617e-02, over 406 pairs. The
      work is to freeze what is measured, not to infer what is uncertain.
    note: >-
      Built under [plan-2026-08-28-promotion-pipeline-implementation](../../docs/project/specs/active/plan-2026-08-28-promotion-pipeline-implementation.md),
      phase 1, contact extraction.
      The n = 11 reproduction stays in scope as a known-answer check on the extraction
      itself, not because n = 29 is uncertain. Generic inference from an arbitrary
      quench endpoint, where the D-021 floor does apply, is a separate and later question.
  - id: BC-043
    purpose: tool_validation
    owner_focus: correctness
    instances: [11, 29]
    state: blocked
    priority: 1
    question: >-
      Can the contact equations be assembled from an accepted structure, reduced to
      eliminate the centres, and closed by determinant conditions rather than left
      underdetermined?
    hypotheses: []
    budget: one or two W7 pipeline-improvement slices of at most 60 minutes each
    entry: >-
      a contact structure accepted under BC-042, with its ambiguity report empty or its
      residual ambiguities explicitly bounded
    exit: >-
      A reduced system in s and the distinct non-axis-aligned angles, closed by
      Jacobian-determinant conditions, reproducing the known n = 11 system; or a typed
      statement of which reduction the particular contact graph does not admit.
    bead: think-va53
    depends_on: [BC-042]
    workflows: [pipeline-improvement]
    next_evidence: >-
      The unreduced system still contains the centres. For several published rigid
      constructions the contact graph lets one eliminate them and leave two unknowns at
      n = 11 and three at n = 17, but that reduction must be derived from the particular
      graph and an angle-class count alone does not perform it. Closure uses
      Lagrange or Fritz-John conditions in determinant form, which is what keeps the
      problem root-finding rather than minimization.
    note: >-
      Built under [plan-2026-08-28-promotion-pipeline-implementation](../../docs/project/specs/active/plan-2026-08-28-promotion-pipeline-implementation.md),
      phase 2, system assembly and closure. That spec carries the module layout, data shapes, API surfaces and
      per-phase negative controls an implementing agent needs.
  - id: BC-047
    purpose: tool_validation
    owner_focus: correctness
    instances: [11, 29]
    state: blocked
    priority: 0
    question: >-
      Can the closed contact system be Newton-refined to a precision at which integer
      relation has real margin, with the residual reported rather than assumed?
    hypotheses: []
    budget: one W7 pipeline-improvement slice of at most 60 minutes
    entry: a closed contact system from BC-043, and the serialized pose as a seed
    exit: >-
      A refined solution at a declared precision, 1000 digits or more, with a reported
      residual bound; or a typed statement of which conditioning prevents it. No algebraic
      claim is made at this step, only precision.
    bead: think-y85e
    depends_on: [BC-043]
    workflows: [pipeline-improvement]
    next_evidence: >-
      A probe recorded in X-004 shows this step is not optional. Integer relation run
      directly on the serialized value returns relations at almost every degree from eight
      to twenty-one, and the degree-eight candidate has a relative residual of order 1e-90
      against roughly a hundred available digits, having consumed almost exactly the
      ninety digits the search was allowed. Ninety-eight digits cannot identify the
      minimal polynomial, so precision must be manufactured from the system rather than
      read from the source. At n = 29 that system is published in the provenance SVG and
      already transcribed in cases/kingbird29/verify_svg.py, where it is evaluated but
      never solved, so this commitment drives an existing transcription rather than
      waiting on BC-042 and BC-043.
    note: >-
      Built under [plan-2026-08-28-promotion-pipeline-implementation](../../docs/project/specs/active/plan-2026-08-28-promotion-pipeline-implementation.md),
      phase 3, high-precision refinement.
      This commitment exists because the first draft of this agenda omitted it and went
      straight from assembly to solving. The omission was caught by a two-minute probe
      rather than by review, which is the cheapest possible place to find it.
  - id: BC-044
    purpose: tool_validation
    owner_focus: correctness
    instances: [11]
    state: blocked
    priority: 1
    question: >-
      Can the closed system be solved exactly, by elimination or by integer relation, and
      can the result be discharged rather than trusted?
    hypotheses: []
    budget: one W7 pipeline-improvement slice of at most 90 minutes
    entry: a refined solution from BC-047 at a precision that gives integer relation real margin
    exit: >-
      A closed round trip at n = 11: the published minimal polynomial recovered
      independently, substituted back exactly, the packing re-verified, and the
      reconstructed side compared against the input pose. Or a typed statement of which
      route failed and at which step.
    bead: think-3lro
    depends_on: [BC-047]
    workflows: [pipeline-improvement]
    next_evidence: >-
      No Gröbner, resultant, PSLQ or LLL code exists in the tree. Both routes produce
      guesses, and the round trip discharges them differently. A wrong minimal polynomial
      is caught by exact back-substitution, because it will not satisfy the system. A
      wrong contact structure is caught by re-verifying the reconstructed packing, but
      only partly: verification catches infeasibility and not a structure that yields a
      valid yet suboptimal packing. That failure appears as a reconstructed side above the
      input pose, so the comparison must be against the input side and not merely against
      validity.
    note: >-
      Built under [plan-2026-08-28-promotion-pipeline-implementation](../../docs/project/specs/active/plan-2026-08-28-promotion-pipeline-implementation.md),
      phase 4, exact solve and round trip.
      The reverse direction is already built and sound, which is the reason to attempt the
      forward one. `sqpack.field` proves irreducibility and isolates the real root, and
      `sqpack.verify` checks separating-axis validity with exact predicates. The unbuilt
      half would be constructed against a back end that can catch it being wrong.
      Elimination is the scaling risk: n = 11 reduces to two unknowns and n = 17 to three,
      while n = 29 has six orientation classes of which one is the axis class, leaving five
      tilted angles and six unknowns. The source's own solve is a six-by-six system, so this
      is measured rather than estimated. A route that works at two or three unknowns may
      still not terminate at six, which is why the integer-relation route is a parallel
      candidate rather than a fallback.
  - id: BC-045
    purpose: tool_validation
    owner_focus: correctness
    instances: [11]
    state: ready
    priority: 1
    question: >-
      Can an interval checker discharge existence and uniqueness for a root of a declared
      contact system, calibrated where the answer is already known?
    hypotheses: []
    budget: one W7 pipeline-improvement slice of at most 90 minutes
    entry: >-
      the n = 11 contact system is available from the literature, so the checker can be
      calibrated against a root that is already certified by other means
    exit: >-
      An outward-rounded interval certificate for the n = 11 root that agrees with the
      existing exact witness, or a typed statement of which conditioning or singularity
      prevents it.
    bead: think-75ll
    depends_on: []
    workflows: [pipeline-improvement]
    next_evidence: >-
      The `PoseBox` scalar and the interval branch-and-bound hook are recorded as unbuilt
      on the proof lane, and `packing-witness promote --strategy interval-existence`
      raises `_interval_not_built()`. This is the missing half of step six, and it is
      independent of BC-042 through BC-044 because the n = 11 system does not need to be
      inferred to be certified.
    note: >-
      Deliberately scoped to n = 11 only. Certified numerics discharge a root of a system
      someone supplies; they do not identify a contact structure or recover a number
      field. Pointing this at n = 29 before BC-042 and BC-043 exist would be certifying a
      system nobody has written down.
  - id: BC-048
    purpose: tool_validation
    owner_focus: correctness
    instances: [5, 11]
    state: ready
    priority: 1
    question: >-
      Can an exact LP over certified rational or algebraic coefficients replace the float
      solver where a certified answer is required, removing the 1e-11 floor?
    hypotheses: []
    budget: two W7 pipeline-improvement slices of at most 60 minutes each
    entry: >-
      the existing float LP and its independent second formulation are available as a
      known-answer pair, agreeing to 4.4e-16 on Trump's cell
    exit: >-
      An exact LP agreeing with the float path on the cells where both are valid, and a
      demonstration that a pose quenched through the exact path carries an unambiguous
      contact structure; or a typed statement of which cells need algebraic rather than
      rational coefficients.
    bead: think-nfsd
    depends_on: []
    workflows: [pipeline-improvement]
    next_evidence: >-
      D-021 names this directly: the float LP solver has a noise floor of about 1e-11 in
      the side, no numerical comparison may claim a difference finer than that floor, and
      the general fix is an exact LP over certified rational or algebraic coefficients,
      which is unbuilt. It is purely rational only for rational-coefficient cells.
    note: >-
      Built under [plan-2026-08-28-promotion-pipeline-implementation](../../docs/project/specs/active/plan-2026-08-28-promotion-pipeline-implementation.md),
      phase 5, exact LP.
      This does not gate the n = 29 result, which consumes a published pose and needs no LP
      of ours. It gates generality. On a source carrying ninety-nine digits the contact
      structure is unambiguous; on a pose this project quenches, the 1e-11 floor is exactly
      the ambiguity that makes step two a guess. Without this the symbolic chain only ever
      consumes someone else's data.
  - id: BC-046
    purpose: measurement_validation
    owner_focus: correctness
    instances: [3, 4, 5]
    state: ready
    priority: 0
    question: >-
      What relation should the atlas count, given that a connected optimal set produces
      many endpoint keys and the current store splits it?
    hypotheses: [H-032]
    budget: one W3 insight-iteration slice of at most 60 minutes, then one W6 round only if a criterion is frozen
    entry: >-
      the exact n = 3 and n = 4 quotient models are available as known answers, and the
      n = 5 face, sheet, obstruction and polytope results are retained
    exit: >-
      A declared identity relation with a criterion that the exact n = 3 sliding family
      and the exact n = 4 point both satisfy, or a typed statement of which property the
      candidate relation cannot decide.
    bead: think-0yo9
    depends_on: []
    workflows: [insight-iteration, research-loop]
    next_evidence: >-
      `distinct_basins` counts endpoint keys, not connected terminal components. The exact
      n = 3 side-2 optimum contains a sliding family of centres, so one connected set
      produces many keys and the store splits it. Until D-034 is resolved the discovery
      curve cannot plateau, the census cannot saturate, and the rarity premise is
      untestable rather than untested.
    note: >-
      This is the map program and it shares nothing with BC-042 through BC-045 except the
      clock. A resolved identity relation still leaves n = 29 uncertified, and a working
      promoter still leaves the map counting keys.
---
# Agenda-005 — Build the Missing Middle, and Decide What the Map Counts

The reading behind this agenda is in
[plan-2026-08-28](../../docs/project/specs/active/plan-2026-08-28-symbolic-promotion-and-the-atlas.md).
Its short form: the promotion pipeline has a built front end and a built back end with
an unbuilt middle, so every exact entry in the atlas today was derived by hand or
supplied by a publication.

## Two programs, and why they are in one agenda

They are independent and must not be confused, but they compete for the same clock, so
putting them in one queue makes the trade visible rather than accidental.

| Program | Commitments | Buys |
| --- | --- | --- |
| Symbolic promotion | BC-042, BC-043, BC-047, BC-044, BC-045 | An exact entry that can be *derived*, not inherited |
| Numeric floor | BC-048 | The same route, usable on poses this project generates |
| Map identity | BC-046 | A census that can saturate, and a testable rarity premise |

None unblocks another.
The numeric lane is the one that decides whether the symbolic lane generalizes past
published sources, which is why it is in this agenda rather than a later one.

## Two targets, used differently

`n = 11` is the **calibration** and `n = 29` is the **target**, and they are not
alternatives.

At `n = 11` the answer is known from Trump’s 1979 polynomial, so every stage has
something to be caught being wrong against: the extraction must reproduce a known
contact structure, the assembly must reproduce a known system, and the solve must
recover a known minimal polynomial.
That is what makes the chain trustworthy.

At `n = 29` there is no published answer, and the best known construction is a numerical
root-find recorded as `public-certificate-missing`. That is the end-to-end test, and it
is where a derived certificate would be new.

The earlier reason for sequencing — that `n = 29`’s contact structure was uncertain —
was withdrawn on measurement.
It is not uncertain; see X-004.

## Bounded blocks

| Block | Commitments | Checkpoint question |
| --- | --- | --- |
| 1 | BC-042, BC-045 | Is the contact structure frozen, and can a root be certified on a system someone else wrote down? |
| 2 | BC-043 | Can the system be assembled and closed, reproducing the known `n = 11` form? |
| 3 | BC-047 | Can precision be manufactured from the system, past what the source carries? |
| 4 | BC-044 | Does the solve recover `n = 11`’s published polynomial, and does the round trip close? |
| 5 | BC-048 | Can the numeric floor be removed, so our own poses become promotable? |
| 6 | BC-046 | What should the map count? |

Blocks 2, 3 and 4 are a strict chain and the probe in X-004 is why: precision cannot be
read from the source, so it must come from the system, so the system must exist first.
Block 1’s two commitments are independent of that chain and of each other.
Block 5 is independent of everything and may run whenever the symbolic lane stalls.

### Replan triggers

- **Any block.** A typed refusal is a valid ending.
  An inference that cannot decide an incidence, or a checker defeated by conditioning,
  is a result — not a failure to be worked around by loosening a tolerance.
- **BC-042.** If the `n = 11` calibration cannot reproduce the known contact structure,
  stop. Do not proceed to `n = 29` on an inference that fails where the answer is known.
- **BC-044.** An integer relation is not a proof.
  If irreducibility, root isolation, or exact back-substitution cannot be completed, the
  round is `invalid`, not `unresolved`.
- **Two consecutive blocks closing zero commitments** stops the agenda for replanning.

## What this agenda may not claim

- That a promoted pose certifies a reported value, until the claim is discharged: by
  exact substitution into the recovered field, or failing that by interval
  certification.
- That the `4.93e-31` Schadt relaxation is progress toward the `n = 29` record.
  The distance to that record is about `1e26` times larger.
- Atlas saturation, census completeness, or any rarity verdict while `distinct_basins`
  counts endpoint keys.
- A contact model inferred from serialized geometry where near-contacts are ambiguous.
  That must remain an explicit typed failure.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
