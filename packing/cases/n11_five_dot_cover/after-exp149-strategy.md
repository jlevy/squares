# After exp149: Test the Escape in the Snapped-Core Model

**Proposed next milestone, 2026-09-09.** Open one registered BC320 discriminator on the
saved exp149 escape before changing dots, scanning another tuple, or multiplying owner
subclasses. Ask whether the escape can be strictly disjoint from some allowed snapped
owner core in each of its four selected classes.
This is a bounded test of the specific relaxation failure, with no new geometry engine.

This proposal reads published contracts, source, and retained receipts only.
No new target geometry, owner pose, mask, or compatibility relation was evaluated.

## Evidence and the Immediate Question

Exp149, at source `5600c0fb4eccf9e9dcdf82b02506d3d4340651cb`, completely refutes D on
tuple (0,0,0,7). Its first direction, axis `owner-000`, has a positive exact deficit and
a replayed strict escape centred at

$$x=\left(\frac{7641479337977841787}{2367233010000000000},
\frac{11240556076810055587}{4734458945995860000}\right).$$

The internal selected check took 0.085299 seconds; most recorded process time preceded
that geometry check.
H147 is refuted; H146’s existence question remains unresolved.

Only TR differs from the already certified tuple (0,0,0,0). Since x avoids D and the
other three unchanged patches, the baseline cover implies that its core intersects the
baseline TR patch. It avoids the chosen TR class-7 patch.
Thus the recorded failure comes from information lost by that changed owner condition.
This implication uses the retained baseline certificate; it is not a new intersection
computation.

Test TR first. The discriminator distinguishes a core admitted only by the common
footprint from one that survives the stronger individual-owner condition.

## One Falsifiable Registered Scope

**Hypothesis:** For at least one of the four selected classes, no allowed snapped
B-owner core can be strictly disjoint from the saved escaping B-core.

Freeze the exact exp149 escape and its receipt blob, exp143 scale/directions, exp146
frame records and source blob, and tuple (0,0,0,7). The coordinator assigns new
hypothesis and experiment IDs on the next milestone branch after the current validation
checkpoint. Use BC320’s 30-minute insight slice, with a proposed 120-second external
target bound and 90-second cooperative bound after input loading.
These are prospective limits, not runtime predictions.
No additional residual pose or class is selected in this run.

Use corner order TR, BL, BR, TL. For each selected class, consume every retained signed
frame and its verified nonempty closed centre polygon Z from exp146, including point or
segment cases. Apply the physical corner map to the axes and centre polygon together.
For owner frame o, residual frame theta, and the eight signed SAT axes

$$n\in\{\pm u_o,\pm v_o,\pm u_\theta,\pm v_\theta\},$$

put $\rho_o(n)=h(|n\cdot u_o|+|n\cdot v_o|)$ and define $\rho_\theta$ identically.
Compute the exact separation slack

$$\Delta_{o,n}(x)=n\cdot x-\min_{z\in Z_o}n\cdot z-\rho_o(n)-\rho_\theta(n).$$

The minimum occurs at a stored rational vertex.
Strict coexistence in that frame is equivalent to at least one positive slack.
This follows from square-square SAT and minimization over the allowed centre polygon; it
needs no LP or owner-position grid.
There are at most 4×181×8 scalar tests before vertex minima, with optional early exits.

Accept the hypothesis when one selected class has every frame/axis slack nonpositive.
Its complete finite certificate proves that this escape cannot coexist with any owner
core in that class. Record the maximum slack: a strictly negative maximum also gives a
neighbourhood excluded by this stronger condition.
A zero maximum excludes the exact pose but does not itself prove a positive-area domain
improvement.

If a positive slack is found for a class, retain its attaining centre and frame and
independently replay centre/class membership and strict square-square separation.
If all four classes supply such witnesses, refute this individual-owner hypothesis for
this escape. A partial frame list cannot support a universal exclusion.
Deadline, invalid provenance, missing frames, or disagreement with independent replay is
unresolved or invalid, never a completed negative.
Stop after one conclusive incompatible class, or four compatible classes; do not widen
the scope.

## Why the Finite Owner Frames Are Sufficient Here

**Both tested shapes have side B=9977/10000. These are snapped cores, not full unit
owner squares.** Exp146’s centre constraints use h=B/2. A compatible core pose therefore
does not establish a realizable contained unit parent.

The retained transfer $B(1+D_{\rm net})<1$ assigns every hypothetical unit packing a
family of full-net B-cores strictly inside its parents.
BC303 supplies four distinct selected core owners containing the corner-pair marks.
Conditioning on one coarse selected-core class puts that actual selected core in one of
its complete recorded frames and centre sets.
The 181 class frames are exhaustive for that finite necessary model; they are not
samples standing in for arbitrary continuous unit-owner angles.

Consequently, exclusion against every allowed snapped core excludes this residual pose
under the already admitted physical transfer.
No new all-angle approximation is being claimed.
Testing full unit squares at only those 181 angles would not justify a universal
continuous-owner conclusion and is outside this protocol.

Conversely, four individually compatible B-core witnesses can overlap one another, can
fail to extend to contained unit parents, and need not accommodate the other residual
cores. They certify only survival of this necessary individual-owner relaxation.
They are not a four-owner packing or an eleven-square witness.

Source theorem:
[owner-pose refinement contract](../../campaign/series/series-000-smoke-and-calibration/results/agenda-032/proofs/owner-pose-refinement-contract.md),
section “Stronger Domain: Some Owner Pose Must Coexist.”

## Decision After That One Test

| Result | Next justified action |
| --- | --- |
| One owner class excludes the escape | Construct only that class’s stronger forbidden-centre polygon at the failed residual direction, using the same exact complementary half-planes. Measure whether it removes a nonempty part of the recorded deficit before funding a full-net cover or selective split. Do not declare the owner class itself impossible. |
| All four classes admit separated cores | Individual-owner tightening cannot remove this witness. Prefer a separately frozen six-dot test on the same tuple: retain D and add x as the sixth site. This certainly hits the saved core and preserves all previous dot hits; acceptance still requires all 361 directions. Four owner plus six dot obstacles require up to 1,023 union subsets. Six dots still contradict seven disjoint residual cores. No LP is needed for this first discriminator. |
| Partial or invalid | Preserve the prefix and diagnose that specific instrument or input issue. No larger tuple scan, extra pose, or automatic budget extension follows. |

A single incompatible residual pose does not prove the entire class domain covered.
Likewise, adding one dot to hit one witness does not prove a six-dot cover.
Those are separate prospective experiments after this classification, and neither
retroactively changes exp149’s fixed-five-dot result.

## Structural Reduction and the Global Gap

Let U contain all sixteen labels and E={0,7,8,15}. Existing analytic witness transport
shows that a D-cover requires BL/TR in E. A cover by D1=H(D) requires BR/TL in E.
Therefore a tuple coverable by either retained five-dot pattern must lie in

$$(E\times U\times U\times E)\cup(U\times E\times E\times U).$$

This union has 7,936 labels; its intersection has 256. The other 57,600 labels are ruled
out as candidates for these two patterns, not as physical packings.
This is a cheap analytic restriction, not a completed census or probability of success.

A precise necessary routing lemma for this portfolio would say: after the retained core
reduction, every hypothetical packing admits valid owner/mark/sector choices with E
available at both corners of at least one diagonal.
The corner-pair theorem supplies owners and marks, but does not establish this
endpoint-sector choice.
Even that lemma would not route directly into the currently certified tuples.
The actual global task is to prove that some valid four-owner selection lies in a
completely excluded tuple family, or to dispose exhaustively of every remaining
selection. Labels may overlap and owning both marks does not create two owners.

With the actual deficit, BC320’s concrete one-escape compatibility test has greater
immediate information value than trying the next tuple.
T-023 remains V3/C3, and no global n11 bound changes.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
