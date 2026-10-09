---
title: H-329 — an exact dual-sheet certificate proves the widened projection theorem over the feature-forced angle box
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-329
  kind: hypothesis
  claim: >-
    Every packing of 17 unit squares of side at most U' = 935106018721/200000000000 in
    the family's occupancy state whose sixteen non-free angles lie within 5e-3 of the
    family's (H254 lifts), whose centres lie within 1e-2 of the family's in the exact
    root's frame, and whose sliders lie in the H256 domain widened by 1e-2, has S >= S*
    with equality only on the family; and this is certified by at most 10^5 direction
    patches on the sphere of the seven backbone angles, each carrying an exact rational
    dual basis of the fixed-feature LP whose sheet S_B(psi) is bounded below by S* over
    the patch by an outward interval bound on its second derivative.
  lane: proof
  derived_from: [X-051]
  criterion:
    shape: determination
    metric: >-
      First the patch counter of the capture R9 review, section 7: 2,000 sampled
      directions at four radii, the distinct optimal bases, the Chao1 estimate of the
      total basis count, and the least sampled slope. Then the exact build: for every
      patch, nonnegativity of the parametric dual on the patch, the slope, the interval
      second-derivative bound, and the inequality S_B >= S* on the patch; the nine
      non-backbone angles by the one-dimensional wall-weight check; the 135 unavailable
      options forced negative throughout the box (H-278's forcing extended to the box).
    direction: >-
      Confirm when the Chao1 estimate is at most 1e5, no sampled slope is negative, and
      the exact build covers the sphere with every patch certified. A negative sampled
      slope, or an estimate above 1e5 with singletons above half the sample, refutes the
      patch route for this box and selects a smaller box or a different certificate.
    threshold: Chao1 <= 1e5; least sampled slope > 0; complete patch cover; every patch exact.
  instrument: >-
    Unbuilt: a patch counter over the fixed-feature LP (numerical, HiGHS proposals), then
    an exact certifier using exp-244's kernel and duals with interval Krawczyk solves
    and outward rounding, as the widened-projection scope review specifies; the
    feature-forcing extension of devtools/check_n17_local_minimum.py's option margins to
    the box.
  instrument_ready: false
  regime: >-
    n = 17; the exact root's frame; the family's state; cap U'; the slider domain of
    H256 plus 1e-2; square 6 coarse and absent from every row; angles as H254 lifts.
  instance: {axis: n, point: 17}
  priority: 1
  cost_estimate: >-
    Patch counter: one W7 slice plus review, 8,000 LPs in minutes. Exact build: one
    slice plus review; a CPU-day at 10^5 patches under a second each.
  prereqs: [H-261, H-268, H-278, H-288]
  replication: false
  registered: '2026-10-09'
  notes: >-
    X-051's route C and the record's candidate C4, made a registered claim. The
    exploratory LP evidence: all 32 coordinate slopes positive from 1e-5 to 3e-2
    radians, softest 0.0155 per radian along -omega16, sheet curvature of order 0.3 per
    squared radian against the 33 that fixes H-261's radius. The certificate is a list
    of exact rational duals and is the kind of object a foolproof proof wants. Nests
    inside H-261's bead until it certifies; a certified instance supersedes the 1/5000
    theorem as the terminal target.
---
# H-329: The Terminal Theorem as an LP Certificate

**Mechanism.** Where the 135 unavailable owner-axis options stay negative, every contact
pair is separated along an endpoint feature, so nonoverlap and containment are linear in
the centres and the side at fixed angles.
The side at fixed angles is then an LP value, a minimum of dual sheets, and the theorem
is that every sheet stays above $S^\ast$ on an angle box.
The sheets are nearly linear (slopes constant to three digits over three decades of
radius), which is why a first-order patch argument with an interval remainder can cover
a box fifty times larger than the ratio test’s.

**Falsifier.** A sampled dual sheet with negative slope inside the box, in particular
along the co-moving 11/12 direction; a patch estimate above $10^5$ under dual degeneracy
at the apex, where the optimal face has dimension about 17; or a centroid option margin
failing along the slider family.

**Expected information.** Whether the terminal region can be made large enough that
capture needs to deliver angles to $5\times10^{-3}$ rather than $2\times10^{-4}$, which
no engine has done either but which is a target the exclusion engines’ own margins come
close to (H-330).

**Limits.** The frame, cap and $u^\ast$-enclosure obligations of the composition review
are unchanged; square 6 stays coarse; the outer route from the cells is a separate
obligation; soundness is the exact build’s, and the counter certifies nothing.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
