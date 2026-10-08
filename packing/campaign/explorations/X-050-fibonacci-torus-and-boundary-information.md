---
title: X-050 — Fibonacci Tori, Contact Equations, and Boundary Information
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-050
  title: Fibonacci Tori, Contact Equations, and Boundary Information
  date: '2026-10-07'
  author: Codex coordinator with independent algebra, geometry, and source reviewers
  campaign: packing.squares
  brief: >-
    Evaluate the owner's unverified Pingyou abstract, reconstruct its checkable
    mathematics, and assess whether marked tori or related representations can
    simplify the eleven-square proof or advance seventeen-square and other cases.
  sources:
    - packing/resources/web/pingyou-fibonacci-torus-2026-10-07/abstract.png
    - packing/resources/web/pingyou-fibonacci-torus-2026-10-07/abstract.md
    - packing/frontier/n-011.md
    - packing/frontier/n-017.md
    - packing/cases/trump11/packing.py
    - packing/atlas/known-best/contact-structures.json
    - docs/project/reviews/review-2026-10-07-fibonacci-torus-algebra.md
    - docs/project/reviews/review-2026-10-07-fibonacci-torus-geometry.md
    - docs/project/reviews/review-2026-10-07-fibonacci-torus-sources.md
    - https://doi.org/10.1090/S0002-9939-97-03930-0
    - https://trump.de/square-packing/Packing-11-squares.pdf
  proposes: []
---
# X-050: Fibonacci Tori, Contact Equations, and Boundary Information

**There is useful mathematics here, especially a compact explanation of Trump’s contact
equations. There is no demonstrated torus shortcut to the global packing problem.** The
finite-field claims have substantial exact content, but their label symmetries do not
preserve the contacts of the eleven physical squares.
Removing the walls also makes the torus problem much easier: explicit periodic packings
already exist below the relevant finite-container sides.

This is W1 source intake, W2 confirmation of reconstructible claims, and W3 assessment
of the next questions.
It is not a new optimality result or a completed replay of the unseen manuscript.
The intake is `think-hleq`; the
[plan](../../../docs/project/specs/active/plan-2026-10-07-fibonacci-torus.md) records
the parallel review lanes and confirmation contracts.

## What Was Supplied and What Is Already Known

The two supplied screenshots are identical files.
They show one abstract and a diagram, with the title *The Fibonacci Geometry of Eleven
Squares* and the author line “PINGYOU LTD.” Tesseract OCR followed by visual correction
recovered all visible text.
The [source packet](../../resources/web/pingyou-fibonacci-torus-2026-10-07/README.md)
retains the pixels, raw OCR and corrected transcription.
Searches did not find the full manuscript.
Its date, authorship beyond the printed line, map definitions and proofs remain
unavailable; this does not establish that no manuscript exists.

The current [eleven-square record](../../frontier/n-011.md) already has
$s(11)=3.8770835900228141773\ldots$ at the exact algebraic endpoint, through the
separate global proof T-060 and the construction T-011. The uniqueness result has its
own scope and review.
The [seventeen-square record](../../frontier/n-017.md) remains open, with verified lower
bound $4.66044275$ and a rational upper witness displayed as $4.67553009360455\ldots$.
Historical text elsewhere still calling eleven open must not reset this baseline.

The meaningful targets are therefore a simpler explanation or smaller verified proof for
eleven, and a new necessary inequality or complete structural reduction for seventeen.
Recovering an already known endpoint polynomial is a diagnostic, not a new bound.

## Claim-by-Claim Disposition

The exponent indexing a quotient is called $m$ below; $N$ counts packed squares.
The source uses $n$ for the exponent, which can otherwise suggest a false identification
with the packing count.

| Visible claim (stable intake ID) | Disposition from this audit | What remains |
| --- | --- | --- |
| FIB-C01: a reversible marked-torus representation recovers all eleven squares and clearances | Unverified as a source theorem: the cells, lattice, mark and inverse are not defined on the supplied page | Obtain the map and prove forward validity and inverse reconstruction on the stated domain |
| FIB-C02: contact equations contain $I+wQ$ | Independently supported: reconstruction of the actual contact family yields $\det(I+wQ)=1+w-w^2$ exactly | Identifying this determinant does not identify the full claimed matrix equation or torus |
| FIB-C03: two clearances yield the degree-eight endpoint and a $1/4$ cusp estimate | Independently proved for the reconstructed family on $u\in[9/25,37/100]$, $L\in[387/100,389/100]$, including every wall and pair | The abstract’s unstated full parameter domain cannot be certified from the screenshot |
| FIB-C04: $R_5\cong\mathbb F_{11}$, with regular action on the 55 unordered pairs | Verified algebraically, including the exceptional exponent classification | No geometric equivariance follows |
| FIB-C05: a 121-cell cover has 55 two-element return orbits corresponding to pairs | Reconstructed exactly in $R_{10}\cong\mathbb F_{11}\times\mathbb F_{11}$ | Identification with the pictured geometric cover is still missing |
| FIB-C06: the bundle with monodromy $-Q^3$ recovers these finite structures | Algebraically plausible, with an essential distinction between homology modules and finite quotients | Cyclic-cover torsion naturally gives $R_{3k}$; the intended meaning of “recover” must be specified |
| FIB-C07: the tori lie on a shortest modular geodesic of length $4\log\varphi$ | That length is the standard shortest hyperbolic length for the oriented modular quotient | Membership of the manuscript’s normalized tori in that geodesic is unverified |
| FIB-C08: the endpoint field has degree eight and normal closure group $S_8$ | Independently verified for the retained side polynomial by finite-field factor certificates | This supplies no global geometric exclusion |
| FIB-C09: an explicit rational counterexample to Erdős #106 is given | The source’s particular witness is unavailable | The problem concerns unequal square sizes and side sums; existing public reports do not authenticate this source’s construction |

The independent
[algebra review](../../../docs/project/reviews/review-2026-10-07-fibonacci-torus-algebra.md),
[geometry review](../../../docs/project/reviews/review-2026-10-07-fibonacci-torus-geometry.md),
and
[source review](../../../docs/project/reviews/review-2026-10-07-fibonacci-torus-sources.md)
give the derivations and retrieval limits.
Executable checks and receipts live in
[the confirmation case](../../cases/fibonacci_torus/README.md).

## The Contact Equations Are the Strongest Positive Finding

Use $u=\tan(\theta/2)$, $c=(1-u^2)/(1+u^2)$ and $s=2u/(1+u^2)$. Keep the construction’s
square-placement formulas and make the enclosing side $L$ free.
Twelve pair contacts persist.
The other two active clearances impose $L\ge f_1(u)$ and $L\ge f_2(u)$, where

$$
f_1(u)=\frac{6u+4}{1+2u-u^2},\qquad
f_2(u)=\frac{4(u+1)(u^6-2u^5+2u^4+7u^3-2u^2+u+1)}{D(u)},
$$

$$D(u)=u^8-2u^7-2u^5+14u^4+2u^3+2u+1.$$

Their difference factors as

$$
f_1(u)-f_2(u)=\frac{2u\,p(u)}{(1+2u-u^2)D(u)},
$$

$$p(u)=5u^8-10u^7-2u^6+14u^5+12u^4-6u^3+2u^2+2u-1.$$

This is the retained half-angle polynomial.
On $u\in[9/25,37/100]$ and $L\in[387/100,389/100]$, all 44 supporting wall inequalities
and 53 other pair separations hold identically or by exact interval bounds.
All fourteen alternative separating features of the two active pairs are strictly
unavailable, so feasibility is equivalent to these two clearances being nonnegative.
The checker proves $f_1'>1/4$, $f_2'<-1/4$ and a unique crossing $u_*$. The least
feasible envelope occurs where both clearances become tight, giving $L-T_*\ge |u-u_*|/4$
throughout this feasible family.
These are rational Bernstein certificates over the whole rectangle, not sampled signs.
This is a practical simplification of the *family calculation*.

The coefficient of $L$ in the second reconstructed clearance is

$$\frac{1+w-w^2}{c\,s^2},\qquad w=cs.$$

The Fibonacci determinant is therefore a real consequence of the contact equations.
Its occurrence deserves investigation.
It still does not establish that the torus encoding reduces the number of geometric
obligations: elimination of a small coupled linear system naturally introduces its
determinant.

For a global proof, a further statement must force every hypothetical better packing
into this family or into finitely many similarly controlled alternatives.
That is the expensive logical step in the existing proof.
An encoding of the displayed optimum does not supply it.
A post-hoc classification using the already proved global theorem would be circular as a
proposed replacement proof.

## Why Eleven Is Arithmetically Special

Let $\mathcal O=\mathbb Z[\varphi]$. Multiplication by $\varphi$ on the basis
$(1,\varphi)$ is $Q$. Thus

$$|R_m|=|\det(Q^m-I)|=L_m-1-(-1)^m,$$

where $L_m$ is the Lucas sequence.
The first values, for $m=3,4,5,6,7,8$, are $4,5,11,16,29,45$. The generated affine group
has order $m|R_m|$; a free transitive action on unordered pairs requires

$$m|R_m|=\frac{|R_m|(|R_m|-1)}2,\qquad |R_m|=2m+1.$$

The algebra review proves that among $m\ge3$ this happens only at $m=5$, and verifies
the action there. In $R_5$, $\varphi=4\pmod{11}$ and $\langle4\rangle=\{1,4,5,9,3\}$.
Translations and these five multipliers give 55 maps acting regularly on the 55 pairs.

The 121-cell statement also has a coherent exact model: $\varphi^{10}-1=11\varphi^5$, so
$R_{10}=\mathcal O/(11)$. Since $t^2-t-1=(t-4)(t-8)$ modulo 11, the Chinese remainder
coordinates have return map $(\alpha,\beta)\mapsto(\alpha,-\beta)$. There are eleven
fixed points and 55 two-cycles.
For $\beta\ne0$, the map $[\alpha,\beta]\mapsto\{\alpha\pm\beta^{-1}\}$ is a bijection
to unordered pairs.
The marked-coordinate translation must be chosen correctly; it is not
every translation in the quadratic ring.

This calculation verifies a finite incidence model, not a contact model.
The reciprocal midpoint/half-difference bijection exists over every odd finite field.
What is special here is its compatibility with the chosen Fibonacci multiplier and
cover, not the existence of a pair parametrization.

### The Physical Squares Have No Such Permutation Symmetry

The eleven-square contact graph has 14 edges and a trivial automorphism group.
Its three degree-four vertices have distinct multisets of neighboring degrees; fixing
those vertices successively fixes all eleven.
The retained checker makes this argument explicit.
Consequently the 55-element affine group cannot act nontrivially as contact-preserving
permutations of these physical squares.

Relabeling the 55 pair inequalities may be convenient.
Replacing them by one inequality requires an additional equivariance theorem preserving
every relevant quantity, including walls, orientations and which pairs touch.
Neither a bijection nor equal cardinality provides that theorem.

### What Fails at Seventeen

There are 136 unordered pairs of seventeen labels.
A group acting on the seventeen labels with a free and transitive induced action on
their unordered pairs would have order 136, hence contain an involution.
The label action must be faithful because the pair action is free.
Any nonidentity involution on seventeen labels swaps some pair, fixing that unordered
pair. That contradicts freeness.
This rules out the exact regular-pair analogue induced by **any** group of label
permutations, not just Fibonacci multipliers.
It says nothing against an arbitrary regular action on an abstract 136-element set.

There is also a field obstruction: $5$ is not a square modulo 17, so $t^2-t-1$ has no
root in $\mathbb F_{17}$. Thus there is no unital quotient map
$\mathbb Z[\varphi]\to\mathbb F_{17}$. The quadratic residue construction instead gives
$\mathbb F_{289}$ modulo 17. These facts do not rule out all periodic representations
for seventeen; they rule out two specific ways of copying the eleven-label mechanism.

For example, $A=\left(\begin{smallmatrix}-2&5\\5&-13\end{smallmatrix}\right)$ has
determinant one and $|\det(A-I)|=17$, so a seventeen-element quotient is easy to
manufacture with another hyperbolic matrix.
That observation is a warning against choosing the arithmetic after the desired count:
it becomes useful only when the square contacts independently force that matrix.
The actual seventeen-square endpoint has two unequal oblique orientations and slider
freedom; its known degree-eighteen polynomial is already registered.
A reversible continuous encoding of the full family must account for those degrees of
freedom through additional parameters or marks.
A separately proved feasibility-preserving reduction could instead canonicalize or
eliminate sliders; it need not encode every original configuration reversibly.

## A Torus Without Its Seams Is Too Weak

There are two different constructions to distinguish.
Periodizing an actual square packing keeps the original unit squares on a torus.
Encoding it with newly shaped square–rectangle cells can preserve information through a
marked inverse, but it does not automatically preserve Euclidean distances, areas, or
square-packing inequalities.
Either route needs its own transfer theorem.

For the ordinary torus relaxation, the obstruction is quantitative.
Set $m=\lfloor\sqrt N\rfloor$, $S=N/m$, and use centres

$$\left(\frac j m,\;j\bmod S\right),\qquad j=0,\ldots,N-1,$$

on the square torus of side $S$. The retained exact checks verify all 55 pairs for
$N=11,S=11/3$ and all 136 for $N=17,S=17/4$, using two different overlap predicates.
The unit squares are axis-parallel; allowing rotations only enlarges the relaxation.
These are not configurations inside an ordinary square of that side.

This agrees with Reztsov and Sloan’s 1997 theorem on axis-parallel torus packing:
$N_2(\lambda)=\lfloor\lambda\lfloor\lambda\rfloor\rfloor$ for $\lambda>2$, in
unit-square scaling.
Their particular Fibonacci-lattice family has separate properties and must not be
confused with the quotient-ring construction here.
See the
[primary-source account](../../../docs/project/reviews/review-2026-10-07-fibonacci-torus-sources.md#the-torus-precedent-and-its-boundary-limitation).

Every wall-contained packing periodizes, but many periodic packings cannot be cut open
along a vertical and a horizontal seam without cutting a square interior.
An ordinary torus infeasibility argument therefore cannot prove the desired bounds: it
admits packings at $3.666\ldots$ and $4.25$. A promising torus invariant must retain the
existence of appropriate empty seams or equivalent wall information.

For these axis-parallel unit squares, that missing information has a simple exact test.
A vertical seam avoiding all square interiors exists if and only if the largest cyclic
gap between their horizontal centre coordinates is at least one; the same holds with the
coordinates exchanged for a horizontal seam.
Consecutive centres must leave room for the two half-widths, with equality allowing a
cut through touching boundaries.
The checker verifies largest gaps of $1/3$ on both axes for eleven and $1/4$ on both
axes for seventeen, so neither periodic example can be cut into a bounded packing.
An independent endpoint-enumeration check and controls at, above and below gap one test
the criterion. For arbitrary rotations, use the actual projected half-widths instead;
this equal-width formula must not be applied unchanged.
The criterion restores containment information; by itself it does not compress the
global bounded problem or improve its known lower bound.

This supplies a cheap control for any future proposal.
First check that it rejects these seam-free examples for a justified reason while
retaining the genuine bounded packing.
If it cannot distinguish them, refining its arithmetic is unlikely to help the
finite-container lower bound.
These controls target periodizations of actual unit squares.
They do not refute a separately defined square–rectangle cell encoding with a valid
marked inverse; that encoding needs its own transfer and necessity theorems.

## What the Galois and Modular Claims Buy

For the retained degree-eight side polynomial, the algebra checker verifies
irreducibility modulo 29 and factor degrees $1+7$ modulo 7 and $1+2+5$ modulo 73. These
certify a transitive group with a seven-cycle, hence a doubly transitive group, and a
transposition obtained from a power of the last permutation.
Conjugating that transposition proves the full symmetric group $S_8$.

Thus a general expression by radicals for the endpoint is unavailable.
This does not prevent short implicit formulas, rational parametrizations before imposing
the final contact, or short inequality proofs.
There is a stronger obstruction to identifying the golden ratio with the endpoint field.
In the certified natural $S_8$ action, $\mathbb Q(T_*)$ is fixed by the point stabilizer
$S_7$, which is maximal in $S_8$. Galois correspondence therefore gives no proper
intermediate field between $\mathbb Q$ and $\mathbb Q(T_*)$; in particular,
$\varphi\notin\mathbb Q(T_*)$. This concerns the root field, not the full splitting
field, and does not prevent an integer Fibonacci matrix or auxiliary golden
eigendirections from organizing the contact equations.
The torus description may explain those equations without reducing their algebraic
degree.

Likewise $4\log\varphi$ follows from a smallest hyperbolic trace, three, in
$\mathrm{PSL}_2(\mathbb Z)$: $Q^2$ has expanding eigenvalue $\varphi^2$ and translation
length $2\log(\varphi^2)$. A short modular geodesic is not a short container side.
The missing step would be a proved relation between a torus functional and packing
feasibility throughout a necessary class of configurations.

## Ranked Directions and First Discriminators

These are W3 judgments.
None is an accepted W6 experiment or a claim that the current seventeen-square lower
bound has improved.

| Priority | Direction | Why it may help | Smallest decisive next result | Stop or redirect when |
| --- | --- | --- | --- | --- |
| 1 | Extend the checked n11 contact-family simplification toward the existing local proof | The exact family theorem here exposes the endpoint and cusp directly | Derive the envelope from all 128 local branches without assuming common angles or persistent contacts, or identify precisely which extra modes prevent that reduction | The simplification assumes the family but is presented as global capture, or adds more obligations than it removes |
| 2 | Recover and audit the marked inverse from the full source | Establishes exactly what information the torus retains | Explicit forward/inverse formulas, cell congruence, and a list of properties preserved | Only the known optimum is encoded and no larger geometrically necessary domain is covered |
| 3 | Boundary-aware periodic lifts and seam defects | The exact seam criterion here identifies the information ordinary torus relaxation loses | A seam-derived relation coupling complete pose domains that excludes a checked region admitted by the current relaxation | The invariant depends only on unmarked lattice arithmetic, density or cell count, or merely restates full containment |
| 4 | Eliminate a constrained n17 contact core while retaining slider fibres | Could shorten endpoint/capture certificates with multiple orientation variables | A smaller exact inequality system equivalent on a named closed chart, covering every slider endpoint and branch | Degree reduction or an attractive diagram is the only gain; existing H-254 through H-258 already cover the needed result |
| 5 | Contact-cycle displacement labels and exact stresses | Periodic rigidity suggests organizing equations by cycles and redundant constraints | A checked relation coupling complete square-pose domains, or a smaller exact dual certificate with all branches retained | Generic bar counts or graph symmetry substitute for unilateral SAT geometry |
| 6 | Periodic dual measures with explicit boundary and corner terms | Existing measure certificates already combine periodic interiors with nonperiodic boundary information | A new exact resource inequality improving a matched finite relaxation, or a uniform family transfer | It merely refines the unchanged scalar charge beyond its known ceiling |
| 7 | Semialgebraic elimination and sum-of-squares certificates on captured patches | Rational half-angle coordinates permit exact sign checks and small certificate search | A positive-width excluded region or verified envelope on an already complete chart cover | A resultant is treated as feasibility, complex roots are counted as real poses, or uncovered charts remain |
| 8 | Periodic constructions, cut-and-project and translation-surface analogies as search seeds | Useful source of structured candidate families | Exactly verified bounded witnesses, followed by a preregistered comparison against existing seeds | A periodic density improvement cannot survive cutting and wall repair |

The current [X-048 program](X-048-n17-optimality-after-n11.md) already owns endpoint
algebra, contact charts, local stress and capture.
Those routes should absorb useful formulas instead of being duplicated under a
“Fibonacci” label. The main distinct candidate from this audit is a *necessary
boundary-aware invariant*, with the two explicit periodic packings as negative controls.
Generalizing Fibonacci numerology before establishing that invariant has low expected
value.

For other counts, investigate arithmetic/contact families only when the geometry
independently produces the integer matrix or recurrence.
The quotient-size sequence $4,5,11,16,29,45,\ldots$ is not a sequence of optimal
finite-square packing counts.
Periodic boundary/corner methods may transfer across $k^2-d$ families, where the
existing campaign already has concrete hypotheses.
Counts congruent to three modulo four can admit regular unordered-pair affine actions
over prime fields, but that necessary arithmetic pattern is not evidence of packing
geometry.

## Scope, Missing Evidence, and Handoff

No new packing bound, global normal form, geometric torus equivalence, or proof-size
reduction is established by this report.
The gains are exact reconstructible algebra, a local contact-envelope explanation,
rigorous obstructions to two tempting generalizations, and controls that make future
proposals easier to reject or justify.

The manuscript’s source, inverse map, claimed full parameter domain and rational Erdős
witness remain missing.
Erdős #106 concerns unequal squares maximizing total side length in a unit square.
The reported seventeen-square constructions do not solve the congruent seventeen-square
minimum-container problem.
The source review preserves public reports and contradictory status metadata without
turning them into a replay.

The selected independent proof-simplification follow-up is `think-zbkk`: test whether
the checked envelope can be derived across the existing captured local branches without
assuming the contact family.
The next source-dependent slice, tracked by `think-aj43`, is to obtain the full
manuscript and check its inverse against the retained packing coordinates.
The independent mathematical slice is to derive one necessary seam or wall relation from
a complete domain of configurations.
Both need an explicit claim and acceptance rule before new target measurements.
The idea board retains the priorities and rejection reasons; the confirmation code is
available without launching a new optimization campaign.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
