---
title: n17 Case-Preserving Owned-Domain Propagation
date: 2026-10-07
status: proposed
---
# n17 Case-Preserving Owned-Domain Propagation

Exp302 proves a further regional pose restriction after splitting owner18’s centre into
two closed cases. The next proposed step uses the new restrictions within each case to
recover owned sets, then performs one collective coverage pass in each case.
It preserves the existing two-case cover and does not introduce another split.

The new composition below is a sole-Astra hand derivation and source contract, without
independent mathematical review or a new target result.
H313/exp305 is reserved for a separately registered finite test.
Accepted exp302 arithmetic and its fresh replay are premises; they do not establish the
proposed propagation outcome.

## Accepted Result and the Information to Preserve

[Exp302](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-302-two-child-collective-propagation/README.md)
completed construction and fresh reconstruction with identical mathematical payloads.
Its two cases are

$$
x_{18}\le471/250,\qquad x_{18}\ge471/250.
$$

Both remain open. Each complete collective pass accounts for all 992 foreign row
positions. After unioning the two cases’ survivors, owner6, which is label3, has the
necessary closed half-angle interval

$$
t_6\in[1/16,19/32].
$$

The additional parameter-length loss is $15/32$. Owner18 retains its earlier $11/32$
loss, with necessary closed union

$$
[0,19/64]\cup[3/8,35/64]\cup[13/16,1].
$$

These lengths are in the half-angle parameter, not radians.
They cannot be added to obtain a measure of excluded joint configurations.

The case-specific data are stronger than their combined projections:

| Accepted case | Owner6 live row indices | Owner18 live row indices |
| --- | --- | --- |
| $x_{18}\le471/250$ | 24–31, giving $[3/8,1/2]$ | 24–28, giving $[3/8,29/64]$ |
| $x_{18}\ge471/250$ | 4–37, giving $[1/16,19/32]$ | 0–18, 24–34 and 52–63, giving the earlier closed union. |

The lower case’s recovered owner18 group has 38 vertices; the upper case’s has 68.
Construction took about 42.42 seconds and fresh reconstruction 39.31 seconds; the
supervised pair completed in 81.92 seconds.
Those measurements cover the selected-owner recovery protocol, not the proposed
all-owner recovery cost.

Every conclusion retains the accepted parent, centered container and owner0 guard at
$h=1/512$. The original seventeen-square endpoint-retention control remains inherited;
that endpoint family is disjoint from this guard.
Neither case was excluded, and the ordinary census, global bound and global capture
claim remain unchanged.

## Two Necessary Covers, One Complete Case Split

Let $\Omega$ be the physical packing set under the accepted original parent and the
fixed regional guard.
Let $\Omega_-$ and $\Omega_+$ impose the two centre inequalities.
Then $\Omega=\Omega_-\cup\Omega_+$; their intersection on the splitting plane is
intentional.

For each sign $s$ and foreign owner $j$, the accepted exp302 result gives a necessary
pose cover

$$
\mathcal S^s_j=\bigcup_k I_{jk}\times P^s_{jk}.
$$

The complete original row intervals and typed references are retained.
A previously excluded row has $P^s_{jk}=\varnothing$. For owner18, the remaining domains
also retain the corresponding closed centre halfspace.
For every other owner, the original regional domain remains unchanged when its row
survives. A boundary pose may belong to adjacent rows or both centre cases; every
surviving occurrence must remain in the necessary cover.

Recover all sixteen foreign groups $K^{s,+}_j$ from this fixed snapshot, keeping
$K^{s,+}_0=Q_0$. Each new group must lie strictly inside every square represented by
$\mathcal S^s_j$. Use the existing exact rectangle-corner recovery with
$\varepsilon=2^{-20}$ and independently check its output vertices through the closed-arc
quadratic inequalities.
The geometry and margin are unchanged from the reviewed
[one-round contract](research-2026-10-07-n17-one-round-owned-domain-propagation.md).

All groups are recovered before any new deletion.
Empty recovered groups are valid and provide no collision information.
An empty necessary pose cover instead contradicts that entire case.
Any nonempty closed intersection of two strictly owned groups also contradicts the case,
including a shared point or segment.

If the case remains open, perform one complete simultaneous collective pass using

$$
F^{s,+}_{jk}=\bigcup_{i\ne j}(K^{s,+}_i-D_{jk}),
$$

where $D_{jk}$ is the existing strict zero-centred core for the complete closed row
interval. Covering all of $P^s_{jk}$ by this union excludes the row.
The union is over different source owners; self-owner collisions are forbidden.
Exact union coverage must preserve holes and degenerate domains.
No newly deleted row feeds back into a recovery or another coverage check during this
pass.

This is a composition of accepted necessary covers and new finite implications.
It does not assume that a represented pose extends to a physical seventeen-square
packing. All new implications remain conditional on the case in which their owned groups
were proved. Combining owned groups from different cases would be unsound.

## Combining the Outcomes

For each owner, union the surviving closed row intervals across both cases.
A closed case contributes the empty set.
For an original row position, the combined live flag is the logical OR of its two
surviving flags. Compare this union with exp302’s already accepted combined union, not
the original $[0,1]$ interval.

The primary criterion is either:

- strictly positive additional exact half-angle union-length loss for at least one
  foreign owner after combining both cases; or
- complete contradiction of both closed centre cases, which excludes the declared
  regional guard under the accepted parent.

A positive deletion in one case need not give combined gain.
Closing one case also does not suffice if the other contributes the entire previous
union. Record case-specific deletions, redundant seam deletions and one-case closure as
secondary results without changing the primary criterion.
The earlier losses of $15/32$ for owner6 and $11/32$ for owner18 are baseline premises
and cannot be counted again.

A complete no-gain result ends this fixed round.
Resource exhaustion, failed custody or an unfinished case is incomplete or refused, not
a mathematical miss.
No automatic second recovery, new centre cut or midpoint selection follows.

## Accepted Inputs and Fresh Consumer

Implement a new disjoint module `check_n17_case_preserving_owned_propagation.py` and its
focused tests. Freeze three byte-bound input roles: `cases_descriptor`,
`cases_certificate` and `cases_replay`. Require exp302’s exact accepted schema, declared
two-case positive status, fresh verification, complete mathematical payload equality,
same parent/container/guard, full endpoint-control identity and both open cases with
complete 992-row collective receipts.

The new consumer may call the existing two-child `intake` once to obtain the accepted
exp300 base domains, groups and named transitive custody roster.
This is structural validation and bounded geometry parsing; it does not replay the
inherited exp300 or exp302 proof arithmetic.
Retain that distinction in the receipt.

For each case:

1. Join all original row references, indices and closed intervals to the accepted base.
   Reconstruct owner18’s fixed halfspace clipping and require exact equality with its
   saved `selected_owner_clipped_rows`; all other owner domains remain the base domains.
2. Check the complete accepted case collective decision roster against these domains.
   Apply its whole-row deletions, then require exact agreement with every saved
   `surviving_rows` flag.
   Do not infer those flags merely from a combined interval.
3. Join the accepted selected-owner group and the unchanged other groups to their
   premise records. New recoveries use the case-specific pruned domains, with unchanged
   $Q_0$. They do not use exp295’s point-conditioned geometry or exp301’s tiny guard.
4. Complete all new recoveries, strict checks, contradiction checks and any required
   collective pass. Retain full 992-row identities even when many domains are empty.

Recompute the accepted combined baseline from the two inherited survivor rosters and
require equality with exp302’s saved combined restrictions.
Recompute the new combined union from the new case results.
A fresh process independently reconstructs every new finite implication and compares the
complete new payload.
All named accepted files are checked again after computation; source integrity remains
Git’s responsibility.

## Frozen Resource Proposal and Controls

Allocate 180 seconds to construction and 180 seconds to fresh reconstruction, with a
360-second outer TERM and 370-second KILL. Use one worker and sampled 4 GiB current RSS
per live process. These are proposed limits, not an estimate that both rounds finish.

| Resource | Proposed bound |
| --- | --- |
| Intake | 10 MiB descriptor, 64 MiB per accepted/new receipt, 1,048,576 parsed inherited vertices, 4,096-bit used rationals. |
| Domains and groups | 1,024 vertices per row domain; 2,048 per recovered foreign group; 32 for unchanged $Q_0$; 4,096 per intersection output. |
| New halfspace reconstruction | 2,097,152 cumulative generated clip-output vertices across both cases. |
| Both all-owner recoveries | 32 million support products, four million strict vertex pairs and sixteen million quadratic checks, shared across both cases. |
| Shared-owned contradiction checks | Four million input vertex products, charged before each nonempty pair intersection. Empty groups consume no intersection work. |
| Each collective pass | Existing limits unchanged: 1,048,576 Minkowski products, sixteen million point/facet charges, eight million prospective sweep pairs and 8,192 edges per sweep. |
| Both collective passes | At most 2,097,152 Minkowski products, 32 million point/facet charges and sixteen million prospective sweep pairs. |

The per-case collective limits remain stricter than the combined allowance for an
unbalanced workload.
Disclose both rather than silently relaxing the existing source.
The sweep’s internal event products and unreduced arithmetic remain outside individual
caps; its phase deadline and outer supervisor remain material.

Synthetic controls must cover all 992 typed row joins; the shared centre plane and
closed angle seams; loss of correlation under an invalid flattened cover; one-child gain
with no combined gain; genuine combined gain; both-case contradiction; old losses
excluded from the new baseline; strict singleton intersections; empty groups versus
empty pose covers; self-owner exclusion; no sequential feedback; resource refusals;
input tampering; and clean two-process reconstruction equality.

Global optimality, ordinary assignment exclusion, census admission and an actual packing
remain false scope flags.
A successful regional contradiction would still need a complete global capture or
complementary-region proof to affect the global theorem.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
