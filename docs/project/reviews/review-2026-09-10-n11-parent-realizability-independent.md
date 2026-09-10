# Independent Review of Translated Individual-Parent Realizability

September 10, 2026. W10 mathematical review for `think-cvvy`.

**Verdict: PASS.** Every centrally translated member of the retained 88-core family has
the claimed concentric unit parent for every real `Delta >= 69/20000`. The parent is
strictly inside the enlarged container, and the declared folding and nearest-direction
selection returns the same geometric core.
The conclusion also extends to the admitted 64-placement A6 family, at its corresponding
side `q >= 76569/20000`.

I reconstructed the containment and selection arguments independently.
The depth, weight, and atom-capacity facts below are admitted inputs from existing exact
receipts; I inspected their sources and receipts without rerunning a scientific target.
This review changes no repository file, registered claim, or bound.
The inspected HEAD was `3a18a05a6af75e3800612549d5a3c5fe419b96f2`. The parent-domain
translation document was untracked; the inspected tracked mathematical inputs and reader
had no local changes.

The reviewed proposals are the
[private frontier review](review-2026-09-10-n11-strategy-frontier.md) and the
[parent-domain translation review](review-2026-09-10-n11-parent-domain-translation.md).
The
[parent-centre contract](../../../packing/cases/n11_five_dot_cover/unit-parent-centre-contract.md)
and its [independent review](review-2026-09-10-n11-parent-centre-independent-review.md)
specify the centre-preserving selection relation.

## Actual Unit Parents and Strict Margins

Let `r` be a unit vector, let `Jr=(-r_y,r_x)`, and put

$$
R_r(s)=[-s/2,s/2]r+[-s/2,s/2]Jr,\qquad S=|r_x|+|r_y|.
$$

The coordinate half-extent of `R_r(s)` is `sS/2` in both coordinates.
Thus closed containment of an old core `P=c+R_r(B)` in `[0,q0]^2` is equivalent to

$$
BS/2\le c_a\le q_0-BS/2\qquad(a=x,y).
$$

Set `B=9977/10000`, `q=q0+Delta`, `h=(Delta/2,Delta/2)`, and construct

$$
P'=P+h,\qquad U=c+h+R_r(1).
$$

Each coordinate wall margin of `U` is at least

$$
\frac{BS+\Delta-S}{2}
=\frac{\Delta-(1-B)S}{2}.
$$

The unit-ray identity gives

$$
1\le S\le\sqrt2<\frac32,\qquad
\frac32(1-B)=\frac{69}{20000}.
$$

Consequently, for every `Delta >= 69/20000`,

$$
\operatorname{margin}(U)
\ge\frac{1-B}{2}\left(\frac32-\sqrt2\right)>0.
$$

This establishes `U subset interior([0,q]^2)` even when an old core touched a wall and
even at equality in the stated threshold.
Also `P' subset interior(U)`: in the parent’s own axes, its four boundary margins are
`(1-B)/2>0`. The proof retains closed cores throughout.
It needs no perturbation, limiting argument, or positive margin in the old family.

This is stronger than satisfying the conservative necessary parent box.
Writing `T=||r_x|-|r_y||`, its admitted extent is

$$
e(r,d)=\max\left\{BS/2,\;1/2,\;\frac{S-Td}{2+d^2}\right\}\le S/2
\quad(0\le d<1).
$$

The three comparisons follow respectively from `B<1`, `S>=1`, and `-2Td<=Sd^2`. The
constructed parent has exact extent `S/2`, so it also survives the exact existential
parent domain after any loss in that lower-bound formula is removed.

For the 88-core family, `q0=191/50`, and therefore

$$
q\ge\frac{191}{50}+\frac{69}{20000}
=\frac{76469}{20000}=3.82345.
$$

## Folding, Source Cells, and Ties

Containment alone would not prove the nearest-selection assertion.
Its verification uses the actual retained orientations.

The
[88-core receipt](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/ceiling-family-191-50-independent-reader.json)
records the strictly increasing net

$$
t_j=\frac{207107j}{90000000},\qquad j=0,\ldots,180,
\qquad\theta_j=2\arctan t_j,
$$

and only indices `0,1,3,5,99,113`, together with their mirrors.
The largest used half-tangent is `23403091/90000000 < 1/3 < sqrt(2)-1`. Hence every used
nonzero folded node lies strictly between zero and `pi/4`. The terminal rational node
`t_180`, which lies beyond `tan(pi/8)`, is absent.

For an unreflected retained orientation, fold the constructed parent as prescribed in
the
[physical transfer](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-032/proofs/fixed-cover-transfer-review.md).
Its folded angle equals `theta_j` exactly.
Its distance to that node is zero, whereas its distance to every other distinct folded
node is positive. For a mirrored orientation the physical angle is `pi/2-theta_j`;
reflection folds it to the same `theta_j`. Undoing the same spatial fold on parent and
core returns `P'` with its original centre and orientation.

The record’s `t=1` entries represent the same square orientation as `t=0`, modulo a
quarter turn. The reader’s `fold` function performs precisely that canonicalization.
Any ambiguity between equivalent axis representatives therefore returns the same
geometric square. The conclusion concerns exact geometric orientation, rather than
requiring the selection routine to reproduce the literal half-tangent token `1`.

For each used interior index, the ordinary Voronoi seams are strictly on either side of
the node. In angle notation they are `(theta_(j-1)+theta_j)/2` and
`(theta_j+theta_(j+1))/2`. This is the same cell construction as
[adaptive.py](../../../packing/src/sqpack/fractional/adaptive.py), whose tangent seams
are `(t_(j-1)+t_j)/(1-t_(j-1)t_j)` and whose seam ties go to the lower index.
Neither a closed-cell convention nor a half-open seam convention removes an interior
node.
At index zero, the physical endpoint angle zero is admitted and uniquely nearest to
the zero node.

Thus every constructed parent has mismatch zero and belongs to its actual nearest-angle
source cell. A smaller permitted mismatch containing zero also admits it.
A physical angle subcell that excludes this node is a different restriction; this proof
does not put the parent in that subcell.
For canonical frames represented by several sources, the physical domain is the union of
their source domains, not their intersection.

The [independent reader source](../../../packing/devtools/independent_ceiling_reader.py)
implements the rational unit-ray formula, closed corners, source membership, and the
`t=1` canonicalization used here.
Its K0 test proves net-or-mirror membership; the additional physical-fold argument above
is needed for the new corollary.

## Point-Cover Consequence and Its Quantifiers

Let `D_iso(q)` be the set of cores produced by the specified concentric, side-`B`,
nearest-direction selection from individual unit squares contained in `[0,q]^2`. The
construction proves membership even in the version requiring parents strictly inside the
container:

$$
\forall\Delta\ge69/20000\quad\forall i\quad
\exists U_i\text{ individually admissible with selected core }P_i'.
$$

This supplies one parent for each fractional placement.
It does not supply an integral eleven-square packing, pairwise disjoint parents,
compatible owners, or completion of a particular core to an eleven-parent configuration.

The admitted 88-core family has weights `y_i=1/8`, total eleven, and closed point depth
at most one everywhere in its old container.
Since its placements are contained there, the depth is zero outside it.
Translation gives

$$
d'(x)=\sum_i y_i\mathbf1_{P_i'}(x)=d(x-h)\le1
$$

on the whole plane. For any nonnegative point measure `mu` charging every member of a
domain containing these translated cores by at least one,

$$
11\le\sum_i y_i\mu(P_i')
=\int d'(x)\,d\mu(x)
\le\mu([0,q]^2).
$$

This covers arbitrary point sites and continuous measures.
The closed-depth receipt already includes boundary intersections, so no exceptional
event sites are omitted.

No symmetry assumption on `mu` is needed when its coverage obligations include the full
reflected family, as `D_iso(q)` does.
A program imposing coverage only on the folded orientations still needs D4 symmetry of
the measure or an explicit equivalent transport argument.
The retained reader’s narrower folded-net theorem must not be silently reinterpreted as
an asymmetric folded-only theorem.

The obstruction therefore survives any domain that includes all individually realizable
selected cores. It also survives a union of complete source-cell refinements when one
common point cover must cover that union.
This does not imply that each separately conditioned angle-profile branch has the same
obstruction.

## A6 Extension

The independently admitted A6 family is the **64-placement** family
[`lane-a6-saturated-symmetric-153-40.json`](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-a6-saturated-symmetric-153-40.json).
Its
[point receipt](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-a6-independent-ceiling.json)
confirms `q0=153/40`, the same B and net, nonnegative weights totaling eleven,
containment, depth one, and D4 symmetry.
Its used folded indices are `0,1,2,3,5,27,116`, with mirrors.
The maximum used half-tangent is `6006103/22500000 < 1/3`, so the preceding
nearest-selection proof applies unchanged.
It follows that all these A6 cores have the constructed individually admissible parents
for

$$
q\ge\frac{153}{40}+\frac{69}{20000}
=\frac{76569}{20000}=3.82845.
$$

This also preserves A6’s mixed obstruction when **every effective threshold-atom site is
translated by h**. The
[atom receipt](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-a6-independent-atom-membership.json)
admits 2,566 orbits and 20,524 images; its source is bound separately in the
[admission record](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-a6-independent-source-record.json).
Translation preserves every closed site-core membership and hence every threshold
capacity inequality.
D4 conjugates under central translation, so symmetry and equal image charges also
persist. Nonnegative point weights and arbitrary nonnegative weights on those unchanged
effective atom images cannot yield budget below eleven.

Regenerating D4 images from **translated** seeds about the new centre is exactly this
transport. Regenerating from unshifted seed coordinates about a changed centre generally
changes the effective atoms and needs new capacity evidence.
New threshold atoms, weighted-token atoms, changed thresholds, and other charge rules
remain outside this result.
It makes no assertion about every later A6 loop family or the separate 280-placement
support bound.

## Exact Scope for the Research Queue

| Proposed change | Consequence of this review |
| --- | --- |
| Replace the conservative parent box by exact isolated unit-parent realizability | The translated obstruction remains. |
| Use exact nearest cells, tighter mismatch bounds containing the node, strict parent containment, or strict concentric core containment | The same zero-mismatch witnesses remain. |
| Add point sites or allow a continuous point measure | The everywhere depth inequality still bounds the budget below by eleven. |
| Refine the net while retaining these exact folded orientations at unchanged B and using nearest selection | The zero-distance selections remain; refinement alone does not remove the obstruction. |
| Reduce B while retaining the same centres, orientations, parents, and monotone point/threshold charges | Concentric smaller cores have no larger depths or threshold charges, so this also preserves the obstruction. |
| Increase B, remove or move the used net nodes, or change core placement or selection | New geometric or source-selection obligations arise; this result decides none of those changes automatically. |
| Require a named owner, its anchored mark/class, actual wall contact, a snug representative, or a genuine parent contact path | Additional conditions may exclude these placements; the construction establishes none of those conditions. |
| Require compatibility with a fixed residual, simultaneous owners, or completion to a physical packing | The existential single-parent witnesses do not establish joint feasibility. |
| Partition physical poses into separately routed conditional domains or demand different charges by angle class | A separate argument is needed for each cover and for complete routing; the common-cover obstruction does not decide that program. |
| Change atoms or charges | The 88-core result concerns point atoms. A6 additionally covers only its admitted atom images transported together with its placements. |

No mathematical correction is required to the private review’s 88-core corollary.
A durable statement should retain the full-versus-folded symmetry qualification, say
“same geometric orientation” at the `t=0/1` endpoint, and distinguish complete
individual-parent domains from extra conditions derived from owners, normalization, or
coexistence. The checked A6 source premises now justify its explicit extension above.
The frozen owner/residual comparison remains a separate conditional test.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
