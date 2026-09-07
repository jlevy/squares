# BC-277: A Closed Boundary-Band Compatibility Domain

**Proposed admission scope:** four independently oriented lower-band squares whose
actual-angle guard octagons form a fence attached to the bottom of the universal center
box. Eight finite inequalities define the selected family.
The accepted lower four-diamond fixture satisfies all eight strictly; it supplies a
four-pose membership control and a nontrivial continuous family, not an eleven-square
witness or evidence for a capacity bound.

The prospective question is whether every member of this family admits at most six
additional unrestricted full unit squares.
**That question is not attempted here.** There is no capacity or region-diameter
conclusion in the guard list.
This report prepares a domain and admission review under BC277 and existing H118,
following the [BC271 allocation assessment](bc-271-comparator-design-assessment.md).
A target requires its own separately committed prospective protocol and record checks.

## Parent, Four-Pose Domain and Eleven-Square Question

Fix $q=96/25$, $b=1/2$, $d=q-1/2=167/50$, and preserve the
[original complete band split](bc-270-capacity-comparison-design.md):

$$
B_0=[1/2,217/150],\quad B_1=[217/150,359/150],\quad
B_2=[359/150,167/50].
$$

Every contained unit-square center belongs to $[b,d]^2$. For counting, assign a seam to
its lower-index band.
Eleven assigned centers force four in at least one band.
Keep every four-label subset $I$ and every weak horizontal ordering $\pi$ of its four
slots. The closed parent $P_{j,I,\pi}$ puts those selected centers in $B_j$; it includes
all eleven unit squares, their actual independent orientations, containment and every
pair nonoverlap condition.
Band seams, ordering ties and cases with more than four centers in one band remain
covered by overlap.

Use the complete closed orientation chart $\theta_i\in[-\pi/4,\pi/4]$ modulo quarter
turns, retaining both endpoint lifts.
For each of the eleven squares, define

$$
e_i=(\cos\theta_i,\sin\theta_i),\quad
f_i=(-\sin\theta_i,\cos\theta_i),\quad
Q_i=\{\alpha e_i+\beta f_i:|\alpha|,|\beta|\le1/2\},
$$

$$
H_i(n)=\tfrac12(|n\cdot e_i|+|n\cdot f_i|),\qquad
h_i=H_i((1,0))=H_i((0,1)).
$$

Every square has its own angle parameter.
Impose all containment conditions $h_i\le C_{i,x},C_{i,y}\le q-h_i$ and, for each of the
55 pairs $i<j$, the complete weak disjunction

$$
\bigvee_{n\in\{e_i,f_i,e_j,f_j\},\ \sigma\in\{-1,1\}}
\sigma(C_j-C_i)\cdot n\ge H_i(n)+H_j(n).
$$

No separating direction comes from a source packing.
No anchor, wall contact, coincident angle, stationarity or contact graph is imposed.

Let $\Gamma_0$ denote the four-pose domain consisting of the selected four contained
unit squares, their six complete pair conditions, their lower-band membership and weak
horizontal order, plus the eight guards below.
It is a set of four poses, without any assertion about the other seven squares.
Let

$$
D_0=P_{0,I,\pi}\cap\{\text{the selected four poses belong to }\Gamma_0\}.
$$

The future question $D_0=\varnothing$ keeps every parameter of the seven other squares
unrestricted except for their actual containment and pair conditions.
It is equivalent to the absence of seven additional full squares for every
$G\in\Gamma_0$. The fixture belongs to $\Gamma_0$; its membership in $D_0$ is neither
asserted nor assumed.

## Eight Geometric Guards

Reuse only the universal core and section geometry accepted in the
[BC270 fence review](bc-270-parent-compatibility-review.md), not its central-band
capacity conclusion.
Put

$$
\mathcal D(m)=\{(X,Y):|X|+|Y|\le m\},\qquad
m_i=\frac1{2\max(|e_{i,x}|,|e_{i,y}|,|f_{i,x}|,|f_{i,y}|)}.
$$

For each actual selected square, $\mathcal D(m_i)\subseteq Q_i$, with
$1/2\le m_i\le1/\sqrt2$. The fixed closed octagon

$$
E=\{(X,Y):|X|,|Y|\le2/5,\quad |X|+|Y|\le699/1000\}
$$

lies strictly inside the radius-$1/2$ disk: its vertex squared norm is
$249401/1000000<1/4$. Thus $C_i+\mathcal D(m_i)+E$ is a closed subset of the strict
forbidden-center set supplied by the actual square $Q_i+C_i$ and a residual incircle.
This uses full-square containment of the cores; it is not a replacement of the target
squares by smaller shapes.

Write the four selected centers in horizontal order as $(x_i,y_i)$, $i=0,1,2,3$, and set

$$
\ell=(y_0+y_2)/2,\quad u=(y_1+y_3)/2,\quad
\varepsilon=\tfrac12\max(|y_0-y_2|,|y_1-y_3|),\quad
m=\min_i m_i,
$$

$$
k=299/1000,\quad A=m+2/5-\varepsilon,\quad R=A+k,\quad
\Delta=u-\ell.
$$

These are exact shared expressions in the four actual poses.
Neither $m$ nor $\varepsilon$ is a freely chosen favorable bound.
Independent angles and unequal row heights remain allowed.

The virtual guard octagon $K_i$ has center $(x_i,v_i)$, where $v_i=\ell$ for even $i$
and $v_i=u$ for odd $i$, and inequalities

$$
|X-x_i|\le A,\quad |Y-v_i|\le A,\quad
|X-x_i|+|Y-v_i|\le R.
$$

The accepted scatter-shrink calculation gives $K_i\subseteq C_i+\mathcal D(m_i)+E$.
Require exactly the following eight scalar expressions to be nonnegative:

| Guard expressions | Count | Geometric meaning |
| --- | --- | --- |
| $\Delta$; $A-k-\Delta$ | 2 | Order the virtual rows and put their overlap endpoints in the accepted section regime |
| $b-u+A$ | 1 | Attach both guard rows to the bottom edge $Y=b$ of the center box |
| $b+k-x_0$; $x_3-d+k$ | 2 | Reach the left and right endpoints of the horizontal center interval |
| $2k+\Delta-x_{i+1}+x_i$, for $i=0,1,2$ | 3 | Join consecutive alternating guard intervals in their row overlap |

The row ordering and separation guards give $A\ge k>0$. The parent already places both
row averages in $[b,d]$. The bottom-attachment guard therefore concerns the
forbidden-center fence, not a physical wall contact of any selected square.

These inequalities come from the reviewed section radius $r_v(Y)=\min(A,R-|Y-v|)$ on
$|Y-v|\le A$: at a row-overlap endpoint the two alternating radii are $k$ and
$k+\Delta$, and the common lower endpoint is $u-A$. They specify a geometric family
before any residual count is sought.
No bound on the number, area, diameter or packing capacity of the remaining cavities is
used to define it.

Unlike the central proof, this domain imposes no top-reaching condition $u+A\ge d$ and
no four-region diameter guards.
In fact every lower-band four-pose parent has

$$
u+A\le217/150+1/\sqrt2+2/5
<217/150+3/4+2/5=779/300<d.
$$

Thus the selected family is outside that central top-reaching premise for a proved
reason; removing that premise is not an appeal to the central capacity theorem.
No new residual-capacity deduction is made in this design.

## Exact Membership Control and Closed Siblings

Use the original lower fixture verbatim:

$$
x_i=18/25+4i/5,\quad
 y_0=y_2=18/25,\quad y_1=y_3=71/50,\quad
\theta_i=\pi/4.
$$

Its containment, band membership and all six pair separations are already accepted in
the original design.
In particular the smallest wall clearance is $18/25>1/\sqrt2$, and the smallest
diamond-center $L^1$ distances are $3/2$ and $8/5$, both greater than $\sqrt2$. These
are four-square controls only.

For $h=1/\sqrt2$, this fixture gives $m=h$, $\varepsilon=0$, $\ell=18/25$, $u=71/50$,
$\Delta=7/10$, $A=h+2/5$, and $R=h+699/1000$. The eight guard values are

$$
7/10,\quad h-599/1000,\quad h-13/25,\quad
79/1000,\quad79/1000,\quad249/500,\quad249/500,\quad249/500.
$$

They are all strictly positive; for example the retained exact enclosure
$7071/10000<h<7072/10000$ suffices.
Original containment, pair separation, band membership and horizontal order also have
strict margins.
Continuity of the actual-pose expressions gives a relative open family in
$\Gamma_0$, including independent inward angle perturbations and nonzero row scatter.
The complete closed family is defined by the eight guards, not by a prescribed
neighborhood or fitted pose box.

All parameter domains are bounded.
The angle chart, containment, SAT alternatives, band/order conditions and eight
continuous weak guards are closed.
Consequently $\Gamma_0$ and $D_0$ are compact.
No added guard is identically tight at the fixture.
There are no generated failure children for coordinates fixed by definition or for
parent-implied identities.

For each fixed lower parent, retain $D_0$ and, for every listed guard $g$, the closed
failure child

$$
P_{0,I,\pi}\cap\{g\le0\}.
$$

The children cover the parent: if a point fails the success conjunction, some guard is
strictly negative. A point of $D_0$ with $g=0$ also belongs to that failure child; an
equality point with another negative guard need not belong to $D_0$. The failure
children exclude the relative open four-pose family where all eight guards are positive,
but that family remains in the unproved success child.
Until a target is decided, no part of that child is pruned from the eleven-square cover.

Retain every subset and ordering.
Retain the central-band cover and its accepted
[24-guard correction](bc-270-parent-compatibility-design.md#closed-siblings-comparison-status-and-next-obligation)
unchanged. For the upper band use the jointly reflected success and failure children
specified next. This preserves the complete three-band parent cover and all its
unresolved branches.

## Joint Reflection for the Upper Band

Apply the same isometry to all eleven poses and the container:

$$
\mathcal R(X,Y)=(X,q-Y),\qquad
C_i'=(C_{i,x},q-C_{i,y}),\qquad \theta_i'=-\theta_i.
$$

The reflected square has canonical basis $e(-\theta_i),f(-\theta_i)$; reflection maps
$e_i$ to the first vector and $f_i$ to the negative of the second, which only permutes
the corner signs. Top and bottom walls exchange.
Every pair displacement and separating normal is reflected together, preserving each
weak SAT disjunction.
The angle chart’s two endpoint lifts exchange; neither is discarded.

One has $\mathcal R(B_0)=B_2$. Horizontal order and labels remain unchanged.
Define $\Gamma_2=\mathcal R(\Gamma_0)$ and $D_2=\mathcal R(D_0)$, reflecting all seven
residual poses in the latter definition.
To evaluate the upper guards directly, replace each selected ordinate by its inward
depth $q-y_i$ before computing $\ell,u,\Delta$ and $\varepsilon$. Equivalently, if the
raw upper row averages are $\ell_U,u_U$, use $\Delta=\ell_U-u_U$ and the attachment
expression $u_U+A-d$; the other guard formulas are unchanged.
The quantities $m$, $A$, $R$ and scatter are invariant under the joint reflection with
these depth coordinates.

The upper fixture is consequently $y_0'=y_2'=78/25$, $y_1'=y_3'=121/50$ with the same
abscissae and angles $-\pi/4$. It has the same eight guard values.
This is a reflected four-pose membership control, not seven additional squares.

Counting seam ownership stays with the lower-index band in the original coordinates.
Reflection need not preserve that counting assignment at a seam: it acts on the closed
branches, whose overlap retains both possible representatives.
Do not remove a reflected boundary because its canonical counting owner changed.
Reflecting only the four selected squares while holding the residual poses or walls
fixed would not justify any transfer of a future exclusion.

## Actual Cavity and Two Distinct Relaxations

For fixed $G\in\Gamma_0$ and an additional actual angle $\theta$, the contained-center
box is $B_\theta=[h_\theta,q-h_\theta]^2$. The actual square’s legal cavity is

$$
\mathcal A(G,\theta)=B_\theta\setminus
\bigcup_{i=0}^3\operatorname{int}(C_i+Q_i+Q_\theta).
$$

The summands are the actual closed unit squares.
Central symmetry makes this the correct Minkowski forbidden-center expression.
Removing only the interiors preserves legal square touching.
Seven additional squares require seven angle/center pairs from their respective cavities
and all 21 complete mutual SAT disjunctions.
Seven individually available cavities or seven individually legal centers do not
establish coexistence.

A weaker disk model keeps each center in $[b,d]^2$, requires its closed radius-$1/2$
disk to avoid the four actual square interiors, and imposes pair distances at least one.
Its center avoidance uses the interiors of $C_i+Q_i+B_{1/2}$, where $B_{1/2}$ is the
closed disk. Every full-square extension yields such a disk configuration.
The converse is not supplied by an inscribed disk.

A still weaker closed octagon model puts centers in

$$
[b,d]^2\setminus\bigcup_i\operatorname{int}K_i
$$

and again imposes pair distances at least one.
Actual feasible centers avoid even the closed $K_i$ because their inclusion in the disk
forbidden region is strict.
Allowing $K_i$ boundaries in this closed relaxation is an explicit weakening; a
surviving point on such a boundary is not an actual-square witness.

If $\kappa_\square$, $\kappa_{\rm disk}$ and $\kappa_{\rm oct}$ denote the maximum
additional counts in these respective models, the sound implication is

$$
\kappa_\square(G)\le\kappa_{\rm disk}(G)\le\kappa_{\rm oct}(G).
$$

No value of any of these capacities is established here.
A uniform upper bound of six in either weaker model would suffice for the full-square
question, after independent verification.
Seven disk or octagon centers would only obstruct that sufficient model; they would not
refute the full-square exclusion.
These are prospective interpretations, not outcomes of a target attempt.

## Admission Controls and Prospective Acceptance

| Control or future receipt | What acceptance or refusal establishes |
| --- | --- |
| Original lower four-diamond fixture | Accept exact membership in $\Gamma_0$ and its strict guard margins. It establishes neither a seven-square extension nor a capacity of six. |
| Jointly reflected fixture and guard list | Accept $\Gamma_2$ membership and the complete isometry/lift map. A partial reflection must be refused as a domain-transfer argument. |
| Actual-angle core and unequal-row source-free controls | Check the already accepted octagon inclusion and that scatter is spent from both required bounds. A free favorable $m$ or understated scatter must be refused. This checks a necessary relaxation, not target capacity. |
| Two axis unit squares touching along an edge | Accept their complete weak nonoverlap. Refuse an alleged exclusion that replaces an actual forbidden interior by the entire closed polygon and counts that contact as overlap. |
| Omitted guard/failure sibling, dropped angle endpoint or altered label/order map | Refuse a claim of complete domain identity or parent coverage. No target conclusion follows from an incomplete cover. |
| Exact seven-center disk or octagon configuration, if later supplied | Check only its declared relaxation. It obstructs exclusion by that weaker model; it is not seven full squares. No such configuration is sought in this design. |
| Exact seven additional full unit squares, if later supplied | Check all eleven poses, actual angles, source guards, containment and all 55 pair conditions. This refutes the proposed exclusion of $D_0$. No such witness is supplied here. |
| A complete uniform upper-capacity argument, if later supplied | Check all $G\in\Gamma_0$, all residual orientations, legal boundaries and every necessary mutual constraint. Only an independently accepted bound of at most six excludes the full eleven-square child. |

A future determination must accept either a uniform exclusion of the entire unchanged
$D_0$ or one rigorously verified eleven-square packing in it.
A strict-subdomain proof, failed construction, surrogate witness, unresolved case or
exhausted cap leaves that full determination open.
A proof for an arbitrary fixed four-pose source is not uniform in $\Gamma_0$. The
reflected conclusion requires the complete reflection contract.

Such a direct exclusion would add a previously uncovered parent child.
It would not establish strict H118 strength without a separately frozen matching
coupled-LP comparator and an exact surviving relaxation point.
No central comparator adapter, capacity search, or proof of an unrestricted packing
bound is admitted here.

## Price, Admission Boundary and Work Receipt

Reserve the already planned 15-minute independent admission review after this report
freezes. Its deliverable is acceptance of the exact domain, finite guard meanings,
fixture membership, closed siblings, actual-square/relaxation distinction and joint
reflection, or a precise blocker.
It must not use a capacity-six assertion to admit the guards.

If that review accepts the scope and the coordinator commits a separate prospective
protocol with passing records, a reasonable first analytical attempt is 30 minutes for
one author and 20 minutes for an independent adversary, concurrently, followed by a
20-minute independent audit after both freeze.
This prices at most 70 worker-minutes and a 50-minute mathematical critical path,
excluding protocol and integration work.
These are caps, not measured completion probabilities.
All questions and accepted outcomes remain at the frozen full-square scope; no automatic
solver switch, domain narrowing or retry is included.
Any instrument or computational run needs its own source-free controls, review and
separately priced authorization.

This design starts no target, and the full-square complement-capacity question remains
open. The eight-guard domain and its membership control are the proposed readiness
output; independent admission and a committed target protocol are still required.

The phase-10 lease is 09:43:03–10:13:03 UTC on 2026-09-07. This worker’s first recorded
clock read was 09:43:37 UTC. The comparator assessment, accepted original band fixtures,
and accepted central fence geometry and correction were read.
Native writing waited for the coordinator’s confirmation that checkpoint 57b85302 was
committed. Only this assigned report was written.
No new capacity target was attempted, tested or solved; no numerical, solver,
resource-search, instrument, Git, shared-record, identifier or dependency work occurred.
The design and complete readback ended at 09:53:09 UTC, 9 minutes 32 seconds after the
first clock read and 10 minutes 6 seconds after the phase lease began.
The document received the common-document and prose-editing passes.
Installed Flowmark 0.4.0 formatted this file and passed its check with caching disabled;
all four linked files and the cited correction section exist, the whitespace check
passed, and the required footer appears once.
A final scoped formatting check follows this receipt.
Independent admission review, rather than these document checks, determines whether the
proposed domain is ready for a separately authorized target.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
