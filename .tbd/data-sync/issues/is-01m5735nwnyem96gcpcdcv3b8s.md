---
type: is
id: is-01m5735nwnyem96gcpcdcv3b8s
title: "Import Daniel: Lean Ryu bound c*(k) <= 8 ceil(sqrt(k-4))-1 (no issue)"
kind: task
status: in_progress
priority: 2
version: 3
delegate: c-lean-1023
labels:
  - result-import
dependencies: []
parent_id: is-01m572ssbx1x412zpvsw1sb6je
hold: null
hold_until: null
created_at: 2026-10-18T08:48:37.268Z
updated_at: 2026-10-23T08:27:55.425Z
started_at: 2026-10-23T06:19:00.734Z
---
W1 intake 2026-10-18, parent think-xmxb. evand/square-packing 8475bdf41571c59c8c240aedaddc48e19e0e4707. lean/Sqpack/RyuBand.lean and RyuBound.lean claim packs_sub_8sqrt and packs_sub_8b for k>=6, standard axioms and no certificates. A second formalized derivation of Ryu bound #471; map asymptotic register and exact strictness/count conventions. Retain/pin sources, price kernel rebuild; independent mathematical review starts with complete packet. No CPU-hour build authorized.

Full source commit inventory retained in packing/campaign/issue-intake/intake-20261018/. Stage0 owned; triage before retention/replay. Budget status: no CPU-hour replay authorized in this pass. Draft acknowledgement/public issue only after significance and report identity are settled (S4+ requires tracking issue). Done when every claim is mapped and imported or reasoned non-import, replay/review individually priced and owned, and source/report is answered after publication where applicable.
blocked_on: none

## Notes

2026-10-23, c-lean-1023 (stages 1 to 3), branch claude/intake-2026-10-23-lean-sources.

Stage 1. Pin: evand/square-packing 8475bdf41571c59c8c240aedaddc48e19e0e4707 (2026-10-18T02:17:40Z), MIT. Claim: UnitSquarePacking.Ryu.packs_sub_8sqrt (k : ℕ) (hk : 6 ≤ k) : ∃ s < (k : ℝ), Packs (k * k - 8 * (Nat.sqrt (k - 5) + 1)) s, and packs_sub_8b (2 ≤ b, b + 4 ≤ k ≤ b^2 + 4): Ryu's Theorem 1.4, c*(k) <= 8 ceil(sqrt(k-4)) - 1 for every k >= 6 (Nat.sqrt (k-5) + 1 = ceil(sqrt(k-4)) for k >= 6), Packs from Spec.lean (closed unit squares in [0,s]^2, disjoint interiors). No certificates; the commit message and tasks/fang-gluing/README.md say standard axioms. An explicit tilt t = 1/b + 1/((b^2+1)(6k+4b)) replaces Ryu's mean-value Lemma 4.2. Closure (devtools.lean_closure): Spec, Conjectures, ConjecturesProofs, ExactPack, FangGlue, RyuBand, RyuBound, Mathlib only, no kernel escapes.
Claim map: the asymptotic register's deficiency row (Theorem 1.4, from #471/#486); it settles no count n <= 324, so no register entry; the row's note now records the Lean proof as reported. Strictness: the theorem gives side < k, i.e. c*(k) < 8b, matching the row's "<= 8 ceil(sqrt(k-4)) - 1".
Stage 2. Same packet as think-57ei: packing/resources/web/evand-fang-ryu-lean-2026-10-18/, key [Daniel Fang and Ryu Lean 2026-10-18]. Packet pushed at 918d780b0; records at 1e22df80f (merged with main at 9ba8e7a85).
Price: under 0.5 CPU-hours (seven modules over Mathlib's cache), a few GB of memory, about 10 GB of disk; fits the lane's 2 CPU-hour limit but this host had 5.2 GB free disk, so not run. Validation bead think-dgrc (with Fang).
think-f8py / think-pf37 (claimed elsewhere): a645fe3, 4b456fe and 13da782 change RyuBand.lean and add RyuFill/RyuEnds/RyuLayers/RyuStair*, so each is a packet at its own revision, not absorbed here; the other closure modules are unchanged there, so their packets can pin them identical to this packet's copies.
Stage 4 review: owed, from the packet.
