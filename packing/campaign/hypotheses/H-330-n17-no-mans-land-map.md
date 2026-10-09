---
title: H-330 — the gap between exclusion reach and the terminal radius is confined to two directions
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-330
  kind: hypothesis
  claim: >-
    Let m be the side margin at which the whole-state engines exclude the family's own
    state (H-325). Along each of the 90 signed non-slider coordinate directions, let d_j
    be the displacement at which the fixed-feature LP side, with the other coordinates
    re-optimised and the sliders in their domain, first exceeds S* + m. Then d_j is at
    most the terminal radius of H-329's box (5e-3 in angles, 1e-2 in positions) for all
    but at most two directions, the exceptions being the softest, -omega16 and
    -omega11.
  lane: proof
  derived_from: [X-051]
  criterion:
    shape: determination
    metric: >-
      The 90 values d_j from the exact fixed-feature LP of the widened-projection scope
      review (19 chain pairs along their endpoint owner normals, 64 containment rows, the
      slider domain as rows), evaluated by bisection in d with HiGHS proposals and exact
      rational re-checks of the final duals, at the margin m H-325 reports.
    direction: >-
      Confirm when at most two directions have d_j above the terminal radius. More than
      two refutes the claim and names the directions capture must bridge by another
      argument.
    threshold: at most 2 of 90 directions above the terminal radius.
  instrument: >-
    Unbuilt: the scope review's LP probe (its scratch version is on no ref) rebuilt as a
    retained devtools module with exact dual re-checks, reading exp-244's kernel rows and
    the H256 slider domain.
  instrument_ready: false
  regime: >-
    n = 17; the exact root's frame; features forced; sliders in the H256 domain plus
    1e-2; the margin m from H-325, or the scan's four caps if H-325 stalls.
  instance: {axis: n, point: 17}
  priority: 1
  cost_estimate: One W7 slice to rebuild the probe with exact re-checks; 90 bisections of about ten LPs each, minutes.
  prereqs: [H-325, H-261]
  replication: false
  registered: '2026-10-09'
  notes: >-
    X-051's route D. The two capture readings of pilot 2 both predict what the receipts
    show; this map replaces that argument by a measurement of where the exclusion engines'
    margin meets the terminal theorem's radius, direction by direction. The two softest
    directions have slopes 0.0155 and 0.088 side per radian; at m = 1e-2 the LP side
    along -omega16 reaches S* + m only at about 0.65 radians, outside every box, which
    is why the claim exempts them.
---
# H-330: Mapping the No-Man’s-Land

**Mechanism.** An exclusion engine certifies a region empty when the side there exceeds
its cap by more than its losses; a terminal theorem certifies a region when it is inside
its box. Between the two is the region capture must bridge.
Along a direction with slope $\kappa_j$ the exclusion margin $m$ is reached at
$d_j\approx m/\kappa_j$, so stiff directions (slopes $0.2$ to $0.7$) are bridged at
$d_j\le5\times10^{-2}$ and the soft ones are not.
The map says which directions need which argument.

**Falsifier.** More than two directions with $d_j$ above the terminal radius.

**Expected information.** The shape of the capture problem: a few soft directions to
bridge by a second-order or feature-flip argument (H-339), with everything else inside
the reach of exclusion at a cap below $S^\ast$ plus the terminal theorem at $U'$.

**Limits.** The LP is the fixed-feature model; off the feature-forced region the true
side is larger, so the map is conservative there.
The margin $m$ is one engine’s on one state; H-325 supplies it or the scan’s four caps
stand in for it.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
