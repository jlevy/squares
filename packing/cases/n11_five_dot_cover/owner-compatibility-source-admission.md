# Saved-Escape Owner Compatibility: Source Admission

**GO, 2026-09-09 17:48 UTC.** The reviewed source implements the frozen BC320
saved-escape discriminator soundly.
No required source correction remains.
This is source admission after the separate mathematical design admission; it is not an
exp150 result. No target compatibility, cover, containment, or escape computation was
invoked during this review.

## Reviewed Surface and Controls

The review covered the shared working files below.
These Git blob identities record the exact source admitted before publication.

| Repository-relative file | Reviewed Git blob |
| --- | --- |
| `packing/devtools/wall_owner_escape_compatibility.py` | `69fd83abec2f2d4f86d6282e271100b5d39e49da` |
| `packing/devtools/wall_owner_selected_cover.py` | `6761a0c62c7b562aae552efe2cf2745aef5fd147` |
| `packing/devtools/wall_owner_containment.py` | `8abfc49e25d351d5b97ab6181024ed56feac1f02` |
| `packing/tests/test_wall_owner_escape_compatibility.py` | `8de6589170a1d462061ff7c40b8448a49db009e3` |
| `packing/tests/test_wall_owner_selected_cover.py` | `4946e51ce7eb5976c075919ba13769970aa8481b` |
| `packing/tests/test_wall_owner_containment.py` | `3cf7375c00027e2e4f337332921d6f5c92854355` |

The reviewer independently ran these three test modules with the project Python 3.14:
**21 passed in 4.53 seconds**. The independent exact-arithmetic fixtures also passed.
Their adversarial cases cover minimum versus maximum projection, strict tangency,
oblique H/V class transport, universal nonpositive slacks, a last-frame positive
witness, and point/segment centre sets.
The implementation lane separately reported BasedPyright with zero errors.

The source review found one consequential deadline defect, now corrected: final expiry
could previously escape as invalid or miss the acceptance boundary.
Both top-level complete outcomes now check the shared deadline and return partial with
the accumulated class rows on expiry.
The synthetic driver control exercises that final acceptance downgrade.

## Mathematical Findings

The optimizer uses

$$\delta(n)=n\cdot x-\min_{z\in Z}n\cdot z-\rho_o(n)-\rho_r(n).$$

The minimum has the correct existential-owner-centre direction.
All eight signed owner/residual SAT axes are evaluated, with exact rational support
radii and a deterministic world-coordinate minimizing vertex.
A frame is compatible only when its maximum is strictly positive; zero remains contact.
Degenerate nonempty Z sets are retained.

Corner placement is BL=I, BR=H, TL=V, TR=R. Reflections exchange the transformed ordered
axes to preserve a right-handed frame and the positive displacement box.
The original local class label is preserved.
Positive replay reconstructs Z, checks the canonical displacement coordinates,
transports the centre and mark consistently, verifies the closed B-core container, and
independently checks strict polygon SAT.

A universal class result requires the complete retained frame list.
It independently reconstructs each Z again and recomputes the maximum from explicit
square-vertex projection intervals.
The latter maximum is sufficient because every signed gap is affine in the owner centre,
so its maximum over a convex Z occurs at a vertex.
The replay must match every stored frame maximum and the full class maximum.

The result quantifiers are correct: the first incompatible class accepts the one-pose
hypothesis; four individually compatible class witnesses refute it; a partial traversal
proves neither. Evaluation order is TR, BL, BR, TL. A compatible class retains only its
observed prefix maximum and leaves its global maximum unset.

## Input Authority and Execution

The CLI binds a clean implementation revision and the exact endpoint, wall, and
selected-cover receipt blobs.
The exp149 reader requires the completed first-direction refutation for tuple (0,0,0,7),
consistent frozen settings, selected polygons, source links, area accounting, and saved
orientation. It replays the saved centre against the open residual container, five dots,
and four selected patches before compatibility.
It performs no new union-area search.

The wall loader compares all sixteen class identities and settings and the entire
ordered generated frame provenance: rays, canonical indices, quarter-turns, and folded
sources. For possible classes with a wall polygon, it additionally reconstructs each
closed centre set exactly.
This is stronger than the earlier design contract’s reliance on the admitted exp146
constructor for Z completeness.
Selected empty, unresolved, or incomplete classes are refused; there is no vacuous
acceptance.

The shared 90-second internal budget begins after loading and covers saved-escape
replay, geometry, witness/universal replay, and the final decision before return.
JSON serialization, fsync, and atomic publication occur afterward under the 120-second
external process bound.
This states the exact scope of the contract’s final-result wording; no additional
publication-time downgrade is required.
Cooperative timeouts retain completed rows in a partial receipt.
External termination can leave no JSON and must be recorded through process status and
receipt absence. Fresh-output guards prevent overwriting an input or writing into
code/test trees.

## Limits on the Inference

Both residual and owner squares here are B-cores.
Exhaustive finite-frame exclusion has physical relevance through the previously admitted
snapping and owner-selection premises; 181 frames are not a substitute for an unproved
all-angle unit-owner claim.
Positive examples establish only individual feasible snapped cores.
They do not establish unit parents, joint owner compatibility, or a packing.

An incompatible class excludes this saved residual pose.
A strictly negative full maximum also excludes a neighbourhood; a zero maximum gives
only the exact-pose conclusion.
Neither outcome excludes the owner class or the entire tuple, establishes a five-dot
cover, resolves H146, or changes T023’s grade by itself.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
