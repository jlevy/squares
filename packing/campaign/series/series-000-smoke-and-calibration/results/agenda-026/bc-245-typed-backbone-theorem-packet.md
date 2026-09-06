# BC-245 Typed Stationary-Backbone Theorem Packet

Status: **author draft complete, with finite-language and Fritz–John completeness
derivations at contract scope; source-distinct theorem review, an implemented atlas, and
every continuous leaf closure remain open, while BC-246 and BC-247 stay blocked.**

This packet supplies BC-245’s (`think-do04`) author draft; coordinator and
source-distinct review disposition remain open.
It replaces a generic planar contact-graph proposal with a finite typed language whose
records retain the continuous systems and degeneracies that a global proof would have to
close.
A record is not a solution, and the existence of finitely many record types is not
a global packing proof.

## Frozen scope and inputs

- Official T+0: `2026-09-06T03:31:00Z`.
- Launch commit: `c55726e1e885227f63110131c0a914665175ff89`.
- Preregistration commit: `f1b6c641e8d3a2fea39cf5aa5292cb8fc1221772`.
- Agenda 026 SHA-256:
  `096470755cb056d6dcd9d103d4233819d03f8bff9035e1027d213ca51ab4cb49`.
- Exact Trump witness SHA-256:
  `3b4eae938c37c13af6252ac5d83fa99aa95f6b1627b99920c5df8be94c56bea9`.
- Retained BC-199 result SHA-256:
  `db124b9956d8051682388cbba3b16772e65406a0003debba1c92b915c0c489a8`.
- Retained exp-013 tangent result SHA-256:
  `60a4b7c48034b37063509a8a641974ed5eae86dccd056e9cbc6cf2fd7f2f0661`.

## Configuration program and existence

For fixed \(n\), use

\[
z=(L,c_1,\theta_1,\ldots,c_n,\theta_n),
\]

where \(L\) is the container side, \(c_i\in\mathbb R^2\), and
\(\theta_i\in\mathbb T_4=\mathbb R/(\pi/2)\mathbb Z\). Square \(i\) is
\(S_i=c_i+R_{\theta_i}[-1/2,1/2]^2\). The original program minimizes \(L\), subject to
containment in \([0,L]^2\) and pairwise disjoint interiors.

Let \(U\) be the side of any exact known feasible packing.
In the sublevel \(0\leq L\leq U\), containment puts every centre in \([0,U]^2\), and the
angle quotients are compact.
Corner containment is closed.
By the separating-axis theorem, pairwise nonoverlap is equivalent to \(G_{ij}(z)\geq0\),
where \(G_{ij}\) is the maximum of the eight continuous owner-axis-order support gaps
defined below. A finite maximum is continuous.
Changing a quarter-turn representative only permutes those eight local gap labels, so
their maximum descends continuously to the angle quotient.
Every pair condition is therefore closed on the compact quotient.
The feasible sublevel is nonempty and compact, so \(L\) attains a minimum there.
Any configuration better than \(U\) lies in the same sublevel, hence this is a global
minimum of the original program.

The inequality \(L\leq U\) is used only for the compactness argument.
It is not a geometric row, does not enter the stationary record, and contributes no
multiplier. Stationarity is taken in the original program, where the attained global
minimum is also a local minimum.

## Smooth support branches

Define the two directed local axes of square \(i\) by

\[
u_{i,0}=(\cos\theta_i,\sin\theta_i),\qquad
u_{i,1}=(-\sin\theta_i,\cos\theta_i).
\]

The projection radius of square \(i\) in a unit direction \(a\) is

\[
r_i(a)=\tfrac12\bigl(|a\mathbin\cdot u_{i,0}|+
|a\mathbin\cdot u_{i,1}|\bigr).
\]

For each unordered pair \(\{i,j\}\), the separating-axis theorem says that their
interiors are disjoint exactly when at least one axis from
\(u_{i,0},u_{i,1},u_{j,0},u_{j,1}\) separates their projected intervals in one of the
two orders. A selected pair row therefore has the type

\[
b=(\{i,j\},o,r,\sigma),
\]

where the owner \(o\in\{i,j\}\), local axis \(r\in\{0,1\}\), and order sign
\(\sigma\in\{-1,+1\}\). With \(a=u_{o,r}\), its inequality is

\[
g_b(z)=\sigma a\mathbin\cdot(c_j-c_i)-r_i(a)-r_j(a)\geq0.
\]

There are eight typed choices before support-sign ties for each square pair.
Choosing one valid row for every pair retains every noncontact inequality rather than
only a proposed backbone.
Positive slack certifies noncontact; zero slack marks an active support row whose
physical-contact status is checked separately below.
It never replaces a square contact by a centre-distance equation.
When angle forcing makes two owner-axis labels induce the same algebraic inequality, the
labels remain distinct until an exact type-preserving duplicate map is recorded.
This distinction matters for the axis-aligned small-n controls below.

Each absolute value in a support radius is resolved by a finite sign cell.
At a zero dot product, both closed sign cells are retained.
Owner-axis or separation-order ties likewise place one geometry in several branches.
On every selected sign cell, \(g_b\) is smooth in local angle coordinates.
The owner’s radius along its own axis is simplified identically to \(1/2\); its
identically zero cross-axis dot product does not create a false branch.
Only genuine support-expression ties are split.

For wall containment, let \(q\) range over the four labelled corners of
\([-1/2,1/2]^2\), and put \(v_{i,q}=c_i+R_{\theta_i}q\). Retain all four inequalities
for every corner:

\[
\begin{array}{ll}
g_{i,q,\mathrm{left}}= (v_{i,q})_x\geq0,&
g_{i,q,\mathrm{right}}=L-(v_{i,q})_x\geq0,\\
g_{i,q,\mathrm{bottom}}=(v_{i,q})_y\geq0,&
g_{i,q,\mathrm{top}}=L-(v_{i,q})_y\geq0.
\end{array}
\]

These row identities retain the responsible corner and wall without a hidden max or min.
In particular,

\[
\partial_L g_{i,q,\mathrm{right}}
=\partial_L g_{i,q,\mathrm{top}}=1,
\qquad
\partial_L g_{i,q,\mathrm{left}}
=\partial_L g_{i,q,\mathrm{bottom}}=0.
\]

Two adjacent active corner rows on one wall encode an edge-wall segment tie; one active
corner row encodes a point feature.
Redundant active corners remain present.

The orientation circle needs a finite overlapping chart atlas.
Make this explicit with the quotient coordinate

\[
\zeta(\theta)=(\cos4\theta,\sin4\theta).
\]

On \(U_+=S^1\setminus\{(-1,0)\}\), use \(t=\zeta_y/(1+\zeta_x)=\tan2\theta\), with
inverse

\[
\zeta_x=(1-t^2)/(1+t^2),\qquad \zeta_y=2t/(1+t^2).
\]

On \(U_-=S^1\setminus\{(1,0)\}\), use \(s=\zeta_y/(1-\zeta_x)=\cot2\theta\), with
inverse

\[
\zeta_x=(s^2-1)/(s^2+1),\qquad \zeta_y=2s/(s^2+1).
\]

The two open charts cover the quotient, so each orientation is interior to at least one
chart. For finite closed branch cells, use

\[
V_+=\{\zeta_x\geq-1/2\}\subset U_+,
\qquad
V_-=\{\zeta_x\leq1/2\}\subset U_-.
\]

They cover the circle with an overlap; at a boundary of either cell, the point is
interior to the other.
Retain both labels in the overlap.
For exact support rows, carry axis variables \(a=\cos\theta,b=\sin\theta\) with
\(a^2+b^2=1\), a finite local-lift identifier, and the polynomial quadruple-angle
equations

\[
\zeta_x=a^4-6a^2b^2+b^4,\qquad \zeta_y=4ab(a^2-b^2).
\]

The four algebraic lifts differ by quarter-turns and induce corresponding local-axis
permutations and signs; a fixed quadrant convention is not smooth across the identified
endpoint. Every applicable lift and chart is retained there.
Local axis coordinates, chart equations, domain signs, and exact isolating intervals
travel together. A producer may use more charts, but it may not claim completeness from
one chart or from floating angles.

## Finite branch-cover lemma

For fixed \(n\), the feasible configuration set is a finite union of smooth inequality
branches carrying all of the labels below.

**Proof.** Use a finite overlapping chart cover for each of the \(n\) compact angle
quotients. For every square pair, choose one of the eight owner-axis-order rows supplied
by the separating-axis theorem.
Split every support absolute value into its two closed sign cells.
Retain all labelled corner-wall inequalities.
These finitely many products of choices cover every feasible configuration.
Inside a choice, all constraint functions are smooth in the chosen local coordinates.
At ties, the configuration lies in every applicable closed branch, so the cover loses no
degenerate point. Contact features, coordinate preorders, cyclic boundary orders, active
masks, and multiplier support masks have finite label sets for fixed \(n\); attaching
them refines the same finite cover.
\(\square\)

Because the two closed atlas cells overlap as specified, the FJ representative can be
chosen in a chart cell whose boundary is inactive at the geometry.
Atlas-boundary rows remain in sibling records for replay; they are not used to
manufacture stationarity.
Support-sign ties are genuine nonsmooth strata and remain in every applicable branch.

The lemma proves finiteness of the **language**. Each record still carries a continuous
semialgebraic feasibility and stationarity system, which may have several roots,
positive-dimensional components, or no realization.
In the algebraic chart encoding, support signs remove every absolute value and clearing
the strictly positive chart denominators leaves polynomial equalities and inequalities;
adjoining FJ variables and their polynomial stationarity equations preserves
semialgebraicity.

## Fritz–John completeness lemma

Let one smooth branch be written as \(g_j(z)\geq0\) for every geometric and branch-cell
row \(j\). If \(z_*\) is a minimum of the full packing program, then on every branch
containing \(z_*\) it is a local minimum.
The Fritz–John theorem supplies nonnegative multipliers \(\alpha\) and \(\lambda_j\),
not all zero, such that

\[
\alpha\nabla L(z_*)-\sum_j\lambda_j\nabla g_j(z_*)=0,
\qquad
\lambda_jg_j(z_*)=0.
\]

Positive rescaling gives the projective normalization

\[
\alpha+\sum_j\lambda_j=1.
\]

For the corner-wall row convention above, the \(L\)-component of stationarity is

\[
\alpha-
\sum_{(i,q,w):\,w\in\{\mathrm{right},\mathrm{top}\}}
\lambda_{i,q,w}=0,
\]

because pair, left-wall, and bottom-wall rows have zero \(L\)-derivative.
This objective equation is retained even when a record is summarized by its positive
support. If a producer adds an \(L\)-dependent order or feature partition row, its
derivative must be added to this equation rather than silently discarded.

This proves that every global minimum is represented by at least one finite typed branch
with a normalized Fritz–John certificate.
It does not prove that every such certificate is feasible, locally minimizing, or
globally optimal.

- If \(\alpha>0\), rescale to the normal/KKT form.
- If \(\alpha=0\), the certificate is an abnormal Fritz–John branch.
- A geometry may admit both normal and abnormal certificates.
- An abnormal branch may be deleted only after a branchwise constraint qualification is
  proved, including every tie stratum affected by the deletion.

The displayed lemma uses local chart coordinates, so algebraic chart-reconstruction
equations are witness identities rather than optimization constraints and the stated
normalization is exactly \(\alpha+\sum\lambda_j=1\). If a replay instead formulates a
redundant algebraic embedding with equality constraints \(h_k=0\), its stationarity
equation must add unrestricted terms \(\sum_k\mu_k\nabla h_k\). It must either eliminate
those equalities before asserting the local-coordinate certificate or carry the
\(\mu_k\). With \(\mu_k=\mu_k^+-\mu_k^-\) and \(\mu_k^\pm\geq0\), the matching
projective normalization is

\[
\alpha+\sum_j\lambda_j+\sum_k(\mu_k^++\mu_k^-)=1.
\]

Silently omitting equality multipliers or retaining the local-only normalization in an
embedding is invalid.
The `normal` or `abnormal` label always refers to the local-coordinate certificate.
If the embedding equations have dependent gradients, a nonzero pure equality multiplier
can exist at an arbitrary feasible point; it is not geometric stationarity evidence.
Such a replay must prove a regular reduction back to the local certificate or leave the
stationarity obligation open.

## Rows, contacts, and degeneracies

Every record keeps these objects separate:

1. `objective_row`: the retained gradient row for the side variable \(L\);
2. `complete_rows`: the selected separation inequality for **every** square pair, all
   labelled corner-wall containment rows, all chart or sign-cell boundary rows, and
   every order or feature comparison used to restrict the branch;
3. `active_rows`: precisely the complete rows whose exact slack is zero; and
4. `positive_multiplier_rows`: precisely the active rows with strictly positive
   multiplier in the particular FJ certificate.

Here `complete` means complete for the selected smooth branch: exactly one separating
disjunct for every unordered square pair, not merely the touching pairs.
The other seven pair alternatives live in sibling branches and remain part of the global
branch cover; they are not simultaneous inequalities of this branch.

The set difference `active_rows - positive_multiplier_rows` is recorded as
`zero_multiplier_rows`. An active contact can carry zero stress.
A redundant contact can be active under several owner axes.
A rattler can be absent from the positive support while its centre, angle, wall rows,
and pairwise noncontact rows remain in the system.
No connected-backbone premise is used.
If one geometry has several multiplier rays or supports, each certified choice is a
separate typed record linked to the same geometry; the language never assumes stress
uniqueness.

For an active pair row, record the actual exposed support faces on both squares and
their tangential intersection.
The feature types distinguish vertex–vertex, vertex–edge, edge–vertex, and edge–edge
segment contact.
A zero projection gap need not by itself assert physical contact: if the
exposed faces have disjoint tangential ranges, retain the active redundant row and mark
the contact feature absent.
Wall features similarly distinguish point and segment incidence.
A vertex–vertex contact can belong to several tied support descriptions; every
applicable branch is retained, and no centre-distance equality substitutes for them.

Coordinate orders are total preorders, not permutations: equal coordinates occupy the
same block. Boundary incidences on each square carry a cyclic preorder with coincident
features tied. Orders are derived from and replayed against the exact witness.
A generic-position assumption, tie-breaking perturbation, or silent deletion of a
zero-length interval is forbidden.

Orders and contact-feature labels may remain derived replay metadata rather than
constraints of the selected support branch.
If a producer instead uses an order or feature comparison to partition a leaf, every
such comparison becomes a `complete_rows` entry and participates in FJ stationarity when
active. It may not restrict a leaf by metadata while omitting the corresponding row.

## Soft record contract

The following is a permissive design contract, not an implemented schema.
A later producer may add fields, but it must emit every required field and an
independent replay must consume every one.

```yaml
schema_version: bc245-v1
record_id: stable typed identifier
geometry_id: shared exact-witness identifier across multiplier certificates
n: positive integer
status: open | infeasible | covered | solved
objective:
  variable: L
  row_id: objective:L
  gradient: exact unit row in the L coordinate
  incumbent_upper: exact value with provenance
provenance:
  launch_commit: full SHA
  source_hashes: {repository_relative_path: sha256}
coordinates:
  variables: [L, centres, angle coordinates]
  exact_domain: rational | real_algebraic | symbolic_semialgebraic
  angle_charts:
    - square: labelled square
      chart_id: finite-atlas member
      local_lift_id: quarter-turn lift with axis-label action
      chart_equations: exact equations
      axis_equations: exact sine/cosine reconstruction equations
      domain_rows: exact inequalities
      isolating_box: outward-rational box
branch:
  pair_rows:
    - row_id: stable identifier
      pair: [i, j]
      owner: i | j
      owner_axis: 0 | 1
      order_sign: -1 | 1
      support_signs: complete tied sign data
      inequality: exact symbolic expression
  wall_rows:
    - row_id: stable identifier
      square: i
      corner: labelled corner
      wall: left | right | bottom | top
      inequality: exact symbolic expression
  partition_rows: complete chart and support-sign boundaries
features:
  square_contacts:
    - pair: [i, j]
      active_row_ids: [stable identifiers]
      face_i: vertex | edge
      face_j: vertex | edge
      intersection: absent | point | segment
      tied_descriptions: [other applicable branch labels]
  wall_contacts:
    - square: i
      wall: labelled wall
      corners: [all responsible labelled corners]
      intersection: point | segment
orders:
  x_coordinate_preorder: ordered blocks with ties
  y_coordinate_preorder: ordered blocks with ties
  cyclic_boundary_preorders: per-square tied cyclic blocks
rows:
  complete: [every feasibility and partition row id]
  active: [exactly zero-slack row ids]
  positive_multiplier: [strictly positive multiplier row ids]
  zero_multiplier: [active row ids with zero multiplier]
fj:
  coordinate_mode: local_parametrization | algebraic_embedding
  kind: normal | abnormal
  alpha: exact nonnegative value
  lambda_by_complete_row: {row_id: exact nonnegative value}
  equality_multipliers: omitted locally or exact mu-plus/mu-minus values
  normalization: alpha+sum(lambda)=1 locally; alpha+sum(lambda)+sum(mu+ + mu-)=1 in embedding
  equality_rank_certificate: null locally or exact regular-reduction evidence
  local_certificate_projection: exact map or open
  stationarity_residual: exact zero vector
  complementarity: exact zero products
degeneracy:
  feature_ties: [typed ties]
  redundant_active_rows: [row ids]
  rattlers: [square ids]
  rattler_attachments: complete retained feasibility row ids
symmetry:
  group: D4_x_Sn
  canonical_key: lexicographic key over every transformed field
  orbit_witness: exact group element from source to canonical record
witness:
  realization_status: unrealized | exact
  exact_values: null or rationals/defining polynomials plus isolating intervals
  feasibility_replay: null or exact row slacks and feature checks
leaf_evidence:
  method: exact_lp_farkas | verified_interval | exact_algebra
  artifacts: [immutable certificate paths and hashes]
  coverage: entire branch | named stationary components | open remainder
obligations:
  discharged: [machine-checkable claims]
  open: [every unclosed branch or component]
```

An `open` unrealized branch record can be well formed, but it is not a certified
realized canonical record.
Every realized canonical record requires the exact witness and orbit replay.
Schema validity, witness validity, branch closure, and global completeness are separate
verdicts.

## Joint symmetry action

The group \(D_4\times S_n\) acts jointly on the continuous geometry and every label.
A container rotation or reflection transforms centres and angles, permutes walls and
corners, changes local-axis and sign conventions where required, transports coordinate
and cyclic preorders, and maps every row together with its multiplier.
A square permutation transports owners, pair order, features, rattlers, and witness
coordinates. Chart IDs may change under either action.

Canonicalization enumerates the full joint orbit, serializes all required transformed
fields, and chooses the lexicographically least serialization.
The record carries the exact group element that maps the source to that representative,
and exact replay must recover the transformed rows and witness.
Graph isomorphism alone is unsound because it forgets walls, support features,
separation order, charts, multiplier states, and rattlers.

## Leaf-closing obligations

Each canonical record denotes a continuous semialgebraic system.
It closes only through a complete certificate assembled from one or more of the
following routes:

- **Exact fixed-angle LP:** when all angles are exact and fixed, use the existing
  `packing/src/sqpack/exact_lp.py::fixed_cell_lp` centre-and-side LP surface.
  An infeasible leaf needs an exact Farkas certificate; an objective claim needs an
  exact primal/dual certificate and replay of every typed row.
- **Verified interval cover:** enclose every coefficient and residual outward on every
  angle and coordinate box.
  A lower objective exclusion must cover the entire leaf.
  Boxes that cross chart, feature, or support-sign ties are split or handled with all
  tied branches.
- **Exact algebra or root isolation:** record defining polynomials and isolating data,
  prove that all real stationary components in the branch were accounted for, replay
  feasibility and FJ equations exactly, and bound the objective on each component.

One exact stationary witness does not close its branch.
Another isolated root or a positive-dimensional rattler family may have a better
objective. A floating realization LP is a proposer, and a cap or timeout produces an
open-branch receipt.

## Pruning table

| Proposed pruning | Status | Required evidence |
| --- | --- | --- |
| Chart-domain or sign-cell contradiction | Safe | Exact inequality contradiction; all tie charts retained |
| Inconsistent coordinate or cyclic preorder | Safe | Exact order contradiction including equality blocks |
| Pair or wall infeasibility at fixed angles | Safe | Exact LP/Farkas certificate over the complete rows |
| Interval objective bound worse than an exact incumbent | Safe | Outward enclosure covering the entire branch |
| Exact algebraic infeasibility or objective exclusion | Safe | Complete real-root or component certificate |
| Joint symmetry quotient | Safe | Full-field `D4 x S_n` transform and exact orbit witness replay |
| Duplicate leaf removal | Conditional | Exact type-preserving bijection, including rows and multipliers |
| Delete inactive inequalities or rattler variables | Refused | They remain part of feasibility even when absent from positive support |
| Keep only positive-stress contacts or a connected graph | Refused | Neither is a necessary condition proved here |
| Assume generic features, strict orders, or nonzero multipliers | Refused | Deletes tie and degenerate minima |
| Discard abnormal FJ branches | Refused | Requires a branchwise constraint-qualification proof |
| Close a branch from one witness, a floating LP, or a timeout | Refused | Does not account for every stationary component |
| Infer n=11 price or completeness from n=5 | Refused | n=5 is representability and local-rigidity only |

## Frozen controls for later implementations

These controls are obligations, not executions performed in this block.

| Control | Frozen expected recovery | Permitted conclusion |
| --- | --- | --- |
| n=3 exact oracle | After axis-aligned orientation forcing, 64 four-way separation choices, 24 consistent one-cells, and a `D4 x S3` quotient that is a closed interval with three named strata | Completeness control for all n=3 optimum strata after an exact map from the general typed labels |
| n=4 exact oracle | After axis-aligned orientation forcing, 4,096 four-way choices, 96 consistent zero-cells, 24 labelled grid states, and one quotient point | Completeness control for the n=4 optimum after an exact map from the general typed labels |
| n=5 Göbel witness | Exact representability and the already proved local rigidity of the named witness | Positive representation and local control only; never full n=5 completeness |
| n=11 Trump endpoint | 14 touching pairs, 20 wall-corner incidences, two angle classes of sizes six and five, 512 raw feature selections, 128 derivative-distinct matrices, 42 active rows per retained tangent branch, and the exact exp-013 verdict | Local endpoint compatibility only; invoke BC-240 only after its source-distinct review |

Separate synthetic exact fixtures are required before claiming coverage of an abnormal
FJ certificate, an active zero-multiplier row, or a rattler family.
Do not assign those labels to n=3, n=4, n=5, or Trump merely to satisfy a control.

The oracle counts are not raw counts for the general eight-label language.
Before support-sign refinement and duplicate-expression handling, that language has
\(8^3=512\) owner-axis-order choices for n=3 and \(8^6=262{,}144\) for n=4. The retained
64 and 4,096 counts are \(4^3\) and \(4^6\) four-way controls after the solved cases
force axis-aligned orientations.
A later producer must emit and replay an exact many-to-one map from its general typed
rows to those four geometric directions; it may not cite the smaller historical counts
as validation of its raw enumeration.

BC-246 must reproduce every Trump count and the retained tangent verdict through the new
typed producer and independent replay before using the BC-240 local theorem.
BC-247 must recover every n=3 quotient stratum and the n=4 orbit, represent the Göbel
witness, make the declared mutations fail for their intended reasons, and derive any
n=11 price only from named measured factors.
Neither cell is open now.

## Draft-satisfied and open obligations

Supplied in this author draft:

- existence of a global minimum below a known feasible side;
- a finite smooth support-branch cover that retains all ties;
- normalized normal/KKT and abnormal Fritz–John alternatives at every minimum;
- separation of complete, active, positive-support, and zero-multiplier rows;
- retention of feature owners, walls, signs, orders, charts, redundant contacts, and
  rattlers;
- the complete soft record vocabulary, joint symmetry action, and sound pruning rules;
- exact LP/Farkas, interval, and algebraic leaf-closing obligations;
- the distinct roles of the n=3, n=4, n=5, and Trump controls.

Open:

- an implemented finite chart atlas and typed-record producer;
- an independent replay guard that consumes every required field;
- enumeration, realization, and exact closure of any nontrivial branch family;
- proofs eliminating any abnormal, tied, zero-multiplier, or rattler branch;
- execution of the BC-246 Trump recovery and BC-247 solved-case controls;
- a measured n=11 branch price;
- every global optimality, uniqueness, or capture conclusion.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
