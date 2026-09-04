---
title: "agenda-017 — six-hour block: the certificate generator, rigidity readiness, ten exact ceilings, and the W9 handoff"
softschema:
  contract: packing.squares:ExperimentAgenda/v1
  schema: ../schemas/agenda.schema.yaml
  envelope: agenda
  status: enforced
agenda:
  id: agenda-017
  title: Six-Hour Block — the Certificate Generator, Rigidity Readiness, Ten Exact Ceilings, and the W9 Handoff
  updated: '2026-09-04'
  status: active
  objective: >-
    Run one six-hour autonomous block from Agenda 016's merged closeout and the
    operator's direction to map the next research strategically, with the operator
    reviewing at the wall before the ten-hour Agenda 018. Four disjoint lanes open
    after a twenty-minute coordinator preflight. Lane A builds, freezes and reviews a
    first-party generator for weighted fractional unavoidable-set certificates -- the
    architecture behind the adopted 4.5058 bound -- and then tests H-061, whose success
    would be the first n = 12-specific lower bound in the retained corpus, at its
    prospectively fixed threshold. Lane B writes the general fixed-side local-rigidity theorem that T-014's
    method proves and decides from T-013's retained evidence whether the n = 40 route is
    open, then audits Stromquist's Theorem 3 at n = 11 to a determination. Lane C
    records what the planning survey found already within reach: the shipped rational
    promotion returned a certificate for every one of the ten decimal records whose
    verified ceiling still sits at the grid, all ten verified first-hand in the launch
    rehearsal, and recording them would move the verified upper bounds by about 1.83 in
    total; the same command reaches T-009's next rung. Lane D executes the selected handoff --
    three of think-ldq2's unrepaired D-044/D-046 clauses under an independent reviewer,
    the fourth and the archive residuals deferred by measured size -- and then makes the
    negative-control snapshot cap a property of the commit rather than the checkout. The research wall is 285 elapsed
    minutes; the final 75 are reserved for W10 disposition, documentation review,
    validation, publication and replanning, so the operator can review a green,
    results-first pull request before Agenda 018 starts.
  items:
  - id: BC-159
    purpose: tool_validation
    owner_focus: process
    instances: [5, 11, 12, 17, 29, 37, 39, 40, 41, 51, 55, 70, 71, 83, 87, 88]
    state: ready
    priority: 0
    question: >-
      Can the merged Agenda 016 handoff, the frozen lane inputs, the live tbd graph,
      the H-061 registration, the clocks and the fresh output paths all be frozen and
      readmitted before any target work begins?
    hypotheses: [H-061]
    budget: >-
      20 elapsed minutes. 0--5 record the common wall start, allocate session-085 as
      the coordinator record with every phase, delegation, stop condition and budget
      declared before dispatch, and arm the recurring 30-minute continuity trigger.
      5--12 confirm the toolchain the last two agendas lacked: the tbd CLI under Node 22
      (create, close and sync must each succeed on a throwaway probe that is closed
      before the sync, so no stray ready bead reaches the closeout's ranking), a
      non-shallow clone, the frozen uv environment and a passing records tier; dry-run
      the closeout's own calls, `tbd show think-2r1q --json` and `tbd ready --json`,
      since that path never ran in Agenda 016; then reconcile live tbd -- name one
      writer for think-ldq2, unpause it and repoint its spec to this agenda, confirm the
      four re-routed defect beads (D-422 and D-429 on think-ahyr, D-427 and D-428 on
      think-g4qi), note that think-g4qi's parent is the standing W9 epic by design, and
      close nothing that is not settled. 12--18 freeze the lane inputs by SHA-256, the
      one list the Launch Checklist's step 4 gives, which is the union the rehearsal
      hashed. Confirm H-061 is registered with its threshold fixed before any Lane A
      command runs, and record that the frozen environment offers scipy's linprog and
      no other LP solver, since it cannot gain a dependency mid-block. 18--20 freeze one
      revision-keyed launch packet naming the four lanes, models, reviewer rotation,
      output paths, safe commands, the concurrency cap of five sub-agents, and typed
      stop rules. Refuse dispatch on any drift, duplicate id, missing record, or
      unreviewed change to a criterion.
    entry: >-
      Agenda 016 is complete and merged (PR 77 at 9d5eae0f); this planning revision is
      pushed with the records tier green; H-061 exists at its registered threshold; the
      two Agenda 017 and 018 epics and their commitment beads exist on tbd-sync; and no
      Lane A output path is writable by another lane.
    exit: >-
      One launch packet naming the 360-minute wall, four lane owners, the reviewer
      rotation, exact input hashes, output paths, safe commands, the concurrency cap
      and typed stop rules; session-085 complete enough to render a resource receipt;
            think-ldq2 unpaused under one named writer; the continuity trigger armed; and no
      target command run. Lanes may read their frozen inputs from 00:05 and may run
      nothing and write nothing before the packet is admitted.
    bead: think-uqgp
    depends_on: []
    parallel_group: agenda017-coordinator
    workflows: [process-review]
    next_evidence: >-
      A passed launch packet opens BC-160, BC-163, BC-165 and BC-167 concurrently. On
      any refusal, the coordinator runs no target, marks every downstream commitment
      never-opened with the preflight reason, and opens BC-169 on that failed packet.
  - id: BC-160
    purpose: tool_validation
    owner_focus: correctness
    instances: [11, 12, 17]
    state: blocked
    priority: 0
    question: >-
      Can a first-party generator produce weighted fractional unavoidable-set
      certificates that the repository's own exact verifier accepts, with the two
      retained n = 17 certificates as positive controls and every named forgery
      refused, before any target side is attempted?
    hypotheses: [H-061]
    budget: >-
      135 elapsed minutes in the Lane A writer, Opus at maximum thinking, on the design
      the planning survey wrote out. 0--30 W7 generalise the n = 17 event-cell verifier
      so its certificate object is (n, rational side L, shrunken side B, rational-weight
      atoms, rational direction list with its largest half-gap tangent D derived from
      the list, symmetry declaration) rather than one fixture, with five conditions
      checked explicitly -- **Condition 1**, symmetry; **Condition 2**, total mass
      strictly below n; **Condition 3**, the arc reaching pi/4; **Condition 4**,
      B(1 + D) < 1; and **Condition 5**, every selected event cell of the B-square sweep
      at every net direction carrying mass at least 1 -- keeping the frozen n = 17
      fixture as a byte-identical replay; note that the package's `shrink_margin` is the
      grid border M and not the theorem's shrink 1 - B. 30--85 build the generator: an
      LP over D4-orbit atom weights on a declared site grid, rows generated by the exact
      event-cell sweep as the separation oracle on the fixed net (angles between net
      directions are handled by the containment lemma, never sampled), column generation
      for new sites from the dual's coverage, rationalisation by a (1 + 1e-6) bump and
      round-up to a multiple of 1/S with the exact mass gate, and the five typed kill
      rules the survey names, including the ceiling by-product: a converged dual
      re-solved at B = 1 and scaled by its exact maximum depth is a theorem that no
      fractional certificate proves the bound at that side. 85--115 controls -- positive:
      the Massaccesi certificate re-encoded (168 atoms, 181 directions, total 203/12,
      all row minima 1, cell counts equal to exp-059's), the retained Burns certificate
      (268 atoms, total 169476/10000, minimum 10003/10000, so a verifier that only
      reports 1/1 is caught), the n17 selftest fixtures, and Massaccesi's published
      generator setting returning a total below 17; limitation: green17's sixteen
      unit-spaced points, expected refused by the shrink verifier at every side and
      recorded as the method's boundary, not as a failure; negative: total mass reaching
      n, one atom lightened, a dropped bracketing direction and separately a dropped
      interior direction, B pushed past the containment condition, the certificate at
      451/100 -- an expected refusal at Massaccesi's own search boundary, typed so that
      an acceptance there is a candidate n = 17 result to review and not a control
      failure -- an atom outside the container, a broken symmetry, and every refusal
      identical under -O; generator-level negative: the full pipeline at n = 12 and at
      n = 16, both at side 401/100, where the side-4 grid packs and so no accepted
      certificate with mass below n can exist, must end in a typed stop, and an
      acceptance is unresolved-invalid-instrument. Stromquist's Figure 13 set is not a control in this lane: its
      coordinates live in Q(sqrt 5), which the rational verifier does not carry, and the
      ten points alone are avoidable by construction, so they are not a certificate at
      any mass. 115--125 freeze the package at a revision and hand it to a target-blind
      readiness reviewer who authored none of it; 125--135 answer that reviewer's
      questions read-only while the review runs, changing nothing under it. No command
      in this block names a target side above 2 + 4/sqrt(5) at n = 12 other than the
      impossible-side negative control at 401/100, which can produce no registrable
      result.
    entry: >-
      BC-159 passed and the Lane A inputs are frozen by hash. The writer owns only the
      new package, its tests and its scratch directory; it may not edit the frozen
      n = 17 packages, the frontier or the result register.
    exit: >-
      A frozen instrument at one revision with passing positive, limitation and
      negative controls and a readiness review that names no blocking caveat, so that
      H-061 may move to instrument-ready; or the first typed stop -- guard refusal,
      technical failure or time limit -- with the retained state and an explicit
      statement that no target was evaluated.
    bead: think-yw5g
    depends_on: [BC-159]
    parallel_group: agenda017-lane-a
    workflows: [pipeline-improvement, factual-review]
    next_evidence: >-
      A passed readiness review sets H-061 instrument-ready and opens BC-161. A caveat
      or refusal keeps H-061 unresolved, marks BC-161 and BC-162 never-opened with the
      reason, and BC-169 records what the generator can and cannot yet do.
  - id: BC-161
    purpose: research
    owner_focus: insight
    instances: [12]
    state: blocked
    priority: 0
    question: >-
      Does the frozen generator produce an exact certificate that s(12) is at least
      19/5, which would be the first lower bound specific to n = 12 in the retained
      corpus -- or an exact ceiling showing that no fractional certificate can?
    hypotheses: [H-061]
    budget: >-
      105 elapsed minutes in the Lane A writer, from 02:40, after BC-160's readiness
      review returns and the coordinator flips H-061 to instrument-ready. 0--10 replay the
      frozen instrument's controls from a clean output root and record the revision.
      10--80 run the generator at n = 12, side 19/5, on the registered site ladder
      (grid 29, then at most two column-generation refinements) with 181 directions
      and B = 9973/10000, so the effective unit-square side is 38000/9973; the survey
      sized one separation sweep at ten to thirty seconds on four cores and the
      generation at ten to ninety minutes, with the kill line at a restricted optimum of
      12 - 1/500 or above. 80--100 rationalise and verify exactly on the int64 path and
      the independent matrix-product path; one repair iteration on a cell the float
      sweep misjudged, then a typed stop. 100--105 freeze the experiment record:
      certificate bytes and hash, direction list, per-direction minima, the V(G, K)
      ladder and dual, the receipts under normal and -O Python, and the claim boundary.
      The side does not move after results are seen; a certificate at a lower side is
      a typed result about the generator. If the dual converges and the master at
      B = 1 reaches twelve, the exact ceiling is recorded as the round's result -- it
      rejects H-061 as registered and is a theorem about the method. The round closes
      needs_review true.
    entry: >-
      BC-160's readiness review passed and H-061 carries instrument_ready true at the
      frozen revision; exp-060 is allocated with fresh result and receipt paths.
    exit: >-
      exp-060 terminal with either an exact certificate the frozen verifier accepts at
      19/5 and n = 12, or an exact ceiling certificate at 19/5, or the first typed stop
      with the retained LP state and an explicit canonical-result absence. Nothing in
      the frontier or the result register changes here.
    bead: think-2sh3
    depends_on: [BC-160]
    parallel_group: agenda017-lane-a
    workflows: [research-loop]
    next_evidence: >-
      BC-162 reviews every terminal outcome. Only an exact pass may register a result
      and move the n = 12 verified lower bound; a ceiling is registered as a result
      about the method after the same review.
  - id: BC-162
    purpose: measurement_validation
    owner_focus: correctness
    instances: [12]
    state: blocked
    priority: 0
    question: >-
      Does an independent Max reviewer reproduce the H-061 certificate and its entire
      admission boundary, and accept the lemma chain that turns finitely many
      directions and event cells into a bound for every orientation?
    hypotheses: [H-061]
    budget: >-
      45 elapsed minutes, Fable at maximum thinking, by a reviewer with no Lane A
      authorship. 0--15 replay the certificate through the frozen verifier from a
      clean output root under normal and -O Python and re-derive the decision from the
      emitted bytes in a separate process. 15--30 write a from-scratch whole-check
      evaluator that imports nothing from the lane and evaluates captured mass for the
      true unit square at every event-cell minimiser, with a few hundred random poses
      as a diagnostic that is never counted as evidence, and audit the lemma chain:
      closed versus open squares, the shrink-and-scaling step, strictness of total mass
      below 12, and finitely many directions; for a ceiling, re-derive in the same
      evaluator that every listed pose is contained in the container, that the depth
      bound holds at every vertex of the full arrangement, and that the scaled weights
      sum to at least 12 exactly. 30--45
      classify pass, bounded caveat, discrepancy, cannot-reproduce or invalid; only on
      an exact pass clear needs_review, register the next-free T-result at V4/C3 with
      a novelty basis that names Burns and Massaccesi's published architecture -- whose
      author anticipated the application to other n -- and claims only the n = 12
      certificate as first-party, move the n = 12 verified lower bound, score
      significance under the rubric with the reasoning written down (the survey reads
      the case at S3, the amount of movement being 0.011, and the instrument at S4 only
      once a second case lands), and regenerate every consumer. This review runs from 04:25 and its last 25 minutes
      fall inside the closeout window by design; registration must be complete before
      the pull request is rendered, and a pass that lands after 05:20 is reported
      needs_review true with registration deferred to Agenda 018.
    entry: >-
      BC-161 is terminal and its writer has stopped; the packet binds every input,
      output, command, decision and declared absence at one revision.
    exit: >-
      One immutable independent determination and either a registered n = 12 result
      with every consumer current, or no frontier change plus the exact caveat,
      discrepancy or cannot-reproduce reason and a named follow-up.
    bead: think-iz5r
    depends_on: [BC-161]
    parallel_group: agenda017-review-a
    workflows: [factual-review]
    next_evidence: >-
      BC-169 reports the result at its honest scope with its significance, and Agenda
      018's BC-170 fixes the next rung of the ladder from the certified side.
  - id: BC-163
    purpose: research
    owner_focus: insight
    instances: [5, 10, 11, 40]
    state: blocked
    priority: 1
    question: >-
      What general fixed-side local-rigidity theorem does the X-012 method prove, what
      exactly does T-013's retained n = 40 evidence -- seven flexes each refused at
      second order -- establish under it, and does one uniform stress refuse the whole
      known six-dimensional span?
    hypotheses: []
    budget: >-
      90 elapsed minutes, Fable at maximum thinking. 0--25 promote the planning
      survey's three exact n = 40 scripts into one refusable tool,
      devtools/assess_n40_second_order.py --check, that recomputes the census (640 wall
      functions with 48 active; 24,960 pair functions; 98 touching pairs in the four
      contact profiles), every retained flex's admitting-branch count, the all-branch
      stress supports, and the twin-row curvature verdict, adopting no count from the
      agenda. 25--50 decide by exact LP plus exact LDL whether one non-negative stress
      on the rows tight along the whole known span refuses every direction of that
      span at once; report yes or no with the certificate or the failing cell.
      50--90 write X-013: the general theorem with every hypothesis explicit --
      intrinsic chart, complete exact classification of every elementary function,
      the branchwise local reduction, the linearised cone per branch, and the
      pointwise positivity condition Lemma 8's induction consumes, with the proof
      that a stress chosen at order m stays supported on the shrinking tight set --
      together with its two corollaries (T-014's line cone, exp-013's zero cones),
      the n = 40 census, the finding that the devtools incidence model intersects
      the two host-side versions of a flush or corner contact and is thereby exact at
      first order and flattering at second, verified first-hand against
      cases.gobel40 before it is filed as a defect, and the obligation list Agenda
      018 executes: characterise the cone on the disjunctive system, check
      positivity face-wise, generalise the instrument to multi-branch contacts, and
      bound the chart's cost at 120 variables.
    entry: >-
      BC-159 passed and the Lane B inputs are frozen by hash. The lane writes only
      X-013, the new devtools entry point and its test, a defect record if the
      twin-intersection finding reproduces, and its scratch directory; it changes no
      frontier property, result or hypothesis.
    exit: >-
      X-013 frozen with the general theorem, the replayable n = 40 tool, the uniform-
      stress determination with its certificate or failing cell, the obligation list
      and the negative control this block's own step can run -- the uniform-stress
      step applied to the exact n = 10 pose's slide directions returns not-refused,
      since every curvature vanishes along a translation -- while the probe-level
      slides and the n = 3 side-2 family are Agenda 018's C9 and C10; or a typed stop
      naming the smallest unresolved question.
    bead: think-87gh
    depends_on: [BC-159]
    parallel_group: agenda017-lane-b
    workflows: [insight-iteration, pipeline-improvement]
    next_evidence: >-
      The determination sizes Agenda 018's rigidity lane: a uniform stress on the
      span leaves only the cone characterisation between T-013 and a theorem, and
      its absence adds face-wise positivity to the obligations. Either way BC-164
      opens in the same lane and the Trump radius route stays the ten-hour lane's
      first theorem target.
  - id: BC-164
    purpose: research
    owner_focus: correctness
    instances: [11]
    state: blocked
    priority: 1
    question: >-
      Does Stromquist 2003's Theorem 3 -- every n = 11 packing whose orientations all
      lie in {0, 45} degrees has side at least 2 + (4/3) sqrt 2 -- certify exactly as
      printed, or where exactly does it escape?
    hypotheses: []
    budget: >-
      165 elapsed minutes, Fable at maximum thinking, in the Lane B agent after
      BC-163 freezes. 0--10 transcribe Theorem 3's point sets from the frozen raw
      extraction, since cases/stromquist carries only Theorem 2's Figure 14 set over
      Q(sqrt 5): the ten Figure 13 points and the twelve Theorem 3 points, all over
      Q(sqrt 2) at s = 2 + (4/3) sqrt 2, with the closed-box convention declared.
      10--25 run search_escape with theta_steps = 2 and refine_top = 0, the supported
      call that sweeps exactly {0, pi/4}, on the ten Figure 13 points at 0 degrees --
      which is how the paper proves that case -- and on the twelve at 45 degrees; the
      rehearsal measured the twelve at 45 degrees unavoidable by a margin near 1.1e-3
      and the 0-degree case decided only by the closed-box convention, so an exact
      escape here is a determination on its own and is certified before anything else.
      25--120 reconstruct the region decompositions on the repaired-cover machinery
      over Q(sqrt 2), proving Lemmas 7 and 8 finitely for the two orientations rather
      than citing them, and deciding the zero-margin Lemma 7 premise exactly. 120--150
      controls: a displaced point, a removed face and a widened region must each be
      refused. 150--165 freeze the packet with its claim boundary. Stop at the first
      typed proof gap or at the wall; a partial cover is process evidence and not a
      negative result.
    entry: >-
      BC-163 is frozen and the Lane B agent is free; cases/stromquist and the
      Stromquist 2003 raw extraction, which is where Theorem 3's points are printed,
      are frozen by hash. The lane writes only its new case
      directory, tests and scratch directory; no frontier or result-register change.
    exit: >-
      An exact cover certificate for Theorem 3 as printed, or an exact escape
      certificate plus, if found inside the wall, a source-distinct repair
      certificate; or the first typed stop. Registration of any outcome waits for an
      independent review, in BC-169's window if it fits and otherwise in Agenda 018.
    bead: think-plvi
    depends_on: [BC-163]
    parallel_group: agenda017-lane-b
    workflows: [factual-review, research-loop]
    next_evidence: >-
      A certificate as printed is a machine audit at V4/C3, previously-published; the
      survey reads it at S3, and an exact refutation with a repair at S4 on the T-010
      precedent, for the reviewer to score. Its independent review and registration
      are Agenda 018's BC-185, in the Fable agent's free hour before the Trump radius
      opens; nothing is registered without it. Either outcome opens H-036's
      neighbourhood theorem as a later candidate.
  - id: BC-165
    purpose: research
    owner_focus: correctness
    instances: [29, 37, 39, 41, 51, 55, 70, 71, 83, 87, 88]
    state: blocked
    priority: 1
    question: >-
      Does the shipped rational promotion certify every one of the ten open cases whose
      verified upper bound still sits at the grid while a decimal record is reported,
      and does the same command at n = 29 reach T-009's declared next rung?
    hypotheses: []
    budget: >-
      180 elapsed minutes, Opus at maximum thinking. 0--20 replay the sweep the
      planning survey ran -- packing-witness promote --strategy robust-rational
      --max-side-increase 1e-6 on the known-best witnesses at n = 37, 39, 41, 51, 55,
      70, 71, 83, 87 and 88 -- writing each certificate straight to its final
      packing-relative path, witnesses/known-best-n0NN-rational.yaml beside the
      retained n = 11 control and not under witnesses/known-best/, which the atlas
      builder treats as generated; the certificate's replay command embeds the output
      path verbatim, so a scratch path would bake into the record. Verify each with
      packing-witness verify from a clean root; the rehearsal produced and verified all
      ten in 24 seconds with side increases between 5.8e-31 and 7.9e-29 and every
      certified pose touching the container exactly, which the claim boundary states. 20--40 run the calibration controls: the retained n = 11 rational
      control, and n = 29 against both retained certificates, where the rational
      certificate on the Kingbird witness lands about 5.43e-20 below T-009's interval
      bound. 40--70 draft one evidence family, the ten witness records and the ten
      frontier field changes, with the claim boundary written verbatim: a bound at the
      certified side, which is the reported decimal plus the stated increase, not at
      the decimal, not on the source pose, and nothing about optimality; the reported
      upper bound stays uncertified. 70--140 run the gates that read the moved fields -- check_basic_bounds inside the
      exact-verification step, whose grid replay is conditional on the E-basic-grid-upper
      evidence id each move replaces and so must be re-pointed rather than silently
      dropped, check_results, check_certificate_citations, which does not see
      witness-file certificates and is kept for the frontier records it does read, and
      the records tier -- and repair what they name; add the in-lane refusal control,
      one coordinate of one certificate mutated and verify recording the refusal, so
      the family names a control path. 140--170
      register the n = 29 rational certificate as its own evidence entry, rewrite the
      interval entry's limitations -- including its sentence that the verified upper
      bound has not been moved to it, which n-029.md contradicts -- and T-009's
      rationale to compare the two routes on the same packing (D-431), restate T-009's
      claim method-neutrally so the evidence carries the routes, and propose the raise
      to C4 through the results checker, noting that the rational route certifies a
      dilated neighbour of the pose and not the source pose. 170--180 freeze the packet for the reviewer. Any case whose verify does
      not pass is dropped from the batch and typed, not debugged in-lane.
    entry: >-
      BC-159 passed and the Lane C inputs are frozen by hash. The lane writes only new
      witness files, evidence and frontier fields for the eleven named cases, the
      results register entries the reviewer will confirm, and its scratch directory.
    exit: >-
      Ten reviewed verified-upper-bound moves totalling 1.830, or the subset that
      passed with each refusal typed; the n = 29 rational certificate registered and
      D-431 repaired; and nothing claimed about any reported decimal.
    bead: think-stb5
    depends_on: [BC-159]
    parallel_group: agenda017-lane-c
    workflows: [research-loop, factual-review]
    next_evidence: >-
      BC-166 reviews every certificate and, on a pass, registers one family result and
      T-009's rung change before the closeout renders the pull request. H-049, the
      n = 90 primitive, moves to Agenda 018's BC-178 with its corrected framing.
  - id: BC-166
    purpose: measurement_validation
    owner_focus: correctness
    instances: [29, 37, 39, 41, 51, 55, 70, 71, 83, 87, 88]
    state: blocked
    priority: 1
    question: >-
      Does an independent reviewer reproduce every rational certificate, confirm that
      the record claims exactly the certified side and no more, and accept the family's
      registration and T-009's rung change?
    hypotheses: []
    budget: >-
      30 elapsed minutes by a reviewer with no Lane C authorship, Opus at extra-high
      thinking. Re-run packing-witness verify on every certificate from a clean root;
      confirm each certified side exceeds its reported decimal by the recorded amount
      and that no frontier field or prose claims the decimal; check the evidence family
      against the schema and the claim boundary against epistemics.md; on an exact pass
      register one family result at V4/C3, previously-published, with its significance
      scored under the rubric and the reasoning written down, apply the ten field
      moves, raise T-009 to C4 on the n = 29 rational certificate as a distinct method,
      and regenerate every consumer; on any other determination leave the frontier
      unchanged and name the follow-up.
    entry: >-
      BC-165 is terminal and its writer has stopped.
    exit: >-
      One immutable determination -- pass, bounded caveat, discrepancy or
      cannot-reproduce -- and either a registered family result with every consumer
      current or no frontier change and a named follow-up.
    bead: think-vyff
    depends_on: [BC-165]
    parallel_group: agenda017-review-c
    workflows: [factual-review]
    next_evidence: >-
      BC-169 presents the family result and T-009's rung change with their
      significance in the synopsis headline and above the pull request's dispositions.
  - id: BC-167
    purpose: tool_validation
    owner_focus: correctness
    instances: [5, 11, 17]
    state: blocked
    priority: 1
    question: >-
      Can the three D-044 and D-046 source-finding clauses that fit one block -- the
      exact-zero overlap screen, the timebox contract stated three ways, and the report
      that omits runnable-but-unrun work -- be repaired with regressions, under an
      independent review of the one that loosens an acceptance screen, without changing
      a scientific criterion?
    hypotheses: []
    budget: >-
      100 elapsed minutes for the writer, Opus at extra-high thinking, then 45 for a
      reviewer with no W9 authorship, Opus at maximum thinking. 0--10 regenerate
      defects.md, reproduce each clause against the current runner.py and confirm it
      still stands. 10--45 W9-1: validated_record's `overlap != 0.0` screen admits
      `0 <= overlap <= POSE_TOLERANCE` and lets the separate-process oracle decide, with
      regressions that a 1e-18 and a 1e-9 overlap reach the oracle and a 2e-9 overlap is
      refused at the screen; this repair is proposed, not merged, until the reviewer
      accepts it, because it loosens an admission screen and only the oracle stands
      behind it afterwards. 45--75 W9-3: the per-cell timebox contract is stated once --
      per round with an equal per-cell share, which is what the code does and what
      D-046's clause exists to close -- in the hypothesis schema, the runbook and
      runner.py, and the timing-sensitive share test is driven off a monkeypatched
      clock; this is BC-154's unapplied correction 3. 75--100 W9-4: run() and
      write_report() track the runnable hypotheses the session never reached and report
      them in a third section, with the regression that names one. The reviewer replays
      every regression, reverts each repair in a copy to prove it load-bearing, and
      returns pass or bounded caveat per unit. The remaining two units -- the
      unconditionally true dirty flag (W9-2) and the archive digest that binds execute to
      record and closes the three archive residuals (W9-5) -- are Agenda 018's wave two,
      not this block's, by measured size.
    entry: >-
      BC-159 unpaused think-ldq2 under one named writer; runner.py and
      test_campaign_runner_trust_boundary.py are frozen by hash. The lane writes only
      runner.py, its tests, the schema and runbook lines the timebox contract needs, the
      D-044 and D-046 records, and its scratch directory.
    exit: >-
      Each of the three units carries one disposition -- fixed with regression,
      contained, rerouted or blocked -- with the reviewer's determination recorded per
      unit and the D-044 and D-046 `fix` and `regression` prose rewritten against what
      landed; neither defect moves to fixed while W9-2 or W9-5 stands open.
    bead: think-ldq2
    depends_on: [BC-159]
    parallel_group: agenda017-lane-d
    workflows: [remediation, factual-review]
    next_evidence: >-
      BC-169 records each unit's terminal disposition. The same writer opens BC-168 once
      the reviewer has the packet, and Agenda 018's BC-179 takes W9-2 and W9-5.
  - id: BC-168
    purpose: tool_validation
    owner_focus: efficiency
    instances: [5, 11, 17]
    state: blocked
    priority: 1
    question: >-
      Can the negative-control snapshot cap be made a property of the commit rather
      than of the checkout, so the full local gate passes on a used tree, and can the
      generated-view fold stop refusing the formatter's own output?
    hypotheses: []
    budget: >-
      65 elapsed minutes for the writer, Opus at extra-high thinking, in the Lane D
      writer from 02:45, once the BC-167 reviewer has returned, so that a reviewer
      replaces a writer rather than adding to it; then 30 for the same reviewer.
      0--10 measure the current tree: snapshot_source_bytes() with and without
      __pycache__, .pytest_cache and .ruff_cache -- the planning survey measured
      68,224,754 bytes against the 67,108,864 cap on this checkout, 11,318,965 of them
      caches, so the guard is red today. It is red on the hosted runner too: the
      pull-request surface at dd458471 failed this assertion at 67,173,741 bytes and main
      at 9d5eae0f fails the same step, so this repair is also what turns hosted CI green
      for every branch. 10--45 D-422: a CACHE_DIRS set pruned from the
      walk and from the root-document glob in snapshot_source_bytes(), the two top-level
      caches added to PRUNE so _clone_into skips them, and every nested __pycache__
      removed from a cloned worker after the copy; the control plants a cache file of
      known size under a counted path and asserts the count is unchanged and no cache
      survives in a worker. 45--65 D-429: the one `.replace(" ...", "...")` in fold,
      deletion of the headline renderer's local workaround, and the regression that
      renders a cell ending in `...`, runs the pinned flowmark, and asserts `--check`
      still reports the block current. The reviewer replays both controls and reverts
      each repair in a copy; both touch shared guards, which is why neither lands
      unreviewed.
    entry: >-
      BC-167's reviewer has returned its determination; run_negative_controls.py,
      render_research_tables.py and render_results_headline.py are frozen by hash.
    exit: >-
      D-422 and D-429 fixed with regressions and a before/after byte measurement, or a
      typed stop naming what still breaches the cap; the reviewer's determination
      recorded for each.
    bead: think-ahyr
    depends_on: [BC-159]
    parallel_group: agenda017-lane-d
    workflows: [pipeline-improvement, factual-review]
    next_evidence: >-
      BC-169's full local gate is the test: it either passes the negative-control step
      on this used checkout, or the closeout records exactly which surface still
      breaches and by how much.
  - id: BC-169
    purpose: research
    owner_focus: process
    instances: [11, 12, 29, 37, 39, 40, 41, 51, 55, 70, 71, 83, 87, 88]
    state: blocked
    priority: 0
    question: >-
      What did Agenda 017 establish, fail to establish or repair, what significance
      does each registered result carry, why did each incomplete scope stop, and
      which one entry runs next after the operator's review?
    hypotheses: [H-061]
    budget: >-
      75 elapsed minutes reserved from 04:45 through 06:00, with two pieces pre-staged
      during the 04:00--04:45 freeze because Agenda 016 needed 120 minutes for nine
      commitments and this block has eleven: the outcome-row skeleton for every
      commitment is drafted before 04:45 so the closeout fills it rather than writes
      it, and the six-document review is taken as a fallback card at 04:00 by an agent
      whose lane is terminal. 0--10 stop every writer and process and freeze evidence,
      including partial LP state and declared absences. 10--25 complete the outcome
      rows at the smallest honest scope with classification, evidence, disposition and
      follow-up, and update the D-044, D-046, D-422 and D-429 records. 25--40 close
      think-tkwj and sync first, because close_session --agenda refuses while the
      selected next bead is blocked on it; then regenerate the ledger, agenda map,
      session-close, synopsis, results-headline, defect and document views in that one
      call, and reconcile live tbd, closing settled beads. 40--55 pass the records tier
      and the push tier, commit and push so hosted CI starts while the full local gate
      runs; any registration BC-162 or BC-166 landed regenerates the results headline
      before this step or the records tier is red. 55--70 render the pull-request
      description leading with cost, then with every result scored inside the wall and
      its significance in the rubric's own words, then stop reasons, dispositions, file
      changes, validation and limitations; record operator input as unavailable if the
      wall closes before the review, and select Agenda 018's BC-170 as the one next
      entry without executing it. 70--75 the documentation and de-slop pass over the
      documents this block created. If the full gate outlasts 06:00, record the
      research wall as complete and continue only the same mechanical closeout,
      reporting that post-wall time separately.
    entry: >-
      BC-164, BC-166, BC-167 and BC-168 are terminal, including never-opened branches,
      and every lane writer has stopped; BC-162 is the one review the plan expects to
      run inside the closeout window, and its registration must complete before the
      pull request is rendered. The coordinator owns the only shared-record, tbd, Git,
      generated-view and pull-request writes.
    exit: >-
      Agenda 017 and session-085 terminal; every attempted scope carries an outcome,
      stop reason, evidence, disposition and follow-up; every generated and
      reader-facing document has an explicit decision; the records and push tiers
      pass and the full local gate passes or the exact blocker is recorded; the pull
      request leads with measured cost and then with each result and its significance;
      tbd is synchronized through the CLI; and SYNOPSIS publishes exactly one
      unexecuted next entry. No merge occurs without the owner.
    bead: think-tkwj
    depends_on: [BC-162, BC-164, BC-166, BC-167, BC-168]
    parallel_group: agenda017-closeout
    workflows: [review-planning-oversight, documentation-pass, process-review]
    next_evidence: >-
      The operator's review of the pull request confirms or revises Agenda 018's lane
      order; BC-170 begins only after that review or the declared autonomous fallback,
      never inside this closeout.
---
# Agenda 017 — Six-Hour Block: the Certificate Generator, Rigidity Readiness, Ten Exact Ceilings, and the W9 Handoff

## Workflow Entry Point

This agenda is the operator-directed successor to
[Agenda 016](agenda-016-results-first-continuation-rigidity-and-remediation.md), whose
W10 closeout selected `think-5j8d` as the marker of where its chain stopped and
`think-ldq2` as the recommended follow-up.
The operator then asked for a strategic map of the next research in two blocks — six
hours to be reviewed the same evening, then ten hours overnight — that pushes
aggressively on the dimensions most likely to produce significant results soonest, keeps
several avenues open, returns to routes where the program has been stuck, and balances
mathematical innovation with process efficiency and documentation rigour.
This agenda is the six-hour block;
[Agenda 018](agenda-018-ten-hour-continuation-ladders-theorems-and-wave-two.md) is the
ten-hour block and stays paused until the operator has reviewed this one.

Begin at `BC-159`. The coordinator declares `process-review` for the preflight, creates
`session-085` before dispatch, freezes the wall, and then holds `research-loop` for the
lanes and `review-planning-oversight` for the closeout.
`BC-159` opens four disjoint lanes: `BC-160` and the certificate route in Lane A,
`BC-163` then `BC-164` in Lane B, `BC-165` in Lane C, and `BC-167` then `BC-168` in Lane
D. The coordinator alone writes shared records, generated views, tbd, Git and the pull
request; lane authors write only their declared packages, tests, experiment and packet
artifacts; reviewers rotate so no author clears that author’s own result.

**Model assignment**, under `OR-2` and `OR-10`: Claude Fable at maximum thinking for the
mathematics and every independent review of a scientific result — `BC-162`, `BC-163` and
`BC-164`; Claude Opus at maximum thinking for the Lane A build and round, the Lane C
sweep and the `BC-167` reviewer; Claude Opus at extra-high thinking for the Lane D
writer, `BC-166`, `BC-168`, the readiness reviewer and mechanical integration.
Codex Max corresponds to Fable and Codex High or Extra High to Opus where a matched
handoff applies.

## Launch Checklist

The coordinator runs these in order at `BC-159`, from the repository root unless noted,
and refuses dispatch at the first failure.

1. Record the wall start in `session-085` and arm the recurring 30-minute continuity
   trigger; under `OR-8` only the operator deletes it.
   If the harness refuses a sub-hourly cadence, arm it hourly and keep a one-shot chain
   beside it, never the chain alone.
2. Toolchain: `tbd prime` must run from the session script.
   This planning session installed the pinned `get-tbd@0.8.0` under `/opt/node22` and a
   launcher at `~/.local/bin/tbd` that puts Node 22 first, because the script’s own
   `PATH` line finds Node 20 first -- the reason the last two agendas ran without the
   CLI. On a fresh container repeat that install before anything else;
   `close_session --agenda` hard-requires the binary.
   Create, close and sync one throwaway probe bead, closing it before the sync, and
   dry-run `tbd show think-2r1q --json` and `tbd ready --json`, the calls the closeout
   depends on. `git rev-parse --is-shallow-repository` must print `false`; if it prints
   `true`, `git fetch --unshallow origin` before the gate, or the provenance step fails
   on a record no commit here touches.
3. `cd packing && uv run --frozen --all-extras --group dev packing-validate --records`
   must pass; note the step count it prints rather than restating one.
4. Freeze inputs by `sha256sum` into the launch packet, one list for the agenda and the
   packet: `packing/devtools/pierce_pilot.py`; all five
   `packing/cases/n17_weighted_certificate*` packages; the retained Burns verifier under
   `packing/resources/web/n17-lower-bounds-2026/`; the BC-150 packet at
   `docs/project/reviews/review-2026-09-03-bc150-4-5058-adoption-packet.md`; `X-012`;
   the `E-n005-second-order-rigidity` and `E-n040-first-order-flexibility` entries
   extracted from `packing/frontier/evidence.yaml`, since they are entries and not
   files; `packing/cases/stromquist/` and the Stromquist 2003 raw extraction under
   `packing/resources/papers/`; the ten known-best witnesses,
   `packing/witnesses/known-best-n011-rational-control.yaml`,
   `packing/witnesses/kingbird-n029-2026-interval.yaml` and
   `packing/witnesses/schadt-n029-2025-rational.yaml`;
   `packing/src/sqpack/campaign/runner.py`,
   `packing/tests/test_campaign_runner_trust_boundary.py`,
   `packing/devtools/run_negative_controls.py`,
   `packing/devtools/render_research_tables.py` and
   `packing/devtools/render_results_headline.py`. The rehearsal hashed this union and
   found every path.
5. Confirm `H-061` is registered at its fixed threshold with `instrument_ready: false`,
   and allocate `exp-060` for Lane A with fresh result and receipt paths, in the
   experiment schema’s day-one shape: `hypotheses: [H-061]`, `primary_criterion` copied
   verbatim from H-061’s threshold, `results: []`, `decision: in-progress`, a lease, and
   no `effort` until terminal.
   Lane C allocates no experiment: it records witness files, evidence entries and
   frontier fields, and the ledger refuses a round that tests no hypothesis.
   `session-085` carries every required phase field from the start, with outcome and
   evidence written as the declared expectation and rewritten at close.
   No placeholder reserves an id.
6. Unpause `think-ldq2` under one named writer and repoint its spec to this agenda;
   confirm the four re-routed defect beads, and note in the packet that `think-g4qi`’s
   parent is the standing W9 epic `think-cyko` by design, so `BC-170` does not repair
   it.
7. Dispatch the four lanes three minutes apart from 00:20, with the concurrency cap of
   five sub-agents in flight, reviewers included; a ten-minute stagger would push Lane
   C’s review out of the wall, so the stagger is short and the harness’s usage is read
   at every 30-minute reminder instead.

## Why These Lanes Are Next

**Lane A is where the machinery now points.** Agenda 016 adopted, at source-backed
scope, Massaccesi’s fractional unavoidable-set certificate for `s(17) ≥ 4.5058`, and in
doing so built and reviewed five independent replays of the exact event-cell reduction
that turns “every unit square captures mass at least one” into finitely many rational
directions and cells.
The generation side of that architecture does not exist here.
Building it is the most valuable instrument the program can add: the same LP that
produced the `n = 17` certificate can produce certificates at the sizes the survey
priced as reachable, `n = 20` to `32`, where the proved lower bound is still Nagamochi’s
2005 closed form, and at the two sizes that matter most.
The first target is `n = 12`, where the standing lower bound is Stromquist’s `n = 11`
bound `2 + 4/√5 ≈ 3.7889` inherited by monotonicity and nothing specific to `n = 12` has
ever been proved. `H-061` fixes the threshold before synthesis, as `H-039` requires, and
a certificate there is the first `n = 12`-specific result in the problem’s history — by
`0.011`, which the record will say plainly; the durable value is the crossing curve the
ladder measures and the exact ceilings the dual yields where a certificate does not
exist.
Agenda 018 then climbs the ladder and takes the `n = 11` shot, where a certificate
with total mass below eleven at any side above `2 + 4/√5` would be the first movement on
the central open case since 2003.

**Lane B turns one theorem into a technique.** `T-014` proved fixed-side local rigidity
of Goebel’s `n = 5` optimum by a chart, a complete inequality accounting, curve
selection and an order-`2m` coefficient induction closed by a non-negative self-stress.
Whether that argument is a reusable technique — `S4` under the rubric — or one case
depends on a question nobody had written down: what exactly the induction needs from the
stress on a cone of dimension above one.
The planning survey’s answer, to be written out and checked in `X-013`, is that the
condition is pointwise — every flex in every local branch refused by a stress supported
on the rows tight along it — so `T-013`’s seven refusals at `n = 40` are the hypothesis
at fourteen rays and not on any face, and the real obligation there is the cone
characterisation `D-391` names.
The same survey found, by exact computation on `cases.gobel40`, that the devtools
incidence model intersects the two host-side versions of a flush contact, which is exact
at first order and flattering at second; `BC-163` verifies that first-hand before it is
filed. It also found that the `n = 11` radius `H-022` asks for is a different and easier
theorem than `n = 40`: first-order rigidity in every branch gives an explicit radius by
Taylor bounds with no curve selection, reachable at `V4`, which is why Agenda 018’s
rigidity lane targets Trump’s packing first.
The same Fable agent then audits Stromquist’s Theorem 3, the `0°/45°` theorem that
settled Gardner’s conjecture at `n = 11`: its twelve points are printed exactly, the
cover machinery exists at another side, and the printed `G` point has the shape of the
one `D-152` showed escapes in Theorem 2, so a twenty-minute escape search is a
determination on its own.

**Lane C banks what is already within reach.** Every route above is a lower bound or a
rigidity theorem, and the verified upper bounds have their own cheap movement waiting:
the planning survey ran the shipped rational promotion on the ten open cases whose
verified ceiling still sits at the grid while a decimal record is reported, and every
one returned an exact certificate at a side above the decimal by less than `8 × 10⁻²⁹`;
the coordinator reproduced two of them first-hand before dispatch.
Recording them moves ten verified upper bounds by `1.830` in total for about three hours
of record work at a risk the survey already retired, and the same command at `n = 29`
lands `5.4 × 10⁻²⁰` below `T-009`’s interval certificate, which both reaches that
result’s declared next rung and exposes that its comparative rationale compared two
different packings (`D-431`). The upper-bound construction avenue is not dropped:
`H-049`, the `n = 90` primitive, moves to Agenda 018 with the correction the survey
derived from Arslanov’s own inequality — a squeezable `(4, 6)/20` primitive would also
pack thirty squares below side six, the `m = 6` instance of `s(m² − m) = m` — and with
the instrument gap it found, since nothing in the tree measures a squeeze in a rectangle
yet.

**Lane D is the selected handoff.** `OR-4` says take the next slice from the handoff,
and Agenda 016’s closeout ranked `think-ldq2` first: four clauses of the D-044 and D-046
source findings that never reached either record, one of which loosens an acceptance
screen and so needs the reviewer the closing run no longer had.
After that packet is with its reviewer, the same writer closes the two gate defects that
made the last full local gate red on a used checkout — the snapshot cap breached by
build caches the gate itself writes (`D-422`) and the fold that refuses the formatter’s
own output (`D-429`) — so that this agenda’s own closeout gate can pass where Agenda
016’s could not.

## Exact Wall and Reviewer Rotation

| Elapsed | Coordinator | Lane A (`n = 12`) | Lane B (rigidity, Theorem 3) | Lane C (ten ceilings) | Lane D (W9, gate) |
| --- | --- | --- | --- | --- | --- |
| 00:00--00:20 | `BC-159` preflight; lanes read frozen inputs from 00:05 and run nothing | read-only design from 00:05 | read-only | read-only | inventory snapshot, read-only |
| 00:20--01:50 | observe, integrate only frozen packets | `BC-160` build | `BC-163` theorem and `n = 40` decision | `BC-165` sweep, controls, records | `BC-167` writer |
| 01:50--02:35 | dispatch the readiness reviewer at 02:25 | `BC-160` controls, freeze at 02:25, answers read-only to 02:35 | `BC-164` transcription, escape search, then cover | `BC-165` continues | `BC-167` writer to 02:00; reviewer 02:00--02:45 |
| 02:35--04:00 | integrate reviews; flip `H-061` instrument-ready at 02:40 | `BC-161` target round 02:40--04:25 | `BC-164` continues | `BC-165` gates to 03:20; `BC-166` review 03:20--03:50 | `BC-168` writer 02:45--03:50; reviewer 03:50--04:20 |
| 04:00--04:45 | freeze lanes; draft the outcome-row skeleton; six-document review as a card | `BC-162` review from 04:25, its last 25 minutes inside the closeout by design | `BC-164` freezes by 04:35 | registration and consumers by 04:20 | integration and hand-back to 04:20 |
| 04:45--06:00 | `BC-169` W10 closeout with all lanes | closeout support | closeout support | closeout support | closeout support |

Peak concurrency is five sub-agents, at 02:25--02:40 when the readiness reviewer joins
four lanes, and otherwise four; a reviewer replaces its lane’s writer rather than adding
to it, which is why `BC-168` opens only when the `BC-167` reviewer has returned.
The planning survey measured Agenda 016’s interruption as a rate, not a count: the limit
at about 10:45Z followed four consecutive hours above 170 million tokens per hour at 57
million per agent-hour, while the run’s peak of seven concurrent agents did not trip it.
Four sustained sits inside the band that produced it, so the coordinator staggers the
four dispatches three minutes apart, never opens three fresh agents in the same minute,
reads the harness’s usage at every 30-minute reminder, and on the first rate-limit
signal pauses Lane C -- the most self-contained lane -- until another lane hands off.
The two measured wastes are ruled out in advance: no agent blocks on a gate or a poll
for more than 120 seconds (the last run spent 89 minutes, 34.9% of its tool time,
watching gates), and the third one-off measurement of the same thing becomes a
`devtools/` entry point under `OR-1`. No process-exclusive lease is declared, because no
lane’s exact computation is expected to exceed the minute scale; if Lane A’s LP or
verification runs past ten minutes, the coordinator declares a lease prospectively in
the launch packet’s amendment log and the other lanes read status once without polling.

## Routing Rules

1. `BC-160` freezes before any target side is named, and its readiness reviewer never
   sees a target. `H-061` moves to instrument-ready only on that review’s pass.
2. `BC-162` reviews `BC-161` whatever its outcome.
   Only an exact pass registers a result, moves the `n = 12` verified lower bound, and
   scores its significance; every other determination leaves the frontier unchanged and
   names the follow-up.
3. `BC-164` opens only after `BC-163` freezes, and its first twenty minutes are the
   escape search. An escape is certified before any cover is attempted.
4. `BC-166` reviews `BC-165` whatever its outcome.
   Only a pass registers the family result and moves the ten verified ceilings, and
   every move states the certified side rather than the reported decimal.
5. `BC-167` merges the F-02 screen repair only on its reviewer’s explicit acceptance;
   the other clauses may land on the writer’s regressions and are still reviewed.
6. `BC-169` starts at 04:45 even when a lane used less than its allocation.
   Saved time does not consume the closeout reserve.
7. Every result registered inside the wall is presented in the synopsis headline and
   above the pull request’s dispositions with its `V`, `C` and `S` rungs and the
   rubric’s own wording, as `conventions.md` now requires; a result that is recorded but
   unpresented is a closeout failure.

## Bounded Fallback Cards

An agent whose authored lane is terminal may take one coordinator-assigned card at a
time. Cards never change a frozen criterion, start a new experiment, or review the
agent’s own work.

1. **Packet preflight, 15 minutes.** Check hashes, declared absences, one mutation, safe
   replay commands and claim boundaries for another lane.
2. **Readiness review of the generator, 15 minutes.** Replay `BC-160`’s controls from a
   clean root without seeing a target; return pass or bounded caveat.
3. **Green17 exact-ceiling readiness, 25 minutes.** Read `think-iye2` and the retained
   `753/250 + √2` evidence; list the exact obligations without changing code.
4. **Stale-count sweep, 20 minutes.** The frontier prose said sixty-three open cases
   rest on Nagamochi’s closed form when the count is sixty; this planning revision
   corrected it and filed `D-430`, and the launchability review found the figure
   surviving at line 933 of the 2026-08-22 research report on eleven squares.
   Sweep `docs/project/` and `TUTORIAL.md` for that figure and for stale `n = 17`--`19`
   lower bounds the adoption review named as unsurveyed; a dated report is appended to,
   not rewritten.

If no eligible card remains, the agent assists `BC-169` with read-only evidence
assembly. No card becomes an undeclared fifth research lane.

## Stop and Outcome Rules

A lane stops on frozen-input drift, a known-answer or mutation failure, a missing
independent verifier, an invalid theorem transfer, three consecutive execution or
persistence failures, or the research wall.
It records the first applicable W10 classification rather than the most flattering:
never-opened, guard-refused, technical-failure, time-limited, then achieved,
bounded-negative or inconclusive under the frozen criterion.

A certificate at a side below `H-061`’s threshold is a typed result about the generator
and does not move the threshold or the frontier.
A partial cover in `BC-164` is process evidence, not a negative.
A negative in `BC-165` is bounded by its declared structure class and never a theorem.
A W9 repair is engineering work and never a scientific result.
Every terminal scope receives one disposition — retire as success, retire as a completed
bounded negative, continue from a preserved state, fix and rerun, or defer to a named
dependency — and continue, fix-and-rerun and defer always name a live bead.

## Time and Cost Accounting

The closeout reports four clocks without collapsing them: the exact 360-minute session
wall from `BC-159`’s start marker to the research stop; per-lane wall intervals, which
overlap and do not add to session wall time; recursive agent-active and command time
from retained session receipts; and separately labelled post-wall mechanical time if
validation or hosted checks finish after 06:00. `BC-169` closes `session-085` before
rendering the pull-request cost block, states any coverage limitation, and then reports
results with their significance, stop reasons, dispositions and file changes.
A pending gate is work still in progress, not permission to call the agenda done.

## Record Corrections Made in This Planning Revision

Agenda 016’s closeout declared its follow-up bead ids while the `tbd` CLI was absent and
recorded them as unverified.
With the CLI restored under Node 22, every declared id was resolved against the sync
branch: `think-c46d`, named for `D-422` and `D-429`, is a closed bead (`BC-075`’s gate
retiering), and `think-xdly`, named for `D-427`, is the open rigidity task for
`n = 5, 28, 40`. Those four defect records now name the live beads that own the work —
`think-ahyr` for `D-422` and `D-429` under `BC-168`, and `think-g4qi` for `D-427` and
`D-428` under Agenda 018’s W9 wave — while the terminal agenda-016 record keeps its
declared text, since it was true to what the run could verify when written.
Separately, the frontier prose in `packing/frontier/README.md` and the generated case
bodies said sixty-three of the sixty-five open cases rest on Nagamochi’s closed form;
the count over the case records is sixty, because the 4.5058 adoption took `n = 17`,
`18` and `19` off it.
Corrected here and recorded as `D-430`. The survey also found, and the coordinator
reproduced, that `T-009`’s significance rationale compares its interval certificate
against a certificate on a different `n = 29` packing; that is `D-431`, repaired in
`BC-165`.

## Ranked Portfolio Outside the Wall

| Rank | Candidate | Disposition before Agenda 017 |
| ---: | --- | --- |
| 1 | The certificate generator and the first `n = 12` bound (`H-061`) | Execute in Lane A |
| 2 | The general rigidity theorem and the `n = 40` decision | Execute in Lane B; the proof itself waits for Agenda 018 |
| 3 | Stromquist Theorem 3 audit at `n = 11` | Execute in Lane B after the decision; the only published-proof audit that can reach a determination inside a block |
| 4 | The ten exact ceilings and `T-009`’s rung change | Execute in Lane C; the survey retired the risk |
| 5 | `think-ldq2`, the four W9 clauses, then `D-422` and `D-429` | Execute in Lane D |
| 6 | Bentz 2010 Theorem 9 audit (`T-006` to `C3`, `think-1o1f`) | Park: 12--18 agent-hours, cannot reach a determination in either block |
| 7 | Nagamochi Theorem 1’s unargued `λ = 1` step | Agenda 018’s `BC-181`, a two-hour spike under sixty open lower bounds |
| 8 | `H-049`, the `n = 90` primitive, now read as `s(30) < 6` | Agenda 018’s `BC-178`, with the rectangle instrument it needs built first |
| 9 | The generic interval certifier (`H-056` at `n = 39` first) | Agenda 018’s `BC-184`, tentative, as the technique rather than the bounds |
| 10 | Green17 exact ceiling (`think-iye2`), bespoke `n = 12` set (`think-0z9b`) | Retain; the generator supersedes the integral-set framing |

`BC-169` reranks this table from actual outcomes and operator input.

## Final Guard

At elapsed 04:45 every research lane begins terminalization and W10 owns the tree.
The coordinator updates the agenda with outcome rows and a closeout block, regenerates
all owned views, applies the documentation and de-slop pass, closes session receipts,
runs the records tier and the required `packing-validate --push` tier, commits and
pushes before the slower full gate finishes, and keeps the pull request current through
hosted checks. The pull request leads with measured cost, then states every result
registered inside the wall with its rungs and its significance in the rubric’s own
words, then why each other scope stopped, what files and interfaces changed, which
defects closed or remain, validation, and the one selected next entry.
The operator alone merges the pull request and confirms or revises Agenda 018 before it
starts.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
