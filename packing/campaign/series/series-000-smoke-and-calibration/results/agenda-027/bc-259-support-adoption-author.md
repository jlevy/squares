# BC-259: Source Binding for the Seven-Row Support Ceiling

Status: source-free author assessment under `think-m24i`, not adoption of the
contributed numerical certificate.
The mathematical reduction and a small history-free verification contract are ready for
independent review.
The exact quotient, orbit permutation and seven box memberships still
require a separately admitted implementation and recorded verification.

This is [Session095][session]’s first BC-259 allocation under [Agenda027][agenda].
Observed author start: 2026-09-07 at 11:53:32 UTC. Original hard deadline: 12:22:47 UTC.
Static derivation and documentation review completed at 12:05:30 UTC, after 718 seconds.
The scoped Flowmark 0.4.0 pass used 0.01 seconds wall, with user and system CPU both
rounded to 0.00 seconds.
No computational mathematics or test timing is claimed.
The author read source and retained data as text, without calling a scientific
constructor, creating a target field, evaluating target geometry, running tests or
inspecting the parallel independent assessment.
Only this prose file is in the author’s write scope.

## What Corresponds Statically

The [archived checker][archive-checker] transcribes the eleven-square construction in
[source-packet file09][source-packet]. That construction matches
[the current exact source][current-source] as rational functions of the same parameter,
with the same ordered square and corner labels.
The archive names the snapshot `4d305597a505ebfbe85f1851fa7148374661e622`. This
comparison concerns the inspected formulas; a future execution must record its own
immutable source revision.

Both declare the polynomial, in descending powers,

\[
P(u)=5u^8-10u^7-2u^6+14u^5+12u^4-6u^3+2u^2+2u-1,
\]

and select its root in $(36/100,37/100)$. This parameter is the half-angle tangent, not
the container side. The variable correspondence is:

| Archived `geometry()` | Current `build_in()` | Common expression or role |
| --- | --- | --- |
| `c`, `s` | `cos_a`, `sin_a` | $(1-u^2)/(1+u^2)$, $2u/(1+u^2)$ |
| `L` | `side` | $(6u+4)/(1+2u-u^2)$ |
| `r` | `r1` | $1-(L-3)c$ |
| `a` | `u1` | $((1+r)c-1)/s$ |
| `v` | `v1` | $c-s$ |
| `b` | `v2` | $(L-1)/s-r-(3+a)c/s$ |
| `x` | `x0` | $1+2/c-(L-2)s/c$ |

On the declared interval, $0<u<1$, so $1+u^2$, $1+2u-u^2$, $c$ and $s$ are positive.
Thus every displayed denominator is nonzero.
The identity $c^2+s^2=1$ is algebraic.
Both implementations send a local corner $(X,Y)$ of a tilted square to

\[
(1+cX-s(Y-r),\;1+sX+c(Y-r)).
\]

They use the same six axis-aligned offsets and five tilted offsets, in the same order,
and the same local corner sequence $(0,0),(1,0),(1,1),(0,1)$. No approximate-coordinate
comparison or root-to-side conversion is needed to establish this formula
correspondence.

The archive encloses that root by rational interval arithmetic.
The current [NumberField][field] validates irreducibility and the unique real root in
the declared open interval before enabling exact field operations.
Those are different arithmetic mechanisms for the same specified root.
Their actual preconditions and the archived positive enclosures were not replayed in
this allocation. The independent reader should use the current validated field rather
than trusting the archive’s root-bracket strings or `margin_positive` booleans.

## All Source Images and the Orbit Map

Write $Q_i$ for current zero-based seed $i$, and use the container maps

\[
R(X,Y)=(L-Y,X),\qquad F(X,Y)=(L-X,Y).
\]

The full labelled source consists of the 88 triples $(i,f,r)$ with $0\leq i<11$,
$f\in\{0,1\}$ and $0\leq r<4$, representing $R^rF^fQ_i$. The archive uses
representatives

\[
(k_0,\ldots,k_7)=(0,2,4,7,10,8,6,9).
\]

The omitted seeds are accounted for symbolically:

\[
Q_1=RQ_0,\qquad Q_3=R^3Q_0,\qquad Q_5=RFQ_4.
\]

For the last identity, $Q_4=[1,2]\times[L-1,L]$ maps under $RF$ to
$[0,1]\times[L-2,L-1]=Q_5$. Also $FQ_0=RQ_0$, so the four unreflected quarter-turn
images of $Q_0$ include its whole geometric D4 orbit.
The other seven representatives receive all eight maps.
Consequently the archive’s enumeration covers the full source closure, with at most the
60 listed placements.
This establishes coverage; it does not establish that all 60 listed placements are
distinct.

The remaining exact check must establish the claimed distinctness and classes

\[
\{0,1,3\},\{2\},\{4,5\},\{7\},\{10\},\{8\},\{6\},\{9\},
\]

with sizes $(4,8,8,8,8,8,8,8)$. The archive’s disjoint center enclosures are a
sufficient distinctness test, but its successful retained output is not an independent
current-source replay.
The new reader can instead compare exact reduced corner sets from all 88 maps.

Let $\sigma(j)$ be the unique current orbit containing $Q_{k_j}$. The reader must derive
this permutation and require equality of the complete orbit sets.
It must not assume that the archived representative order is the current lexicographic
order, even if the resulting permutation is the identity.
Reindex every row and its size vector by this same permutation.
Compare all labelled preimages as well as the geometric quotient; matching only the
eight sizes or weight strings is insufficient.

[Producer binding][support-binding] supplies `bind_source()` and `support_metadata()`.
[The existing independent reader][independent-reader] supplies `reconstruct_source()`
using eight explicit coordinate maps rather than the producer’s iterative rotations.
Its source factory and exact arithmetic remain shared foundations.
The serialized corner sets are identity keys, not cyclic polygon boundaries; row
geometry must use reconstructed cyclic corners.

## Averaging and the Matching Baseline

Let $\mathcal F$ be the distinct D4 support and let nonnegative weights on it have depth
at most one Lebesgue-almost everywhere in $[0,L]^2$. Average these weights over D4.
Isometries preserve null sets, and a finite union of null exceptional sets is null, so
the average remains feasible and preserves total mass.
It has a constant weight $a_j$ on each distinct orbit.
This applies to real weights and hence to [H099][h099]’s rational weights.

For an orbit of size $s_j$ containing $n_j$ original seeds, every placement in that
orbit has $8n_j/s_j$ labelled preimages.
Indeed, each original seed contributes one coset of its stabilizer, of size $8/s_j$. The
average of the eight complete original packings therefore assigns the per-placement
weight $n_j/s_j$ and has total mass $\sum_j n_j=11$.

Subject to the quotient check above, the archived order gives

\[
n=(3,1,2,1,1,1,1,1),\qquad
a^{\rm avg}=(3/4,1/8,1/4,1/8,1/8,1/8,1/8,1/8).
\]

The lower-bound premise is that the original eleven squares form a contained
interior-disjoint unit-square packing.
The existing `verify_packing(..., sign=exact_sign)` check supplies that premise in both
source-binding paths; boundary contacts are permitted.
No new arrangement certificate, pair-clique certificate or local-isolation theorem is
needed for this average.
Every source placement, including any placement assigned zero by a different candidate,
remains part of the support identity.

## The Seven Necessary Rows

The [retained row data][archive-rows] fixes seven rational centers, the common
$\ell^\infty$ radius $r=1/100000$, the following incidence rows and the multipliers
$\lambda=(1,3,1,1,5/2,1,3/2)$ in archived orbit order:

\[
A=\begin{pmatrix}
1&1&0&0&1&0&0&0\\
1&2&0&0&0&0&0&0\\
0&1&1&0&1&0&2&2\\
0&0&2&2&1&0&0&1\\
0&0&2&2&2&0&0&0\\
0&0&0&1&0&2&3&2\\
0&0&0&0&0&4&2&2
\end{pmatrix}.
\]

The rational identity is

\[
A^T\lambda=(4,8,8,8,8,8,8,8),\qquad
\mathbf1^T\lambda=11.
\]

For example, its eight column sums are respectively $1+3$, $1+6+1$, $1+2+5$, $2+5+1$,
$1+1+1+5$, $2+6$, $2+3+3$ and $2+1+2+3$. This is arithmetic on the supplied rational
data, not a geometric measurement.

For a cyclic square edge with vector $(d_x,d_y)$ and orientation sign $o$, put

\[
g_e(z)=o\det((d_x,d_y),z-v_e).
\]

On the closed box $B=p+[-r,r]^2$, its exact range is

\[
[g_e(p)-r(|d_x|+|d_y|),\;g_e(p)+r(|d_x|+|d_y|)].
\]

Thus the independent reader can establish that $B$ lies strictly inside a square when
all four lower endpoints are positive, or strictly outside it when at least one upper
endpoint is negative.
Otherwise that square’s membership is unresolved.
It must also check all four strict container margins for the same unchanged box.
Each row counts every distinct placement once; it is not a binary orbit-incidence row.
The producer can use the separate center/orthonormal-axis projection formulation.

Once those checks establish constant incidence throughout each positive-area box, a.e.
feasibility implies $Aa\leq\mathbf1$. Multiplication by $\lambda\geq0$ gives

\[
\sum_j s_ja_j=\lambda^TAa\leq\lambda^T\mathbf1=11.
\]

Together with the valid packing average, this proves that the full fixed-support
supremum is exactly eleven.
No optimization, LP history or full arrangement enumeration is part of that deduction.

There is a specific adapter gap: the current `_replay_upper()` requires clearance from
every supporting line of every square, even when one edge already separates an exterior
square from the box.
The archive only requires that separating edge.
A box can meet an extension of another edge and still be strictly exterior.
Consequently the existing stronger guard is not known to admit the frozen row boxes.
Use the exact box contract above, with source-free controls; do not silently shrink a
radius, move a point or bypass the side-two guard on `replay_upper()`.

## Smallest History-Free Verification Contract

The next implementation should be a fixed-row adapter and its independent reader,
without an LP or general face-enumeration engine.
Its scientific factory must be explicit and lazy; imports and synthetic controls must
not construct the Trump field, source or rows.

The proposed positive packet contains:

- A distinct versioned packet kind, fixed source `trump11-v1`, the declared real field
  embedding and the unchanged archived seven-row dataset identity.
- Complete existing support metadata: exact side, orbit corner keys, every labelled
  preimage, sizes, original counts and average weights, plus the derived
  archive-to-current orbit permutation.
- Exactly seven ordered rows with their unchanged rational centers and radii,
  reconstructed integer counts and frozen nonnegative multipliers; the claimed upper
  value eleven.
- A complete status with no unresolved membership or source obligation.
  Partial or timeout output has no positive interpretation.

The producer reuses `build()` and `bind_source()` and verifies each fixed box by
projection. The independent reader reuses `reconstruct_source()` and verifies the boxes
by oriented edges. It reconstructs all source metadata and the orbit permutation,
compares the packet and frozen row data exactly, and checks the rational identity.
Neither side needs `initial_rows()`, `extend_rows()`, `solve_screen()` or the old
candidate-refutation box.

Reuse [the existing reader’s][independent-reader] bounded `load_packet()` and its
canonical rational parsing discipline: reject duplicate keys, floats, unsafe exponent
syntax and oversized strings before conversion; enforce the 2 MiB packet limit and full
eight-coefficient field-element width.
The new packet needs its own closed shape and inventory checks.
`checked_rational()` alone is not an untrusted-input guard.
The producer may reuse [the solver-free `check_upper()`][support-geometry] after
parsing; the reader’s eight column sums and multiplier sum are small enough to implement
independently. Shared `NumberField`, exact signs, seed construction and packing validity
must be named as shared foundations, not counted as independent implementations.

The old `replay_packet()` cannot consume this packet: it requires exp113’s deterministic
row-generation history, dispositions, matching primal and solve metadata.
Do not fabricate that history, alter exp113 or import the contributed executable as the
new independent reader.

Controls must cover reflected and reparameterized cyclic squares; interior and exterior
boxes; an exterior box meeting another supporting-line extension; actual boundary
straddling; zero radius and wall crossing; stabilizer multiplicity and duplicate seed
labels; altered geometry, orbit order, preimages, field identity, counts and
multipliers; missing or duplicate rows; and malformed, oversized and partial packets.
Use unrelated rational and degree-eight toy fields and forbid scientific factories and
solver calls in these controls.
The legacy `test_full_size_density_support_screen_review.py` cannot be run wholesale
under that prohibition: its Trump source-control test constructs the actual packing, and
its algebraic toy uses the actual Trump field.

## Funding Decision and Accepted Scope

The static formula correspondence, symbolic coverage of all source seeds, averaging
argument and rational upper-bound implication have no identified mathematical gap.
There are two unmeasured geometric obligations: source validity and exact quotient/orbit
binding, and the seven unchanged box-incidence checks.
Their finite contract is explicit enough to price the one further BC-259 allocation,
subject to the parallel review.
This report does not establish instrument readiness or authorize a target.

If the coordinator funds at most thirty more active minutes, spend them on the narrow
adapters, source-free controls, independent review and the prospective admission record.
A possible later protocol is one whole-process producer capped at sixty seconds and,
only after an actual exit-zero complete positive packet, one independent reader capped
at sixty seconds. These are proposed caps, not runtime measurements or execution
authority. Stop at the original allocation boundary if readiness is incomplete.
Do not extend the row set, change its boxes, repeat a refused target or build a general
higher-order verifier within this allocation.

Only a future independently accepted ceiling may reject H099 for this exact support and
side. It would not establish a full-pose primal covering density, equality of the
unrestricted primal and dual values, a below-side transport, global optimality or a new
packing bound. The prior exp113, exp115 and exp126 receipts retain their historical
scope. The separate candidate-refutation box is unnecessary for the ceiling adoption.

[session]: ../../../../agent-sessions/session-095-collision-cover-and-support-ceiling.md
[agenda]: ../../../../agendas/agenda-027-compatibility-and-restricted-families.md
[h099]: ../../../../hypotheses/H-099-trump-d4-finite-support-dual.md
[archive-checker]: ../../../../../resources/papers/n11-complete-research-bundle-2026-09-07/original_review/certificate/check_support_ceiling.py
[archive-rows]: ../../../../../resources/papers/n11-complete-research-bundle-2026-09-07/original_review/certificate/support_exact_result.json
[source-packet]: ../../../../../resources/papers/n11-complete-research-bundle-2026-09-07/source_packet/09-trump-construction-and-local-proof.md#source-1
[current-source]: ../../../../../cases/trump11/packing.py
[field]: ../../../../../src/sqpack/field.py
[support-binding]: ../../../../../src/sqpack/full_size_density/support_screen.py
[support-geometry]: ../../../../../src/sqpack/full_size_density/support_ceiling.py
[independent-reader]: ../../../../../devtools/check_full_size_density_support_ceiling.py

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
