# Pending Controls for the #1052 Alignment Variants

Written on 21 November 2026 before any whole-packing replay of the follow-up variants or
bounded-motion solver check in this intake.
The original accepted review, the contributor’s programs as text, and the small
comparisons in [comparisons.json](comparisons.json) have already been read.
These jobs are not blind.
The comparison program has checked artifact identities and five local blocking pairs.

## Variant Feasibility: think-rbyl

Bind `n305_31_quarter_turns.json` and `n305_37_aligned.json` to
[the custody manifest](../acquisition/manifest.json) before decoding them through the
maintained `center-direction-json` adapter.
Decide the exact filed side, not the rounded 12-place display.

For each variant, both `sqpack.verify` and `devtools.check_rational_witness_independent`
must accept 305 unit squares, containment in the box and all 46,360 distinct pairs.
Use the maintained positive, duplicate-square and outside-container jobs, followed by
the maintained sharp wall and pair controls at contact and $10^{-30}$ past contact.
Both routes must refuse the negative controls.
Include the enlarged-square shape controls.
Retain the verdict of every job, including refusals, mismatches and timeouts.
Producer verdict files do not satisfy this plan.

Use one worker under the host memory guard with a 600-second ceiling per maintained job,
on the external scratch volume.
Coordinate the host reservation before starting; no such jobs ran for this packet.
Freeze the concrete launch arguments and input roster in the replay receipt before
execution. Use the standard maintained import harness once the coordinator has wired the
artifact declaration; a new geometry checker is unnecessary.

A successful 31-turn replay, combined with the five exact forced turns in the saved
comparison, establishes maximum 31 only when every center, the enclosing side and every
other direction stay fixed and each of the specified 36 directions is kept or snapped.
A successful 37-turn replay establishes a same-side nine-center witness.
A separate 36-turn witness must also be checked before claiming the same nine moves
suffice with square 43 retaining its original direction.
Assess any publication of these as drawing variants through the existing drawing
workflow; they do not reduce the filed side.

## Bounded-Motion Minimality: think-3n8h

Tracker: think-3n8h, child of think-rbyl.
All 34 solver checks and the hitting-set proof remain pending independently of the
variant feasibility lane.
The proof concerns exactly aligned versions of the 36 near-axis squares, all other
directions fixed, the original box side, and an absolute bound $2\times10^{-11}$ on each
changed center coordinate.
Review both alternatives for square 43: its original direction and exactly upright.

Reconstruct each of the 17 groups from `source/local-move-conflicts.json`. Independently
check that fixing the named centers at their original positions makes the listed subset
of tiles infeasible even when every other retained center can move anywhere within its
permitted coordinate box.
Audit the signed separating-axis disjunctions, exact wall inequalities, coordinate
bounds and any pair-pruning condition.
Omitting all outside tiles relaxes the full problem; the reviewer must preserve that
direction of implication.
A solver’s timeout, unknown answer or error is not infeasibility.

Retain the 34 exact rational solver inputs, solver version and verdicts.
Predeclare satisfiable and unsatisfiable small geometric controls with hand-derived
answers, including touching, an exact positive gap, a small overlap, a wall crossing and
a coordinate-bound crossing.
Controls must check the inequality signs and disjunction coverage.
Require expected solver verdicts on each before relying on the 34 unsat results.
Set explicit solver and host ceilings in the separate launch plan; do not infer them
from a successful unbounded source run.

Separately reproduce the finite hitting-set statement: no set of at most eight center
IDs meets all 17 groups, while a set of nine does.
The lower bound requires every geometric group claim and complete combinatorial
coverage. The upper bound requires exact feasibility of the corresponding nine-center
witnesses, including the permitted displacement bounds.
Record these two directions separately before calling nine a minimum.
This result would not prove unrestricted local or global optimality.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
