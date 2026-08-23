---
type: is
id: is-01m0r516kvkaaa5bbf9nm948qa
title: Calibrate endpoint identity independently of the D-021 side floor
kind: bug
status: open
priority: 0
version: 1
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - pr-14
  - ambiguity
  - numerical-identity
dependencies: []
parent_id: is-01m0qxpb7634zbzt638d239jks
created_at: 2026-08-23T20:29:43.930Z
updated_at: 2026-08-23T20:29:43.930Z
---
PR #14 ambiguity 3. D-021 bounds error in the polished side objective; it is not a metric or resolution theorem for high-dimensional endpoint identity. The current closest_pair is only a side gap, while identity also uses a 1e-6 pose quantum and 1e-9 contact tolerance. Distinct configurations may have exactly equal side and one connected family may span many geometric keys. Acceptance: rename or document the side-gap diagnostic honestly; add quotient-space pose distances, contact/active-set disagreement, and interval enclosures; sweep quench tolerances, identity quantums, and repeated deterministic runs to find a stability plateau; represent unresolved equality as an ambiguity graph rather than forced merge/split; certify separations when interval enclosures are disjoint; and report basin/component counts as intervals whenever ambiguity remains.
