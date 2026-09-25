---
title: agenda-042 — overnight n11 settlement ladder and low-n angles after PR 230
softschema:
  contract: packing.squares:ExperimentAgenda/v1
  schema: ../schemas/agenda.schema.yaml
  envelope: agenda
  status: enforced
agenda:
  id: agenda-042
  title: Overnight n11 Settlement Ladder and Low-n Angles After PR 230
  updated: '2026-09-25'
  status: active
  objective: >-
    Turn PR 230's W3 review and the two explorations it led to, X-046 and X-047, into
    one night of bounded work. At n11 no counting certificate can prove equality and
    Kleddamag's certificate has no side headroom, so the night starts the verified
    settlement ladder instead: rung 0 of H-112 (Trump is globally optimal at its own
    angle), a quantified capture radius around Trump, and a repaired census of minima
    near U. At low n the additive-ceiling map selects n21 at 4.88 as the one material
    point-certificate rung and n12's additive ceiling as a decisive negative; the
    parent-centre clip that would carry both further is built as a W7 instrument. At
    most about three sub-agents run at once: Opus 5.5 builds and runs, Fable extra-high
    does the mathematics and reviews each chunk, and Fable max reviews anything that
    would move a bound.
  items:
  - id: BC-374
    purpose: research
    owner_focus: insight
    instances: [11, 12, 17, 18, 19, 20, 21, 26, 29]
    state: complete
    priority: 0
    question: >-
      Which of PR 230's 31 shaped candidates, and which new directions, could move n11
      significantly or settle it, and which distinct angles fit the other small cases?
    hypotheses: [H-236, H-237, H-238, H-239, H-240, H-241]
    budget: >-
      Session 156 phases 1 and 2: four reviews of PR 230, a Fable max n11 lane and a
      Fable extra-high low-n lane, then codification, about two hours in all.
    entry: PR 230 published with a passing hosted checkpoint and no selected entry.
    exit: >-
      X-046 and X-047 retained, the selected directions registered as H-236 to H-241,
      and the commitments below given beads and parallel groups.
    bead: think-nbij
    depends_on: []
    next_evidence: >-
      docs/project/reviews/review-2026-09-23-pr230-w3-directions.md, X-046 and X-047.
    workflows: [insight-iteration, review-planning-oversight]
    program: n11-settlement
    artifacts:
    - docs/project/reviews/review-2026-09-23-pr230-w3-directions.md
    - packing/campaign/explorations/X-046-n11-settlement-program.md
    - packing/campaign/explorations/X-047-low-n-angles-after-the-parent-core-advance.md
    parallel_group: overnight-planning
    note: >-
      H-121 (angle merging) is recommended for retirement as a route: X-046 argues it
      is the conjecture restated. That disposition is left to the owner.
    outcomes:
    - scope: The W3 review and codification of PR 230's directions.
      classification: achieved
      result: >-
        No fatal error in PR 230. Settling n11 is verified global optimization with the
        eleven angles as the bottleneck; the first rung is fixed-angle optimality at
        Trump's angle. Kleddamag's certificate carries no transferable slack at U. At
        low n, additive headroom is about 0.001 at n12, about 0.01 at n18 to n20 and
        about 0.036 at n21.
      evidence:
      - docs/project/reviews/review-2026-09-23-pr230-w3-directions.md
      - packing/campaign/explorations/X-046-n11-settlement-program.md
      - packing/campaign/explorations/X-047-low-n-angles-after-the-parent-core-advance.md
      disposition: retire-success
      follow_up: null
  - id: BC-375
    purpose: research
    owner_focus: correctness
    instances: [11]
    state: complete
    priority: 1
    question: >-
      Does a fixed-shape cell tree with rotational cores and exact leaf certificates
      prove H-236 on the half-tangent box of half-width 10^-6 around Trump's tilt, and
      how many nodes does it need?
    hypotheses: [H-236]
    budget: >-
      Opus extra-high, four to five hours to build and control the driver and its
      independent reader, then at most two hours or 10^6 nodes on the box; Fable
      extra-high reviews the certificate contract in the next chunk.
    entry: X-046's design; exact_lp, the uniform-cell reader and the BC-240 local theorem.
    exit: >-
      A certificate accepted by the independent reader with both controls passing, a
      verified counterexample candidate, or an unresolved leaf list with the node count
      at the declared cap.
    bead: think-ie35
    depends_on: []
    next_evidence: >-
      The frozen instrument digests and the run output, admitted from attic/rung0/ into
      results/agenda-042/.
    workflows: [pipeline-improvement, research-loop]
    program: n11-settlement
    artifacts:
    - packing/campaign/hypotheses/H-236-n11-fixed-angle-global-optimality-at-trump.md
    parallel_group: overnight-n11-a
    note: >-
      The node count prices H-112 and every later rung; a bounded negative at the cap is
      a result about the instrument, not about n11.
    outcomes:
    - scope: H-236 on the half-tangent box around Trump's tilt, frozen run and two resumes (exp-231).
      classification: time-limited
      result: >-
        198 of 256 subtrees closed on 1.19e8 nodes with every checked certificate
        accepted and three Trump-degenerate leaves; 58 subtrees remain at the wall cap and
        no leaf below U appeared. The tree is about a thousand times X-046's estimate, so
        rung 1 needs a stronger relaxation.
      evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-231-h236-rung-zero-cell-tree.md
      - docs/project/reviews/review-2026-09-23-rung0-certificate-contract.md
      disposition: continue
      follow_up: think-ie35
    - scope: H-236, the 58 remaining subtrees and the reader over the complete tree (exp-232).
      classification: achieved
      result: >-
        All 256 subtrees closed; the independent reader accepted the whole tree
        (119,556,859 leaf certificates, 19,883,887 branch nodes, three Trump-degenerate
        leaves, no unresolved leaf). H-236 is confirmed at its registered scope, pending
        BC-241 for the local theorem its terminal leaves use.
      evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-232-h236-rung-zero-closed.md
      disposition: retire-success
      follow_up: think-6w2y
  - id: BC-376
    purpose: research
    owner_focus: insight
    instances: [11]
    state: complete
    priority: 1
    question: >-
      Do exp-013's exact stresses and a second-order remainder certify side at least U
      on a sup-norm ball around Trump's pose larger than the BC-240 radius?
    hypotheses: [H-237]
    budget: Fable extra-high, about four hours.
    entry: The exp-013 tangent-cone record, the BC-240 packet and exact_jets.
    exit: >-
      Explicit rational constants with a replayable tool, or a bounded negative naming
      the binding constant.
    bead: think-cj7r
    depends_on: []
    next_evidence: packing/cases/trump11/capture_radius.py and its receipt.
    workflows: [research-loop]
    program: n11-settlement
    artifacts:
    - packing/campaign/hypotheses/H-237-n11-trump-angular-capture-radius.md
    parallel_group: overnight-n11-b
    note: A confirm needs a Fable max adversarial review before it is used as a leaf.
    outcomes:
    - scope: H-237 by the growth-cone route over all 128 branches and 66 faces (exp-227).
      classification: bounded-negative
      result: >-
        An exhaustion lemma caps every per-row-remainder certificate at the BC-199
        modulus, and the exact computation confirms it on all 8,448 faces; the growth
        minimum 0.05177 is healthy, but the route cannot exceed rho. Along the binding
        direction 36 of 42 rows do not recover at second order, so the loose part is the
        remainder model.
      evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-227-h237-trump-growth-cone-capture-radius.md
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-042/exp-227-h237-growth-cone-and-route-radius.json
      disposition: retire-negative
      follow_up: null
  - id: BC-377
    purpose: research
    owner_focus: insight
    instances: [11]
    state: complete
    priority: 2
    question: >-
      With a descent filter that rejects the X-046 stalls, does any census minimum with
      three or more orientation classes lie below Stromquist's value?
    hypotheses: [H-238]
    budget: Opus extra-high, three to four hours, in the second chunk.
    entry: A free agent slot; X-046 probes C and D as controls.
    exit: >-
      A census table of verified descent-stable minima, or a verified three-class
      minimum below 3.885618.
    bead: think-cdc2
    depends_on: []
    next_evidence: The census receipt under results/agenda-042/.
    workflows: [pipeline-improvement, research-loop]
    program: n11-settlement
    artifacts:
    - packing/campaign/hypotheses/H-238-n11-no-third-class-minimum-below-stromquist.md
    parallel_group: overnight-n11-c
    note: Support, never proof; its kill would make the three-orientation rung mandatory.
    outcomes:
    - scope: H-238 on 1,000 jolted starts about Trump and Stromquist (exp-228).
      classification: achieved
      result: >-
        Support only, as registered: no descent-stable minimum with three or more
        classes below 3.885618; all 85 such quench endpoints descend. New minima within
        U + 0.02: a two-class 0/41.56 degree packing at 3.8867460 and a genuine
        three-class packing at 3.8943219.
      evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-228-h238-descent-filtered-census.md
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-042/exp-228-h238-census-minima.json
      disposition: retire-success
      follow_up: null
  - id: BC-378
    purpose: research
    owner_focus: insight
    instances: [21]
    state: complete
    priority: 2
    question: Does a window-enriched point certificate retain at n21, side 122/25, below mass 21?
    hypotheses: [H-240]
    budget: >-
      Opus high runs the stock column generator for one or two runs of at most 3,600 s
      each beside BC-379, then the decision gate.
    entry: H-240 registered; stock instruments.
    exit: >-
      RETAINABLE with mass below 21, then a Fable max W2 review before any register
      entry; or two site sets converging at 21 or above.
    bead: think-gkki
    depends_on: []
    next_evidence: The run log, frozen certificate and decision receipt under results/agenda-042/.
    workflows: [research-loop]
    program: low-n-angles
    artifacts:
    - packing/campaign/hypotheses/H-240-n21-additive-certificate-at-4-88.md
    parallel_group: overnight-low-n
    note: A retain would move s(21) from 4.85 to 4.88, the largest low-n point rung left.
    outcomes:
    - scope: H-240 on three site sets at n=21, side 122/25 (exp-229).
      classification: achieved
      result: >-
        Set C's point certificate (1,228 atoms, mass 20.145724) is RETAINABLE from both
        routes of decide_certificate at least cell mass 250001/250000. Set B converged
        but its interval route stalled on a degenerate seam and refused; set A reached
        its deadline. The register entry waits for the Fable max W2 review.
      evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-229-h240-n21-point-certificate-122-25.md
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-042/exp-229-n21-122-25-receipt.md
      disposition: continue
      follow_up: think-gkki
  - id: BC-379
    purpose: research
    owner_focus: correctness
    instances: [12]
    state: complete
    priority: 2
    question: Does the cutting loop certify an additive ceiling at n12, side 39609/10000?
    hypotheses: [H-241]
    budget: The same Opus high agent as BC-378, one cutting run of about 90 minutes plus the readers.
    entry: H-241 registered; T-017's certificate as the seed.
    exit: A proved ceiling of at least 12 accepted by both readers, or a settled value below 12.
    bead: think-xmm4
    depends_on: []
    next_evidence: The cutting-run log and ceiling receipt under results/agenda-042/.
    workflows: [research-loop]
    program: low-n-angles
    artifacts:
    - packing/campaign/hypotheses/H-241-n12-additive-route-dead-above-3-9609.md
    parallel_group: overnight-low-n
    note: A confirm is a decisive negative about a method and leaves n12 to thresholds or structure.
    outcomes:
    - scope: H-241, three cutting legs at n=12, side 39609/10000 (exp-230).
      classification: time-limited
      result: >-
        No proved ceiling: the best family totals were 10.704 and 9.878 against 12,
        while the unconverged row objective stayed near 11.98. Neither criterion was
        reached; a later attempt needs a converged row loop or a larger family support.
      evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-230-h241-n12-additive-ceiling-3-9609.md
      disposition: defer-dependency
      follow_up: think-xmm4
    - scope: H-241 round 2, the warm-started cutting loop with more rows and a larger support (exp-233).
      classification: bounded-negative
      result: >-
        The row loop converged at a covering value of 11.980175 < 12 with no family
        reaching 12, so H-241 is rejected as registered: the additive route at n12 is not
        shown dead above 3.9609. Freezing the converged covering for the stock gate is a
        cheap follow-up, not selected.
      evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-233-h241-n12-ceiling-settles-below-12.md
      disposition: retire-negative
      follow_up: null
  - id: BC-380
    purpose: tool_validation
    owner_focus: correctness
    instances: [12, 18, 21]
    state: ready
    priority: 3
    question: >-
      Can a direction-dependent parent-centre clip behind colgen's clip parameter, and a
      converter from a frozen clipped certificate to a ParentCoreCertificate, pass T-017
      re-decision, a planted undercharged pose and the closed-boundary band?
    hypotheses: []
    budget: Opus extra-high, several hours, when a slot frees after BC-378 and BC-379.
    entry: X-047's instrument specification.
    exit: >-
      An admitted instrument with its three controls passing, ready for H-240's
      successor at 4.9; a W2 review before its first target run.
    bead: think-m9iz
    depends_on: []
    next_evidence: parent_clip.py, freeze_to_parent_core.py and their tests.
    workflows: [pipeline-improvement]
    program: low-n-angles
    artifacts:
    - packing/campaign/explorations/X-047-low-n-angles-after-the-parent-core-advance.md
    parallel_group: overnight-low-n
    note: The first target runs of the clip are a later session's registered hypotheses.
    outcomes:
    - scope: The ParentClip build, dispatched at 03:10 PT.
      classification: never-opened
      result: >-
        The lane was stopped by the harness session quota at about 03:15 PT before it
        wrote any file; no instrument exists. It remains the enabling build for the n21
        4.9 and n18 4.70 rungs.
      evidence:
      - packing/campaign/agent-sessions/session-156-w3-overnight-n11-settlement.md
      disposition: defer-dependency
      follow_up: think-m9iz
  - id: BC-381
    purpose: research
    owner_focus: correctness
    instances: [11]
    state: complete
    priority: 1
    question: >-
      Does a Fable max adversarial W2 review of the closed rung-0 tree (exp-232) accept
      H-236 at its registered scope, and what register entry, rated by epistemics.md,
      does it support?
    hypotheses: [H-236]
    budget: One Fable max review lane, daytime, reading the retained reader verdict and the 5.5 GB tree in place.
    entry: exp-232 closed with the reader's verdict retained; the rung-0 contract review of 2026-09-23.
    exit: An accepting or rejecting review, and a register entry or a stated reason for none.
    bead: think-6w2y
    depends_on: []
    next_evidence: A dated review under docs/project/reviews/ and, if accepted, a results.yaml row.
    workflows: [factual-review]
    program: n11-settlement
    artifacts:
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-232-h236-rung-zero-closed.md
    parallel_group: n11-rung0-review
    note: The terminal leaves use BC-240's first clause, verified and exact since BC-382 closed BC-241.
    outcomes:
    - scope: The Fable max W2 review of the closed rung-0 tree and the register decision.
      classification: achieved
      result: >-
        Accepted, with the scope split: the machine-verified reduction to Trump's ball is
        T-035 (V4/C5/S3), and the composed optimality theorem, which adds BC-240's audited
        first clause, is T-036 (V3/C2/S3). Eleven subtrees re-replayed independently and
        all 259 archived files match the manifest. "First global optimality statement in
        any n = 11 family" was narrowed, since Stromquist's 0/45-degree bound is earlier.
      evidence:
      - docs/project/reviews/review-2026-09-24-rung0-closed-tree.md
      - packing/frontier/results.yaml
      disposition: retire-success
      follow_up: null
  - id: BC-382
    purpose: research
    owner_focus: correctness
    instances: [11]
    state: complete
    priority: 1
    question: >-
      What did BC-241 leave open on the BC-240 isolation packet, and does an independent
      radius-generator replay close it, so that results ending in Trump-degenerate leaves
      no longer carry the pending-BC-241 qualifier?
    hypotheses: []
    budget: One Fable extra-high lane; the radius replay is about six minutes of CPU.
    entry: The BC-240 packet, the BC-241 review, and exp-227's method-distinct modulus control.
    exit: A dated review closing BC-241 or scoping exactly what remains retained-record-dependent.
    bead: think-mlz3
    depends_on: []
    next_evidence: docs/project/reviews/review-2026-09-24-bc241-closure.md
    workflows: [factual-review]
    program: n11-settlement
    artifacts:
    - packing/cases/trump11/isolation-theorem.md
    parallel_group: n11-lock-in
    note: Every rung of the settlement ladder closes its Trump leaves with BC-240's first clause.
    outcomes:
    - scope: BC-241's open obligations on the BC-240 packet.
      classification: achieved
      result: >-
        A full radius-generator replay reproduced BC-199 on all 4,954 values, the
        method-distinct capture_radius control confirmed the weighted modulus on all 8,448
        faces to 32 digits, and BC-241's checker accepts with its mutations rejected.
        BC-240's first clause, the one rung leaves use, is verified and exact; per-face dual
        witnesses are recomputed rather than retained and the gap cap is single-source and
        non-binding.
      evidence:
      - docs/project/reviews/review-2026-09-24-bc241-closure.md
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-042/bc382-isolation-radius-replay.json.gz
      disposition: retire-success
      follow_up: null
  - id: BC-383
    purpose: research
    owner_focus: insight
    instances: [11]
    state: complete
    priority: 1
    question: >-
      What does the rung-0 cell tree cost on boxes away from Trump's tilt, and does rung 1
      (H-112) become a tiling computation or need a stronger relaxation first?
    hypotheses: [H-242]
    budget: >-
      Opus extra-high builds an additive parameterized box preset with h236 unchanged, a
      short Fable review admits it, then one overnight CPU pilot on about nine workers.
    entry: exp-232's closed tree and its cost; the reviewed instrument contract.
    exit: >-
      Per-box closed/unresolved verdicts and node counts from the reader for the pilot
      boxes, and a pricing of H-112.
    bead: think-6b12
    depends_on: []
    next_evidence: The pilot receipts under results/agenda-042/ and an experiment record.
    workflows: [pipeline-improvement, research-loop]
    program: n11-settlement
    artifacts:
    - packing/campaign/hypotheses/H-242-n11-rung1-pilot-cost-away-from-trump.md
    parallel_group: n11-rung1-pilot
    note: A measurement that prices H-112; it moves no bound.
    outcomes:
    - scope: H-242, eighteen boxes at six tilts and three widths, 150,000 nodes per subtree (exp-234).
      classification: bounded-negative
      result: >-
        No box closed at the declared cap; every box closed about two-thirds of its
        measure (0.624 to 0.672) for about four million nodes, with no trend in width or
        tilt. Rung 1's cost lives in the fixed-angle centre enumeration, so a stronger
        per-node bound is the prerequisite for H-112; wide boxes cost no more than narrow
        ones once it exists.
      evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-234-h242-rung1-pilot.md
      disposition: retire-negative
      follow_up: think-ggk5
  - id: BC-384
    purpose: research
    owner_focus: insight
    instances: [11]
    state: blocked
    priority: 1
    question: >-
      Which stronger per-node bound for the fixed-angle cell tree closes a rung-0 subtree
      or an exp-234 pilot box in orders of magnitude fewer nodes, with the reader's
      certificate contract unchanged or reviewed?
    hypotheses: []
    budget: A W3 design note, then a W7 prototype measured against retained pilot and rung-0 trees.
    entry: exp-234's flat response to width and tilt; X-046's second-order dual bound; exp-228's descent filter.
    exit: A measured node-count reduction on retained boxes, or a scoped reason none of the candidates helps.
    bead: think-ggk5
    depends_on: [BC-388, BC-389]
    next_evidence: A design note and a benchmark receipt.
    workflows: [insight-iteration, pipeline-improvement]
    program: n11-settlement
    artifacts:
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-234-h242-rung1-pilot.md
    parallel_group: n11-rung1-relaxation
    note: >-
      Rung 1 (H-112) is priced out with the present relaxation; this is its prerequisite.
      Narrowed by BC-385: the design note chooses between parametric-in-tilt
      certificates, which certify a midpoint dual vector over a whole tilt interval by
      univariate polynomial positivity, and per-square counting at each node, after
      BC-388 and BC-389 report. The second-order dual bound, the descent filter,
      symmetry reduction and LP warm starts are retired as BC-384 candidates; node
      throughput is a separate efficiency item.
  - id: BC-385
    purpose: research
    owner_focus: insight
    instances: [11, 12, 17, 21]
    state: complete
    priority: 0
    question: >-
      What else do R052 at n17 and the closed rung 0 at n11 make possible, and which
      bounded commitments should follow them?
    hypotheses: [H-243, H-244, H-245, H-246, H-247]
    budget: >-
      Session 159's W10 planning block: two Fable max assessments in parallel, one per
      case, each with at most ten minutes of probes, then codification.
    entry: R052 integrated at V4/C3 with its review; rung 0 closed as T-035 and T-036; exp-234 retained.
    exit: >-
      The plan document retained, the selected directions registered as H-243 to H-247,
      and BC-386 to BC-391 given beads, prices, stop conditions and an order.
    bead: think-f0if
    depends_on: []
    next_evidence: docs/project/specs/active/plan-2026-09-25-after-r052-planning.md
    workflows: [review-planning-oversight]
    artifacts:
    - docs/project/specs/active/plan-2026-09-25-after-r052-planning.md
    - docs/project/reviews/review-2026-09-25-n17-guzhou-r052.md
    parallel_group: after-r052-planning
    note: >-
      Not selected: a first-party n17 producer beyond 4.62002 waits for BC-387 and is
      reconsidered only if the ceiling is at least 4.64; the n12 parent-core transfer
      waits for BC-387's n12 price and BC-380's parent clip; any n11 lower-bound
      increment stays under the owner's 2026-09-14 hold.
    outcomes:
    - scope: The Session 159 planning block after R052.
      classification: achieved
      result: >-
        R052's certificate is nearly saturated and its public ladder is flattening, so a
        first-party increment is not worth building until the architecture's ceiling is
        priced; at n11 the cost of rung 1 is the relaxation, so a per-node bound must
        price all pairs at once. Six commitments were selected, and BC-384 was narrowed
        to two designs. Nothing in the block moves a bound.
      evidence:
      - docs/project/specs/active/plan-2026-09-25-after-r052-planning.md
      disposition: retire-success
      follow_up: null
  - id: BC-386
    purpose: tool_validation
    owner_focus: correctness
    instances: [17]
    state: ready
    priority: 1
    question: >-
      Does this repository's native coverage engine decide every row of R052's
      certificate at or above its charge once its memory-policy ceilings are lifted
      behind an explicit byte budget, so that R052 can be rated C4?
    hypotheses: []
    budget: >-
      Opus extra-high about two hours to lift the ceilings, add a contract test admitting
      R052's dimensions and re-baseline the n11 native audit; about 15 CPU-hours, about
      eight hours of wall on the tool's two workers; Fable extra-high checks the transfer
      contract.
    entry: >-
      R052 at V4/C3; packing/devtools/verify_guzhou_r052_native.py; the sizing rows
      that certified at or above the charge in Session 159.
    exit: >-
      Every row decided by the native engine on a clean reviewed commit, with the byte
      budget recorded in the receipt, or the rows it refuses listed as refusals.
    bead: think-amx8
    depends_on: []
    next_evidence: A native-decision receipt for R052 under results/agenda-042/ and the reviewed cap-lift commit.
    workflows: [pipeline-improvement, factual-review]
    program: low-n-angles
    artifacts:
    - docs/project/reviews/review-2026-09-25-n17-guzhou-r052.md
    - packing/devtools/verify_guzhou_r052_native.py
    parallel_group: n17-native-c4
    note: >-
      The cap lift lands as a reviewed commit before the run starts. R052 has zero
      slack, so a stalled or seam row is possible; it is recorded as a refusal, never as
      a negative.
  - id: BC-387
    purpose: research
    owner_focus: insight
    instances: [17, 12]
    state: ready
    priority: 1
    question: >-
      Does the capacity-one ceiling lemma survive review, and do triangle-free overlap
      families of 34 squares at 463/100 and 465/100, and of 24 at 397/100 and 399/100,
      exist under an exact checker?
    hypotheses: [H-243, H-244]
    budget: >-
      Fable extra-high lemma review about one hour; Opus extra-high build of the search
      and exact checker four to six hours; the searches run in minutes wherever a slot
      is free.
    entry: The lemma as derived in the plan document; R052's certificate and Bidwell's packing as the two ends.
    exit: >-
      An accepting or rejecting lemma review, then an exact-checker verdict on a family
      at each target or a search budget spent without one.
    bead: think-68la
    depends_on: []
    next_evidence: A dated lemma review under docs/project/reviews/, then the checker receipts under results/agenda-042/.
    workflows: [factual-review, pipeline-improvement, research-loop]
    program: low-n-angles
    artifacts:
    - packing/campaign/hypotheses/H-243-n17-triangle-free-34-family-at-4-63.md
    - packing/campaign/hypotheses/H-244-n12-triangle-free-24-family-at-3-99.md
    parallel_group: architecture-ceiling
    note: >-
      Stop if the lemma fails review. No family found is inconclusive, not a negative.
      The price decides the first-party n17 producer (reconsidered only at a ceiling of
      at least 4.64) and the n12 parent-core transfer.
  - id: BC-388
    purpose: research
    owner_focus: insight
    instances: [11]
    state: ready
    priority: 1
    question: >-
      What is the least side f(theta) along the six-axis plus five-common-angle family at
      200 tilts, and on which window is it within 0.01 of U?
    hypotheses: [H-245]
    budget: Opus high about two hours to build the frozen-angle census, then one night on seven workers.
    entry: The exp-228 census driver and quench; H-245 registered.
    exit: A table of f(theta) at 200 tilts with verified witnesses and the window where f(theta) - U < 0.01.
    bead: think-91yk
    depends_on: []
    next_evidence: The census receipt under results/agenda-042/ and an experiment record.
    workflows: [pipeline-improvement, research-loop]
    program: n11-settlement
    artifacts:
    - packing/campaign/hypotheses/H-245-n11-family-side-profile-along-the-tilt.md
    parallel_group: n11-family-profile
    note: None as a stop; it is a measurement that prices BC-389 and BC-384 and moves no bound.
  - id: BC-389
    purpose: research
    owner_focus: insight
    instances: [11]
    state: ready
    priority: 2
    question: >-
      Does a two-class parent-core counting certificate close the rung-1 box at 20
      degrees, half-tangent [0.1758, 0.1768], outright?
    hypotheses: [H-246]
    budget: >-
      Opus extra-high one to two days of build and hours of CPU; Fable extra-high
      reviews the two-class lemma.
    entry: >-
      sqpack.fractional.classcert, the parent-core and threshold separators, and the
      native sweep; exp-234's box at 20 degrees.
    exit: >-
      A native-swept certificate with an accepting lemma review, or the mass still above
      11 after site column generation with two-of-three and three-of-five atoms.
    bead: think-nho8
    depends_on: []
    next_evidence: The frozen certificate, the native sweep receipt and a dated lemma review.
    workflows: [pipeline-improvement, research-loop, factual-review]
    program: n11-settlement
    artifacts:
    - packing/campaign/hypotheses/H-246-n11-two-class-certificate-closes-a-rung1-box.md
    parallel_group: n11-two-class-closer
    note: >-
      Stop when the mass stays above 11 after site column generation with two-of-three
      and three-of-five atoms. Aimed at a box, not at the side, so it is outside the
      owner's hold on n11 lower-bound increments.
  - id: BC-390
    purpose: research
    owner_focus: correctness
    instances: [11]
    state: ready
    priority: 2
    question: >-
      Does the unchanged rung-0 instrument prove H-236's statement on the half-tangent
      box of half-width 10^-4 around Trump's tilt?
    hypotheses: [H-247]
    budget: A launcher only; about 1.7e8 nodes, one night on nine workers, then the reader.
    entry: The fixed_angle_tree box preset and reader at their exp-234 bytes; T-035 and T-036.
    exit: >-
      A reader-closed tree on the widened box, a verified counterexample candidate, or an
      unresolved leaf list at the declared cap.
    bead: think-7c17
    depends_on: []
    next_evidence: The frozen digests, run output and reader verdict under results/agenda-042/.
    workflows: [research-loop]
    program: n11-settlement
    artifacts:
    - packing/campaign/hypotheses/H-247-n11-rung0-widened-to-half-width-1e-4.md
    parallel_group: n11-rung0-wide
    note: Stop if the enclosure reach of a Trump-degenerate leaf meets the local-theorem radius rho.
  - id: BC-391
    purpose: research
    owner_focus: insight
    instances: [21]
    state: ready
    priority: 3
    question: >-
      Does the additive point certificate at n21 reach side 4.89 on stock column
      generation, without the parent clip?
    hypotheses: []
    budget: Opus high, runs of under an hour each, in idle slots.
    entry: >-
      T-034's certificate at 4.88 and the stock column generator; an H-item registered
      for the 4.89 claim before any run.
    exit: >-
      A value below 21 retained by the decision gate, or a converged value of at least 21
      on two site sets.
    bead: think-t50i
    depends_on: []
    next_evidence: The run logs and decision receipts under results/agenda-042/.
    workflows: [research-loop]
    program: low-n-angles
    artifacts:
    - packing/campaign/hypotheses/H-240-n21-additive-certificate-at-4-88.md
    parallel_group: idle-slot
    note: >-
      Register the H-item before the first run. Stop when the value reaches 21 on two
      site sets or when the certificate fails on both.
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

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
