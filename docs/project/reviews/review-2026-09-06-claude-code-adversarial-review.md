---
title: Adversarial Review of the s(11) ≥ 381/100 Explainer
description: An adversarial review of the published explainer for the new lower bound on eleven unit squares in a square, and of the verifiable-claim documents it links to. The theorem and certificate hold. The page's own presentation of the argument has gaps, and the review lists every one, with fixes.
author: Claude Code
---
# Research: Adversarial Review of the s(11) ≥ 381/100 Explainer

**Date:** 2026-09-06 (last updated 2026-09-06)

**Author:** Claude Code

**Status:** Complete

## Overview

This is an adversarial review of the explainer page
[s(11) ≥ 381/100](https://jlevy.github.io/squares/t-018-explainer.md) and of the
documents it links as its verifiable claim: the two claim files, the proof card, the two
standard-library verifiers, and the retained certificates in
[jlevy/squares](https://github.com/jlevy/squares).
The question put to every part of it was the same: is anything false, unproved, or
misleading as written, and what would fix it.

**Verdict.** The mathematical claim stands.
The theorem is correct, its proof in the claim document is complete, and the certificate
for `s(11) ≥ 381/100` passes three verifiers and an independent re-derivation of every
number the page states.
A numerical attack that searched unit squares at all angles, not only the net angles the
certificate checks, found no placement below mass 1.

The explainer’s own presentation of the argument does not stand as written.
Its Contradiction box asserts that every unit square, “whatever its angle,” contains a
concentric side-`B` square at one of the 181 net angles and attributes that to Condition
4\. That is false for every angle past `π/4`: the net covers only `[0, π/4]`, and the
proof needs the diagonal reflection and Conditions 1 and 3 to get there.
The same omission runs through the section that derives the shrink.
The Five Conditions box leaves out two hypotheses the proof uses (`t₀ = 0` and the sign
of the weights). The budget section’s informal argument double-counts boundary atoms.
None of this affects the theorem, which is stated and proved correctly in the linked
claim documents. All of it affects a reader who takes the page as the proof.

Beyond the logic, the page misdescribes its own supporting package as a “third-party
check” (the package’s README says the opposite), never names the originators of the
method it uses, and calls two validation routes “independent” where the project’s own
epistemics vocabulary says “distinct.”
The verifiers have small, conservative defects; one of them scores 1,194 cells outside
the domain it claims to sweep.
The rest is exposition: naming, ordering, captions, and the Markdown edition’s rendering
of the credits.

The findings are ranked below.
The highest-priority corrections, in order:

1. Rewrite the Contradiction box and the opening of “From a Continuum of Angles to 181”
   to carry the reflection step (Findings A1 and A2).
2. State every hypothesis in the Five Conditions box: `0 = t₀ < t₁ < ⋯ < t_K`, and
   nonnegative weights (A3).
3. Fix the budget section’s “disjoint, so no atom is counted twice” (A4).
4. Attribute the method to Burns and Massaccesi, with the Göbel and Nagamochi lineage
   (C1).
5. Replace “third-party check” with the package’s own description (C2).
6. Say what the covering linear program ranges over, so that the two sentences drawn
   from it are true (A6).

## Scope and Method

### What was reviewed

The page host is blocked from the review sandbox, so the Markdown edition was
regenerated from the source repository at commit `c743d7bb` (2026-09-05, the commit the
page was rendered from) using the project’s own renderer, and then compared with the
copy the reviewer supplied.
The two are identical apart from line wrapping.
Quotations below are from that copy.

Documents read in full:

- The explainer, its Markdown source with the figure panels the edition strips, the
  template it is filled from, and the page shell with the JavaScript that draws Figures
  4 through 7.
- `t-018-verifiable-claim-381-100.md` and `t-018-verifiable-claim-19-5.md`: the claim,
  theorem, proof, sweep-exactness argument, embedded verifier, and embedded certificate.
- `t-018-proof-card.md`, `minimal_verify.py`, `verify_claim.py`, and the three retained
  certificates.
- `thirdparty/README.md` and its verifier, the project verifier `certificate.py` and
  sweep `sweep.py`, the net-coarsening measurement, the result register entry `T-018`,
  the atlas figure record, and the project’s epistemics rubric.
- The project’s prior reviews of the same result, so that defects they already fixed are
  not re-reported unless they persist in the explainer.

### What was run

| Check | Result |
| --- | --- |
| `minimal_verify.py certificate.json` (CPython 3.13, pinned SHA-256) | `VERIFIED s(11) >= 381/100`, least mass `4001/4000` at direction 0, 57.6 s |
| `verify_claim.py` on the 381/100 claim document | `VERIFIED`, least mass `4001/4000` at `(27/50, 27/50)`, 567,130,649 cells |
| `verify_claim.py` on the 19/5 claim document | `VERIFIED`, least mass `50003/50000` at `(53/100, 53/100)` |
| `verify_claim.py` on the 189/50 calibration rung | `VERIFIED`, least mass `200009/200000` |
| `thirdparty/check.py` | control rebuilt identically; 19/5 and Massaccesi’s `n = 17` both `VERIFIED` |
| Independent recomputation of every number on the page (own code, exact rationals) | all match; see the table in “What Holds” |
| From-scratch exact event-cell enumeration at direction 0 | minimum `4001/4000`, attained at the cell containing `(27/50, 27/50)` |
| Numerical attack: minimise the mass of a unit square at any angle and position | least found `1.00025`, at angle 0; no placement below 1 |
| Comparison of the two verifiers’ reachable-cell sets, direction by direction | `minimal_verify.py` scores cells outside the centre domain; see B1 |

### How the review was organised

Nine reviewing lenses worked independently over the same material: theorem-level logic;
the explainer’s own argument read as a proof; verifier faithfulness; a numerical attack;
numeric reproduction; exposition; framing and provenance; the figures and the page’s
JavaScript; and cross-document consistency.
A completeness critic then named lines of attack none of them had taken, and a second
round pursued those.
Every finding, including the coordinator’s own, was then handed to two refuters with
different briefs (one attacking the substance, one attacking the reading and the value
of the fix). A finding both refuters rejected is not reported as a defect; a few such
items appear in “Considered and Set Aside” so the reader can judge.
Severity is assigned by the coordinator after reading the verdicts.

**Severity scale.** *High*: a stated argument is invalid or a stated fact is false in a
way a careful reader will catch.
*Medium*: misleading, inconsistent with the linked documents, or missing a hypothesis.
*Low*: clarity or precision.
*Nit*: wording. No finding rose to *blocker*, which would have meant the claim itself
fails.

## What Holds

The theorem in the claim documents was checked step by step: the orientation reduction
(the reflection `(x, y) ↦ (y, x)` sends orientation `φ` to `π/2 − φ`, and `φ = π/4` is
its own image); the nearest-net-angle step (`d ≤` half a gap and `tan d ≤ D`, since
`tan` is increasing and `tan(arctan t₂ − arctan t₁) = (t₂ − t₁)/(1 + t₁t₂)`); the
support-function containment (`(B/2)(cos d + sin d)` is the half-width of the rotated
`B`-square along each edge normal of the unit square, so `B(cos d + sin d) < 1` puts it
in the open interior, corners included);
`cos d + sin d = cos d (1 + tan d) ≤ 1 + tan d`; the pull-back through the reflection,
which needs only invariance under that one reflection; the counting step, which needs
nonnegative weights and the pairwise disjointness of closed sets each inside a different
open interior; and the passage from “no packing in side `L`” to `s(n) ≥ L`. All correct.

The sweep-exactness argument is also correct: mass is constant on each open cell of the
arrangement, a boundary point carries at least its neighbouring cell’s mass because the
coverage boxes are closed and the weights nonnegative, and each admissible centre lies
in the closure of a cell that meets the centre domain.
The cell-meets-domain test in both verifiers is exact.

Every number on the page reproduces from the certificate with independent code:

| Quantity on the page | Recomputed |
| --- | --- |
| `D = 207107/90000000` | same; the widest half-gap is the first one, at `k = 0` |
| `B(1 + D) = 0.999995896154` | `899996306539/900000000000` |
| `t_K² + 2t_K − 1 = 309449/250000000000` | same |
| total mass `434547/40000 = 10.863675` | same, summed over the 1,121 atoms |
| 1,121 atoms in 149 orbits, 100 distinct weights in `[0.000075, 0.14672]` | 149 = 132 orbits of size 8, 16 of size 4, and the centre; weights `3/40000` to `917/6250`, all multiples of `1/200000` |
| least covered mass `4001/4000`, “50 parts in 200000 above” | same; `1/4000 = 50/200000` |
| Stromquist `3.7888543…`, Trump `3.8770835…` | `2 + 4/√5 = 3.78885438…`; the stated polynomial has a root at `3.87708359002281…` |
| Figure 3 gaps `0.0670835…` and `0.0882292…` | same |
| Figure 6 peaks `0.9999971…` at `B = 9977039/10⁷` and `0.9999932…` at `B = 9977/10⁴` | `B(1 + D)/√(1 + D²)` gives `0.99999715…` and `0.99999324…`; `9977039/10⁷` is one step below the largest seven-place side Condition 4 admits |
| Figure 7: halving the 19/5 net shrinks `B` by ≈0.23% and costs ≈9% of the least mass | 0.229% and 9.30% from the retained measurement |
| “23 years”, “21 results”, “7 of the lower bounds” | 2026 − 2003; 21 register entries; seven atlas cells marked first proved here (`n = 11, 12, 17, 18, 19, 20, 21`) |
| calibration rung `189/50` below Stromquist | `(189/50 − 2)² · 5 = 7921/500 < 16` |

The numerical attack, written without the project’s code, minimised the mass of a closed
unit square over centre and angle in `[0, π/2)` with 5,000 random restarts, local
descent, and starts placed along the edges, in the corners, on the ring inside the
corners, and at angles halfway between net directions.
The least mass found is `1.00025 = 4001/4000`, at angle 0, the same value the exact
sweep reports for `B`-squares at net angles.
The shrink argument costs nothing at this certificate: the axis-parallel placement is
the global minimum.
The worst value of `B(cos d + sin d)` over all mismatches `d` the net
allows is `0.99999325…`, at the midpoint of the widest gap, matching Figure 6.

## Part A: Logical and Mathematical Gaps in the Explainer

These concern the explainer’s own text.
The theorem and proof in the claim documents are correct; the defects are in how the
page presents them.

### A1. The Contradiction box is false for angles past π/4 (High)

**Where.** The Contradiction: “Each square, whatever its angle, contains a side-$B$
square $Q_i$ with the same center at one of the 181 net angles.
That is Condition 4.”

**Problem.** The 181 net angles lie in `[0, π/4]`. A unit square at orientation 60° is
nearest to the net angle `π/4`, a mismatch `d` of 15°, and
`B(cos 15° + sin 15°) = 0.9977 × 1.2247 = 1.222 > 1`: no concentric `B`-square at a net
angle fits inside it.
Containment holds only for `d` up to about 0.13°. The proof in the claim document
handles this in two steps the box omits: reflect the square across the container’s
diagonal so that its orientation lands in `[0, π/4]` (step 1), and, after finding the
`B`-square inside the reflected square, pull it back through the reflection, which
preserves covered mass because the atom set is reflection-invariant (step 5). The square
the argument actually finds inside `S_i` is the *mirror image* of a net-angle square,
not a net-angle square.
The box’s conclusion needs Conditions 1, 3, and 4 together; “That is Condition 4”
credits one of them.

The Atom Set section does say, two pages earlier, that invariance “lets the proof check
angles only up to $\pi/4$, since a square at any other angle reflects onto that arc and
covers the same mass,” and the sentence introducing Condition 3 calls `π/4` “the end of
the arc that Condition 1 reflects every angle onto.”
Neither is wired into the box’s chain of reasoning, which is the place a reader will
check.

**Fix.** Replace the first two sentences of the box with:

> Take any packing of eleven unit squares in the side-3.81 container.
> A square’s orientation can be taken in $[0, \pi/2)$; if it exceeds $\pi/4$, reflect
> the whole picture across the container’s diagonal, which the atom set is symmetric
> under (Condition 1), so the reflected square has orientation at most $\pi/4$ and every
> mass is unchanged. The net reaches $\pi/4$ (Condition 3), so the nearest net angle is
> within half a gap, and by Condition 4 the square contains, with the same centre, a
> side-$B$ square $Q_i$ at that net angle.
> Reflecting back if needed gives a side-$B$ square inside the original square that
> covers the same mass as $Q_i$.

The rest of the box then follows as written.
The sentence “Because Condition 4 is a *strict* inequality, each $Q_i$ sits inside its
unit square’s interior” is correct and should stay.

A secondary point in the same sentence: “with the same center at one of the 181 net
angles” reads, on first pass, as if the centre were at an angle.
“centred at the same point and oriented at the nearest net angle” removes the garden
path.

### A2. “From a Continuum of Angles to 181” quantifies over unreduced angles (High)

**Where.** “Take a unit square at any angle $\varphi$ and let $\theta$ be the nearest
net angle. […] So if every placement of the smaller square at a net angle covers mass at
least 1, every unit square at any angle does too.”

**Problem.** The same omission as A1, at the point where the shrink is derived.
For `φ` outside `[0, π/4]` the nearest net angle can be 45° away, the mismatch is not
bounded by half a gap, and the displayed containment fails.
The section’s conclusion ("every unit square at any angle does too") is true, but not by
the argument the section gives; it needs the reflection, which the section never
invokes.
The later sentence about “the arc that Condition 1 reflects every angle onto” is
a reference to the reduction, not a use of it.

**Fix.** Open the section with the reduction and then argue on the arc:

> A square is unchanged by a quarter turn, so its angle $\varphi$ can be taken in
> $[0, \pi/2)$. If $\varphi > \pi/4$, reflect the container, the atoms and the square
> across the diagonal: the atoms are unchanged (Condition 1), the square’s angle becomes
> $\pi/2 - \varphi \le \pi/4$, and the mass it covers is unchanged.
> So take $\varphi \in [0, \pi/4]$ and let $\theta$ be the nearest net angle; since the
> net runs from $0$ to at least $\pi/4$ (Condition 3), the mismatch
> $d = |\varphi - \theta|$ is at most half a gap.

The existing text from “A smaller square of side $B$ at angle $\theta$” onward then
stands.

### A3. The Five Conditions box does not state all of the hypotheses (Medium)

**Where.** The Five Conditions: “a finite set of weighted points in the container (the
atoms), a net of directions $\theta_k = 2\arctan t_k$ for $k = 0, \dots, K$, each fixed
by its rational half-tangent $t_k$, and a shrink $B \lt 1$, such that:” followed by the
five conditions, and “Together the five prove $s(n) \ge L$.”

**Problem.** Two hypotheses the proof uses are absent.

- *The net starts at zero and increases:* `0 = t₀ < t₁ < ⋯ < t_K`. Condition 3 fixes the
  top of the net; nothing in the box fixes the bottom.
  `D` is a maximum over gaps between consecutive net angles, so a net starting at
  `θ₀ > 0` would leave orientations in `[0, θ₀)` farther from any net angle than `D`
  accounts for. The claim document’s Data section states it, its proof uses it by name
  ("By Condition 3 and $t_0 = 0$"), and the project verifier refuses a net that does not
  start at zero.
- *Nonnegative weights.* The counting step $\sum_i \mu(Q_i) \le \mu([0,L]^2)$ holds only
  because uncounted atoms cannot subtract.
  The project’s prior review found that the verifier at the time lacked this check and
  accepted a five-atom certificate with a weight of `−1` that satisfied all five stated
  conditions and “proved” `s(1) ≥ 11/10`. The box, presented as the complete list of
  what a certificate is, does not mention the sign.
  The later definition ("An **atom** is a point in the container with a positive
  rational weight") covers it for a sequential reader, but it comes one section after
  the box, it uses “positive” where every formal document says “nonnegative,” and the
  Contradiction box’s counting step does not cite it.

**Fix.** In the preamble: “a finite set of points in the container, each with a
nonnegative rational weight (the atoms; every weight in this certificate is positive), a
net of directions $\theta_k = 2\arctan t_k$ with rational half-tangents $0 = t_0 < t_1 <
\cdots < t_K$, and a shrink $B$, such that:”. `B < 1` can go; Condition 4 implies it.
In the Contradiction box: “Because the weights are nonnegative and no atom is counted
twice, the eleven together cover at most the container’s total mass.”

### A4. The budget section’s argument double-counts boundary atoms (Medium)

**Where.** Atoms, Mass, and the Budget: “The eleven squares are disjoint, so no atom is
counted twice, and together they cover mass at least $11$. The container holds only
$10.863675$. So eleven unit squares do not fit.”

**Problem.** A packing has squares with pairwise disjoint *interiors*, as the page’s own
definition says. Two closed unit squares that share an edge both cover an atom on that
edge, so “no atom is counted twice” does not follow from “disjoint,” and the section
ends with “So eleven unit squares do not fit” as if the argument were complete.
The page itself later explains why the shrink has to be strict: “With $\le$ in Condition
4, two shrunken squares could share an atom on a common boundary, count it twice, and
add up to more than the container holds.”
The budget section has exactly that hole.
It is the page’s first statement of the argument and the one a hurried reader stops at.

**Fix.** “The eleven squares have disjoint interiors.
An atom on a shared edge would be counted twice, which is why the proof shrinks each
square strictly into its own interior before counting (Condition 4, below); with that
done, no atom is counted twice, and the eleven cover mass at least 11.” Alternatively,
keep the sketch but replace “So eleven unit squares do not fit” with “Once the boundary
is handled, eleven unit squares do not fit.”

Related wording elsewhere: the opening sentence says “eleven disjoint unit squares”;
“eleven unit squares with disjoint interiors” or “eleven non-overlapping unit squares”
is what is meant (nit).

### A5. “Condition 5 says every event cell … carries mass at least 1” (Low)

**Where.** Every Placement Covers Mass at Least One: “Condition 5 says every event cell,
at every net direction, carries mass at least $1$.”

**Problem.** Only cells the square’s centre can reach while the square stays inside the
container are checked; cells beyond that domain carry as little as 0, and Figure 5’s own
caption says so ("Outside it the mass falls away at once"). As written the sentence is
false, and it also misdescribes the verifier, which scores 567 million “reachable” cells
rather than the full arrangement.
One refuter read the qualifier as implied by the preceding sentence’s “positions”; the
fix costs five words.

**Fix.** “Condition 5 says every event cell the square’s centre can reach without
leaving the container, at every net direction, carries mass at least 1.”

### A6. The covering linear program is not pinned down, and two sentences about it are each true only under a different reading (Medium)

**Where.** Generator and Verifier: the display $\tau^*(L,B) = \min_{w \ge 0} \sum_a w_a$
subject to $\sum_{a \in Q} w_a \ge 1$ “for every placement $Q$”, followed by “A
certificate exists exactly when $\tau^* \lt n$. Since $\tau^*$ depends on $L$ and $B$
alone, an optimum that lands on a round number is a sign of a bug, not a result: the
target never enters the program.”

**Problem.** The display does not say which placements `Q` range over (unit squares or
`B`-squares; all angles or the net’s) or what the index `a` ranges over (a fixed finite
site set, as the generator uses, or all points).

- If the program is the one the generator solves, over `B`-squares at the net’s
  directions on a fixed site set, then “exists exactly when $\tau^* < n$” is right up to
  rationalisation, but $\tau^*$ depends on the site set and the net as well as on `L`
  and `B`. The register entry for this result records two site sets at side 3.82 whose
  optima differ, which is the dependence the sentence denies.
- If the program is the idealised one over all sites and all angles, then $\tau^*$ does
  depend on `L` and `B` alone, but “exactly when” fails in one direction: a certificate
  needs mass at least 1 only for `B`-squares at net angles, so a certificate can exist
  while the all-angle `B`-square program has $\tau^* \ge n$.

The sentence’s point, that `n` never enters the program, is right under either reading.
Also, “exactly when” glosses the rationalisation step: the search runs in floating
point, and the retained total (`10.863675`) is not the LP objective (`10.8603`, per the
register) because the weights were scaled up and rounded so that Condition 5 still holds
in exact arithmetic.

**Fix.** State the program the generator solves and say what depends on what:

> $\tau^*$ is the least total weight on a candidate set of sites such that every
> $B$-square at a net direction inside the container carries weight at least 1. It
> depends on the container, the shrink, the net and the candidate sites, and not on $n$:
> an optimum that lands exactly on an integer is a sign of a bug, not a result.
> If $\tau^* < n$, scaling a solution up slightly and rounding it to rationals gives a
> certificate; if $\tau^* \ge n$, none exists on those sites.

### A7. “A wrong linear program will be rejected by the verifier” (Nit)

**Where.** Generator and Verifier.

**Problem.** The verifier never sees the program; it decides the certificate.
A wrong program that happened to emit a valid certificate would pass, and a right one
whose output was corrupted would fail.
The preceding sentence already says what is meant.

**Fix.** “A certificate written by a wrong program is rejected by the verifier.”

### A8. $\mu(Q)$ names a minimum (Nit)

**Where.** “The least covered mass over every placement and all 181 directions is
$\mu(Q) = 4001/4000$.”

**Problem.** $\mu$ was defined as the mass of a region; here $Q$ is unbound.
Both refuters read it as “at the tightest placement $Q$,” which is standard usage, so
this is optional. Naming the placement makes the sentence carry information: “is
$4001/4000 = 1.00025$, attained at direction 0 by the square centred at $(27/50,
27/50)$.”

### A9. The sweep-exactness argument in the claim document skips one clause (Nit, linked document)

**Where.** `t-018-verifiable-claim-381-100.md`, “Why the Sweep Is Exact”: “every
admissible center lies in the closure of some open cell that meets the admissible
square, since that square has interior and finitely many lines cannot cover an open
set.”

**Problem.** The stated reason gives, for each $\varepsilon$, a cell within
$\varepsilon$ of the point, not one cell whose closure contains it.
The missing clause is that there are finitely many cells, so one of them meets the
domain within every distance of the point.
The comment block in `verify_claim.py` has the same gap.
Harmless, and one clause closes it.

### A10. “The four lines bounding the admissible centers” is not what the verifier adds (Medium, linked document)

**Where.** `t-018-verifiable-claim-381-100.md`, “Why the Sweep Is Exact”: “the edges of
these rectangles, with the four lines bounding the admissible centers, cut the plane
into finitely many open cells.”
The comment block in `verify_claim.py` says the same.

**Problem.** At any direction other than 0 the centre domain is a rotated square in the
sweep’s coordinates, and its four bounding lines are oblique.
The code does not add those lines.
It adds the domain’s extreme `u` and `v` values, that is, its axis-parallel bounding box
(`umin, umax` and `vmin, vmax`), and then decides which cells meet the rotated domain by
clipping. The decision is correct either way, because mass is constant on the cells cut
by the atom rectangles alone and the clip test is exact.
But a reader implementing the sweep from the prose would build a different, finer
arrangement, and the prose is offered as the explanation of why the verifier is exact.
`minimal_verify.py` describes its own construction correctly ("The domain’s own extremes
join the events, so no cell straddles the domain’s edge").

**Fix.** “…with the extreme $U$- and $V$-coordinates of the admissible square, cut the
plane into finitely many open cells.
A cell may straddle the admissible square’s oblique edge; the clipping test decides
exactly which cells meet it.”

## Part B: The Verifiers and Supporting Documents

None of these affects the verdict.
Each is a place where two documents or two programs that present themselves as
equivalent disagree, or where a program’s description of itself is off.

### B1. `minimal_verify.py` scores 1,194 cells outside the centre domain, and the proof card quotes that count (Low)

**Where.** `t-018-proof-card.md`: “checked exactly over all 567131843 event cells its
centre can reach, at all 181 directions”; `minimal_verify.py` prints the same number.
`verify_claim.py` prints 567,130,649 for the same certificate.

**Problem.** The difference was traced by comparing the two programs’ cell sets
direction by direction on the 19/5 certificate and testing each disputed cell exactly.
`minimal_verify.py` clips the centre domain to each strip between consecutive `u` events
and skips a strip whose clipped polygon has fewer than three vertices.
A strip that touches the domain only along an edge (at direction 0, the strip just left
of `u = h`) or at a vertex (two strips at every other direction) clips to a degenerate
polygon with four coincident or collinear vertices, passes the test, and contributes
cells whose open interiors lie entirely outside the domain: 374 at direction 0 on the
19/5 certificate, 2 at each other direction; 834 + 360 = 1,194 on the 381/100
certificate. `verify_claim.py` iterates only over strips within the domain’s
`u`-projection and counts none of them.

This is conservative: an extra cell can only lower the reported minimum, never raise it,
so the verifier cannot accept a bad certificate because of it.
Two consequences remain.
The proof card’s “cells its centre can reach” overstates the reachable count by 1,194,
and a reader who runs the claim document’s own verifier gets a different number from the
card. And a valid certificate could in principle be refused because a cell outside the
domain, which the theorem says nothing about, carries mass below 1.

**Fix.** In `minimal_verify.py`, skip a strip whose clipped polygon has zero area (or
iterate strips from the domain’s minimum `u` event to its maximum, as `verify_claim.py`
does). Regenerate the proof card’s count.
Until then, the card could say “over 567,131,843 event cells (a superset of those its
centre can reach).”

### B2. `verify_claim.py` crashes with a traceback, not `REFUSED`, if its self-check fails (Low)

**Where.** `verify_claim.py`, `least_mass`: `raise AssertionError(message)` when the
direct sum at the witness disagrees with the swept minimum; `main` catches only
`OSError, KeyError, TypeError, ValueError`, and only around loading.

**Problem.** The documented contract is one line per condition and then `VERIFIED` or
`REFUSED`, exit status 0 or 1. An implementation bug surfaces as a Python traceback with
status 1, which a caller checking the status reads as a refusal of the certificate.
`minimal_verify.py` routes the same check through its `refuse` path.

**Fix.** Catch `AssertionError` around `decide` and print an internal-error line with
exit status 2, distinct from both verdicts; or document that a traceback means the
verifier, not the certificate, is broken.

### B3. The two standard-library verifiers accept different inputs (Low)

**Where.** `verify_claim.py` `symmetric` merges the weights of atoms at a repeated site
(`weight[x, y] = weight.get((x, y), 0) + w`); `minimal_verify.py` `condition_1` refuses
a repeated site.
`minimal_verify.py` refuses an atom outside `[0, L]²`; `verify_claim.py`
does not check.

**Problem.** Both are offered as verifiers of the same theorem, and a certificate with a
duplicated site or an atom outside the container passes one and fails the other.
Neither choice is unsound: merging preserves the mass function, and an outside atom only
adds to the total. But the claim documents present `verify_claim.py` as the verifier of
the theorem “as stated,” and the theorem’s Condition 1 as written allows repeated sites
("a site of the same total weight"). The two programs should agree on what a well-formed
certificate is, or the difference should be stated.

**Fix.** Add the duplicate-site and containment checks to `verify_claim.py` as
preconditions (as `thirdparty/verify.py` does), or note in the claim document that it
merges duplicates and tolerates outside atoms because both are harmless.

### B4. `certificate.py` says the certificate proves `s(n) > L`; everything else says `≥` (Low, linked code)

**Where.** The explainer links `certificate.py` as “the verifier.”
Its module docstring concludes “so `n` unit squares do not fit in a container of side
`L`, and `s(n) > L`,” and `bounded_side` says “what the certificate proves is
`s(n) > L`. Reported as `>= L`.” The same docstring’s opening line says “It proves
`s(n) >= L`.” The claim documents prove `≥ L` from the infimum and deliberately do not
use compactness.

**Problem.** The strict inequality is true (a packing exists at the infimum, so no
packing at side `L` gives `s(n) > L`), but it is not what the claim documents prove, and
the linked file contradicts itself.
The explainer could turn this into a sentence of value: the certificate shows the side
`3.81` is too small, and by compactness `s(11)` is strictly larger; the claim is stated
as `≥` because that is what the proof in the file establishes without an appeal to
compactness.

**Fix.** Make `certificate.py` consistent (`≥ L`, with a one-line remark that `> L`
follows by compactness), and consider adding that remark to the explainer’s
Contradiction section.

## Part C: Framing, Facts, and Provenance

### C1. The method’s originators are never named (High)

**Where.** The Five Conditions, Generator and Verifier, and the opening: “The
computer-assisted proof was found via an automated research framework” and “Five exact
conditions and a pigeonhole-style argument then imply the claim.”
No name is attached to the certificate form anywhere on the page.

**Problem.** The claim document says, in its Theorem section: “The argument is a
weighted, fractional form of the classical unavoidable-set argument for square packing,
in the shape Gustavo Massaccesi used for $n = 17$ in August 2026 after Sam Burns
proposed the weighted form.
Neither the theorem nor the certificate shape is this project’s; the $n = 11$ instance
is.” The register entry’s significance rationale says the same, and the project’s prior
review traces the lineage to Göbel (1979) and Nagamochi (2005). `certificate.py` calls
the object “the Burns–Massaccesi object.”
The page, which is the public face of the result and cites Stromquist, Friedman, and
Trump in footnotes, attributes the method to no one.
A reader will take the five-condition certificate as the project’s invention.

**Fix.** One sentence at the head of The Five Conditions, with footnotes to the two
posts: “The certificate is the weighted unavoidable-set argument Sam Burns proposed and
Gustavo Massaccesi used for $n = 17$ in August 2026, descended from Göbel’s unavoidable
points (1979) and Nagamochi’s weighted resources (2005); what is new here is the $n =
11$ instance and the generator that found it.”

### C2. “A self-contained third-party check” contradicts the package it links (Medium)

**Where.** Generator and Verifier: “A self-contained third-party check, one file on
Python’s standard library, decides the 19/5 certificate without trusting anything else
here.”

**Problem.** The linked README opens: “It is not itself a third-party check, and the
name says so. This project wrote every file here, on the day of the result; a package
assembled by the party making the claim cannot be the independent check of it.”
Its title is “Self-Contained Package for Third-Party Checking.”
The project’s prior review made that correction (its finding F3); the explainer template
still carries the earlier wording.
“One file” is also inaccurate: the package is a verifier, a falsifier, a control, and a
driver.

**Fix.** “A self-contained package for third-party checking: a standard-library verifier
written from the theorem that decides the 19/5 certificate without importing anything
else here. It was written by this project; no outside party has yet checked the result.”

### C3. “Independent validation methods” (Medium)

**Where.** What Is This?: “a retention gate that keeps results only when independent
validation methods agree.”

**Problem.** The gate’s own docstring says the two routes “share the Certificate
representation and Conditions 2–4 but decide Condition 5 by different methods with
different failure modes.”
The epistemics rubric defines the rung the result holds as “confirmed by distinct
methods” and warns that “two independently written implementations using the same method
still derive C3, not C4.” The register scopes “independent in method” to Condition 5.
“Independent” on the page reads as independent validation of the whole result.

**Fix.** “a retention gate that keeps a certificate only when two methods that decide
Condition 5 differently, an exact sweep and an interval branch-and-bound, both accept
it.” That sentence would also be the page’s first mention of the interval route, which
the register calls the basis of the result’s confirmation rung and which the page never
names.

### C4. “One of 21 results registered over a few days” (Low)

**Where.** What Is This?: “This is one of 21 results registered over a few days, all
within the same automated research framework.”
Also “found via an automated research framework run over a few days.”

**Problem.** The register’s scored dates run from 2026-08-31 to 2026-09-05, and the
campaign that produced the entries runs from session 001 (2026-08-23) to session 087
(2026-09-06): two weeks, not a few days.
Seven of the 21 are marked `previously-published`; they were verified and registered,
not found. Both refuters accepted “a few days” for the four scoring dates; the
coordinator’s view is that a reader will take the sentence as the time the work took.

**Fix.** “This is one of 21 results the program registered between 23 August and 5
September 2026, fourteen of them apparently new,” or drop the count.

### C5. “Positive” versus “nonnegative” (Low)

Covered under A3. The page’s definition of an atom says “positive”; the proof card, both
claim documents, and the verifier output say “nonnegative.”
Either is sound for this certificate, whose weights are all positive.
Use the theorem’s word and note the certificate’s fact.

### C6. Two verifiers, two runtimes, neither named (Low)

**Where.** Verifiable Claim: “425 atoms, verified in about half a minute” and “1,121
atoms, verified in about 3 minutes.”
The proof card says the same certificate verifies in 47.5 to 67 seconds.

**Problem.** The page’s times are `verify_claim.py`’s; the card’s are
`minimal_verify.py`’s. Neither document says which program or what machine, so they look
inconsistent. On the review machine `verify_claim.py` took 3 min 45 s on the 381/100
document and `minimal_verify.py` 58 s.

**Fix.** “…verified by the embedded standard-library verifier in about 3 minutes on a
laptop (the pinned one-file checker beside it, `minimal_verify.py`, takes about a
minute).”

### C7. The basis of the novelty claim is not stated (Low)

**Where.** “This appears to be the first improvement in 23 years on the smallest open
case.”

**Problem.** The hedge is conventional and the refuters split on it.
What the page could say, and the package README does, is what the search covered:
Friedman’s survey, the Kingbird register, Stromquist 2003, Bentz, Nagamochi, and the two
2026 posts, with no systematic preprint sweep.
Stating the basis is more useful than the hedge.

**Fix.** “No improvement on Stromquist’s 2003 bound is known to us; the search covered
Friedman’s survey, Kingbird’s register, and the 2026 posts, not the preprint servers.”

### C8. Optional: the status of the bound being displaced (Low)

The register records (`T-010`) that the project found Stromquist’s printed argument for
`s(11) ≥ 2 + 4/√5` does not close at his Figure 14 and repaired it with a
source-distinct point set.
Both refuters judged its omission from the explainer acceptable, since the bound itself
is correct and the new proof is independent of it.
A footnote would still serve a reader who wants to know what the previous bound rested
on.

## Part D: Exposition and Structure

### D1. The opening spends three paragraphs on the framework before any mathematics (Low)

**Where.** What Is This?, paragraphs five to seven: “This is one of 21 results…”, “Most
of the research work is not the proof but the process…”, “None of this is particular to
square packing…”, with links to three tools.

**Problem.** A reader who came for the proof reaches the problem statement after a
project inventory (hypothesis registry, experiment ledger, retention gate) and a tool
list. One refuter defended the placement as the author’s stated thesis ("Most of the
research work is not the proof but the process"). The thesis can stay in one sentence;
the inventory and the tool names are a closing section.

**Fix.** Keep paragraphs one to four and a single sentence of the fifth; move the rest
to a final section, “About the Project,” after Verifiable Claim.

### D2. “Why the Net Has 181 Directions” promises more than the section shows (Low)

**Where.** The section title; the caption concedes “This shows these atoms are tight
against their own net, not that no coarser net could be made to work.”

**Problem.** The section prices coarsening the net under atoms optimised for `K = 180`;
it does not show that 181 directions are needed, or say why 181 was chosen.
Both refuters read the title as the mathematical “why” and accepted it.
The coordinator’s view is that the caption’s own disclaimer is the better title.

**Fix.** “What a Coarser Net Costs,” plus one sentence on how `K = 180` was chosen, if
the reason is known (the coarsest net the generator was run on, a compute budget, or the
net Massaccesi used).

### D3. The Markdown edition: credits, captions without figures, Figure 3’s preposition (Low)

**Where.** Lines 5–7 of the edition: “September 5, 2026 (DRAFT v0.1.0-3bd273e6) Tooling
and human oversight: **Joshua Levy** Agents: … Open source at …” as one paragraph.
Figure 3: “The shaded band is the bound gap … Below $381/100$ it is $0.0670835\ldots$
wide”. Figures 2, 5, 6, 7: captions describing “the dashed domain,” “the dark outline,”
“orange,” with nothing above them.

**Problem.** The credits run together because the renderer’s list conversion looks for
`<div class="credits">` and the template emits `<div class="credits centred">`, so the
regex never matches and the four spans fall through to the paragraph flattener; the
code’s own comment says the list form is intended.
The edition note does warn that Figures 2 to 7 are captions only, and the refuters
accepted that; the captions still describe colours and outlines a reader of this edition
cannot see. Figure 3’s “Below $381/100$” is the wrong preposition for a gap that lies
above the bound.

**Fix.** Change the regex to match `class="credits[^"]*"`. Give each figure-only caption
a lead clause ("On the page, Figure 6 draws…") or a text-only alternative.
Figure 3: “With the lower bound at $381/100$ the gap is $0.0670835\ldots$ wide, down
from $0.0882292\ldots$ at Stromquist’s bound.”

### D4. Figure 6’s caption is opaque about the side it quotes (Low)

**Where.** “that product’s largest value, at the widest half-gap, is $0.9999971\ldots$
at $B = 9977039/10000000$, a seven-place value one step below the largest Condition 4
admits, and $0.9999932\ldots$ at the certificate’s own side.”

**Problem.** “A seven-place value one step below the largest Condition 4 admits” is the
renderer’s construction, not an explanation: the figure uses the largest side with seven
decimals for which $B(1 + D) < 1$, so that the shrink shown is the smallest the net
allows, and the caption quotes two peaks without saying why.

**Fix.** “…is $0.9999971\ldots$ at $B = 0.9977039$, the largest seven-decimal side that
still satisfies Condition 4 (the figure uses it so the shrink shown is the least the net
allows), and $0.9999932\ldots$ at the certificate’s own $B = 0.9977$.”

### D5. “The project proves two bounds” without saying why the weaker one is kept (Low)

**Where.** Packing 11 Squares: “Here we prove $s(11) \ge 381/100 = 3.81$. The project
proves two bounds. (Some of the figures below also show the looser one …)”

**Problem.** $19/5$ is implied by $381/100$. The package README gives the reason it is
kept (it is the certificate the project’s adversarial review read line by line, and its
smaller numbers make the figures legible); the page gives only the parenthesis.

**Fix.** “A second certificate at $19/5$, with 425 atoms, is kept because its smaller
numbers make the figures legible and because it is the one the project’s adversarial
review checked line by line; the $381/100$ certificate supersedes it.”

### D6. Wording (Nit)

- Figure 4 caption: “The board holds less mass” is the only “board” on a page that says
  “container” twelve times.
- Condition 1 names $\mathbf{D}_4$ without a gloss; the gloss ("the eight rotations and
  reflections of the container") arrives two sections later.
  “(its four rotations and four reflections)” in the box would make it self-contained.
- “The witness used in the proof places 1,121 rationally weighted points” in the
  opening, “certificate” everywhere after; Figure 1 uses “witness” for packings.
  Use “certificate” for the atom set and keep “witness” for packings.
- “50 parts in 200000 above the threshold”: the reader has to notice that 200000 is the
  weight unit from two sentences earlier.
  “the margin is 50 of the smallest weight units” says it.
- “The first condition on the atoms” (Every Placement Covers Mass at Least One) refers
  to the first bullet of the budget section, not to Condition 1; both refuters found the
  appositive disambiguates it.
  “The covering requirement” avoids the collision.
- Figure 4 caption uses “covering linear program” four sections before it is defined.

## Considered and Set Aside

Findings raised by a lens and rejected by both refuters, listed so that the reader can
disagree:

- “Pigeonhole-style” for the counting argument: the weighted, resource-exhaustion form
  of pigeonhole is exactly what the argument is, and “-style” marks the generalisation.
- “This paper” for a web page: standard for a formal presentation of a result at any
  publication status; the DRAFT stamp carries the status.
- “Check by hand”: read in contrast with “paste into any coding agent,” it means run the
  verifier yourself.
- “The proof makes it finite twice over”: idiomatic for “in two respects,” and the next
  two sentences name the two.
- “An optimum that lands on a round number”: nobody reads $434547/40000$ as round; the
  heuristic is a valid engineering one.
- Figure 3’s “shaded band” as a standalone defect: the edition note covers it; folded
  into D3.

## Suggested Rewrites in One Place

The three passages that carry the argument, rewritten so that each stands on its own.

**The Five Conditions, preamble.** The proof is a **certificate**: for $n$ unit squares
in a container of side $L$, a finite set of points in the container, each with a
nonnegative rational weight (the atoms; every weight in this certificate is positive), a
net of directions $\theta_k = 2\arctan t_k$ with rational half-tangents $0 = t_0 < t_1 <
\cdots < t_K$, and a shrink $B$, such that: [Conditions 1 to 5 as now].

**From a Continuum of Angles to 181, opening.** A square is unchanged by a quarter turn,
so its angle $\varphi$ can be taken in $[0, \pi/2)$. If $\varphi > \pi/4$, reflect the
container, the atoms and the square across the diagonal: the atoms are unchanged
(Condition 1), the square’s angle becomes $\pi/2 - \varphi \le \pi/4$, and the mass it
covers is unchanged.
So take $\varphi \in [0, \pi/4]$ and let $\theta$ be the nearest net angle; since the
net runs from $0$ to at least $\pi/4$ (Condition 3), the mismatch
$d = |\varphi - \theta|$ is at most half a gap.
A smaller square of side $B$ at angle $\theta$, with the same centre, covers no more
mass than the unit square if it fits inside it, because the weights are nonnegative.
[Continue as now from “It fits exactly when”.]

**The Contradiction.** Take any packing of eleven unit squares in the side-3.81
container. Reflect any square whose angle exceeds $\pi/4$ across the container’s
diagonal, which changes no mass (Condition 1). Its angle is then within half a gap of a
net angle (Condition 3), and by Condition 4 it contains, with the same centre, a
side-$B$ square $Q_i$ at that net angle; reflecting back gives a side-$B$ square inside
the original square with the same mass as $Q_i$. Because Condition 4 is a *strict*
inequality, each of these sits inside its unit square’s interior, so the eleven are
pairwise disjoint and no atom is counted twice.
Each covers mass at least $1$ (Condition 5), and the weights are nonnegative, so
[display as now], where the last step is Condition 2. The two ends contradict each
other, so no such packing exists, and $s(11) \ge 381/100$. (By compactness a packing
exists at the infimum, so in fact $s(11) > 381/100$; the claim is stated as $\ge$
because that is what the verifier’s theorem proves without it.)

## Limitations of This Review

- The page host was unreachable; the interactive page was reviewed from its source (the
  shell’s JavaScript and the figure panels) rather than by viewing it.
  The Markdown edition was regenerated locally and matched the reviewer’s copy.
- The literature was checked against the project’s own records and the reviewers’
  knowledge; Friedman’s survey, Stromquist’s paper, and the 2026 posts could not be
  fetched.
- No formal (proof-assistant) check of the theorem exists, and this review adds none.
  The theorem was checked by hand and by three independent readers.
- The numerical attack is a search, not a proof; its value is that it found the same
  minimum the exact sweep reports, not that it excludes a lower one.
  The exact sweep does that.

## References

- The explainer: [s(11) ≥ 381/100](https://jlevy.github.io/squares/t-018-explainer.md),
  Markdown edition of [jlevy.github.io/squares](https://jlevy.github.io/squares/).
- The claim documents, proof card, verifiers, and certificates:
  [`packing/cases/n11_fractional_certificate/`](https://github.com/jlevy/squares/tree/main/packing/cases/n11_fractional_certificate)
  in jlevy/squares.
- The project verifier and sweep:
  [`certificate.py`](https://github.com/jlevy/squares/blob/main/packing/src/sqpack/fractional/certificate.py)
  and
  [`sweep.py`](https://github.com/jlevy/squares/blob/main/packing/src/sqpack/fractional/sweep.py).
- The result register:
  [`results.yaml`](https://github.com/jlevy/squares/blob/main/packing/frontier/results.yaml),
  entry `T-018`; the epistemics rubric:
  [`epistemics.md`](https://github.com/jlevy/squares/blob/main/epistemics.md).
- The project’s prior reviews of the result:
  [review-2026-09-04-pr78-s11-adversarial.md](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-09-04-pr78-s11-adversarial.md)
  and
  [review-2026-09-04-t018-thirdparty-package.md](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-09-04-t018-thirdparty-package.md).
- Walter Stromquist,
  [Packing 10 or 11 unit squares in a square](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v10i1r8),
  Electronic Journal of Combinatorics 10 (2003), R8.
- Erich Friedman,
  [Packing unit squares in squares: a survey and new results](https://erich-friedman.github.io/papers/squares/squares.html),
  Electronic Journal of Combinatorics, Dynamic Survey DS7.
- Sam Burns,
  [Proposing a better lower bound for n = 17 square packing](https://sam-burns.com/posts/proposing-better-lower-bound-for-n17-square-packing/)
  (August 2026); Gustavo Massaccesi,
  [Another better lower bound for n = 17](https://gus-massa.blogspot.com/2026/08/another-better-lower-bound-for-n17.html)
  and
  [Linear programming for square packing](https://gus-massa.blogspot.com/2026/08/linear-programing-for-square-packing.html)
  (August 2026), as cited by the project.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
