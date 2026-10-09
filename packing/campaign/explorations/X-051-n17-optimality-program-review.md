---
title: X-051 — The n = 17 Optimality Program After Session 186
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-051
  title: The n = 17 Optimality Program After Session 186
  date: '2026-10-09'
  author: Claude Fable 5.1 at max reasoning, W3 insight-iteration lane for the owner; W2 review corrections applied by Claude Opus 5.5; not yet reviewed by the coordinator
  campaign: packing.squares
  brief: >-
    The owner asked for a comprehensive W3 review of everything done so far toward
    s(17) = S* and for the most productive directions toward a foolproof proof or the
    greatest mathematical progress toward one. Read the whole n17 record on main at
    533dd42 and the unmerged PR 464 review, map every proof obligation with its
    evidential status, assess the architecture critically, rank the routes, specify
    what a foolproof package needs, and codify candidate hypotheses H-325 to H-340.
    No target experiment was run; three cheap read-only computations on the cover
    geometry are reported with their arithmetic stated. No bound, verdict or census
    count changes.
  sources:
    - packing/campaign/explorations/X-048-n17-optimality-after-n11.md
    - packing/campaign/explorations/X-046-n11-settlement-program.md
    - packing/campaign/explorations/X-050-fibonacci-torus-and-boundary-information.md
    - docs/project/n17-optimality-explainer.md
    - packing/frontier/n-017.md
    - packing/frontier/results.yaml
    - epistemics.md
    - docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
    - docs/project/reviews/review-2026-10-08-n17-strategy-and-exact-sos.md
    - docs/project/reviews/review-2026-10-08-n17-issue-pattern-reconciliation.md
    - docs/project/reviews/review-2026-10-08-n17-merge-readiness.md
    - docs/project/reviews/review-2026-10-07-n17-session-184-progress.md
    - docs/project/reviews/review-2026-10-07-n17-session-185-progress.md
    - docs/project/reviews/review-2026-10-05-n17-capture-r9.md
    - docs/project/reviews/review-2026-10-05-n17-stall-classification.md
    - docs/project/reviews/review-2026-10-05-guzhou-r071.md
    - docs/project/reviews/review-2026-10-03-n17-local-radius.md
    - docs/project/reviews/review-2026-10-02-n17-local-theorem-recipe.md
    - docs/project/reviews/review-2026-10-02-n17-local-half-composition.md
    - docs/project/reviews/review-2026-10-02-n17-capture-feasibility.md
    - docs/project/reviews/review-2026-10-02-n17-widened-projection-scope.md
    - docs/project/reviews/review-2026-10-02-n17-kernel-adaptation-spec.md
    - docs/project/reviews/review-2026-10-02-n17-residue-process.md
    - docs/project/research/research-2026-10-07-n17-session-186-w3-strategy.md
    - docs/project/research/research-2026-10-07-n17-w3-capacity-and-route-selection.md
    - docs/project/research/research-2026-10-07-n17-proof-interfaces-and-lp-contract.md
    - docs/project/research/research-2026-10-07-n17-shared-centre-lp-readiness.md
    - docs/project/research/research-2026-10-07-n17-global-contact-budget.md
    - packing/resources/web/n11-optimality-2026-09-29/README.md
    - packing/campaign/hypotheses/H-261-n17-local-minimum-modulo-sliders.md
    - packing/campaign/hypotheses/H-273-n17-distance-two-infeasible-at-cap.md
    - packing/campaign/hypotheses/H-275-n17-unsampled-strata-per-state-price.md
    - packing/campaign/hypotheses/H-288-n17-capture-cap-root-join.md
    - packing/campaign/hypotheses/H-323-shared-centre-endpoint-control.md
    - packing/campaign/hypotheses/H-324-shared-centre-explicit-f1-control.md
    - packing/campaign/ledger.md
    - packing/campaign/ideas.md
    - packing/campaign/explorations/X048-session-168-pilots/certified-sub-patterns.yaml
    - packing/campaign/series/series-000-smoke-and-calibration/results/exp-259-current-admitted-residue/partition.json
    - packing/campaign/resource-usage/codex-task-tree-session184-through-20261007T165726Z.yaml
    - packing/campaign/resource-usage/codex-task-tree-session185-final-checkpoint.yaml
    - packing/campaign/resource-usage/codex-task-tree-session186-final-checkpoint.yaml
    - packing/hosted/n17-x048-session-168-certificates.yaml
    - packing/devtools/check_n17_capacity_one_cover.py
    - packing/devtools/n17_shared_centre_lp.py
    - packing/campaign/series/series-000-smoke-and-calibration/results/exp-247-n17-unique-state-cover/run-001/receipt.json
    - packing/campaign/series/series-000-smoke-and-calibration/results/exp-308-n11-corner-cardinality/descriptor.json
    - packing/campaign/explorations/X051-centre-survivors/centre-survivors.json
    - https://github.com/jlevy/squares/pull/473#pullrequestreview-5469083247
    - https://github.com/jlevy/squares/issues/405
    - https://github.com/jlevy/squares/issues/413
    - https://github.com/jlevy/squares/issues/358
    - https://github.com/jlevy/squares/issues/367
    - https://github.com/jlevy/squares/issues/400
    - https://github.com/jlevy/squares/issues/445
    - https://github.com/jlevy/squares/issues/375
    - https://github.com/jlevy/squares/issues/419
    - https://github.com/jlevy/squares/blob/51368bec05b6fa30bebca7b31d0cf3dd0d810c09/docs/project/reviews/review-2026-10-08-n17-global-optimization-and-sos.md
  proposes: [H-325, H-326, H-327, H-328, H-329, H-330, H-331, H-332, H-333, H-334, H-335,
    H-336, H-337, H-338, H-339, H-340]
---
# X-051: The n = 17 Optimality Program After Session 186

**The architecture is right and the record is honest, but the program has spent the last
week on the two parts of the proof that cannot finish it.** Since 5 October the verified
bracket has not moved, the admitted census has moved by two orbits out of 4,685, and the
capture step, the one part of the n = 11 architecture whose n = 17 analogue has no
working engine, has not been run from the actual starting point.
The conditional lemmas, relaxations and readiness controls of Sessions 184 to 186 are
sound and exactly scoped, and fifteen of the mathematical rounds they ran (exp-285 to
exp-312) missed their criteria.
Meanwhile three things the final proof will need in any case have no owner at the
mathematical level: a measurement of how far pure exclusion reaches toward the endpoint,
a terminal theorem of radius larger than $1/5000$, and a composition checker that would
turn the receipts into a theorem.

Computations on the committed cover, corrected and extended by the
[W2 review](https://github.com/jlevy/squares/pull/473#pullrequestreview-5469083247),
change two of the record’s current selections.
The shared-centre LP, the weighted-vertex screen and the proposed incircle SOS keep two
facts about the squares: each centre lies in its assigned cell, and centres are pairwise
at distance at least one.
For every one of the 95 distance-2 orbits, the frozen first eight included, there are
exact rational centres inside the state’s own cells that are pairwise at distance at
least one, and the repository’s own LP checker accepts them.
So the first-eight LP’s outcome is already known (eight exact relaxation survivors, and
no Farkas certificate can exist), and no centre-only method can exclude any distance-2
orbit. On the 24-cell cover every one of the 2,024 cell triples has a product vertex
whose three pairwise squared distances are all at least $1.33$. That vertex satisfies
every constraint of the triple’s encoded system, so no weighted-vertex or SOS
certificate of any order, with or without a ball generator, exists for any triple.
The next mathematical slice should therefore not be the first-eight LP. It should be a
scan of the endpoint’s own occupancy state at caps below $S^\ast$, which measures the
one number the program has never measured: the side at which exclusion alone stops
reaching.

This is a W3 reading of the record.
It certifies nothing, changes no bound, verdict or count, and spends no target budget.
Its own computations are read-only scripts over the committed cover design and
elementary arithmetic.
The per-state centres come from the W2 review; they are retained with a replay recipe in
[section 3.1](#31-centre-only-relaxations-exclude-no-distance-2-orbit), and no
registered experiment has recorded them.
[Evidence Status](#evidence-status) gives the evidential level of each.

## 1. Honest Status Map

The target is $s(17)=S^\ast$, the root of the catalogue’s degree-18 polynomial, with
$S^\ast=4.67553009360455\ldots$. The record on `main` at `533dd42` is:

| Quantity | Value | Where |
| --- | --- | --- |
| Verified bracket | $4.66044275<s(17)\le4.6755300936045509516342148538535054$; gap $0.0150873436$ | [n-017](../../frontier/n-017.md), T-093 and T-065, both `V3/C3` |
| Last lower-bound movement | T-093, 5 October, $+2.75\times10^{-6}$ over T-043; R070’s obstruction leaves R071’s charge $2.5\times10^{-8}$ of runway | [R071 review](../../../docs/project/reviews/review-2026-10-05-guzhou-r071.md) |
| Cover | 24 closed capacity-one cells at $U=1169/250$; $\binom{24}{17}=346{,}104$ states, 43,593 $D_4$ orbits; the family in one state with margin at least $0.002111$ (the receipt’s lower bound; the record rounds it to $0.002112$) | exp-247, H-266 |
| Admitted exclusions | 60 entries: 2 of arity 6, 10 of arity 7, 8 of arity 8, 1 of arity 9, 39 whole 17-cell states | [ledger](X048-session-168-pilots/certified-sub-patterns.yaml) |
| Residue | 36,768 states in 4,683 orbits, the endpoint’s among them; 10.6 per cent of the states and 10.7 per cent of the orbits | exp-274 census |
| Residue by Hamming distance from the endpoint’s state (58-entry partition) | distance 2: 95 orbits, 744 states; 4: 975, 7,664; 6: 1,942, 15,268; 8 and beyond: 1,672 orbits and the endpoint’s own, 13,108 states together | [exp-259 partition](../series/series-000-smoke-and-calibration/results/exp-259-current-admitted-residue/partition.json) |
| Contributor certificates | 33 reported #413 rows and 2 #358 classes, all unadmitted; the 33 #413 rows’ conditional union is 2,234 orbits, 17,604 states, and #358’s C1 and C2 add a separately counted 21 orbits, 148 states; only row 23 touches the distance-2 tail (one orbit) | [reconciliation](../../../docs/project/reviews/review-2026-10-08-n17-issue-pattern-reconciliation.md) |
| Local theorem | capture-target theorem at $r=1/5000$ on $B_W'$; a per-coordinate vector with floor $1/1216$ composes but is held as a component | exp-244, exp-248, [local radius](../../../docs/project/reviews/review-2026-10-03-n17-local-radius.md) |
| Capture | no engine has contracted anything from the cells; pilot 2 from a $1/1024$ box met its falsifier; R9’s discriminating runs unrun | [R9](../../../docs/project/reviews/review-2026-10-05-n17-capture-r9.md) |
| Custody | 204 certificate objects, 2.17 GB, Session 184’s four included, all listed in a manifest and none hosted | [manifest](../../hosted/n17-x048-session-168-certificates.yaml), tracker |

### 1.1 Every obligation, with its status

The statuses use the explainer’s vocabulary: *proved* (an exact argument with its
checking scope stated), *verified* (an exact or outward computation with a replay),
*admitted* (a certificate a standing verifier passed in full), *conditional* (true under
a stated guard that nothing yet delivers), *reported* (a source’s claim, not replayed
here) and *open*.

| Obligation | Status | What remains | Movement since 2 October |
| --- | --- | --- | --- |
| Upper bound and identity of the side | verified and proved: exact endpoint feasible, side is the catalogue’s irreducible degree-18 root | restate T-065 at the exact algebraic value is a registration decision | none needed |
| Frame: every packing of side $\le S^\ast$ embeds in the $U$-container; the centred-container lemma | proved as hand lemmas, sole-Astra reviewed | machine-check or second review; the composed argument should read states in the centred box, as X-048 noted | centred-container lemma written (Session 184) |
| Cover and capacity | verified twice (tool and independent recomputation); the depth-width wall lemma proved and sharp | nothing mathematical; Lean is optional | none needed |
| Census and $D_4$ | verified (Burnside and brute force agree) | nothing | none needed |
| Exclusion of the residue at a cap $\ge S^\ast$ | 89.3 per cent of orbits admitted; 4,683 open | every remaining orbit needs a certificate at a cap at least $S^\ast$, or capture | 4,685 to 4,683 (Tail A, Tail B; two distance-8 orbits, 16 states); contributor rows unadmitted |
| Near-endpoint stage: states feasible at $U$ but not below $S^\ast$ | open; H-273’s float search of all 95 distance-2 orbits found no placement | an exact decision for each such orbit at $U'$ | none |
| Capture into the local box | open; no evidence from the cells; two readings of the box-seeded stall, the box-set reading better supported | an engine, or a terminal theorem large enough that an engine is unnecessary | none; the pull repair has an external executor |
| Local family theorem | proved with one review as the composition of three exact certificates and six hand lemmas | end-to-end machine check; second review; the per-coordinate vector is unregistered | per-coordinate composition at $1/1216$ (3 October); widened feature forcing, apex, cones and one patch, all conditional (7 October) |
| Caps, frame and slider joins | $U'=935106018721/200000000000$ joins the root exactly (H-288); slider box $B_W'$; the $u^\ast$-enclosure charge is a stated obligation | a composed statement naming which cap each certificate uses | cap join verified (7 October) |
| Composition | not written | an obligation table with a checker behind it | the proof-interfaces document lists the joins; no checker |
| Replay from a fresh clone | fails: the objects are not hosted | publication, fetch, representative replay | none; blocked on egress and an owner decision |
| Assurance rungs | every piece has at most one AI review; no human oversight record; T-093 at `V3/C3` | two adversarial reviews and an oversight record per load-bearing piece for rung 4 | none |

### 1.2 What moved and what it cost

Counted from the records, not from narrative:

- **Experiments.** exp-240 to exp-316 (77 rounds since 1 October): 42 accepted, 16
  rejected, 11 unresolved, 7 blocked, 1 abandoned.
  Of the 42 accepted, 17 are readiness, calibration or diagnostic rounds (exp-240, 241,
  259, 268, 272, 273, 276, 277, 280, 288, 290, 294, 309, 310, 313, 314, 316) that moved
  no proof obligation; they are correctly labelled in their own records.
- **Hypotheses.** H-261 to H-324 hold 60 claims of the n17 program: 33 confirmed, 16
  refuted, 7 unresolved, 3 open questions, 1 blocked.
  These counts include H-281, the n = 11 relaunch control; the 59 claims made at n = 17
  itself have 32 confirmations.
  About fifteen of the confirmations are instrument readiness, not mathematics.
  A reader who counts confirmed hypotheses overstates progress by about two.
- **Sessions 184 to 186 (7 to 8 October).** Receipts record 39.20, 14.34 and 21.42
  overlapping agent-hours, each a lower bound: about 75 agent-hours.
  Output: two ordinary exclusions (two orbits), the cap join, the numeric-cap parent,
  three conditional restrictions inside one owner-0 guard (25 of 64 half-angle units of
  one partner at one pose, 22 of 25 rows throughout $h=1/512$, and $15/32$ of owner 6’s
  parameter from two closed centre cases), one feasible relaxation witness, and fifteen
  completed method misses.
  Sixteen research documents and eleven n17 reviews were written on 7 and 8 October.
- **Sessions 182 and 183 (5 to 6 October),** for comparison: 15,953 orbits to 4,685 in
  two overnight sessions on two workers, by arity-7 and arity-8 flags and about three
  dozen whole-state closures under the adaptive-row recipe.
- **The ledger’s shape.** The 21 sub-pattern entries account for 99.9 per cent of the
  309,336 excluded states; the 39 whole-state entries account for 304 states (37 orbits
  of eight states and two of four).
  Per-state closure is a tail method and cannot be the method for 4,683 orbits at
  measured costs of 547 to 4,522 CPU-seconds of production and 257 to 1,899 seconds of
  verification per state: at one CPU-hour per orbit, 4,682 orbits are about 4,700
  CPU-hours (about 2,100 at the measured medians), and the stalls (three of seven
  per-state stalls on 5 October were consistency-limited, two of them at distance 2)
  need a different grammar.

The verified bracket is where it was on 5 October.
Nothing in the week was unsound; what was missing was a reason, stated in advance, why
each round would move an obligation in the table above.

## 2. Critical Assessment of the Architecture

### 2.1 Where the n = 11 analogy holds and where it breaks

The three-part shape transfers: a closed capacity-one cover, exclusion of states by
containment and per-state certificates, capture of the endpoint’s state into a local
theorem. Four things do not transfer, and each is now measured.

- **The endpoint is a family, not a point.** Square 6 is free and squares 5, 11 and 13
  slide at fixed side.
  The local theorem handles this by dropping square 6 and quotienting three slides,
  which is sound and reviewed, but it makes the terminal region a product of a
  45-coordinate box and a slider box, and H-261 as worded stays unresolved because the
  family with squares 5 and 6 exchanged meets its premises outside the box.
  The usable theorem carries a state premise instead.
  This is handled, not open.
- **The soft slope is nine times smaller.** $\kappa_\infty=1/175.8$ against n11’s
  $0.0518$. At the exclusion cap $U$ the first-order feasible set extends about $0.08$
  along the softest direction and about $0.02$ along stiff ones, which is why capture
  needs a second cap $U'$ within $10^{-12}$ of $S^\ast$. The two-cap design is proved
  (H-288) and is not a bottleneck.
  What the small slope does is set the local radius: the ratio test’s radius scales like
  $1/\lVert\lambda\rVert_1$ with $\lVert\lambda\rVert_1=1{,}439$, so the uniform radius
  is about $1/4630$ for the certified duals and at most about $1/4391$ for any
  certificate of the recipe’s form, an exact floor, and no finer curvature lemma buys
  more than a factor of two.
  The terminal region cannot be enlarged by the n11 recipe; it needs a different
  theorem.
- **Pairwise ownership induction has a fixpoint at the box.** R9’s reading of pilot 2 is
  that corner-to-edge links lose the corner recession $\alpha/\sqrt2$, that far-side
  cuts land at the owner’s own box edge, and that this loop is homogeneous in the box
  radius. Four runs at two box scales and four row counts agree.
  The row-driven reading survives only with an angle constant above 290 row widths.
  The record keeps both readings open; this review treats the box-set reading as the
  default until stage 1 of R9 refutes it, because every measured number favours it.
- **Wall crowds and consistency-limited states.** Five squares on a wall of length
  $3.676$ must tilt or stagger by margins of $0.011$ to $0.018$, below the kernel’s
  first-order losses at the rows the per-state runs used, and three of seven per-state
  stalls were consistency-limited: every owner at least 63 per cent supported, so no
  one-partner cut at any row width removes a quarter of any owner.
  Two of those three are distance-2 states.
  The hard tail is hard for a structural reason, not for want of rows.

### 2.2 Single points of failure

1. **Capture has no engine.** The only runs from the actual cells (exp-276, exp-277,
   exp-280) completed one round and left every owner’s orientation interval whole; all
   contraction evidence comes from $1/1024$-box seeds, which assume the hard part.
   The conditional owned-hull, partner-coupling and regional work of Sessions 184 to 186
   fixed owner 0’s pose or guard to make progress at all, and every such result is
   conditional on a guard that no global step delivers.
   If the box-set reading is right, the n11 kernel is not the capture engine at n17, and
   the program has no second engine built.
2. **The terminal theorem is too small for any engine.** Even a working engine must
   deliver 45 coordinates within $1/5000$, or the $1/1216$ vector, in the exact root’s
   frame. The widened projection theorem (angles within about $10^{-2}$, centres within
   $10^{-2}$, features forced) would make the target fifty times larger in angle and is
   scoped as plausible on exploratory LP evidence, but its instrument, a dual-sheet or
   patch certificate over the backbone angles, has never been built and its patch count
   is unmeasured.
3. **The hard tail has no method with a price.** The 95 distance-2 orbits and the
   consistency-limited states resist the pairwise kernel at every row width.
   The branch and bound closes interior crowds but stalled on W7 at 24 million nodes
   because 80 to 85 per cent of its open nodes are held by separating-normal
   disjunctions, and the one hard-tail class a contributor reached (row 23) has no
   published certificate.
   Row 33’s estimated 480 GB certificate for 76 marginal orbits shows that sub-pattern
   branch and bound can be verification-infeasible even when it closes.
4. **Composition is unwritten and replay is impossible.** No checker reads the cover,
   the ledger, the capture and the local theorem together, and no fresh clone can verify
   a single admitted certificate because none is hosted.

### 2.3 Soundness risks and unverified premises

None is a known defect; each is a place where the trusted base is larger or thinner than
a reader would assume.

- The standing kernel verifier imports nothing from the producer’s package, the checker,
  the selector or the branch and bound (its docstring says so and its imports agree),
  but it is one implementation of 1,751 lines: W7 and A were re-proved by second,
  separately written verifiers, and every later kernel admission rests on the standing
  verifier alone. The Rust kernel verifier of PR 410 has receipt parity on seven
  certificates and is unadopted.
  Three closed-cover verifier defects were found and fixed on 3 October after the first
  admissions; the re-verification covered W7, SW9 and N1.
- The branch-and-bound verifier has an open soundness-relevant weakness for externally
  produced certificates (`think-t41a`: arbitrary full-BB intake needs complete
  source-cell enclosure); the new header guard supplies the check for guarded intake,
  but any admission of a contributor BB certificate must pass through it.
- The 39 whole-state admissions rest on the standing verifier’s full pass with no
  per-certificate review, under OR-16 as amended.
  That is a recorded decision, not an error, but it is a different assurance class from
  W7 and A, and the register should say so when the composition is written.
- The capture-target theorem composes machine-certified parts with six hand lemmas that
  have one AI review; the centred-container lemma, the stabiliser argument and the
  continuous cones are sole-Astra hand proofs.
  The explainer’s label “proved, with one review” is accurate and should travel with
  every restatement.
- Every assurance rung on the n17 record is `V3/C3` or below, with no human oversight
  record; T-060 shows what rung 4 costs even after the mathematics is done.

### 2.4 Is the cap margin a bottleneck?

$U-S^\ast=4.699\times10^{-4}$, half of it the frame offset $\sigma=2.35\times10^{-4}$.
For exclusion it is not a bottleneck: the admitted certificates’ margins are
$5\times10^{-3}$ to $5\times10^{-2}$, far above the cap slack, and a certificate at $U$
remains valid at every smaller cap by monotone embedding.
For capture the margin forces the two-cap design, which is proved.
The real bottleneck is a different gap, which this review names the **no-man’s-land**:
the region of the family’s state between the largest neighbourhood of the family that
exclusion engines can certify empty (margin-limited, unmeasured) and the smallest
neighbourhood the terminal theorem covers ($1/5000$ now, perhaps $10^{-2}$ with the
widened theorem). Nothing in the record measures the first number.
H-325 and H-330 measure it.

### 2.5 Things in the record that are mistaken, stale or overstated

- The explainer (its text is “as of 2026-10-06”; its frontmatter date is 2 October) and
  X-048’s “Current Selection” still say 58 entries, 36,784 states and 4,685 orbits; the
  merged record says 60, 36,768 and 4,683. The explainer’s own rule, “where this
  document and a record differ, the record is right”, covers it; the numbers should be
  refreshed when the explainer is next touched.
- The strategy review says “The first-eight shared-centre LP remains the next entry” and
  files exp-313 and exp-314 under “Cheap tests of weaker models”.
  [Section 3.1](#31-centre-only-relaxations-exclude-no-distance-2-orbit) shows that the
  LP’s outcome on the first eight is already known: each state has an exact feasible
  primal, so the run would return eight survivors and no Farkas certificate.
  [Section 3.2](#32-no-centre-only-certificate-exists-for-any-cell-triple) shows that no
  weighted-vertex or SOS certificate exists for any cell triple.
  The record’s own exp-313 and exp-314 results already pointed this way (no relevant
  pair has its whole difference domain inside the open unit disk).
- Thirty-three confirmed hypotheses of the n17 program is the ledger’s count (32 at n =
  17 itself; H-281 is an n = 11 control); about half confirm that an instrument runs,
  not that a packing property holds.
  The registry allows this and the experiment records are honest, but the synopsis
  roll-up reads as more progress than there is.
- The stall-classification review’s plan rule classified four wall-crowd stalls as
  “mixed”; the review itself argues they are loss-limited at the floor the flags used.
  The classification is sound; what is stale is that the aimed-split producer policy
  (C2) it selected has not been built, and the record keeps selecting conditional
  propagation instead.
- X-048’s candidate C3 (“the kernel capture’s constant is larger than the probe’s”) was
  replaced by R9’s window; R9’s stage 0 and stage 1 were selected by the consolidation
  on 6 October and have not run.
  The one producer defect R9 found, the compression pull at $2^{-12}$, has an external
  executor but no merged repair.
- The contributor comparison on #413 (19,164 states, 2,449 orbits if all rows were
  admitted) is reproduced exactly by the maintained tool; the tracker correctly calls it
  hypothetical. What the tracker does not say is that even full admission would leave the
  distance-2 tail at 94 of 95 orbits.

## 3. Three Computations

All three are read-only computations over the committed design
`ring-3-voronoi-8-tabbed-unique` in `check_n17_capacity_one_cover.py` and the constants
of the record. They are planning evidence of X-046’s kind, not admitted results, and the
arithmetic of each is stated.
The per-state centres of section 3.1 and the exact replay of section 3.2 come from the
W2 review of this report; the first version of section 3.1 drew its conclusion from a
witness that could not support it, and [Corrections and Limits](#corrections-and-limits)
lists what changed.

### 3.1 Centre-only relaxations exclude no distance-2 orbit

Every unit square contains the open disk of radius $1/2$ about its centre, so a
packing’s centres are pairwise at distance at least one.
The shared-centre LP, the octagon $P_8$ clipping, the disk convexification, the
weighted-vertex screen and the incircle SOS generators keep that fact and one more: each
centre lies in its assigned cell $E_i$. In `packing/devtools/n17_shared_centre_lp.py`,
`build_model` (lines 274–300) adds every facet of each assigned cell as a row
(`centre_domain`, lines 223–235) and builds each pair’s domain from $E_j-E_i$
(`pair_domain`, lines 238–256); PR 464’s face reduction is stated on “the original exact
convex polygonal domain” $E_i$. Each pair’s LP domain is the convex hull of the cells’
difference set clipped outside an octagon whose interior lies in the open unit disk, so
it contains every difference of norm at least one, and any placement of centres in their
cells pairwise at distance at least one satisfies every LP row.
A relaxation of this kind can therefore exclude a state only when its seventeen named
cells cannot host seventeen such centres.

The W2 review showed that the distance-2 states can host them.
For each of the eight frozen first-eight states (masks 849919, 850943, 851839, 851903,
916351, 980927, 981887 and 1630207) it found exact rational centres inside the state’s
own closed cells, pairwise squared distance at least 1 (exact minimum 1.0023 to 1.0051).
The repository’s `build_model` and `check_primal` accept each 34-vector, with 755, 755,
758, 758, 811, 811, 811 and 752 rows; the endpoint’s state, as a control, gives 810
rows, the count exp-316 recorded.
The review’s search found unit-separated centres in their own cells for all 95
distance-2 orbit representatives of the exp-308 descriptor (exact minimum squared
distance at least 1.00396), checking the other 87 against cell membership and distance
only. For this correction the same search was rerun on those 87, and the vectors were
rounded to rational grids and accepted only when `check_primal` and the exact distance
check passed. All 87 were accepted.
The 96 retained vectors sit on grids of 1/1000 (63 of them), 1/10000 (22), 1/100000 (8)
and 1/1000000 (3); their exact minimum squared distances are 1.0020 to 1.0115, and their
LPs have 750 to 864 rows.
By the cover’s $D_4$ symmetry the result extends from each representative to its orbit.

What follows, at its evidential level:

- **The first-eight LP’s outcome is known.** Each of the eight states has an exact
  feasible primal of the relaxation, so the readiness contract’s first outcome holds for
  all eight, and a Farkas certificate cannot exist for any of them.
- **No centre-only method excludes any distance-2 orbit.** The centres satisfy the
  nonconvex incircle constraints, not only the LP rows, so no LP, weighted screen or SOS
  certificate of any order, with or without a ball, over centres in their cells can
  exclude these states.
  Only generators that carry orientation, such as the separating-axis branches, can act.
- **What the vectors are not.** An exact feasible primal of the relaxation, accepted by
  the repository’s checker, is relaxation survival.
  Squares at these centres may overlap; it is not a packing, not an exclusion and not an
  admission.
- **Who produced it.** These are computations of the W2 review and of this correction,
  not a registered W6 experiment.
  [H-328](../hypotheses/H-328-n17-centre-only-relaxations-are-blind.md) records the
  determination and reads as open until a round replays it.

**Replay.** The 96 vectors (the endpoint control, the first eight and the other 87) are
retained with their row counts and exact minimum squared distances in
[`X051-centre-survivors/centre-survivors.json`](X051-centre-survivors/centre-survivors.json).
The coordinates are $(x_0,y_0,\ldots,x_{16},y_{16})$ in the $U$ frame, one centre per
occupied cell in increasing cell index, and the cells are those of the exp-247 receipt.
From `packing/`, with the project interpreter:

```bash
.venv/bin/python3 -c '
import itertools, json, time
from fractions import Fraction as Q
from devtools import n17_shared_centre_lp as lp
E = json.load(open("campaign/explorations/X051-centre-survivors/centre-survivors.json"))
R = json.load(open("../" + E["cells"]))
P = [[(Q(x), Q(y)) for x, y in c["vertices"]] for c in R["cells"]]
B = lambda: lp.Budget(time.monotonic() + 120, lp.OPERATION_LIMIT)
for s in E["states"]:
    m = lp.build_model(P, tuple(i for i in range(24) if s["mask"] >> i & 1), B())
    x = lp.check_primal(m, s["point"], B())
    d = min((x[2 * a] - x[2 * b]) ** 2 + (x[2 * a + 1] - x[2 * b + 1]) ** 2
            for a, b in itertools.combinations(range(17), 2))
    assert len(m.rows) == s["rows"] and d == Q(s["min_d2"]) and d >= 1, s["mask"]
print(len(E["states"]), "accepted")
'
```

`check_primal` raises on the first violated row; the assertion checks the row count and
the exact minimum squared distance.
Run on 9 October 2026 on this branch, it printed `96 accepted` in 38 seconds on one
core.

**The box alone, a secondary remark.** Without the cell assignment the centre box says
nothing: with $p=8661/10000>\sqrt3/2$, the twenty points
$x=\tfrac12+c+\tfrac12[r\text{ odd}]$, $y=\tfrac12+rp$ for $r=0,\ldots,4$ and
$c=0,\ldots,3$ lie in $[1/2,U-1/2]^2$ ($\max y=9911/2500<522/125$) with minimum squared
distance exactly $1$ (exact rational check, 190 pairs).
So a relaxation that kept only the box and the centre distances could prove no bound on
$s(17)$ near $U$. At n = 11 the same construction places twelve points in a box of side
$2.877$. This says nothing about any per-state LP, which keeps the cells.

### 3.2 No centre-only certificate exists for any cell triple

PR 464’s derivation reduces every no-ball order-2 Putinar certificate for a cell triple
with the three incircle generators to a strict weighted-vertex inequality
$\sum_k\alpha_k(q_k(v)-1)\le-\varepsilon$ at every product vertex $v$, and shows that a
product vertex with $q_k(v)\ge1$ for all three pairs is a mixture obstruction that rules
out every such certificate.
On the 24-cell cover (cells already inside the centre box, so $E_i=C_i$), every one of
the 2,024 triples has a product vertex with all three pairwise squared distances at
least $562823713/423200000\approx1.329924$; the smallest triple sum $M_{ijk}$ is
$1581577/250000\approx6.326$ against the threshold $3$, and the smallest pair maximum
squared distance is $4077323093/2116000000\approx1.9269$. This report first computed
these in floats; the W2 review replayed them in exact rationals, and the minimum
reproduces from `packing/` with

```bash
.venv/bin/python3 -c '
import itertools as it, json
from fractions import Fraction as Q
R = json.load(open("campaign/series/series-000-smoke-and-calibration/results/exp-247-n17-unique-state-cover/run-001/receipt.json"))
C = [[(Q(x), Q(y)) for x, y in c["vertices"]] for c in R["cells"]]
d = lambda a, b: (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
print(min(max(min(d(a, b), d(a, c), d(b, c)) for a in C[i] for b in C[j] for c in C[k])
          for i, j, k in it.combinations(range(24), 3)))
'
```

which prints `562823713/423200000` in under two seconds.

The vertex is more than a mixture obstruction: it is a feasible point of the triple’s
encoded system. It lies in the product domain $P$, every incircle generator $g_k=q_k-1$
is nonnegative there, and PR 464 requires a ball generator $B$ to be valid on all of
$P$, so $B(v)\ge0$ as well.
Evaluating any identity
$-1=\sigma_0+\sum_f\sigma_f\ell_f+\sum_k\sigma_kg_k\,(+\,\sigma_BB)$ at $v$ gives
$-1\ge0$. So no certificate exists for any triple at any order, with or without the
ball: the equal-weight screen, the weighted screen, the no-ball order-2 SOS, the
ball-augmented order-2 recipe and reduced order 3 on original cells are refuted, not
unpriced. Only generators that carry information beyond centre distances, such as
orientation or separating axes, can act.

### 3.3 Whole-state closure economics

From H-275’s receipts the counted closures cost 547 to 4,522 CPU-seconds of production
and 257 to 1,899 seconds of verification; call it one CPU-hour per orbit.
The residue is 4,682 non-endpoint orbits: about 4,700 CPU-hours if every state closed,
or roughly 19.5 days on ten cores, before stalls; at the measured medians (1,112.5 s of
production and 482.5 s of verification, about 0.44 hours) it is about 2,100 CPU-hours,
or nine days.
Sessions 182 and 183 closed about three dozen whole states in two overnight
sessions on two workers.
At that rate the tail is months of two workers; and a whole-state certificate removes at
most eight states, where the arity-7 entry W7 alone removed 133,152. The arithmetic says
the residue must fall by sub-pattern certificates of arity 8 to 12, by a grammar change,
or by contributor admissions; per-state closure is for the last few hundred orbits.

## 4. Directions, Ranked

Each route names its mechanism, what it proves, the information it buys per unit of
effort, its early-kill test, prerequisites, risks and a cost order.
Costs are agent-hours and CPU-hours for the first decision, not forecasts of completion.

| Route | Mechanism | Proves if it works | Information per effort | Early kill | Prerequisites | Risks | Cost order |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A. Endpoint-state cap scan (H-325) | run the whole-state kernel and the branch and bound on the family’s own state in the centred container at caps $V<S^\ast$ ($S^\ast-V=2,5,10,15\times10^{-3}$) | the largest cap $V_{\max}$ at which exclusion alone reaches the endpoint’s state; the width of the no-man’s-land | highest: one number no one has, from existing tools, in days | a stall at $S^\ast-V=1.5\times10^{-2}$ under the 2,304-row recipe and $10^6$ BB nodes | the centred-cap producer (exp-280 path) accepting a cap below the root | the kernel’s loss floor ($10^{-3}$ at $1/512$) may sit above the margin at every useful cap | 4 to 8 CPU-hours, 4 agent-hours |
| B. Cap-ladder lower bound (H-326) | exclude all 4,683 residue orbits at a centred cap $V_1<S^\ast$; the 60 admissions carry down by monotonicity; register $s(17)>V_1$ | a new verified lower bound, a step of $10^{-3}$ order against R071’s $2.75\times10^{-6}$ | high for the “soonest progress” criterion; its certificates do not enter the optimality proof, which needs caps $\ge S^\ast$ | the 95 distance-2 orbits do not close at $V_1$ in a 30-orbit stratified pilot | A; a census consumer that reads per-entry caps | cost of the tail; stalls need a grammar change | 100 to 4,000 CPU-hours; two to six weeks |
| C. Feature-forced LP terminal certificate (H-329, H-339, H-340) | on the region where the 135 unavailable options stay negative, the side at fixed angles is an LP in the centres; certify $S_B(\psi)\ge S^\ast$ over an angle box by exact dual sheets on direction patches, then widen by a feature-flip atlas | a restricted-optimality theorem with radius about $10^{-2}$ in angles, fifty times the present terminal target | high for a foolproof proof: the certificate is a list of exact rational duals, small and checkable in any language | a sampled dual sheet with negative slope inside the box; a Chao1 patch estimate above $10^5$ | the exact kernel and duals of exp-244; the feature margins along the family (H-278) | dual degeneracy at the apex (the optimal face has dimension about 17); the $u^\ast$ enclosure | one W7 slice plus review for the patch counter; CPU-day for the exact build |
| D. No-man’s-land map (H-330) | along the 90 signed non-slider directions, the exact fixed-feature LP gives the side growth; compare with the kernel-closable margin from A | where exclusion reach and terminal radius meet, direction by direction | high and cheap; replaces the two competing capture readings by a measurement | none needed; it is a measurement | A’s margin; the LP of the scope review | the LP probe was never retained and must be rebuilt | 4 to 8 agent-hours |
| E. B2-branching branch and bound on the hard tail (H-331) | the contributor’s learned-weight angle-split rule, which shrank two arity-7 trees 11 and 14 times, on the smallest-margin sub-patterns of the 95 distance-2 orbits | whether branch and bound reaches the tail at all | medium-high; the only engine that closed interior crowds | more than $10^6$ nodes on each of ten targets | the 200-line B2 module (unmerged); a certificate size ceiling | tree sizes near the family; verification cost per node (37 ms, PR 452 helps memory not time) | 20 to 60 CPU-hours |
| F. Hard-tail decomposability survey (H-327) | minimal infeasible sub-pattern arity of each of the 95 distance-2 orbits by the retained float survey | whether the tail decomposes into sub-patterns or is jointly infeasible | medium; cheap; routes E versus whole-state | none | existing survey tool | float search is a lower bound on arity | 5 CPU-hours |
| G. State-conditioned charge (H-338) | a counting certificate of R068’s kind whose sites and parent envelopes are specialised to one residue state’s cells, evaluated at a cap $V$ | exclusion of consistency-limited states where pairwise induction has no facts | medium; the only non-pairwise engine candidate | the family’s own state at $V=S^\ast-10^{-2}$ not excluded by the state-conditioned LP | the fractional tooling with state-restricted envelopes | charges collapse at the cap (exp-243); the specialised charge may too | 20 agent-hours to a verdict |
| H. Contributor admission throughput (H-332) | same-object FULL replay of #358 C1/C2 and #413 rows 1 and 2 with the PR 452 verifier; original-domain and $D_4$ joins; admission | removal of 21 orbits (the #358 union) and whatever rows 1 and 2 add | medium; engineering, but the census moves | FULL replay exceeding 8 GB or 4 hours | custody of the packages; `think-t41a` guard | repackaged manifests; fast-verifier-only rows | 20 CPU-hours, 10 agent-hours |
| I. n11 positive control for the repaired capture producer (H-337) | R9 stage 0 with the pull at $2^{-18}$ | whether the kernel route is dead or merely untested | high for closing a question that has consumed three sessions | contraction below $0.5$ by round 15 keeps the route; above $0.9$ kills the producer | the pull repair merged | none mathematical | 2 to 4 CPU-hours |
| J. Composition checker (H-334) and custody (H-335, H-336) | a consumer that reads cover, ledger with per-entry caps, capture receipt and local receipt and derives the theorem or refuses; Rust and Python parity on all 60 entries; hosted objects and a fresh-clone replay | nothing new, but the proof becomes a proof | required for any foolproof outcome | mutation suite not refused | an owner decision on hosting | none mathematical | 20 to 40 agent-hours |
| K. Lean for the hand lemmas (H-333) | formalise the depth-width wall lemma, the centred-container lemma and the separation lemma first | the thin hand layer of the trusted base becomes mechanised | high per lemma; the lemmas are short | a lemma that resists formalisation in a day | Mathlib; the n11 formalisation’s conventions | the local theorem’s lemmas 1 to 6 depend on exact receipts and are longer | 10 to 30 agent-hours for the first three |
| L. Pairwise-kernel capture pilots from box seeds | more rows, more rounds | nothing unless reading A holds | low: four runs agree with reading B | already met its falsifier | — | — | 20 to 45 CPU-hours per stage |
| M. Shared-centre LP and incircle SOS | relaxations that keep each centre’s cell and the pairwise centre distances | nothing on the distance-2 tail: every distance-2 orbit has exact unit-separated centres in its cells, and no triple certificate of any order exists (section 3) | none: the outcome is determined | already met: eight exact first-eight survivors (W2 review) | implemented adapter; the retained vectors | none | minutes, for a round that registers the known outcome |
| N. Conditional propagation inside one guard | owned hulls, partner coupling, collective rows | restrictions conditional on a guard no global step delivers | low after fifteen misses | already reached fixed points | — | consumes sessions | — |
| O. New global charge or structural inequality | wall budget, contact rank, four-corner capacity | a necessary condition; none has excluded a state | low until one bites | all 95 survived three filters | — | — | — |

### 4.1 The top three, and why

**First: measure exclusion reach on the endpoint’s own state (A, then D).** This is the
one experiment that informs every other route.
If the family’s state closes at $S^\ast-V=5\times10^{-3}$, the cap ladder (B) is viable
and worth a verified bound about $5\times10^{-3}$ above R071 within weeks; the
no-man’s-land is then the difference between that margin and the terminal radius, and D
says along which directions it is widest.
If the family’s state does not close even at $1.5\times10^{-2}$, that would suggest the
per-state engines need a side margin larger than that to act.
It would not show that the hard tail cannot close at $U'$: a distance-2 state’s margin
at $U'$ is its own minimal side minus $U'$, which nobody has measured and which may
exceed $1.5\times10^{-2}$. The program would then weigh moving its exclusion effort to
grammar changes and contributor admissions, with a control on the tail states themselves
deciding, such as H-326’s stratified pilot, which runs distance-2 states at a cap below
$S^\ast$. Either way the answer costs days and uses only existing tools.

**Second: rebase capture on exact LP certificates over the feature-forced region (C,
with I as the kill test for the kernel route).** The widened projection theorem is the
only proposal in the record that makes the terminal target larger than any engine must
reach, and its certificate is the kind a foolproof proof wants: finitely many exact
rational dual vectors over named patches, checkable by a program that knows only linear
algebra. Its risks (dual degeneracy, patch count) are measurable by the patch counter
specified in R9 section 7, which has never been built.
The n11 control (I) should run once, with the pull repaired, so that the kernel route is
either reinstated by a number or closed by one.

**Third: throughput on the hard tail (E, F, H, with G as the alternative engine).** The
residue falls by sub-pattern certificates, not by whole states.
The contributor’s branching rule is the only measured lever on branch-and-bound tree
size, and the tail’s decomposability is unknown; both are cheap to test.
The state-conditioned charge is the one engine candidate that is not pairwise, which is
what the consistency-limited stalls ask for.

**What to stop.** Stop running conditional propagation rounds inside the owner-0 guard
(N): fifteen recipes missed in two days, and the accepted restrictions have no consumer
until a global step delivers the guard.
Stop presenting the shared-centre LP as the mathematical entry (M): its first-eight
outcome is known, and a round on it can only register that outcome by replaying the
retained vectors (H-328). Do not fund any incircle SOS pilot on original cells, at any
order and with or without the ball: no certificate exists.
Stop box-seeded kernel capture pilots (L) until I says otherwise.
Stop writing a new reconciliation document for each merge gate; the explainer and the
tracker are the two living documents, and OR-3 says CI runs beside the research, never
ahead of it.

## 5. What a Foolproof Package Looks Like

The proof will be a finite statement checked by programs plus a thin layer of hand
lemmas. For a reader to trust it with the least possible faith, each of the following
should hold. The right column says where the record stands.

| Element | Requirement | Status |
| --- | --- | --- |
| One statement | “Every packing of 17 unit squares in a square of side $S\le S^\ast$ lies on the Bidwell family and has $S=S^\ast$”, with $S^\ast$ the root of the stated polynomial in its isolating interval | the statement is in the explainer; nothing checks it |
| A trusted base listed in one place | the cover design and its capacity lemma; the $D_4$ action; the centred-container lemma; the certificate semantics of each format; the local theorem’s hand lemmas; the composition rule | scattered across reviews; the proof-interfaces document is the nearest thing |
| Exact arithmetic throughout | rationals or outward intervals; no float on the critical path | met in every admitted certificate and checker |
| Certificates as data | each exclusion a self-describing object naming its cells, cap, frame and the checker version that passed it | met for kernel and BB formats; caps are implicit ($U$) and must become explicit before a cap ladder or a $U'$ stage exists |
| Two independent checkers per format | a second implementation sharing no code, with same-object parity on every admitted object and a mutation suite | partial: the Rust kernel verifier has parity on seven objects; the BB format has the contributor’s Rust checker, unreviewed; `think-t41a` open |
| A composition checker | reads the cover receipt, the ledger, the capture receipt and the local receipt; refuses any uncovered orbit, any cap mismatch, any missing join | absent (H-334) |
| Replay from a fresh clone | every object hosted with digests; one command replays one certificate of each kind within hours; the full collection replays in a documented CPU budget | absent: 204 objects unhosted (H-336) |
| Hand lemmas mechanised or doubly reviewed | the short lemmas in Lean; the longer ones with two adversarial reviews and an oversight record | none mechanised; one review each (H-333) |
| Rung 4 records | two adversarial AI reviews by distinct reviewers and a human oversight record per load-bearing piece | none |
| Portability | checkers in a pinned toolchain with no network; certificate formats documented outside the code | kernel and BB formats are documented in reviews; the standing checkers need the repository |

The n11 packet (T-060) shows the pattern: a completion inventory and a final composer
that bind reviewed receipts and refuse a missing premise, an exclusion inventory naming
every accepted execution, and a validation guide.
None of it reruns geometry, and its child receipts pin byte-exact parents, which is why
a fresh end-to-end replay there needs a rebinding workflow.
The n17 package should avoid that: receipts should pin mathematical state identities,
not timing fields.

## 6. Process Observations

- **Effort went to the parts that cannot finish the proof.** About 75 agent-hours on 7
  to 8 October produced two orbits of census movement and fifteen misses of conditional
  recipes. The two parts of the proof with no working engine, capture from the cells and
  the hard tail, received diagnostics and contracts but no discriminating run.
  The W3 consolidation of 6 October selected R9’s stage 0 and stage 1; neither ran.
- **Readiness controls are registered as hypotheses.** They pass, they are counted as
  confirmations, and the synopsis roll-up shows 33 confirmed claims of the n17 program
  (32 at n = 17 itself).
  A separate kind, or a `role: readiness` field on the experiment, would keep the count
  honest without changing the workflow.
- **Conditional rounds have no stop rule tied to a consumer.** The regional and
  propagation work was allowed to continue after each miss because each miss was
  “completed and fresh”.
  A rule of the form “no third round on a guard without a named global step that
  delivers the guard” would have stopped it after exp-296.
- **Qualification work gated mathematics.** Merge readiness, snapshot caps, suite-cost
  registers and CI reruns occupy most of the tracker’s last six comments.
  OR-3 and OR-14 say what to do: run the gates beside the research and never let a 192
  MiB cap decide what mathematics is attempted.
- **Documents multiplied.** Sixteen research documents and eleven reviews in two days,
  several restating each other’s counts; the explainer, which is the reader-facing
  account, is three days stale.
  One living explainer regenerated from the census tool, plus the tracker, is enough.
- **A metric for efficiency blocks (OR-12).** Count mathematical movement per
  agent-hour: orbits excluded, verified-bound movement, terminal radius, and
  exclusion-reach margin.
  Last week’s figure is two orbits per 75 agent-hours.
  Sessions 182 and 183 moved 11,000 orbits in two overnight sessions of two workers.
  The difference is not the people; it is that the earlier sessions ran the engine that
  moves the obligation.

## 7. Candidate Hypotheses

Each is a registry file under `hypotheses/` with `derived_from: [X-051]`; the summaries
below give mechanism, falsifier, expected information and limits.
H-325, H-327, H-332, H-335, H-336 and H-340 are runnable with existing tools and read as
open in the ledger. H-328 also reads as open, but its outcome is already known from the
W2 review; it waits only for a round that registers it by replaying the retained
vectors. H-337 waits on the unmerged pull repair; the rest name an instrument that does
not exist and read as blocked until it does.

| Id | Claim | Mechanism | Falsifier | Expected information | Limits |
| --- | --- | --- | --- | --- | --- |
| [H-325](../hypotheses/H-325-n17-endpoint-state-cap-scan.md) | The family’s own state is excluded by the whole-state kernel or the branch and bound in the centred container at cap $S^\ast-10^{-2}$ | below $S^\ast$ the family’s state is infeasible by a side margin the engines can see | a stall at $S^\ast-1.5\times10^{-2}$ under the 2,304-row recipe and $10^6$ nodes | the exclusion-reach margin, the first number of the no-man’s-land | reach on one state; other states may differ |
| [H-326](../hypotheses/H-326-n17-cap-ladder-lower-bound.md) | $s(17)>V_1$ for $V_1=S^\ast-10^{-2}$ by exclusion of every residue orbit at the centred cap, the 60 admissions carried down | monotone embedding; the per-state engine at a cap with margin | a stratified 30-orbit pilot with fewer than 27 closures | a verified bound about $5\times10^{-3}$ above R071 | its certificates do not enter the optimality proof |
| [H-327](../hypotheses/H-327-n17-hard-tail-decomposability.md) | At least 60 of the 95 distance-2 orbits contain an infeasible sub-pattern of arity at most 10 | the float survey’s minimal sub-pattern search | fewer than 60 | whether the tail is decomposable or jointly infeasible | float lower bound on arity |
| [H-328](../hypotheses/H-328-n17-centre-only-relaxations-are-blind.md) | A determination pending registration: every distance-2 orbit representative, the first eight included, has exact centres in its own cells pairwise at distance at least one, which the shared-centre LP checker accepts; no cell triple admits a weighted-vertex or SOS certificate of any order | the W2 review’s exact search and replay; each triple’s best product vertex is a feasible point of its encoded system | moot as a prediction, since no Farkas certificate can exist where an exact primal does; a replay that rejects a retained vector exposes a defect in the vectors or the checker | none beyond registration; the outcome is known | relaxation survival, not a packing; says nothing about orientation-aware generators |
| [H-329](../hypotheses/H-329-n17-feature-forced-lp-terminal-certificate.md) | A patch certificate of exact dual sheets proves $S\ge S^\ast$ with equality only on the family over the feature-forced angle box of radius $5\times10^{-3}$ | at forced features the side at fixed angles is an LP; sheets are nearly linear | a negative sampled slope; Chao1 patch estimate above $10^5$ | a terminal theorem fifty times larger than $1/5000$ | the $u^\ast$ enclosure; square 6 coarse; outer capture still owed |
| [H-330](../hypotheses/H-330-n17-no-mans-land-map.md) | Along at most two of the 90 signed directions does the kernel-closable margin fail to reach the terminal radius | exact fixed-feature LP side growth against H-325’s margin | more than two directions | which directions capture must bridge | the LP probe must be rebuilt |
| [H-331](../hypotheses/H-331-n17-b2-branching-on-the-hard-tail.md) | With the B2 rule, branch and bound closes at least three of the ten smallest-margin sub-patterns of the distance-2 orbits within $10^6$ nodes each | learned Farkas weights aim angle splits at the squares the duals use | fewer than three | whether branch and bound reaches the tail | the rule is unmerged; verification cost per node |
| [H-332](../hypotheses/H-332-n17-contributor-admission-throughput.md) | #358 C1/C2 and #413 rows 1 and 2 replay FULL with the PR 452 verifier within 4 hours and 8 GB each and join to the ordinary ledger | the lifetime repair bounds retained nodes | a FULL replay exceeding the ceilings or a failed join | 21 or more orbits removed and a measured admission cost | custody of repackaged objects |
| [H-333](../hypotheses/H-333-n17-lean-hand-lemmas.md) | open question: which of the hand lemmas (wall lemma, centred container, separation, recipe lemmas 1–6) formalise in Lean within a day each | the lemmas are short real-analysis statements | — | the size of the hand layer of the trusted base | needs Mathlib fluency |
| [H-334](../hypotheses/H-334-n17-composition-checker.md) | A composition checker reproduces the 4,683-orbit residue from the cover and ledger, refuses a ledger with one entry removed or one cap changed, and refuses a missing capture or local receipt | the n11 composer pattern with per-entry caps | any mutant accepted | the proof becomes a checkable object | nothing mathematical |
| [H-335](../hypotheses/H-335-n17-two-verifier-parity.md) | The Rust and Python kernel verifiers agree on all 60 admitted entries, and 30 corrupted objects are refused by both | PR 410’s receipt parity extended to the whole ledger | one disagreement or one accepted mutant | an independent second checker for every admission | the BB format needs its own second checker |
| [H-336](../hypotheses/H-336-n17-fresh-clone-replay.md) | All hosted objects publish, and a fresh clone replays one kernel and one BB certificate end to end within 4 hours | release assets with digests | a failed fetch or replay | replay portability | an owner decision on hosting |
| [H-337](../hypotheses/H-337-n11-capture-positive-control.md) | With the pull repaired, the n17 producer on n11’s state from its cells contracts the worst two-sided extent below $0.5$ by round 15 | the n11 proof’s own capture, replayed through the n17 producer | above $0.9$ | whether the kernel route is dead or untested | says nothing about n17 directly |
| [H-338](../hypotheses/H-338-n17-state-conditioned-charge.md) | open question: does a charge specialised to one residue state’s cells exclude the family’s own state at $S^\ast-10^{-2}$ | counting is not pairwise | — | an engine for consistency-limited states | charges collapse at the cap |
| [H-339](../hypotheses/H-339-n17-feature-flip-atlas.md) | At most eight unavailable options have centroid margin below $0.1$, and the LP over each flipped feature set has side above $U'$ throughout the box of radius $2\times10^{-2}$ | enumerate near-margin features; LP per branch | more than eight, or a flipped set with side below $U'$ | a terminal region of radius $2\times10^{-2}$ | numeric first; exact duals after |
| [H-340](../hypotheses/H-340-n17-per-coordinate-radius-composition.md) | The composed local theorem passes exactly with every coordinate at least $1/1216$ on $B_c$ from a clean worktree | the local-radius review’s vector, re-run as a registered round | a failed check | a terminal target four to five times larger, load-bearing for H-329 and H-330 | the vector was found against the same instrument |

## Evidence Status

| Kind | Items |
| --- | --- |
| Computed here, exact rationals | the twenty-centre box witness in section 3.1 (190 pairwise squared distances, minimum exactly 1; all points inside $[1/2,522/125]^2$) |
| Computed by the W2 review, exact rationals, accepted by the repository’s checker | section 3.1: centres in their own cells, pairwise squared distance at least 1, for the eight first-eight states (`build_model` and `check_primal`, 752 to 811 rows) and the endpoint control (810 rows); unit-separated centres in their own cells for all 95 distance-2 representatives (minimum squared distance at least 1.00396). Relaxation survival only |
| Computed in this correction, exact rationals, accepted by the repository’s checker | section 3.1: vectors for the 87 distance-2 representatives beyond the first eight, regenerated with the W2 search; the replay of all 96 retained vectors |
| Computed here in floats, replayed exactly by the W2 review | section 3.2: for all 2,024 cell triples of `ring-3-voronoi-8-tabbed-unique`, a product vertex with all three squared distances at least $562823713/423200000$; smallest $M_{ijk}=1581577/250000$; smallest pair maximum squared distance $4077323093/2116000000$; no pair with maximum below 1 (agreeing with exp-314) |
| Derived here, checked by the W2 review | section 3.2: the feasible vertex rules out every weighted-vertex and SOS certificate for every triple, at any order, with or without the ball |
| Computed here from the records | experiment and hypothesis counts; the ledger’s arity composition; residue by distance from exp-259; agent-hours from the three session receipts; closure economics from H-275’s receipts |
| Read from records | every count, cost and verdict cited to an experiment, review, hypothesis or issue |
| Derived here, needing review | the no-man’s-land framing; the default to R9’s box-set reading; the cap-ladder route and its caveat; the ranking; the foolproof table |
| Not done | any registered experiment; any verification of a certificate; any change to a verdict, bound or census count |

## Corrections and Limits

- The per-state survivors and the triple computation concern relaxations that keep each
  centre’s cell and the pairwise centre distances.
  They say nothing against relaxations whose generators see orientation, such as the
  full separating-axis branches, and a survivor of such a relaxation is not a packing.
- The cap-ladder route produces lower bounds, not the optimality proof: its certificates
  are at caps below $S^\ast$ and cannot replace the exclusions at $U'$ the final
  argument needs. Its value is a verified bound and a measurement.
- Reading B of pilot 2 is adopted here as the default because every measured number
  favours it; R9 leaves it formally open, and H-337 and R9’s stage 1 are the tests.
- Agent-hour figures are lower bounds from partial receipts, and the experiment
  classification into readiness and mathematics is this review’s reading of each record.
- No bead, issue or frontier field is changed; the coordinator publishes.
- **W2 review, 9 October.** The
  [W2 factual review](https://github.com/jlevy/squares/pull/473#pullrequestreview-5469083247)
  checked 38 claims against the committed artifacts and found one blocking error.
  This revision applies it and the non-blocking findings:
  - Section 3.1 and the summary said the centre-only relaxations keep only the centre
    box and the pairwise distances.
    They also keep each centre’s assigned cell, so the twenty-point box witness could
    not decide any per-state LP. The section now rests on the review’s exact per-state
    survivors and 87 vectors regenerated with its search, retained in
    [`X051-centre-survivors/centre-survivors.json`](X051-centre-survivors/centre-survivors.json)
    with a replay that accepts all 96, and the witness remains only as a remark about
    the box. H-328 is re-scoped from a prediction to a determination pending
    registration; its falsifier, under which exactly one Farkas certificate was neither
    outcome, is moot.
  - Section 3.2 called the ball-augmented and higher-order recipes unpriced.
    The feasible product vertex refutes them for every triple; route M, the stop-list
    and H-328 now say so.
  - Counts: exp-240 to exp-316 are 42 accepted, 16 rejected and 11 unresolved, and 17 of
    the 42 are readiness rounds; the 39 whole-state entries cover 304 states; closure at
    one CPU-hour per orbit is about 4,700 CPU-hours (19.5 days on ten cores), or 2,100
    at the measured medians; W7 alone removed 133,152 states, replacing an unsourced “up
    to 23,300”; custody is 204 objects and 2.17 GB, here and in H-336; the 2,234-orbit
    union is the #413 rows’ alone; the n17 hypothesis counts include H-281; the cover’s
    margin is cited as the receipt’s lower bound; “fifteen of the nineteen recipes” is
    now the fifteen missed rounds by number.
  - Section 2.5 quoted two phrases that occur in neither the consolidation nor the
    strategy review; it now quotes the strategy review’s own words.
  - Section 4.1 and H-325 inferred from a stall on the family’s state that the hard tail
    cannot close at $U'$. A distance-2 state’s margin at $U'$ is unmeasured, so both now
    say only what such a stall would suggest.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
