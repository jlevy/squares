# Selected-Cover Adapter: Source Admission

**GO for the single registered H147/exp149 run.** No consequential mathematical blocker
remains in the reviewed source.
This is the explicit tuple (0,0,0,7), with unchanged D and the admitted exp146 wall
footprints. No target geometry, candidate, or escape was evaluated in this review.

Reviewed source and controls:
[wall_owner_selected_cover.py](../../devtools/wall_owner_selected_cover.py) and
[test_wall_owner_selected_cover.py](../../tests/test_wall_owner_selected_cover.py),
against the [selected-cover contract](after-exp148-strategy.md).
The reviewer independently ran the five synthetic controls using project Python 3.14:
**5 passed in 0.44 seconds**. They exercise selected footprint identity, complete-zero
coverage, first-deficit stopping with actual strict escape extraction on synthetic
polygons, final-deadline refusal, receipt provenance, and CLI source refusal.

## Source and Geometry

The CLI binds the clean expected implementation revision, exact retained exp143 blob,
and exp146 blob and constructor revision.
Exp147/148 are not parsed: their role is to justify the prospectively declared choice,
while this instrument tests that choice directly.
Source loading, validation, and output-path refusal use the existing admitted helpers.

Although `run_selected_cover` itself only checks the number of directions, its admitted
CLI input path independently reconstructs the complete manifest in `load_frozen_input`,
checks serialized provenance against that reconstruction, and binds the known exp143
bytes. Thus the actual target does not rely on a count of 361 alone.
No additional parser or direction generator is required for this frozen run.

`select_four_footprints` uses the fixed tuple, loaded outer side, and BL/BR/TL/TR corner
maps. It requires the four selected polygons to have four vertices.
Only those four footprints replace the independent union input’s baseline patches.
The receipt records the actual selected polygons, class IDs, corners, and wall source.
It preserves the endpoint source separately for D and the other fixed data.

## Exact Outcomes

The direction loop uses the existing independent nine-obstacle union with all 511
nonempty subsets available.
It rejects negative uncovered area, stops at the first positive deficit, and requires
all 361 exact zero deficits for cover acceptance.

`extract_selected_escape` subtracts only the selected four owner collisions and five dot
collisions from the legal centre container.
Its deterministic rational component means are independently replayed against the strict
open container, closed-core dot contacts, and strict separating-axis avoidance of each
of the four selected polygons.
These are the correct open/closed semantics.
It does not call the 64-class mask routine or construct a witness bank.

A positive deficit with a replayed strict escape completes the selected-cover refutation
of H147. It does not refute H146’s existence claim.
A complete 361-direction cover accepts H147 and supplies another conditional
owner-branch exclusion.
No result here establishes joint owner feasibility or a global packing bound.

## Time and Receipt Semantics

The internal 240-second clock begins after input loading and before selected geometry
construction. Checks occur before each direction, within the independent union routine,
before and after escape extraction/replay, and before final cover success.
A crossing returns partial/incomplete.
Failure to find a strict escape after a positive area raises an invalid-input/instrument
result, rather than silently treating the area as a complete refutation.
There is one tuple, no seed stage, and no retry.

The external 300-second bound must cover input loading and output publication too.
JSON is written atomically only on return or a caught exception.
External termination or an unexpected borrowed exception can leave no JSON; preserve
that absence with process status, elapsed time, and logs.
It is not completed mathematical evidence.

The receipt preserves exact rational areas, completed direction rows, expected and
checked counts, and any strict escape.
An early refutation may have status complete with fewer than 361 rows because the
selected question has been answered; its actual checked count remains explicit.
A partial run may retain a positive-area row or even an escape without upgrading the
outcome.

The implementation agent confirms stable source, five passing controls, clean Ruff, and
zero BasedPyright findings.
T-023 remains V3/C3.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
