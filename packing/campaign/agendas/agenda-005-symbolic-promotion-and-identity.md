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
    state: complete
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
    artifacts:
    - atlas/known-best/contact-structures.json
    - atlas/known-best/contact-structure.schema.yaml
    - src/sqpack/promote/contacts.py
    - tests/test_promote_contacts.py
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
      Closed in session-035. The n = 29 structure is frozen at atlas/known-best/contact-structures.json with 52 pair and 37 wall incidences, 89 in total across six orientation classes, an empty ambiguity report, and 97.5013 decades between the worst contact and the smallest strict separation. The same extractor reproduces Trump's n = 11 structure exactly under exact arithmetic, which was the known-answer check on the extractor itself.
           Built under [plan-2026-08-28-promotion-pipeline-implementation](../../../docs/project/specs/active/plan-2026-08-28-promotion-pipeline-implementation.md),
      phase 1, contact extraction.
      The n = 11 reproduction stays in scope as a known-answer check on the extraction
      itself, not because n = 29 is uncertain. Generic inference from an arbitrary
      quench endpoint, where the D-021 floor does apply, is a separate and later question.
  - id: BC-043
    purpose: tool_validation
    owner_focus: correctness
    instances: [11, 29]
    state: complete
    discharged_by: BC-054
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
      Unblocked by block A. BC-042 delivered a contact structure whose ambiguity report is empty, which is exactly this commitment's entry criterion, so the dependency is discharged rather than merely older.
      Built under [plan-2026-08-28-promotion-pipeline-implementation](../../../docs/project/specs/active/plan-2026-08-28-promotion-pipeline-implementation.md),
      phase 2, system assembly and closure. That spec carries the module layout, data shapes, API surfaces and
      per-phase negative controls an implementing agent needs.
  - id: BC-047
    purpose: tool_validation
    owner_focus: correctness
    instances: [11, 29]
    state: complete
    priority: 0
    question: >-
      Can the closed contact system be Newton-refined to a precision at which integer
      relation has real margin, with the residual reported rather than assumed?
    hypotheses: []
    budget: one W7 pipeline-improvement slice of at most 60 minutes
    entry: >-
      At n = 29, the closed system already transcribed in cases/kingbird29/verify_svg.py,
      with the serialized pose as a seed; no assembly step is required, which is why this
      commitment is ready rather than blocked. At n = 11, a closed system from BC-043.
    exit: >-
      A refined solution at a declared precision, 1000 digits or more, with a reported
      residual bound; or a typed statement of which conditioning prevents it. No algebraic
      claim is made at this step, only precision.
    artifacts:
    - campaign/series/series-000-smoke-and-calibration/results/bc-047-n29-refinement.json
    - src/sqpack/promote/refine.py
    - cases/kingbird29/system.py
    - cases/kingbird29/refine_system.py
    - tests/test_promote_refine.py
    bead: think-y85e
    depends_on: []
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
      Closed in session-035. The transcribed system refines to 1000 declared digits with a reported residual bound of 1.09829e-1039, and the residual tracks the working precision across five rungs rather than plateauing. A finding is recorded rather than worked around: displacing one equation of a square consistent system by a constant does not plateau the residual, so residual_falls is an observation and not a control at this size.
           Built under [plan-2026-08-28-promotion-pipeline-implementation](../../../docs/project/specs/active/plan-2026-08-28-promotion-pipeline-implementation.md),
      phase 3, high-precision refinement.
      This commitment exists because the first draft of this agenda omitted it and went
      straight from assembly to solving. The omission was caught by a two-minute probe
      rather than by review, which is the cheapest possible place to find it.
  - id: BC-044
    purpose: tool_validation
    owner_focus: correctness
    instances: [11]
    state: complete
    discharged_by: BC-060
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
      Unblocked by block A. BC-047 delivered a refinement at 1000 declared digits, which is this commitment's entry criterion. The honest prior stays poor: the X-004 sweep found no integer relation through degree twenty with coefficients below 1e22, and elimination in six unknowns may not terminate. Ready does not mean promising.
      Built under [plan-2026-08-28-promotion-pipeline-implementation](../../../docs/project/specs/active/plan-2026-08-28-promotion-pipeline-implementation.md),
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
    instances: [5, 10, 11, 29]
    state: complete
    discharged_by: BC-053
    priority: 0
    question: >-
      Can an interval checker discharge existence and uniqueness for a root of a declared
      contact system, calibrated where the answer is already known, and then certify the
      reported n = 29 value?
    hypotheses: []
    budget: >-
      two W7 pipeline-improvement blocks of about four hours each, phased as
      plan-2026-08-28-interval-certification describes; no individual slot over 30 minutes
    entry: >-
      the n = 11 contact system is available from the literature, and the n = 29 system
      and layout map are published in the retained SVG and already transcribed in
      cases/kingbird29/verify_svg.py, so both can be certified without an assembler
    exit: >-
      Outward-rounded interval certificates for n = 5, n = 10 and n = 11 that agree with
      the existing exact witnesses, controls proving the operator refuses on two-root and
      no-root boxes, and either an n = 29 certificate recorded unresolved with
      needs_review or a typed statement of which conditioning prevents it.
    bead: think-75ll
    depends_on: []
    workflows: [pipeline-improvement]
    next_evidence: >-
      Built under plan-2026-08-28-interval-certification, all four phases, linked from
      this commitment's note. The witness contract already names this method:
      sqpack.assurance
      lists interval-certified among the methods that may carry verified, and
      sqpack.witness enforces it, but exact_verify raises checker-not-built. The socket
      exists and the checker does not. witness.schema.yaml has no scalar kind for an
      enclosure, which is a deliberate contract change the spec calls out.
    note: >-
      Rescoped on 2026-08-28. The previous note said pointing this at n = 29 would be
      certifying a system nobody has written down. That is false: the retained SVG
      publishes the closed system and the symbolic layout map together, and this
      repository already transcribes both. BC-045 is now the primary route to the
      n = 29 prize rather than an n = 11 exercise, because it needs no minimal polynomial
      and BC-044 may not terminate. Built under
      [plan-2026-08-28-interval-certification](../../../docs/project/specs/active/plan-2026-08-28-interval-certification.md).
  - id: BC-048
    purpose: tool_validation
    owner_focus: correctness
    instances: [5, 11]
    state: complete
    discharged_by: BC-061
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
      Built under [plan-2026-08-28-promotion-pipeline-implementation](../../../docs/project/specs/active/plan-2026-08-28-promotion-pipeline-implementation.md),
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
    state: complete
    discharged_by: BC-080
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
    artifacts:
    - packing/campaign/explorations/X-005-identity-relation-and-its-controls.md
    - packing/devtools/check_identity_relation.py
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
      Scheduled as `BC-080` in
      [agenda-007](agenda-007-twelve-hour-steered-run.md), block 4, on this same bead and
      with this scope unchanged. This cell moves to `blocked` when that block opens, so one
      bead never backs two ready commitments.

      This is the map program and it shares nothing with BC-042 through BC-045 except the
      clock. A resolved identity relation still leaves n = 29 uncertified, and a working
      promoter still leaves the map counting keys.
  - id: BC-049
    purpose: research
    owner_focus: correctness
    instances: [5, 28, 40]
    state: ready
    priority: 1
    question: >-
      Are the packings the catalogue annotates "Rigid." actually rigid, on evidence of our
      own rather than on the catalogue's word? The catalogue annotates four -- n = 5, 11,
      28 and 40 -- and this commitment carries three of them; n = 11 was already settled
      locally-rigid on a first-party certificate before this was scoped, which is why it
      is not in `instances`.
    hypotheses: []
    budget: one W1 research-pass slice of at most 60 minutes on n = 5 alone, then a replan
    entry: >-
      the n = 11 tangent-cone machinery in cases/trump11/tangent_cones.py as a worked
      example, and the retained witnesses for n = 5, 28 and 40
    exit: >-
      Each record's rigidity block moves from undetermined to locally-rigid on a
      first-party certificate with a stated scope, or a feasible motion is exhibited and
      the record becomes not-rigid, which is a finding about the catalogue. A typed
      refusal naming what the machinery could not decide also closes the slice.
    bead: think-xdly
    depends_on: []
    workflows: [research-pass, research-loop]
    next_evidence: >-
      The translation escape screen finds no movable square for exactly n = 5, 11, 28, 40
      and the ten perfect squares -- an independent partition that agrees with the
      catalogue's own four annotations. But the screen is sound in one direction only: a
      hit exhibits a motion and proves not-rigid, while a miss rules out single-square
      translation and nothing else. Rotation and coordinated multi-square motion are
      outside it, so these three records now read undetermined, which is a result rather
      than an absence.

      n = 5 is now settled as far as this machinery reaches, and what remains for n = 28
      and n = 40 is not a rerun of it. The argument needs an exact pose, and both retain
      decimal witnesses.

      That next slice has since been priced, and the price is a source rather than a
      computation. The obvious first step -- extract a contact structure from the decimals,
      which is what a closed system is written against -- was run and calibrated at the two
      sizes whose answers are known, and it reproduces neither. n = 11's structure is exact,
      14 pair and 20 wall contacts at floor 0, and the decimal route decides at no floor at
      all. n = 29's is 52 pair and 37 wall at floor 1e-80, extracted from a 160-digit
      materialisation of a provenance SVG, and the route reports different numbers from the
      99-digit witness. The floors where it appears to decide sit below the retained
      precision, so they are windows on the materialisation's padding.

      Stage one says the same thing from the other end: promote.solve.reach is 0 at the
      retained precision for all four sizes, n = 11 included, whose degree-eight minimal
      polynomial was recovered from four hundred manufactured digits rather than from its
      32-digit witness. The retained decimals are not the input to this route at any size.

      So the first step for n = 28 is a higher-precision source, and it has none: no case
      module, no retained contact structure, and no provenance artifact of the kind n = 29's
      extraction was run against. That is the typed refusal this exit accepts for that size.

      **That refusal was challenged and it stands.** The challenge was worth recording
      because the reasoning behind it was tempting and wrong. A source is not the only
      route to precision -- n = 11's degree-eight polynomial came from four hundred
      *manufactured* digits, not from its 32-digit witness -- so it looked as though
      n = 28 needed only its contact structure, and extraction appeared to supply one:
      32 pair contacts, 40 wall, nothing undecided, 41 decades of separation.

      That measurement was an artifact of over-materialisation. The witness carries 57
      fractional digits in its side; the extraction ran at 200 and read incidences at a
      floor of 1e-80, far below anything the record holds, so what decided at that floor
      was the padding rather than the pose. `price_exact_construction` already sweeps this
      properly, at the witness's own precision plus a margin, and reports 27 pair contacts
      rather than 32.

      The calibration is what settles it, and it is why that tool sweeps at all: at n = 29
      the true structure is known from a 160-digit provenance artifact -- 52 pair and 37
      wall -- and the decimal route reports 17 and 36. A route that reproduces neither
      known answer cannot have its numbers at n = 28 read as structure. So the refusal's
      "no retained contact structure" clause is not a gap waiting to be filled by running
      the extractor harder; it is a statement about what the retained decimals can support.

      What would change this is what the refusal already says: a higher-precision source
      for n = 28. The published minimal polynomial does not substitute for one -- the
      catalogue gives s^6 - 24s^5 + 212s^4 - 812s^3 + 1025s^2 + 882s - 1615, and
      `NumberField` constructs it and proves it irreducible mod 13, but a polynomial for
      the side is not a pose.

      For n = 40 the refusal was wrong, and D-389 records why it was reached. Goebel's
      construction is published and transcribed here -- [Friedman DS7] section 2, the centred
      diagonal block family, 2a^2 + 2a + b^2 squares in side a + 1 + b/sqrt(2), which at
      a = 3, b = 4 is exactly forty squares in 4 + 2 sqrt(2). The retained witness is a
      materialisation of it: all eighty coordinates fit p + q sqrt(2) with half-integer p
      and q, the angles are exactly 0 and 45, and the only error anywhere is one 6.04e-31
      truncation of the side. The promotion route was priced without anyone asking whether
      its destination was already reachable another way.

      cases/gobel40 now builds it exactly, deriving the frame from Goebel's rule rather than
      reading it off the witness, and the exact verifier accepts it: 40 squares, 780 pairs,
      48 corner coordinates exactly on the boundary, 98 pairs at zero gap, agreeing with the
      retained witness to that witness's own truncation.

      The rigidity question at n = 40 is still open, and D-388 is why. X-007's assessor
      cannot consume the pose: 296 of its 608 constraint rows carry both a rational and a
      sqrt 2 part, which no positive scalar rationalizes, and the rational-weight Farkas
      search was answering a different system. It answered "no certificate anywhere", which
      reads as a motion. It now refuses instead. Deciding n = 40 needs a Farkas search whose
      weights live in the ordered field, which is a different instrument.
    note: >-
      n = 5 first: it is proved optimal, its side is 2 + sqrt(2)/2, and its structure is
      the smallest of the three. Promoting reported_upper_bound.catalogue_rigid into the
      rigidity block is not a shortcut to this result, it is D-354, and
      tests/test_frontier_rigidity_assessment.py fails on it.

      n = 5 is done and D-354 was not touched. Exactly, over Q(sqrt 2), at Goebel's exact
      pose rather than the retained witness: the cone of infinitesimal motions is exactly
      one-dimensional -- rotation of the middle square about its own centre, which no
      contact mentions because each corner square's inner corner rests at the midpoint of
      the middle square's edge -- and the other fourteen coordinates are pinned by verified
      Farkas certificates. That one direction is then refused at second order by a verified
      non-negative self-stress, since turning an edge line about the centre it is nearest
      to can only bring it closer to the resting corner.

      The frontier block deliberately keeps property: undetermined. The schema's vocabulary
      is [locally-rigid, semi-rigid, not-rigid, undetermined] and second-order rigidity is
      none of them: no motion has been exhibited, and the step from "no arc with nonzero
      derivative" to local rigidity is cited rather than run. The D-354 guard stays green
      without being edited, which is the outcome to want -- a guard you have to weaken to
      land a result was telling you something.

      Recorded in campaign/explorations/X-007-the-n5-optimum-flexes-once-and-that-once-is-shut.md,
      devtools/assess_n5_rigidity.py, tests/test_n5_rigidity.py, and
      campaign/series/series-000-smoke-and-calibration/results/bc-049-n5-rigidity-certificates.json.
    artifacts:
    - devtools/assess_n5_rigidity.py
    - campaign/series/series-000-smoke-and-calibration/results/bc-049-n5-rigidity-certificates.json
    - campaign/explorations/X-007-the-n5-optimum-flexes-once-and-that-once-is-shut.md
    - devtools/price_exact_construction.py
    - campaign/series/series-000-smoke-and-calibration/results/bc-049-exact-construction-price.json
    - tests/test_exact_construction_price.py
    - cases/gobel40/packing.py
    - cases/gobel40/verify_exact.py
  - id: BC-050
    purpose: measurement_validation
    owner_focus: correctness
    instances: [68, 69]
    state: blocked
    blocked_on: >-
      Witnesses for n = 68 and n = 69 whose squares are unit squares to the residual the
      screens require. The retained ones are not, and the upstream construction the
      records cite has not been re-run. No commitment owns producing them, so this waits
      on an artifact rather than on a predecessor.
    priority: 2
    question: >-
      Can n = 68 and n = 69 be given witnesses precise enough to carry a contact claim, so
      the two records excluded from every contact-based screen rejoin the corpus?
    hypotheses: []
    budget: one W7 pipeline-improvement slice of at most 45 minutes to scope the source, before any run
    entry: >-
      the current witnesses and their measured shape residuals, and whichever upstream
      construction the records cite
    exit: >-
      Witnesses whose squares are unit squares to the residual the screens require, or a
      typed statement that the available source cannot supply one, recorded against the
      exclusion rather than left as a silent gap.
    bead: think-ecqk
    depends_on: []
    workflows: [pipeline-improvement]
    next_evidence: >-
      Shape residuals of 1.9e-8 and 1.5e-8 against 5.1e-50 or better everywhere else. Both
      records are excluded from the translation escape screen by measurement, so their
      rigidity blocks read undetermined for a reason that is about our witness rather than
      about the packing. Every future contact-based screen inherits the same exclusion.
    note: >-
      Blocked on nothing technical; it is blocked on deciding whether a better source
      exists before spending a slice regenerating one. Scope the source first.
  - id: BC-051
    purpose: tool_validation
    owner_focus: efficiency
    instances: [5, 11, 29]
    state: stopped
    discharged_by: BC-084
    priority: 0
    question: >-
      Can verification run only the steps a change can reach, without any chance of
      running fewer than it should?
    hypotheses: []
    budget: one W5 efficiency-loop slice of at most 60 minutes, against a measured baseline
    entry: >-
      D-355's measurement, and `packing-validate --only`, which already selects steps by
      name but has nothing mapping a change to the names it should select
    exit: >-
      A change-scoped selector that is conservative by construction -- an unrecognized
      path selects the full gate rather than an empty set -- with a negative control
      proving it cannot silently under-select, and a check that every step is reachable
      from at least one declared path pattern. Or a typed statement of which steps cannot
      be attributed to sources, which is itself the useful answer.
    bead: think-ej1d
    depends_on: []
    workflows: [efficiency-loop]
    next_evidence: >-
      Measured on 2026-08-28: a two-file edit to the rigidity assessor was verified with a
      979.79s full gate, while the two steps that edit can affect run together in 12.06s.
      That is 82x. Across one session the full gate ran six times to completion and was
      killed twice, and the last run's only finding was a single broken behavioural test.
    note: >-
      The commitment is n-agnostic; the instances name the calibration sizes whose coverage
      the selector must be shown to preserve.
      This is the efficiency principle applied to the tooling that enforces the others.
      Coverage and cycle time are a real tension and the design's job is to deliver both:
      the standing asymmetry lets efficiency simplify process but never weaken the
      assurance a claim requires, so selecting fewer steps is only admissible when the
      unselected ones provably cannot fail on this change. That is why the selector must
      be catchable under-selecting; a fast checker nobody can catch being wrong is the one
      outcome worse than a slow one. The full gate keeps its role at commit and merge
      boundaries. This changes the edit loop, not the contract.
    artifacts: []
---
# Agenda-005 — Build the Missing Middle, and Decide What the Map Counts

The reading behind this agenda is in
[plan-2026-08-28](../../../docs/project/specs/active/plan-2026-08-28-symbolic-promotion-and-the-atlas.md).
Its short form: the promotion pipeline has a built front end and a built back end with
an unbuilt middle, so every exact entry in the atlas today was derived by hand or
supplied by a publication.

## Four programs, and why they are in one agenda

They are independent and must not be confused, but they compete for the same clock, so
putting them in one queue makes the trade visible rather than accidental.

| Program | Commitments | Buys |
| --- | --- | --- |
| Symbolic promotion | BC-042, BC-043, BC-047, BC-044, BC-045 | An exact entry that can be *derived*, not inherited |
| Numeric floor | BC-048 | The same route, usable on poses this project generates |
| Map identity | BC-046 | A census that can saturate, and a testable rarity premise |
| Rigidity closure | BC-049, BC-050 | The last five records that say `undetermined` saying something |

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

Replanned on 2026-08-28 after the second correction in
[X-004](../explorations/X-004-n29-exact-promotion.md).
The previous ordering rested on a chain that does not hold at `n = 29`: it assumed
precision had to come from a system this project assembles, so assembly had to come
first. The source publishes the system, and it publishes the layout map with it, so at
this size neither assembly step gates anything.

| Block | Commitments | Checkpoint question | State |
| --- | --- | --- | --- |
| A | BC-047, BC-042 | Can precision be manufactured on demand in-repository, and is the contact structure frozen at `n = 11` and `n = 29`? | **Closed** in [session 035](../agent-sessions/session-035-agenda005-block-a.md). Yes to both. |
| B | BC-045 phases 1–2 | Does the operator prove *uniqueness* on a known root, and refuse on the two-root and no-root controls? | Next |
| C | BC-045 phases 3–4 | Does the interval verdict agree with the exact route where both apply, and what does `n = 29` return? | After B |

Block A answered its checkpoint question in the affirmative on both lanes.
Precision is manufactured rather than inherited — 1000 declared digits at a reported
residual bound of `1.09829e-1039`, with the residual tracking working precision across
five rungs — and the `n = 29` contact structure is frozen with 89 incidences at
`97.5013` decades of separation, calibrated against the known `n = 11` answer.
Neither result gates block B; they remove the two reasons it might have had to wait.

The ordering is now driven by which route can actually reach the prize.
Certifying the reported `n = 29` value moves `verified_upper_bound` from the Schadt
rational to Kingbird’s, closing `5.23e-5`, and there are two routes to it.
BC-044 recovers a minimal polynomial and discharges it exactly — strictly stronger, and
of uncertain feasibility: the completed sweep in X-004 found no integer relation through
degree twenty with coefficients below `10^22`, so the polynomial is large and
elimination in six unknowns may not terminate.
BC-045 needs no polynomial at all.
**The robust route is therefore the one that had no specification**, which is why
[plan-2026-08-28-interval-certification](../../../docs/project/specs/active/plan-2026-08-28-interval-certification.md)
was written before this replan and why BC-045 now owns two of the three blocks.

Within a block, BC-047 and BC-042 are independent of each other and of everything else,
so they are two lanes rather than a sequence.

**Reserve lanes**, for when a block stalls rather than as scheduled work:

| Commitment | Why it is not scheduled |
| --- | --- |
| BC-043 | Generalizes the route to sizes with no published system. Real value, but it gates nothing at `n = 29`. |
| BC-044 | The ambitious route. Its honest prior is poor; run it against a BC-047 refinement if a block closes early. |
| BC-048 | Independent of the whole symbolic lane; the natural filler. |
| BC-046 | A different program, and a decision before it is a build. It also unblocks BC-033. |

### Shape of an overnight run

Three blocks of about four hours give a ten-to-twelve hour run with a coherent
integration checkpoint at each boundary.
The
[portable session guide](../agent-sessions/README.md#starting-a-portable-four-hour-session)
owns the within-block discipline and this agenda does not restate it: one absolute
deadline per block, no slot over thirty minutes, protected finalization, and later
slices re-planned from measured elapsed time at every boundary.

Each block boundary runs the **full** `packing-validate`, not `--fast`, and commits
before the next block opens.
A block that closes zero commitments is reported, not silently extended.

### The session queue

Two commitments carry `priority: 0` and they are not interchangeable, so the order is
written down here rather than left to whoever reads the numbers first.
Each row is one session artifact under
[the portable session guide](../agent-sessions/README.md#starting-a-portable-four-hour-session).

| Next | Session | Commitment | Bead | Size | What it buys |
| ---: | --- | --- | --- | --- | --- |
| 1 | session-036 | BC-051 | `think-ej1d` | ~60 min | Change-scoped verification — it pays for itself inside the next session |
| 2 | session-037 | BC-045 phases 1–2 (block B) | `think-75ll` | ~4h | An operator that proves *uniqueness*, and refuses on the two-root and no-root controls |
| 3 | session-038 | BC-045 phases 3–4 (block C) | `think-75ll` | ~4h | Calibration at `n = 5, 10, 11`, then the `n = 29` verdict — the prize |
| 4 | session-039 | BC-049, then BC-046 | `think-xdly`, `think-0yo9` | ~60 min each | The rigidity residue, then what the atlas counts |

**Reserve, in the order to reach for them:** BC-048 (`think-nfsd`, the natural filler
and the only one that makes the symbolic route work on poses this project generates),
BC-043 (`think-va53`, generalizes assembly to sizes with no published system), BC-044
(`think-3lro`, ready but with a poor prior), BC-050 (`think-ecqk`, blocked on a scoping
decision rather than on anything technical).

Why this order, given the priorities are not a total ordering:

- **BC-051 goes first because it is the only item that makes the others cheaper.** D-355
  measured a two-file edit verified at `979.79s` against the `12.06s` its affected steps
  need. A sixty-minute slice that cuts iteration cost pays for itself inside the very
  next session, and every session after it.
  Sequencing it behind four hours of interval-certification work would spend that four
  hours at the old rate for no reason.
- **BC-045 leads the research line because it is the only route to the `n = 29` prize
  that needs no minimal polynomial.** Certifying the reported value moves
  `verified_upper_bound` from the Schadt rational to Kingbird’s, closing `5.23e-5` that
  no amount of better sourcing can close.
  BC-044 is the stronger route and may simply not terminate.
- **BC-046 is also `priority: 0` and still goes fourth**, because it is a different
  program. A resolved identity relation leaves `n = 29` uncertified, and the census
  cannot saturate either way until it is resolved — real value, no interaction with the
  prize.
- **BC-049 is short and mostly discharged.** The bulk first-party rigidity assessment
  covers 94 of 100 records; what remains is `n = 5, 28, 40`, where the catalogue says
  “Rigid.” and this repository deliberately does not restate that as its own finding.
- **Block C ends in a human decision.** An unattended runner may not accept the `n = 29`
  verdict: it is recorded `unresolved` with `needs_review: true` and a person decides.
  Plan for the session to stop there rather than treating it as a failure.

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
