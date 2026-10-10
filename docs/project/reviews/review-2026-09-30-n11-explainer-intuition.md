---
title: N11 Optimality Review — Intuition and Visual Structure
date: 2026-09-30
status: draft
---
# N11 Optimality Review — Intuition and Visual Structure

## Scope and Context

The [article](../../../packing/devtools/templates/n11-optimality-review-article.md)
explains Ahmed’s computer-assisted proof for a mathematically curious reader who has not
studied its certificates.
This review compares that reading experience with the
[earlier explainer](../../../packing/devtools/templates/n11-lower-bounds-explainer-article.md).
Astra at max reasoning reviewed the mathematical limits of proposed intuitions; separate
Sol passes reviewed narrative and visual design.
The article is unchanged by this pass, and no quality scores are assigned.
Tracking: `think-8j43`, under `think-75cp`.

The central difficulty is the missing connection between scales: the article describes
many exact checks before readers have a durable picture of how they turn an arbitrary
packing into a local question.
Adding pictures of more inputs would not resolve that.
The priority is a whole-proof map, followed by pictures of the implications.

This is an exposition review, not a new mathematical confirmation or geometric replay.
The [technical reconciliation](review-2026-09-30-n11-explainer-proof-reconciliation.md)
owns the source comparison and mathematical qualifications; the
[validation guide](../../../packing/resources/web/n11-optimality-2026-09-29/VALIDATION.md)
owns the current verification entry point and standalone-package limitations.

## Strengths to Preserve

The theorem allows independent rotations and legal touching, and the exact construction
is visible before the lower-bound machinery.
The article separates outer possibility from guaranteed interior, retains closed
boundaries, and explains why local linear rigidity is insufficient.
It also discloses the difference between a recorded composition and fresh computation.
These distinctions should become easier to see, without being removed from the argument.

Keep the user’s provenance-first opening and original links.
The proposed roadmap belongs after the statement and attaining construction.
The earlier explainer’s useful pattern is to teach a concrete mechanism before its
exhaustive computation; its point-mass interface itself is not a verifier or a visual
model for all of T-060.

## Tier 1: Common Edit

No separate mechanical cleanup is proposed.
The consequential changes below affect explanation or proof-linked figures and need
their own review.

## Tier 2: Copy Edit

**1. Give the pose vocabulary a physical referent (E1, E2).** In “One Geometric
Invariant Supports the Certificates,” introduce a pose as a center and an angle, and an
owner as the square assigned to an occupied cell.
Follow the definitions with “In every valid packing under the current assumptions, each
square’s pose belongs to its outer cover and its interior contains its owned hull.”
Keep both formal terms for the reader who follows the code.

**2. Name the denominator when it is used (E1).** In “From a linear obstruction to a
finite neighborhood,” “The right-hand denominator is positive” precedes the fraction it
refers to. Name $2(r_j-\epsilon_jR)$ there.
The three local-proof levels should remain explicit: the inequality’s intuition, its
derivation, and the complete checked census.

## Tier 3: Full Feedback

These changes reorganize the teaching sequence and should be implemented as reviewed
publication slices rather than silently folded into a copy edit.

**3. Make the capture figure readable independently of its table.** In “Capture Forces
Case 438 Near the Construction,” Figure 3 shows ancestry while the preceding table
carries the branch conditions.
Put the closed inequalities on the corresponding edges, and label the near leaf
“enclosed; local theorem still needed.”
Retain the ten-node ancestry and all endpoints.
This gives a printed or separately viewed figure its premises without changing the
argument.

**4. Show the whole implication before its machinery (P1, E2, R4).** “The Result” has a
short count summary, but the reader must retain it through many sections.
Add a compact map with two routes to the theorem: the exact construction attains $T$;
assuming a packing with side $S<T$ leads to a contradiction.
Along the second route, label what each stage establishes.
Counts such as 2,184 and 2,180 are secondary annotations, not the names of the ideas.
Foreshadow the rational cap $U>T$ and the fixed-`T` local theorem here, so their
different roles do not become a surprise at the end.

The witness also retains an atlas footer labeled “U Trump.”
In the article adaptation, call it the construction at $T$ so it cannot be confused with
the article’s larger rational cap $U$. Preserve the original atlas asset.

**5. Teach one exclusion before the exclusion inventory (P4, R3).** The Minkowski
formula in “Removing poses that force overlap” has no worked geometric example.
First show a simple possible-center region and another square’s guaranteed interior,
deleting only centers that force overlap.
Then use the accepted row already selected in the
[illustration plan](../specs/active/plan-2026-09-30-n11-optimality-illustrations.md):
case 2095, step 1, owner 10, row 17. Show four aligned panels: possible centers over a
whole angle interval; the strict core and another square’s guaranteed hull; the
forbidden center region; and the retained remainder.
Introduce the sum $K+(-Q)$ after the picture explains why the centers are forbidden.
Label this as one row of a complete update, not as a complete exclusion or a case-438
capture step.

**6. Explain charge as a capacity argument before presenting its notation (P4, R3).**
“Charge Budgets” introduces sets $O,P,J$ and $b$ before a concrete transfer.
First show the proposed two-required-cells example: each square must consume one unit of
a feature whose capacity across disjoint strict cores is one.
Only then introduce the general strict budget and required-owner conditions.
A projection strip should show why two separated cores cannot both cover the same
directional median. It must not depict the charge as counting three contained sites.
Any numerical example presented as actual proof data must be bound to its accepted field
input and transferred mask.

**7. Give symmetry a picture of a point, not a rotated cell (R2, G2).** “Symmetry
Reduces the Four Survivors to One” describes an unseen overlay through counts.
Reuse the cell figure to show four transformed views of one center and one strict
distance ban.
Keep the exhaustive 220-region and 1,572-ban census in the caption or audit
detail. The illustrative example explains what the search rejects; it cannot replace the
search.
A colored cell must not appear to rotate into another cell, since these irregular
cells do not have that symmetry.

**8. Separate capture from isolation visually (P4, R2).** The capture tree gives an
enclosure; the next section opens with several feature counts before explaining what
local isolation does.
Put the conceptual statement first: for a packing feasible in the fixed-`T` container
whose coordinates lie inside the checked rectangle, any nonzero feasible displacement
would require $\tau\le c_j\tau^2$ with $0<\tau\le1$ and $c_j<1$. Plot the two sides as
an algebraic schematic, then derive the inequality and give its complete
branch/coordinate census.
A two-coordinate projection may illustrate uncertainty, but must not purport to draw the
full 33-dimensional feasible set or prove isolation by a few animated motions.

**9. Make the exact endpoint part of the main story (R2, J3).** In “Closing the Gap,”
show the same hypothetical side-`S` container centered in the rational cap and then
rigidly aligned inside the fixed-`T` container.
The field scale is a coordinate conversion.
The physical unit squares never shrink.
Local isolation forces the exact construction, whose span $T$ contradicts fitting in
$S<T$. This is the conceptual payoff, not a numerical limit argument, and deserves an
early preview and a closing figure.
It does not claim that every optimal packing has been classified.

## Proposed Reader Roadmap

The main body should let the reader answer these questions in order:

1. What construction fits at $T$, and why does that establish only half the result?
2. How can an argument cover every possible position and rotation?
3. What lets an exact certificate safely rule out a whole region of possibilities?
4. Why does every hypothetical smaller packing reach the case-438 capture argument?
5. How does capture put it within reach of a local theorem?
6. Why does the finite local estimate exclude every nonzero displacement there?
7. How does that contradict a container smaller than $T$?

Proposed overview prose, to be checked with the final figure:

> The proof must handle a packing we have never seen.
> It first assigns its centers to finitely many patterns and uses exact certificates to
> discard impossible patterns.
> Every remaining possibility, after a symmetry of the container, enters the capture
> argument. Capture encloses its positions and angles near the known construction.
> For a hypothetical smaller container, the checked change of frame places that same
> packing inside the exact container and within a neighborhood where only the
> construction is feasible.
> The construction spans $T$, so it cannot fit in the smaller container.
> The exact construction itself supplies the matching upper bound.

The paper needs two levels of detail.
Its main route carries the geometric ideas and short connecting arguments.
Adjacent captions, appendices and the validation guide carry source case IDs, complete
inventories, exact branch counts and replay links.
Do not hide mathematical premises, such as whole-angle coverage or strict interiors, as
implementation detail.
Preserve the provenance links at the start.

## Implementation and Review Disposition

The user approved implementation of the restructuring.
The
[illustration plan’s implementation record](../specs/active/plan-2026-09-30-n11-optimality-illustrations.md#implementation-record)
maps every finding above to an article change, figure and bead.
The paper now has twelve SVGs in eleven numbered figures.
Static panels carry the complete explanations into HTML, Markdown and PDF; optional
selectors remain deferred.

Astra reviewed the restructured article and all three figure modules against retained
accepted inputs. The illustrations preserve the actual-packing ownership invariant,
whole-angle strict cores, closed forbidden regions and residual coverage, complete-step
ownership promotion, median-projection capacity and mask-transfer conditions, pointwise
D4 views, closed capture splits, the fixed-T local hypothesis, and the unchanged-size
endpoint contradiction.
Receipt and decoded-object bindings were checked.
The cell inset uses current-U diameter arithmetic rather than historical-cap metadata.
Corrections to field-coordinate labels, charged-subset/mask notation and receipt
bindings resolved the mathematical findings; no blocker remains in this exposition
audit. No geometric certificate replay was performed.

Sol’s common-doc and rendered review confirmed the proof sequence, citation proximity,
shared typography and static figure layout.
The initial worked-row and capture labels overlapped in print; the revised labels fit.
Raw math delimiters in HTML captions were replaced with readable notation, and the
publication tests now check caption rendering and label bounds at desktop, mobile and
print sizes. The provenance-first opening is retained as requested.
The redundant sentence describing this as an illustrated exposition was removed.

Integration is tracked by `think-rlg8`; the earlier review bead `think-8j43` is
complete. The PR carries final validation results.
Success remains the reader test: trace both halves of the theorem, explain one safe
exclusion, and distinguish capture from fixed-T isolation using the figures and
captions.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
