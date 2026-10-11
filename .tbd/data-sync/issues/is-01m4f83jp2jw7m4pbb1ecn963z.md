---
type: is
id: is-01m4f83jp2jw7m4pbb1ecn963z
title: Prepare exact weighted-vertex screen and conditional n17 SOS pilot
kind: task
status: open
priority: 3
version: 4
delegate: claude-code@spud10.local
labels:
  - n-17
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-09T02:33:04.961Z
updated_at: 2026-10-09T10:55:27.979Z
started_at: 2026-10-09T03:28:53.760Z
---
Conditional successor to the first-eight shared-centre LP; no target has run. Use the PR454 exact-SOS strategy and the extended PR464 source assessment at docs/project/reviews/review-2026-10-08-n17-global-optimization-and-sos.md. Preserve the existing think-dvcs dependency.

After a certified LP survivor, freeze one triple of original convex centre cells using the specified exact ranking. Run the equal-weight vertex obstruction, then an exact weighted-vertex LP: alpha>=0, sum(alpha)=1, G alpha<=-epsilon with epsilon>0, where every row is reconstructed from a complete original product vertex. A positive exact certificate directly excludes the triple after original-cell/D4 composition and admission review. An exact mixture beta>=0, sum(beta)=1, G^T beta>=0 proves no weighted certificate and retires the entire no-ball/no-equality order-2 SOS ansatz for that triple; it proves no physical feasible triple. Numerical failure remains unresolved.

Readiness first: verify the forced-face degree proof, generator shapes, rational exposing identities and PSD/LDL factors, reduced-to-original Gram embedding, cross-degree zero rows and corrupted-exposure controls. Under exactly affine facets plus three incircle generators, reduced order2 uses31+28F Gram unknowns and84 coefficient rows; reduced order3 uses490+406F and462. At12facets order3 exceeds the2M dense-entry cap; actual facets must be counted.

If the weighted obstruction is certified, a separately frozen ball-augmented order-2 recipe is a plausible true SOS successor. Fix rational centre/radius coefficients and prove the ball covers the entire original domain, including point/segment cells. A quadratic ball invalidates the no-ball face reduction; at12facets its unreduced order2 system has854 unknowns and179340 entries. Passing counts does not promise a certificate or successful rational exactification. A reduced order3 alternative needs separate eligibility and registration.

Keep touching/endpoint, exact primal/mixture, complete vertex, singular-PSD, corrupted identity/weight, generator-mismatch and resource-stop controls. Existing ceilings remain10k Gram unknowns,2M coefficient entries,300s per eligible order including exact reconstruction,120s fresh checking,4GiB RSS,8MiB artifact and4096-bit rational coefficients. Keep the provisional6–12agent-hour implementation allowance until the readiness slice measures work. Freeze all source, generators, basis and controls before target execution. No full all17SDP, bound/admission claim from numerical infeasibility, or algebraic-field certificate implementation is part of this slice.

## Notes

2026-10-09T10:55Z 2026-10-09 W2 review on #473: on the 24-cell cover every one of 2,024 cell triples has a product vertex that is a feasible point of the triple's encoded system (all pairwise q >= 562823713/423200000), so no weighted-vertex certificate and no SOS infeasibility certificate exists for any triple at any order, with or without ball augmentation. This lane is refuted as specified. Recommend closing as retire-negative after owner review.
