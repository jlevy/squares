# BC264: Kernel Bound and Feature-Class Acceptance

The kernel implication needed by BC260 is sound.
A real symmetric kernel whose constant-one subtraction is positive semidefinite, whose
diagonal is at most $b$, and whose values on every compatible pair are nonpositive
bounds packing cardinality by $b$. The compatible-pair condition includes touching.

There is also an exact obstruction to a proposed small feature class: if every feature
is a polynomial of total center degree at most three when orientation is fixed at zero,
the kernel conditions are impossible in any square container of side $L\ge3$, for every
$b$. A contained $3\times3$ grid gives the contradiction.
This rules out that class, including its joint $D_4$ averages; it does not resolve
[H114](../../../../hypotheses/H-114-two-pose-kernel-exclusion.md) for richer features.

This is the independent source-free first pass under `think-b271`, within Session097’s
BC264 allocation.
The first observed clock was 2026-09-07 20:57:37 UTC; the hard deadline
is 21:18 UTC. No target, numerical optimization, sampling, scientific constructor, or
test was run. The parallel feature-author report was not inspected.
The coordinator supplied the proposed grid stencil during this review; its proof is
checked below, independently of any implementation.

## The Exact Bound

Let $L\ge1$ and $C_L=[0,L]^2$. A pose $p=(z,\theta)$ represents the closed unit square

$$
S_p=z+[-1/2,1/2]e_\theta+[-1/2,1/2]f_\theta,
\qquad
e_\theta=(\cos\theta,\sin\theta),\quad
f_\theta=(-\sin\theta,\cos\theta).
$$

Orientations are taken modulo $\pi/2$, since a quarter-turn about its own center does
not change a square.
Let $P_L$ contain all poses satisfying $S_p\subseteq C_L$. Equivalently, each center
coordinate lies in $[h_\theta,L-h_\theta]$, where
$h_\theta=(|\cos\theta|+|\sin\theta|)/2$. All orientation and wall boundaries belong to
the domain. Two poses are **compatible** when their square interiors are disjoint.
Their closed squares may share an edge or a point.
Identical physical squares are not compatible, even if represented by different labels.

Write $A(p,q)=K(p,q)-1$. Here the subtracted one is the constant kernel, not an identity
matrix. **Positive semidefinite (PSD)** means that for every finite list
$p_1,\ldots,p_m\in P_L$ and every real vector $a$,

$$
\sum_{i,j}a_i a_j A(p_i,p_j)\ge0.
$$

Suppose $K$ is real and symmetric, $A$ is PSD, $K(p,p)\le b$ for every pose, and
$K(p,q)\le0$ for every distinct compatible pair.
For a packing of $N>0$ squares, apply PSD to the all-ones vector:

$$
N^2\le \sum_{i,j=1}^N K(p_i,p_j)
\le \sum_{i=1}^N K(p_i,p_i)\le Nb.
$$

Thus $N\le b$, or $N\le\lfloor b\rfloor$ when a numerical integer bound is wanted.
For an empty packing the assertion is immediate when $P_L$ is nonempty, since PSD forces
$b\ge1$. More generally, $K-a$ PSD for a fixed $a>0$ gives $N\le b/a$. Checking $K$ PSD,
or using $a=0$, does not supply the $N^2$ term.

Consequently an exact $b<11$ certificate on all of $P_{96/25}$ excludes eleven squares
at that side and every smaller side.
It does not prove the exact Trump endpoint.
At the Trump side $U$, the accepted eleven-square packing forces $b\ge11$ for every
valid certificate; $b=11$ excludes twelve but permits eleven.
A proof at one side cannot be transferred to another by rescaling the unit squares.

This independently establishes the elementary implication in the archived
[Proposition E](../../../../../resources/papers/n11-complete-research-bundle-2026-09-07/original_review/n11_research_review.md#proposition-e-a-kernel-certificate).
It does not adopt a hierarchy-convergence theorem or assert existence of a useful finite
feature family.

## What a Complete Certificate Must Bind

A finite feature construction

$$
K(p,q)=1+\phi(p)^TQ\phi(q),\qquad Q=Q^T\succeq0,
$$

proves the PSD condition for every pose, because the resulting quadratic form is
$(\sum_i a_i\phi(p_i))^TQ(\sum_i a_i\phi(p_i))$. The feature definitions, their order,
the exact coefficients, the field and real embedding, the container side, and the
orientation convention must be fixed.
A sampled pose Gram matrix being PSD proves only that finite restriction.
A positive numerical eigenvalue tolerance is not an exact PSD certificate.

Acceptable finite PSD evidence includes an exact identity $Q=R^TDR$ with every diagonal
entry of $D$ proved nonnegative in the declared real field.
An exact pivoted $LDL^T$ certificate is another form of this identity; a zero pivot must
be handled without silently dropping a nonzero residual row.
Checking only the diagonal, determinant, or nonnegative leading principal minors is
insufficient. If redundant features admit an indefinite coefficient matrix for an
otherwise PSD kernel, that requires a separately proved quotient representation; it does
not excuse an indefinite $Q$ in this declared ansatz.

The remaining geometric obligations are independent of PSD:

- **Diagonal:** prove $b-K(p,p)\ge0$ over the whole three-dimensional pose domain.
  Centers, walls, all orientations, and the identified angle seam must be covered.
- **Pairs:** prove $-K(p,q)\ge0$ over the whole six-dimensional compatible-pair domain.
  No overlap pair needs the sign condition, but every compatible pair does.
- **Normalization and margin:** bind the constant term exactly and prove the strict
  comparison $b<11$. A floating candidate with an unresolved sign or PSD condition
  remains a candidate.

The separating-axis theorem gives a finite, closed pair-domain decomposition.
A pair is compatible exactly when one of the eight signed axes
$\pm e_\theta,\pm f_\theta,\pm e_\psi,\pm f_\psi$ weakly separates its squares.
For a selected axis $n$, one branch is the collection of all sixteen inequalities
$n\cdot(v_q-v_p)\ge0$, one for each pair of vertices.
These branches may overlap; their union must cover the whole compatible domain.
Equality is legal separation, so edge contact and point contact cannot be discarded as
measure-zero events.

Rational angle charts can make these obligations polynomial after multiplying by proved
positive denominators.
Any absolute-value or sign split needs its own complete closed partition.
An exact sum-of-squares identity with nonnegative domain multipliers, or a complete
closed-domain subdivision with exact sign certificates, can be sufficient.
For example, on a branch $g_i\ge0$, $h_j=0$, verify the coefficient identity
$-K=\sigma_0+\sum_i\sigma_i g_i+\sum_j\tau_jh_j$, with each $\sigma_i$ certified as a
sum of polynomial squares and the equality multipliers $\tau_j$ unrestricted.
The analogous identity for the diagonal uses $b-K(p,p)$. Failure of a chosen sufficient
certificate is unresolved, not a geometric counterexample.
Samples, incomplete subdivisions, timeouts and omitted boundary strata cannot establish
either universal inequality.

## Symmetry and Feature Information

The valid container-symmetry average is

$$
\bar K(p,q)=\frac18\sum_{g\in D_4}K(gp,gq).
$$

For each $g$, the PSD test is the original test on $gp_1,\ldots,gp_m$; averaging
preserves PSD. The same $g$ preserves containment and compatibility, so the diagonal and
pair inequalities survive.
Exchanging $p$ and $q$ is also valid for a symmetric kernel.
Intrinsic orientation changes by $\pi/2$ identify the same physical square.
These facts do not permit independently reflecting or rotating the two physical poses
into separate preferred regions.

Independently averaging the features, then forming their Gram kernel, need not preserve
the pair condition. If $\phi(p)=\phi(q)$ for compatible poses, then
$K(p,q)=1+\phi(p)^TQ\phi(p)\ge1$, an immediate contradiction.
In particular, features depending only on orientation fail whenever two squares of that
orientation fit. Features individually invariant under all container symmetries also
fail: for $L\ge2$, the axis-aligned unit squares in opposite corners are compatible and
related by a container half-turn.
Joint averaging retains nontrivial representation components; replacing each feature by
an invariant function can erase them.

A more general obstruction is an exact mixed-sign feature dependence on a finite
compatible family.
Let $\Phi$ have feature vectors as rows, $A=\Phi Q\Phi^T$, and suppose
$\Phi^Tc=0$ with both positive and negative entries in $c$. Set $u_i=\max(c_i,0)$ and
$v_i=\max(-c_i,0)$. Then $Au=Av$, while

$$
0\le u^TAu=u^TAv
\le-\Bigl(\sum_i u_i\Bigr)\Bigl(\sum_j v_j\Bigr)<0.
$$

The last inequality uses disjoint supports and $A_{ij}=K_{ij}-1\le-1$ for every cross
pair. This proof needs no diagonal bound.
It also applies directly to any finite PSD kernel restriction for which $Ac=0$ has been
proved, without assuming a particular matrix representation.

## The Cubic Center-Feature Obstruction

For $L\ge3$, take nine axis-aligned unit squares with centers

$$
z_{ij}=(L/2+i,L/2+j),\qquad i,j\in\{-1,0,1\}.
$$

Their coordinates stay at least $1/2$ from the container walls.
Distinct members are compatible: in at least one coordinate their centers differ by one
or two. Adjacent grid members touch; none overlap in their interiors.

Let $d_{-1}=1$, $d_0=-2$, $d_1=1$, and $c_{ij}=d_i d_j$. For any monomial $x^a y^b$ of
total degree $a+b\le3$,

$$
\sum_{i,j}c_{ij}(L/2+i)^a(L/2+j)^b
=\left(\sum_i d_i(L/2+i)^a\right)
 \left(\sum_j d_j(L/2+j)^b\right)=0.
$$

At least one of $a,b$ is at most one, and its second finite difference is zero.
Every feature whose restriction to orientation zero has total center degree at most
three therefore obeys $\Phi^Tc=0$. The positive entries of $c$ are the four corner ones
and the central four; the four remaining entries are $-2$. Hence $\sum u_i=\sum v_i=8$,
and the preceding argument gives

$$
0\le u^TAu=u^TAv\le-64,
$$

a contradiction. This proves impossibility for the entire stated class, for every $b$,
including at H114’s proposed side.
Arbitrarily many angular features do not help if their fixed-zero-orientation
restrictions remain center polynomials of degree at most three.
The same is true after joint $D_4$ averaging: composing with a container symmetry
preserves the total center degree on this axis-aligned slice.

The obstruction is more specific than a feature-count limit.
Adding features that still obey this dependence cannot fix it.
At total center degree four, the mixed term $x^2y^2$ has stencil value four and can
break this particular dependence; that observation is neither a feasible kernel nor a
reason to escalate the degree automatically.
The active Gram representation must retain the new direction.
Rational, piecewise, or other nonpolynomial features are outside this theorem unless the
same dependence is proved separately.

The full kernel class is nonempty.
For example, with ordinary area on $C_L$, $K(p,q)=L^2|S_p\cap S_q|$ has diagonal $L^2$
and vanishes on compatible pairs.
Its constant-one subtraction is the Gram kernel of the functions $L\mathbf1_{S_p}-1/L$
in $L^2(C_L)$: each square has area one and the container has area $L^2$. This is the
elementary area bound, not an improvement for H114. It also shows why a finite
polynomial obstruction must not be reported as failure of the kernel method.

## Required Controls and the Next Decision

Before a scientific kernel invocation, an independently reviewed instrument should
exercise the following finite controls.
These are prospective controls, not runs performed by this review.

| Control | Required behavior |
| --- | --- |
| Constant normalization | Reject $K=0$ as a kernel bound even though $K$ itself is PSD, its diagonal is zero and all pair values are zero; $K-1$ is not PSD. |
| Exact PSD and degeneracy | Accept an exact nonnegative Gram factorization; reject an indefinite matrix with nonnegative diagonal; detect a zero-pivot residual rather than omit it. |
| Finite packing equality | On an abstract compatible $N$-tuple, accept $K=NI$, for which $K-J=NI-J$ is PSD and $b=N$. This checks the bound calculation, not a continuum extension. |
| Touching and containment | Classify unrelated exact edge-touching, corner-touching and rotated touching pairs as compatible; distinguish a strict-overlap mutation; retain legal wall contact and reject a pose outside the container. |
| Identity and symmetry | Preserve the intrinsic quarter-turn identity, exchange symmetry and joint container symmetries; reject independent physical-pose folding and changed feature/source order. |
| Completeness and resource refusal | Refuse missing angle or separating-axis branches, incomplete diagonal coverage, altered coefficients or field embedding, unresolved signs and exhausted limits. |
| Trump packing control | Bind the accepted exact eleven-square packing at its own side $U$ and retain all eleven diagonal constraints and 55 unordered compatible-pair constraints. Any valid kernel must have $b\ge11$ there. Do not transplant this packing to $96/25$. |

A finite necessary-constraint obstruction is acceptable only with an exact certificate
of infeasibility for the prospectively fixed family.
The grid argument above supplies such a certificate analytically for cubic center
features. A solver’s infeasible status, a failure to find a matrix, or an unsuccessful
adversarial separator does not.
Conversely, a finite feasible matrix with $b<11$ cannot settle the full domain.

The smallest next decision is to compare the proposed feature family with this
obstruction before implementing a proposer or pair verifier.
Stop that family if the fixed-angle cubic premise holds.
A different family needs a precise definition and a credible price for its exact PSD
evidence, diagonal certificate, and all eight closed pair branches.
The pair problem still has six continuous pose coordinates; no runtime or manageable
subdivision count has been established here.
There is no automatic degree increase, target allocation or new campaign verdict.

The task’s scope follows
[Agenda027’s BC260 and BC264 entries](../../../../agendas/agenda-027-compatibility-and-restricted-families.md)
and
[X017’s kernel proposal](../../../../explorations/X-017-compatibility-and-complete-case-covers.md#c-two-pose-kernels-a-separate-bounded-opportunity).
The fixed-support density optimum from exp128 and Session096’s unweighted five-point
results supply no obstruction to the full interaction-kernel class.
The archive’s functional embedding of a boundary-null measure uses an unrestricted Gram
space; it does not promise that a small polynomial feature family reproduces that
kernel.

## Post-Freeze Admission: The Finite LP Instrument

This separate `think-330w` review began at the observed clock 2026-09-07 21:18:42 UTC,
after both first passes were frozen.
Its hard deadline is 21:26 UTC. The entire
[feature design](bc-264-kernel-feature-design.md) and the first-pass review above were
read. The following admission does not change that earlier report or its allocation.
No solver, target, scientific constructor, test, or coefficient evaluation was run.

**GO to implement only the finite refutational LP instrument**, with the exact
acceptance conditions below.
This is not target readiness, a continuum-verifier allocation, or an extension of any
earlier cap.

The feature and parameter counts are correct.
The four entries of $z$ transform trivially under $D_4$; $s$, $d$, and $w$ have three
distinct nontrivial scalar characters.
Both $V_0$ and $V_1$ transform as ordinary vectors: under a quarter-turn, $(uv^2,u^2v)$
becomes $(-u^2v,uv^2)$, and reflection changes the corresponding component sign.
Thus the joint-invariant symmetric coefficient matrices have blocks $A$, the three
scalars, and $B\otimes I_2$. There are eleven features and $10+3+3=16$ kernel
parameters. This decomposition retains all joint-invariant kernels in the selected span;
it does not independently symmetrize the poses.

The nine-grid positive control is valid.
The tensor Lagrange functions sum to one identically, and their node values are the nine
coordinate vectors. Hence $K_{\rm grid}=9\sum_a\psi_a(P)\psi_a(Q)$ has node matrix $9I$,
while its constant-one subtraction has the exact PSD factorization $9I-J$. The
polynomial is jointly invariant and lies in the declared biquadratic feature span.
The control must establish only the nine-node equalities and PSD evidence, not non-grid
pair signs or a continuum diagonal bound.

The proposed pool has at most $4\cdot9+9=45$ axis-aligned poses, at most 45 diagonal
rows and $\binom{45}{2}=990$ unordered pair candidates.
These are upper bounds before exact deduplication, not observed counts.
Both translated-grid origins keep their three centers in $[1/2,L-1/2]$ for $L\ge3$.
Compatibility is exactly the stated coordinate disjunction, with equality included.
Axis-only constraints are necessary for a full-angle kernel and can therefore refute it;
they cannot establish one.

For the $4\times4$ block, the fixed tests comprise four coordinate vectors and twelve
vectors $e_i\pm e_j$. The $2\times2$ block contributes four tests, and the three scalar
inequalities give $16+4+3=23$. All are necessary PSD conditions.
They are an outer relaxation, not a PSD characterization.

The normalized objective-bound certificate has the correct sign.
With $\alpha,\beta\ge0$, $\sum\alpha=1$, and the design’s reconstructed matrix $M$, the
diagonal and pair inequalities imply

$$
b\ge1+\sum\beta+\langle M,R\rangle.
$$

Full $M\succeq0$ is sufficient.
For this invariant family, a projected certificate is also sound, with an explicit
factor that the reader must retain.
Let $M_A$ be the invariant-feature block and let $M_{ij}^{V}$ be the $2\times2$ spatial
block between vector copies $i,j$. Put $T_{ij}=\operatorname{tr}(M_{ij}^{V})$. Then

$$
\langle M,R\rangle
=\langle M_A,A\rangle+M_{ss}a_s+M_{dd}a_d+M_{ww}a_w+\langle T,B\rangle.
$$

The joint average’s vector block is $(T/2)\otimes I_2$. Therefore exact PSD evidence for
$M_A,T$ and nonnegativity of the three scalar entries suffices.
In the minimal LP route, retain identities expressing these blocks as nonnegative
rational sums of the fixed test-vector outer products.
No numerical PSD test is needed.
The reader must reconstruct the blocks and verify those identities, rather than trust a
supplied projection.
With either format, $\sum\beta\ge10$ proves $b\ge11$ and rejects the selected family.
The nine-clique weights give $\sum\beta=8$ and the rank-one matrix stated in the design,
so that control proves only $b\ge9$.

The continuum descriptions are compatible.
Eight signed geometric axes become at most sixteen closed pieces after splitting the
sign of the relative sine.
In the quarter-turn chart the relative cosine is nonnegative; chart endpoints and
zero-sine seams remain included.
Expanding $(1+it)^8$ gives exactly the design’s numerators for $\cos4\theta$ and
$\sin4\theta$. Clearing the positive denominators gives diagonal tensor degrees at most
$(4,4,16)$ and pair degrees at most $(2,2,8,2,2,8)$, hence 425 and 6,561 coefficients
per surrounding box.
These counts do not certify any constrained box or bound the number of boxes.
The missing total continuum price remains a blocker for a continuum implementation.

The minimal implementation admission requires:

- A lazy, fixed scientific pool and feature definition, with deterministic exact
  deduplication and complete source binding.
  Source-free tests use unrelated rational inputs and forbid the scientific constructor.
- A separately authored reader that reconstructs poses, feature order, containment,
  compatibility, the 23 test directions, all weighted matrices and exact identities.
  Retain nonnegative rational multipliers, exact normalization and the exact threshold
  comparison. A more general Farkas format needs its own explicit identity and reader;
  the normalized objective-bound route suffices for this first instrument.
- Positive nine-grid and its $b\ge9$ dual controls; mutations for normalization,
  multiplier sign, threshold, mixed-block trace factors, feature/source order, omitted
  or duplicated poses in the fixed source, illegal overlap, misclassified touching pairs
  and invalid PSD identities.
  The nine-grid certificate must not be reported as an eleven-bound obstruction.
  Axis-only angular zeros and repeated feature values do not authorize changing the
  eleven-feature order.
- Bound input sizes and complete-child resource limits prospectively.
  A solver status, approximate dual, feasible outer relaxation, failed rationalization,
  malformed packet, or timeout gives no family refutation.
  Feasibility does not supply a PSD kernel candidate.
  No pool expansion, SDP or retry follows automatically.

A dual may have sparse support: omitting a zero-weight pair does not invalidate the
proof. The packet must distinguish that declared zero from a changed source inventory or
a false claim that all prescribed proposer rows were used.
Every positive-weight pair must be independently proved compatible; unweighted unused
pairs need not appear in the dual evidence.
This keeps source completeness separate from proof support.

The design’s proposed author, review and integration costs remain estimates; its
proposed once-only 60-second proposer and 60-second reader caps are not launch
authority. Registration, instrument controls and independent review must precede any
separately allocated scientific invocation.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
