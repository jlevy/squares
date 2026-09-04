---
title: "agenda-018 — ten-hour continuation: certificate ladders, the Trump radius, and W9 wave two"
softschema:
  contract: packing.squares:ExperimentAgenda/v1
  schema: ../schemas/agenda.schema.yaml
  envelope: agenda
  status: enforced
agenda:
  id: agenda-018
  title: Ten-Hour Continuation — Certificate Ladders, the Trump Radius, and W9 Wave Two
  updated: '2026-09-04'
  status: paused
  objective: >-
    Run one ten-hour autonomous block after the operator has reviewed Agenda 017's pull
    request, carrying the operator's confirmed or revised lane order. Four disjoint
    lanes open after a thirty-minute preflight that registers every ladder hypothesis
    before a target command runs. Lane A climbs the n = 12 certificate ladder at the
    next fixed rung, takes the n = 11 shot -- a fractional certificate with total mass
    strictly below eleven at a side strictly above 2 + 4/sqrt(5), which would be the
    first movement on the central open case since 2003 -- and then sweeps the generator
    over Nagamochi-only sizes as a bound family. Lane B reviews Agenda 017's Theorem 3 audit, generalises the local-rigidity
    instrument to arbitrary poses and proves an explicit isolation radius at Trump's
    n = 11 packing, the quantitative theorem H-022 asks for, with its exact constants
    as V4 fragments and the compound at V3, as T-014 is registered. Lane C runs
    H-049's construction round at the bar its corrected framing sets and, if time
    remains, builds the generic interval certifier. Lane D runs W9 wave two over the
    clauses Agenda 017 deferred and over D-426, D-427 and D-428, spikes the one unargued
    sentence under sixty open lower bounds, and measures the gate's slowest step. The
    research wall is 480 elapsed minutes; the final 120 are reserved for W10
    disposition, documentation review, validation, publication and replanning.
  items:
  - id: BC-170
    purpose: tool_validation
    owner_focus: process
    instances: [11, 12, 20, 21, 26, 30, 39, 40, 90]
    state: blocked
    priority: 0
    question: >-
      Can Agenda 017's terminal handoff, the operator's review, the frozen generator and
      instrument, the ladder registrations and the fresh output paths all be frozen and
      readmitted before any target work begins?
    hypotheses: [H-061]
    budget: >-
      30 elapsed minutes. 0--8 record the wall start, allocate the coordinator session
      and arm the recurring continuity trigger; read the operator's review of Agenda
      017's pull request and record its input as confirmed, revised or unavailable, and
      apply any reordering before dispatch. 8--18 register the ladder hypotheses from
      Agenda 017's outcomes, each with its side fixed before any target command: H-062
      at the next rung of the declared n = 12 ladder above the side BC-161 certified
      (383/100, then 77/20, then 97/25, 39/10 and 79/20), or a refined atom grid at
      19/5 under a new registration if BC-161 closed as a bounded negative for its
      grid, and none at all if BC-161 produced an exact ceiling at 19/5; H-063 for the
      n = 11 shot, total mass strictly below eleven at a fixed side strictly above
      2 + 4/sqrt(5) -- 379/100 by default, with at least 1800 directions so the shrink
      loss stays below the gap, and only after its diagnostic; and H-064 for the bound
      family, first the n = 13 probe at 399/100 and at 4, then n = 20 at 19/4. Before
      dispatch, rewrite BC-171, BC-172 and BC-173's hypotheses lists from the H-061
      placeholder they carry in this planning revision to H-062, H-063 and H-064, so the
      ledger files each round under the claim it tests; and take X-013's Theorem A
      induction as a fallback-card replay, since nothing else reviews it before BC-175
      consumes it. 18--26 verify the toolchain
      exactly as BC-159 did -- tbd under Node 22, a non-shallow clone, the records
      tier -- and freeze by hash the generator and verifier at Agenda 017's terminal
      revision, X-013 and the n = 40 tool, cases/trump11 and exp-013's certificates,
      H-049's amended record, runner.py and its tests, and run_negative_controls.py.
      26--30 freeze the launch packet with lanes, models, reviewer rotation, output
      paths, safe commands, the concurrency cap of four sub-agents sustained with
      reviewers replacing writers, and typed stop rules; refuse dispatch on any drift.
    entry: >-
      Agenda 017 is complete with its closeout published and its pull request reviewed
      by the operator or, if the operator is unavailable at the wall, the declared
      fallback applies: Agenda 017's ranked candidates stand in the order its closeout
      recorded. H-061's determination is terminal, the generator is frozen at a named
      revision, and this agenda's beads exist on tbd-sync.
    exit: >-
      One launch packet; H-062, H-063 and H-064 registered with fixed sides; every
      frozen input hashed; the continuity trigger armed; and no target command run.
    bead: think-2r1q
    depends_on: []
    blocked_on: >-
      Agenda 017's W10 closeout (BC-169) and the operator's review of its pull request;
      this agenda is paused until both have happened or the declared fallback applies.
    parallel_group: agenda018-coordinator
    workflows: [process-review]
    next_evidence: >-
      A passed packet opens BC-171, BC-175, BC-178 and BC-179 concurrently, staggered
      by ten minutes. On any refusal the coordinator runs no target, marks every
      downstream commitment never-opened with the reason, and opens BC-182.
  - id: BC-171
    purpose: research
    owner_focus: insight
    instances: [12]
    state: blocked
    priority: 0
    question: >-
      Does the frozen generator certify s(12) at the next fixed rung of the ladder
      above Agenda 017's certified side?
    hypotheses: [H-061]
    budget: >-
      120 elapsed minutes, Opus at maximum thinking, in the Lane A writer. 0--15 replay
      the frozen instrument's controls and Agenda 017's certificate from a clean root.
      15--95 run the generator at n = 12 and H-062's registered side with 720
      directions -- generate on 181, verify on 720, add the new directions' violated
      cells and re-solve -- growing the atom grid by column generation until the
      verifier accepts a rationalised certificate, the restricted optimum reaches the
      kill line, or the converged dual yields an exact ceiling. 95--120 freeze the
      experiment record with certificate bytes, hashes, direction list, per-direction
      minima, the V(G, K) ladder and receipts under normal and -O Python. The side does
      not move after results are seen; the round closes needs_review true.
    entry: >-
      BC-170 passed and H-062 is registered with instrument_ready true at the frozen
      revision; a fresh experiment is allocated with fresh paths.
    exit: >-
      A terminal experiment with an exact certificate the frozen verifier accepts at the
      registered side, or the first typed stop with retained LP state and an explicit
      canonical-result absence.
    bead: think-k6if
    depends_on: [BC-170]
    parallel_group: agenda018-lane-a
    workflows: [research-loop]
    next_evidence: >-
      BC-174 reviews the outcome. The writer proceeds to BC-172 whatever it was; a
      failure at this rung caps the ladder for the agenda and is reported as such.
  - id: BC-172
    purpose: research
    owner_focus: insight
    instances: [11]
    state: blocked
    priority: 0
    question: >-
      Does the frozen generator certify a measure of total mass strictly below eleven
      at a side strictly above 2 + 4/sqrt(5), improving the s(11) lower bound for the
      first time since Stromquist 2003?
    hypotheses: [H-061]
    budget: >-
      150 elapsed minutes, Opus at maximum thinking, in the Lane A writer after
      BC-171. 0--40 the diagnostic the survey requires first: the generator at n = 11 at a side
      whose effective unit-square side L/B lies below 2 + 4/sqrt(5) by at least 1/200
      -- 189/50 at B = 99975/100000 gives 3.780945 -- must reach a restricted optimum at
      or below 11 - 1/500, because a certificate above the inherited side needs a
      measure Stromquist's argument does not supply and the generator has to show it
      can find one below it; a failure is a bounded negative for that grid, and only a
      ceiling certificate in H-061's form at that side closes the lane, since the
      piercing value is monotone in the side. 40--120 on a passed diagnostic,
      run at H-063's registered side with at least 1800 directions, growing the grid
      until the verifier accepts a certificate, the kill line is reached, or the dual
      yields a ceiling; retain the LP's best objective at every refinement. 120--150
      freeze the record. A certificate here is the central result of the program to
      date and is presented as such only after BC-174's independent pass.
    entry: >-
      BC-171 is terminal and H-063 is registered with its fixed side.
    exit: >-
      A terminal experiment with an exact certificate at the registered side and mass
      below eleven, or a bounded negative for the declared grid and pose set with the
      best objective retained, or the first typed stop.
    bead: think-bj0s
    depends_on: [BC-170]
    parallel_group: agenda018-lane-a
    workflows: [research-loop]
    next_evidence: >-
      BC-174 reviews the outcome; on a pass the n = 11 verified lower bound moves, and
      the n = 12 bound moves only if the certified side exceeds the rung Agenda 017
      certified there, since a mass below eleven serves both.
  - id: BC-173
    purpose: research
    owner_focus: insight
    instances: [13, 20, 21]
    state: blocked
    priority: 1
    question: >-
      Does the generator reproduce Bentz's proved s(13) = 4 fractionally or meet a
      certified ceiling below it, and then certify a lower bound strictly above
      Nagamochi's closed form at n = 20, so that the technique is a bound family rather
      than one case?
    hypotheses: [H-061]
    budget: >-
      150 elapsed minutes, Opus at maximum thinking, in the Lane A writer after BC-172,
      conditional on the generator's measured cost per size.
      SUPERSEDED IN PART on 2026-09-04, before this agenda ran. The n = 13 probe was
      planned as 0--50: n = 13 at 399/100 and at 4, on the reading that a restricted
      value at or above 13 at 399/100 would be either grid coarseness or a genuine
      fractional ceiling, distinguishable only by a ceiling certificate at B = 1, and
      that a value below 13 at side 4 would be a machine-checked fractional reproof of
      s(13) = 4. That question is now settled analytically and the fifty minutes are
      free. A certificate cannot exist above ceil(sqrt(n)) * B, since a wider container
      holds ceil(sqrt(n))^2 pairwise disjoint axis-parallel B-squares whose masses
      **Condition 5**
      forces past n; for n = 13 that ceiling is 4B = 3.9908, below the case's own lower
      bound of 4. So the probe at 399/100 can only report the ceiling it is looking for,
      and the hoped-for second outcome is impossible outright: at side 4 the refuting
      grid forces mass to sixteen, so no fractional reproof of s(13) = 4 exists at any
      net. See frontier/CERTIFICATE-REACH.md, which does this for all 100 cases.
      50--150 n = 20 at H-064's fixed side
      above 1 + sqrt(13), where the n = 17 calibration suggests a certificate near
      4.75 to 4.85 against a gap of 0.4; the survey sized generation at half an hour
      to five hours on four cores, so a round that does not close is time-limited and
      continues in the next agenda. n = 21 opens only if n = 20 closes early; n = 26
      onward are two lanes each and wait.
      The reach table also reorders what waits. n = 26 onward are not the tail of this
      lane but its largest prizes: eleven cases above +0.49, headed by n = 51 at
      +0.5364, against +0.0671 at n = 11 and +0.0955 at n = 17. Whether the covering
      value permits any of it is unmeasured -- four restricted optima are the whole of
      what is known -- and measuring one is the first thing the successor agenda should
      buy with the fifty minutes this correction returns.
    entry: >-
      BC-172 is terminal, H-064 is registered, and the generator's per-size cost from
      the n = 12 and n = 11 rounds fits the budget.
    exit: >-
      Up to three terminal experiments, each with an exact certificate at its
      registered side or a typed stop.
    bead: think-flk4
    depends_on: [BC-170]
    parallel_group: agenda018-lane-a
    workflows: [research-loop]
    next_evidence: >-
      BC-174 reviews each; three passes make the S4 bound-family claim reviewable at the
      closeout, and fewer are reported as the case results they are.
  - id: BC-174
    purpose: measurement_validation
    owner_focus: correctness
    instances: [11, 12, 13, 20, 21]
    state: blocked
    priority: 0
    question: >-
      Does an independent Max reviewer reproduce every Lane A certificate and its
      admission boundary, and what may each be registered as?
    hypotheses: [H-061]
    budget: >-
      90 elapsed minutes in total, Fable at maximum thinking, by a reviewer with no
      Lane A authorship, taken in three sittings as each round freezes: 30 minutes
      after BC-171, 30 after BC-172 and 30 after BC-173. Each sitting replays the
      certificate from a clean root under normal and -O Python, re-derives the decision
      from the emitted bytes with the from-scratch evaluator BC-162 wrote, and audits
      strictness and the direction lemma; on an exact pass it registers the result at
      V4/C3 with its novelty basis and significance reasoning written down, moves the
      verified lower bound and regenerates consumers. The n = 11 sitting additionally
      re-derives the whole lemma chain by hand before anything moves, because the
      claim is the program's central result if it holds.
    entry: >-
      The round under review is terminal and its writer has stopped.
    exit: >-
      One immutable determination per round and either registered results with every
      consumer current or no frontier change and a named follow-up per round.
    bead: think-p2t5
    depends_on: [BC-171, BC-172, BC-173]
    parallel_group: agenda018-review-a
    workflows: [factual-review]
    next_evidence: >-
      BC-182 presents every registered result with its significance in the synopsis
      headline and above the pull request's dispositions.
  - id: BC-175
    purpose: tool_validation
    owner_focus: correctness
    instances: [3, 5, 10, 11, 40]
    state: blocked
    priority: 1
    question: >-
      Can sqpack.local_rigidity be generalised from the n = 5 shape to arbitrary poses
      -- multi-branch contacts, twin rows kept distinct and enveloped, a chart that
      builds in minutes at 120 variables and over a degree-8 field -- with controls that
      can fail, before any theorem is attempted on it?
    hypotheses: []
    budget: >-
      240 elapsed minutes, Opus at maximum thinking. 0--60 a multi-branch pair report
      carrying every zero-margin branch and its zero corners in place of the
      DisjunctiveTouchError refusal, and the branchwise neighbourhood X-013 states.
      60--120 per-branch first- and second-order data with the two host-side versions
      of a flush or corner contact kept distinct and enveloped, never intersected, and
      the uniform-stress check as an LP proposal verified by exact LDL. 120--180
      performance: sparse polynomial keys or per-pair sub-arity polynomials and
      bucketed feasibility so the n = 40 book builds under ten minutes and the n = 11
      chart over Q(u) evaluates exactly. 180--225 controls: Control 9, the exact n = 10 pose,
      whose axis and diagonal slides the probe must exhibit and the stress test must
      report unrefused; Control 10, the exact n = 3 side-2 family, which must not certify
      isolation; Control 11, the n = 5 known answer, reproducing T-014's counts, rows, jets and
      all eight control verdicts through the generalised path; Control 12, Trump's 128 zero
      branch cones as exp-013 found them. 225--240 freeze at a target-blind readiness
      review by the Lane D reviewer. Kill: a chart book over ten minutes, or a control
      that cannot fail.
    entry: >-
      BC-170 passed; X-013 and the n = 40 tool are frozen by hash; the lane writes only
      the package, its tests and its scratch directory.
    exit: >-
      A frozen generalised instrument with all four controls passing and a readiness
      review naming no blocking caveat, or the first typed stop naming what still
      refuses.
    bead: think-ppg1
    depends_on: [BC-170]
    parallel_group: agenda018-lane-b
    workflows: [pipeline-improvement, factual-review]
    next_evidence: >-
      A passed readiness review opens BC-176 on the same lane's Fable agent; a caveat
      keeps BC-176 never-opened and reports the instrument's state as it stands.
  - id: BC-176
    purpose: research
    owner_focus: insight
    instances: [11]
    state: blocked
    priority: 1
    question: >-
      Does first-order rigidity in every branch at Trump's n = 11 packing yield an
      explicit chart-distance radius within which the labeled pose is the only
      fixed-side packing, and hence within which no packing fits a smaller container?
    hypotheses: [H-022]
    budget: >-
      195 elapsed minutes, Fable at maximum thinking, on the frozen instrument. 0--45
      the complete accounting of the 176 wall and 1,760 pair elementary functions in
      the half-angle chart over Q(u), the strict conditions that define the
      neighbourhood, and the confirmation that every one of the 128 derivative-distinct
      branch cones is zero with a strictly positive stress. 45--120 the bound: Taylor
      remainder bounds on every cleared polynomial from coefficient sums, the exact left
      inverse of each branch's pivot rows, and the radius on which every strict
      condition keeps its sign against the exact base margins, combined into one exact
      rational lower bound on the isolation radius. 120--165 controls: the n = 5 known
      answer must reproduce T-014's counts and give a positive radius; a pose displaced
      by more than the radius must not be refused by the bound alone. 165--195 the
      proof packet with its claim boundary: fixed side, labeled pose, a lower bound on
      the chart-distance radius in the named chart, the side-stability clause with its
      one-line embedding argument (a packing of side s' < s embedded in [0, s]^2 is a
      feasible pose at side s, and if any translate lies within the radius of the pose
      it is the pose, which touches all four walls); no optimality, no uniqueness, no
      global statement; V4 fragments and a V3 compound, as T-014, unless the ball is
      swept by interval arithmetic. A partial packet at
      the wall is time-limited and continues.
    entry: >-
      BC-175's readiness review passed; exp-013's certificates and cases/trump11 are
      frozen by hash.
    exit: >-
      A review-pending packet with replayable receipts and an exact rational radius, or
      the first typed proof gap, guard refusal, technical failure or time-limited stop.
    bead: think-fikx
    depends_on: [BC-175]
    parallel_group: agenda018-lane-b
    workflows: [research-loop]
    next_evidence: >-
      BC-177 reviews the packet; only an exact pass registers the radius as a result
      and moves H-022. BC-183 opens only if this block closes early.
  - id: BC-177
    purpose: measurement_validation
    owner_focus: correctness
    instances: [11]
    state: blocked
    priority: 1
    question: >-
      Does an independent reviewer reproduce the Trump radius packet and accept every
      bound, and what may it be registered as?
    hypotheses: []
    budget: >-
      60 elapsed minutes, Fable at maximum thinking, by a reviewer with no Lane B
      authorship. Replay the accounting and every bound from clean roots under normal
      and -O Python; re-derive the radius argument by hand for one branch and check
      the exact left inverse; audit the strict-condition radius against the base
      margins; on an exact pass register the next-free T-result at V4/C3 with H-022's
      radius and side-stability clauses at their honest scope, update the n = 11 case
      and its consumers, and score significance with the reasoning written down;
      otherwise no frontier change and a named follow-up.
    entry: >-
      BC-176 is terminal and its writer has stopped.
    exit: >-
      One immutable determination and either a registered result with every consumer
      current or no frontier change and a named follow-up.
    bead: think-ljdy
    depends_on: [BC-176]
    parallel_group: agenda018-review-b
    workflows: [factual-review]
    next_evidence: >-
      BC-182 presents the result with its significance; the S4 technique claim waits
      for a disjunctive instance and is not made on n = 5 and n = 11 alone.
  - id: BC-178
    purpose: research
    owner_focus: insight
    instances: [30, 90]
    state: blocked
    priority: 1
    question: >-
      Do twenty unit squares pack squeezably in a 4 by 6 rectangle within a declared
      structure class -- which by Arslanov's inequality would also pack thirty below
      side six -- and if so does the certified squeeze survive every control?
    hypotheses: [H-049]
    budget: >-
      240 elapsed minutes, Opus at maximum thinking. 0--25 read Arslanov, Mustafin and
      Shangitbayev first-hand, re-derive the assembly and inequality (2), and confirm
      H-049's amended record states the s(30) < 6 implication before measuring. 25--55
      build the squeeze instrument: the zero-code encoding that fixes the ten grid
      squares of a 2 x 5 block inside a square container of side 6 - delta, or the
      delta column in fixed_cell_lp. 55--85 controls first: the (4, 8)/26 primitive
      certifies at delta = 0.0177702 and refuses at 0.02; delta = 0.42 refuses; the
      4 x 5 grid at delta = 0 certifies; kill the round here if any control fails.
      85--105 declare and freeze the structure class with its parameter ranges.
      105--200 enumerate and measure, retaining every candidate's squeeze; take any
      delta above 1e-8 to exact or interval certification and pad it to thirty squares
      in (6 - delta)^2 as the cross-check, and state that a negative is at the 1e-8
      screening resolution above the regime's 1e-11 floor. 200--225 freeze the experiment: a certified
      squeeze, a bounded negative with the per-candidate table, or a typed stop.
      225--240 write the claim boundary and hand to the reviewer.
    entry: >-
      BC-170 passed; H-049's amended record and Arslanov's paper are frozen by hash;
      the lane writes only its case directory, tests, experiment and scratch directory.
    exit: >-
      A terminal experiment with a certified squeezable primitive and the assembled
      sides at n = 30 and n = 90 exactly, or a bounded negative over the declared class,
      or a tooling stop with the instrument retained.
    bead: think-nh1s
    depends_on: [BC-170]
    parallel_group: agenda018-lane-c
    workflows: [research-loop]
    next_evidence: >-
      A positive is recorded needs_review and is not registered inside this agenda:
      the operator makes the accept decision on an independent replay taken as a
      fallback card, as H-049's own notes require; a negative closes the declared class
      and opens BC-184 in the same lane.
  - id: BC-179
    purpose: tool_validation
    owner_focus: correctness
    instances: [5, 11, 17]
    state: blocked
    priority: 1
    question: >-
      Can W9 wave two close the two D-044/D-046 units Agenda 017 deferred and the three
      defects Agenda 016 recorded -- D-426, D-427 and D-428 -- with regressions, under
      independent review, without changing a scientific criterion?
    hypotheses: []
    budget: >-
      180 elapsed minutes for the writer, Opus at extra-high thinking, then 45 for a
      reviewer with no W9 authorship, Opus at maximum thinking. 0--40 W9-2: capture
      engine dirtiness before the round's own stub and ledger render so method.dirty is
      no longer unconditionally true, with regressions for a clean tree and a
      dirty tree. 40--110 W9-5: execute digests the archive it produced into its
      receipt and record compares that digest against both the verification receipt
      and the archived bytes, closing the three archive residuals with the three
      regressions the review named. 110--140 D-426: a control-cell breach stops the
      unattended session, with a regression that breaches a control and observes the
      stop. 140--170 D-427: every negative control is scored against a per-command
      unmutated baseline cached across the suite's forty distinct commands, with
      baseline failures reported as their own category, and a control that plants an
      already-red checker and observes the refusal; this changes the scoring rule for
      all 155 controls and needs the full suite run once. 170--180 D-428: tie the
      rebuilt chain spine to carried_boundary in the n = 17 successor validator with
      the altered-manifest regression. The reviewer replays every regression and
      reverts each repair in a copy.
    entry: >-
      BC-170 passed; runner.py, its tests, run_negative_controls.py and the successor
      validator are frozen by hash; the lane writes only those surfaces, their tests,
      the defect records and its scratch directory.
    exit: >-
      Each of the five items exits fixed with regression, contained, rerouted or
      blocked, with the reviewer's determination per item; D-044 and D-046 move to
      fixed only if nothing named in their records remains open.
    bead: think-g4qi
    depends_on: [BC-170]
    parallel_group: agenda018-lane-d
    workflows: [remediation, factual-review]
    next_evidence: >-
      BC-182 records each disposition and regenerates the defect views; BC-180 opens
      on the same lane once the reviewer has the packet.
  - id: BC-180
    purpose: tool_validation
    owner_focus: efficiency
    instances: [5, 11, 17]
    state: blocked
    priority: 2
    question: >-
      Can the gate's slowest step be cut under an equivalence guard, so the pull-request
      tier and the full gate stop paying twenty minutes for one step?
    hypotheses: []
    budget: >-
      90 elapsed minutes, Opus at extra-high thinking, after BC-179's packet is with its
      reviewer. 0--20 baseline the fast behavioral tests step with the existing profile
      -- 1,210.79 s at 1,607 passing tests in Agenda 016's closeout measurement -- and name
      the two most expensive test modules.
      20--75 cut wall time in those modules under an equivalence guard (identical test
      selection and outcomes, no correctness check touched), measuring before and
      after. 75--90 record the delta or the rejection, and the guard, in the
      efficiency record.
    entry: >-
      BC-179's packet is with its reviewer.
    exit: >-
      A measured delta with its guard, or a recorded rejection with the reason.
    bead: think-jzqi
    depends_on: [BC-179]
    parallel_group: agenda018-lane-d
    workflows: [efficiency-loop]
    next_evidence: >-
      BC-182 reports the measurement; a cut that survives the full gate lands, one that
      does not is retained as a measured rejection.
  - id: BC-181
    purpose: measurement_validation
    owner_focus: correctness
    instances: [20, 26, 30, 40, 50, 61, 78, 97]
    state: blocked
    priority: 1
    question: >-
      Does the one unargued sentence in Nagamochi 2005's Lemma 1 proof -- that lambda
      may be taken as 1 to estimate the minimum -- hold exactly, given that sixty open
      cases rest on it?
    hypotheses: []
    budget: >-
      120 elapsed minutes, Fable at maximum thinking, in Lane D between BC-179's
      handoff and BC-180. 0--30 isolate the claim from the retained extraction: a
      monotonicity statement about the mass a lambda-by-lambda square captures as
      lambda varies on [1, 1.01], across the seven cases of the proof. 30--90 prove or
      refute it exactly per case, with a planted non-monotone configuration that
      the check must refuse. 90--120 record the outcome as a separate evidence entry
      for the sub-lemma on the E-bentz13-figure2-audit precedent, review-pending until
      a reviewer with no spike authorship replays the case analysis and the planted
      non-monotone control, with nothing citing the entry before that; T-007 stays at
      its composition minimum either way. A refutation is a
      defect against the published record and a frontier-wide caveat, never a bound
      change inside this block.
    entry: >-
      BC-179's packet is with its reviewer; the Nagamochi 2005 extraction is frozen by
      hash.
    exit: >-
      An evidence entry that proves or refutes the sub-lemma exactly with its control,
      or a typed stop naming the smallest unresolved case.
    bead: think-8y1g
    depends_on: [BC-170]
    parallel_group: agenda018-lane-d
    workflows: [factual-review]
    next_evidence: >-
      BC-182 reports the determination; a refutation routes to W2 on every case that
      cites the record before any bound is touched.
  - id: BC-182
    purpose: research
    owner_focus: process
    instances: [11, 12, 20, 21, 26, 30, 90]
    state: blocked
    priority: 0
    question: >-
      What did Agenda 018 establish, fail to establish or repair, what significance
      does each registered result carry, why did each incomplete scope stop, and which
      one entry runs next?
    hypotheses: [H-061]
    budget: >-
      120 elapsed minutes reserved from 08:00 through 10:00. 0--15 stop every writer and
      process and freeze evidence. 15--40 add outcome rows to every commitment at the
      smallest honest scope, including the tentative ones as never-opened where they
      did not run. 40--60 regenerate every generated view and reconcile live tbd
      through the CLI. 60--75 review the six root documents with an explicit decision
      each and run the documentation and de-slop pass. 75--90 pass the records and
      push tiers, commit and push so hosted CI starts while the full local gate runs.
      90--105 render the pull-request description leading with cost, then with every
      result scored inside the wall and its significance in the rubric's own words,
      then stop reasons, dispositions, file changes, validation and limitations.
      105--120 rank the retained candidates, record operator input, and select exactly
      one next entry without executing it. Post-wall mechanical closeout continues
      only until green or a typed blocker, reported separately.
    entry: >-
      BC-174, BC-177, BC-178, BC-179, BC-180, BC-181 and BC-185 are terminal, the
      tentative BC-183 and BC-184 are terminal or never-opened, every writer has stopped,
      and
      the coordinator owns the only shared-record, tbd, Git, generated-view and
      pull-request writes.
    exit: >-
      Agenda 018 and its sessions terminal; every attempted scope with an outcome, stop
      reason, evidence, disposition and follow-up; every document with an explicit
      decision; the required tiers passing or the exact blocker recorded; the pull
      request leading with cost and then with each result and its significance; tbd
      synchronized; and exactly one unexecuted next entry published.
    bead: think-tfwa
    depends_on: [BC-174, BC-177, BC-178, BC-179, BC-180, BC-181, BC-185]
    parallel_group: agenda018-closeout
    workflows: [review-planning-oversight, documentation-pass, process-review]
    next_evidence: >-
      The selected entry becomes the only handoff; a new agenda may be drafted after
      operator confirmation or the declared fallback and does not begin inside this
      closeout.
  - id: BC-185
    purpose: measurement_validation
    owner_focus: correctness
    instances: [11]
    state: blocked
    priority: 1
    question: >-
      Does an independent reviewer reproduce Agenda 017's Stromquist Theorem 3
      determination -- the certificate as printed, or the exact escape and any repair --
      and what may it be registered as?
    hypotheses: []
    budget: >-
      60 elapsed minutes, Fable at maximum thinking, in the Lane B Fable agent's free
      hour from 00:30 while BC-175 builds; the reviewer authored no part of BC-164. On a
      certificate as printed: replay the cover from a clean root, re-derive Lemmas 7
      and 8 for the two orientations, and on a pass register the next-free T-result at
      V4/C3, previously-published, as the third machine-audited published proof here,
      scoring significance with the reasoning written down. On an exact escape: replay
      the escape certificate against the transcribed points and, if a source-distinct
      repair was found, replay it and register on the T-010 precedent with the erratum
      recorded; if no repair exists, register the refutation as a citable detail and
      leave Theorem 3 as printed unproved here. On a typed stop: confirm the retained
      state replays and record BC-164 as continue.
    entry: >-
      BC-170 passed and BC-164 is terminal with a frozen packet; if BC-164 was
      never-opened or produced nothing to review, this block records never-opened and
      the hour returns to BC-175's readiness support.
    exit: >-
      One immutable determination and either a registered result with every consumer
      current or no frontier change and a named follow-up.
    bead: think-7vi7
    depends_on: [BC-170]
    parallel_group: agenda018-lane-b
    workflows: [factual-review]
    next_evidence: >-
      BC-182 presents any registered result with its significance; a certified
      Theorem 3 makes H-036's neighbourhood theorem a candidate for a later agenda.
  - id: BC-183
    purpose: research
    owner_focus: insight
    instances: [40]
    state: tentative
    priority: 2
    question: >-
      Can the n = 40 admissible cone be characterised on the disjunctive system, so that
      Goebel's n = 40 packing's fixed-side local rigidity follows from X-013's theorem
      rather than standing as a conditional statement?
    hypotheses: []
    budget: >-
      Up to 180 elapsed minutes, Fable at maximum thinking, only if BC-176 closes early
      or the operator reorders. Pin the thirty-nine uncertified functionals on the
      disjunctive cone by branch-and-bound over the forty-two axis choices, each leaf's
      Farkas certificate verified in the field and the certificate tree retained; kill
      at more than 1e5 leaves or fewer than thirty of thirty-nine pinned at three hours,
      and then record the conditional theorem -- if the admissible cone lies in the
      known six-dimensional span then the pose is isolated at fixed side -- rather than
      a claim. A new admissible direction is a T-013 strengthening in its own right; an
      unrefused one is a candidate motion that reroutes the lane to nonlinear
      continuation.
    entry: >-
      BC-175's instrument is frozen, BC-176 has closed with time remaining, and the
      coordinator assigns the block explicitly.
    exit: >-
      A certificate tree that pins the cone, or the conditional theorem with its
      obligation list, or a typed stop.
    bead: think-3yxk
    depends_on: [BC-175]
    parallel_group: agenda018-lane-b
    workflows: [research-loop]
    next_evidence: >-
      A pinned cone makes the n = 40 theorem the next Lane B target; a conditional
      theorem is retained as the smallest unresolved obligation.
  - id: BC-184
    purpose: tool_validation
    owner_focus: efficiency
    instances: [11, 17, 29, 37, 39]
    state: tentative
    priority: 2
    question: >-
      Can the generic interval certifier be wired end to end and reproduce T-009's
      n = 29 bound through the generic path, before attempting a first new interval
      certificate at n = 37 and then n = 39?
    hypotheses: [H-056]
    budget: >-
      Up to 180 elapsed minutes, Opus at maximum thinking, after BC-178 closes at 04:30,
      so that Lane C freezes at 07:30 with the others. 0--45
      freeze the calibration: n = 11 reproduces 14 pair and 20 wall contacts, n = 29
      reproduces 52 and 37, n = 17 assembles to full rank with zero side leak. 45--150
      build the two missing joins -- rank-revealing square-subsystem selection for
      refine and a policy that freezes rattlers at rational coordinates -- and wire
      --strategy interval-existence. 150--210 reproduce T-009's bound through the
      generic path within 1e-19 of the bespoke one; only then attempt n = 37. Kill if
      the generic path cannot reproduce n = 29 by minute 150; n = 39 waits for a later
      agenda. The claim is the
      technique; the bounds are already held by Agenda 017's rational certificates.
    entry: >-
      BC-178 is terminal and the coordinator assigns the block explicitly.
    exit: >-
      The generic path reproducing n = 29, or a typed stop with the instrument
      retained; any new certificate is review-pending.
    bead: think-4f4d
    depends_on: [BC-178]
    parallel_group: agenda018-lane-c
    workflows: [pipeline-improvement]
    next_evidence: >-
      A reproduced n = 29 makes H-056 instrument-ready; the S4 technique claim waits
      for an independent review in a later agenda.
---
# Agenda 018 — Ten-Hour Continuation: Certificate Ladders, the Trump Radius, and W9 Wave Two

## Workflow Entry Point

This agenda is paused.
It becomes active when
[Agenda 017](agenda-017-six-hour-generator-rigidity-ceilings-and-w9-block.md) has closed
through W10 and the operator has reviewed its pull request, and its lane order carries
whatever that review confirms or revises.
If the operator is unavailable at the wall, `OR-11`’s fallback applies: Agenda 017’s
closeout ranking stands as recorded and this agenda begins on it without inventing a new
criterion.

Begin at `BC-170`. The coordinator declares `process-review` for the preflight, creates
the coordinator session before dispatch, registers the ladder hypotheses with their
sides fixed, freezes the wall, and then holds `research-loop` for the lanes and
`review-planning-oversight` for the closeout.
`BC-170` opens four disjoint lanes: `BC-171` through `BC-173` in Lane A; `BC-175` in
Lane B’s Opus agent while its Fable agent reviews Agenda 017’s Theorem 3 audit in
`BC-185` and then takes `BC-176`; `BC-178` in Lane C; and `BC-179`, `BC-181` and
`BC-180` in Lane D. `BC-183` and `BC-184` are tentative and open only on the
coordinator’s explicit assignment when a lane closes early.

**Model assignment**, under `OR-2` and `OR-10`: Claude Fable at maximum thinking for the
Trump radius proof, the Nagamochi spike, the `n = 40` cone if it opens, and every
independent review of a scientific result; Claude Opus at maximum thinking for the Lane
A rounds, the instrument generalisation, the `H-049` round and the W9 reviewer; Claude
Opus at extra-high thinking for the W9 writer, the gate measurement and mechanical
integration.

## Why These Lanes Are Next

**Lane A climbs, then takes the shot.** Agenda 017 built the generator and fixed the
first rung; this block moves the rung and then aims the same instrument at `n = 11`,
where a measure of total mass below eleven at any side above `2 + 4/√5` would be the
first improvement to the lower bound of the problem’s motivating case since 2003. The
survey’s reading makes the shot honest: a certificate above the inherited side needs a
measure Stromquist’s argument does not supply, and the shrink that a finite direction
net costs must stay below the gap, which is why the `n = 11` round runs a diagnostic at
an effective side strictly below the inherited one first and uses at least 1,800
directions.
The family sweep opens with a calibration against a proved theorem — `n = 13`
at side `4`, where a fractional value below thirteen would be a machine-checked reproof
of Bentz’s `s(13) = 4` — and then `n = 20`, the best return per lane after `n = 12`; it
is the `S4` claim under the rubric and is worth its budget only at the per-size cost the
earlier rounds measure.

**Lane B proves the theorem the survey found easier.** The planning survey established
that an explicit isolation radius at Trump’s packing needs no curve selection: with
every branch cone zero and a strictly positive stress in each, Taylor remainder bounds
and an exact left inverse give a radius directly, every step exact or interval, so the
result is reachable at `V4` where `T-014` sits at `V3`. That is `H-022`’s radius and
side-stability clause, at the famous case, on the instrument that the same lane
generalises first; the closing Taylor-remainder step is a proof, so the compound sits at
`V3` with `V4` fragments unless the ball is swept by interval arithmetic.
The `n = 40` theorem stays behind it because its real obligation — characterising the
admissible cone on the disjunctive system, the lesson of `D-391` — was priced at three
hours with a coin-flip chance of pinning enough functionals, and a conditional theorem
is the honest fallback.

**Lane C runs the long shot at the right bar.** `H-049`’s positive would settle
`s(30) < 6` as well as `s(90) < 10`, and that is why it is reviewed at that bar and why
the prior is small; the instrument it needs — a squeeze in a rectangle — is built in the
first hour with Arslanov’s own two-sided calibration as the gate.
If the round closes negative over its declared class, the same lane turns to the generic
interval certifier, whose value is the technique rather than any bound.

**Lane D finishes the wave and buys assurance.** W9 wave two closes the two `D-044` and
`D-046` units the six-hour block could not fit, and the three defects Agenda 016
recorded about its own run.
Between the wave and the gate measurement, a Fable spike attacks the single unargued
sentence in Nagamochi’s Lemma 1 proof, which the survey rated the best assurance
purchase per hour in the register: sixty open cases carry that lemma as their verified
lower bound.

## Exact Wall and Reviewer Rotation

| Elapsed | Coordinator | Lane A (ladders) | Lane B (instrument, radius) | Lane C (`H-049`, certifier) | Lane D (W9, spike, gate) |
| --- | --- | --- | --- | --- | --- |
| 00:00--00:30 | `BC-170` preflight, registrations, dispatch | read-only design from 00:10 | read-only | read-only | inventory snapshot |
| 00:30--02:30 | observe, integrate only frozen packets | `BC-171` ladder round | `BC-175` generalisation; `BC-185` Theorem 3 review 00:30--01:30 in the Fable agent | `BC-178` instrument, controls, class | `BC-179` writer |
| 02:30--05:00 | first review sitting at 02:30 | `BC-172` diagnostic, then the `n = 11` shot | `BC-175` continues; readiness review at 04:30 | `BC-178` enumeration, freezes at 04:30 | writer to 03:30; reviewer 03:30--04:15; `BC-181` spike 04:15--06:15 |
| 05:00--07:30 | second review sitting at 05:00 | `BC-173` calibration, then `n = 20` | `BC-176` radius from 04:45 | `BC-184` if assigned | `BC-180` gate 06:15--07:45 |
| 07:30--08:00 | third review sitting | freeze | `BC-176` freezes by 08:00; `BC-177` in the closeout window | freeze | freeze |
| 08:00--10:00 | `BC-182` W10 closeout with all lanes | closeout support | closeout support | closeout support | closeout support |

Concurrency is four sustained, one agent per lane with a reviewer replacing its lane’s
writer rather than adding to it, plus a brief fifth five times: `BC-185`’s hour at
00:30--01:30 beside `BC-175`, the three Lane A review sittings of thirty minutes at
02:30, 05:00 and 07:30, which overlap the Lane A writer’s next round by design so the
ladder does not wait on its reviews, and the readiness review at 04:30. Dispatch is
staggered by ten minutes.
On the first rate-limit signal the coordinator pauses Lane C until another lane hands
off, and no agent blocks on a gate or poll for more than 120 seconds.

## Routing Rules

1. Every ladder side is fixed at `BC-170` and never moves afterwards; a certificate at a
   lower side is a typed result about the generator.
2. `BC-174` reviews every Lane A round in its own sitting.
   Only an exact pass registers a result; the `n = 11` sitting re-derives the whole
   lemma chain by hand first.
3. `BC-176` opens only on `BC-175`’s readiness pass, and `BC-177` may run inside the
   closeout window, but registration must be complete before the pull request is
   rendered or the result is reported review-pending.
4. A positive in `BC-178` is reviewed at the `s(30) < 6` bar by a Fable reviewer before
   anything is registered; a negative closes the declared class only.
5. `BC-183` and `BC-184` open only on the coordinator’s explicit assignment, never as an
   undeclared fifth lane.
6. `BC-182` starts at 08:00 even when a lane used less than its allocation.
7. Every result registered inside the wall is presented with its rungs and the rubric’s
   wording in the synopsis headline and above the pull request’s dispositions.

## Stop and Outcome Rules

A lane stops on frozen-input drift, a known-answer or mutation failure, a missing
independent verifier, an invalid theorem transfer, three consecutive execution or
persistence failures, or the research wall.
It records the first applicable W10 classification: never-opened, guard-refused,
technical-failure, time-limited, then achieved, bounded-negative or inconclusive under
the frozen criterion.
A bounded negative in Lane A names the atom grid and pose set it exhausted and never a
ceiling on the method.
A partial radius packet is time-limited and continues.
A W9 repair is engineering work and never a scientific result.
Every terminal scope receives one disposition, and continue, fix-and-rerun and defer
always name a live bead.

## Time and Cost Accounting

The closeout reports four clocks without collapsing them: the exact 600-minute wall from
`BC-170`’s start marker to the research stop; per-lane intervals, which overlap;
recursive agent-active and command time from retained receipts; and post-wall mechanical
time separately. `BC-182` closes every session before rendering the cost block and then
reports results with their significance, stop reasons, dispositions and file changes.

## Ranked Portfolio Outside the Wall

| Rank | Candidate | Disposition before Agenda 018 |
| ---: | --- | --- |
| 1 | The `n = 12` ladder and the `n = 11` shot | Execute in Lane A |
| 2 | The generalised rigidity instrument and the Trump radius | Execute in Lane B |
| 3 | W9 wave two and the Nagamochi spike | Execute in Lane D |
| 4 | `H-049` at the `s(30) < 6` bar | Execute in Lane C |
| 5 | The bound-family sweep | Execute in Lane A if the per-size cost allows |
| 6 | The generic interval certifier | Tentative in Lane C |
| 7 | The `n = 40` cone characterisation | Tentative in Lane B |
| 8 | Bentz 2010 Theorem 9 audit (`think-1o1f`), Green17 ceiling (`think-iye2`) | Retain for a later agenda |

`BC-182` reranks this table from actual outcomes and operator input.

## Final Guard

At elapsed 08:00 every research lane begins terminalization and W10 owns the tree.
The coordinator updates the agenda with outcome rows and a closeout block, regenerates
all owned views, applies the documentation and de-slop pass, closes session receipts,
runs the records tier and the required `packing-validate --push` tier, commits and
pushes before the slower full gate finishes, and keeps the pull request current through
hosted checks. The pull request leads with measured cost, then states every result
registered inside the wall with its rungs and significance, then why each other scope
stopped, what changed, which defects closed or remain, validation, and the one selected
next entry. The operator alone merges the pull request.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
