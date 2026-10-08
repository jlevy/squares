---
title: n17 One-Round Owned-Domain Propagation
date: 2026-10-07
status: proposed
---
# n17 One-Round Owned-Domain Propagation

The accepted exp296 exclusions remove alternatives from a foreign square’s necessary
pose cover.
Recovering owned sets from the remaining alternatives can strengthen the next
collective collision argument.
This note specifies one recovery followed by one simultaneous whole-row coverage pass.
It does not authorize repeated propagation.

The mathematical composition is a sole-Astra hand derivation and source audit, without
independent mathematical review or a new finite receipt.
Its inputs are the accepted point exp296 proof, or that same proof under an accepted
[fixed-core regional transfer](research-2026-10-07-n17-strict-core-regional-transfer.md).
The latter remains prospective H307/exp299 when this contract is written.
No new scientific geometry, recovered set or coverage predicate was evaluated for this
note.

## Selected Premises and Scope

Use the original numeric-cap parent, fixed labels, outer frame, unit scale $B=1$ and
centered container $C(V)$ already joined by exp293 and exp296. The original parent and
root proofs remain accepted premises.
The new consumer does not use exp284’s unaccepted child, rebuild a producer seed, change
a square’s label or alter the container.

Two input modes are allowed in this first contract:

| Mode | Required accepted implication | Scope of every new deletion or contradiction |
| --- | --- | --- |
| `point` | Exp296 construction/fresh agreement on the original exp293 point geometry. | Owner0 has exactly the matched centre and $t=53/128$. |
| `fixed_core_regional` | The same accepted exp296 geometry, plus a fresh accepted H307 fixed-$Q_0$ transfer at $h=2^{-23}$. | Owner0 lies in the transfer’s exact closed centre/angle guard. |

The regional mode inherits the transferred foreign necessary domains.
It must not copy the historical owner0 point footprint as a regional constraint.
Owner0’s unchanged $Q_0$ has the new uniform ownership proof in this mode.
Original seventeen-square endpoint retention remains inherited, and the selected point
or guard remains disjoint from the endpoint family’s owner0 charts.

A direct $h=1/512$ regional receipt has a different domain construction.
Admitting it as a third input mode requires a separately reviewed adapter; it is outside
this first contract.
Root selects the actual input mode and registers its byte identities before any new
recovery or coverage evaluation.

## Mathematical Invariant

For each foreign owner $j$, retain the original closed row intervals $I_{jk}$, typed
references and convex necessary centre domains $P_{jk}$. There are 992 foreign row
positions in total: 32 for coarse square6 and 64 for each other foreign square.
Preserve their order and interval endpoints even when a row becomes empty.

Let $E_j$ be the set of rows already excluded by the accepted collective proof, and set

$$
P^-_{jk}=\begin{cases}
\varnothing,&k\in E_j,\\
P_{jk},&k\notin E_j.
\end{cases}
$$

Every physical packing under the selected context has its owner-$j$ pose in

$$
\mathcal S^-_j=\bigcup_{k:P^-_{jk}\ne\varnothing} I_{jk}\times P^-_{jk}.
$$

This is an outer necessary pose cover.
Its angle projection is a union of closed intervals.
A seam can remain through a surviving neighboring row even when another incident row was
excluded. The saved projection must retain that seam; it does not assert stronger
exclusion at an interval boundary.
Interval lengths below are in the half-angle parameter, not radians.

Recover $K^+_j$ so that it lies strictly inside every square with pose in
$\mathcal S^-_j$. Keep $K^+_0=Q_0$. These are simultaneous consequences of the already
accepted cover, before any new row deletion.
For a target row $I_{jk}$ let $D_{jk}$ be its strict zero-centred common square core.
Then

$$
F^+_{jk}=\bigcup_{i\ne j}\bigl(K^+_i-D_{jk}\bigr)
$$

contains only centres whose target square must overlap another square under the selected
context. Indeed, $y=q-d$ gives the point $q=y+d$ strictly inside both squares.
If $P^-_{jk}\subseteq F^+_{jk}$, the complete row can be deleted.
The union is over different source owners; self-owner collisions are excluded.
Degenerate owned sets and closed collision boundaries are valid because both ownership
premises are strict.

The proof is not circular: all $K^+_i$ use $P^-$, and every new coverage check uses the
same frozen groups. No deletion discovered during the pass is fed back into recovery.
If all rows of an owner disappear, its necessary cover is empty.
A shared strictly owned point between two fully justified groups also gives a
contradiction. Both conclusions retain the selected point or regional scope.

## Exact Recovery and Source Boundaries

Reuse the retained exact functions in
[`guard`](../../../packing/devtools/check_n17_guard_conditioned_ownership.py) and
[`collective`](../../../packing/devtools/check_n17_collective_row_coverage.py).
The consumer should be a new module, provisionally
`check_n17_owned_domain_propagation.py`, with disjoint focused tests.
Existing accepted modules remain unchanged.

For every foreign owner with a nonempty surviving cover, call `guard.common_owned` once
with all original row positions and their $P^-_{jk}$. It starts from $[0,U]^2$ and uses
the existing margin $\varepsilon=2^{-20}$. More explicitly, for each live row, each
corner $(c,s)$ of its exact closed sine/cosine enclosure and each signed axis
$n\in\{\pm(c,s),\pm(-s,c)\}$, impose

$$
n\cdot q\le\frac12-\varepsilon+
\min_{x\in P^-_{jk}}n\cdot x.
$$

The support minimum is attained at a retained domain vertex.
Bilinearity in the axis coefficients and affine dependence on $x$ make these corner
constraints sufficient throughout the rectangle and convex centre domain.
As in the existing source, fresh closed-arc quadratic checks must independently
establish strict ownership for every output vertex against every surviving centre-domain
vertex. Empty recovered groups are allowed; an empty owner pose cover is a different,
contradictory condition.

The same bounding polygon and margin make the ideal recovery operator monotone under row
deletion: removing alternatives can only enlarge its output.
Preserve this as a synthetic invariant test.
It does not replace fresh ownership checks or supply a runtime speed estimate.

After all groups are recovered, check for a shared strictly owned point in lexicographic
owner-pair order.
Any nonempty exact closed intersection counts, including a singleton or
segment.
Precharge each pair’s input vertex product against the new consumer’s cumulative
intersection limit before invoking the exact intersection primitive.
The existing `guard.shared_owned` records these products but does not itself enforce
such a cumulative limit; do not silently treat its counter as a guard.

If no earlier complete contradiction holds, call `collective.construct` once on the
unchanged $P^-$ snapshot and the fully recovered groups.
This accounts for all 992 row positions, uses each row’s entire original closed
interval, preserves holes through exact union coverage, and retains every noncovered
domain unchanged. There is no partial centre clipping, angular refinement, new core
recipe or optional second pass.

## Input Contract and Fresh Verification

Use a new descriptor schema, provisionally `n17-owned-domain-propagation-context/v1`,
with an explicit `mode`. Each input role has a path and byte digest.
These byte joins identify accepted external proof artifacts; source/version control
remains Git’s role.

| Descriptor field | Required meaning |
| --- | --- |
| `schema`, `mode` | Exact schema and one of the two declared modes; reject extra or missing roles. |
| `collective_descriptor` | Accepted exp296 context and all inherited guard/route-selection inputs. |
| `collective_certificate` | Exp296 construction receipt with the exact selected 25 row identities. |
| `collective_replay` | Accepted fresh receipt with identical mathematical payload. |
| `transfer_descriptor`, `transfer_certificate`, `transfer_replay` | Required only in regional mode; accepted H307 fixed-$Q_0$ proof referring to exactly the same three collective inputs and guard. |

In each phase, verify the prior collective proof exactly once.
Point mode calls `collective.check`. Regional mode calls the future transfer checker,
whose contract already calls `collective.check` once; do not add a second full
collective check. The new consumer must compare the selected prior construction/fresh
payloads and preserve all inherited parent, container, label, endpoint and canonical
object joins.

Then use `collective.intake` to obtain the same byte-bound point geometry and groups.
This repeats bounded intake and geometry parsing, not the original parent proof or a
second collective pass.
Keep every touched input in a held-byte roster and recheck it after computation.
In regional mode, verify that the transfer’s core is exactly the same inherited
`owner0_owned` and `owned_groups["0"]`; its guard and uniform ownership premise are part
of the selected context.

Before pruning, join every inherited coverage decision to the corresponding original row
index, typed reference, interval and nonempty-domain flag.
Require the complete owner roster, all 992 foreign positions, the accepted SAME25
owner18 exclusions and the full original 1,056-row premise.
Apply every prior proved row exclusion, including already-empty rows; never infer
additional exclusions from the old interval union alone.

Compute the closed interval union of the surviving nonempty $P^-_{jk}$ for each owner
and require exact equality with the prior collective receipt’s saved surviving union.
This is the new pass’s baseline.
It prevents counting the old $25/64$ loss again.
Reconstruct every new owned group, contradiction test and coverage decision in a fresh
process, and require equality of the complete new mathematical payload.
No newly written owned set or boolean is accepted solely because the producer saved it.

The fresh phase does not replay the original native parent, root, old point conditioning
or endpoint proof. It checks the new finite implications on accepted premises.
The regional mode additionally rechecks the finite fixed-core transfer, while relying on
its stated hand-composition theorem.

## Output and Acceptance Contract

Use a distinct receipt schema, provisionally `n17-owned-domain-propagation/v1`. Retain
the following fields or equivalent explicit fields with the same meaning:

| Field group | Required content |
| --- | --- |
| Context | Mode, exact matched point or transferred closed guard, $Q_0$ identity, original parent/container/labels and accepted input roles. |
| Prior restriction | All 992 row identities, prior exclusion flags, effective live/empty state and baseline closed interval unions. Geometry may be referenced through the checked prior inputs. |
| Recovery | All seventeen groups, unchanged owner0 core, all foreign recovery/strictness checks completed, work counts and output vertex counts. |
| Contradiction | Exact kind and witnesses: complete empty owner cover, or lexicographically selected nonempty intersection of strictly owned groups. No invented coverage checks after an earlier contradiction. |
| Collective pass | Full original row order, all new finite decisions and regions, complete row accounting, and explicit simultaneous recovered-group scope. |
| Progress | Additional excluded live rows, before/after closed interval unions, exact additional parameter-length loss per owner and whether any entire owner cover is empty. |
| Assurance | New finite reconstruction, inherited original geometry/proofs, context-specific implication flags, fresh agreement, limits and all post-computation byte checks. |

Strip or replace the reused collective routine’s point-only labels.
Its `original_owned_sets_unchanged` means unchanged during that routine’s pass, but the
new consumer has just recovered different groups.
Report `recovered_groups_frozen_during_collective_pass=true` and
`groups_recovered_from_prior_surviving_cover=true` instead of implying that no recovery
occurred.
The target centre domains remain unchanged during the pass except for whole-row
deletion.

The primary criterion is either:

- strict additional exact closed-interval-union length loss for at least one owner,
  after complete new recovery and coverage; or
- a freshly checked complete contradiction under the selected context.

For a covered live row, a new deletion is counted only if it was not already empty in
$P^-$. Each owner’s new interval union must be contained in its baseline union, and
every reported length difference must be nonnegative.
A contradiction found by shared owned sets follows complete recovery; collective owner
emptiness follows complete 992 row accounting.
An already-empty input owner would itself be a prior contradiction and must be refused
as inconsistent with the selected noncontradictory exp296 premise.

A complete pass with no additional length loss and no contradiction is
`criterion_missed`. Keep new row deletions as a separate diagnostic.
The current `parent.closed_rows` grammar requires each interval to start at the previous
endpoint and have strictly positive width.
Thus its interiors are disjoint: deleting any live row in this particular target
necessarily lowers union length.
Shared seams can remain in neighboring rows, but there are no singleton or duplicate
chart rows in the admitted roster.
In a more general overlapping cover, row deletion could leave projected length
unchanged; such a control belongs at the interval-union helper level and does not expand
this input grammar.

A resource stop is `incomplete`; a malformed or inconsistent premise is `refused`.
Neither is a negative mathematical result.
No success is accepted until the separate fresh phase agrees.

Use context-specific proof flags.
A point contradiction does not imply a nonzero regional exclusion.
A transferred regional contradiction applies only to that exact guard.
Every outcome keeps unconditional parent exclusion, ordinary census admission, new
global side bound, optimality and a seventeen-square counterexample false.
Original endpoint retention is inherited; conditional endpoint retention is not required
because the context is disjoint from the endpoint family.

## Frozen Resource Recommendation

Accepted exp296 took about 13.70 seconds for construction and 14.18 seconds for fresh
reconstruction, 28.14 seconds supervised.
Its input groups had already been recovered; those measurements do not time the new
recovery. Accepted exp293’s complete point conditioning/recovery took about 75 seconds
per phase, but its costs were not separated enough to predict this new consumer.
Larger recovered groups may also increase the next coverage cost.

Allocate 180 seconds for construction and 180 for the independent fresh phase, including
prior proof reconstruction, intake, byte checks and output.
Use one worker, outer TERM at 360 seconds and KILL at 370, and sampled 4 GiB current RSS
per live process. This is a prospective allowance, not a forecast.
There is no automatic retry with larger limits after an incomplete result.

| Resource | Proposed fixed limit |
| --- | --- |
| Descriptor and accepted finite receipts | 10 MiB descriptor; 64 MiB per accepted receipt; 64 MiB new output. |
| Used geometry | 4,096-bit rationals; inherited 1,048,576-vertex parsing ceiling; no new root-coordinate arithmetic. |
| Row domains and groups | 1,024 domain vertices; 2,048 vertices per recovered foreign group; fixed inherited owner0 core at most 32 vertices. |
| Recovery supports | Sixteen million point-normal products across the full new recovery. |
| Fresh strict ownership | Two million point/centre vertex pairs and eight million exact quadratic checks across the full new recovery. |
| Shared-owned intersections | Two million cumulative input vertex products, precharged before each call; at most 4,096 vertices in any output intersection. |
| New collective pass | Existing limits: 1,048,576 Minkowski products on cache misses, 4,096 vertices per region, sixteen million point/facet products, 8,192 edges per sweep, eight million cumulative prospective sweep-edge pairs. |
| Prior collective reconstruction | Its own unchanged accepted limits, counted and reported separately from the new recovery and new collective work. |

The recovery and collective clocks share the phase deadline.
Their counters remain separate rather than silently resetting a single total.
Ordinary exact hull/clipping and sweep routines do not independently cap every unreduced
integer product, internal sweep event or trusted intersection operation; the explicit
input/output/work limits, cooperative deadline and outer supervisor remain material
safeguards. An old source counter without a corresponding refusal is not an enforced
limit.

## Target-Free Controls and Next Decision

The source controls must establish:

- exact original row/ref/interval matching, missing/duplicate row refusal, coarse
  square6 coverage, prior-exclusion application and equality with the saved baseline
  union;
- retained closed seams in the admitted strict partition, plus helper-level singleton
  and overlapping-interval union controls; reject those broader row shapes at the
  original-parent intake boundary;
- recovery from the complete prior cover, strict closed-arc ownership on all remaining
  alternatives, monotonic recovery under row deletion, allowed empty groups and refusal
  of a purported already-empty input owner;
- no use of a new deletion during recovery or the same collective pass, unchanged owner0
  core, self-owner exclusion and exact union coverage rather than vertex-only
  acceptance;
- a positive additional interval-loss fixture, a complete miss, shared singleton-owned
  intersection, whole-owner emptiness and correct point/regional scope flags;
- all new resource refusals, accepted-input tampering and two clean processes with exact
  payload agreement.

After a verified positive pass, compare the new row deletions and group growth with
their actual cost before selecting any later pass.
A complete pass with no new row deletions is a fixed point of this specified
recovery/deletion operator.
It is not a feasible packing, nor a reason to abandon stronger coupling.
In this strict partition, zero additional length loss also implies no new live-row
deletion; a future overlapping cover would require the two diagnostics to be
distinguished.

This consumer tests whether the accepted conditional restriction generates further exact
consequences before adding another branch or pose split.
A regional implication still needs a complete guarded-cover composition to affect the
global theorem; neither one successful round nor finite-height termination provides that
cover or a proof completion estimate.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
