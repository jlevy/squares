---
type: is
id: is-01m51fazgfznhff7cbtrpwp0s3
title: "Validate: Fitzharding s(19) Lean proof (#640), full from-source build, axiom check and kernel replay (~190-420 CPU-h estimate; HELD)"
kind: task
status: in_progress
priority: 2
version: 5
delegate: codex@spud10.local
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m51e5sp1t03c20hqp7d3wajm
hold: null
hold_until: null
created_at: 2026-10-16T04:25:47.279Z
updated_at: 2026-10-18T08:51:43.103Z
started_at: 2026-10-18T08:47:56.005Z
---
Validation part of think-a4x3 (#640, Oscar Fitzharding's Lean proof that s(19) = 3 + 4 sqrt 2 / 3). Record-changing at 19 (a new optimality entry; rungs).

## Validation
- Claim: `Sq19.square19_optimality (L : ℝ) : Feasible19 L ↔ 3 + 4 * Real.sqrt 2 / 3 ≤ L` in ofitzharding/sq19 at 34fb2b7bc39465db368c45cb48d4db58829d3051 (tag v1.0.0), with release v1.0.0's five archives of generated certificate sources (1,110,588,236 B; SHA256SUMS 218f59d0...2751) and sq17-lean at 0a7167efa8dcae7fa73855890630fb7e2de550ed; axiom set of expected/axioms.txt (3 standard axioms and 4,320 native_decide facts, no sorryAx). Checker: Lean 4.34.1's kernel and compiler; the source's scripts/fetch.sh and scripts/verify.py.
- Run: from the stage 2 packet's pin, `bash scripts/fetch.sh` (downloads and hash-checks the archives and their 2,112 files), `python3 scripts/verify.py --kernel-replay` (lake exe cache get; lake build of the hand-written modules and the six native checker libraries; lean on the generated modules in dependency order; statement and axioms compared with expected/; LeanChecker.replayFromImports over the 13,143-module closure). Accept only VERIFIED with the statement and axiom set of expected/.
- Cost: the source gives "several hours on a 64-core, 512 GB machine" and no CPU time: about 190 to 380 CPU-h if 64 cores are busy for 3 to 6 hours (estimate, not a receipt), plus at most about 40 CPU-h for the kernel replay (37 wall-minutes on 64 cores, kernel-replay.json).
- Budget status: HELD (above the owner's 40 CPU-h cap of 2026-10-14; the 2026-10-16 pass names the same cap). It also needs a machine of hundreds of GB of memory; this host has 4 CPUs, 15 GB and 16 GB of free disk.
- Possible subset under the cap (proposed; runs on the owner's word): (a) fetch.sh's download and hash check alone (1.11 GB, minutes of CPU; unpacked size unmeasured, about 4 GB if like sq17's 3.6x); (b) the existence half, `lake build Sq19Lean.EndpointPacking` with Mathlib's cache and its #print axioms (no native_decide in that file; unmeasured, an hour or two of CPU estimated); (c) pricing the full build by compiling one generated certificate module with the native checker library and scaling by the 2,112 generated modules, as think-r109's notes propose for sq17. (a) to (c) need Lean 4.34.1 and the Mathlib v4.34.1 cache installed (several GB).
- Depends on: think-a4x3's stage 2 packet; an owner budget and a large machine for the full run.
- Done when: a VERIFIED receipt with the axiom list equal to expected/axioms.txt (and, with --kernel-replay, 0 failures) is committed on a branch this bead names and registered as replay evidence on the stage 3 entry (same-implementation: the source's build), or the owner dispositions the build.
- Machine note: not this host for the full run. Subsets (a) to (c) fit here outside a validation gate, disk permitting.

blocked_on: none

## Notes

2026-10-16 ~05:58Z OWNERSHIP TRANSFER by the owner's word to the overnight coordinator user-eb (epic think-hg5s): "We have some changes with the regularization and a couple other things from another agent that you should take over and incorporate into your work." The ecstatic-edison lanes should stop work on this bead and its branch, and record any unpushed state in a note here. user-eb's lanes fetch before every push and stop if the branch moved.

2026-10-18 W1 intake (think-xmxb): PR667 A9 pricing update: source clean rebuild at ofitzharding/sq19 c86a991ea1379d1598739182f5f26619c9b7126a reports VERIFIED,13143 modules,64vCPU x5h18m (about340 CPU-h). Replace old unmeasured190-420 range with this measured source basis when repricing; preserve machine scaling uncertainty. Full build remains held; no build here.
