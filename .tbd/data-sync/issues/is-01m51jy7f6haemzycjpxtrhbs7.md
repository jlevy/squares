---
type: is
id: is-01m51jy7f6haemzycjpxtrhbs7
title: "Import wand125: the Lean kernel proof of ValidTilt9, s(k^2 - 4) = k for every k >= 8 (2c75edc), a formalization of T-081 (#643)"
kind: task
status: in_progress
priority: 1
version: 7
delegate: user-eb-intake-residue
labels:
  - result-import
dependencies: []
parent_id: is-01m51hyxstsa9ptekd2ss26ksn
hold: null
hold_until: null
created_at: 2026-10-16T05:28:43.750Z
updated_at: 2026-10-18T08:51:43.753Z
started_at: 2026-10-16T05:28:49.870Z
---
Found in the 2026-10-16 intake sweep's read of wand125/square-packing (lane A of think-hg5s, bead think-mu5v, acting name user-eb-intake-residue); nothing on GitHub asked (no jlevy/squares issue names ValidTilt9 as of 05:40Z). Stage 1 triage only, read-only, from a blobless clone in the lane's scratch; nothing retained, registered or run yet.

## Source pin

wand125/square-packing (Hiroaki Hosono), head 319a779efcc78db2f92bffc87844446f8723b01d (tree 46d195db826de5ee1f5ae9109df41eee9d3c96fb, 2026-10-16T04:47:29Z). The result is in two commits: 2c75edc501e31468513bf818eceed082e8bb8767 (2026-10-16T03:25:10Z) adds problems/square-lower-bounds/certificates/k2m4_n77_L9/lean/ (56 files, 2,908,328 bytes at the head) and e99f5e39c3406ef85e7757a60fae895d25b49ccc (03:25:35Z) adds its four receipt logs. Both carry Co-Authored-By: Claude Opus 5.5. Licence: MIT (wand125), by problems/square-lower-bounds/LICENSE, which the root LICENSE.md says applies to folders without their own; the statement, reduction and certificate input are Evan Daniel's (MIT).

Release validtilt9-lean-v1 (tag at 0eb3fe5, the previous read) holds what is not in Git, digests from lean/receipts/ASSETS.sha256: v9-certs.tar.zst (109 MB, c40eed8bc57aca82824bcb9a00d8b8d37773b6258bc6e86aa171cd8a01774593, the 16,200 per-root certificates as pickles), SOURCES.sha256.zst (0367b0e78b60e654273442d27f92f4509e7d0bb5a3ea940f1a39aab6d70739fd; SOURCES.sha256 itself 5bce91b1232261b356fa0d16d94acdd51b05c275327f8b4c8a268d09e53270db, the sha256 of each of the 1,275,911 generated Lean files, which are not stored) and v9-logs.tar.zst (c3c856968207fd1482712efb5c0b1229572ca70fcb2088da695932fdaf0d29ab). The release's API metadata was not read: this session's gh is bound to jlevy/squares.

## Claims at the pin (every claim, in scope or not)

1. In scope. Sqpack/V9/Main.lean (generated, sha256 39f42605c45e3c084f5de66e900c2b3e862356bee756db5d730ef5e3dc0904f9) proves in namespace SquarePacking.LemmaELeaf: `theorem validTilt9 : Bentz4.ValidTilt9`, `theorem valid9 : Bentz4.Valid9 := Bentz4.valid9_of_tilt validTilt9` and `theorem bentz4 : ∀ k : ℕ, 8 ≤ k → minSide (k ^ 2 - 4) = k := Bentz4.bentz4_of_validTilt9 validTilt9`. Axioms (receipts/main.log, Lean 4.33.1 aarch64, commit 819816b): propext, Classical.choice, Quot.sound for all three; no sorry, no native_decide (each leaf and row group is `decide +kernel`). Main.olean as built 4a60a684ec935f3a16fd033e57f671926c0051e9501a64a6a64d4575eed6e442. That is T-081's finite premise ValidTilt9, which T-081 holds only as two reported runs (qx2_zm.py, E-k2m4-evand-validtilt9-qx2-report; wand125's checker, E-k2m4-wand125-validtilt9-report), now a kernel proof, and with the reduction (which this record built on 3 October, E-k2m4-evand-bentz4-lean-build) a proof-assistant proof of s(k^2 - 4) = k for every k >= 8.
2. Out of scope: 4c926da adds s△(46) = 10 + 2/√3 for unit squares in an equilateral triangle (lattice lower certificate; Joshua Wolk's packing as the upper bound); 574d27c and 319a779 put it in the source's triangle paper. Another container; nothing to register.
3. Not a claim: 0aa00f7 (INDEX.json and site data: theme #10 closed, the release listed); the k2m4_n77_L9 README's status line, which notes s(77) = 9 is the case k = 9 of the Lean theorem, from Daniel's certificate rather than wand125's own n77 cover.

## Statement binding, checked here (minutes)

- lean/library/library.sha256 lists 59 files (the 56 of Main.lean's import closure, lakefile.toml, lake-manifest.json, lean-toolchain). Every one of them that the evand-square-packing-2026-10-03 packet retains (packing/resources/web/evand-square-packing-2026-10-03/square-packing/s12/lean/, 19 files) is byte-identical to it: Basic.lean, S32.lean (where minSide is `sInf {s | Packs n s}`), Bentz.lean, Bentz4.lean (408b34d0..., bentz4_of_validTilt9), Bentz4Data.lean (02ff2aab..., box9Cover), BentzData.lean, BentzFam.lean, Chord.lean, Cover.lean, D4.lean, MixedMeasure.lean, S32Data.lean, ValidSplit.lean, ValidSplit9.lean (8424bc9c..., ValidTilt9 and Valid9), ValidSplitData.lean, ZeroMargin.lean, lakefile.toml, lake-manifest.json, lean-toolchain. So every definition the three theorems' statements use is the one this record's 3 October build of the reduction used.
- The other 40 files are proof machinery from evand/square-packing after 3 October (060c1a1, the merge of wand125's PR #6, which think-0ayk owns, to 44a105e), not retained here; the source says 51 are byte-identical to upstream 060c1a1..44a105e, and two are changed: library/Sqpack/RowMinN.lean (new, rmChk and rmChk_sound : rmChk … = true → rmLoop … = true) and LemmaEKM.lean (4-line diff, calls rmChk, no statement change), for kernel speed. Not compared here (needs evand at 060c1a1; minutes).
- Bridge.lean proves box9Cover_eq_mcoverP (Bentz4.box9Cover.measure equals the cover of Data.lean), and Tilt.lean proves validTilt_of_tree, so the cover's identity with K4_k008_box9.txt is inside the kernel proof. The certificates are new (run_v7.py per root, 9 roots by hand, 4 rebuilt with V7_TOUCH / V7_SGK options): they are proof data, and any error in them fails the kernel check rather than the statement.

## Claim map (result-import.md register table)

- "A proof in a proof assistant of a result the record already holds is a formalization" (epistemics.md, kinds; the kind exists since 2026-10-13, after the T-066 precedent think-xk3f, which was mapped as new evidence): one new `formalization` entry, proves_kind optimality, naming T-081, scope the cases T-081 holds at k >= 8: n = 60, 77, 96, 117, 140, 165, 192, 221, 252, 285, 320 (k = 8 to 18). It cites evidence of its own: a reported proof-assistant-checked entry (origin reported, the source's run; nothing replayed here). The alternative, an evidence update on T-081 with no new entry (the think-xk3f mapping), is for the registering lane to weigh; the kind rule reads as the formalization entry.
- Other holders: T-081 (Daniel's theorem, V0/C1, S4); T-062 (s(60) = 8) and T-067 (wand125's s(77) = 9, first published 1 October) hold k = 8 and 9 on other certificates, and the k2m4_n77_L9 README says the Lean proof uses Daniel's certificate, not wand125's n77 cover. T-064 / think-0ayk: the same machinery for Valid7 (k^2 - 3). think-hwpr: the full replay of wand125's ValidTilt9 checker run (records-tilt9-v1), a different route to the same premise. think-kqi1: a scope that can say "every k >= 8".
- No count moves: the verified lower bounds at k = 10 to 18 stay unchanged until something is replayed here.

## Price (cap: 40 CPU-h per item, think-lh7d; tonight: no very large compute)

- Stage 2 retention: the lean/ directory at 319a779 (2.9 MB) in a packet with an acquisition record; the three release assets by digest, not committed (OR-18; v9-certs.tar.zst is 109 MB). Under an hour of agent work, seconds of CPU.
- Statement binding, rest: compare the 40 machinery files with evand at 060c1a1 and 44a105e, read RowMinN.lean and LemmaEKM.diff, read Bridge/Tilt against ValidSplit9.lean's ValidTilt9. Minutes of CPU, about an hour of agent work.
- Full kernel replay: HELD. The source reports about 7,390 CPU-h of kernel checks (leaf modules 2,694, row groups 4,665, roots 31) plus 177 CPU-h of certificates (skippable with v9-certs.tar.zst), peaks of 22 to 32 GB per module, and Main.lean's assembly at 230 GB resident over 1.27 M oleans (340 GB of disk). About 185 times the 40 CPU-h cap, and the host has 15 GB of memory and 30 GB of disk.
- Sampled replay (optional, under the cap): rebuild a handful of roots from v9-certs.tar.zst with driver/run9.py and compare the generated sources with SOURCES.sha256, choosing light roots from tasks.jsonl (v9-logs.tar.zst). About 27 CPU-min a root on average, but a Lean v4.33.1 toolchain with Mathlib (about 5 GB) and evand's library at 060c1a1 are needed first, and memory rules out the heavy roots. A component check: it substantiates no whole value (epistemics.md), so it moves no rung.
- Review: an AI statement-fidelity review (agent hours, no CPU); V5 needs a human expert's formalization review and a replay here, neither available.
- Rung: a reported formalization enters V0/C0, as T-154 did; nothing here moves T-081.

## Proposed disposition

An import bead (this one): stage 2 (packet at 319a779 with the asset digests), stage 3 (a formalization entry naming T-081, reported, credited "Hosono after Daniel", AI assistance as the commits state: Co-Authored-By: Claude Opus 5.5), the statement-binding checks above in the packet's receipts, and a validation bead for the held full replay (about 7,400 CPU-h and 230 GB; HELD above the cap). Draft significance S4: the first proof-assistant proof of a bound family that settles nine open cases of this record (k = 10 to 18) once adopted, on the anchor "a substantial new result"; S3 if the registering lane reads it as verification of an existing S4 result. At S4 the project opens an intake issue for it (the owner's rule of 2026-10-14, stage 1 step 5): that is the coordinator's call, not this lane's. Until a packet pins 2c75edc, the intake-watch.yaml read through 319a779 names this bead.

## Draft acknowledgement (not posted; no T-NNN, no rung; for the tracking issue if one is opened)

@wand125, thank you for publishing the kernel proof of ValidTilt9 with its environment, scripts and receipts. We have read wand125/square-packing at 319a779efcc78db2f92bffc87844446f8723b01d, where 2c75edc and e99f5e3 add problems/square-lower-bounds/certificates/k2m4_n77_L9/lean/, together with the digests of the validtilt9-lean-v1 assets. Every file of the import closure that this repository already holds from Evan Daniel's 3 October release, including Basic.lean, S32.lean, ValidSplit9.lean, Bentz4.lean and Bentz4Data.lean, is byte-identical to the copy your library.sha256 lists, so validTilt9, valid9 and bentz4 are stated with the definitions our own build of the reduction used. Next, the lean/ directory is retained here at that commit and the result is registered as reported, beside Daniel's theorem. The kernel run itself, about 7,400 CPU-hours and 230 GB for the assembly, is far beyond what we can replay here, so the entry will say it is reported, not replayed.

---
_Generated by [Claude Code](https://claude.ai/code)_

## Notes

2026-10-16 ~05:45Z user-eb-intake-residue: the coordinator opened the tracking issue under the owner's S4+ rule: https://github.com/jlevy/squares/issues/643 (jlevy, 2026-10-16T05:29:57Z, labelled intake, no comments; its description is the acknowledgement, so the draft acknowledgement above is not to be posted). Title moved from (no issue) to (#643). #643's entry (kind result-report, one queued result validtilt9-lean, bead and answer bead think-jh0n) goes into packing/campaign/result-requests.yaml on branch claude/intake-2026-10-16-residue. Stages 2-3 stay with this bead and are out of lane A's PR unless time allows.

2026-10-16 06:15Z user-eb-intake-residue: statement binding, the rest (read-only, from blobless clones in the lane's scratch; no build).
- The import closure against evand/square-packing: of library.sha256's 59 entries, 54 are byte-identical to evand at 060c1a1052029f81f30c8a97134ee03666b1bb77 and again at 44a105ef95ac1925d83aab087d7ddab7f672b747 (under lean/). The rest is as the source says: Sqpack/LemmaEKM.lean differs, and Sqpack/RowMinN.lean and Sqpack/V9/{Bridge,Data,Tilt}.lean are absent upstream, being new. So the 51 machinery and statement files plus lakefile.toml, lake-manifest.json and lean-toolchain are upstream's, at both revisions.
- LemmaEKM.lean against 060c1a1's: exactly the four hunks of library/LemmaEKM.diff. The import RowMinK becomes RowMinN, a doc sentence is added, rmChk replaces rmLoop in the computable check, and the proof step becomes rmLoop_sound … (rmChk_sound hK hloop). No statement changes.
- RowMinN.lean (199 lines): defs minN, digN, rmLoopN, rmChk; lemmas through rmChk_sound. No sorry, axiom, native_decide, implemented_by, extern, unsafe or attributes.
Together with the 19-file check above: every definition the three theorems' statements use is the record's own 3 October copy, and the only non-upstream library code is a proved reflection lemma. What stays open for stage 2-4: retaining lean/ at 319a779 with the asset digests, reading Bridge.lean and Tilt.lean against ValidSplit9.lean's ValidTilt9 (a reviewer's job), and the held replay.
Scratch: laneA/src/evand-sp, laneA/src/wand125-sp, laneA/library.sha256.

2026-10-16 ~07:50Z coordinator: per PR #647 review A2, the next #643 reply should report the comparison of the 40 machinery files as done (06:15Z note) and count the 19 retained closure files as 16 Lean modules + 3 build files; #643's body was corrected at 06:44Z.

2026-10-18 W1 intake (think-xmxb): PR667 A9 notification: wand125/square-packing 746b0c06cdb1ef7988381153cebfba1b5e720b04 publishes Lean rectangle AB-5 theorem, A,B>=8; square specialization is T-081 lower half by second Lean route using same ValidTilt9 premise. Intake-watch holds read for this bead; retain scope and classify evidence/formalization before claiming imported. No build here.
