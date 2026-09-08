# BC-277: Independent Boundary-Band Admission Review

**Accepted for admission:** the unchanged eight-guard family in the
[frozen design](bc-277-boundary-band-domain-design.md) is a precisely specified, compact
four-pose domain with a strict exact membership control.
Its success and failure children preserve the full eleven-square parent cover, and its
upper-band counterpart is justified by joint reflection.
The actual-square, disk and octagon models have the stated relaxation directions.

This accepts a question for a separately authorized attempt.
It establishes no residual capacity, no eleven-square packing, and no exclusion of the
success child. No desired capacity or diameter bound was used in this admission.
One sentence about failure-child equality needs the qualification below; the formal
domain and cover definitions require no change.

## Exact Parent and Guard Inventory

With $q=96/25$, every contained unit-square center lies in $[b,d]^2$, where $b=1/2$ and
$d=167/50$. The actual coordinate support is
$h_i=(|\cos\theta_i|+|\sin\theta_i|)/2\ge1/2$, so the larger universal center box is
necessary.
The design retains the stronger actual containment inequalities for all eleven
squares.

The three closed bands have endpoints $1/2,217/150,359/150,167/50$. Assigning each seam
to its lower-index band is a counting convention: eleven assigned centers force four in
one band. Every four-label subset and every weak horizontal ordering is retained in the
closed parents. Ties, seams and additional centers in the selected band therefore remain
covered.

For each of the 55 unordered pairs, the design retains all four edge-axis normals and
both signs. For squares these are the complete separating-axis alternatives.
The support inequality is weak, preserving legal touching.
The actual angle chart $[-\pi/4,\pi/4]$ covers orientations modulo quarter turns; its
two equivalent endpoint lifts are both retained.
These statements justify the full parent, without a source-derived contact graph or a
restricted separating direction.
The 55 pair conditions divide into six selected-pair, 28 selected-to-residual and 21
residual-pair conditions.

The selected-pose quantities $m,\ell,u,\varepsilon,A,R,\Delta$ are the exact expressions
in the design. In particular $m=\min_i m_i$ and the scatter $\varepsilon$ are determined
by the poses. They are not existentially chosen bounds.
The complete added guard list is

$$
\Delta,\quad A-k-\Delta,\quad b-u+A,\quad
b+k-x_0,\quad x_3-d+k,\quad
2k+\Delta-x_{i+1}+x_i\quad(i=0,1,2),
$$

with $k=299/1000$, and each expression is required to be nonnegative.
This is exactly eight guards.
None states a cavity capacity, area or diameter conclusion.

I independently checked the geometry supporting these guards.
For the actual square basis, the support of the axis diamond $\mathcal D(m_i)$ along
either square normal is at most $m_i\max(|e_{i,x}|,|e_{i,y}|)=1/2$. Hence the diamond
lies in the actual unit square, and $1/2\le m_i\le1/\sqrt2$. The fixed octagon $E$ has
vertices given by signs and coordinate permutations of $(2/5,299/1000)$. Their squared
norm is $249401/1000000<1/4$, proving strict inclusion in the open incircle.

The Minkowski sum $\mathcal D(m_i)+E$ is exactly the octagon with coordinate bounds
$m_i+2/5$ and $L^1$ bound $m_i+699/1000$. The measured vertical displacement of each
virtual center is at most $\varepsilon$. Thus a point in $K_i$ satisfies the
actual-center coordinate bounds using $A+\varepsilon=m+2/5\le m_i+2/5$, and the diagonal
bound using $R+\varepsilon=m+699/1000\le m_i+699/1000$. This proves the stated shrink
inclusion. Because $E$ lies strictly inside the disk, even the closed $K_i$ lies in the
interior of the actual square-plus-incircle forbidden set.

The first two guards imply $0\le\Delta\le A-k$, so $A\ge k>0$. The lower parent puts
both row means at least $b$. The attachment guard gives $u-A\le b$; therefore $b$
belongs to the common row interval $[u-A,\ell+A]$. At either endpoint of that overlap,
the alternating section radii are $k$ and $k+\Delta$. Their sum is concave in height and
consequently at least $2k+\Delta$ throughout the overlap.
The three gap guards join consecutive intervals, and the endpoint guards reach both
horizontal sides of the center box.
This verifies the advertised bottom attachment and section meanings, without drawing a
conclusion about the remaining capacity.

The absent top-reaching premise cannot be imported from the central theorem:

$$
u+A\le217/150+1/\sqrt2+2/5
<779/300<167/50=d.
$$

This follows already from lower-band membership and $\varepsilon\ge0$. The new family
has not inherited the central four-region diameter conclusion.

## Membership, Compactness and Closed Coverage

At the proposed lower fixture, $x_i=18/25+4i/5$, the even heights are $18/25$, the odd
heights are $71/50$, and all four angles are $\pi/4$. Write $h=1/\sqrt2$. Direct
substitution gives the eight values

$$
7/10,\quad h-599/1000,\quad h-13/25,\quad
79/1000,\quad79/1000,\quad249/500,\quad249/500,\quad249/500.
$$

They are strictly positive.
The exact enclosure $7071/10000<h<7072/10000$ follows by squaring the positive rational
endpoints. The minimum wall clearance is $18/25>h$. For equal diamond orientations the
pair condition is an $L^1$ center distance of at least $\sqrt2$; the six distances are
three copies of $3/2$, two copies of $8/5$, and $31/10$. Every one is strictly larger.
The selected heights are strictly inside the lower band, with upper margin
$217/150-71/50=2/75$, and all horizontal gaps equal $4/5$.

These strict inequalities and continuity give a nontrivial family of four actual poses.
The angle endpoints permit independent inward angle changes; small unequal height
changes produce nonzero scatter.
Minima, maxima and absolute values in the guard expressions remain continuous at the
fixture’s ties. No fixed-angle or coincident-row equation is needed for this argument.

Bounded center coordinates and the closed angle chart give a compact parameter box.
Containment, band membership, weak order, finite unions of closed SAT alternatives and
the continuous weak guards are closed subsets.
Consequently $\Gamma_0$ is compact, and so is the corresponding full eleven-pose child
$D_0$. The strict fixture proves that $\Gamma_0$ has a nontrivial four-pose family.
It does not prove that $D_0$ is nonempty: seven simultaneous additional squares are
still the question.

For each lower parent, success means all eight guards are nonnegative.
Outside success at least one guard is strictly negative, so the eight closed failure
children $P_{0,I,\pi}\cap\{g\le0\}$ cover every remaining parent point.
Every listed guard is strictly positive at the fixture; none is an identity of the
four-pose parameterization.
This does not assert that all failure children are distinct, nonempty or proper subsets
of the full eleven-square parent.
Establishing that a strictly guarded four-pose fixture extends to that full parent
remains part of the unanswered target question.

**Wording qualification:** the design’s sentence “Equality belongs to both children”
applies to $D_0\cap\{g=0\}$. If another guard is negative, a point with $g=0$ belongs to
the corresponding failure child but need not belong to success.
The formal definitions already give the correct closed cover.
No boundary needs to be removed or reassigned.

The central remainder is explicitly preserved with its current
[24-guard correction](bc-270-parent-compatibility-design.md#closed-siblings-comparison-status-and-next-obligation).
That inventory has nine fence, three bottom-middle, three top-middle, two top-left,
three bottom-right and four diameter guards; its failure children remain present.
The lower and reflected upper branches do not replace these unresolved central children.
No success child is pruned by this admission, and the retained band, label and ordering
inventory still covers every full parent packing.

## Upper Reflection and the Counting Seam

The map $\mathcal R(X,Y)=(X,q-Y)$ must act on all eleven poses.
Its linear part sends $e(\theta)$ to $e(-\theta)$ and $f(\theta)$ to $-f(-\theta)$,
which merely changes one corner sign.
Reflecting each displacement and normal preserves the full weak SAT alternatives.
The square container is invariant, with its top and bottom walls exchanged.
The angle endpoint lifts exchange and remain represented.

Since $q-217/150=359/150$, reflection maps the closed lower band exactly to the closed
upper band and preserves horizontal order and labels.
The upper definition uses inward depths $q-y_i$, so $m$, scatter, $A$ and $R$ are
unchanged. In raw upper means, the lower $\Delta$ becomes $\ell_U-u_U$ and the lower
attachment guard becomes $u_U+A-d$. The stated upper fixture heights $78/25$ and
$121/50$ and angles $-\pi/4$ therefore reproduce the same eight strict guard values.

The seam caveat is necessary and correctly retained.
A lower point at $217/150$, canonically counted in band zero, reflects to $359/150$,
canonically counted in band one.
It nevertheless belongs to the closed band-two parent.
Reflection transfers closed branches, not the auxiliary counting assignment.
Discarding that reflected seam would break the transfer.
Reflecting only the selected four poses would likewise fail to preserve their cross-pair
conditions with the other seven.

## Three Models and Admissible Outcomes

For a fixed four-pose member $G$ and an actual residual orientation $\theta$, the stated
cavity

$$
[h_\theta,q-h_\theta]^2\setminus
\bigcup_i\operatorname{int}(C_i+Q_i+Q_\theta)
$$

is the correct contained-center set.
Central symmetry accounts for the absence of a minus sign in the Minkowski sum.
Removing interiors preserves touching.
Seven centers in their individual cavities still require all 21 mutual full-square SAT
conditions.

Each full unit square contains its radius-$1/2$ disk.
Consequently every actual extension yields centers in $[b,d]^2$ whose disks avoid the
selected actual square interiors and whose mutual distances are at least one.
Those disk centers avoid the interiors of $C_i+Q_i+B_{1/2}$. Since the closed $K_i$ lies
strictly inside that forbidden set, every disk-legal center lies outside the closed
$K_i$, and hence also satisfies the weaker octagon model, which removes only
$\operatorname{int}K_i$. The directions are therefore

$$
\kappa_\square(G)\le\kappa_{\rm disk}(G)\le\kappa_{\rm oct}(G).
$$

Allowing an octagon boundary point is a deliberate relaxation, not an actual square
contact certificate.
A seven-center disk or octagon control can refute a proposed bound of six in its
declared model at that $G$. It does not construct seven full squares, an eleven-square
packing, or a refutation of the full-square capacity question.
A seven-center octagon control need not even satisfy the disk model.

The exact admissible target is whether the unchanged $D_0$ is empty, equivalently
whether every $G\in\Gamma_0$ admits at most six additional unrestricted actual unit
squares. The following are sufficient future outcomes or controls:

- A uniform full-square upper bound of six, or a uniform bound of six in either stated
  relaxation, suffices for exclusion once independently verified on the entire closed
  domain. A proof at one fixture or on a strict subdomain does not.
- An exact eleven-square packing in $D_0$, checked against the eight source guards,
  actual containment, all actual angles and all 55 complete pair conditions, refutes
  exclusion. No such packing is supplied here.
- The strict four-pose fixtures test membership only.
  Actual-angle and unequal-row controls must reject a freely enlarged core or
  understated scatter.
  A touching two-square control must retain weak SAT and actual forbidden interiors.
- Omitted alternatives, dropped angle or band endpoints, lost failure siblings, changed
  label/order maps and partial reflection must fail claims of complete domain identity.
  Surrogate witnesses must be checked only in their declared models.

A failed construction, unresolved case, exhausted lease or surrogate witness leaves the
full-square target open.
The joint reflection transfers a subsequently accepted whole-domain result to $D_2$; it
supplies no result now.
The [BC271 comparator assessment](bc-271-comparator-design-assessment.md) also remains
applicable: strict H118 strength would require a separately specified matching
coupled-LP comparator representing the nonlinear guards and an exact surviving point.
Admission supplies neither.
The rest of the global packing cover remains unresolved as recorded.

## Work Receipt and Next Action

The prospective session-092 phase-11 lease was 09:55:44–10:10:44 UTC on 2026-09-07. This
review’s first clock read was 09:56:23 UTC. I read the complete frozen BC277 design, the
current central correction and the BC271 assessment, using the previously reviewed
original band fixtures and accepted core geometry.
The mathematical checks above were reconstructed by hand.
No capacity target, seven-center construction, numerical script, solver or resource
search was attempted.
Only this assigned review was written; no source report, Git state, shared record,
identifier or dependency was changed.

The mathematical audit and full readback ended by 10:06:54 UTC, 10 minutes 31 seconds
after the first clock read.
The document received the common-document and prose-editing passes.
Installed Flowmark 0.4.0 formatted this file and passed its check with caching disabled;
all three linked files and the cited correction section exist, the whitespace check
passed, and the required footer appears once.
These checks completed at 10:07:12 UTC, an elapsed 10 minutes 49 seconds.
A final scoped formatting check follows this receipt; all work remains within the
10:10:44 UTC hard deadline.

The next action is for the coordinator to record this admission, qualify the equality
wording when appropriate, and commit a separate prospective target protocol with passing
record checks before dispatching target work.
The proposed 30-minute author, 20-minute concurrent adversary and 20-minute subsequent
audit are future caps: at most 70 worker-minutes and a 50-minute mathematical critical
path, excluding integration.
This review does not launch those phases.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
