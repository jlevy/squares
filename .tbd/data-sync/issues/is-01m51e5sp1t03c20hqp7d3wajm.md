---
type: is
id: is-01m51e5sp1t03c20hqp7d3wajm
title: "Import ofitzharding: complete Lean proof of s(19) optimality (#640)"
kind: task
status: in_progress
priority: 1
version: 7
delegate: ecstatic-edison-intake-1016
labels:
  - result-import
dependencies: []
parent_id: is-01m51e5r3sg4h1wcrh7c826v7b
child_order_hints:
  - is-01m51fazgfznhff7cbtrpwp0s3
  - is-01m51fb0dmzb511d3zxfjv14m3
hold: null
hold_until: null
created_at: 2026-10-16T04:05:28.896Z
updated_at: 2026-10-16T04:56:51.528Z
started_at: 2026-10-16T04:05:36.664Z
---
Stage 1 triage of jlevy/squares#640 (ofitzharding, Oscar Fitzharding, "Complete Lean proof of s(19) optimality: registration request", opened 2026-10-16T03:41:08Z, labelled `intake`, no comments when read at about 04:20Z). Intake pass 2026-10-16 (epic think-mdnn), read-only: nothing was built or run, and nothing of the source is retained yet.

## Pin

- ofitzharding/sq19 at 34fb2b7bc39465db368c45cb48d4db58829d3051 (committed 2026-10-16T03:20:12Z), the head and the commit the issue pins; tag v1.0.0 points at it. The repository was created 02:19:07Z; the proof is in its first commit, 0ffc604f7b79a6d113d575aa95c5560a9daa1d66 (02:15:45Z), and the five later commits change only README.md, scripts/verify.py and verification/kernel-replay.json. Tree: 243 files, 3,360,904 bytes (89 Lean modules under Sq19Lean/, 137 certificate modules under s19/certificates/, scripts, expected/, verification/).
- Release v1.0.0 (published 2026-10-16T02:38:08Z): SHA256SUMS (475 B, SHA-256 218f59d01bf21cbb850574cdf077ce632caf05a6bc7e12f8daa15a20f5fc2751, downloaded here) and five archives of generated certificate sources, 1,110,588,236 bytes together, whose digests in SHA256SUMS equal GitHub's asset digests: sq19-generated-census.tar.xz 296,168,032 B (507ac095...), sq19-generated-S3435.tar.xz 520,505,480 B (9c919f68...), sq19-generated-S3438.tar.xz 73,115,752 B (ec769208...), sq19-generated-S3442.tar.xz 113,206,288 B (641a76a8...), sq19-generated-survivors.tar.xz 107,592,684 B (0c134b59...). expected/generated-sources.sha256 (SHA-256 34d31ea1...) lists the 2,112 files they extract to; scripts/fetch.sh checks both. The archives were not downloaded here.
- SHA-256 of the statement-bearing files at the pin: Sq19Lean/Assembly/Optimality.lean 26358beb65fa85c7c5b13a6f2eb0015e9128be0b1f9af80974dca07c8038dbad, Sq19Lean/Assembly/PlainPacking.lean addd5d5900b27a5579e9e43f28a3958829dea34998a203d7f54cbeb2272b089c, Sq19Lean/SquareBase.lean 2799b499078dbf44ac94fcab6363d8e9717ad9c3eb7e2c47e420624ec9619bca, Sq19Lean/Basic.lean 202c139f565cd061352cd93b793c51428991d9528885519232bc3d90848aa3a0, Sq19Lean/EndpointPacking.lean 935f8dc14755f776226e2ad1cb1ef74d029c9b1435bbd477c0c131fc76da5e80, verification/Square19Optimality.log bfe8c69fd7ddcecaeed52e95b31cf8a8a6a913eda5b631b53b4a1c28c0ef9b37, expected/axioms.txt 84367f34dae85905be43339f1155e019fe8ba8864d5c34c4696fa9fdfba0fd8e, expected/statement.txt 0d26ff0afff12e7e8da8d2888043ddbf2f32a1fd1b3fb5b8fb5170c53e01863e, verification/kernel-replay.json 2d49a318844053b7f022eff39456b446887c66770b46563d739791d510e22975, scripts/verify.py 8bed6f6a736e41fb8a1c4a0fdc89b7e2756742f5c66231bc1d9688b5003619cf, lakefile.toml 73b785763a8a9adf..., lake-manifest.json b86789363df42289....
- Build pins: Lean 4.34.1 (lean-toolchain), Mathlib v4.34.1 (d13f23b723b8a846827a245b89c10fc7d3f11612), and sq17-lean at 0a7167efa8dcae7fa73855890630fb7e2de550ed (its v1.0.0, the commit T-154 cites), whose Sq17Lean modules the lakefile compiles in place as the half-plane checker. The fitzharding-n17-lean-2026-10-13 packet pins e6ee548, whose tree differs from 0a7167e only by CITATION.cff, with every module's SHA-256 in its manifest.json.
- Licence: MIT ("Copyright (c) 2026 Oscar Fitzharding"); CITATION.cff names Oscar Fitzharding, version 1.0.0, released 2026-10-16.

## Every claim

1. `Sq19.square19_optimality (L : ℝ) : Feasible19 L ↔ 3 + 4 * Real.sqrt 2 / 3 ≤ L`: nineteen closed unit squares, each `sq cx cy ux uy` with ux^2 + uy^2 = 1 (any centre and rotation), inside [0, L]^2, with pairwise disjoint interiors, fit exactly when L >= 3 + 4 sqrt 2 / 3 = 4.88561808316412673..., Robert Wainwright's 1979 side. Existence at the endpoint (endpoint_packing, EndpointPacking.lean, no native_decide in that file) and impossibility below it, with no certificate-acceptance or case-exclusion premise.
2. Trust boundary (verification/Square19Optimality.log, expected/axioms.txt, 4,323 lines): propext, Classical.choice, Quot.sound and 4,320 `..._native.native_decide.ax_1_1` facts, no sorryAx (counted here in the log). Lean's compiler, native evaluator and C toolchain are trusted; scripts/verify.py compiles six *Fast checker modules to C and links them into the library native_decide runs.
3. Kernel replay (verification/kernel-replay.json): LeanChecker.replayFromImports over the theorem's 13,143-module import closure, Mathlib included, 0 failures (project modules 2,400 in 12m57s, Mathlib and standard libraries 10,744 in 24m04s, 64 cores), on the compiled objects of the research build of 15 October; a smoke test of scripts/verify.py --kernel-replay on 16 October. A kernel replay checks the proofs and takes the 4,320 native facts as axioms.
4. scripts/verify.py smoke-tested end to end (fetch and hash check, Lake build, native library, fresh rebuilds of every kind of certificate module byte-identical to the original); a complete from-scratch rebuild "takes several hours on 64 cores and has not yet been run".

## Map to the register

- n = 19 is open: reported and verified upper bounds 3 + (4/3)sqrt(2) (Wainwright 1979, Kingbird; E-lifted-q2-upper), conjectured optimum 4.88561808316412; lower bounds 193/40 = 4.825 reported and verified (wand125; E-n019-wand125-mixed-4825-*). No register entry claims s(19) optimality (the entries with 19 in scope, T-016, T-019, T-020, T-045, T-046, T-068, T-074, T-083, T-100 and T-103, are lower bounds), and no other issue on jlevy/squares claims it (#446 and #523 concern lower bounds and a census at 19). Green's reported s(19) lower bound (E-green-ds7-theorem10-reported-lower) is a blocker on the case, not an optimality claim.
- Statement binding, read here without a build: side19 = 3 + 4 * Real.sqrt 2 / 3 is the case's exact form 3 + (4/3)sqrt(2); Feasible19 is the record's problem (unit squares, independent rotations, disjoint interiors, touching allowed); sq and IsUnitSquare are copied from sq17-lean v1.0.0's SquareBase into the Sq19 namespace, and PlainPacking.lean's bridge rewrites them to Sq17.sq and containerBox. The theorem module Optimality.lean ends with #print axioms and says "Do not describe this as verified until this file builds against the complete census and all three accepted capture-state modules".
- Register action at stage 3: a new entry, s(19) = 3 + 4√2/3 = 4.8856180831641267…, an optimality value the record does not hold (runbook, the table's first row), proved in Lean, reported until a replay or a review moves it. T-154 took kind formalization because T-153 already held s(17); here no earlier claim holds 19, which the stage 3 lane settles by epistemics.md. Draft significance S5: it settles a case the record has open, as T-154 was proposed. Case record: n-019.md's status and lower lanes stay until the rungs say otherwise; the proof is linked from the case page, as asked.
- Novelty and priority: the first optimality proof at 19 the record knows of. Lineage, by the issue: Wainwright's 1979 construction; "extends the method and checker code of the s(17) Lean proof (#565)"; thanks to the Squares Project and Manasseh Ahmed. Whether it uses this project's n = 19 data (as sq17-lean used the n = 17 plan, T-154's review finding F-1) is for the review.
- Credit and AI, as the source gives them: "Credit: Oscar Fitzharding (@ofitzharding)"; "Development used Claude and Codex assistance" (issue); "Developed with substantial assistance from Claude and Codex." (README). The record's person entry for Fitzharding exists (credit-attributions.json, bibliography credited_names).

## Price

- Full from-source build with axiom check (scripts/fetch.sh, then scripts/verify.py): the source gives "several hours on a 64-core, 512 GB machine" and no CPU time, so about 190 to 380 CPU-h if the cores are busy for 3 to 6 hours (an estimate, not a receipt). With --kernel-replay, at most about 40 CPU-h more (37 wall-minutes on 64 cores). HELD: above the owner's 40 CPU-h cap, and it needs a machine of hundreds of GB; this host has 4 CPUs, 15 GB and 16 GB of free disk. T-154's full build (think-r109) waits on the same kind of budget.
- Subset under the cap (proposed; runs on the owner's word): fetch.sh's download and hash check of the five archives and their 2,112 files (1.11 GB download, minutes of CPU; unpacked size unmeasured, sq17's archives unpacked 3.6x); the existence half alone, `lake build Sq19Lean.EndpointPacking` with Mathlib's cache and its #print axioms (unmeasured, an estimate of an hour or two of CPU), which needs no native_decide; and the statement-binding read above, done.
- Mathematical review: a tbd-strong-max lane at maximum reasoning in its own worktree, as T-154 had two; it starts once stage 2 retains the source (runbook stage 4, "Who reviews, and when"). Review bead under this one.
- Nothing here decides the theorem without the source's code: the 4,320 native facts are the certificate.

## Disposition (proposed)

Import. Stage 2: a packet fitzharding-n19-lean-2026-10-16 at 34fb2b7, retaining the hand-written tree (about 3.4 MB; the axiom log and expected/ gzip by the archive's rule) and pinning the release archives by size and digest, with a bibliography key [Fitzharding n19 Lean 2026]; not done in the triage pull request, since the key makes the site a release-impact candidate, which the stage 3 pull request carries anyway. Then the review lane starts, in parallel with stage 3, which registers the entry and links the proof from n-019.md. The full build waits for the owner's budget. The `n-19` label does not exist on jlevy/squares (gh label list, 2026-10-16); whether to create it and add it to #640 is the owner's.

## Draft acknowledgement (not posted; stage 7 posts it after the pull request carrying this triage merges)

@ofitzharding, thank you, and congratulations on the release. We have pinned ofitzharding/sq19 at 34fb2b7, which tag v1.0.0 names, and release v1.0.0's five certificate-source archives by the SHA-256 in its SHA256SUMS, which match GitHub's asset digests. In triage we read the statement and its definitions without building them: `Feasible19` is the record's problem at n = 19 (closed unit squares, any centre and rotation, inside [0, L]², disjoint interiors), and `3 + 4 * Real.sqrt 2 / 3` is the exact form the n = 19 case record holds for Wainwright's side. The axiom report lists the three standard axioms and 4,320 native_decide facts, and no sorryAx. Nothing in the record claims s(19) optimality, so this would be a new result for it. Next we retain the source in a packet, start a mathematical review of the proof, as your s(17) proof had, and register it as reported, with a link from the n = 19 case page. A full rebuild from source is above this intake's compute budget and needs a larger machine than ours, so it waits for the owner's decision; your offer to help with reproduction is welcome, and we will report here what is registered and what the review finds.

blocked_on: none

## Notes

2026-10-16 owner: track the public announcement of this proof, https://x.com/ofitzharding/status/2110935681597874374 (ofitzharding on X), with the repository https://github.com/ofitzharding/sq19 (v1.0.0, pinned 34fb2b7bc39465db368c45cb48d4db58829d3051 in #640). Record the announcement as a source of the #640 entry alongside the repo; add the repo to intake-watch.yaml.
