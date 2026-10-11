---
title: "agenda-042 \u2014 overnight n11 settlement ladder and low-n angles after PR 230"
softschema:
  contract: packing.squares:ExperimentAgenda/v1
  schema: ../schemas/agenda.schema.yaml
  envelope: agenda
  status: enforced
agenda:
  id: agenda-042
  title: Overnight n11 Settlement Ladder and Low-n Angles After PR 230
  updated: '2026-10-05'
  status: active
  objective: 'Turn PR 230''s W3 review and the two explorations it led to, X-046 and X-047, into one night
    of bounded work. At n11 no counting certificate can prove equality and Kleddamag''s certificate has
    no side headroom, so the night starts the verified settlement ladder instead: rung 0 of H-112 (Trump
    is globally optimal at its own angle), a quantified capture radius around Trump, and a repaired census
    of minima near U. At low n the additive-ceiling map selects n21 at 4.88 as the one material point-certificate
    rung and n12''s additive ceiling as a decisive negative; the parent-centre clip that would carry both
    further is built as a W7 instrument. At most about three sub-agents run at once: Opus 5.5 builds and
    runs, Fable extra-high does the mathematics and reviews each chunk, and Fable max reviews anything
    that would move a bound.'
  items:
  - id: BC-374
    purpose: research
    owner_focus: insight
    instances:
    - 11
    - 12
    - 17
    - 18
    - 19
    - 20
    - 21
    - 26
    - 29
    state: complete
    priority: 0
    question: Which of PR 230's 31 shaped candidates, and which new directions, could move n11 significantly
      or settle it, and which distinct angles fit the other small cases?
    hypotheses:
    - H-236
    - H-237
    - H-238
    - H-239
    - H-240
    - H-241
    budget: 'Session 156 phases 1 and 2: four reviews of PR 230, a Fable max n11 lane and a Fable extra-high
      low-n lane, then codification, about two hours in all.'
    entry: PR 230 published with a passing hosted checkpoint and no selected entry.
    exit: X-046 and X-047 retained, the selected directions registered as H-236 to H-241, and the commitments
      below given beads and parallel groups.
    bead: think-nbij
    depends_on: []
    next_evidence: docs/project/reviews/review-2026-09-23-pr230-w3-directions.md, X-046 and X-047.
    workflows:
    - insight-iteration
    - review-planning-oversight
    program: n11-settlement
    artifacts:
    - docs/project/reviews/review-2026-09-23-pr230-w3-directions.md
    - packing/campaign/explorations/X-046-n11-settlement-program.md
    - packing/campaign/explorations/X-047-low-n-angles-after-the-parent-core-advance.md
    parallel_group: overnight-planning
    note: 'H-121 (angle merging) is recommended for retirement as a route: X-046 argues it is the conjecture
      restated. That disposition is left to the owner.'
    outcomes:
    - scope: The W3 review and codification of PR 230's directions.
      classification: achieved
      result: No fatal error in PR 230. Settling n11 is verified global optimization with the eleven angles
        as the bottleneck; the first rung is fixed-angle optimality at Trump's angle. Kleddamag's certificate
        carries no transferable slack at U. At low n, additive headroom is about 0.001 at n12, about 0.01
        at n18 to n20 and about 0.036 at n21.
      evidence:
      - docs/project/reviews/review-2026-09-23-pr230-w3-directions.md
      - packing/campaign/explorations/X-046-n11-settlement-program.md
      - packing/campaign/explorations/X-047-low-n-angles-after-the-parent-core-advance.md
      disposition: retire-success
      follow_up: null
  - id: BC-375
    purpose: research
    owner_focus: correctness
    instances:
    - 11
    state: complete
    priority: 1
    question: Does a fixed-shape cell tree with rotational cores and exact leaf certificates prove H-236
      on the half-tangent box of half-width 10^-6 around Trump's tilt, and how many nodes does it need?
    hypotheses:
    - H-236
    budget: Opus extra-high, four to five hours to build and control the driver and its independent reader,
      then at most two hours or 10^6 nodes on the box; Fable extra-high reviews the certificate contract
      in the next chunk.
    entry: X-046's design; exact_lp, the uniform-cell reader and the BC-240 local theorem.
    exit: A certificate accepted by the independent reader with both controls passing, a verified counterexample
      candidate, or an unresolved leaf list with the node count at the declared cap.
    bead: think-ie35
    depends_on: []
    next_evidence: The frozen instrument digests and the run output, admitted from attic/rung0/ into results/agenda-042/.
    workflows:
    - pipeline-improvement
    - research-loop
    program: n11-settlement
    artifacts:
    - packing/campaign/hypotheses/H-236-n11-fixed-angle-global-optimality-at-trump.md
    parallel_group: overnight-n11-a
    note: The node count prices H-112 and every later rung; a bounded negative at the cap is a result
      about the instrument, not about n11.
    outcomes:
    - scope: H-236 on the half-tangent box around Trump's tilt, frozen run and two resumes (exp-231).
      classification: time-limited
      result: 198 of 256 subtrees closed on 1.19e8 nodes with every checked certificate accepted and three
        Trump-degenerate leaves; 58 subtrees remain at the wall cap and no leaf below U appeared. The
        tree is about a thousand times X-046's estimate, so rung 1 needs a stronger relaxation.
      evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-231-h236-rung-zero-cell-tree.md
      - docs/project/reviews/review-2026-09-23-rung0-certificate-contract.md
      disposition: continue
      follow_up: think-ie35
    - scope: H-236, the 58 remaining subtrees and the reader over the complete tree (exp-232).
      classification: achieved
      result: All 256 subtrees closed; the independent reader accepted the whole tree (119,556,859 leaf
        certificates, 19,883,887 branch nodes, three Trump-degenerate leaves, no unresolved leaf). H-236
        is confirmed at its registered scope, pending BC-241 for the local theorem its terminal leaves
        use.
      evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-232-h236-rung-zero-closed.md
      disposition: retire-success
      follow_up: think-6w2y
  - id: BC-376
    purpose: research
    owner_focus: insight
    instances:
    - 11
    state: complete
    priority: 1
    question: Do exp-013's exact stresses and a second-order remainder certify side at least U on a sup-norm
      ball around Trump's pose larger than the BC-240 radius?
    hypotheses:
    - H-237
    budget: Fable extra-high, about four hours.
    entry: The exp-013 tangent-cone record, the BC-240 packet and exact_jets.
    exit: Explicit rational constants with a replayable tool, or a bounded negative naming the binding
      constant.
    bead: think-cj7r
    depends_on: []
    next_evidence: packing/cases/trump11/capture_radius.py and its receipt.
    workflows:
    - research-loop
    program: n11-settlement
    artifacts:
    - packing/campaign/hypotheses/H-237-n11-trump-angular-capture-radius.md
    parallel_group: overnight-n11-b
    note: A confirm needs a Fable max adversarial review before it is used as a leaf.
    outcomes:
    - scope: H-237 by the growth-cone route over all 128 branches and 66 faces (exp-227).
      classification: bounded-negative
      result: An exhaustion lemma caps every per-row-remainder certificate at the BC-199 modulus, and
        the exact computation confirms it on all 8,448 faces; the growth minimum 0.05177 is healthy, but
        the route cannot exceed rho. Along the binding direction 36 of 42 rows do not recover at second
        order, so the loose part is the remainder model.
      evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-227-h237-trump-growth-cone-capture-radius.md
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-042/exp-227-h237-growth-cone-and-route-radius.json
      disposition: retire-negative
      follow_up: null
  - id: BC-377
    purpose: research
    owner_focus: insight
    instances:
    - 11
    state: complete
    priority: 2
    question: With a descent filter that rejects the X-046 stalls, does any census minimum with three
      or more orientation classes lie below Stromquist's value?
    hypotheses:
    - H-238
    budget: Opus extra-high, three to four hours, in the second chunk.
    entry: A free agent slot; X-046 probes C and D as controls.
    exit: A census table of verified descent-stable minima, or a verified three-class minimum below 3.885618.
    bead: think-cdc2
    depends_on: []
    next_evidence: The census receipt under results/agenda-042/.
    workflows:
    - pipeline-improvement
    - research-loop
    program: n11-settlement
    artifacts:
    - packing/campaign/hypotheses/H-238-n11-no-third-class-minimum-below-stromquist.md
    parallel_group: overnight-n11-c
    note: Support, never proof; its kill would make the three-orientation rung mandatory.
    outcomes:
    - scope: H-238 on 1,000 jolted starts about Trump and Stromquist (exp-228).
      classification: achieved
      result: 'Support only, as registered: no descent-stable minimum with three or more classes below
        3.885618; all 85 such quench endpoints descend. New minima within U + 0.02: a two-class 0/41.56
        degree packing at 3.8867460 and a genuine three-class packing at 3.8943219.'
      evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-228-h238-descent-filtered-census.md
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-042/exp-228-h238-census-minima.json
      disposition: retire-success
      follow_up: null
  - id: BC-378
    purpose: research
    owner_focus: insight
    instances:
    - 21
    state: complete
    priority: 2
    question: Does a window-enriched point certificate retain at n21, side 122/25, below mass 21?
    hypotheses:
    - H-240
    budget: Opus high runs the stock column generator for one or two runs of at most 3,600 s each beside
      BC-379, then the decision gate.
    entry: H-240 registered; stock instruments.
    exit: RETAINABLE with mass below 21, then a Fable max W2 review before any register entry; or two
      site sets converging at 21 or above.
    bead: think-gkki
    depends_on: []
    next_evidence: The run log, frozen certificate and decision receipt under results/agenda-042/.
    workflows:
    - research-loop
    program: low-n-angles
    artifacts:
    - packing/campaign/hypotheses/H-240-n21-additive-certificate-at-4-88.md
    parallel_group: overnight-low-n
    note: A retain would move s(21) from 4.85 to 4.88, the largest low-n point rung left.
    outcomes:
    - scope: H-240 on three site sets at n=21, side 122/25 (exp-229).
      classification: achieved
      result: Set C's point certificate (1,228 atoms, mass 20.145724) is RETAINABLE from both routes of
        decide_certificate at least cell mass 250001/250000. Set B converged but its interval route stalled
        on a degenerate seam and refused; set A reached its deadline. The register entry waits for the
        Fable max W2 review.
      evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-229-h240-n21-point-certificate-122-25.md
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-042/exp-229-n21-122-25-receipt.md
      disposition: continue
      follow_up: think-gkki
  - id: BC-379
    purpose: research
    owner_focus: correctness
    instances:
    - 12
    state: complete
    priority: 2
    question: Does the cutting loop certify an additive ceiling at n12, side 39609/10000?
    hypotheses:
    - H-241
    budget: The same Opus high agent as BC-378, one cutting run of about 90 minutes plus the readers.
    entry: H-241 registered; T-017's certificate as the seed.
    exit: A proved ceiling of at least 12 accepted by both readers, or a settled value below 12.
    bead: think-xmm4
    depends_on: []
    next_evidence: The cutting-run log and ceiling receipt under results/agenda-042/.
    workflows:
    - research-loop
    program: low-n-angles
    artifacts:
    - packing/campaign/hypotheses/H-241-n12-additive-route-dead-above-3-9609.md
    parallel_group: overnight-low-n
    note: A confirm is a decisive negative about a method and leaves n12 to thresholds or structure.
    outcomes:
    - scope: H-241, three cutting legs at n=12, side 39609/10000 (exp-230).
      classification: time-limited
      result: 'No proved ceiling: the best family totals were 10.704 and 9.878 against 12, while the unconverged
        row objective stayed near 11.98. Neither criterion was reached; a later attempt needs a converged
        row loop or a larger family support.'
      evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-230-h241-n12-additive-ceiling-3-9609.md
      disposition: defer-dependency
      follow_up: think-xmm4
    - scope: H-241 round 2, the warm-started cutting loop with more rows and a larger support (exp-233).
      classification: bounded-negative
      result: 'The row loop converged at a covering value of 11.980175 < 12 with no family reaching 12,
        so H-241 is rejected as registered: the additive route at n12 is not shown dead above 3.9609.
        Freezing the converged covering for the stock gate is a cheap follow-up, not selected.'
      evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-233-h241-n12-ceiling-settles-below-12.md
      disposition: retire-negative
      follow_up: null
  - id: BC-380
    purpose: tool_validation
    owner_focus: correctness
    instances:
    - 12
    - 18
    - 21
    state: ready
    priority: 3
    question: Can a direction-dependent parent-centre clip behind colgen's clip parameter, and a converter
      from a frozen clipped certificate to a ParentCoreCertificate, pass T-017 re-decision, a planted
      undercharged pose and the closed-boundary band?
    hypotheses: []
    budget: Opus extra-high, several hours, when a slot frees after BC-378 and BC-379.
    entry: X-047's instrument specification.
    exit: An admitted instrument with its three controls passing, ready for H-240's successor at 4.9;
      a W2 review before its first target run.
    bead: think-m9iz
    depends_on: []
    next_evidence: parent_clip.py, freeze_to_parent_core.py and their tests.
    workflows:
    - pipeline-improvement
    program: low-n-angles
    artifacts:
    - packing/campaign/explorations/X-047-low-n-angles-after-the-parent-core-advance.md
    parallel_group: overnight-low-n
    note: 'The first target runs of the clip are a later session''s registered hypotheses. Retargeted
      2026-09-27: wand125''s rectangle certificates at n = 18 (4.695) and n = 21 (4.985) pass the clip''s
      n = 18 and n = 21 targets, so the instrument keeps n = 12 only, behind H-244''s price.'
    outcomes:
    - scope: The ParentClip build, dispatched at 03:10 PT.
      classification: never-opened
      result: The lane was stopped by the harness session quota at about 03:15 PT before it wrote any
        file; no instrument exists. It remains the enabling build for the n21 4.9 and n18 4.70 rungs.
      evidence:
      - packing/campaign/agent-sessions/session-156-w3-overnight-n11-settlement.md
      disposition: defer-dependency
      follow_up: think-m9iz
  - id: BC-381
    purpose: research
    owner_focus: correctness
    instances:
    - 11
    state: complete
    priority: 1
    question: Does a Fable max adversarial W2 review of the closed rung-0 tree (exp-232) accept H-236
      at its registered scope, and what register entry, rated by epistemics.md, does it support?
    hypotheses:
    - H-236
    budget: One Fable max review lane, daytime, reading the retained reader verdict and the 5.5 GB tree
      in place.
    entry: exp-232 closed with the reader's verdict retained; the rung-0 contract review of 2026-09-23.
    exit: An accepting or rejecting review, and a register entry or a stated reason for none.
    bead: think-6w2y
    depends_on: []
    next_evidence: A dated review under docs/project/reviews/ and, if accepted, a results.yaml row.
    workflows:
    - factual-review
    program: n11-settlement
    artifacts:
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-232-h236-rung-zero-closed.md
    parallel_group: n11-rung0-review
    note: The terminal leaves use BC-240's first clause, verified and exact since BC-382 closed BC-241.
    outcomes:
    - scope: The Fable max W2 review of the closed rung-0 tree and the register decision.
      classification: achieved
      result: 'Accepted, with the scope split: the machine-verified reduction to Trump''s ball is T-035
        (V4/C5/S3), and the composed optimality theorem, which adds BC-240''s audited first clause, is
        T-036 (V3/C2/S3). Eleven subtrees re-replayed independently and all 259 archived files match the
        manifest. "First global optimality statement in any n = 11 family" was narrowed, since Stromquist''s
        0/45-degree bound is earlier.'
      evidence:
      - docs/project/reviews/review-2026-09-24-rung0-closed-tree.md
      - packing/frontier/results.yaml
      disposition: retire-success
      follow_up: null
  - id: BC-382
    purpose: research
    owner_focus: correctness
    instances:
    - 11
    state: complete
    priority: 1
    question: What did BC-241 leave open on the BC-240 isolation packet, and does an independent radius-generator
      replay close it, so that results ending in Trump-degenerate leaves no longer carry the pending-BC-241
      qualifier?
    hypotheses: []
    budget: One Fable extra-high lane; the radius replay is about six minutes of CPU.
    entry: The BC-240 packet, the BC-241 review, and exp-227's method-distinct modulus control.
    exit: A dated review closing BC-241 or scoping exactly what remains retained-record-dependent.
    bead: think-mlz3
    depends_on: []
    next_evidence: docs/project/reviews/review-2026-09-24-bc241-closure.md
    workflows:
    - factual-review
    program: n11-settlement
    artifacts:
    - packing/cases/trump11/isolation-theorem.md
    parallel_group: n11-lock-in
    note: Every rung of the settlement ladder closes its Trump leaves with BC-240's first clause.
    outcomes:
    - scope: BC-241's open obligations on the BC-240 packet.
      classification: achieved
      result: A full radius-generator replay reproduced BC-199 on all 4,954 values, the method-distinct
        capture_radius control confirmed the weighted modulus on all 8,448 faces to 32 digits, and BC-241's
        checker accepts with its mutations rejected. BC-240's first clause, the one rung leaves use, is
        verified and exact; per-face dual witnesses are recomputed rather than retained and the gap cap
        is single-source and non-binding.
      evidence:
      - docs/project/reviews/review-2026-09-24-bc241-closure.md
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-042/bc382-isolation-radius-replay.json.gz
      disposition: retire-success
      follow_up: null
  - id: BC-383
    purpose: research
    owner_focus: insight
    instances:
    - 11
    state: complete
    priority: 1
    question: What does the rung-0 cell tree cost on boxes away from Trump's tilt, and does rung 1 (H-112)
      become a tiling computation or need a stronger relaxation first?
    hypotheses:
    - H-242
    budget: Opus extra-high builds an additive parameterized box preset with h236 unchanged, a short Fable
      review admits it, then one overnight CPU pilot on about nine workers.
    entry: exp-232's closed tree and its cost; the reviewed instrument contract.
    exit: Per-box closed/unresolved verdicts and node counts from the reader for the pilot boxes, and
      a pricing of H-112.
    bead: think-6b12
    depends_on: []
    next_evidence: The pilot receipts under results/agenda-042/ and an experiment record.
    workflows:
    - pipeline-improvement
    - research-loop
    program: n11-settlement
    artifacts:
    - packing/campaign/hypotheses/H-242-n11-rung1-pilot-cost-away-from-trump.md
    parallel_group: n11-rung1-pilot
    note: A measurement that prices H-112; it moves no bound.
    outcomes:
    - scope: H-242, eighteen boxes at six tilts and three widths, 150,000 nodes per subtree (exp-234).
      classification: bounded-negative
      result: No box closed at the declared cap; every box closed about two-thirds of its measure (0.624
        to 0.672) for about four million nodes, with no trend in width or tilt. Rung 1's cost lives in
        the fixed-angle centre enumeration, so a stronger per-node bound is the prerequisite for H-112;
        wide boxes cost no more than narrow ones once it exists.
      evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-234-h242-rung1-pilot.md
      disposition: retire-negative
      follow_up: think-ggk5
  - id: BC-384
    purpose: research
    owner_focus: insight
    instances:
    - 11
    state: blocked
    priority: 1
    question: Which stronger per-node bound for the fixed-angle cell tree closes a rung-0 subtree or an
      exp-234 pilot box in orders of magnitude fewer nodes, with the reader's certificate contract unchanged
      or reviewed?
    hypotheses: []
    budget: A W3 design note, then a W7 prototype measured against retained pilot and rung-0 trees.
    entry: exp-234's flat response to width and tilt; X-046's second-order dual bound; exp-228's descent
      filter.
    exit: A measured node-count reduction on retained boxes, or a scoped reason none of the candidates
      helps.
    bead: think-ggk5
    depends_on:
    - BC-388
    - BC-389
    next_evidence: A design note and a benchmark receipt.
    workflows:
    - insight-iteration
    - pipeline-improvement
    program: n11-settlement
    artifacts:
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-234-h242-rung1-pilot.md
    parallel_group: n11-rung1-relaxation
    note: 'Rung 1 (H-112) is priced out with the present relaxation; this is its prerequisite. Narrowed
      by BC-385: the design note chooses between parametric-in-tilt certificates, which certify a midpoint
      dual vector over a whole tilt interval by univariate polynomial positivity, and per-square counting
      at each node, after BC-388 and BC-389 report. The second-order dual bound, the descent filter, symmetry
      reduction and LP warm starts are retired as BC-384 candidates; node throughput is a separate efficiency
      item.'
  - id: BC-385
    purpose: research
    owner_focus: insight
    instances:
    - 11
    - 12
    - 17
    - 21
    state: complete
    priority: 0
    question: What else do R052 at n17 and the closed rung 0 at n11 make possible, and which bounded commitments
      should follow them?
    hypotheses:
    - H-243
    - H-244
    - H-245
    - H-246
    - H-247
    budget: 'Session 159''s W10 planning block: two Fable max assessments in parallel, one per case, each
      with at most ten minutes of probes, then codification.'
    entry: R052 integrated at V4/C3 with its review; rung 0 closed as T-035 and T-036; exp-234 retained.
    exit: The plan document retained, the selected directions registered as H-243 to H-247, and BC-386
      to BC-391 given beads, prices, stop conditions and an order.
    bead: think-f0if
    depends_on: []
    next_evidence: docs/project/specs/active/plan-2026-09-25-after-r052-planning.md
    workflows:
    - review-planning-oversight
    artifacts:
    - docs/project/specs/active/plan-2026-09-25-after-r052-planning.md
    - docs/project/reviews/review-2026-09-25-n17-guzhou-r052.md
    parallel_group: after-r052-planning
    note: 'Not selected: a first-party n17 producer beyond 4.62002 waits for BC-387 and is reconsidered
      only if the ceiling is at least 4.64; the n12 parent-core transfer waits for BC-387''s n12 price
      and BC-380''s parent clip; any n11 lower-bound increment stays under the owner''s 2026-09-14 hold.'
    outcomes:
    - scope: The Session 159 planning block after R052.
      classification: achieved
      result: R052's certificate is nearly saturated and its public ladder is flattening, so a first-party
        increment is not worth building until the architecture's ceiling is priced; at n11 the cost of
        rung 1 is the relaxation, so a per-node bound must price all pairs at once. Six commitments were
        selected, and BC-384 was narrowed to two designs. Nothing in the block moves a bound.
      evidence:
      - docs/project/specs/active/plan-2026-09-25-after-r052-planning.md
      disposition: retire-success
      follow_up: null
  - id: BC-386
    purpose: tool_validation
    owner_focus: correctness
    instances:
    - 17
    state: stopped
    priority: 1
    question: Does this repository's native coverage engine decide every row of R052's certificate at
      or above its charge once its memory-policy ceilings are lifted behind an explicit byte budget, so
      that R052 can be rated C4?
    hypotheses: []
    budget: Opus extra-high about two hours to lift the ceilings, add a contract test admitting R052's
      dimensions and re-baseline the n11 native audit; about 15 CPU-hours, about eight hours of wall on
      the tool's two workers; Fable extra-high checks the transfer contract.
    entry: R052 at V4/C3; packing/devtools/verify_guzhou_r052_native.py; the sizing rows that certified
      at or above the charge in Session 159.
    exit: Every row decided by the native engine on a clean reviewed commit, with the byte budget recorded
      in the receipt, or the rows it refuses listed as refusals.
    bead: think-amx8
    depends_on: []
    next_evidence: A native-decision receipt for R052 under results/agenda-042/ and the reviewed cap-lift
      commit.
    workflows:
    - pipeline-improvement
    - factual-review
    program: low-n-angles
    artifacts:
    - docs/project/reviews/review-2026-09-25-n17-guzhou-r052.md
    - packing/devtools/verify_guzhou_r052_native.py
    parallel_group: n17-native-c4
    note: The cap lift lands as a reviewed commit before the run starts. R052 has zero slack, so a stalled
      or seam row is possible; it is recorded as a refusal, never as a negative.
    outcomes:
    - scope: The native R052 decision, before any build.
      classification: never-opened
      result: Superseded on 2026-09-27 by Kleddamag v1.1.0 (s(17) > 232001/50000), which replaces R052
        as the verified bound. The cap lift and the native decision carry over to BC-393, whose v1.1.0
        loader also reads R052's schema as a subset if a second data point is ever wanted; nothing was
        run.
      evidence:
      - docs/project/specs/active/plan-2026-09-27-after-4640020-overnight.md
      disposition: defer-dependency
      follow_up: think-0rbj
  - id: BC-387
    purpose: research
    owner_focus: insight
    instances:
    - 17
    - 12
    state: ready
    priority: 1
    question: With the capacity-one ceiling lemma proved in the 4.640020 review, does a clique-weighted
      family of unit squares with fractional stability at least 17 exist at 4675/1000 and 467/100, and
      a triangle-free family of 24 at 397/100 and 399/100, under an exact checker?
    hypotheses:
    - H-243
    - H-244
    - H-248
    budget: Opus extra-high about three hours to promote the attic/planning-160 anneal to a devtool and
      drive geometric_graph_certificate, check_weighted_clique_certificate and an exact containment check;
      the searches run in minutes wherever a slot is free.
    entry: The lemma reviewed on 2026-09-27; Kleddamag's 4.66001 certificate and Bidwell's packing as
      the two ends, so the ceiling lies in [4.66001, 4.67553].
    exit: An exact-checker verdict on a family at each target or a search budget spent without one.
    bead: think-68la
    depends_on: []
    next_evidence: A dated lemma review under docs/project/reviews/, then the checker receipts under results/agenda-042/.
    workflows:
    - factual-review
    - pipeline-improvement
    - research-loop
    program: low-n-angles
    artifacts:
    - packing/campaign/hypotheses/H-243-n17-triangle-free-34-family-at-4-63.md
    - packing/campaign/hypotheses/H-244-n12-triangle-free-24-family-at-3-99.md
    - packing/campaign/hypotheses/H-248-n17-clique-weighted-family-at-4-675.md
    - docs/project/reviews/review-2026-09-27-n17-kleddamag-466001.md
    parallel_group: architecture-ceiling
    note: 'Retargeted 2026-09-27: H-243''s 463/100 is refuted by the v1.1.0 certificate itself, since
      every one of its atoms has capacity one. H-248''s 465/100 and 466/100 were refuted in turn by the
      4.66001 certificate on 2026-09-27; H-248 takes 4675/1000 and 467/100 in the clique-weighted form.
      No family found is inconclusive, not a negative. The price decides the first-party n17 producer
      (reconsidered only if the search at 4675/1000 finds no family within its budget; a family there
      caps the architecture below 4.675 and closes the producer question) and the n12 parent-core transfer.
      A two-minute anneal at 4.65 ended at two triangles with fractional stability 16.'
  - id: BC-388
    purpose: research
    owner_focus: insight
    instances:
    - 11
    state: ready
    priority: 1
    question: What is the least side f(theta) along the six-axis plus five-common-angle family at 200
      tilts, and on which window is it within 0.01 of U?
    hypotheses:
    - H-245
    budget: Opus high about two hours to build the frozen-angle census, then one night on seven workers.
    entry: The exp-228 census driver and quench; H-245 registered.
    exit: A table of f(theta) at 200 tilts with verified witnesses and the window where f(theta) - U <
      0.01.
    bead: think-91yk
    depends_on: []
    next_evidence: The census receipt under results/agenda-042/ and an experiment record.
    workflows:
    - pipeline-improvement
    - research-loop
    program: n11-settlement
    artifacts:
    - packing/campaign/hypotheses/H-245-n11-family-side-profile-along-the-tilt.md
    parallel_group: n11-family-profile
    note: None as a stop; it is a measurement that prices BC-389 and BC-384 and moves no bound. Priced
      2026-09-27 at 11 to 19 s a start on one worker with the stock census (8 s quench cap, 20 s filter
      cap), so about 80 CPU-hours for 20,000 starts; second night of the after-4.640020 order.
  - id: BC-389
    purpose: research
    owner_focus: insight
    instances:
    - 11
    state: ready
    priority: 2
    question: Does a two-class parent-core counting certificate close the rung-1 box at 20 degrees, half-tangent
      [0.1758, 0.1768], outright?
    hypotheses:
    - H-246
    budget: Opus extra-high one to two days of build and hours of CPU; Fable extra-high reviews the two-class
      lemma.
    entry: sqpack.fractional.classcert, the parent-core and threshold separators, and the native sweep;
      exp-234's box at 20 degrees.
    exit: A native-swept certificate with an accepting lemma review, or the mass still above 11 after
      site column generation with two-of-three and three-of-five atoms.
    bead: think-nho8
    depends_on: []
    next_evidence: The frozen certificate, the native sweep receipt and a dated lemma review.
    workflows:
    - pipeline-improvement
    - research-loop
    - factual-review
    program: n11-settlement
    artifacts:
    - packing/campaign/hypotheses/H-246-n11-two-class-certificate-closes-a-rung1-box.md
    parallel_group: n11-two-class-closer
    note: Stop when the mass stays above 11 after site column generation with two-of-three and three-of-five
      atoms. Aimed at a box, not at the side, so it is outside the owner's hold on n11 lower-bound increments.
  - id: BC-390
    purpose: research
    owner_focus: correctness
    instances:
    - 11
    state: ready
    priority: 2
    question: Does the unchanged rung-0 instrument prove H-236's statement on the half-tangent box of
      half-width 10^-4 around Trump's tilt?
    hypotheses:
    - H-247
    budget: A launcher only; about 1.7e8 nodes, one night on nine workers, then the reader.
    entry: The fixed_angle_tree box preset and reader at their exp-234 bytes; T-035 and T-036.
    exit: A reader-closed tree on the widened box, a verified counterexample candidate, or an unresolved
      leaf list at the declared cap.
    bead: think-7c17
    depends_on: []
    next_evidence: The frozen digests, run output and reader verdict under results/agenda-042/.
    workflows:
    - research-loop
    program: n11-settlement
    artifacts:
    - packing/campaign/hypotheses/H-247-n11-rung0-widened-to-half-width-1e-4.md
    parallel_group: n11-rung0-wide
    note: 'Stop if the enclosure reach of a Trump-degenerate leaf meets the local-theorem radius rho.
      Selected on 2026-09-27 as the first lane of the night: the box [731338615209/2000000000000, 731738615209/2000000000000]
      is admitted by box_setup (reach 2.02e-4 against rho 4.04e-3); about 95 CPU-hours at exp-232''s node
      rate, eight workers, resumed by subtree if the morning cutoff comes first.'
  - id: BC-391
    purpose: research
    owner_focus: insight
    instances:
    - 21
    state: stopped
    priority: 3
    question: Does the additive point certificate at n21 reach side 4.89 on stock column generation, without
      the parent clip?
    hypotheses: []
    budget: Opus high, runs of under an hour each, in idle slots.
    entry: T-034's certificate at 4.88 and the stock column generator; an H-item registered for the 4.89
      claim before any run.
    exit: A value below 21 retained by the decision gate, or a converged value of at least 21 on two site
      sets.
    bead: think-t50i
    depends_on: []
    next_evidence: The run logs and decision receipts under results/agenda-042/.
    workflows:
    - research-loop
    program: low-n-angles
    artifacts:
    - packing/campaign/hypotheses/H-240-n21-additive-certificate-at-4-88.md
    parallel_group: idle-slot
    note: Register the H-item before the first run. Stop when the value reaches 21 on two site sets or
      when the certificate fails on both.
    outcomes:
    - scope: The n21 point certificate at 4.89, before any run.
      classification: never-opened
      result: 'Retired on 2026-09-27 as moot, not as a negative about the additive route: wand125''s rectangle-density
        certificate proves s(21) >= 997/200 = 4.985, and Daniel''s weighted cover claims 5000/1001 = 4.995,
        past 4.89 and past every point-certificate rung the register could reach at n = 21. The intake
        of those certificates is other lanes''.'
      evidence:
      - docs/project/specs/active/plan-2026-09-27-after-4640020-overnight.md
      disposition: retire-negative
      follow_up: null
  - id: BC-392
    purpose: research
    owner_focus: insight
    instances:
    - 11
    - 12
    - 17
    - 50
    - 82
    state: complete
    priority: 0
    question: After Kleddamag v1.1.0 (s(17) > 4.640020) and wand125's rectangle certificates for n = 18..78,
      which deeper pushes are worth an overnight CPU budget, and in what order?
    hypotheses:
    - H-248
    - H-249
    - H-250
    - H-251
    budget: One Fable max planning lane with probes of at most fifteen minutes each on two cores, then
      codification; about three hours.
    entry: v1.1.0 reviewed with no defect and the capacity-one lemma proved; wand125's rectangle certificates
      published; the 2026-09-25 plan's order not yet started.
    exit: The plan document retained; H-248 to H-251 registered; BC-393 to BC-395 given beads, prices,
      stop conditions and a queue; BC-386, BC-387, BC-391 and BC-380 dispositioned.
    bead: think-0v60
    depends_on: []
    next_evidence: docs/project/specs/active/plan-2026-09-27-after-4640020-overnight.md
    workflows:
    - review-planning-oversight
    artifacts:
    - docs/project/specs/active/plan-2026-09-27-after-4640020-overnight.md
    parallel_group: after-4640020-planning
    note: 'Not selected: a first-party n17 producer beyond 4.640020 (the same dictionary caps near 4.646;
      BC-387''s price at 4.65 decides), the Kleddamag/Guzhou family at n = 18..21 (the rectangle route
      leads there), BC-389 (a build), and any n11 lower-bound increment under the owner''s hold.'
    outcomes:
    - scope: The 2026-09-27 planning block.
      classification: achieved
      result: v1.1.0 has 2,048 rows, 8,876 sites and 4,328 charged images, every atom of capacity one,
        including 240 winning-subset rules the native route lacks; its ledger sits on a plateau with 65
        binding rows, so reweighting caps near 4.646. H-243's 4.63 target is refuted by the certificate
        itself and the ceiling search moves to 4.65 in clique-weighted form, where a two-minute anneal
        reaches two triangles. The largest prize is the rectangle ladder at the rows wand125 left (n =
        50 and 82..97, gaps near 0.49); tonight runs BC-390, BC-394 and BC-395, and the day builds BC-393,
        BC-388 and BC-387. Nothing in the block moves a bound.
      evidence:
      - docs/project/specs/active/plan-2026-09-27-after-4640020-overnight.md
      disposition: retire-success
      follow_up: null
  - id: BC-393
    purpose: tool_validation
    owner_focus: correctness
    instances:
    - 17
    state: ready
    priority: 1
    question: Does this repository's native coverage engine decide every one of the 2,168 rows of Kleddamag's
      4.66001 certificate (57519bb) at or above its charge, once a loader for its schema, a winning-subset
      atom and the lifted site ceiling exist, so that s(17) > 466001/100000 can be rated C4?
    hypotheses: []
    budget: Opus extra-high three to four hours for the loader (sets, coefficients, winning_masks), the
      winning-subset atom in the parent-core and interval routes, the cap lift behind a byte budget and
      their tests; Fable extra-high one hour on the atom's capacity-one lemma and the box bounds of a
      monotone rule; masks on up to 12 sites, the cap lift to at least 20,856 sites, and about 2 to 12
      CPU-hours on two workers.
    entry: The 4.66001 certificate at V4/C3 on the intake branch; packing/devtools/verify_guzhou_r052_native.py
      as the pattern; the 2026-09-27 rule census.
    exit: Every row decided on a clean reviewed commit with the byte budget in the receipt, or the refused
      rows listed as refusals; a Fable max reading before the rating changes.
    bead: think-0rbj
    depends_on: []
    next_evidence: A native-decision receipt in the 4.66001 source packet and the reviewed commit.
    workflows:
    - pipeline-improvement
    - factual-review
    program: low-n-angles
    artifacts:
    - docs/project/specs/active/plan-2026-09-27-after-4640020-overnight.md
    - docs/project/reviews/review-2026-09-27-n17-kleddamag-466001.md
    - packing/devtools/verify_guzhou_r052_native.py
    parallel_group: n17-native-c4
    note: Carries BC-386's cap lift. A refused row is a refusal; a row below the charge contradicts two
      exact sweeps and is a loader defect until shown otherwise. Second night of the after-4.640020 order.
      Retargeted 2026-09-27 from v1.1.0 (2,048 rows, 8,876 sites) to the 4.66001 certificate that supersedes
      it, since a C4 rating of 4.640020 would be superseded on arrival.
  - id: BC-394
    purpose: research
    owner_focus: insight
    instances:
    - 82
    - 50
    state: ready
    priority: 1
    question: Do rectangle-density ladders from the trivial seed, with tokoharu's pinned push.py, reach
      93/10 at n = 82 and 73/10 at n = 50, with every accepted rung admitted by the exact preflight and
      an unmodified verifier replay?
    hypotheses:
    - H-250
    - H-251
    budget: 'Launcher only tonight: one search worker each plus verify workers; the per-rung cost is read
      from the first rungs. Admission needs audit_tokoharu_density generalised to any certificate directory,
      Opus high one to two hours, before any row is written.'
    entry: The pinned clone at 84bebef with its dependencies in a scratch Python 3.12 environment; the
      tokoharu review of 2026-09-22 (DENS-1 on push.py --from, which from-seed runs do not take).
    exit: The highest accepted rung of each ladder replayed and preflighted, then a Fable max W2 review
      before a register row; or the driver giving up below the register.
    bead: think-pr2b
    depends_on: []
    next_evidence: The ladder logs and certificate directories, then the replay receipts.
    workflows:
    - research-loop
    - factual-review
    program: low-n-angles
    artifacts:
    - packing/campaign/hypotheses/H-250-n50-rectangle-density-certificate-at-7-3.md
    - packing/campaign/hypotheses/H-251-n82-rectangle-density-certificate-at-9-3.md
    parallel_group: rectangle-ladders
    note: 'The largest expected gain on the board: about 0.2 to 0.35 of verified side on gaps near 0.49.
      A mass below 82 at side L covers every n >= 82 whose verified row is below L. Never a bound on the
      driver''s own status.'
  - id: BC-395
    purpose: research
    owner_focus: insight
    instances:
    - 12
    state: ready
    priority: 2
    question: Does the rectangle-density ladder from the trivial seed pass Daniel's 3.968616 at n = 12
      and reach 399/100?
    hypotheses:
    - H-249
    budget: Launcher only; one worker; about an hour to 3.96 at step 1/50, unknown above it.
    entry: The same pinned clone and environment as BC-394; the fourteen-minute probe from the seed.
    exit: An accepted rung above 3.968616 replayed and preflighted, or the driver giving up below 3.9687.
    bead: think-ujwy
    depends_on: []
    next_evidence: The ladder log and the highest certificate directory.
    workflows:
    - research-loop
    program: low-n-angles
    artifacts:
    - packing/campaign/hypotheses/H-249-n12-rectangle-density-certificate-at-3-99.md
    parallel_group: rectangle-ladders
    note: The one n = 12 route not yet tried; the parent-core architecture cannot reach the endpoint 4,
      the additive point route stalled near 3.96, and Daniel's pure cover LP sits at exactly 12.000 at
      the endpoint. Runs in the slot that frees first.
  - id: BC-396
    purpose: research
    owner_focus: insight
    instances:
    - 45
    state: blocked
    priority: 1
    question: Does Daniel's zero-margin weighted closed cover, which proves s(32) = 6, carry to k = 7,
      giving a cover of [0,7]^2 with mass below 45 and hence s(45) = 7?
    hypotheses:
    - H-252
    budget: Fable extra-high one to two hours on the method beside the intake lane's review; Opus extra-high
      half a day if the search must be adapted to k = 7; about 4 CPU-h per cover for the margin-zero check,
      by scaling the k = 6 census of 7,200 roots at 2.8 CPU-h.
    entry: The intake lane's accepting review of evand/square-packing at 167d842; the cover search under
      its s12/search and the two checkers.
    exit: A cover at k = 7 certified by both checkers here and a Fable max W2 review, or the search stalling
      at or above mass 45.
    bead: think-0g4t
    depends_on: []
    blocked_on: The intake lane's accepting review of evand/square-packing's s(32) certificate at 167d842,
      which is also the reading of the method this transfer needs.
    next_evidence: The k = 7 cover, both censuses and the review.
    workflows:
    - factual-review
    - research-loop
    program: low-n-angles
    artifacts:
    - packing/campaign/hypotheses/H-252-n45-zero-margin-closed-cover-at-7.md
    parallel_group: zero-margin-transfer
    note: 'Blocked on the intake lane''s review of Daniel''s s(32) certificate. The construction fell
      short at k = 5 (4.995) and k = 4 (3.968616), so the transfer is upward in k: n = 45, then 60, 77
      and 96. Nothing here replays or registers Daniel''s own results.'
  - id: BC-397
    purpose: measurement_validation
    owner_focus: correctness
    instances:
    - 17
    state: complete
    priority: 0
    question: Does the retained rational n17 upper certificate pass two local exact geometry implementations
      at its fixed side?
    hypotheses:
    - H-253
    budget: One 30-minute instrument and review slice; then one 10-minute measurement slice, 90 seconds
      per command, one worker.
    entry: Three Session165 W3 lanes identify a retained exact candidate; the corner adapter and parser
      contract require controls before target execution.
    exit: Exact 17-square, 68-vertex, 136-pair agreement with the source checker and local checkers, or
      retained refusal/timeout; no endpoint or optimality claim.
    bead: think-08sm
    depends_on: []
    next_evidence: packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-235-h253-n17-rational-upper.md
    workflows:
    - pipeline-improvement
    - research-loop
    - factual-review
    program: post-optimality-low-n
    artifacts:
    - packing/campaign/agent-sessions/session-165-post-optimality-overnight.md
    - packing/campaign/hypotheses/H-253-n17-retained-rational-upper.md
    note: Selected at the October1 W10 checkpoint. H248/BC387 remains the architecture question; this
      is feasibility admission of an existing source upper construction.
  - id: BC-398
    purpose: research
    owner_focus: insight
    instances:
    - 17
    state: complete
    priority: 0
    question: Does the proposed n17 endpoint contact chart match the retained rational witness within
      its frozen exact residual and feature thresholds?
    hypotheses:
    - H-254
    budget: One 20-minute instrument slice; one target evaluation capped at90seconds, one worker and10
      MiB output; independent output review.
    entry: H253 accepts the source feasibility; fresh Astra max derives the equality chart and identifies
      the missing capture implication.
    exit: Every frozen fidelity clause passes or its exact counterexample is retained; no root or optimality
      claim.
    bead: think-j516
    depends_on:
    - BC-397
    next_evidence: packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-236-h254-n17-contact-chart.md
    workflows:
    - pipeline-improvement
    - research-loop
    - factual-review
    program: post-optimality-low-n
    artifacts:
    - packing/campaign/hypotheses/H-254-n17-contact-chart-fidelity.md
    - docs/project/reviews/review-2026-10-01-post-optimality-w3-opening.md
    note: Preregistered before target arithmetic. H027 continues to own local angle-cone proof obligations;
      this test only assesses chart fidelity.
  - id: BC-399
    purpose: research
    owner_focus: insight
    instances:
    - 17
    state: complete
    priority: 0
    question: Does the fixed rational box contain an exact root of the two n17 contact-chart polynomials?
    hypotheses:
    - H-255
    budget: One controlled instrument slice, one90second producer run and one90second independent checker
      run; one worker and10 MiB per output.
    entry: H254 chart fidelity and independently reviewed polynomial reduction and conditional box-minimum
      theorem.
    exit: Exact contraction and inclusion pass independent checking, or a complete unresolved refusal
      is retained without changing the box.
    bead: think-bj81
    depends_on:
    - BC-398
    next_evidence: packing/campaign/hypotheses/H-255-n17-exact-polynomial-root.md
    workflows:
    - pipeline-improvement
    - research-loop
    - factual-review
    program: post-optimality-low-n
    artifacts:
    - packing/campaign/hypotheses/H-255-n17-exact-polynomial-root.md
    - docs/project/reviews/review-2026-10-01-post-optimality-w3-opening.md
    note: Root existence only; endpoint feasibility, joint slider domains and capture remain separate
      obligations.
  - id: BC-400
    purpose: research
    owner_focus: insight
    instances:
    - 17
    state: complete
    priority: 0
    question: Does the exact H255 root with fixed centroid sliders give a feasible17square endpoint packing?
    hypotheses:
    - H-256
    budget: One 20-minute controlled instrument slice; one 180-second run, one worker,10 MiB per output
      and independent output review.
    entry: H255 root existence accepted; full contact identity roster and centroid slider domain independently
      derived.
    exit: All68 wall and 136 pair obligations certified by identities or strict exact intervals, or retained
      unresolved refusal with no retuning.
    bead: think-bj81
    depends_on:
    - BC-399
    next_evidence: packing/campaign/hypotheses/H-256-n17-exact-endpoint-feasibility.md
    workflows:
    - pipeline-improvement
    - research-loop
    - factual-review
    program: post-optimality-low-n
    artifacts:
    - packing/campaign/hypotheses/H-256-n17-exact-endpoint-feasibility.md
    note: Endpoint feasibility only; common-orientation and branch capture remain open.
  - id: BC-401
    purpose: research
    owner_focus: correctness
    instances:
    - 17
    state: complete
    priority: 0
    question: Does the exact n17 endpoint have the complete predicted owner-axis and wall-corner feature
      inventory?
    hypotheses:
    - H-257
    budget: One25minute controlled instrument slice; one180second target, one worker,10MiB per output
      and independent review.
    entry: H255 root and H256 endpoint accepted; owner-axis inventory counts independently derived.
    exit: All168pair options,60active-wall corners and9tangent offsets certified, or retained unresolved
      refusal without retuning.
    bead: think-6dg0
    depends_on:
    - BC-400
    next_evidence: packing/campaign/hypotheses/H-257-n17-endpoint-contact-features.md
    workflows:
    - pipeline-improvement
    - research-loop
    - factual-review
    program: post-optimality-low-n
    artifacts:
    - packing/campaign/hypotheses/H-257-n17-endpoint-contact-features.md
    note: Accepted exp239 completes all168owner options,60corners and9offsets; independent175interval
      audit passes. Stationarity remains separate.
  - id: BC-402
    purpose: research
    owner_focus: correctness
    instances:
    - 17
    state: complete
    priority: 0
    question: Does the fixed analytic common-core stress exclude negative-side first-order directions
      in both n17corner branches?
    hypotheses:
    - H-258
    budget: One25minute controlled instrument slice; one300second target,oneworker,10MiB output andindependent
      review.
    entry: H257 exact feature inventory accepted; deterministic force/torque allocation derived beforetarget.
    exit: Exact52column dual identities andall58commonrow weight signs certified, orretained unresolvedcandidate
      withoutretuning.
    bead: think-wrgx
    depends_on:
    - BC-401
    next_evidence: packing/campaign/hypotheses/H-258-n17-common-core-stress.md
    workflows:
    - pipeline-improvement
    - research-loop
    - factual-review
    program: post-optimality-low-n
    artifacts:
    - packing/campaign/hypotheses/H-258-n17-common-core-stress.md
    note: Three target-free symbolic preparation guard failures stop this instrument. No target run or
      stationarity verdict; exact residual proof and controls remain missing. Local/globaloptimality remains
      separate. Unblocked 2026-10-01 by the BC-405 route review, lane A1 of BC-406. Two exploratory reconstructions
      find the candidate correct (exact identity at the exp-237 midpoint and three other rational points;
      all 58 weights nonnegative, exactly six zero); the stall was sympy.cancel expression swell. Repair
      the identity proof with polynomial-ring arithmetic or exact evaluation beyond the degree bound,
      within the frozen criterion. Session 167 repaired it at 2fbf8d29 (polynomial-ring identities, 256-bit
      outward bounds, denominator-factor guards); exp-242 accepted after independent review, with a clean replay.
  - id: BC-403
    purpose: research
    owner_focus: correctness
    instances:
    - 17
    state: complete
    priority: 0
    question: Does the exact mixed-capacity5by5 cover reduce the complete raw n17 occupancy census?
    hypotheses:
    - H-259
    budget: One15minute instrument/review slice;30second combined count/audit,oneworker,1MiB per output.
    entry: Exact wall-support lemma and closed-cover proposal registered before coefficient calculation.
    exit: Independent geometry review and exact DP/binomial agreement, or retained missing premise.
    bead: think-70sf
    depends_on: []
    next_evidence: packing/campaign/hypotheses/H-259-n17-mixed-capacity-cover.md
    workflows:
    - insight-iteration
    - pipeline-improvement
    - research-loop
    - factual-review
    program: post-optimality-low-n
    artifacts:
    - packing/campaign/hypotheses/H-259-n17-mixed-capacity-cover.md
    note: H259accepted:161100756 versus8597496600; independent36coefficient audit;0.35s group. Raw census
      only.
  - id: BC-404
    purpose: research
    owner_focus: correctness
    instances:
    - 17
    state: complete
    priority: 0
    question: Does a closed-assignment D4 quotient reduce the n17 occupancy census with independent exact
      counting?
    hypotheses:
    - H-260
    budget: Ready14:15UTC,target/review14:25UTC;30seconds,oneworker,1MiBoutputs.
    entry: Accepted H259cover; independent D4closedassignment proof.
    exit: Complete eight-term independent audit and controlled orbit count, or retained readiness gap.
    bead: think-gr22
    depends_on:
    - BC-403
    next_evidence: packing/campaign/hypotheses/H-260-n17-closed-cell-symmetry.md
    workflows:
    - insight-iteration
    - pipeline-improvement
    - research-loop
    - factual-review
    program: post-optimality-low-n
    artifacts:
    - packing/campaign/hypotheses/H-260-n17-closed-cell-symmetry.md
    note: H260accepted:20155518necessaryclosedassignmentorbits; all8countsindependentlyagree,0.14s group.
      Geometricexclusionsremainthink-11ma.
  - id: BC-405
    purpose: research
    owner_focus: insight
    instances:
    - 17
    state: complete
    priority: 0
    question: What does PR 265 leave for an n17 optimality proof, which route is most likely to finish
      one, and what bounded work comes next?
    hypotheses:
    - H-261
    - H-262
    - H-263
    - H-264
    - H-265
    budget: 'Session 166: two Fable extra-high assessments (proof route; local endpoint theorem), one survey lane,
      then coordinator reconciliation and codification, about four hours in all.'
    entry: PR 265 merged into main with its morning report, and think-11ma as the recorded next entry.
    exit: The route review retained, H-261 to H-265 registered, BC-406 to BC-411 given beads and lanes,
      BC-402 unblocked, think-11ma re-scoped, and one coordinating entry selected.
    bead: think-9fc1
    depends_on:
    - BC-404
    next_evidence: docs/project/reviews/review-2026-10-01-n17-route-after-pr265.md
    workflows:
    - review-planning-oversight
    program: post-optimality-low-n
    artifacts:
    - docs/project/reviews/review-2026-10-01-n17-route-after-pr265.md
    - packing/campaign/explorations/X048-route-review/README.md
    note: No mathematical error found in PR 265. The H-258 stress checks out exploratorily and the endpoint
      is a first-order minimum modulo its six slider directions, so the local theorem needs no second-order
      analysis. The global half has no exclusions; the hybrid route ranks first. No bound or verdict changes.
  - id: BC-406
    purpose: research
    owner_focus: correctness
    instances:
    - 17
    state: complete
    priority: 0
    question: Can the n17 local theorem, the occupancy census and the polynomial identification proceed
      as three disjoint parallel lanes?
    budget: One coordinated session; lane budgets are those of BC-402, BC-407, BC-408 and BC-409.
    entry: BC-405 complete; lanes A1 (BC-402), B (BC-408) and C (BC-409) ready.
    exit: Each dispatched lane reaches its own exit, then the coordinator integrates the records and
      runs W10 on the results.
    bead: think-c7kv
    depends_on:
    - BC-405
    next_evidence: docs/project/reviews/review-2026-10-01-n17-route-after-pr265.md
    workflows:
    - pipeline-improvement
    - research-loop
    - review-planning-oversight
    program: post-optimality-low-n
    artifacts:
    - docs/project/reviews/review-2026-10-01-n17-route-after-pr265.md
    note: Allocation per OR-10. Opus 5.5 builds instruments; Fable extra-high reviews instruments; Fable
      max derives and reviews the endpoint theorem and anything that moves a bound. Reconsider the order
      if the H-258 identity fails at a rational point or lane B leaves more than 1e5 orbits.
  - id: BC-407
    purpose: research
    owner_focus: correctness
    instances:
    - 17
    state: complete
    priority: 0
    question: Is the n17 endpoint a strict local minimum modulo its slider cone, with an explicit radius?
    hypotheses:
    - H-261
    budget: One controlled build and review slice of about two hours; target arithmetic in seconds to
      minutes, one worker.
    entry: H-258 accepted through BC-402.
    exit: Exact kernel, duals, curvature bounds, unavailability checks and slider uniformity certified
      at a declared radius with independent review, or a retained failed ratio test that selects interval
      enlargement.
    bead: think-n95s
    depends_on:
    - BC-402
    next_evidence: packing/campaign/hypotheses/H-261-n17-local-minimum-modulo-sliders.md
    workflows:
    - pipeline-improvement
    - research-loop
    - factual-review
    program: post-optimality-low-n
    artifacts:
    - packing/campaign/hypotheses/H-261-n17-local-minimum-modulo-sliders.md
    note: Exploratory first-order estimate of the radius is 3e-4 (worst ratio 0.86); it defines the capture
      target. Session 167 accepted H-258 (exp-242); the recipe review fixes items C1-C12
      and a uniform radius of about 1/5000 over the slider box; the checker's point half is at 11bdcd7c. exp-244 (unresolved)
      certifies the ratio test at r = 1/5000 over the declared box (worst 0.925818); the claim's physical
      slider domain exceeds it, and H-268 (BC-417) owes the bound. Session 168 met the exit with exp-248,
      which re-runs the ratio test over the widened box B_W' (worst 0.925931). H-261 stays unresolved as
      worded, since the family with squares 5 and 6 exchanged meets its premises outside B_W'.
  - id: BC-408
    purpose: research
    owner_focus: correctness
    instances:
    - 17
    state: complete
    priority: 0
    question: How many H260 occupancy orbits survive the s(6) and s(10) subcontainer cuts and exact conditional
      charge floors?
    hypotheses:
    - H-262
    budget: One build and review slice; about six R068-sized charge sweeps, hours in all.
    entry: H259 and H260 accepted; charge construction and floor definitions reviewed before any target
      count.
    exit: An exact, independently recounted survivor count with the endpoint pattern surviving, or a
      retained refusal without retuning.
    bead: think-j1uw
    depends_on:
    - BC-404
    next_evidence: packing/campaign/hypotheses/H-262-n17-conditional-charge-occupancy-census.md
    workflows:
    - insight-iteration
    - pipeline-improvement
    - research-loop
    - factual-review
    program: post-optimality-low-n
    artifacts:
    - packing/campaign/hypotheses/H-262-n17-conditional-charge-occupancy-census.md
    note: Exploratory cut counts leave about 7.7 million orbits before any charge floor. At most 1e4 survivors
      makes the hybrid route affordable; more than 1e5 sends the question back to W3. Session 167 ran it as a one-sided pilot (exp-243, rejected). R068's charge collapses at U
      and excludes nothing; 7,703,312 orbits survive the cuts. One D4-symmetric linear floor vector leaves at least
      30,966 by theorem; asymmetric and nonlinear floors escape that bound and are open.
  - id: BC-409
    purpose: research
    owner_focus: correctness
    instances:
    - 17
    state: complete
    priority: 2
    question: Is the certified n17 chart endpoint a root of the catalogue's irreducible degree-18 polynomial?
    hypotheses:
    - H-265
    budget: One short build slice; seconds to minutes of exact algebra.
    entry: H255 accepted.
    exit: An exact identification with an independent recheck, or a retained different factor.
    bead: think-e6y1
    depends_on:
    - BC-399
    next_evidence: packing/campaign/hypotheses/H-265-n17-catalogue-polynomial-identity.md
    workflows:
    - pipeline-improvement
    - research-loop
    program: post-optimality-low-n
    artifacts:
    - packing/campaign/hypotheses/H-265-n17-catalogue-polynomial-identity.md
    note: Closes the frontier identification blocker; not on the optimality proof's critical path. Session 167
      accepted H-265 in exp-245 (identical with unit 1, irreducible); the n-017.md blocker text is updated
      separately.
  - id: BC-410
    purpose: research
    owner_focus: insight
    instances:
    - 17
    state: stopped
    priority: 2
    question: Which closed cover keeps the n17 endpoint family inside one occupancy state and leaves the
      fewest survivors?
    hypotheses:
    - H-263
    budget: One W3 design slice, then one BC-408 census per candidate cover.
    entry: BC-408's census instrument accepted.
    exit: A selected cover with proved capacities and its survivor count, or the H259 grid retained with
      the reason.
    bead: think-x4a6
    depends_on:
    - BC-408
    next_evidence: packing/campaign/hypotheses/H-263-n17-endpoint-adapted-cover.md
    workflows:
    - insight-iteration
    - research-loop
    program: post-optimality-low-n
    artifacts:
    - packing/campaign/hypotheses/H-263-n17-endpoint-adapted-cover.md
    note: Square 9's centre is 0.0012 below an H259 seam; the cover was chosen without reference to the
      endpoint. Stopped 2026-10-02 by the route review's own condition, since BC-408 left more than 1e5
      orbits. The cover question returns with the bulk-exclusion design (Session 167 lane F).
  - id: BC-411
    purpose: research
    owner_focus: efficiency
    instances:
    - 17
    state: stopped
    priority: 1
    question: What does one exact geometric exclusion of an n17 occupancy leaf cost, on a uniform sample
      of the residue at a cap at or above the endpoint?
    hypotheses:
    - H-264
    budget: At most 2 CPU-hours per sampled leaf, 10 to 20 leaves.
    entry: BC-408 reported and BC-410 has selected the cover.
    exit: Exclusion fraction, producer and checker cost per leaf and an extrapolated total, with unresolved
      leaves explicit.
    bead: think-11ma
    depends_on:
    - BC-408
    - BC-410
    next_evidence: packing/campaign/hypotheses/H-264-n17-geometric-exclusion-cost-per-leaf.md
    workflows:
    - insight-iteration
    - research-loop
    program: post-optimality-low-n
    artifacts:
    - packing/campaign/hypotheses/H-264-n17-geometric-exclusion-cost-per-leaf.md
    note: Re-scopes Session 165's handoff. A cap below the endpoint (the candidate 4.67) would leave sides
      in (4.67, S*) uncovered; exclusions at a cap U >= S* apply to every smaller side. Stopped 2026-10-02 with BC-410, since no residue small enough to sample exists yet.
  - id: BC-412
    purpose: research
    owner_focus: insight
    instances:
    - 17
    state: complete
    priority: 1
    question: What does capture cost as a function of the local radius, and must the radius be enlarged first?
    budget: One Fable analysis lane of about 90 minutes in Session 167.
    entry: BC-406 dispatched; H-261 radius estimated.
    exit: A dated review with n11's capture statistics, a cost model by radius and a recommendation.
    bead: think-rode
    depends_on:
    - BC-406
    next_evidence: docs/project/reviews/review-2026-10-02-n17-capture-feasibility.md
    workflows:
    - insight-iteration
    program: post-optimality-low-n
    artifacts:
    - docs/project/reviews/review-2026-10-02-n17-capture-feasibility.md
    note: >-
      n11's focused radii were 6.5e-4 to 6.8e-3, not 1/64, so the n17 target is 1.5 to 16
      times finer rather than 50. Capture cost is modelled as logarithmic in the radius;
      leaves and the contraction rate drive it. The route review carries a dated correction.
  - id: BC-413
    purpose: research
    owner_focus: insight
    instances:
    - 17
    state: complete
    priority: 2
    question: Can the conditional projection theorem be widened into a theorem whose premises capture can deliver?
    budget: One Fable analysis lane of about 80 minutes in Session 167.
    entry: BC-412 complete.
    exit: A dated scope review with the plausible radius, the hardest premise and an instrument plan.
    bead: think-xnhx
    depends_on:
    - BC-412
    next_evidence: docs/project/reviews/review-2026-10-02-n17-widened-projection-scope.md
    workflows:
    - insight-iteration
    program: post-optimality-low-n
    artifacts:
    - docs/project/reviews/review-2026-10-02-n17-widened-projection-scope.md
    note: >-
      Plausible at angle radius 5e-3 to 1e-2 as a parametric-LP dual-sheet certificate over
      patches of seven backbone angles; nests inside H-261; the slider domain is the hardest
      premise. Next slice builds the certificate on a coarse patching and reports the patch
      count before any target run.
  - id: BC-414
    purpose: research
    owner_focus: insight
    instances:
    - 17
    state: complete
    priority: 0
    question: What bulk exclusion engine could take the n17 census to a residue geometric exclusion can absorb?
    hypotheses:
    - H-266
    - H-267
    budget: One Fable analysis lane of about 100 minutes in Session 167.
    entry: BC-408 reported a no-go for per-cell charge floors.
    exit: A dated design review with registrable hypotheses.
    bead: think-8ul6
    depends_on:
    - BC-408
    next_evidence: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
    workflows:
    - insight-iteration
    program: post-optimality-low-n
    artifacts:
    - docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
    note: >-
      n11's census was tractable through a minimal capacity-one cover and isolated
      sub-pattern certificates. The H259 grid counts like a 30-cell cover; an exploratory
      24-cell design has 43,593 orbits. Registered H-266 and H-267.
  - id: BC-415
    purpose: research
    owner_focus: correctness
    instances:
    - 17
    state: complete
    priority: 0
    question: Does a D4-symmetric capacity-one cover of at most 25 cells hold the n17 endpoint family in one state?
    hypotheses:
    - H-266
    budget: One Opus build lane and one Fable proof review of the depth-width wall lemma.
    entry: H-266 registered.
    exit: An exact cover receipt with an independently reviewed wall lemma, or the seam or capacity failure retained.
    bead: think-qjdb
    depends_on:
    - BC-414
    next_evidence: packing/campaign/hypotheses/H-266-n17-minimal-capacity-one-cover.md
    workflows:
    - pipeline-improvement
    - research-loop
    - factual-review
    program: post-optimality-low-n
    artifacts:
    - packing/campaign/hypotheses/H-266-n17-minimal-capacity-one-cover.md
    note: >-
      Started in Session 167 as lanes G (checker) and G-proof (wall lemma). exp-246 certifies the tabbed 24-cell cover (43,593
      orbits) and the review proves the wall lemma; unresolved because the family also realises a second
      state through side cell S1 and square 6's range is declared. Next, a unique-state check and a derived
      square-6 range. Lane G2 then built the unique-state design (0dabde12);
      Session 168 accepted H-266 on it in exp-247 after an independent review.
  - id: BC-416
    purpose: research
    owner_focus: correctness
    instances:
    - 17
    state: in_progress
    priority: 1
    question: Do certified isolated sub-patterns of arity at most seven leave at most 1e4 orbits on the H-266 cover?
    hypotheses:
    - H-267
    budget: About a week to adapt the n11 kernel; hours of CPU for certificates.
    entry: H-266 accepted.
    exit: A certified residue count with the endpoint surviving and n11 mask 0 reproduced, or a retained refusal.
    bead: think-1s3i
    depends_on:
    - BC-415
    next_evidence: packing/campaign/hypotheses/H-267-n17-isolated-sub-pattern-residue.md
    workflows:
    - pipeline-improvement
    - research-loop
    program: post-optimality-low-n
    artifacts:
    - packing/campaign/hypotheses/H-267-n17-isolated-sub-pattern-residue.md
    note: >-
      n11 excluded 1,904 of 2,180 cases with 59 such certificates; an exploratory
      arity-five proxy leaves 11,939 orbits on the 24-cell design. Session 168 built the
      selector (44 flags to arity seven, 5,084 projected orbits), the kernel and an
      independent branch and bound, and admitted W7 and A in exp-249: 17,690 certified
      orbits. exp-250 admitted SW9 (arity 9) and the state N1 on the standing verifier's
      full pass: 15,953. The residue process review plans the rest.
  - id: BC-417
    purpose: research
    owner_focus: correctness
    instances:
    - 17
    state: complete
    priority: 0
    question: Does square 6's H-266 cell keep the slides of squares 5 and 13 inside the box exp-244 certifies?
    hypotheses:
    - H-268
    budget: One short build and review slice.
    entry: exp-244 recorded; H-266 cover committed.
    exit: An exact bound with independent review, or a widened box and a re-run of exp-244.
    bead: think-set0
    depends_on:
    - BC-407
    - BC-415
    next_evidence: packing/campaign/hypotheses/H-268-n17-local-theorem-slider-coverage.md
    workflows:
    - pipeline-improvement
    - research-loop
    - factual-review
    program: post-optimality-low-n
    artifacts:
    - packing/campaign/hypotheses/H-268-n17-local-theorem-slider-coverage.md
    note: >-
      Closes H-261's scope gap. With square 6 at its centroid the review's float scan keeps a
      below 0.037 and z above -0.0235, well inside the box. Lane H proved a <= 21/100, z >= -1/20, b <= 3/40 on
      the tabbed design's S2 (7cd4e652); re-run on the unique design and review remain, and the box's
      faces a >= 0, b >= 0, z <= 1/16 need their own argument. Session 168 accepted H-268 (exp-248) on the
      unique design, with a in [0, 23/200], b in [-1.684957 r, 37/500] and z in [-49/1000, 0.0241]; since b
      can go negative, the local theorem was re-run over B_W' and passes. The capture target is the composed
      theorem in the local-half composition review.
  - id: BC-418
    purpose: research
    owner_focus: correctness
    instances:
    - 17
    state: ready
    priority: 0
    question: Can the n17 local theorem and cover be closed, and do sub-pattern exclusion and capture fit the budget?
    hypotheses:
    - H-261
    - H-266
    - H-267
    - H-268
    budget: One coordinated session; lane budgets per BC-415, BC-416 and BC-417, and a bounded capture pilot.
    entry: Session 167 complete with exp-242 to exp-246 recorded.
    exit: >-
      H-266 and H-268 decided and H-261 re-recorded with review; the H-267 instrument built
      with its method control; a measured capture contraction rate; then W10 on the results.
    bead: think-tmz6
    depends_on:
    - BC-406
    next_evidence: packing/campaign/agent-sessions/session-167-n17-parallel-lanes-after-route-review.md
    workflows:
    - pipeline-improvement
    - research-loop
    - review-planning-oversight
    program: post-optimality-low-n
    artifacts:
    - packing/campaign/agent-sessions/session-167-n17-parallel-lanes-after-route-review.md
    note: >-
      Selected next entry after Session 167. Read that session record, the capture,
      bulk-exclusion and local-theorem instrument reviews, and exp-244 and exp-246 first.
      The 6 October W3 reconciliation is
      docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md (think-gxls).
      Sessions 182 and 183 leave 36,784 states in 4,685 orbits under 58 admitted entries.
      The next planning checkpoint selects proof interfaces and portable replay,
      controlled capture discrimination with cheap widened-projection reconnaissance,
      and actual-residue tail stratification in parallel. H-266, H-268 and the H-267
      low-arity milestone have been decided; accepted experiments keep their criteria,
      and held closures remain outside the census pending the control ruling.
  - id: BC-419
    purpose: research
    owner_focus: correctness
    instances:
    - 17
    state: complete
    priority: 0
    question: >-
      Do at least half of the ten counted seed-182 draws close under the 17-owner kernel
      within the 7,000 s ceiling, and what does a verified closure cost per state?
    hypotheses:
    - H-264
    budget: >-
      At most 26 CPU-hours on two compute slots: 2,700 s for the endpoint-state control
      and 7,000 s per state, each under a hard timeout of 7,600 s.
    entry: >-
      H-264 rewritten with instrument_ready true in the session-182 registration commit,
      and the run worktree synced at that commit.
    exit: >-
      All twelve draws run, each closure re-proved by the standing kernel verifier in
      full and admitted, and the verdict fixed by the arithmetic; or a soundness alarm
      (the kernel closes the endpoint's own state), which stops the instrument.
    bead: think-z8an
    depends_on:
    - BC-415
    next_evidence: packing/campaign/agent-sessions/session-182-n17-overnight-lanes.md
    workflows:
    - research-loop
    program: post-optimality-low-n
    parallel_group: n17-overnight-182
    artifacts:
    - docs/project/specs/active/plan-2026-10-05-n17-overnight.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-252-h264-n17-overnight-per-state-price.md
    - docs/project/reviews/review-2026-10-05-exp-252-h264.md
    note: >-
      Under BC-418, lane A of the n17 overnight plan. The float pre-screen (survey seed 182, sample 12,
      two workers) runs first and also places the endpoint as its positive control; a
      draw it places leaves the count as a candidate near-endpoint state. Then the
      kernel control on the endpoint's own state, then the draws in the survey's index
      order, two at a time, at 32 bins. A run at its ceiling with process CPU below
      6,300 s is re-run once. Stop rules: a soundness alarm, or three consecutive
      crashes or refusals; the verdict stops nothing. Evidence record exp-252.
  - id: BC-420
    purpose: research
    owner_focus: correctness
    instances:
    - 17
    state: in_progress
    priority: 0
    question: >-
      Do the standing flags with the most census weight close under the frozen SW9
      adaptive-row kernel recipe, or under the branch and bound where its tree can be
      admitted tonight?
    hypotheses:
    - H-267
    budget: >-
      Kernel at most 17 CPU-hours at 7,000 s per target; branch and bound at most 14
      CPU-hours at 300 s per Knuth estimate and 5,400 s per certificate run. One compute
      slot, and a second when slot 4 opens.
    entry: >-
      The session-182 registration commit with the kernel target list frozen, and the
      run worktree synced at that commit.
    exit: >-
      The target list exhausted, each closure re-proved by a standing verifier in full
      and admitted; or a soundness alarm (endpoint7 closes, or the branch and bound
      certifies an endpoint control). A verifier FAIL stops admissions from that
      producer until a review.
    bead: think-035m
    depends_on:
    - BC-415
    next_evidence: packing/campaign/agent-sessions/session-182-n17-overnight-lanes.md
    workflows:
    - research-loop
    program: post-optimality-low-n
    parallel_group: n17-overnight-182
    artifacts:
    - docs/project/specs/active/plan-2026-10-05-n17-overnight.md
    - packing/campaign/explorations/X048-session-182-overnight/kernel-targets.txt
    note: >-
      Under BC-418, lane K of the n17 overnight plan. Targets: arity at most seven, at least three wall
      or corner cells, best penetration at least 5e-3, in projected-gain order, from the
      census at the registration commit (nine classes, frozen in kernel-targets.txt).
      Frozen recipe, SW9's: --bins 64 --max-rounds 24 --hull-limit 16 --producer-share
      0.6 --split-floor 512 --max-rows 1152 --split-patience 1 --max-seconds 7000. The
      endpoint7 control runs first at 3,600 s and must not close. The branch-and-bound
      queue routes on the Knuth estimate's mean with A and W7 as calibration controls and
      certifies classes of at most 1.5e5 nodes. Evidence record exp-251.
  - id: BC-421
    purpose: research
    owner_focus: correctness
    instances:
    - 17
    state: complete
    priority: 1
    question: >-
      Does any of the 95 distance-2 orbits of the arity8 frame pack at U, which would make
      the near-endpoint stage non-empty?
    hypotheses:
    - H-273
    budget: >-
      At most 6 CPU-hours on slot 4: ten shards of 9 or 10 orbits, each at a 3,600 s
      survey ceiling under a hard timeout of 3,900 s.
    entry: >-
      H-273 registered with the survey's shard option at its registration commit, a
      second clean run worktree at that commit, and slot 4 open at the coordinator's word.
    exit: >-
      All 95 orbits searched, or a placement found, which stops the lane for an exact
      check and the coordinator. A shard whose endpoint control fails to place stops the
      lane as an instrument failure.
    bead: think-tmz6
    depends_on:
    - BC-415
    next_evidence: packing/campaign/agent-sessions/session-182-n17-overnight-lanes.md
    workflows:
    - research-loop
    program: post-optimality-low-n
    parallel_group: n17-overnight-182
    artifacts:
    - docs/project/specs/active/plan-2026-10-05-n17-overnight.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-255-h273-n17-distance-two-survey.md
    - packing/campaign/explorations/X048-session-182-overnight/receipts/E
    note: >-
      Under BC-418, lane E of the n17 overnight plan (the backfill). The plan's run line
      named shards of 30 on two workers at a 3,600 s ceiling; the survey had no way to
      shard, so 504a84464 adds --shard K/N, and on one slot the same ceiling holds ten
      shards of 9 or 10. A positive result needs exclusion at U' in the composed argument;
      a negative is recorded as no placement in that many searches. Evidence record
      exp-253 or the next free id when it is written.
  - id: BC-422
    purpose: tool_validation
    owner_focus: efficiency
    instances:
    - 17
    state: in_progress
    priority: 1
    question: >-
      With a W5 block due under OR-12, do packing-validate --edit and --push stay within
      their 240 s and 1,800 s ceilings on this container, and what does the kernel
      producer's in-process self-check cost per row against the standing kernel verifier
      on tonight's closures?
    budget: >-
      No dedicated compute. The gate walls are read from the session-182 registration's
      own validation runs, and the per-row costs from lane A and lane K receipts.
    entry: The OR-12 count read at session-182's W10 phase is at least eight.
    exit: >-
      Both gate walls recorded against their ceilings, and the self-check-to-verifier
      ratio per row from at least one verified closure, or a record that none came back.
    bead: think-9ntw
    depends_on: []
    next_evidence: packing/campaign/agent-sessions/session-182-n17-overnight-lanes.md
    workflows:
    - efficiency-loop
    program: post-optimality-low-n
    parallel_group: n17-overnight-182
    note: >-
      Under BC-418, added at session-182's W10 phase because the count read from the agenda records is past
      eight: 34 cells terminal since BC-369, the last cell declaring efficiency-loop (nine
      sessions terminal since session-180's efficiency-loop phase). The prior per-row
      reading is 0.91 s for the producer's self-check against 0.18 s for the standing
      verifier on N1. CPU is tonight's bottleneck, so the block adds no gate run while
      the compute lanes hold the CPUs. BC-421 is lane E's.
  - id: BC-423
    purpose: research
    owner_focus: correctness
    instances:
    - 17
    state: in_progress
    priority: 0
    question: >-
      Does lane K's target 2 (corner-SW, side-N0, side-W0, side-W1, interior-SW,
      interior-NW, interior-W) close under SW9's recipe with lane D's diagnosed settings:
      48 rounds, 2,304 rows and the octagon core?
    hypotheses:
    - H-267
    budget: >-
      Two runs of at most 7,000 s each in lane K's freed slot (the endpoint7 control
      under the same settings, then the target) and one verification of at most 4,000 s.
    entry: >-
      Lane D's classification of K-k2 as loss-limited, and the coordinator's re-plan at
      the 11:27 UTC check-in; this cell committed before either run.
    exit: >-
      One run, verdict as observed: a closure re-proved by the standing kernel verifier
      in full and admitted, or a non-closure retained. A closure of the control is a
      soundness alarm.
    bead: think-035m
    depends_on:
    - BC-415
    next_evidence: packing/campaign/agent-sessions/session-182-n17-overnight-lanes.md
    workflows:
    - research-loop
    program: post-optimality-low-n
    parallel_group: n17-overnight-182
    artifacts:
    - docs/project/specs/active/plan-2026-10-05-n17-overnight.md
    note: >-
      Under BC-418, a future slice added at a check-in (the plan's rule 8); no frozen
      criterion and no running ceiling changes. The recipe is SW9's frozen one except
      --max-rounds 48 --max-rows 2304 --core octagon: --bins 64 --hull-limit 16
      --producer-share 0.6 --split-floor 512 --split-patience 1 --max-seconds 7000, from
      the clean run worktree at cebb5d15a. Lane D read the stall as loss-limited: the knot
      owners interior-NW and interior-W are 0.5 and 4.5 per cent supported, with median
      cut margins near 0.010 against the 1/512 core loss of 0.00097, and the run stopped
      at its 24-round cap with about 2,400 s of producer share unused. Caveat: lane K2
      found on W7 that the octagon core does not remove a coarse row's domain loss, so
      the hull side of a cut may still need the rows. Target 2 projects 2,917 orbits and
      the arity-at-most-7 residue stands at 10,173, so a closure would bear on H-267's
      threshold; any verdict change gets a W2 review. Evidence record exp-251. Target 2
      closed under these settings at 15:02:59 UTC (46 rounds) and its standing verifier
      passed in full at 15:22:50, but the endpoint7 control ended INCOMPLETE at 16:16:40:
      the producer stopped at its time share in round 9 with every owner's rows still live,
      and the checker ran out of the 7,000 s ceiling. An INCOMPLETE control is not a pass, so
      the gate voided the closure and nothing was admitted. At the coordinator's decision
      the checker alone re-checks the kept control node with --check-saved at a 14,000 s
      ceiling; only a stall there releases target 2 for admission, and a closure is a
      soundness alarm. The receipt and the producer's progress records are in
      receipts/K of X048-session-182-overnight. The re-check returned PASS_SAVED_STALL at
      17:40:21 on the endpoint7 node (cells and seed and node ids those of the kept
      control, receipts/K/kernel-control-endpoint7-bc423-check.json), but the queue's
      identity comparison failed on a JSON formatting difference and left target 2
      voided; target 2 awaits the user's ruling.
  - id: BC-424
    purpose: research
    owner_focus: correctness
    instances:
    - 17
    state: complete
    priority: 1
    question: >-
      Do at least two of the four counted lane A stalls (masks 2817021, 3063677, 2878207
      and 2784767) close under SW9's frozen adaptive-row recipe?
    hypotheses:
    - H-274
    budget: >-
      Five runs of at most 7,000 s (the endpoint-state control, then the four states in
      mask order) and a verification of at most 4,000 s per closure, in the slots lane A
      frees when its draws are done.
    entry: >-
      H-274 registered with the frozen list before its first run, and lane A's remaining
      draws finished; after BC-423 and lane E in the freed-slot order.
    exit: >-
      All four states run once, each closure re-proved by the standing verifier in full
      and admitted (each removes its own orbit), and the verdict read; or a soundness
      alarm (the endpoint-state control closes).
    bead: think-z8an
    depends_on:
    - BC-415
    next_evidence: packing/campaign/agent-sessions/session-182-n17-overnight-lanes.md
    workflows:
    - research-loop
    program: post-optimality-low-n
    parallel_group: n17-overnight-182
    artifacts:
    - packing/campaign/hypotheses/H-274-n17-per-state-closure-under-adaptive-rows.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-253-h274-n17-stalls-under-adaptive-rows.md
    - docs/project/reviews/review-2026-10-05-exp-253-h274.md
    note: >-
      Under BC-418, a future slice added at a check-in; H-264 keeps running to its own
      verdict on N1's recipe. Recipe: --bins 64 --max-rounds 24 --hull-limit 16
      --producer-share 0.6 --split-floor 512 --max-rows 1152 --split-patience 1
      --max-seconds 7000, from the clean run worktree at cebb5d15a. The list is frozen
      at this registration: the four counted draws that had stalled by then. The
      distance-2 draw 1964767 is left out (uncounted, and lane D found it
      consistency-limited). Mechanism and limits are lane D's stall classification, cited
      in H-274.
  - id: BC-425
    purpose: research
    owner_focus: correctness
    instances:
    - 17
    state: complete
    priority: 1
    question: >-
      Do the next ten standing flags by projected gain against the certified line at
      18b7c5ae1 (arity at most 8, at least three wall or corner cells, best penetration
      at least 0.005) close under lane K's frozen SW9 recipe?
    hypotheses:
    - H-267
    budget: >-
      At most ten runs of at most 7,000 s each and one verification of at most 4,000 s per
      closure, on the slot freed after BC-423 and the next slot freed after BC-424, ahead
      of lane E's second worker.
    entry: >-
      The coordinator's re-plan at the 16:30 UTC check-in; this cell and its frozen target
      list committed before the first run.
    exit: >-
      The list exhausted, each run's verdict as observed: a closure re-proved by the
      standing kernel verifier in full and admitted, one commit each, or a non-closure
      retained. Any soundness alarm or one verifier FAIL stops the slice.
    bead: think-035m
    depends_on:
    - BC-415
    next_evidence: packing/campaign/agent-sessions/session-182-n17-overnight-lanes.md
    workflows:
    - research-loop
    program: post-optimality-low-n
    parallel_group: n17-overnight-182
    artifacts:
    - packing/campaign/explorations/X048-session-182-overnight/kernel-targets-bc425.txt
    - packing/campaign/explorations/X048-session-182-overnight/receipts/K/census-bc425-targets.json
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-254-h267-n17-second-tranche-flags.md
    note: >-
      Under BC-418, lane K's second tranche, a future slice added at a check-in. The
      targets are frozen in kernel-targets-bc425.txt from the census at 18b7c5ae1
      (receipts/K/census-bc425-targets.json, reading the selector recheck): lane K's
      filter with the arity widened from 7 to 8, the top ten by projected orbits, 1,494
      down to 863. All ten are arity 8. Lane K's target 2 is not among them: its recheck
      penetration, 0.0049995, is under the 0.005 floor, and BC-423 holds it. The
      instrument is lane K's frozen SW9 recipe exactly (--bins 64 --max-rounds 24
      --hull-limit 16 --producer-share 0.6 --split-floor 512 --max-rows 1152
      --split-patience 1 --max-seconds 7000) from the clean run worktree at cebb5d15a, so
      lane K's endpoint7 control under that recipe (K-control-endpoint7,
      PASS_CONTROL_STALLED in 1,244 s, receipts/K/kernel-control-endpoint7.json) covers it
      and no new control runs. An arity-8 closure counts for the certified census but not
      toward H-267's criterion, which is read at arity at most seven. Evidence record
      exp-254, written at the first admission.
  - id: BC-426
    purpose: research
    owner_focus: correctness
    instances:
    - 17
    state: in_progress
    priority: 1
    question: >-
      Do BC-425's two round-cap stalls, targets 3 and 6, close under BC-423's recipe, the
      one that took lane K's target 2 from a round-cap stall to a closure?
    hypotheses:
    - H-267
    budget: >-
      Two runs of at most 7,000 s each on the two slots free at 18:25 UTC, behind BC-425's
      remaining targets, and one verification of at most 4,000 s per closure.
    entry: >-
      The coordinator's re-plan at the 18:25 UTC check-in; this cell committed before
      either run.
    exit: >-
      Both targets run once, verdict as observed: a closure re-proved by the standing
      kernel verifier in full and held as a verified candidate, or a non-closure retained.
      No closure is admitted before the user rules on the control evidence for this
      recipe. A soundness alarm stops the slice.
    bead: think-035m
    depends_on:
    - BC-415
    next_evidence: packing/campaign/agent-sessions/session-182-n17-overnight-lanes.md
    workflows:
    - research-loop
    program: post-optimality-low-n
    parallel_group: n17-overnight-182
    artifacts:
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-254-h267-n17-second-tranche-flags.md
    - packing/campaign/explorations/X048-session-182-overnight/receipts/K/kernel-control-endpoint7-bc423-check.json
    note: >-
      Under BC-418, a future slice added at a check-in, citing BC-423 and exp-254. The
      targets are BC-425's target 3 (side-S0 side-E0 side-S1 side-S2 interior-NW
      interior-W interior-S interior-SE) and target 6 (side-N0 side-S1 side-W2 interior-NW
      interior-W interior-S interior-N interior-SE), both stopped at SW9's 24-round cap with
      producer time unused (exp-254). The recipe is BC-423's verbatim. The argv, from
      packing/ of the clean run worktree at cebb5d15a, is nice -n 10 timeout -k 120 7600
      .venv/bin/python3 -m devtools.check_n17_subpattern --cells CELLS --bins 64
      --max-rounds 48 --hull-limit 16 --producer-share 0.6 --split-floor 512 --max-rows
      2304 --split-patience 1 --core octagon --max-seconds 7000 --save-objects DIR --output
      FILE. Like BC-423's, it differs from SW9's in --max-rounds 48, --max-rows 2304 and
      --core octagon. --max-rows is 2304, BC-423's value, not SW9's 1152. The only control under this recipe is BC-423's endpoint7 control,
      whose run ended INCOMPLETE and whose saved node the checker alone then found
      PASS_SAVED_STALL (receipts/K/kernel-control-endpoint7-bc423-check.json). Lane K's
      target 2 rests on the same receipt and awaits the user's ruling, so every BC-426
      closure is verified and held, not admitted, until that ruling. Both targets are
      arity 8: a closure would count for the census but not toward H-267's arity-7
      criterion. Both closed, and both are held. Target 6 closed at 18:30:04 in 202 s of
      wall (9 rounds, finest row 1/128), and target 3 at 18:35:35 in 538 s (13 rounds,
      finest row 1/256). The standing verifier at cebb5d15a passed each in full, in 124 s
      and 293 s. Both wait in ADMIT-AFTER-CONTROL for the user's ruling, with their
      receipts in receipts/K.
  - id: BC-427
    purpose: research
    owner_focus: correctness
    instances:
    - 17
    state: complete
    priority: 1
    question: >-
      Do the remaining standing flags of arity at most seven, the sixteen with the most
      projected gain against the certified line at 71b1d0363, close under lane K's frozen
      SW9 recipe?
    hypotheses:
    - H-267
    budget: >-
      At most sixteen runs of at most 7,000 s each and one verification of at most 4,000 s
      per closure, on two workers, to the run operator's delegation deadline at
      2026-10-06T07:14:04Z.
    entry: >-
      The coordinator's re-plan at the 18:55 UTC check-in; this cell, exp-256 and the
      frozen target list committed before the first run.
    exit: >-
      The list exhausted, each run's verdict as observed: a closure re-proved by the
      standing kernel verifier in full and admitted, one commit each, or a non-closure
      retained with its node kept. Any soundness alarm or one verifier FAIL stops the
      slice.
    bead: think-035m
    depends_on:
    - BC-415
    next_evidence: packing/campaign/agent-sessions/session-182-n17-overnight-lanes.md
    workflows:
    - research-loop
    program: post-optimality-low-n
    parallel_group: n17-overnight-182
    artifacts:
    - packing/campaign/explorations/X048-session-182-overnight/kernel-targets-bc427.txt
    - packing/campaign/explorations/X048-session-182-overnight/receipts/K/census-bc427-targets.json
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-256-h267-n17-third-tranche-flags.md
    note: >-
      Under BC-418, lane K's third tranche, a future slice added at a check-in and aimed at
      H-267 independently of lane K's target 2. The census at 71b1d0363
      (receipts/K/census-bc427-targets.json, 39,656 states in 5,057 orbits) flags 34
      classes of arity at most seven, target 2 among them. The other 33 are more than the
      sixteen-target cap, so the list is the top sixteen of them by projected orbits
      against that line, 509 down to 43: fourteen of arity 7 and two of arity 6, frozen in
      kernel-targets-bc427.txt. No arity-8 flag fills it. Target 2 is left out because
      BC-423 holds it. H-267's count at arity at most seven is 10,173 orbits
      (receipts/K/census-arity7-after-k9.json, unchanged since s182-k9). Reaching its
      threshold of at most 10^4 needs 173 orbits off that line, and going below it needs
      174. With target 2 admitted, which projects 1,372 there, none more is needed; after
      s182-bc427-t4 it projects 1,344 against the 9,990 line
      (receipts/K/census-arity7-after-bc427-t4.json).
      Without it, any one of the ten listed flags that project at least 174 orbits
      against the arity-7 line (183 to 1,799) would suffice alone. The instrument is lane
      K's frozen SW9 recipe exactly (--bins 64 --max-rounds 24 --hull-limit 16
      --producer-share 0.6 --split-floor 512 --max-rows 1152 --split-patience 1
      --max-seconds 7000) from the clean run worktree at cebb5d15a, so lane K's endpoint7
      control (K-control-endpoint7, PASS_CONTROL_STALLED in 1,244 s,
      receipts/K/kernel-control-endpoint7.json) covers it. A stall stays a stall, with its
      node kept; none is re-run under BC-423's recipe. Evidence record exp-256. Closed
      after target 10 at the coordinator's re-plan: targets 4 and 6 closed and were
      admitted, taking the arity-7 line to 8,191; six stopped at the round cap and two at
      producer fixed points; targets 11 to 16 were not run, since SW9 had stopped five of
      the eight runs finished by then at the cap, the six project 15 to 54 orbits each
      against the certified line, and H-267 was confirmed. Those six and every kept
      cap-stall node are the natural input to BC-423's recipe once the user rules on its
      control.
  - id: BC-428
    purpose: research
    owner_focus: correctness
    instances:
    - 17
    state: complete
    priority: 1
    question: >-
      What does per-state exclusion cost in the 21 strata of the arity8 frame that H-264's
      seed-182 draw never reached, under SW9's frozen adaptive-row recipe?
    hypotheses:
    - H-275
    budget: >-
      At most 31 runs of at most 7,000 s each and one verification of at most 4,000 s per
      closure, on two workers, to the run operator's deadline at 2026-10-06T07:14:04Z.
    entry: >-
      The coordinator's re-plan at the 21:43 UTC check-in after BC-427; this cell, H-275,
      exp-257 and the frozen draw committed before the first run.
    exit: >-
      The list exhausted or the deadline reached, each run's verdict as observed: a closure
      re-proved by the standing kernel verifier in full and admitted, one commit each, or a
      non-closure retained with its node kept; states not run are reported as not run. Any
      soundness alarm or one verifier FAIL stops the slice.
    bead: think-z8an
    depends_on:
    - BC-415
    next_evidence: packing/campaign/agent-sessions/session-182-n17-overnight-lanes.md
    workflows:
    - research-loop
    program: post-optimality-low-n
    parallel_group: n17-overnight-182
    artifacts:
    - packing/campaign/hypotheses/H-275-n17-unsampled-strata-per-state-price.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-257-h275-n17-unsampled-strata.md
    - packing/campaign/explorations/X048-session-182-overnight/kernel-targets-bc428.txt
    - packing/campaign/explorations/X048-session-182-overnight/receipts/U
    note: >-
      Under BC-418, a future slice added at a check-in, following exp-252's report of 21
      unsampled strata (827 orbits) and H-274's closure of all four counted stalls under
      SW9's recipe. Registered under a new hypothesis, H-275, because H-264's claim
      fixes its seed-182 draw and its 32-bin instrument. The draw rule is one state per
      unsampled stratum, and a second from each stratum holding more than the mean of
      827/21 orbits (ten strata), from numpy's default_rng(428) over the strata in name
      order. The run order is a permutation from the same generator, every stratum's
      first state before any second. The 31 states are frozen in
      kernel-targets-bc428.txt, written from receipts/U/draw-bc428.jsonl, which
      receipts/U/draw-bc428.cmd.txt reproduces from receipts/U/frame-arity8.json
      (survey_n17_residue --flag-set arity8 --sample 0 --strata-only) and
      receipts/A/survey-seed182.json. The instrument is SW9's frozen recipe exactly
      (--bins 64 --max-rounds 24 --hull-limit 16 --producer-share 0.6 --split-floor 512
      --max-rows 1152 --split-patience 1 --max-seconds 7000) on whole 17-cell states, so
      BC-424's endpoint-state control under it (PASS_CERTIFIED_STALL,
      receipts/A/kernel-control-endpoint-sw9.json) and lane K's endpoint7 control cover
      it. Admission is the standard one: the standing verifier's full pass and the
      census with the endpoint surviving. Evidence record exp-257. Ended at the deadline
      with exp-257 accepted: 24 of 27 counted draws closed and were admitted; u8 closed
      and was admitted and u1 ended INCOMPLETE at the ceiling; all 19 counted strata
      have a finished counted draw. u31 was not run: new starts stopped at 06:17 UTC
      under the coordinator's session-lease rule, 57 minutes before the registered
      deadline. u29 closed with its verification still running at the verdict; it
      passed at 07:38 UTC and u29 is admitted (25 of 28 counting it). The W2 factual
      review (docs/project/reviews/review-2026-10-06-exp-257-h275.md) confirmed the
      verdict with corrections; the round stopped on its clock and resumes at u31.
      Every non-closure's node is kept.
  - id: BC-429
    purpose: research
    owner_focus: correctness
    instances:
    - 17
    state: complete
    priority: 1
    question: >-
      Is draw 31 of BC-428's frozen draw (mask 6015871, stratum c4/i>=5/d>=8), the one
      state exp-257 never ran, excluded under SW9's frozen adaptive-row recipe within its
      7,000 s ceiling?
    hypotheses:
    - H-275
    budget: >-
      One run of at most 7,000 s and, on a closure, one verification of at most 4,000 s,
      on one worker, inside Session 183's deadline at 2026-10-06T17:07:43Z; a producer
      still running at 16:57:43Z is stopped unless its ceiling ends before the deadline.
    entry: >-
      exp-257's verdict.resume_from, which names draw 31 under its recipe and command;
      this cell, exp-258 and Session 183's record committed and pushed before the run.
    exit: >-
      The run's verdict as observed: a closure re-proved by the standing kernel verifier
      in full and admitted, or a non-closure retained with its node kept; or the timebox,
      recorded as stopped_by timebox with resume_from. A soundness alarm or a verifier
      FAIL stops the slice.
    bead: think-2pjf
    depends_on:
    - BC-428
    next_evidence: packing/campaign/agent-sessions/session-183-n17-draw-31.md
    workflows:
    - research-loop
    program: post-optimality-low-n
    parallel_group: n17-overnight-182
    artifacts:
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-258-h275-n17-draw-31.md
    - packing/campaign/explorations/X048-session-182-overnight/kernel-targets-bc428.txt
    - packing/campaign/explorations/X048-session-182-overnight/receipts/U
    note: >-
      BC-428's continuation at its one unrun draw, under BC-418. The state, the recipe
      and the command are exp-257's unchanged: the 31st line of kernel-targets-bc428.txt
      under --bins 64 --max-rounds 24 --hull-limit 16 --producer-share 0.6 --split-floor
      512 --max-rows 1152 --split-patience 1 --max-seconds 7000, from the clean run
      worktree at cebb5d15a, so BC-424's endpoint-state control and lane K's endpoint7
      control cover it and no new control runs. Admission is the standard one: the
      standing verifier's full pass and the census with the endpoint surviving. Evidence
      record exp-258. Complete
      with exp-258 accepted: draw 31 closed in 577 s of wall and 547 s of process CPU, the
      standing verifier passed it in full in 266 s, and s183-bc429-u31 is admitted, the
      census at 36,784 states in 4,685 orbits with the endpoint surviving. Every one of
      BC-428's 31 draws now has a verdict; counted with exp-257's, 26 of 29 counted draws
      closed.
---
# Agenda 042: The n11 Settlement Ladder and Low-n Angles

[Session 156](../agent-sessions/session-156-w3-overnight-n11-settlement.md) reviewed PR
230’s three explorations and opened two more.
The review’s central finding changes what counts as progress at n11: once $s(11)>31/8$
is known, any theorem that closes the gap to Trump’s $U$ is the whole problem, and no
counting certificate can reach $U$ itself.
[X-046](../explorations/X-046-n11-settlement-program.md) therefore lays out a ladder of
restricted-family theorems, each a strengthening of Stromquist’s Theorem 3, and prices
its first rung tonight.
[X-047](../explorations/X-047-low-n-angles-after-the-parent-core-advance.md) maps where
the additive route dies at each low n and selects the two stock-instrument runs that
decide the most.

## Order of Work

| Chunk | Clock (PT) | n11 lanes | Low-n lanes |
| --- | --- | --- | --- |
| 1 | 01:15–03:30 | BC-375 build and controls; BC-376 derivation | BC-378 and BC-379 stock runs |
| 2 | 03:30–05:45 | BC-375 frozen run; Fable review of its contract; BC-377 census | BC-380 build if a slot is free |
| Wind-up | 05:45–07:00 | Terminal records, dispositions and handoff | — |

No more than about three sub-agents run at once.
A lane that finishes early frees its slot for the next ready item in priority order.

## After R052

Session 159’s planning block, BC-385, added six commitments after R052 was integrated;
the [plan](../../../docs/project/specs/active/plan-2026-09-25-after-r052-planning.md)
keeps the assessments behind them.
Each runs within about three agents at once.

| Step | n17 and low-n lanes | n11 lanes |
| --- | --- | --- |
| Day | BC-387’s lemma review; BC-386’s cap lift, landed as a reviewed commit | BC-388’s census build |
| First night | BC-386’s full native run on 2 workers; BC-387’s searches in any free slot | BC-388’s census on 7 workers |
| Next | BC-391 in idle slots | BC-389’s build, then BC-390’s night; a Fable max reading of BC-388 and BC-389 selects BC-384’s design |

## After 4.640020

Two days later Kleddamag’s v1.1.0 proved $s(17) > 4.640020$ and wand125 published
rectangle certificates past every low-n rung here.
The planning block BC-392
([plan](../../../docs/project/specs/active/plan-2026-09-27-after-4640020-overnight.md))
retired BC-386 and BC-391 as superseded, retargeted BC-387 to $4.65$ in clique-weighted
form, and reordered the nights around what is launcher-only today.
Later the same day Kleddamag’s $s(17) > 4.66001$ (`57519bb`) superseded $4.640020$; the
[4.66001 review](../../../docs/project/reviews/review-2026-09-27-n17-kleddamag-466001.md)
moved BC-393 to that certificate’s 2,168 rows and BC-387 (H-248) to $4675/1000$ and
$467/100$, its $4.65$ and $4.66$ targets refuted by the certificate itself.

| Step | n17 and low-n lanes | n11 lanes |
| --- | --- | --- |
| Tonight | BC-394’s ladders at n = 82 and n = 50 on 2 workers; BC-395 at n = 12 in the slot that frees | BC-390 on 8 workers, resumed by subtree if needed |
| Day | BC-393’s loader, atom and cap lift as a reviewed commit; BC-387’s search and checker driver | BC-388’s census build |
| Second night | BC-393 on 2 workers; BC-387’s searches in the gaps | BC-388 on 7 workers |
| Next | The ladders’ top rungs through the wand125-format intake | BC-389’s build; the Fable max reading that selects BC-384’s design |

## October 1 W10 Selection

Session 165 selects BC-397 before new n17 endpoint or global searches.
It reuses a retained rational upper certificate, with independent admission still
pending. The following disposition controls this overnight queue; historical experiments
and other sessions’ open beads are preserved.

| Existing commitment | Overnight disposition |
| --- | --- |
| BC-384, BC-388, BC-389, BC-390: n11 settlement instruments | Not selected: T-060 now supplies the accepted global result. These may support proof simplification, but no longer compete as open-optimality searches. |
| BC-391: n21 decimal ladder | Retired as a scientific target: accepted s(21) = 5 supersedes another sub-endpoint rung. |
| BC-396: n45 endpoint transfer | Retired as an open target: T-053 supplies accepted s(45) = 7. Preserve the old blocked instrument record. |
| BC-380: parent-centre clip | Deferred until a selected geometric discriminator needs it. |
| BC-386, BC-393: native certificate replay | Supporting verification work; do not displace n17 geometry or duplicate existing source replays. |
| BC-387 / H-248: capacity-one ceiling | Retained, without a duplicate hypothesis. The full clique condition and a bounded ready producer are prerequisites. |
| BC-394: n50/n82 ladders | Outside this night’s n17/low-n target axes. |
| BC-395: n12 ladder | Deferred: first decide the available exact additive obstruction and conditional route. |

The secondary n12 side-4 dual replay is not admitted yet: its portable worker setup,
nonnegative-weight guards and exact target assertions need review under `think-q5tt`.
n20 lacks a concrete conditional saving above 0.89474919732, so it remains deferred.
The
[W3 review](../../../docs/project/reviews/review-2026-10-01-post-optimality-w3-opening.md)
records the source and mathematical reasons.

## October 1 Checkpoint After PR 265

Session 166 ran BC-405, a W10 checkpoint on the merged PR 265 record, and selects
**BC-406** (`think-c7kv`) as the coordinating entry.
The
[route review](../../../docs/project/reviews/review-2026-10-01-n17-route-after-pr265.md)
holds the assessment, the evidence status and the handoff reading order.

| Commitment | Disposition |
| --- | --- |
| BC-402 / H-258: common-core stress | Unblocked, lane A1. Exploratory checks find the candidate correct; repair the identity proof within the frozen criterion. |
| BC-407 / H-261: local minimum modulo sliders | New, lane A2 after BC-402. Defines the capture target. |
| BC-408 / H-262: cuts and charge floors | New, lane B, parallel with A1. Decides whether the hybrid route is affordable. |
| BC-409 / H-265: catalogue polynomial | New, lane C, parallel and mechanical. |
| BC-410 / H-263: endpoint-adapted cover | Tentative until BC-408 reports. |
| BC-411 / H-264: exclusion cost per leaf (`think-11ma`) | Re-scoped to a cap at or above the endpoint and a uniform residue sample; tentative until BC-408 and BC-410. |
| BC-387 / H-248: capacity-one ceiling | Unchanged; eligible beside lane B when capacity allows, since it decides whether pure counting is dead. |

The capture prototype and any strengthening of the conditional theorem wait for H-261’s
radius and the BC-410 cover.

## October 5 n17 Overnight

[Session 182](../agent-sessions/session-182-n17-overnight-lanes.md) runs the
[n17 overnight plan](../../../docs/project/specs/active/plan-2026-10-05-n17-overnight.md)
under BC-418, with three cells registered before the first target run.

| Cell | Lane | Disposition |
| --- | --- | --- |
| BC-419 / H-264: per-state price | A, two compute slots | H-264 rewritten in place with `instrument_ready: true`; the seed-182 draw of 12 states, 10 counted. |
| BC-420 / H-267: flag certification | K, one compute slot, two when slot 4 opens | Nine kernel targets frozen in projected-gain order; the branch-and-bound queue waits for slot 4. |
| BC-421 / H-273: distance-2 orbits at the cap | Slot 4, one worker | Ten shards of the 95 distance-2 orbits through the float survey; a placement stops the lane for an exact check. |
| BC-422: OR-12 efficiency block | No compute | Gate walls from the registration’s validation runs; per-row costs from the lanes’ receipts. |
| BC-423 / H-267: K-k2 with lane D’s settings | Lane K’s freed slot | Added at the 11:27 check-in: 48 rounds, 2,304 rows, octagon core; the endpoint7 control first under the same settings. |
| BC-424 / H-274: lane A’s stalls under adaptive rows | Lane A’s freed slots, after BC-423 and lane E | The four counted stalls frozen at registration, the endpoint-state control first under SW9’s recipe. |

BC-421 is lane E (H-273, near-endpoint sizing), registered when slot 4 opened.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
