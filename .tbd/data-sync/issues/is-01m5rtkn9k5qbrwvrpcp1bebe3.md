---
type: is
id: is-01m5rtkn9k5qbrwvrpcp1bebe3
title: "Validate: Jatloe s(12) = 4 Lean proof (#810, T-243), from-source build of 5,377 modules and axiom check (~28 CPU-h, 17-40 by the source's receipts; gated on decision)"
kind: task
status: open
priority: 2
version: 1
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m5rs2qz5f6js86hpr6qmbgta
created_at: 2026-10-25T06:05:18.003Z
updated_at: 2026-10-25T06:05:18.003Z
---
Validation part of think-4l14 (#810, Jatloe's Lean proof that s(12) = 4, published by Manasseh Ahmed in Queuingtheorydotcom/Jatloe12SquaresFormalized). Record-changing at 12 (T-243, a new optimality entry, at V0/C0 when registered; the case's verified lanes and status).

## Validation
- Claim: `N12Compact.Final.optimality : S12.packingConstant12 = 4` in Queuingtheorydotcom/Jatloe12SquaresFormalized at d0caf4532a7ead68be1389ef87387b126fc2e0ab (tag n12-verified-2026-10-16), project Lean/Proofs/N12-jatloe; packet packing/resources/web/jatloe-n12-lean-2026-10-16/ (the statement closure, Compact/Assembly/ and the run's evidence retained; the other 5,249 closure modules pinned by the commit and by their Git blobs in receipts/lean-closure.json.gz). Accepted only with the axiom list of verification/run-38849916588/global-type-axiom-audit.log: propext, Classical.choice, Quot.sound and 1,624 native_decide axioms, no sorryAx. Checker: Lean v4.35.0's kernel and compiler (native_decide trusts the compiler), Mathlib 56a005855ea17e0b0958f73ec801ae140b0a1679; a build of the source is reproduction with the producer's code (same-implementation).
- Run: a checkout of the source at d0caf45, checked against receipts/lean-closure.json.gz (rerun devtools.lean_closure on the checkout and compare); elan with leanprover/lean4:v4.35.0; Mathlib at 56a00585 placed at Lean/Proofs/N12-jatloe/.lake/packages/mathlib with its dependencies, then `lake exe cache get`; `lake build Compact.Assembly.Final` from Lean/Proofs/N12-jatloe; then `lake env lean ../../../verification/run-38849916588/GlobalTypeAudit.lean` and compare its axiom list with the retained log. Keep the build log, each module's exit status, wall time and peak memory, and the axiom output as receipts in the packet. The producer's public workflow (.github/workflows/verify.yml, n12.yml, serial modules with 2 to 4 Lean threads) is the alternative route; run here it is the same build.
- Cost: about 28 CPU-hours, 17 to 40. Basis: the source's own per-module receipts, checked-modules.json in the release asset N12-jatloe-final-evidence-1.zip (SHA-256 db3447b212544e83028fdabd73cf3acd14b796e7ff977cbb899b6e7164b5d9f8, checked on download 2026-10-25): all 5,377 modules exit 0 with no rejected admission, 59,586.74 wall-seconds of serial module builds (16.6 h) and 138,504.10 Lean-thread-seconds (38.5 h), the longest module 248.25 s; `unzip -p N12-jatloe-final-evidence-1.zip checked-modules.json | jq '[.[] | .record] | {modules: length, wall_s: (map(.elapsed_seconds) | add), thread_s: (map(.elapsed_seconds * .lean_threads) | add)}'`. Setup (154 extra external modules, two package configs) and the final audit add minutes. The receipts' times are the producer's runner's (88 CPUs); not a run here.
- Budget status: gated on decision. Within the owner's 40 CPU-hour item cap (2026-10-14, think-lh7d) by the receipts, at the cap at the high reading: run with a stop at 40 CPU-hours, as think-v511 is. It waits on a machine whose memory holds the largest modules (peak memory is not recorded per module; the producer's runner had 170 GB free and bounded the build at 157,113 MiB) and on the pass's decision to start a run of 17 wall-hours or more. Triage on 2026-10-25 and the tracking issue's text called it far above the cap; the receipts say otherwise.
- Possible subset under the cap: the 109-module statement closure of S12.PackingConstant, all retained in the packet, with a probe printing UnitPacking, OpenSquare.Inside, feasibleSides and packingConstant12 and the axioms of gridPacking and packingConstant12_le_four: 9.4 wall-minutes and 37.5 thread-minutes by the same receipts, plus the Mathlib cache. It decides the statement and the grid in Lean and moves no rung; it belongs to the statement audit if that lane wants a build.
- Depends on: the statement audit (another lane, docs/project/reviews/) reading the theorem as s(12) = 4; a machine with known memory; the pass's word.
- Done when: the receipts are committed in the packet on a branch this bead names (every module exit 0; the axiom list equal to global-type-axiom-audit.log's), a replayed-here evidence entry (proof-assistant-checked, relationship same-implementation, build_receipt and axioms_receipt, the build's programs registered in frontier/verifiers.yaml) is cited by T-243, the unfinished_confirmations item naming this bead is removed, and devtools.check_results re-derives V and C with the accepted review.
- Machine note: this host (4 cores, 15 GB, 20 GB free disk on 2026-10-25) would take 17 wall-hours or more and may not hold the largest modules; the build writes about 3 GB of objects on top of the toolchain and the Mathlib cache (about 7 to 10 GB). Do not share the machine with a validation gate.

blocked_on: none
