---
title: n17 Two-Child Collective Propagation
date: 2026-10-07
status: proposed
---
# n17 Two-Child Collective Propagation

The selected wider regional recovery pass and tiny-guard sensitivity test have both
completed at their declared fixed points.
The selected instrument therefore applies collective coverage in two complete centre
cases. The existing exp295 test recovered an owned set in each case and tested shared
owned points. It did not apply the later collective coverage argument.
The proposed test preserves that fixed split and checks what the stronger argument adds.

This is a sole-Astra hand composition and source contract, without independent
mathematical review.
Exp302 has now supplied a matching fresh finite result, summarized below; the remaining
sections retain the contract written before that target.
It is conditional on an accepted, complete `direct_regional` result from the
[one-round consumer](research-2026-10-07-n17-one-round-owned-domain-propagation.md).
No target geometry was evaluated while preparing the original contract.
The selected sequence is H308/exp300 on the wider 22-row premise, then a separately
preregistered H309/exp301 test on the stronger 25-row premise at $h=2^{-23}$ if exp300
is a complete fixed point.
Both use the existing one-round instrument.
A complete sensitivity miss selects this two-case implementation; a positive result
receives a new disposition first.
An incomplete run does not count as a fixed point or supply a new accepted base proof.
The two-case base remains the accepted wider regional proof; no tiny-guard domains are
substituted into it.

The trigger is now satisfied: exp300 and exp301 both have fresh matching complete
results, all 992 foreign rows and sixteen recoveries, zero additional interval loss,
zero new live-row deletions and no contradiction.
Their supervised wall times were 73.1934 and 107.6803 seconds respectively.
H310/exp302 then completed with both children open and full 992-row accounting in each.
After unioning their survivors, owner6, label3, is restricted to the closed half-angle
interval $[1/16,19/32]$, an additional parameter-length loss of $15/32$. Owner18’s
earlier $11/32$ loss is unchanged.
The supervised construction/fresh pair took 81.92 seconds.
The accepted wider exp300 proof remains the base; exp301 contributes no geometry to it.
The stronger per-case restrictions and selected next recovery contract are retained in
the
[case-preserving note](research-2026-10-07-n17-case-preserving-owned-propagation.md).

## Fixed Base and Exhaustive Cases

Use the accepted numeric-cap parent, its original frame and labels, and the directly
reconstructed owner0 guard of half-width $1/512$. The base proof retains all 992 foreign
closed row positions, including empty ones, and strictly owned groups $K_j$ for all
seventeen owners.
Its accepted exclusions give necessary centre domains $P_{jk}$ over the
original closed row intervals $I_{jk}$.

Freeze the exp295 choice, without running its selector again:

$$
j_\ast=18,\qquad m=471/250,\qquad
H_- = \{x:x_1\le m\},\quad H_+=\{x:x_1\ge m\}.
$$

Both halfplanes are closed.
Their common boundary belongs to both cases, and their union is the plane.
For $s\in\{-,+\}$ define

$$
P^s_{18,k}=P_{18,k}\cap H_s,\qquad
P^s_{j,k}=P_{j,k}\quad(j\ne18).
$$

Every physical packing under the base guard belongs to at least one case.
This fact does not require an intrinsic-diameter estimate or an assumption that either
case has a physical packing.
Exp295’s point-context diameter measurements and child domains are not regional inputs.
Recompute the two clips on the selected regional domains.

Preserve every row’s typed reference and closed interval.
A degenerate clipped polygon, including a segment or point on $x_1=m$, remains a domain.
An empty complete owner18 cover proves that case impossible; an empty individual row
does not.

## One Recovery and Collective Pass per Case

In case $s$, recover $K^s_{18}$ from all of its remaining owner18 poses using the
existing strict common-ownership construction with $\varepsilon=2^{-20}$. Freshly check
the resulting vertices against every live centre-domain vertex and every closed angle
interval. The other sixteen groups remain the accepted base groups:

$$
K^s_j=K_j\quad(j\ne18).
$$

Those groups remain strictly owned because each case only restricts the base packing
set. They do not need a new recovery.
In particular, owner0’s regional core and its ownership premise remain unchanged.

Check whether the newly recovered group intersects another strictly owned group.
Every nonempty closed intersection proves a contradiction in that case, including
singleton or segment intersections.
Precharge the exact intersection work; never discard vertices to fit a cap.
A closed case can stop at this complete contradiction, with its unperformed coverage
explicitly recorded.

For each case that remains open, perform one complete 992-row collective pass using the
frozen groups $K^s$. For each target row, let $D_{jk}$ be the unchanged strict
zero-centred square core throughout its closed interval.
The forbidden union is

$$
F^s_{jk}=\bigcup_{i\ne j}(K^s_i-D_{jk}).
$$

If $P^s_{jk}\subseteq F^s_{jk}$, delete that whole case-row.
Exact union coverage must check holes and degenerate domains; vertex membership alone
may only establish a negative shortcut.
Exclude self-owner obstacles.
Strict ownership of both summands justifies closed collision boundaries.

Recover the selected group before any coverage deletion in its case, and freeze it for
the entire pass. Do not feed one case’s deletions or groups into the other case.
Do not recover additional groups after a new deletion or run a second pass.

## Combine the Cases Before Measuring Progress

Let $\widehat P^s_{jk}$ be the surviving case domain, or empty if that case has a
complete contradiction.
The necessary parent-domain consequence is

$$
\widehat{\mathcal S}_j
=\bigcup_{s\in\{-,+\}}\ \bigcup_k
 I_{jk}\times\widehat P^s_{jk}.
$$

The union over cases is essential.
A restriction established in only one case cannot be applied to every packing under the
base guard. For each owner compute the exact closed interval union of rows surviving in
at least one noncontradictory case.
Compare its half-angle parameter length with the accepted base union.

The primary criterion is either a strict additional length loss for at least one owner
in this combined union, or complete contradictions in both cases.
The latter excludes the selected nonzero owner0 guard.
A contradiction in one case alone is retained as a case result, with the other case
still requiring its full proof.

For $j\ne18$, the two input row domains are equal, so a whole parent row disappears only
if both cases exclude it or are contradictory.
For owner18, the clipped halves must both disappear before its whole row is gone.
One surviving half remains a necessary centre restriction, but is not a complete row
exclusion. Report per-case row deletions and centre restrictions separately from the
primary combined interval loss.

The centre seam and all angle seams remain closed in the saved outer cover.
A boundary point can survive through either case or an adjacent live angle row.
Length loss does not establish a stronger boundary exclusion.

## Accepted-Premise Consumer

The proposed consumer is a new disjoint module and focused test file.
It must not modify the accepted exp295 source or re-run its selector.
Use an explicit descriptor with five byte-bound roles:

| Role | Purpose |
| --- | --- |
| `propagation_descriptor` | Selected wider regional one-round context and its complete input chain. |
| `propagation_certificate`, `propagation_replay` | Identical accepted mathematical payloads, fresh verification, complete `direct_regional` primary miss and no contradiction. |
| `selection_certificate`, `selection_replay` | Accepted exp295 proof of the historical fixed choice; use its owner/axis/midpoint only. |

Require the propagation mode `direct_regional`, the exact nonzero guard, inherited 1,056
original rows, all 992 effective foreign rows, all completed strict recoveries, and a
complete new collective pass.
Join every saved row decision to its original index, typed reference, interval and
live/empty state. The selected initial trigger has zero additional loss and no new
live-row deletion; retain those facts explicitly rather than accepting any record whose
status happens to be a miss.

Reconstruct the effective base domains from the byte-bound exp297 regional context and
the accepted prior/new exclusion flags.
Parse the accepted newly recovered groups from the one-round receipt, retaining their
explicit accepted-proof premise.
The consumer may inherit that complete proof instead of re-running the entire preceding
conditioning and propagation chain.
It must say so: new finite checks establish the two clips, selected-owner recoveries,
contradictions, collective coverage and combined unions, while the base domains and base
ownership remain accepted premises.

Bind the five top roles and the same finite named transitive custody roster as the
direct regional adapter.
Reject conflicting path/hash aliases and rehash all held inputs after computation.
Preserve the original container, canonical native object identities, labels, typed
parent references and original endpoint witnesses.
The new consumer never reads exp284 geometry.

The selection receipts must agree on the mathematical payload and contain owner18, axis0
and midpoint $471/250$. Their accepted original-parent identity must match the base’s
ancestry.
Their point-conditioned child polygons, owned sets and intrinsic diameter flags
are not copied into the regional proof.

A separate fresh process must reconstruct every new finite implication and match the
complete new payload.
It need not repeat the inherited base proof; source and receipt fields must distinguish
these assurance levels.
This composition remains conditional on the original parent and the reviewed hand proof
of the accepted regional premises.

## Resources and Controls

Propose 180 seconds per construction/fresh phase, 360 seconds combined, with one worker
and sampled 4 GiB current RSS per live process.
Use outer TERM at 360 seconds and KILL at 370. This is an allocation to test, not an
estimate that two new passes will finish.
Freeze the actual command and source only after readiness review.

The two children share the phase deadline and cumulative new-work counters.
Limits are prospective and must be registered before any child computation:

| Work | Fixed proposed limit |
| --- | --- |
| Artifacts and geometry | Descriptor 10 MiB; accepted/new receipts 64 MiB each; 4,096-bit used rationals; 1,048,576 parsed inherited vertices. |
| Closed centre clipping | 1,024 vertices per child row domain; 2,097,152 cumulative generated clip-output vertices. |
| Selected-owner recoveries | 2,048 output vertices per child; sixteen million cumulative support products, two million strict vertex pairs and eight million strict quadratic checks across both children. |
| New shared-owned intersections | Two million cumulative input vertex products, charged before each call; 4,096 vertices per output. |
| Both collective passes | Cumulative 2,097,152 Minkowski products on cache misses, 32 million point/facet charges and sixteen million prospective sweep-edge pairs; unchanged 4,096 vertices per region and 8,192 edges per sweep. |

Reuse the unchanged collective routine with its existing per-case limits of 1,048,576
Minkowski products, sixteen million point/facet charges and eight million prospective
sweep pairs. At most two calls imply the declared doubled cumulative limits; retain both
per-case and cumulative counts.
These per-case limits can refuse a workload that would fit the combined allowance, and
must be disclosed rather than silently relaxed.
The clip, recovery and intersection counters remain shared across both cases.
Per-case caches are allowed, but their work is included in the cumulative report.
Inherited base geometry is parsed once.
There is no new original conditioning, native parent replay or optional third case.
The exact sweep’s internal event products and unreduced integers remain outside
individual caps, so the deadline and outer guard remain material.
Resource exhaustion is incomplete; it cannot establish a mathematical miss or justify
using one finished child as a complete cover.

Target-free controls must cover:

- closed lower/upper clipping with their exact union, shared centre boundary and
  point/segment domains; empty one-case covers and both-case contradiction;
- unchanged original row identities, complete 992-row accounting in every open case, and
  inherited groups remaining separate from the freshly recovered selected group;
- strict ownership, singleton shared-owned contradiction, self-owner exclusion and an
  exact union with a hole that defeats a vertex-only positive test;
- one-child gain with no combined gain, gains on different rows in different children,
  positive combined loss, and one closed child with an unresolved surviving child;
- closed angle-seam retention, exact union-length subtraction, conditional regional
  flags, input tampering and all cumulative work stops;
- two clean processes reconstructing identical new proof payloads.

A complete criterion miss ends this fixed two-case test.
Do not choose a new midpoint or repeat the same propagation automatically.
Preserve the branch implications for a later complete-cover consumer, but distinguish
them from a parent-level interval gain.
Global optimality, ordinary census admission, unconditional parent exclusion and an
actual seventeen-square packing remain unproved unless their separate interfaces are
completed.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
