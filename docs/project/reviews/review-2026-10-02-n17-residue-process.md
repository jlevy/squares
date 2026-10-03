---
title: n17 Residue Process
date: 2026-10-02
status: planning-review
---
# n17 Residue Process

**Session:** 168, BC-418, lane Q2. **Baseline:** `767e3066`, with the W7 and A
certificates pending in the
[certified-sub-patterns ledger](../../../packing/campaign/explorations/X048-session-168-pilots/certified-sub-patterns.yaml).
**Question:** after sub-pattern exclusion, 5,084 D4 orbits of n17 occupancy states
remain if the 44 flags of arity at most seven are all certified, and 2,256 with the 46
arity-eight flags.
How hard is each one, what does excluding it require, and what process
admits thousands of such exclusions when the first two each took a full independent
review?

This review designs that process from what n11 did with its own residue and what the two
n17 provers have done so far.
It changes no bound, verdict or frontier field.
Its one computation is a structural profile of the residue, made with the retained
selector’s exact consumer on one worker; the script and its log are in the session
scratchpad (`lanes/q2/residue_profile.py`, `near_endpoint.py`), outside the record for
the usual reason. Lane Q1’s survey of the residue (`survey_n17_residue.py`) had produced
no sample by the time this review closed; section 9 says what its sample must show.

## Summary

- **n11’s residue was 276 cases, each a full eleven-owner induction at one cap.** 273
  were plain sequential wall-seed nodes, one split once on a centre coordinate, and two
  inherited D4 halfplanes.
  The checker replay cost about 636 CPU-seconds per case; the producer’s cost is not
  published. n11 had no feasible-at-cap problem because its cap sat $2\times10^{-21}$
  above the endpoint.
- **The n17 residue is endpoint-shaped.** The sub-pattern engine removes 99.3% of the
  orbits at Hamming distance 10 from the endpoint’s state and 19% of those at distance
  2; under the 90 flags, 1,826 of the 2,256 survivors are within distance 6 of the
  endpoint, and 95 of the 117 one-square moves survive.
  The residue is where margins are thinnest, by construction.
  *Added 2026-10-02:* Q1’s survey does not bear that last clause out: in float search
  every sampled state is infeasible by at least $9.1\times10^{-3}$, and 43 of 44 by more
  than $10^{-2}$ (section “Q1’s Measurement”).
- **Structure, not margin, separates the two closures from the eight stalls.** The one
  wall-anchored chain (W7) closed under the kernel and defeated the branch and bound;
  the one all-interior crowd (A) closed under the branch and bound and defeated the
  kernel; every mixed pattern of two to four wall cells and three to four interior cells
  stalled under both, at margins from $6\times10^{-5}$ to $5\times10^{-3}$. Margin
  predicts branch-and-bound cost in the expected direction; the kernel’s cost is
  predicted by how many owners ever own a point.
- **Some residue states near the endpoint are probably feasible at the census cap**, and
  no sound certificate at $U=1169/250$ can exclude them.
  n11 had none because of its cap.
  n17 needs a cap ladder: every state is excluded at its own rational cap in
  $[S^{\ast},U]$, which the kernel’s frame already supports through `capture_cap`, and
  the near-endpoint states are treated as far leaves of the capture at the capture cap
  $U'$. This is a design, not yet a measurement.
  *Added 2026-10-02:* the measurement finds no support for the conjecture: 0 of 9
  sampled distance-2 states fit at $U$, the best penetration is $9.1\times10^{-3}$, and
  the 95% upper bound is about 27 of 95. The ladder stays as the thin-flag retry and as
  insurance; stage 5 may be empty.
- **The pipeline has six stages**, ordered by what each costs per orbit removed: the
  exact consumer, the selection of a minimal failing sub-pattern per surviving orbit,
  sub-pattern certification routed by structure, per-state seventeen-owner exclusion for
  orbits with no certifiable small sub-pattern, near-endpoint exclusion at $U'$, and
  capture. Each stage has one certificate kind, one independent checker and one admission
  rule, in section 5. *Added 2026-10-02:* Q1’s minimal failing sub-patterns are arity 8
  to 15, median 11, all new and never recurring, so the weight moves from stage 5.3 to
  stage 5.4.
- **Admission scales by promoting the two review-written verifiers to standing tools and
  reviewing by weight.** Every certificate gets an automated full re-check by a verifier
  that shares no code with its producer; a human reads the batch record, the controls
  and every certificate whose marginal removal exceeds 1% of the census; a 5% random
  sample is read as well.
  The ledger becomes a directory of per-certificate records with a generated index.
  *Added 2026-10-02:* the standing verifiers exist (commit `55656158`), the census
  requires a passing full verification for an admitted entry, and W7 and A are admitted
  under exp-249.
- **Cost, on today’s tools, is $4\times10^3$ to $4\times10^4$ CPU-hours**, dominated by
  per-state exclusions at 5 to 15 CPU-hours each.
  A compiled exact backend for the kernel’s collision and sweep steps would cut it by
  ten to fifty times. The critical path is not CPU: it is Q1’s residue sample, H-264’s
  per-state pilot and the capture pilot’s contraction rate, in that order.
  *Added 2026-10-02:* the totals stand and the shape changes: several hundred to about a
  thousand sub-pattern certificates of arity 8 to 15 at 2 to 9 CPU-hours each replace
  the 100 to 500 small classes, stage 5 falls to 0 to 150 states, and the first gate is
  passed.
- **Three measurements would end this route**: fewer than half of H-264’s sampled states
  closing within 2 CPU-hours; a contraction factor above $0.95$ at the $10^{-3}$ scale
  in the capture pilot; or more than about 10% of Q1’s sampled states holding a
  seventeen-square placement at the census cap.
  Section 8 names the fallback for each.
  *Added 2026-10-02:* the third did not occur (0 of 44 sampled states fit); the second
  occurred at the capture pilot’s row budget and the follow-up review reads it as
  producer-limited, with a second pilot specified; the first has two preliminary
  45-minute stalls from lane K2 and no verdict.

## 1. What n11 Did With Its Residue

Measured from the record; every number has a source.

n11’s 2,180 exclusions split into 1,904 *field* cases, excluded by 59 counting packets
of arity five to seven transferred by containment, and 276 *non-field* cases
([census contract](review-2026-09-29-n11-optimality-census-contract.md), lines 161–176).
The 276 are the residue in this review’s sense: cases with no forbidden sub-pattern
among the 59.

**What excluded them.** 273 were plain sequential wall-seed executions of the
ownership-induction kernel on all eleven owners; case 1383 split once, on owner 13’s
centred height at $4/3$, into two closed leaves that each reached contradiction; cases
2175 and 2176 inherited 72 and 73 necessary D4 centre halfplanes proved on the
baseline’s 253 survivors (lines 241–242 and 291–310). The certificate kind was the
generic node, `exact_generic_owned_hull_v1`, closed by `all_parent_poses_forbidden` or
`owned_hulls_intersect`
([PROOF.md](../../../packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md),
section 5). The checker was the frozen `audit_capture_v9.py` upstream and
`check_n11_generic_sequential.py` here.

**What it cost.** The final batch of 32 cases took 20,359 CPU-seconds, about 636
CPU-seconds each, with 4,409 complete updates and 336 million collision inequalities;
case 1383 took 2,111 CPU-seconds over its two branches; case 2129 alone took 22.6
seconds wall (lines 1133–1141 and 2358–2380). Those are checker replays.
The producer, which chose residual polygons, cores, collision regions, owner orders and
the one split, is not published, and its cost is the larger unknown
([capture feasibility review](review-2026-10-02-n17-capture-feasibility.md), lines
89–91).

**How it was admitted.** One reviewed checker, byte-pinned, replayed every case from its
source objects; the exclusion inventory was recomputed from eighteen batch summaries and
ten pilot bindings by exact disjoint union with an empty remainder (lines 2383–2395).
Admission was per batch, not per case: a batch was accepted when its checker and runner
were the reviewed ones, every execution exited zero, and every receipt identity matched
its earlier audit.

**The feasible-at-cap question did not arise.** n11’s cap $U$ satisfied
$U-T\approx2.1\times10^{-21}$ (PROOF.md line 131), so the only states holding packings
of side at most $U$ were the four D4 images of Trump’s mask, and those were the capture,
not the residue. The capture tree handled the region around the endpoint by three closed
branch predicates, with the three far leaves ending in contradictions and the near leaf
enclosed in the local rectangle (PROOF.md section 8).

## 2. The n17 Residue Today

**Counts, measured.** 346,104 states and 43,593 D4 orbits on
`ring-3-voronoi-8-tabbed-unique` at cap $1169/250$
([unique-state cover review](review-2026-10-02-n17-unique-state-cover.md)). The selector
flags 44 classes to arity seven and 46 more in a priority subset of arity eight
([X048 Session 168 receipts](../../../packing/campaign/explorations/X048-session-168-pilots/README.md)).
Two are certified and pending admission: W7 by the kernel
([W7 closure review](review-2026-10-02-n17-w7-closure.md)) and A by the branch and bound
([branch-and-bound certifier review](review-2026-10-02-n17-branch-and-bound-certifier.md)).
Those two alone leave 139,976 states and 17,690 orbits.

**Structure, measured here.** The residue profile in the scratchpad applies the
selector’s flags exactly and reads each surviving orbit’s representative:

| Flags applied | Orbits | Interior cells 3–5 | Corners 3–4 | Distance 2 | 4 | 6 | 8 | 10–12 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| none | 43,593 | 18,630 | 29,256 | 117 | 2,220 | 11,708 | 19,617 | 9,930 |
| W7 and A | 17,690 | 10,655 | 13,426 | 106 | 1,561 | 6,604 | 7,229 | 2,189 |
| 44, to arity 7 | 5,084 | 4,849 | 4,380 | 106 | 1,126 | 2,209 | 1,328 | 314 |
| 90, to arity 8 | 2,256 | 2,197 | 2,036 | 95 | 810 | 920 | 363 | 67 |

Distance is the Hamming distance between a 17-cell state and the nearest D4 image of the
endpoint’s state, so distance 2 is one square in another cell.
The endpoint survives every line.

Two readings follow.
First, the engine removes far states and spares near ones: under the 90 flags the
survival fraction is 0.7% at distance 10, 1.9% at 8, 7.9% at 6, 36% at 4 and 81% at 2.
Second, the survivors look like the endpoint: 97% have three to five interior cells (the
endpoint has three) and 90% have three or four corners occupied (the endpoint has four).
States with six or more interior cells, the crowds that A and C exclude, are nearly gone
(14 of 2,256).

**The thin flags.** Dropping every flag with best penetration below $10^{-3}$ raises the
2,256 to 2,350; below $3\times10^{-3}$, to 2,823. The selector’s 90 flags are heuristic,
and the two reviews found its best penetration overstated by 20–70% on both certified
patterns (W7: $1.1\times10^{-2}$ against $9.0\times10^{-3}$; A: $1.49\times10^{-2}$
against $8.8\times10^{-3}$), so the ten flags below $10^{-3}$ are the likeliest to be
placeable and the least costly to lose.

**What that means.** The 2,256 orbits are not a random sample of the census; they are
the states whose every small sub-crowd is placeable, which is what a state near a tight
packing looks like.
Their infeasibility, where it holds, comes from all seventeen squares
at once, and their margins at the cap are of the order of the cap’s own slack above the
endpoint, $4.7\times10^{-4}$, or smaller.
That is the regime in which both provers have so far stalled.

## 3. Difficulty Axes and What Predicts Cost

Every prover run on a flagged n17 pattern, from the receipts under
[`X048-session-168-pilots/receipts/`](../../../packing/campaign/explorations/X048-session-168-pilots/README.md):

| Pattern | Arity | Wall / interior cells | Best float violation | Kernel (64 bins unless noted) | Branch and bound |
| --- | ---: | --- | ---: | --- | --- |
| W7 | 7 | 5 / 2 | $9.0\times10^{-3}$ (review) | **closed**, 58 steps; producer 838 s, checker 930 s; saved objects re-checked in 27 min | unresolved at 30 min, 0.4% of the tree; Knuth estimate $2\times10^{5}$ (median) to $7\times10^{7}$ (mean) nodes at about 100 nodes per second |
| A | 6 | 0 / 6 | $8.8\times10^{-3}$ (review) | true stall at 32 bins after 609 s, round 8 equal to round 7 | **certified**, 41,598 nodes, 569 s; full independent re-check 1,531 s |
| B | 6 | 2 / 4 | $5.6\times10^{-3}$ | stall, round 1 equals round 0; four of six owners never own a point | unresolved at 10 min, 145,746 nodes |
| C | 6 | 0 / 6 | $2.0\times10^{-3}$ | stall at 16 bins | unresolved at 10 min, 67,925 nodes |
| P4 (a7-3) | 7 | 4 / 3 | $5.0\times10^{-3}$ | wall ceiling at 1,000 s; live rows flat from round 4 | unresolved at 10 min, 42,848 nodes |
| P5 (a7-4) | 7 | 4 / 3 | $2.5\times10^{-3}$ | certified stall, 1,085 s | unresolved at 10 min, 51,411 nodes |
| NW7 (a7-1) | 7 | 3 / 4 | $6.3\times10^{-5}$ | certified stall at 12 rounds, 1,223 s | unresolved at 10 min, 56,341 nodes |
| a7-5 | 7 | 2 / 5 | $1.4\times10^{-2}$ | not run | unresolved at 10 min, 48,299 nodes |

The best float violations are the selector’s except where a review’s own search found a
lower one; none is a bound.
Controls behaved: the endpoint’s own sub-patterns stall under the kernel and run the
witness path to the resolution floor under the branch and bound, and the two placeable
“W7 minus one cell” patterns stall under the kernel (W7 closure review, section 4).

The four axes the brief names, read against that table:

1. **Penetration margin at $U$.** It does not separate the closures from the stalls: A
   and W7 sit at the same $9\times10^{-3}$ and each closed under one prover and stalled
   under the other, while B at $5.6\times10^{-3}$ failed both.
   It does predict branch-and-bound cost in the expected direction once structure is
   fixed: a Farkas or disc closure needs the relaxation gap to exceed the margin, so the
   tree depth grows like $\log(1/\text{margin})$ and its width like a power of that, and
   the thinnest flags ($6\times10^{-5}$) would need a floor near $10^{-7}$. For the
   kernel the margin barely enters: an owner with no owned point contracts nothing at
   any margin.
2. **Arity of the minimal infeasible sub-pattern.** Both provers are exponential in it
   in the worst case: the branch and bound branches on $k$ angles, and the kernel’s step
   cost is rows times partner rows times facets over $k-1$ partners.
   The record has runs at arity six and seven only; arity eight is untested.
   For the residue states the relevant arity is whatever Q1’s shrink finds, and if it is
   17 the per-state route of section 5.4 applies.
3. **Wall chain against interior structure.** This is the axis that separates the
   outcomes. The kernel’s contraction comes from owned points, which come from one-sided
   wall bounds and from collision against a nearly pinned partner; the interior axis
   cells have circumradius about $0.52$ and own nothing from the cell alone (README,
   “The Kernel on Flagged Patterns”). So the kernel closes wall-anchored chains and
   stalls on interior crowds.
   The branch and bound closes interior crowds through disc and pair closures (10,032 of
   A’s 21,215 leaves are disc closures) and does not finish wall chains, where
   near-feasible poses slide along the wall and the angle dimension has to be resolved
   to the floor.
4. **Closeness to the endpoint’s state.** It predicts two things at once: thin margins,
   because a near-endpoint state can hold a packing only slightly worse than the
   endpoint, and the feasible-at-cap problem of section 4. Section 2 shows the residue
   is concentrated there.

**Per-prover predictors, cheap enough to run before every certification.** For the
kernel: run two rounds and count owners whose owned hull is non-empty; B stalled with
four of six empty, W7 closed once side-N0 owned points in round 4. For the branch and
bound: Knuth’s estimator, which the tool exposes as `--estimate N`, 150 to 300 dives in
minutes; it put A at $2\times10^{4}$ to $1.2\times10^{5}$ nodes (actual 41,598) and W7
at a median of $2\times10^{5}$ and a mean of $7\times10^{7}$, so its median is a useful
routing signal and its mean a warning.
Both predictors cost less than 5% of a certification attempt.

## 4. States That May Be Feasible at the Cap

**The problem.** The census cap $U=1169/250$ is $4.7\times10^{-4}$ above $S^{\ast}$. A
packing of side in $(S^{\ast},U]$ is not a counterexample, and no sound certificate at
cap $U$ can exclude the state it realises.
Which states those are is not settled by the record.
The first-order model of the
[kernel adaptation spec](review-2026-10-02-n17-kernel-adaptation-spec.md) (section 4.1)
says a configuration can move about $0.083$ in the softest direction, a rotation of
square 11, and about $0.02$ in stiff directions, while its side stays at or below $U$;
against that, square 13’s seam margin over the slider range is $0.002112$, square 9’s
$0.0238$ and square 16’s $0.0197$ to the nearest other cell (unique-state cover review,
section 4). The same review observes that the margin exceeds the container slack
$U-S^{\ast}$, which rules out a rigid translation crossing the seam but not a
coordinated move, and the [route review](review-2026-10-01-n17-route-after-pr265.md)
(lines 101–105) lists the dual coefficients only for the five softest directions, none
of which is a translation of square 13. Whether any one-square move is feasible at $U$
is therefore one exact LP per seam, or one witness search per distance-2 state, which is
what Q1 runs.
The 95 surviving distance-2 orbits are the candidates; a feasible one has a
float witness that an exact separating-axis check can confirm with margin.

**What n11 did.** It chose its cap so close to the endpoint that the question vanished;
the local theorem’s radii of $6.5\times10^{-4}$ and above dwarfed $U-T$, so every state
other than the candidate’s images was infeasible at $U$ with a margin the kernel could
find (capture feasibility review, section 1).

**What n17 must do.** The cap ladder.
An exclusion certificate at a rational cap $c$ proves that no packing of side at most
$c$ realises the state; the global theorem needs only $c\ge S^{\ast}$, because a packing
of side below $S^{\ast}$ embeds in every such container (PROOF.md, lines 143–151). So
each state may be excluded at its own cap, and a lower cap is never harder.
The cover is unaffected: its capacity-one property is a statement about the cells, not
the cap, and a packing in a smaller centred container is a packing in the $U$-container
whose centres the same cells cover.
The kernel’s frame already implements this: `make_frame` takes `capture_cap`, keeps the
cells in the $U$-frame and centres the wall bounds at $[(U-U')/2+h,\ (U+U')/2-h]$
(`sqpack/hull_kernel/frame.py`, lines 174–195), which is what the capture pilot uses at
$U'$, the exp-238 root box’s enclosure of $S^{\ast}$ rounded up to the $10^{-12}$ grid
(`pilot_n17_capture.py`, a lane’s uncommitted pilot, docstring).
The branch-and-bound tool reads its cap from the pattern (`cover.U`) and clips centres
to $[h,\ \text{cap}-h]$, so a lower cap there needs the same centring before it is
sound.

Three consequences for the pipeline:

- **Bulk at $U$, thin flags lower.** A wall-anchored pattern feels the cap through the
  container, so reducing the cap by $4.7\times10^{-4}$ raises its margin by up to that
  amount; for the flags below $10^{-3}$ that is a gain of up to an order of magnitude at
  no cost in theory, and it is the first thing to try before declaring such a flag
  false. An interior crowd like A sits $0.7$ from every wall and gains nothing.
- **Near-endpoint states at $U'$.** A state feasible at $U$ but not at $U'$ is excluded
  at $U'$, where the feasible set around the family has first-order $\infty$-radius
  about $2\times10^{-10}$ (kernel spec, section 4.1) and the unique-state margin
  $0.002112$ keeps every member of the family in the endpoint’s state.
  The certificate is a kernel node in the capture-cap frame that reaches contradiction:
  n11’s far leaves, which cost 66 to 494 seconds wall each (capture feasibility review,
  section 1), are the precedent, with the difference that n17’s far leaves are separate
  states rather than branches of one tree.
  Their cost depends on the contraction rate the capture pilot is measuring.
- **The embedding is fixed once.** The
  [composition review](review-2026-10-02-n17-local-half-composition.md) requires the
  global half to read the occupancy state with the packing’s lower-left corner at
  $(\sigma,\sigma)$, $\sigma=(U-S^{\ast})/2$. A packing so embedded lies in
  $[\sigma,U-\sigma]^2$, the centred container of side $S^{\ast}$, hence in the centred
  container of every cap $c\ge S^{\ast}$; exclusions on the ladder apply to it
  unchanged.

A proof that only the endpoint’s state is feasible at $U$, the third option the brief
names, is not available: it would need seam margins of at least the $U$-blob’s extent in
every direction, and square 13’s $0.0021$ is fixed by the slider range the family needs.

## 5. The Pipeline

Stages in the order they are applied, cheapest per orbit removed first.
A state leaves the pipeline at the first stage that excludes it; an orbit stands for its
eight images throughout, since every certificate transfers under D4 (W7 closure review,
section 2(e)).

| Stage | Input | Certificate kind | Independent check | Admission rule |
| --- | --- | --- | --- | --- |
| 1. Consumer lookup | the admitted ledger; the 346,104 states | none; an exact set union | a second implementation of the union, as both reviews’ `transfer_count.py` did by enumeration and inclusion–exclusion | counts agree; the endpoint survives; every entry passed the ledger’s checks |
| 2. Minimal sub-pattern selection | each surviving orbit; Q1’s survey | none; a queue of (class, best violation, orbits it would remove) | the endpoint’s own sub-patterns are never selected | not admitted; ordered by orbits removed per expected CPU-hour |
| 3. Sub-pattern certification | a class, a cap on the ladder, a prover chosen by structure | kernel: saved seed and node, digest-named; branch and bound: chunked certificate and manifest | the standing verifier of section 6, full mode | section 6’s rule |
| 4. Per-state exclusion | a surviving orbit with no certifiable sub-pattern of arity at most about 10 | a seventeen-owner kernel node at cap $U$, n11’s generic certificate; transfers only under D4 | the same verifier | section 6’s rule, plus the orbit representative’s identity |
| 5. Near-endpoint exclusion | the states Q1 finds feasible at $U$ | a kernel node in the capture-cap frame at $U'$ reaching contradiction | the same verifier; the endpoint control of the capture pilot on the endpoint’s own state | section 6’s rule, with the cap recorded per entry |
| 6. Capture | the endpoint’s state | a capture tree whose far leaves close and whose near leaf lies in the guard | the pose-inclusion check and the composition theorem of exp-248 | as n11: every leaf closed or enclosed; the frame map fixed as embedding A |

### 5.1 Lookup

[`census_n17_certified.py`](../../../packing/devtools/census_n17_certified.py) is this
stage. It refuses any entry whose receipt is missing, has the wrong digest, is not a
certified closure on this frame, certifies another class, lacks its saved objects, or
touches the endpoint’s state, and it reports every entry’s exclusion alone and at the
margin. Two additions are needed for the ladder and the verifier: a `cap` field and a
`verification` field per entry (section 6).

### 5.2 Selection

Q1’s survey searches a full seventeen-square placement in a surviving state and, when
none is found, shrinks the state to a minimal sub-pattern the search still cannot place.
The output per orbit is a class, its best violation and its arity.
Classes recur across orbits, and the queue is ordered by the orbits a class would remove
divided by its expected cost; the arity-eight receipt shows why: the top five
arity-eight classes carry 81% of that level’s gain and the last twelve nothing (README,
“Arity 8, a Priority Subset”). A state whose shrink reaches arity 17 without a placeable
sub-pattern, or whose search finds a placement, skips to stage 4 or 5.

### 5.3 Sub-Pattern Certification

Routing by section 3: a class with at least three wall cells goes to the kernel first;
an all-interior class goes to the branch and bound first; a mixed class runs the two
predictors and goes to whichever is cheaper, with both tried before the class is
declared uncertified.
Every attempt runs under a wall ceiling (OR-17): 30 minutes for the kernel at 64 bins
and one hour for the branch and bound, or a node budget from the Knuth median.
A thin wall-anchored flag that stalls at $U$ is retried at $U'$ before it is dropped.
A class that fails both provers at both caps is returned to the selector for a deeper
search, since a placeable pattern looks the same as a hard one.

The kernel’s mode B, the counting packet that n11’s 59 fields used (kernel spec, section
3.3), stays in reserve for wall-row patterns the induction stalls on.
It has a checker (`sqpack/hull_kernel/counting.py` and the mask-0 replay) and no n17
producer, so opening it is a build decision, taken only on evidence that induction
stalls on a class of wall rows that the queue needs.

### 5.4 Per-State Exclusion

This is n11’s non-field route: a wall seed on all seventeen cells of the state, uniform
bins, and owner updates until closure, with the row refinement and collision regions the
n17 kernel already has.
It is the H-264 instrument, and the hypothesis’s falsifier is the gate for this stage:
fewer than half of 10 to 20 uniformly sampled residue orbits excluded within 2 CPU-hours
each means the stage is unaffordable as built
([H-264](../../../packing/campaign/hypotheses/H-264-n17-geometric-exclusion-cost-per-leaf.md)).
n11’s precedent is encouraging in kind and silent on the producer: 273 of 276 cases
closed with no split, but with a producer whose cost and search policy are unpublished.
One split per case, on a bimodal residual, is within the grammar (the child node adds
one closed predicate, kernel spec section 1.4) and n11 needed it once in 276.

### 5.5 Near-Endpoint Exclusion

Section 4’s far leaves.
The producer is the capture pilot’s, which already refines rows and keeps the endpoint
control; the difference is the seed state and that closure, not guard inclusion, is the
goal. The number of such states is Q1’s to measure; the 95 distance-2 orbits are the
upper bound at distance 2, and some distance-4 orbits may join them.

### 5.6 Capture

Unchanged from the kernel spec’s section 4 and the capture review: one state, the guard
polygons of the local theorem at $r=1/5000$, the composition of exp-248. Its cost model
is 100 to 400 CPU-hours and its stop condition is $g>0.95$ at the $10^{-3}$ scale.

## 6. Scaling the Admission Process

Two certificates have been judged admissible, each by an adversarial review that wrote
its own verifier, a mutation harness and a transfer count, and each review found no
defect in the checker but set conditions on custody.
Thousands cannot have that.
What can be kept is the division those reviews made: the *grammar* is reviewed once, and
each *certificate* is re-derived mechanically by code that shares nothing with the
producer.

**The standing verifier.** The two review scripts, `lanes/r3/verify_cert.py` for kernel
objects and `lanes/r4/verify_cert.py` for branch-and-bound certificates, become retained
tools under the lint floor (OR-1), one per certificate kind, run in full mode on every
certificate before admission: all rows of every step for the kernel (about 90 minutes
for W7 on one core, W7 closure review, section 5), all nodes for the branch and bound
(1,531 seconds for A). The verifier writes a receipt naming the objects’ digests, its
own digest, the mode and the counts; the ledger entry cites it, and the census tool
refuses an entry without one.
The verifier’s independence is the admission argument, so its own review is the one
review that does not scale down: it is read once, mutation-tested once (the 26 and 16
unsound variants of the two reviews become committed tests, so a checker edit that loses
a refusal fails the gate), and re-reviewed when it changes.

**Pinned producers and checkers.** Each entry names the committed digests of its
producer, checker and verifier; the census tool keeps an allowlist of reviewed digests
and refuses any other.
A checker change triggers a full re-verification of every admitted certificate, which is
why the verifier’s cost matters: at 0.5 to 1.5 CPU-hours per certificate, a re-run over
2,000 entries is one to three thousand CPU-hours, affordable on a cluster and not on one
worker.

**Controls per batch, not per certificate.** A batch is a set of certificates produced
by one producer version at one cap with one settings record.
It runs with four controls at the same settings, each of which must *not* certify: the
endpoint’s own sub-pattern of the batch’s arity, a placeable class from the selector, a
“minus one cell” neighbour of one certified class, and for a cap below $U$ the control
that the endpoint’s state does not contract below its first-order blob at $U$. A batch
with a certifying control is refused whole, because a kernel that closes a placeable
pattern is unsound whatever its other certificates say.
The branch-and-bound review’s finding applies to every batch: witness-path controls are
blind to second-order relaxation errors, so the controls are necessary and the verifier
is the gate.

**Review by weight.** A human reads the batch record and its controls, every certificate
whose marginal removal exceeds 1% of the census (436 orbits), and a 5% random sample of
the rest. The reason is in the record: one false flag removed 171,604 states before the
deep stage was added (README, “H-267”), and W7 alone removes 16,701 orbits.
The sample catches a systematic defect in the producer’s outputs that the verifier would
share only if both were wrong in the same way, which the independence argument makes
unlikely but not impossible.

**The ledger.** A YAML file with two entries becomes a directory `certificates/<class>/`
holding `entry.yaml`, the producer receipt, the verifier receipt and the saved objects
or their manifest, with an index generated by the census tool rather than written by
hand. The per-entry marginal computation stays exact: with the union formed once, an
entry’s marginal removal is the set of survivors hit by no other entry, one pass over
the states per entry, seconds each.

**What a human still does.** Reads the verifier’s review, the batch records, the heavy
certificates and the sample; decides the cap ladder and the routing thresholds; and
reads the per-state and near-endpoint certificates for the first batch of each kind in
full, because those are new certificate shapes on this frame.

## 7. The Cost Model and the Critical Path

Unit costs are measured where a receipt exists and estimated by analogy otherwise; the
ranges are about a factor of three wide on each entry and the totals are
order-of-magnitude.

| Stage | Unit cost today | Count | CPU-hours today | With a compiled exact backend |
| --- | --- | ---: | ---: | ---: |
| 3, the 90 flags | kernel 0.3–0.5 h to close or stall; branch and bound 0.15 h (A) to over 100 h (W7); verifier 0.4–1.5 h; two provers under ceilings | 90 | 100–300 | 10–30 |
| 3, Q1’s new classes | 1–3 h each with verification | 100–500, Q1 | 100–1,500 | 10–150 |
| 4, per-state | producer and checker 3–10 h, by scaling W7’s 1,768 s by 2.7 partners and 2.4 steps per round; verifier 2–5 h | 500–2,000 | 2,500–30,000 | 100–3,000 |
| 5, near-endpoint at $U'$ | 10–50 h each if $g<0.9$, from the capture model’s 12 h per leaf at $r=3\times10^{-4}$ | 100–200 | 1,000–10,000 | 100–1,000 |
| 6, capture | 100–400 h | 1 | 100–400 | 10–40 |
| Re-verification on a checker change | 0.5–1.5 h each | all | 1,000–3,000 per change | 100–300 |

Totals: $4\times10^{3}$ to $4\times10^{4}$ CPU-hours on today’s Python kernel; on one
worker that is six months to five years, on 64 workers three days to four weeks, since
every unit is independent and runs under its own ceiling.
The compiled column assumes a ten- to fifty-times speedup of the kernel’s exact
collision-plane construction and sweeps, which the README names as most of the cost;
n11’s replay already used an integer homogeneous backend and a compiled sweep (kernel
spec, risk 5), and the repository has a Rust engine to put one in.
That column is an estimate with no n17 measurement behind it.

**The critical path** has four gates, and CPU is not among them:

1. **Q1’s residue sample**, which decides the mix of stages 3, 4 and 5 and whether any
   state is feasible at $U$. Days.
2. **H-264’s per-state pilot** on 10 to 20 sampled orbits, which decides whether stage 4
   is affordable at all.
   A week, most of it producer work.
3. **The capture pilot’s contraction rate** $g$, which prices stages 5 and 6 together.
   Lane C1’s pilot is at round 1 with no $g$ yet.
4. **The standing verifier and the batch ledger**, a build week, after which admission
   is a cluster job.

A compiled backend is on the critical path only if gate 2 passes at a per-state cost
above about 5 CPU-hours, where the stage-4 block alone exceeds $10^{4}$ CPU-hours.

## 8. Risks and Decision Points

| Measurement | Threshold | What it shows | Fallback |
| --- | --- | --- | --- |
| Q1: fraction of sampled residue states with a seventeen-square placement at $U$ far from the endpoint (distance above 4) | above about 10% | the census cap is too far above $S^{\ast}$ for the cover’s margins, and many states hold packings of side in $(S^{\ast},U]$ | lower the bulk cap toward $U'$ and re-run the selector there; those states are then infeasible by a margin the cap sets, and the cover needs no change |
| Q1: fraction of sampled states whose minimal failing sub-pattern has arity above 10 or best violation below $10^{-3}$ | above about half | the sub-pattern engine is spent; the residue is a per-state job with thin margins | stage 4 carries it, gated by H-264; if H-264 fails too, the route needs a second bulk engine, and the candidates are orientation-conditioned sub-patterns inside states, as n11’s angle rows were, or mode B packets |
| H-264: sampled residue orbits excluded within 2 CPU-hours | below half | the seventeen-owner producer stalls as the seven-owner one did on mixed patterns | producer work first: row splitting on bimodal residuals, finer bins, collision from partner covers at the seed; then a compiled backend; then a hybrid in which the branch and bound closes an interior sub-crowd inside a kernel node, which is new grammar |
| Capture pilot: $g$ at the $10^{-3}$ scale | above $0.95$, or more than 16 splits before $10^{-3}$ | the induction is the wrong engine for the near-endpoint region at any radius | the widened conditional theorem, which raises the capture target to about $10^{-2}$ in angles (capture feasibility review, section 5) |
| Any certified pattern or state that contains the endpoint’s state, or a batch control that certifies | one | a soundness failure in the producer or checker | stop admissions; the verifier’s refusal log is the first evidence |
| Thin flags: the ten below $10^{-3}$ fail both provers at both caps | all ten | they are placeable or beyond today’s provers | drop them; the residue rises from 2,256 to 2,350 orbits, which stage 4 absorbs |

The first two rows are the ones that could end the route rather than slow it, and both
are answered by Q1’s sample before any certificate is produced.

## 9. What Q1’s Sample Must Show

*Added 2026-10-02:* the sample landed after the review was committed; the section “Q1’s
Measurement” below reads it against these conditions, all of which it meets.

The survey had no sample when this review closed.
Its first `summary.md` must report, over a uniform sample of surviving orbits under the
90 flags with the sample size stated:

- how many sampled states hold a seventeen-square placement at $U$, with the witness’s
  exact separating-axis margin and the state’s distance from the endpoint; this is the
  stage-5 count and the first decision row above;
- for the rest, the arity of the minimal failing sub-pattern, its best violation, and
  how many sampled states it covers; the distribution over arity and violation is the
  stage-3 against stage-4 split and the second decision row;
- how often the same minimal class recurs across states, which sets the stage-3 queue’s
  value per certificate;
- the search cost per state, since the survey itself runs over 2,256 orbits;
- its positive control: the endpoint’s own state placed to a penetration far below the
  selector’s $10^{-6}$ margin.
  Q1’s first two probes at default settings reached only $2.1\times10^{-3}$ and
  $1.7\times10^{-3}$ on that state in 75 seconds each
  (`lanes/q1/probe-endpoint-default.txt`), so until the control passes, a state the
  survey cannot place says nothing about feasibility, and every “minimal failing
  sub-pattern” it reports is an artefact of search depth.

With those numbers the cost table’s three unknown counts (Q1’s classes, the per-state
count and the near-endpoint count) become measurements, and the pipeline’s next action
is the batch that the queue puts first.

## Q1’s Measurement

*Added 2026-10-02, after the review was committed (`f501ec08`).* Lane Q1’s survey landed
at `0e110249`: `devtools/survey_n17_residue.py`, the receipts
`receipts/residue-survey-arity8-seed1.json` and `residue-survey-calibration.json`, and
the section “The Residue Survey” in the
[X048 Session 168 README](../../../packing/campaign/explorations/X048-session-168-pilots/README.md).
It sampled 44 orbits surviving the 90 flags, stratified by corner and interior counts
and by distance from the endpoint, plus the endpoint as control; for each it searched a
full seventeen-square placement at $U$ and, failing that, shrank the state by deletion
to a minimal failing sub-pattern, confirmed by a second search.
Every number below is a float search result, planning evidence with the receipt’s own
status line: placements are witnesses, failures are searches that found none, and
minimal sub-patterns are candidates a prover must certify.
Section 9’s conditions are met: the control places the endpoint’s state blind, 3 of 6
seeds in one round and 6 of 6 by round 5, at penetration exactly $0$.

**Feasibility at $U$ is not supported.** No sampled state other than the endpoint’s fits
at $U$: 0 of 44, including 9 distinct states at distance 2. The best full-state
penetration is $9.1\times10^{-3}$, at a distance-2 state, and 43 of 44 exceed $10^{-2}$;
the sample’s worst is $7.1\times10^{-2}$. The 95% upper bound from a sample with no
placement is about 27 of the 95 distance-2 orbits and about 148 of all 2,256. This
changes section 2’s reading that the residue’s margins are of the order of the cap
slack: in float search they are at least twenty times larger, in the range where W7 and
A were certified. Section 4’s conjecture that some distance-2 states hold packings of
side in $(S^{\ast},U]$ finds no support; section 3’s fourth axis, closeness as a
predictor of thin margins, is not borne out by this sample.
The cap ladder keeps two uses: the retry of thin wall-anchored flags at $U'$, and
insurance for whatever the upper bound leaves open.
Stage 5.5 is now sized at 0 to about 150 orbits rather than 100 to 200, and may be
empty.

**Minimal failing sub-patterns are large, new and unrepeated.** Of 21 reductions, 19 are
confirmed by the second search; their arity runs from 8 to 15 with median 11, and their
best penetrations from $3.8\times10^{-4}$ to $1.6\times10^{-2}$. Every one is a new
class, absent from the selector’s 90 flags, and no class was found twice.
Certified together, the 19 would take the projected 2,256 orbits to 987; the largest is
an arity-8 north-wall crowd (corner-NW, corner-NE, side-N0, side-N1, side-N2, side-W2,
side-E2, interior-NW) at penetration $4.1\times10^{-3}$, deferred by the arity-8
priority subset, which alone removes 539 orbits; the rest remove 4 to 237 each, and the
median class about 40. Two readings follow for section 5. Stage 5.3’s queue has a head
worth certifying, since the top class is one certificate for a quarter of the residue,
and the sampling is size-biased toward exactly such classes, so later draws will remove
fewer. Past the head, a class of arity 11 to 15 that removes ten orbits is a per-state
certificate with fewer owners, so the weight moves from stage 5.3 to stage 5.4, and the
cost model’s stage-3 count of 100 to 500 classes becomes several hundred to about a
thousand certificates of arity 8 to 15, at a unit cost between the seven-owner and the
seventeen-owner figures.
Section 3’s second axis, arity, is now the cost driver: nothing of arity above seven has
been certified by either prover, and the branch and bound’s angle dimension at arity 11
is beyond its measured range.
The survey itself costs about 209 seconds per state for the full-state search, about
$3.3\times10^{5}$ seconds over the residue, and as much again for the reductions: about
180 CPU-hours to run stage 5.2 over all 2,256 orbits.

**The selector’s flags may include false ones.** The selector’s descent stops at 600
iterations and polishes only below $10^{-4}$, so on the endpoint’s own state it stalls
near $2\times10^{-3}$, where one long descent from its best pose places the state
exactly. Its flags with best penetration between $10^{-4}$ and $10^{-2}$ never had that
descent. Lane S2 is re-searching the 90 flags with a finish stage; until that lands,
section 2’s thin-flag sensitivities (2,256 to 2,350 without the ten below $10^{-3}$) are
a lower bound on what a false flag costs, and the selector’s penetrations stay search
results, not margins, as both certifier reviews said.

**Two per-state runs, preliminary.** Lane K2’s per-state pilot has run the
seventeen-owner kernel on two residue states, F1 at distance 6 and N1 at distance 4, at
32 bins under a 45-minute wall ceiling; the receipts are in the session scratchpad
(`lanes/k2/h-F1.json`, `h-N1.json`) and not yet committed.
Both are certified stalls at the producer’s time cap, after four to five complete
rounds: F1 after 94 steps in 2,473 seconds with 11 of 17 owners owning no point at the
seed and live rows nearly unchanged (corner-SE 32 to 23, side-E2 32 to 29, every other
owner at 32); N1 after 81 steps in 2,694 seconds with 14 of 17 owners owning nothing at
the seed and contraction beginning in round 3 (side-S2 and interior-S to 6 live rows,
side-S0 to 24, side-W2 to 25). Neither is a true stall in the sense of a round equal to
its predecessor, so neither decides H-264; what they show is that a seventeen-owner node
at 32 bins does not close within 0.7 CPU-hours, and that the owned-point predictor of
section 3 reads these states the way it read B: most owners own nothing from their
cells.

**What else changed since the review.** The capture pilot met its falsifier (commit
`cea300a4`; README, “The Capture Pilot”): position contraction $g=1.000$ at every scale
over 14 rounds and 224 certified updates at a $1/1024$ box, the turns contracting and
then stalling.
The [follow-up review](review-2026-10-02-n17-capture-after-pilot.md) reads
the result as producer-limited, at the pilot’s cap of 24 live rows per owner, and
specifies a second pilot; so section 7’s third gate has been measured once and not yet
decided. The standing verifiers of section 6 exist
(`devtools/verify_n17_kernel_certificate.py` and `verify_n17_bb_certificate.py`, commit
`55656158`), the census counts an admitted entry only with a passing full verification,
and W7 and A are admitted under exp-249.

**The cost model, revised.** The totals stand; the shape does not.
Stage 3 grows from 100 to 500 classes at 1 to 3 CPU-hours to several hundred to about a
thousand classes of arity 8 to 15 at 2 to 9 CPU-hours with verification, so 600 to 9,000
CPU-hours; stage 4 keeps whatever that leaves, which the two K2 runs put above 0.7
CPU-hours per state and H-264 has yet to price; stage 5 falls to 0 to 150 states; stage
2 adds about 180 CPU-hours of search.
The range $4\times10^{3}$ to $4\times10^{4}$ CPU-hours still holds, with the middle of
the range likelier than before.
The critical path is unchanged in order, with the first gate passed: no sampled state is
feasible at $U$, and the second gate, H-264, is the one the two preliminary stalls bear
on.

## Evidence Status

| Kind | Items |
| --- | --- |
| Measured by Q1’s survey (added 2026-10-02) | 0 of 44 sampled states placed at $U$; best penetration $9.1\times10^{-3}$; the 95% bounds; 21 reductions, 19 confirmed, arity 8 to 15; the 987-orbit projection; the control; the per-state search cost |
| Preliminary, uncommitted (added 2026-10-02) | K2’s F1 and N1 stalls at the 45-minute cap |
| Measured from the n11 record | the 1,904 and 276 split; the 273, 1 and 2 recipes; the batch and case costs; the admission by batch; $U-T$ |
| Measured from n17 receipts | every row of the prover table; the selector’s counts and penetrations; the Knuth estimates; the two reviews’ verification costs and mutation counts |
| Measured here, planning evidence | the residue profile: interior and corner counts, distance histogram, the 95 distance-2 orbits, the thin-flag sensitivities |
| Derived here, needing review | the cap ladder and its soundness argument; the routing rule and predictors; the admission design; the cost table’s scaling factors |
| Estimated by analogy | per-state and near-endpoint unit costs; the compiled-backend column; the batch control set |
| Conjecture | that some distance-2 states are feasible at $U$; that n11’s no-split rate transfers to n17’s per-state stage |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
