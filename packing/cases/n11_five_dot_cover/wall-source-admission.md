# Wall Constructor Source Admission

**Readiness addendum:** Both requested controls passed with the corrected source in
Session115 (12 focused tests); the half-side forwarding defect is fixed.
No target geometry was evaluated during these controls.

**Original review verdict:** Mathematical GO for the frozen q, B, and complete
sixteen-class driver.
Finish the two narrow readiness controls below before target freeze.
No new geometric engine or change to H143 is required.
This review inspected the implementation and tests under
`/private/tmp/squares-wall-constructor/`; it did not evaluate owner-class geometry or
run a target. Sol’s eleven passing tests and clean Ruff/BasedPyright are reported
validation, not runs performed by this reviewer.

## Verified Implementation

`validate_owner_manifest()` compares the full direction and branch records to the frozen
generators, then checks exact unit rotations, complete indices and provenance, and all
1444 distinct signed rays.
`retained_owner_frames()` selects every ray in the exact closed endpoint wedge.
The wedge width is below pi, so the cross-product selection and comparator are valid
even across the final sector’s angular wrap.
Boundary rays remain in adjacent classes.

`closed_centre_set()` builds K in world coordinates, clips against the world-coordinate
anchored quarter, and takes a hull that preserves points and segments.
The reused production clipper keeps nonempty degenerate intersections through its
remaining half-plane operations.
It is the appropriate helper for this boundary policy.

The support bounds use max minus h and min plus h on both orthonormal axes.
The world-coordinate reconstruction is correct.
Every nonempty centre set, including a point or segment, reaches the support
calculation. The standard caller creates a complete frame record and the combiner
intersects all allowed rectangles.

Exact nesting and positivity precede the shoelace area comparison, so strict area gain
decides proper inclusion.
All-empty completed frames give class impossibility; a timeout inside a class returns a
partial manifest containing only previously completed classes.
An empty retained-frame list or failed geometry invariant is invalid.
There is no path from a partial current class to a reported impossible class in the
driver.

## Two Required Readiness Controls

1. **Exercise degenerate K-intersections through the public wrapper.** The current
   dimension test calls `convex_polygon_intersection()` directly, while the wrapper test
   has a positive-area answer.
   Add `closed_centre_set()` fixtures with q=4, h=1, and ray `(1,0)`: mark `(0,0)` must
   return the point `((1,1),)`; mark `(0,1)` must return the segment with endpoints
   `(1,1)` and `(1,2)`. These catch a replacement with area-only clipping at the actual
   constructor boundary.
   They are the wrapper controls already required in the admission addendum.
2. **Make every tested allowed-frame intersection matter.** In
   `test_class_completion_keeps_degenerate_frames_and_distinguishes_impossible`, all
   nonempty frames currently contain the identical rectangle.
   Skipping any of them passes that test.
   Use two distinct rectangles whose intersection is the old footprint, with either
   omission giving a strict enlargement.
   For example, with old `[0,1]^2`, intersect `[-1,1]^2` and `[0,2]x[0,1]`. The result
   must be `[0,1]^2`, with `proper_inclusion=false`. Retain the empty and
   degenerate-frame disposition checks.
   This directly tests the consequential universal quantifier over feasible frames.

These are additions to existing focused tests, not a request for another test suite.
Once they pass on the frozen source, proceed to the all-sixteen discriminator.

## Small API Defect Outside the Frozen Target

At `wall_owner_footprints.py:384`, the call to `endpoint_footprint()` omits `half=half`,
although `wall_owner_footprint()` accepts a custom half-side.
Therefore a nondefault helper call compares the newly constructed footprint to an old
footprint at the default B. Pass `half=half` through.
The actual sixteen-class CLI uses the frozen default and is unaffected; this is not a
mathematical blocker for that target.

The combiner also assumes its frame records come from the standard constructor.
Its filter silently omits an `allowed` record with no rectangle when another rectangle
is present. The current caller cannot construct that combination.
If this helper becomes an independent receipt consumer, reject inconsistent records
before filtering; that future use is outside this first discriminator.

Keep the 128 containment matrices in the subsequent phase.
This constructor establishes geometry and exact nesting; a strict gain is not yet an
extension of the five-dot certificate or a global bound.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
