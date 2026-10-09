---
title: n17 Strict-Core Regional Transfer
date: 2026-10-07
status: proposed
---
# n17 Strict-Core Regional Transfer

A fixed strictly owned core can extend the accepted exp296 row exclusions to a nonzero
pose region without changing the foreign conditioned domains.
The new premise is that the same core remains strictly inside every owner-0 square in
that region. Once this is proved, the foreign-domain, common-ownership and collective
coverage arguments retain their original inputs and apply throughout the region.

This is a sole-Astra hand derivation and source-dependency audit, without independent
mathematical review or a new finite receipt.
The proposed explicit radius is $h=2^{-23}$, subject to the finite premise checks below.
It is a separate proposed test and does not change Session186’s first
[$h=1/512$ reconstruction contract](research-2026-10-07-n17-session-186-w3-strategy.md#first-regional-contract).
No new scientific values, margins or radius tests were evaluated for this note.

## Exact Pose and Core Premises

Use the accepted original numeric-cap parent, its physical unit scale $B=1$, its fixed
outer frame, and the accepted label-to-owner mapping.
All coordinates below are in that same frame; there is no additional rotation,
translation, rescaling or label permutation.
The centered numerical container remains the original $C(V)$ inside the outer $U$ frame.
The argument concerns packings already satisfying that parent and container.

Let the accepted matched owner-0 pose be $p^\ast=(c^\ast,t^\ast)$, with $t^\ast=53/128$.
This is the direct square half-angle chart used by the finite parent tools, not a
perturbation chart relative to the endpoint root.
Write

$$
u(t)=\frac{(1-t^2,2t)}{1+t^2},\qquad v(t)=(-u_y(t),u_x(t)).
$$

Let $Q_0$ be the exact polygon in the accepted exp293 point context’s `owner0_owned`,
equal to its `owned_groups["0"]`. Set $\varepsilon=2^{-20}$. The needed point-margin
premise is

$$
|u(t^\ast)\cdot(q-c^\ast)|\le\frac12-\varepsilon,
\qquad
|v(t^\ast)\cdot(q-c^\ast)|\le\frac12-\varepsilon
\quad\text{for all }q\in Q_0.
$$

The accepted source constructs these inequalities at half-width zero in
[`guard_owned` and `ownership_planes`](../../../packing/devtools/check_n17_guard_conditioned_ownership.py).
At a point angle, the rectangular sine/cosine bounds coincide with the exact unit axes.
Intersecting the resulting halfplanes with the outer frame preserves these bounds.
A new finite checker must verify the four signed inequalities directly on every retained
vertex, rather than infer the numerical margin merely from a function name.
Convexity then proves them throughout $Q_0$.

## An Explicit Regional Ownership Bound

For any $s,t\in[0,1]$,

$$
\|u(t)-u(s)\|_2^2
=\frac{4(t-s)^2}{(1+t^2)(1+s^2)}\le4(t-s)^2.
$$

The same identity holds for $v$. The point-margin premise also gives

$$
\|q-c^\ast\|_2^2
\le2(1/2-\varepsilon)^2<1.
$$

For $\|c-c^\ast\|_\infty\le h$ and $|t-t^\ast|\le h$, each of the two signed body-axis
projections is bounded by

$$
\begin{aligned}
|u(t)\cdot(q-c)|
&\le |u(t^\ast)\cdot(q-c^\ast)|
 +\|u(t)-u(t^\ast)\|_2\|q-c^\ast\|_2
 +\|u(t)\|_1\|c-c^\ast\|_\infty\\
&\le\frac12-\varepsilon+2h+2h.
\end{aligned}
$$

The bound for $v$ is identical.
Choose

$$
h=\varepsilon/8=2^{-23}.
$$

Both absolute projections are then at most $1/2-\varepsilon/2<1/2$. Thus every point of
the unchanged $Q_0$ lies strictly inside every owner-0 square in the closed guard

$$
G_h=\{(c,t):\|c-c^\ast\|_\infty\le h,
\ |t-53/128|\le h\}.
$$

The angle interval lies strictly inside $(0,1)$. All estimates include the closed
centre-box corners and closed angle endpoints.
The argument does not require every pose in the rectangular guard to fit the parent or
container. Its conclusion applies to the intersection of the guard with the original
physical packing set.
The declared guard has positive width; no nonempty family of seventeen-square packings
inside it is asserted.

## Which Proof Objects Can Be Reused

The exact source dataflow matters because a point-conditioned object cannot usually be
given a larger guard by changing metadata.
The relevant finite construction here separates its owner-0 diagnostic footprint from
its foreign necessary-domain argument:

| Source object | Dependence on the owner-0 pose | Regional treatment |
| --- | --- | --- |
| Original parent, root/cap/frame, labels and original foreign rows | The accepted parent is unguarded; `finite.extract` requires empty constraints/guard and no guard source. | Retain the accepted original premise and all custody joins. |
| Original foreign wall clipping and row cores | Depend on $U,V$ and each foreign row’s own closed angle interval. | Retain unchanged. |
| `guarded_owner0` output | Clips owner0’s original pieces to the exact point in exp293. | Do not transport it. It remains historical point calibration, not the new regional owner0 domain. |
| `condition_row` foreign pieces and hulls | Depend on the original foreign pieces, their strict cores, and $Q_0$. They do not otherwise use $c^\ast$ or $t^\ast$. | Retain once unchanged $Q_0$ is newly proved strictly owned throughout $G_h$. |
| Recovered foreign $K_i$ | `common_owned` uses every surviving foreign row domain and its own angle interval. | Retain unchanged, since their complete necessary pose domains remain valid. |
| Group0 used by collective coverage | Exactly $Q_0$. | Replace its point-only ownership premise by the new uniform ownership proof. |
| Exp296 forbidden regions and union coverage | Depend on these groups, each target’s own interval/core and conditioned row hull. | Reconstruct the finite collective proof on the same geometry, then compose it with the new ownership premise. |
| Matched point and endpoint controls | Establish the selected point’s parent membership and original endpoint retention. | Retain their accepted scope; separately prove the new guard is disjoint from endpoint owner0 charts. |

This audit follows
[`parent.intake` and `row_domain`](../../../packing/devtools/check_n17_partner_pose_coupling.py),
[`condition_context`, `condition_row` and `common_owned`](../../../packing/devtools/check_n17_guard_conditioned_ownership.py),
and the
[`collective` construction](../../../packing/devtools/check_n17_collective_row_coverage.py).
The original intake recovers the unguarded H289/H290 native final state and binds its
accepted same-object centered full replay.
It does not use the unaccepted exp284 child or the guarded trial’s augmented initial
owned-point sets as foreign centre restrictions.

To prove the transfer, take any physical packing in the original parent with owner0 pose
in $G_h$. Its owner0 square contains the unchanged $Q_0$ strictly.
For a foreign row with strict core $D_{ik}$, a centre in $Q_0-D_{ik}$ would produce a
shared strictly interior point and hence an overlap.
Therefore its centre lies outside that forbidden body’s interior, exactly the necessary
closed-complement condition used by exp293. Every retained outside-facet alternative and
the convex hull of their union still cover all physically possible centres.
The old foreign row domains remain necessary domains for this new guard.

Each old $K_i$ is strictly inside every square in those necessary row domains, so it is
still strictly owned by the actual foreign square.
Exp296’s union coverage then excludes the same owner18 rows, with their original closed
angle intervals. This argument uses no point-only owner0 centre clipping.
It replaces only the ownership premise on $Q_0$ and retains the full downstream chain.
It proves a regional necessary-domain restriction, not that $G_h$ is empty.

The original endpoint family has owner0 chart alternatives $0$ and $1$ under the
accepted fixed labels.
Both are disjoint from $[53/128-h,53/128+h]$. The old seventeen-square
endpoint-retention proof remains an inherited premise.
The new guard-disjointness check is finite arithmetic and must be recorded separately.

## Prospective Finite Consumer

A separate consumer can certify this transfer without modifying the first regional
instrument or any accepted receipt.
Root must allocate its hypothesis and experiment after source review; this note is not
registration.

Use three explicit byte-bound inputs: the accepted collective descriptor, its
construction receipt and its fresh receipt.
Follow that descriptor’s complete existing chain to exp293 and the original accepted
parent. Require matching full mathematical payloads, the accepted
`angle_union_restricted` outcome, the exact owner18 row roster 19–23 and 33–52, all 992
foreign rows, the original 1,056-row premise, all seventeen endpoint witnesses and
unchanged root/container/frame and canonical object identities.

In each new phase, call the existing collective checker to reconstruct all 992 finite
coverage decisions from the accepted exp293 geometry and compare them with exp296. This
rechecks collective coverage; it does not replay the original parent or rebuild the
point conditioning. Parse $Q_0$ and $c^\ast$ from the byte-bound point context, require
equality of the two stored owner0 group fields, positive area and the declared 32-vertex
bound. Check its point-margin inequalities exactly at every vertex.

For a finite ownership proof independent of numerical norm estimates, check every
retained $q$ and all four corners $c$ of the new centre box.
For $x=q_x-c_x$, $y=q_y-c_y$, $\sigma\in\{-1,1\}$ and $a=1/2-\varepsilon/2$, the two
numerator polynomials are

$$
f_{u,\sigma}(t)=(a-\sigma x)-2\sigma yt+(a+\sigma x)t^2,
$$

$$
f_{v,\sigma}(t)=(a-\sigma y)+2\sigma xt+(a+\sigma y)t^2.
$$

Require their exact minima on $[53/128-h,53/128+h]$ to be nonnegative, checking interval
endpoints and any interior stationary minimum.
The positive denominator $1+t^2$ and $a<1/2$ prove strict ownership.
For each fixed angle the inequalities are affine in both $q$ and $c$, so vertex/corner
checks extend to their entire convex domains.
This is at most 512 quadratic checks for the declared 32-vertex limit.
It directly verifies the claimed guard rather than trusting the Lipschitz calculation as
the only finite acceptance rule.

The primary finite criterion is complete accepted collective reconstruction plus these
uniform ownership checks, exact SAME25 identity, fixed $h=2^{-23}>0$, original endpoint
premises, new endpoint-family disjointness and fresh payload agreement.
A point-margin failure or a regional ownership failure refuses the proposed implication;
a resource stop is incomplete.
Do not shrink $h$ after failure without a new contract.

Retain these assurance distinctions in the result:

- New guard ownership and endpoint-family disjointness are checked now.
- All 992 collective finite decisions are reconstructed now on inherited geometry.
- Foreign point-conditioned domains are reused under the new fixed-core theorem; they
  are not newly generated regional domains.
- Original full parent, root and seventeen-square endpoint retention remain accepted
  premises.
- The same twenty-five row exclusions hold throughout the new guard; point
  contradiction, whole-guard exclusion, parent exclusion, census admission and global
  optimality remain false.

Proposed resources are 60 seconds construction and 60 seconds fresh reconstruction, one
worker, external TERM at 120 and KILL at 130 seconds, and sampled 4 GiB current RSS per
live process. Retain collective geometry and sweep limits unchanged, 10 MiB for the
descriptor, 64 MiB for each accepted finite receipt, and 4,096-bit used rational
geometry. The compact new output can be capped at 1 MiB: retain inherited proof
identities and new ownership minima rather than copying the six-megabyte collective
payload. Post-computation byte rechecks and serialization count against the clock.
These are prospective allowances, not a measurement of the new consumer.

Target-free controls must include all four centre corners, both signed axes, an interior
quadratic minimum, equality at the positive reserve threshold, zero reserve refusal,
tampered $Q_0$ equality or margin, changed guard width, missing original rows, shifted
frame/labels, missing endpoint controls, and two fresh processes with exact agreement.
A synthetic case must demonstrate that copying the old owner0 point footprint would
exclude nearby poses even though fixed-core transfer remains valid.

## Mathematical Payoff and Limits

This gives an explicit sufficient radius from an existing strictness margin and a small
finite test. It improves the previous existence-only compactness conclusion.
Its potential radius is much smaller than the first $1/512$ discriminator; it cannot
justify filling the entire owner0 domain with tiny boxes.
A successful receipt would establish one reusable regional implication and validate an
analytic proof interface, while leaving the guard complement and surviving owner18 rows
open.

For a larger useful guard, fresh regional conditioning can establish ownership
implications where the fixed point core no longer remains owned.
With nested guards and these exact constructions, enlarging the guard shrinks its owner0
core, enlarges the foreign necessary domains and can only weaken the common owned sets.
The first direct reconstruction seeks a rule that applies over a larger region; it does
not promise stronger groups than the point context.
The enlarged-$K_i$ domain-inclusion method in the W3 is another possible quantitative
continuation if fixed-core transport is too narrow.
Choose between these approaches using their declared mathematical payoff and measured
cost; avoid a sequence of shrinking radii whose only outcome is another isolated patch.

## One Propagation Round on an Accepted Context

The next propagation consumer can use the accepted exp296 point context, an accepted
direct regional reconstruction, or the foreign domains justified by the fixed-core
transfer. These are different premises and must be selected explicitly before a run.
Using the transferred foreign domains retains the new guard’s uniform ownership premise
on the unchanged $Q_0$; it does not reinstate the old point-only owner0 footprint.

For foreign owner $j$, retain every original closed row interval $I_{jk}$, reference and
centre domain $P_{jk}$. Mark a proved excluded row empty rather than joining neighboring
rows or changing their intervals.
The necessary pose cover is

$$
\mathcal S_j=\bigcup_{k:\,P_{jk}\ne\varnothing} I_{jk}\times P_{jk}.
$$

Every physical pose under the selected context must remain in this union.
Its angle projection is the union of the surviving closed intervals, which is a safe
outer necessary restriction.
In particular, a shared seam can survive through an adjacent row even after another
incident row is excluded.
The saved union does not assert stronger boundary exclusion.
Its length is measured in the half-angle parameter, not radians.

First recover all foreign common owned sets from the complete surviving covers.
For every vertex of a recovered set, independently check strict ownership over every
surviving centre-domain vertex and the whole associated closed angle interval.
Keep owner0’s $Q_0$ fixed.
Then perform one simultaneous collective coverage pass over all 992 original foreign row
positions, using only these recovered groups and excluding self-owner collisions.
Newly deleted rows must not alter groups during this pass.
Empty rows, singleton seams and all coarse square6 rows retain their original
identities. The same nonoverlap implication that justified exp296 proves each new
deletion; the recovery step is sound because every actual foreign pose remains in its
complete cover.

The primary progress discriminator is strict additional exact closed-interval-union
length loss for at least one owner, compared with the selected accepted input, or a
separately checked complete contradiction.
A contradiction needs either an empty entire owner cover after complete accounting or a
shared strictly owned point after every participating group has been justified.
It inherits the selected context’s point or regional scope.
A completed noncontradictory pass with no further length loss misses this discriminator;
unfinished construction or fresh checking is incomplete.

Record new row deletions separately from union-length loss.
Deleting a row whose angle interval is redundantly covered can change the necessary pose
cover while leaving its projected interval union unchanged.
A row-deletion fixed point therefore means no new row was deleted, not merely zero
measured length loss.
Do not repeat an unchanged fixed point.
A later changing round, if selected, must use the newly accepted cover and retain its
ancestry; this note does not authorize automatic iteration or predict its cost.

All original endpoint-retention premises remain intact.
The point or regional guard is still disjoint from the endpoint family; this conditional
pruning rule cannot enter the unconditional census.
Neither a successful round nor the closed-union representation supplies a larger radius
or a complete global guard cover.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
