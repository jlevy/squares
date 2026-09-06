# BC-230 Source-Distinct Review

Status: conditional pass.
The adaptive-core lemma and certificate theorem are sound as stated.
BC-231 should correct the control oracles in Findings 1–3 before treating the matrix as
executable acceptance evidence.
No adaptive verifier or adaptive candidate exists yet, so this review approves a theorem
and proposed decision contract, not an implementation.

Review window: `2026-09-06T05:18:28Z` through `2026-09-06T05:33:28Z` (hard freeze)\
Review started: `2026-09-06T05:18:58Z`\
Review ended and frozen early: `2026-09-06T05:25:00Z`\
Cell: BC-230 (`think-c678`)

## Findings

1. **[Moderate] P5’s boundary oracle is too weak to detect lost boundary atoms.** The
   matrix requires the boundary mass to be at least the *smaller* of the two adjacent
   open-cell masses (`bc-230-control-matrix.md`, line 21). For a closed square and
   nonnegative weights, the boundary coverage contains the coverage from each adjacent
   open cell; the current sweep states this explicitly in `sweep.py`, lines 3–8. Thus
   the boundary mass must be at least the *larger* adjacent mass, and more directly it
   must equal the mass of the union of the atoms covered on the adjacent sides.
   A buggy boundary evaluator that drops every atom unique to the heavier adjacent cell
   can still satisfy the written `>= min(left,right)` oracle.
   Correct P5 to compare the boundary result with a direct closed-square membership
   calculation and require both equality to that calculation and
   `boundary_mass >= max(adjacent_masses)`. At a multiple-event intersection, take the
   maximum over every incident open cell.

2. **[Moderate] F4 and F5 do not isolate the named coverage and endpoint checks.** The
   contract fixes `q_0 = 0`, `q_{K+1} = 1`, and every interior seam from adjacent
   half-tangents (`bc-230-adaptive-core-contract.md`, lines 45–59), then requires each
   declared boundary to equal the derived rational (`bc-230-adaptive-core-contract.md`,
   lines 307–313). Changing a declared boundary to create F4’s overlap or gap, or
   changing F5’s endpoint fields, necessarily triggers F3’s derivation-mismatch refusal
   first under the prescribed gate order.
   Conversely, if every boundary equals its derivation and the endpoint and monotonicity
   checks hold, a gap or overlap is impossible: consecutive closures share the same
   derived `q_k`. These mutations show that malformed bytes are rejected, but they
   cannot show that a distinct folded-cover branch detects its named defect.
   Keep F3 as the serialized mutation.
   Replace F4 and F5’s endpoint cases with positive invariant assertions over
   independently derived seams (`q_0 = 0`, `q_{K+1} = 1`, `q_K < 1`, adjacent endpoints
   equal, and the union is `[0,pi/4]`), or test a pure cover validator directly on
   fabricated derived-cell sequences and say that this bypasses serialized-field
   validation. F5’s final-interior-seam case can remain a negative control if it changes
   the half-tangents, recomputes every dependent declaration, and reaches `q_K >= 1`
   while preserving the earlier format and ordering premises.

3. **[Moderate] T10’s atom-lightening branch can be refused before Condition 5.** T10
   says to lighten one atom at a known worst cell and expects a coverage witness
   (`bc-230-control-matrix.md`, line 66). Lightening one member of a nontrivial `D4`
   orbit violates T5, and leaving `total_mass` unchanged violates T8; leaving the old
   minimum also triggers T11. Any of those earlier refusals lets a verifier with a
   broken coverage sweep pass the mutation suite.
   Construct the mutation by changing every distinct member of one complete `D4` orbit
   by the same amount, updating `total_mass`, and declaring the independently known
   subunit minimum. Preserve nonnegative weights, total mass below `n`, and every format
   and geometry premise.
   Then require all three routes to return the same cell, center, and exact mass below
   one. The side-shrinking alternative is usable only with an independently fixed witness
   and updated cell fields; “so a reachable placement covers less than one” is a fixture
   precondition that the test must establish rather than assume.

4. **[Low] P2 does not freeze its first-worst-direction value.** P1 names direction `0`,
   while P2 asks only for “the same first worst direction” between the scalar and
   adaptive routes (`bc-230-control-matrix.md`, lines 17–18). That comparison detects
   specialization drift but permits a common ordering or tie-breaking defect to become
   the new oracle. Record the current scalar direction index in P2 and require both
   routes to equal it. This correction does not affect the theorem or the exact minimum
   `12501/12500`.

## Contract Determination

The following parts passed source-level review:

- **Quantifiers and closed cover.** The net has `K+1 >= 2` directions.
  The final pair brackets `pi/4`, the last seam lies strictly below it, and the derived
  closures run from tangent `0` to tangent `1`. The cells
  `[beta_0,beta_1], (beta_1,beta_2], ..., (beta_K,beta_{K+1}]` are disjoint and cover
  the folded arc. Interior seams belong to the lower index, while both adjacent closures
  remain available for containment bounds.
- **Rational geometry.** From `t_k = tan(alpha_k/2)`, the formulas
  `a_k = 2t_k/(1-t_k^2)`, `q_k = (t_{k-1}+t_k)/(1-t_{k-1}t_k)`, and
  `r(a,q) = |a-q|/(1+aq)` are exact.
  Endpoint maximization gives the stated rational `D_k`. The bracket and `q_K < 1` imply
  every relevant mismatch is below `pi/4`, hence `0 <= D_k < 1`.
- **Containment.** For every folded angle in a cell, the core’s coordinate half-extent
  is `B_k(cos(delta)+sin(delta))/2`. The inequalities
  `cos(delta)+sin(delta) <= 1+tan(delta) <= 1+D_k`, together with strict
  `B_k(1+D_k) < 1`, put the closed core inside the open unit-square interior.
  This is a sufficient conservative rule.
  The stronger squared rule is correctly separated as a future contract version.
- **D4 and zero weights.** The theorem needs invariance of the nonzero measure, with one
  serialized site per distinct orbit image and no stabilizer multiplicity.
  The separate requirement that a listed zero-weight site bring its whole zero orbit is
  correctly identified as presentation-domain validation, not measure invariance.
  T15 and P9 distinguish those cases.
- **Mass and coverage theorem.** Condition 5 quantifies over every admissible center at
  each selected direction.
  Strictly interior cores of interior-disjoint packed squares are disjoint closed sets.
  Nonnegative finite atomic mass is additive on their disjoint union, so mass at least
  `n` contradicts total mass below `n`. The exact event-cell reduction is justified
  because crossing an event can remove or add atoms, while an event boundary for a
  closed square only adds atoms relative to incident open cells.
- **Scalar specialization.** For the bracketed production nets, each interior endpoint
  mismatch is an adjacent half-gap; the folded endpoint mismatch is smaller than the
  final adjacent half-gap.
  Therefore `max_k D_k` is the current scalar `D`, and positive equal sides make the
  per-cell containment predicates equivalent to `B(1+D) < 1`. Condition 5 then uses the
  same directions, centers, side, atoms, total, global minimum, and first-tie ordering.
  The contract also correctly leaves noncanonical legacy nets on the unchanged scalar
  route rather than silently applying the stricter adaptive bracket.
- **Refusal boundary.** The schema separates bounded parsing, exact rational and integer
  validation, derived geometry, atom and symmetry premises, strict containment, the
  method ceiling, coverage, cross-route agreement, and frozen-byte identity.
  The ceiling guard `L > mB_0`, where `m` is the least integer with `m^2 >= n`, follows
  from separated closed axis-aligned cores.
  Equality is correctly left eligible by this guard alone.

Subject to Findings 1–4, the other matrix rows name an input mutation or route outcome
that reaches the stated premise and has a sufficiently specific oracle on paper.
That judgment is about control design; it is not evidence that BC-231 has executed any
row.

## Disposition and Required Follow-Up

**Conditional pass.** No correction is required to the adaptive-core lemma, the five
theorem conditions, the rational seam and mismatch formulas, the mass contradiction, or
the equal-side specialization for the stated production-net adapter.
Before BC-231 uses the control matrix as its acceptance gate, it should strengthen P5
and T10, recast F4/F5 so their asserted branch is actually exercised, and pin P2’s
existing first-worst direction.

BC-231 remains implementation work.
In particular, this review did not establish that the future project sweep accepts
per-cell sides, that the interval route maps reflected directions to the correct `B_k`,
that the standalone parser is independent, or that any three route outputs agree.
Those claims require the implementations and executions specified in the packet.

## Frozen Evidence, Cost, and Limits

Frozen author inputs, verified before review:

- `bc-230-adaptive-core-contract.md` SHA-256
  `7530f32b568c7b0b3b8b7fc28a56b3f2fe1c34c65ee0646b5ae2fd6a1579cee9`
- `bc-230-control-matrix.md` SHA-256
  `262029bf695937bf0af98e0b92cb7d94e714578861a0c128205164d6cfdc49b7`

The final review-file SHA-256 is computed after formatting and freeze and reported in
the coordinator handoff; embedding that digest in the hashed file would change the
digest.

Cost: one reviewer, no child agents; 6 minutes 2 seconds of active reviewer time from
the recorded start, ending 8 minutes 28 seconds before the hard freeze.
No scientific or numerical program ran.
Read-only evidence comprised the two frozen author files, agenda-025’s BC-230 contract
and implementation inventory, X-016’s proof boundary, and the local scalar certificate,
event-sweep, class-cell, retention-gate, standalone, and retained-fixture sources.

Limits: this was a bounded source review, not an execution audit.
I did not run any certificate sweep, interval calculation, fixture mutation, test suite,
or verifier; did not inspect network sources; and did not assess adaptive search
quality, performance, or the proposed kernel successor.
The review does not certify code that has not been written.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
