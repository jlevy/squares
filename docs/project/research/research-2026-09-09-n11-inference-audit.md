# Inference Audit: Owner Geometry and Fixed-D Continuation

**Read-only audit, 2026-09-09.** This report separates definitions, retained results,
derived arguments, and unmeasured alternatives.
It inspects the SYNOPSIS and Agenda033 snapshots, retained proof and experiment records,
two strategy drafts subsequently adopted into the repository, and
[PR145](https://github.com/jlevy/squares/pull/145) at head
`2acf4b859d39e01cc9fcb1156d8573f65e08efbd`. No target geometry or source replay was
evaluated. The PR body was read successfully once; a later attempt to retain a local
snapshot failed on network connection, so PR findings identify its section and quoted
sentence rather than a local line number.

## Definitions and the Direction of Inference

1. **Physical packing.** Eleven closed unit squares lie in `K=[0,q]^2`, `q=96/25`, with
   pairwise disjoint interiors and arbitrary physical angles.
   A global exclusion says no such eleven-square configuration exists.
   The current work has not proved this.
   A conditional exclusion assumes additional, explicitly stated owner conditions.

2. **Selected B-core.** Each physical square can be assigned a concentric closed square
   of side `B=9977/10000` at a retained rational direction.
   The nearest-frame mismatch bound `D_net=207107/90000000` and `B*(1+D_net)<1` put that
   core strictly inside its parent.
   Therefore selected cores of distinct parents are disjoint compact sets, and have
   positive clearance from one another and from the container boundary.
   The full finite family has 361 canonical square orientations; signed owner axes
   retain further quarter-turn and reflection provenance.
   This is a proved selection map from arbitrary physical angles, not an empirical angle
   grid.
   [Retained transfer](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-032/proofs/fixed-cover-transfer-review.md)

3. **Owner and owner selection.** BC303’s corner-pair argument supplies four distinct
   selected cores in a hypothetical eleven-square packing, each containing at least one
   of its corner’s two marks.
   A mark may lie on the core boundary.
   Owning both marks does not create two owners, and the theorem does not make the
   parents literal corner squares.
   These four cores account for four physical parents; seven remain.
   [Primary replay](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/bc-303-first-wave-selection.md)

4. **Owner class and tuple.** A local class specifies one mark and one of eight closed
   sectors for the first signed core axis.
   The axes are ordered counterclockwise and chosen so that the mark-to-centre
   displacement has two nonnegative coordinates.
   For ray r, an allowed centre has `centre=mark+a*r+b*Jr`, `0<=a,b<=B/2`. Two marks
   give sixteen labels per corner; a tuple selects four labels in BL, BR, TL, TR order.
   Closed sectors and multiple owned marks make labels overlap.
   `16^4=65536` is a label count, not a count or measure of physical packings.
   The continuous parent angle is not required to lie in its snapped core’s sector.
   [Class proof](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-031/proofs/corner-owner-sector-footprints.md)

5. **Allowed core poses and common footprint.** For class k, the wall constructor
   retains all its signed frames and the closed centre sets permitted by the B-core
   container box and class displacement box.
   These are a necessary model of actual owners.
   The common footprint A_k is the intersection of all modeled owner cores; every actual
   owner assigned to k contains A_k. The converse fails: a residual core avoiding A_k
   need not avoid any whole allowed owner core.
   An allowed B-core pose need not extend to a contained unit parent.
   Four individually allowed poses need not coexist.
   Exp146’s word “container” refers to the B-core container condition.
   [Constructor](../../../packing/devtools/wall_owner_footprints.py)

6. **Strict residual relaxation.** For a fixed tuple t, let F_t consist of every
   retained-direction B-core strictly inside K and strictly disjoint from the four
   selected closed footprints.
   The seven actual residual cores of any packing routed to t belong to F_t. Members of
   F_t need not have actual owners, unit parents, or seven mutually compatible residual
   companions. An exact escaping member is a counterexample to coverage on F_t, not a
   packing witness. Testing compatibility with each entire allowed owner individually
   gives a smaller necessary family; testing their joint coexistence gives another
   restriction.

7. **Dots, weighted cover, and counting.** D denotes the retained five sites, with unit
   weights after dividing exp143’s common positive weight by itself.
   D covers F_t when every C in F_t contains some site of D. More generally, a
   nonnegative measure mu covers F_t if `mu(C)>=1` for every C. A cover with available
   mass below seven contradicts seven disjoint actual residual cores.
   Mass inside the guaranteed occupied union can be removed before counting; four small
   footprints do not automatically provide four units of banked mass.
   Five unit dots permit at most five residual cores; six permit at most six.
   Acceptance needs the complete centre domain at every required direction and the
   physical transfer premise.
   [Counting proof](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-031/proofs/corner-owner-sector-footprints.md)

8. **Zero area and strict witnesses.** A positive exact uncovered area proposes a
   rational strict escape, which must independently replay.
   Exact zero area at all directions covers the strict open domains: a strictly missed
   core would have an open missed neighbourhood.
   Event boundaries retain closed-dot membership, and nonnegative weights support the
   recorded boundary transfer.
   Contact-only artificial centre sets are not silently claimed as physical
   selected-core placements.
   A closure-support attainer is not automatically a strict escape.
   [Boundary transfer](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-032/proofs/five-dot-transfer-review.md)

9. **Sixth-site support feasibility.** Let `F_t(D)` be the members of F_t missing every
   original site. A single added site p works exactly when
   `p in I*=intersection(C for C in F_t(D))`. At one direction with axes u,v, this is
   equivalent to `sup(u dot c)-h <= u dot p <= inf(u dot c)+h`, and similarly for v,
   over its strict D-missed centre domain.
   Extrema over every vertex of every positive-area component closure are exact only
   because the admitted decomposition proves that their union equals the closure of that
   strict domain. An arbitrary closed overapproximation would not justify a negative.
   Empty I* means `for every p, some modeled core misses D and p`. A prefix can
   establish emptiness because subsequent intersections only remove points.
   [Direct-domain contract](../../../packing/cases/n11_five_dot_cover/direct-sixth-site-contract.md)

10. **Fractional core family and pricing.** A fractional family assigns nonnegative
    weights lambda_j to core poses, with pointwise depth `sum(lambda_j*1_(C_j)(x))<=1`
    everywhere. Its total weight lower-bounds the mass of any point cover of those poses.
    A verified family of residual mass at least seven would obstruct every
    mass-below-seven cover of that relaxation; it would not supply seven physical
    parents. A finite-support LP value or a floating dual proposal alone is not that
    certificate. H135 is narrower: solve one transported BC232 unit-square cutting state,
    then find the same absent site orbit with exact `depth_first32<=1<depth_full` under
    two truncations of that one rationalized dual sequence.
    It tests a pointwise pricing truncation mechanism; it neither prices the present
    owner-patch family nor proves a global cover.
    [H135’s exact scope](../../../packing/campaign/hypotheses/H-135-paired-full-support-pricing.md)

The sufficient global routing statement for this architecture is
`for every hypothetical physical packing P, there exists a valid owner selection s
whose tuple belongs to the certified excluded set E`. Proving every raw tuple excluded
would suffice, but is stronger than necessary.
An overlap-aware routing theorem can select one excluded representation per packing.
Other global proof architectures need not use this tuple ledger at all.

## What Exp145–153 Establish

The experiment records and bound receipts are the authority for the following facts.
No result in this table changes the global n11 bound or, by itself, T023’s grade.

| Experiment | Retained observation | Exact inference and limit |
| --- | --- | --- |
| [145](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-145-independent-five-dot-union.md) | All 361 deficits zero in an independent exact union implementation. | Confirms the fixed baseline D/patch certificate. Its self-contained geometry is independent of the preceding project geometry implementation; the supplied rational input and analytic physical premises are shared. This adds assurance, not a new tuple. |
| [146](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-146-wall-owner-footprints.md) | All sixteen classes complete; twelve proper footprint enlargements, four equal, none impossible. The unchanged ones are j0 and j7 for both marks. | Establishes exact geometry gain from B-core wall constraints. Larger area alone implies neither certificate transfer nor a new excluded physical case. |
| [147](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-147-wall-owner-containment.md) | 128 relations: eight contained and 120 not; two baseline tuple products, zero new tuples. | Refutes the declared same-corner component-containment expansion. Direct coverage, other sufficient transfer relations, and physical feasibility remain undecided. |
| [148](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-148-fixed-five-dot-wall-expansion.md) | Partial seed bank, two replayed witnesses, no completed seed and no selected candidate. Their products reject 49,152 labels for D. | Partial negative evidence for fixed-pattern coverage. The separate D-preserving symmetry argument raises the rejection set to 61,440 labels; it does not increase the executed witness count. Neither percentage measures physical packings or progress toward a numerical bound. H146 remains unresolved. |
| [149](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-149-selected-wall-tuple-cover.md) | First direction owner-000 has a positive deficit and a strict replayed escape for tuple (0,0,0,7). | Completely refutes H147’s fixed-D cover on that patch relaxation. The physical tuple and H146’s existence of a new D-covered tuple remain open. |
| [150](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-150-wall-owner-escape-compatibility.md) | Each of the four selected classes has a positive, independently replayed frame-0 B-core witness against the saved exp149 core; four frame evaluations suffice existentially. | Refutes individual-owner exclusion of this one escape in this B-only necessary model. It does not exhaust 724 frames, test another escape, or establish joint owners or contained unit parents. |
| [151](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-151-selected-six-dot-cover.md) | D plus the exp149 centre passes directions 0–5; direction 6 has a strict six-dot escape. | Refutes this specified six-site candidate. No conclusion about other sixth sites or repositioned six-site patterns followed from this experiment alone. |
| [152](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-152-sixth-site-two-core-screen.md) | The two saved escaping cores have a nonempty two-dimensional intersection with four exact vertices and replayed canonical membership. | Accepts a necessary two-witness site screen. The region contains candidates that hit those two cores; it was not an all-domain cover. |
| [153](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-153-direct-sixth-site-feasibility.md) | I* becomes empty after support directions 0–187. No candidate confirmation is needed. | Refutes every single-added-site extension of fixed D for the selected patch relaxation. The result leaves repositioned sites, general weighted covers, tighter owner models, and physical feasibility open. Its closure attainers have not yet been turned into a separately replayed strict pair or triple. |

The last inference is stronger than exp151’s failed candidate and narrower than an
arbitrary six-site or weighted-cover impossibility.
A subsequently replayed disjoint pair of D-missed cores would force added nonnegative
mass at least two; with all five original unit atoms retained, total mass would then be
at least seven. That extra statement has not yet been established by the proposed pair
target. This is a nominal total-mass statement.
To identify it with the available-mass threshold after occupied-union banking, retain an
exact premise that all five original sites lie outside the selected occupied union.
Otherwise any banked original-atom mass must be accounted for separately.
No new site/patch relation is evaluated by this audit.
Empty intersection of three pairwise-intersecting cores alone permits their three
witness demands to be met by three pair-intersection sites of weight one half each.
That construction covers only those three demands, not the full residual family.

## Statements to Narrow or Backfill

The table records the corrections proposed at the audit snapshot.
Location numbers refer to that snapshot; subsequent backfills can move the text.
The strategy-draft links now resolve to their adopted repository documents.
Dated prospective records retain their original criteria and receive a disposition;
current handoffs state the latest outcome.

| Location | Issue | Replacement prose |
| --- | --- | --- |
| [SYNOPSIS:697](../../../SYNOPSIS.md) and [785](../../../SYNOPSIS.md) | Calls exp147 unrun despite its completed retained result. | “Exp147 completed all 128 declared component-containment relations. It recovered only the two baseline tuples and added none.” |
| [SYNOPSIS:811](../../../SYNOPSIS.md) and [840](../../../SYNOPSIS.md) | Labels exp153 and the exp150/151 decision tree as next work after their completion. | “Exp150–153 completed the saved-escape and fixed-D-plus-one-site sequence. Exp153’s empty support intersection rules out one added site for the selected patch relaxation. The next activity is an evidence and inference review; successor geometry remains unrun.” |
| [SYNOPSIS:850](../../../SYNOPSIS.md) | Says global exclusion requires every admissible owner combination to be covered. This overstates the necessary routing quantifier and makes this architecture sound mandatory. | “For this owner-based route, every hypothetical packing must admit at least one valid owner selection whose tuple is excluded. Exhausting every raw label is sufficient, but a proved routing reduction may require fewer labels.” |
| [Agenda033:136](../../../packing/campaign/agendas/agenda-033-overnight-owner-geometry.md) and [155](../../../packing/campaign/agendas/agenda-033-overnight-owner-geometry.md) | “Exp149 refutes selected tuple” can be read as physical tuple exclusion. | “Exp149 refutes coverage by fixed D on the selected tuple’s four-patch relaxation, using a strict owner-000 escape. It does not refute physical feasibility of the tuple.” |
| [Agenda033:213](../../../packing/campaign/agendas/agenda-033-overnight-owner-geometry.md), [330](../../../packing/campaign/agendas/agenda-033-overnight-owner-geometry.md), and [SYNOPSIS:818](../../../SYNOPSIS.md) | “Refuted individual-owner exclusion” needs its witness and model quantified. | “Exp150 refutes individual-owner exclusion of the saved exp149 core in the unchanged B-core centre model: each selected class has one independently replayed compatible core.” |
| [Agenda033:315](../../../packing/campaign/agendas/agenda-033-overnight-owner-geometry.md) | “The main gap” presents one route’s open obligation as a demonstrated global bottleneck. | “The current certificate excludes one specified owner condition. Extending this route to a global bound requires an exhaustive physical routing argument together with certificates or geometric exclusions for the routed cases. Its comparative cost against other proof routes is unmeasured.” |
| [Agenda033:338](../../../packing/campaign/agendas/agenda-033-overnight-owner-geometry.md) | “Actual cores” may suggest physical parent realizability; “an empty triple proves only” overlooks a triple containing a disjoint pair. | “A strictly replayed disjoint pair in the residual-core relaxation would force added mass at least two with D’s five unit atoms retained. An empty triple alone establishes the one-site obstruction; its pair intersections determine whether this stronger mass argument also applies.” |
| [After exp149:25](../../../packing/cases/n11_five_dot_cover/after-exp149-strategy.md) | “Information lost by that changed owner condition” treats changing the TR class as evidence that the class-7 common footprint discarded a physically valid constraint. The baseline implication locates the changed patch, not a physical artefact. | “The baseline cover implies that this escaping core intersects the old TR patch while avoiding the selected class-7 patch. The coverage difference is localized to that replacement. Whether stronger valid class-7 owner constraints remove the core is a separate question.” |
| [After exp149:116](../../../packing/cases/n11_five_dot_cover/after-exp149-strategy.md) | “Individual-owner tightening cannot remove this witness” is broader than the tested unchanged B-core model. | “The tested individual-owner B-core compatibility condition does not remove this witness. Stronger necessary parent constraints and joint-owner compatibility remain untested.” |
| [After-direct draft:15](../../../packing/cases/n11_five_dot_cover/after-direct-family-decision.md), [28](../../../packing/cases/n11_five_dot_cover/after-direct-family-decision.md), [114](../../../packing/cases/n11_five_dot_cover/after-direct-family-decision.md), and [150](../../../packing/cases/n11_five_dot_cover/after-direct-family-decision.md) | “Prefer,” “economical,” “smallest,” and “cheapest” are prospective judgments without comparative measurements. | “The proposed fixed-pair construction would distinguish a single-site obstruction from an added-mass-at-least-two obstruction. Its exact gap and runtime are unmeasured. A triple extractor, necessary parent restrictions, and new weighted or repositioned-site covers answer different questions; no comparative productivity result has been obtained.” |
| [After-direct draft:154](../../../packing/cases/n11_five_dot_cover/after-direct-family-decision.md) | Calling retained cores “witness artefacts” assumes the outcome of a future parent-compatibility test. | “The parent restriction tests whether a retained relaxed witness can be removed by an additional necessary physical condition. Its exclusion and physical realizability are both unmeasured.” |
| [Parent-centre draft:3](../../../packing/cases/n11_five_dot_cover/unit-parent-centre-contract.md) and [46](../../../packing/cases/n11_five_dot_cover/unit-parent-centre-contract.md) | “Mathematical design admission” can be mistaken for completed independent assurance. The proof should explicitly select the principal mismatch interval before replacing cosine by a positive reciprocal square root. | “This note derives a necessary unit-parent centre bound for independent audit. No footprint gain or witness removal has been measured. Choose the nearest-frame representative with abs(delta)<pi/4 and 0<=tan(abs(delta))<=d<1; the signed-L1 calculation then yields L=(S-T*d)/(2+d²).” |
| PR145, “Exact compatibility discriminator,” sentence “For every one of the 181 retained frames … it computes” | Describes the universal path without the early existential stopping rule; the actual run evaluated four frames total. | “The checker traverses up to 181 frames per class, stopping once a strictly separated witness independently replays. A universal non-separation verdict requires the complete frame list. Exp150 found one frame-0 witness in each class.” |

PR145’s final paragraph beginning “This proves that no single sixth site completes”
already states the selected four-patch relaxation and explicitly leaves physical,
repositioned-site, weighted, T023, and global claims open.
Preserve that qualification.
The dated direct-sixth-site design’s original “unrun” statement is legitimate
prospective history; a short status pointer to exp153 would make that temporal scope
clear without rewriting its original decision.

## Alternatives and the Evidence That Would Distinguish Them

This is a map of unresolved mathematical questions, not a ranking.

| Alternative | Present premise | Discriminating evidence still needed |
| --- | --- | --- |
| Compact strict obstruction | Exp153 has an empty intersection of exact support constraints, with source-bound closure attainers. | A fixed inward perturbation and independent strict replay preserving a disjoint pair would prove the fixed-five-unit-atoms mass barrier. Nonpositive gap refutes only the frozen x-axis construction. No target gap has been calculated. |
| General weighted continuation with D retained | Single-site impossibility does not settle added mass below two. | A complete nonnegative added measure hitting every D-missed core with mass below two, or a feasible fractional D-missed core family of mass at least two and depth at most one everywhere. A pair would supply the latter special case. |
| Reweight or reposition the original sites | None of exp149,151,153 quantifies over these changes. | An explicitly bound support/site proposal followed by complete exact coverage below seven, or a valid obstruction for its declared enlarged family. A failed solve or finite-support optimum is not a universal impossibility. |
| Unit-parent centre restrictions | Concentric selection supplies the universal half-box. The signed-L1 frame-aware formula is an analytic derivation awaiting independent audit, and can be intersected with the existing B-core box. | Independent proof/source review, followed by exact footprint comparison or fixed-witness compatibility under the derived domains. Strict footprint growth and witness removal are different outcomes and both remain unmeasured. |
| Joint-owner compatibility | Exp150 supplies only four individual core witnesses for one residual core. | One jointly separated four-owner-plus-residual core witness would establish feasibility of that necessary core model at those poses. A bounded failed search would not prove infeasibility; universal exclusion needs exhaustive branches and exact replay. Contained unit-parent realizability remains a further condition. |
| Owner-pose refinement | A common footprint forgets centre and angle correlations by construction. | A proved exhaustive subdivision, with measured stronger footprints or compatibility exclusions and eventual full-direction covers. No evidence yet gives the size of a sufficient refined census. |
| Structural routing | The corner-pair theorem supplies distinct owners; the endpoint-sector routing needed for the small D/D-image portfolio is unproved. | A theorem sending every hypothetical packing to at least one fully excluded tuple, with correct overlap and mark choices, or a counterexample within the stated necessary model to a proposed routing lemma. Merely proving endpoint-sector membership would not finish the presently uncertified endpoint combinations. |
| H135 full-support pricing | The transport control is retained and the pointwise paired-pricing target remains unrun. | One same-orbit exact depth comparison under the frozen first32/full rationalized dual supports. Acceptance would identify the truncation mechanism; a useful covering or packing conclusion requires subsequent separately justified work. |
| Other global or conditional proof architectures | The owner ledger is one sufficient architecture. Existing global weighted covers, angle restrictions, and penetration/contact premises have distinct retained scopes. | Explicit prerequisites and an exact contradiction in the relevant physical or necessary-core domain. No present experiment compares their total cost or establishes owner geometry as the sole remaining route. |

The evidence supports the specific fixed-family negative and the exact conditional
baseline certificate.
Choices among the unmeasured alternatives should be recorded as prospective judgments
attached to those definitions and criteria.
Source-admission GO, passing controls, target completion, a valid analytic implication,
and a stronger physical theorem are separate facts.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
