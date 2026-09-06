---
type: is
id: is-01m1v5aqasqkmfh9qwg24fxerd
title: Prove the two-core endpoint theorem for the T-018 dilation family
kind: feature
status: open
priority: 1
version: 2
labels:
  - mathematics
  - fractional
  - follow-up
dependencies: []
parent_id: is-01m1sn5t0dm6rjj200pw5p1b7a
created_at: 2026-09-06T10:48:21.080Z
updated_at: 2026-09-06T10:52:41.301Z
---
Nonblocking follow-up to T-022. At q*=sqrt(1+D^2)/(B(1+D)), the single concentric core loses strict containment only at the unique worst net midpoint. Audit a two-core averaging theorem there: average the two tied net-core indicators; each contributes at most 1/2 on a unit-square edge and zero at vertices, so an interior-disjoint family has pointwise summed multiplicity at most one while each averaged core has T-018 mass at least one. This may prove endpoint no-fit; compactness of finite square packings would then imply s(11)>S*, but no explicit epsilon. Acceptance: fully state/prove uniqueness of the worst gap, exact boundary coordinates beta=(1-D)/(2(1+D)), local edge-incidence/multiplicity lemma, irrational-scaling measure semantics, all Condition-5 boundary premises, compactness/attainment step, and independent adversarial review. Keep it outside T-022 until reviewed; never claim an explicit improvement without one.

## Notes

Independent max-level read-only audit 2026-09-06: viable, no blocker if kept outside T-022. With h=D and half-tangents u_k=k h, the kth half-gap tangent h/[1+k(k+1)h^2] decreases, so only k=0 is worst. At q*, b*=sqrt(1+D^2)/(1+D); tied cores at relative angles +/-atan D touch each edge at distinct offsets +/-beta, beta=(1-D)/(2(1+D)) in (0,1/2). Their averaged indicator is 1/2 at each contact and zero at square vertices. For interior-disjoint convex squares, a point inside one has no other contribution; off all interiors, at most two edge-relative-interior incidences contribute and vertex incidences contribute zero, hence summed averaged indicators <=1. Push the finite atomic measure forward by irrational q*; inverse dilation preserves closed-core membership and Condition 5 mass. Integration gives 11 <= total mass < 11, proving endpoint no-fit. Compactness of labeled centers/angles with closed containment and nonoverlap then gives s(11)>S*, but no explicit epsilon. Needs durable proof packet and separate adversarial review before promotion.
