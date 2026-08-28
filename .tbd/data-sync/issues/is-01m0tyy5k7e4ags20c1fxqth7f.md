---
type: is
id: is-01m0tyy5k7e4ags20c1fxqth7f
title: Bridge numerical witnesses to exact or interval-certified certificates
kind: task
status: in_progress
priority: 1
version: 15
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-28-numeric-symbolic-round-trip.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m0typjn7s866m042zsemybj6
child_order_hints:
  - is-01m0vjynw583941h5xyg5d3n1s
  - is-01m131tt5pc69dm47zxy5n3s58
  - is-01m131v6jfzt21ggvn3ngskjgr
  - is-01m131v6x68y5sdrap8s7zyv0a
  - is-01m132naa53qc03r9k0gjv135x
hold: paused
hold_until: null
created_at: 2026-08-24T22:40:56.422Z
updated_at: 2026-08-28T02:26:39.338Z
started_at: 2026-08-27T07:58:10.864Z
---
Build honest promotion paths from decimal or SVG witnesses to formal evidence: robust exactification to rational or algebraic data, possibly at an explicit relaxed side, and outward-rounded interval existence certificates for suitable contact systems. Higher decimal precision plus tolerance is not promotion. Return a certificate or a typed source, importer, checker, field-precondition, or mathematical blocker. Demonstrate on a high-value witness such as n=29 when possible, without promising that arbitrary poses or the reported value can always be certified.

## Notes

BC-032 frozen 2026-08-27 00:57 PT: run the retained n=11 center-angle witness through existing robust-rational promotion at rational_digits=36 and max_side_increase=1e-8. Accept only a complete 11-id/55-pair artifact with source_side < generated_side <= source_side+cap, generic exact replay and devtools.check_rational_witness_independent both passing, cap-zero/incomplete/overlap mutations rejecting, and limitations denying source-decimal exactness, record improvement, rigidity, and optimality. This is tool validation only. Kingbird n=29 remains typed contact-system/checker blocker; no generic interval work enters this slice.

Paused: BC-032 bounded n=11 robust-rational control completed 2026-08-27: generator-owned known-best-derived artifact passes generic exact and independent Fraction replay for 11 ids/55 pairs at a strictly positive side relaxation below 1e-8; seven focused mutations and the exact-verification gate pass. This is tool validation only, not source-decimal certification, Trump algebraic equivalence, record improvement, rigidity, or optimality. Resume only with an explicit n=29 contact system, isolation boxes, outward-rounded certificate contract, and independent checker.
