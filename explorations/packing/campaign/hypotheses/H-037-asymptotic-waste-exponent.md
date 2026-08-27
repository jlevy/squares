---
title: H-037 — what is the asymptotic waste exponent?
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-037
  kind: open_question
  claim: >-
    Can the gap between W(x) not in o(x^(1/2)) and W(x) = O(x^(3/5)) be narrowed, and
    which synchronization or geometric obstruction determines the true exponent?
  lane: proof
  derived_from: [X-002]
  strategy_refs: ['search:9', 'proof:12', 'proof:13', 'proof:14']
  instrument: >-
    Reproduce the current lower-bound and construction error balances; use symbolic
    parameter searches to falsify proposed balances, and finite constructor experiments
    only as diagnostics for boundary overhead and synchronization.
  instrument_ready: false
  regime: x tending to infinity, with fractional part and inclination conditions explicit
  instance: {axis: asymptotic-scale, point: x-to-infinity}
  priority: 3
  cost_estimate: parallel paper-mathematics lane; finite diagnostics tier S per parameter family
  prereqs: []
  replication: true
  registered: '2026-08-24'
  notes: >-
    Bui's good-square reduction and the 2025-2026 O(x^(3/5)) constructions are the
    current primary starting points. No finite-n search result determines this question.
---
# H-037 — keep the global frontier visible

This open question prevents the campaign’s common-`n` tooling from becoming the whole
definition of square-packing research.
Its intermediate artifacts are checked derivations and finite synchronization
experiments, not overnight basin counts.

## Reproduced source balance

Bui’s Proposition 7 states the following reduction.
For $\frac{1}{2}<\beta<1$, real $\epsilon$, and $0<\nu<\beta+\frac{1}{2}$, suppose right
trapezoids of height $m$, bases $w$ and $w+\Theta(\sqrt m)$, and $w\in\Theta(m^\nu)$ can
be packed with waste $O(m^\beta(\log m)^\epsilon)$. The stated square-packing reduction
has total waste

$$ O\!\left(m^\beta(\log m)^\epsilon+\frac{x}{\sqrt m}\right).
$$

Balancing the two displayed terms gives

$$ m=\left(x(\log x)^{-\epsilon}\right)^{2/(2\beta+1)} $$

and hence

$$ W(x)=O\!\left( x^{2\beta/(2\beta+1)}(\log x)^{\epsilon/(2\beta+1)} \right).
$$

For the Section 4 primitive, $\beta=\nu=3/4$ and $\epsilon=0$. Thus $m=x^{4/5}$, and
both $m^{3/4}$ and $x/\sqrt m$ equal $x^{3/5}$. This is an algebraic reproduction of the
balance printed in
[Bui, Section 5](../../resources/papers/square-packing-x06-wasted-area-2508.04603.pdf),
not an independent proof of the reduction.
The archived cleaned transcription now flags two extraction errors in this proposition:
it had omitted the condition on $\nu$ and had changed $x/\sqrt m$ into $x\sqrt m$.

## Exact transfer boundary

The first blocker for H-035 is external to this asymptotic balance: the repository has
no independently verified public-parent frontier above $n=100$, while H-035 requires a
preregistered parent in $100\leq n\leq324$. Even after that corpus exists, neither the
displayed proposition nor the surrounding source passage supplies effective hidden
constants, a finite threshold $x_0$, integer synchronization rules, an exact square
count, or complete boundary and rounding accounting for the residual stacks.
Those are the missing finite-constructor obligations; the $x^{3/5}$ exponent alone does
not discharge them.

## Local repair of McClenagan’s sign step

McClenagan’s Section 3 proof of $\theta'\leq\theta$ prints $d_1+d_2>d$ and then
$d>d_1+d_2>DB=1$ in the same paragraph.
The contradiction is present in the
[archived PDF](../../resources/papers/mcclenagan-2026-optimally-packing-large-square.pdf),
not introduced by extraction.
Figures 4 and 6 and equations (2.1), (2.2), (2.5), and (3.2) nevertheless give two
independent local repairs.

For the diagrammatic repair, let $D(a)$ be the Figure 6 clearance when the horizontal
stacks have inclination $a$. Resolving the horizontal displacements gives

$$ D(a)=\cos a-\sin a+\sin a+\cos a\tan\theta=(1+\tan\theta)\cos a. $$

Thus $d=D(\psi)>D(\varphi)=d_1+d_2$ because $0<\psi<\varphi<\pi/2$. Moreover,

$$ d_1=\cos\varphi-\sin\varphi>DC, \qquad
d_2=\frac{\sin(\varphi+\theta)}{\cos\theta}>CB, $$

where the first inequality follows from (2.1)--(2.2), and the second uses
$CB=DB-DC=\sin(\varphi+\theta)$. The intended chain is therefore

$$ d>d_1+d_2>DC+CB=DB=1. $$

The equation-only check does not use Figure 6. Substituting (2.2) into (2.5) gives
$\tan(\psi+\theta)=\tan\varphi$, hence $\psi+\theta=\varphi$ on the acute geometric
branch. Put $p=\tan\varphi$ and $t=\tan(\psi/2)$. Equation (2.2) then gives

$$ t=\frac{p(1-p)}{2-p+p^2}. $$

On the principal branch dictated by Figure 5, equation (3.2) becomes

$$ \tan(\psi+\theta')=\frac{2t}{1-t} =\frac{p(1-p)}{1-p+p^2}. $$

For $0<p<1$, this quantity is strictly between $\tan\psi$ and $p$, with

$$ \tan(\psi+\theta')-\tan\psi=\sec\psi-1>0, \qquad
p-\tan(\psi+\theta')=\frac{p^3}{1-p+p^2}>0. $$

Monotonicity of tangent on the acute branch proves $0<\theta'<\theta$. The mean value
theorem and $\sec^2 a\geq1$ give $0<\theta-\theta'\leq
p-\tan(\psi+\theta')=O(p^3)=O(\varphi^3)$. The paper’s unqualified phrase “unique
solution” is not globally true because tangent is periodic; uniqueness here means the
principal acute solution fixed by the geometry.

This repairs only the contradictory feasibility/sign step.
It is not an independent audit of the full construction and does not discharge H-035’s
finite-transfer obligations.

## Exact count in Bui’s replacement grid

Bui Section 3.1 starts with `m` columns of sloped squares and defines

$$ i_j=\left\lceil (j-1)c\right\rceil+1, \qquad c=\frac{1-\Delta_1}{\Delta_2}>0. $$

The modification paragraph says “for each $j\geq2$,” but the construction has only
columns $1,\ldots,m$. The later range $3\leq j\leq m$, the row
$T_{i_m,1},\ldots,T_{i_m,m-1},S_{i_m,m}$, and the named deletion of $S_{i_m,m}$ fix the
intended finite range as $2\leq j\leq m$. Reading the phrase as unbounded would refer to
nonexistent columns and eventually remove the square the source says remains.

For a column $k<m$, put $j=k+1$. The modification removes $S_{r,k}$ at every $r\geq
i_{k+1}$ and inserts $T_{r,k}$ with precisely the same row labels.
After rows above $i_m$ are deleted, the retained labels in column $k$ are therefore

$$ S_{r,k}\quad(1\leq r<i_{k+1}), \qquad T_{r,k}\quad(i_{k+1}\leq r\leq i_m). $$

These disjoint integer intervals partition $1,\ldots,i_m$ because $c>0$ makes the
sequence $i_j$ nondecreasing.
Coincident thresholds affect different columns and create neither a gap nor a duplicate.
Column $m$ is not replaced and retains $S_{1,m},\ldots,S_{i_m,m}$. Thus there is exactly
one labelled square in every cell of the $i_m\times m$ index grid: $m i_m$ squares
before the final deletion and $m i_m-1$ afterward.

The case-local exact replay in `cases/asymptotic/bui_integer_count.py` checks the same
partition for rational $c$, refuses the unbounded-range reading, and preserves the
source’s named final square.
This is only an integer-index and exact-count result for the stated primitive.
It does not prove that the labelled squares exist geometrically, do not overlap, lie in
the quadrilateral, achieve the waste estimate, transfer to a finite public parent, or
establish Proposition 7 or the asymptotic exponent.

## Exact local inequalities in Bui’s Proposition 6

Bui Section 4.2 leaves Lemmas 3-5 to interval arithmetic and differentiation.
They instead admit a short exact proof on the printed domains.
For $0<z<1/8$, the elementary bound $\cos z>1-z^2/2$ gives

$$ \cos z>\frac{127}{128}>\frac{100}{101}, \qquad
\frac{127}{128}-\frac{100}{101}=\frac{27}{12928}>0. $$

Also $\cos z<1$, so $1<\sec z<101/100$, proving Lemma 3.

For Lemma 4 put $c=\cos\theta$. On $0<\theta<1/8$ we have $0<c<1$, so cancelling the
strictly positive factor $(1-c)^2$ is valid.
The claimed inequality becomes

$$ 4c^3<(1+c)^2, $$

and its exact difference factors as

$$ (1+c)^2-4c^3=(1-c)(4c^2+3c+1)>0. $$

For Lemma 5, cancelling the positive factor $1-c$ reduces the claim to

$$ c^2>\frac{49}{100}(1+c). $$

The difference is increasing once $c>49/200$. Since $c>127/128$, its value is bounded
below by

$$ \left(\frac{127}{128}\right)^2 -\frac{49}{100}\left(1+\frac{127}{128}\right)
=\frac{677}{81920}>0. $$

The exact rational replay in `cases/asymptotic/bui_local_inequalities.py` retains both
margins, both cleared-denominator identities, and typed failures for strengthened
constants or domains.
This packet proves only the three local inequalities.
It does not audit the Lemma 6 induction, Proposition 6’s geometry and recurrence,
Proposition 7, an effective threshold, finite transfer, or the exponent.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
