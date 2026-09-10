# The Retained Point Obstruction in the Individual-Parent Domain

**September 10, 2026. Verdict: exact analytic consequence of admitted inputs.** The
retained 88-core point family at side `191/50` can be translated so that every core is
the exact nearest-selected concentric core of an individually contained unit square at
every side

```text
q >= 76469/20000 = 3.82345.
```

Its total weight and depth do not change.
It therefore remains a mass-eleven obstruction to point-only covering certificates on
the fixed core side and retained direction net.
Replacing the old core-centre box by either the conservative necessary parent box or the
exact individual-parent domain at `q = 3.827` cannot improve T-026.

This is a proof review, not a target measurement.
It supplies no physical packing, no new lower bound, and no obstruction to changed
threshold atoms, larger cores, contact or owner conditions, joint compatibility, or
conditional certificates.
The independently reviewed
[unit-parent centre bound](review-2026-09-10-n11-parent-centre-independent-review.md)
supplies the necessary-domain formula.
A separate
[independent realizability review](review-2026-09-10-n11-parent-realizability-independent.md)
reconstructed the stronger individual-parent argument, including the source-cell and
endpoint cases. The retained
[ceiling reader](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/ceiling-reader-191-50.md)
supplies the weighted family and its exact depth decision.

## Objects and Quantifiers

Let `r = (r_x,r_y)` be a unit core direction and set

```text
S = |r_x| + |r_y|,
T = ||r_x| - |r_y||.
```

For core side `B` and the admitted maximum angular mismatch `D`, every nearest-selected
core from a physical unit square has its centre in

```text
[e(r,D), q-e(r,D)]^2,
e(r,D) = max(B*S/2, 1/2, (S-T*D)/(2+D^2)).
```

This necessary restriction applies before any owner selection.
The point obstruction uses the 88 placements in the retained family at

```text
q0 = 191/50,
B = 9977/10000.
```

The independent reader verifies exact total weight eleven, exact depth at most one, the
retained directions and reflections, and D4 symmetry.
Those are source facts for the argument below; this review does not recompute them.

## Translation Proof

The three terms in `e` are all at most `S/2`:

- `B*S/2 <= S/2` because `B < 1`;
- `1/2 <= S/2` because a unit vector has `S >= 1`;
- `(S-T*D)/(2+D^2) <= S/2` because `T,D >= 0`.

Hence `e(r,D) <= S/2` for every retained direction.

Increase the container side by `Delta` and translate every old core by
`(Delta/2,Delta/2)`. An old core had coordinate wall margin at least `B*S/2`, so the
translated core has margin at least

```text
B*S/2 + Delta/2.
```

It lies in the necessary parent box whenever

```text
B*S/2 + Delta/2 >= e(r,D).
```

The bound `e(r,D) <= S/2` makes it sufficient that

```text
Delta >= (1-B)*S.
```

For a unit vector, `S <= sqrt(2) < 3/2`. Therefore the rational condition

```text
Delta >= (3/2)*(1-B)
      = (3/2)*(23/10000)
      = 69/20000
```

is sufficient for every direction at once.
At equality the comparison with the true maximum `sqrt(2)` is still strict.
Adding this increment to `q0` gives

```text
191/50 + 69/20000 = 76469/20000 = 3.82345.
```

## Exact Individual Parents

Write the old core as

```text
P = c + [-B/2,B/2]r + [-B/2,B/2]Jr.
```

After the central translation, give it the concentric unit parent

```text
U = c + (Delta/2,Delta/2) + [-1/2,1/2]r + [-1/2,1/2]Jr.
```

Each coordinate wall margin of `U` is at least

```text
(Delta - (1-B)*S)/2.
```

At `Delta = 69/20000`, this is strictly positive because `S <= sqrt(2) < 3/2`. The
translated core is also strictly inside `U`, with parent-axis margin `(1-B)/2`. This is
an explicit parent construction, rather than an inference from the conservative centre
box.

The retained 88-core family uses only folded net indices `0,1,3,5,99,113` and their
mirrors. Give each parent exactly its core’s physical orientation.
Folding that orientation lands on the retained node at distance zero, so ordinary
nearest-angle selection returns the same geometric square.
The two endpoint tokens `t=0` and `t=1` represent the same square orientation modulo a
quarter turn. Half-open Voronoi seam conventions do not remove a net node from its own
source cell.

The quantifiers are

```text
for every translated core i, there exists an individually admissible parent U_i.
```

They do not say that the parents are pairwise disjoint or jointly realizable.
Uniform central translation preserves point depth and total weight.
Thus any nonnegative point measure charging every core in a domain containing these
translated placements has total mass at least eleven.
This covers arbitrary point support, including continuous measures.

On a folded-only domain, this conclusion applies to D4-symmetric point covers or after
an explicit symmetry transport.
On the full reflected domain, it applies without a symmetry assumption because every
translated placement is explicitly present.

## What the Argument Does Not Transfer

The 88-core family violates one of T-025’s two-of-three capacity rows.
Translating it does not make it a feasible obstruction to the mixed threshold program.
The result says nothing about a changed threshold family or a floor atom.

The A6 family supplies a different fixed-family obstruction.
Its 64 admitted placements use folded indices `0,1,2,3,5,27,116` and their mirrors, so
the same exact-parent and nearest-selection construction applies at every

```text
q >= 153/40 + 69/20000 = 76569/20000 = 3.82845.
```

That calculation preserves A6’s existing threshold incidences when all atom sites move
with the placements about the new centre.
It obstructs the unchanged A6 atom family at `3.83`; it does not cover regenerated atoms
about a new centre or another charge rule.

The construction survives a refinement that retains the used net nodes, a smaller
mismatch allowance that still contains zero, and a smaller concentric core at the same
centres and orientations.
It does not automatically survive a larger B, removal or movement of the used nodes, a
physical angle subcell excluding a node, or a domain defined by contact, ownership, or
simultaneous parent compatibility.
The unit parent itself does not scale under T-026’s dilation, so the old dilation proof
cannot simply be relabeled as a parent-domain proof.

## Planning Consequence

Do not allocate a point-only LP at `3.827` merely to replace the conservative box by
exact isolated-parent realizability on the retained B and net.
Its answer is already determined by this admitted fractional family.
Productive tests must change at least one premise: the atom family, core side or net,
necessary domain, or conditional selection rule.

This removes one redundant experiment from the queue.
It does not rank the remaining directions by mathematical promise and does not close the
broader parent-geometry program.
The saved exp151 owner escape still tests a stronger conditional restriction: whether
the fixed residual and a selected anchored owner remain compatible with their necessary
parent domains. The individual-parent construction proves none of those owner or joint
conditions, so that bounded target remains distinct.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
