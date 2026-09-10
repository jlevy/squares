# BC318: Exact Containment Transfer from the Retained Five-Dot Certificate

**Design admission, 2026-09-09.** The next containment experiment may use at most 128
component relations after a complete, valid exp146 wall-footprint receipt and a
separately published prospective protocol are available.
Exp146 was unrun at the previous cutoff; the coordinator reports that the user has now
authorized a fresh research window.
This design evaluates no wall geometry or target containment and records no scientific
result.

The order is sound: finish the sixteen-class geometry discriminator, then test the small
containment matrices before constructing a shared arrangement.
A complete result in which every possible wall footprint equals its old footprint
permits an analytic disposition of BC318 without a redundant containment target.

## Frozen Inputs and Certificate Authority

Freeze q = 96/25, B = 9977/10000, h = B/2, angle-limit parameter 207107/500000, 180
direction steps, all 361 canonical orientations, all 1444 signed rays, the sixteen
bottom-left classes, and the retained boundary policy.
The class order is `m1:j0` through `m1:j7`, then `m2:j0` through `m2:j7`. The marks are

$$m_1=(3152/3175,2336/3175),\qquad m_2=(2336/3175,3152/3175).$$

The source of the certified old polygons and five dots is the unchanged exp143 endpoint
receipt, whose retained Git blob is `cc66f06ddd3f7cc52d8a06d30a3920ba8e992c19`. Bind its
path and blob, the exact exp144 and exp145 evidence actually adopted by the coordinator,
the completed exp146 receipt, and the containment implementation through Git.
Record their repository-relative paths and full revisions.
A coverage certificate requires its completed exact coverage evidence and analytic
transfer; the exp143 numerical proposal alone supplies candidate geometry.
A string saying “complete” is not a substitute for the admitted receipt and its scope.

Use the existing frozen-input loader and geometry primitives where applicable.
Require the old polygons and dots to match the retained input exactly.
In the wall receipt, require all sixteen unique classes in order, the frozen settings,
and a completed disposition for every required signed frame.
Resolve frame rays, orientation indices, quarter-turn selectors, and complete source
lists against the generated manifest.
A missing frame, class, or source is invalid input.
Preserve the admitted point and segment policy.
Do not rebuild a second wall constructor or change exp146’s settings to make a
containment pass.

The existing source’s `ENDPOINT_FOOTPRINT_STATUS` is a geometry-layer status.
The mathematical authority for this use is the retained endpoint proof and five-dot
transfer review, together with completed coverage evidence.
Record that dependency explicitly rather than upgrading a status string.

Sources: [wall constructor contract](wall-constructor-contract.md),
[constructor source](../../devtools/wall_owner_footprints.py),
[frozen-input loader](independent_union.py), and
[five-dot transfer review](../../campaign/series/series-000-smoke-and-calibration/results/agenda-032/proofs/five-dot-transfer-review.md).

## Two Occupied Tuples and Four Patch-and-Dot Pairs

Define the affine container maps explicitly:

$$
H(x,y)=(q-x,y),\quad V(x,y)=(x,q-y),\quad
R=HV,\quad S(x,y)=(y,x).
$$

Use corner order BL, BR, TL, TR and maps $(F_c)_c=(I,H,V,R)$. Let E be the saved
bottom-left exp143 endpoint polygon.
The two certified component families are

$$P_{0,c}=F_c(E),\qquad P_{1,c}=F_c(S(E)).$$

The corresponding old class tuples in these reflected local coordinates are

$$b_0=(m_1{:}j0)^4,\qquad b_1=(m_2{:}j7)^4.$$

Diagonal reflection exchanges BR and TL; BL and TR stay fixed.
Thus $S(P_{0,c})=P_{1,S(c)}$. Applying S to each stored component without that corner
permutation gives the wrong indexed family.

Let D be the five retained dots:

$$
D=\{(73/75,187/90),(793/450,43/15),(48/25,48/25),
(187/90,73/75),(43/15,793/450)\}.
$$

Write $D_0=D$ and $D_1=H(D)$. Exact set equality gives $S(D)=D$, $R(D)=D$, and
$V(D)=H(D)$. The retained stabilizers therefore supply these four pairs:

| Global transport of the retained certificate | Occupied family | Dot pattern |
| --- | --- | --- |
| I | $P_0$ | $D_0$ |
| H | $P_0$ | $D_1$ |
| S | $P_1$ | $D_0$ |
| $S\circ H$ | $P_1$ | $D_1$ |

There are two occupied geometries and four paired certificates.
Both dot patterns accompany each occupied geometry, so they do not multiply the number
of containment relations or newly covered tuples.
No additional full-net covering run is needed to transport a completed certificate by a
verified global symmetry.

For every global map $g(x)=Lx+b$, resolve the transformed core orientation through exact
geometric lookup modulo quarter-turns in the full manifest.
Require a bijection on all 361 orientations.
Transport dots, physical corners, patches, and any certificate direction references
together.

Owner displacement boxes require an ordered frame.
With J the counterclockwise quarter-turn, use $r'=Lr$ when $\det L=1$ and $r'=L(Jr)$
when $\det L=-1$. For a reflection, $Jr'=Lr$: the two axes exchange roles.
For S this is $r'=S(Jr)$, and the local class map is
$\tau(m_a{:}j)=(m_{3-a}{:}(7-j)\bmod8)$. If support receipts are transported, include
the affine translation: the reflected first interval is the old second interval plus
$r'\cdot b$; the reflected second interval is the old first interval plus $Jr'\cdot b$.
Resolve target source lists afresh.
Polygon transport alone suffices for BC318; support transport does not require another
implementation layer.

Source: [owner-case census design](owner-case-census-design.md).

## The 128 Relations and Their Meaning

For each possible bottom-left class k, let $A_k$ be its admitted wall footprint and set
$A_{c,k}=F_c(A_k)$. Preserve impossible classes as dispositions without polygons.
For e in $(0,1)$, c in $(\mathrm{BL},\mathrm{BR},\mathrm{TL},\mathrm{TR})$, and k in the
fixed sixteen-class order, test

$$M_{e,c,k}:\quad P_{e,c}\subseteq A_{c,k}.$$

That direction of inclusion is required: larger guaranteed occupied sets leave smaller
residual domains. Test the vertices of the certified old patch against every closed
half-plane of the positive-area convex wall polygon.
For a counterclockwise edge $(a,b)$, the test is $\operatorname{cross}(b-a,v-a)\ge0$.
Exact equality passes.
With convexity validated, membership of every old vertex proves the complete
containment. Area, bounding boxes, sampled points, and a centroid do not establish this
relation.

Record one of `contained`, `not-contained`, or `impossible-class` for each completed
logical slot. A failed relation should retain the first old vertex and wall edge with a
negative exact cross product in the frozen order.
That is a counterexample to component containment, not an escaping residual core.
A missing or invalid calculation has a separate unresolved or invalid disposition.
An impossible class has no containment truth value; do not interpret its absent polygon
as an empty intersection, the plane, or a universal pass.

Evaluate all 128 logical slots initially, with at most 128 polygon-containment tests and
skips for impossible classes.
The corner maps imply $M_{e,c,k}=M_{e,\mathrm{BL},k}$ for every possible k. Keep the
four corner rows as transport controls.
There are only 32 distinct relations after pullback, but do not silently report 128
executed tests if an implementation computes 32 and transports the other slots.

For one tuple $t=(k_c)_c$, a *single* e with all four component relations gives

$$\bigcup_cP_{e,c}\subseteq\bigcup_cA_{c,k_c}.$$

Every strict residual core avoiding the latter union then avoids the certified former
union and meets a dot from either paired pattern.
Seven mutually disjoint residual cores cannot each meet one of five dots.
The tuple therefore inherits a conditional exclusion under the existing physical
transfer premises. The wall polygons need not be pairwise disjoint for this implication.

All four relations must use the same certified family e. Combining some components from
family 0 with others from family 1 does not preserve a certified occupied union.
Failed component containment leaves whole-union containment and direct dot coverage
unresolved.

## Tuple Counts and Impossible Classes

Let $L_c$ be the set of individually possible class labels at corner c, and put

$$S_{e,c}=\{k\in L_c:M_{e,c,k}=\mathrm{contained}\},\qquad
C_e=\prod_cS_{e,c},\qquad C=C_0\cup C_1.$$

The correct union count is

$$|C|=\prod_c|S_{0,c}|+\prod_c|S_{1,c}|-
\prod_c|S_{0,c}\cap S_{1,c}|.$$

Taking $\prod_c(S_{0,c}\cup S_{1,c})$ is unsound: it includes mixed-family tuples
without one complete inherited certificate.
A tuple in both $C_e$ has two available occupied-family proofs and is counted once.
Dot-pattern choices do not multiply this count.

Within the raw label universe $U=\{0,\ldots,15\}^4$, retain these disjoint dispositions:

| Disposition | Definition and count |
| --- | --- |
| Structurally impossible by an individual class | $I=U\setminus\prod_cL_c$, with $\lvert I\rvert=65536-\prod_c\lvert L_c\rvert$ |
| Excluded by inherited dot coverage | C, counted by the formula above |
| Unresolved | $(\prod_cL_c)\setminus C$, with count $\prod_c\lvert L_c\rvert-\lvert C\rvert$ |

Corner transport makes the four $|L_c|$ equal, so $|I|=65536-|L_{\mathrm{BL}}|^4$. An
impossible class requires every required frame to have completed with an empty centre
set. A partial frame list never supplies this premise.

Report new inherited exclusions as $C\setminus\{b_0,b_1\}$, with count
$|C|-|C\cap\{b_0,b_1\}|$. If a baseline tuple is structurally impossible, retain its
known conditional certificate as historical evidence but place that tuple only in I in
the disjoint disposition table.
List the lexicographically first new tuple and its one complete family of four
successful relations as a compact expansion witness.

These are counts of labelled sufficient conditions.
The closed sectors overlap at endpoints, and a selected owner can contain more than one
mark. Labels do not define disjoint physical cases, and an individually possible class
need not participate in a jointly feasible four-owner tuple.
A fraction of 65,536 cannot be described as a fraction of possible packings.
If distinct wall polygon tuples coincide, report that geometric duplication separately
while retaining every covered label.
The retained endpoint equality discriminator identifies the two baseline geometries;
label membership alone does not establish physical feasibility.

## Minimum Controls Before the Target Freeze

Extend the existing exact predicates with a small public-path suite.
Keep exp146’s admitted constructor controls as prerequisites; a second clipper or a new
geometry engine is unnecessary.

1. **Containment direction and boundary.** Use rational convex fixtures for equality,
   strict inclusion, shared edges and vertices, and a failure with one exterior vertex.
   Reverse a strict inclusion and require failure.
   Include equal-area translated polygons to reject an area-only decision.
   Apply the rational rotation with first axis $(3/5,4/5)$ to the same fixtures and
   retain the answers. Normalize cyclic starts and winding without silently replacing a
   malformed nonconvex polygon by its larger convex hull.
2. **Whole-container transport.** Use asymmetric rational polygons, labelled corners,
   and dots to check S’s BR/TL exchange, reflection involutions, $S H S=V$, and
   simultaneous point/polygon transport.
   Include an oblique ordered-frame fixture that fails under $r'=S(r)$ and passes under
   $r'=S(Jr)$. Verify the full manifest permutation and source resolution using the
   declared net; this does not evaluate a wall class.
3. **Dispositions and input refusal.** Synthetic manifests must distinguish a completed
   all-empty class, a nonempty point or segment frame, a missing frame, a partial class
   list, and inconsistent possible/absent-polygon data.
   Require refusal for wrong q/B, class identity/order, source binding, and incomplete
   or duplicated frame provenance.
   Impossible slots must not set containment-mask bits.
4. **Cartesian products and overlap.** In a four-coordinate toy universe with four
   labels per coordinate, let label 3 be impossible, family 0 accept $\{0,1\}$ in every
   coordinate, and family 1 accept $\{1,2\}$. Require 175 impossible, 31 covered, and 50
   unresolved tuples; the two products each have size 16 and overlap in one tuple.
   The union-of-per-coordinate-masks error would falsely certify all 81 individually
   possible tuples. Compare the formula with direct toy enumeration and ensure missing
   rows cannot produce a completed count.

At target execution, require exact agreement between the saved base polygon and the
corresponding old endpoint in the admitted input, all applicable same-class nesting
relations, corner-row equality, and the S-induced class permutation between the two
families. These are recorded source and transport checks.
They must not be used to tune target footprints or redefine a failed relation.

## Prospective Verdict and Next Action

Publish the input bindings, deterministic e/c/k order, acceptance rule, operational
guard, output path, and no-adaptive-retry policy before evaluating any target relation.
Use one small adapter to existing exact geometry and receipt loading.
Save the matrices, masks, exact counts, failed-relation witnesses, and certificate
references. The coordinator assigns the successor hypothesis and experiment identifiers;
BC318 does not reuse H144’s geometry-only claim.

| Verdict | Required evidence |
| --- | --- |
| Accept containment expansion | Complete valid inputs and matrices, every required control, and $C\setminus\{b_0,b_1\}\ne\varnothing$, with a retained certificate chain for a selected new tuple |
| Refute expansion by this containment rule | Complete valid inputs and matrices with no new tuple, or the exact all-equal obstruction below; direct coverage remains unresolved |
| Incomplete | A guard expires or required relations or certificate evidence remain missing |
| Invalid | A source, geometric, permutation, nesting, or counting guard fails; no scientific accept/refute follows |

| Exp146 outcome, presently unknown | Ranked next action |
| --- | --- |
| Complete, valid, with at least one proper enlargement | Run the frozen BC318 relations first. If they extend the certificate, publish the exact covered/impossible/unresolved ledger, then take the first unresolved tuple. If they do not, use a fixed-pattern escape bank and one selected complete cover check before a large arrangement. |
| Complete with impossible classes, but every possible footprint unchanged | Record the impossible-label product first. The retained equal-area and equality discriminator proves there is no new containment transfer among the remaining old footprints. Dispose of BC318 analytically, then investigate the surviving unresolved classes. |
| Complete, every class possible and every footprint unchanged | The same old-footprint obstruction rules out containment expansion. Move to the fixed-pattern escape/candidate discriminator; another unchanged containment target answers no new question. |
| Partial or invalid | Preserve all valid completed evidence and name the exact missing or failed prerequisite. Complete or repair that prerequisite in an explicitly scoped continuation before certificate-dependent target work. A repair cannot silently change the frozen scientific settings. |

For the next direct-cover slice, freeze a tuple and one dot pattern before a complete
361-direction check.
A checked escaping core supplies class-avoidance masks and refutes only that fixed
pattern on their Cartesian product.
Old escapes must be replayed after footprint enlargement.
Use common dots before class-specific obstacle tests; subtracting all 64 optional owner
obstacles is unsound.
If this route stalls, the mathematical decision lane should choose a bounded six-dot
candidate, the stronger existential-owner domain, or one selective refinement whose
children cover their parent.
A full arrangement is justified by the unresolved structure, not by the 65,536-label
count alone.

Source: [overnight strategy review](overnight-strategy-review.md).

## Remaining Requirements for a Global n11 Statement

The retained certificate excludes prescribed owner tuples.
Exp146 can strengthen their guaranteed footprints or eliminate classes.
A successful BC318 can exclude further tuples.
None of these conclusions alone exhausts the corner owner cases.

A global claim at the unchanged q requires an explicit disposition covering every
admissible selected-owner tuple.
Every hypothetical packing must produce four distinct owners under the corner-pair
theorem, with selected rational-net cores in at least one of the sixteen declared
classes at each corner.
Every such selection must land in a proved impossible case or in a case with an accepted
exclusion. Overlap of labels is harmless for exhaustive coverage but cannot increase the
physical case count.
An explicit owner-selection rule may instead route every hypothetical packing into a
proved subset of the raw label universe.
Such a rule needs its own exhaustive argument; overlap of labels supplies no routing
theorem.

Each exclusion needs either a complete retained certificate and the exact containment
chain above, or a complete new coverage proof.
It must retain the same container/core parameters, all required directions or proved
symmetry transport, the strict-core containment inequality, the owner-footprint lemma,
and the seven-residual-core counting argument.
A failed component relation, an empty witness bank, or a prefix survivor does not close
an unresolved tuple.
If refinements are used, their children must exhaust the parent; if q or B changes, the
marks, ownership, net transfer, and coverage arguments need corresponding justification.
The project claim registry must record the final composed evidence and assurance
separately from the geometry experiment.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
