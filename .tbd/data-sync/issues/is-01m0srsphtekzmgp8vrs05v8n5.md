---
type: is
id: is-01m0srsphtekzmgp8vrs05v8n5
title: Certify the escape from Stromquist's printed Figure 14 point set
kind: bug
status: closed
priority: 0
version: 6
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies:
  - type: blocks
    target: is-01m0srspsyjecv6bdatrx8r5bx
parent_id: is-01m0p4bxnqxb8dsv2rnqgyp0w8
child_order_hints:
  - is-01m0sy843b4a9shhdsynyct6nb
  - is-01m0t0t4pshb047zr7j052t1we
created_at: 2026-08-24T11:34:24.057Z
updated_at: 2026-08-24T14:10:25.788Z
closed_at: 2026-08-24T14:10:25.787Z
close_reason: Exp-016 exact-replays the source-bound strict side-10001/10000 escape from all twelve printed Figure 14 points, localizes the failing Lemma 4 cell, retains eleven mutation controls and source hashes, terminally refutes H-010 without rejecting the numerical lower bound, and now replays in the focused gate.
resolution: null
duplicate_of: null
---
Soundness/source-proof gap. The printed twelve-point Figure 14 set appears avoidable: an open square of side 10001/10000 with tan(theta)=27/10 and a declared exact center avoids all twelve printed points inside the claimed container. This invalidates the published unavoidability subclaim and therefore the printed proof chain, but does not by itself refute the lower-bound theorem because a nearby repaired point set may restore the argument. Acceptance: bind the printed P12 tuple to the primary page; replay the witness with exact or outward-rounded interval arithmetic and strict open-box semantics; independently verify containment and avoidance margins; localize the uncovered proof cell; terminally record H-010 against its original claim; log the defect without calling the theorem false; and retain a mutation that makes the witness fail.

## Notes

2026-08-24 independent 80-digit and symbolic replay: L=10001/10000, tan(theta)=27/10, center=(37L/(2sqrt829),11/8) is container-feasible with its left support at x=0. Every printed P12 point has one local-coordinate avoidance margin >0; minimum is about 4.93957e-5 at G, next 7.96539e-5 at A1. SymPy certifies each selected radical expression positive. Awaiting retained exact checker and independent replay before terminalizing H-010 or promoting D-152.
