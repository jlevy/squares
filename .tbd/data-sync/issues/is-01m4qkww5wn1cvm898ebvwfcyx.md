---
type: is
id: is-01m4qkww5wn1cvm898ebvwfcyx
title: "Import E. Summins: simple-square stratification of s(n), n = 11 scoreboard and Lean layer, a strategy registration (#522)"
kind: task
status: in_progress
priority: 1
version: 7
delegate: bold-ritchie-l7
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-12T08:33:03.676Z
updated_at: 2026-10-31T11:44:39.726Z
started_at: 2026-10-12T08:52:51.243Z
---
https://github.com/jlevy/squares/issues/522 (2026-10-12T04:12:28Z). Esummins/packing at 651a9a54688341880e9c0dc9fcfc19f2c04cd3cb: writeup/outreach/01-stratification-program.md, 07-timeline.md; A56 scoreboard.json; A57 verify_case.py (sha256 521cb01fe656...); lean/AUDIT.md, Main.lean, Statements/. Not a bound: a proof strategy for proof-strategies.yaml, an n = 11 census theorem (Lean, standard axioms), 52/52 k5/k6 window kills under a frozen verifier, and a Lean layer with three named open axioms.

## Notes

## Stage 1 triage (2026-10-12, lane intake-esummins, worktree branch intake-esummins from l4 dead83f0e)

- Pin: Esummins/packing 651a9a54688341880e9c0dc9fcfc19f2c04cd3cb (master, committed 2026-10-12T04:11:54Z); head at the read eb3ae15 adds only writeup/outreach/POSTED.md. Issue filed 2026-10-12T04:12:28Z. Licence: code MIT, documents and data CC BY 4.0. AI assistance: produced by Claude under the PI's direction (stated on the issue). Credit name: E. Summins (PI), n = 11 lab.
- Claims mapped (stage 1 table), one issue holding five:
  1. Method: the simple-square stratification as a proof strategy. Where: packing/frontier/proof-strategies.yaml (kind proof; the lab proposes family modern_machinery or a new structural_case_split; status by the catalogue's vocabulary). A catalogue edit is a record edit for the records lane and an owner decision: the strategy has proved no bound; at n = 11 its window layer is closed and its low-k strata and k = 0 are open. No register entry.
  2. Theorem: the n = 11 census, 1110 tuples / 163 D4 classes exhaustive at every side in (3, 4); Lean `stratification`, `skeleton_in_census`, `exists_stratum_stmt` (Statements/Stratification.lean), AUDIT.md: theorem on std axioms. Where: a structural theorem at a settled count (T-060, T-112), not a bound and not an exclusion the record acts on; a method record in the packet, no register entry. Not built here.
  3. Certificate-backed: 52 of 52 k5/k6 scoreboard rows FULL on [191/50, 969271/250000]. Re-read here from the retained scoreboard.json: 52 rows, every `result` FULL on that window, 4 by the single-corner transfer theorem M1 without computation, 48 by parametric certificates (A56, A61 re-solves, A114 sub-windows, A146 slabs). Where: class exclusions at a settled count; a ledger note at most (n-011.md could carry a paragraph if the owner wants the programme noted). The certificates themselves live in attempts/A56, A114, A146 and are pinned by the commit, not retained; the frozen verifier verify_case.py is retained.
  4. The Lean layer: see below. A method record; no register entry (conditional on three open axioms, one of which, stratum_kill, is the programme's own open residue).
  5. Negatives and corrections, as ledger notes: Lemma K1's direction corrected (kills climb up containment; "all extensions dead implies the class dead" is unsound); k5_11 and k5_16 open on slab G1 (A270 at its 150 CPU-h cap); the protected tier THEORY-LIMITED (corners4, k4_05); A55's k4 kills hold at s0 only (not window rows; PARAM-FAIL in A241).
  By-products the issue does not claim, below the standing bounds (table: none, stay in the packet): s(11) >= 3.82 end to end in Lean (`lower_bound_382`, std + native_decide(check_3_82) on certs/measure_certificate_3.82.json; T-060 holds the exact value) and s(12) >= 3.90 certified by A33 (n-012.md holds 7943/2000 = 3.9715 verified).
- Dependencies on this record: T-037 (their W' = [31/8, s0] and the A242 dry run: 99 of 1,795 frontier nodes dead at once), T-060 and T-112 (the value and uniqueness they do not claim; their Main.lean states the same three statements conditionally), the n11 threshold-bound review (Part II) for the certificate's meaning.
- Digest caveat for the lab: the frozen verifier's quoted sha256 521cb01fe656... is the digest of the file with CRLF line endings; the committed blob is LF and digests 1574ddbdcd57e6428ef23b393a8d42b51c7b9e7454f287133fe3fc6ee2c7fb68. The same holds for certs/verify_measure.py (quoted 2a735939d67f = CRLF; LF 87fa3d31cb91c7ef...). A Windows working-copy join key; the "byte-faithful" Lean checker claim (A70, A117: 30/30 byte-identical) should say which bytes it read.
- Lean files (the retained lean/ subset: AUDIT.md, lakefile.toml, lake-manifest.json, lean-toolchain, Main.lean, TopLevel.lean, Statements/ with Open/, 71 files; the core library and the Corpus library are pinned by the commit):
  - Toolchain pin: leanprover/lean4:v4.34.0-rc1 (lean-toolchain); Mathlib v4.34.0-rc1 at de5ce8a9a66a4aa68a9bdbb35b63a06d34d9ca11 (lake-manifest.json, 8 packages, fixedToolchain false). A release candidate, not a release.
  - sorry: none in Main.lean, TopLevel.lean or Statements/ (grep; AUDIT.md's sorry column is 0 on every row). Axioms: the three main theorems rest on std (propext, Classical.choice, Quot.sound) + three project axioms (stratum_kill, trump_residual, a22_exact_structure) + six native_decide evaluations (Lean.ofReduceBool: cidl_gate_delta, cidl_gate_e, cidl_identity, checkA22_a22, checkA36_universal, check_3_82). Statements/Open/ declares 93 `axiom`s in all (the open-lemma layer: one_flush, locked_crowd_free, theorem_FC, one_tilted, lemma_PUSH, lemma_CT, threshold_bound_31_8, the k0 chain's meeters_split, rows_classified, band_count, ...); the main theorems use none of those but the three. Theorems on std alone that the issues cite: stratification, case_verifier_kill, slot_crowd_stmt, fc_transfer_stmt, snap_dead, swap_packing, cells_swap, no_retreat_of_psiMin, fourcrowd_dead_of_step_kill, gate, role_split, theorem_G, windows_clause_kill. exists_optimal_singly_met and optimal_psiMin_not_stuck rest on the axiom locked_crowd_free; wedged_seal on lemma_PUSH; flush_eleven_four on lemma_FLUSH.
  - Build price here: toolchain download plus the Mathlib cache for v4.34.0-rc1 (about 5 minutes if the cache serves that rev; the 2026-10-11 precedent took 54 s + 1 m 44 s for Ahmed's pin at a different rev), then `lake build PackingCertMathlib` (the default target, the Corpus library excluded): the lab's status sheet prices its 3.82 end-to-end build at about 40 minutes, the native_decide replays run compiled checkers on certificate files, and the lab recorded 571 s and 6,707 s for two other native_decide modules; on this loaded four-core machine a cold build is 1 to 3 hours wall, so it was not built. A statement-closure build of Statements/ alone (as think-66e5 did for 11SquaresFormalized) would be about 20 minutes and proves only that the statements type-check against the pinned core.
- Review route and price: (a) the strategy-catalogue entry, records lane, 1 hour, owner decision first; (b) a mathematics-tier review of the bridge lemmas the scoreboard rests on: instratum_bridge.md E.1 (Lemma K1), closed_disjoint_bridge.md Lemma B.0 (dilation), forced_corners.md section 2 (pads), soundness.md M1 (single-corner transfer), about one day; (c) the verifier soundness, verify_case.py (retained, 7 KB) with CaseVerifier.lean and the frozen spec, about one day; (d) a replay of the 48 certificate rows and the A146 slab sweep: the certificates are pinned by the commit and would need a further sparse fetch of attempts/A56, A114 and A146; the lab prices verify_case.py at seconds per certificate, so hours of CPU at most, priced after listing them. None of (b) to (d) is needed unless the owner takes the programme into the record.
- Retained: packet packing/resources/web/esummins-packing-2026-10-12/ (whole series): writeup/outreach, the write-up and status sheet, docs/proofs, residue_ledger.md, shadows/STATUS.md, the Lean subset above, certs (cited files; a82, uladder and byte code pinned by digest), REGISTRY.md, A53 census files, A56 scoreboard.json, the frozen verifiers v1/v3/v4/v5 and verify_swap232.py.

## Acknowledgement draft (stage 1; not posted)

@Esummins, thank you. Received: the stratification programme, its n = 11 scoreboard and the Lean layer at [Esummins/packing@651a9a5](https://github.com/Esummins/packing/tree/651a9a54688341880e9c0dc9fcfc19f2c04cd3cb/writeup/outreach), pinned at that commit; the paths your index's section 4 names are retained here, with the bulk data pinned by digest or by the commit.

What will be checked: the scoreboard was re-read here (52 rows, each FULL on [191/50, 969271/250000]); the Lean layer's toolchain pin, axiom roster and absence of `sorry` were read from the sources and `lean/AUDIT.md`, and its build is priced rather than run. Whether the strategy enters the catalogue, and in which vocabulary, is the owner's decision; nothing here claims a bound, and the n = 11 value and uniqueness stand on T-060 and T-112. One note for you: the verifier digests your notes quote (521cb01fe656 for `verify_case.py`, 2a735939d67f for `verify_measure.py`) are the digests of CRLF working copies; the committed files are LF and digest differently.

---
_Generated by [Claude Code](https://claude.ai/code)_

2026-10-12 09:00Z: packet committed on worktree branch intake-esummins at 7d4cc96c1 (not pushed); acquire_source --check PACKET_MATCHES_ITS_CONTRACT; proposed result-requests.yaml and intake-watch.yaml entries in the lane scratch file proposed-entries.yaml (reported to the coordinator), nothing applied to the shared records.


2026-10-31 bold-ritchie-l7 (intake pass think-3guf, lane L7): posted the #522 follow-up from main 90b79dbe1, acknowledging the author's comment of 22 October (LF digests 1574ddbd... and 87fa3d31..., outreach notes at 429bcda, pin 651a9a5 unchanged): https://github.com/jlevy/squares/issues/522#issuecomment-6542831736. Recorded on branch claude/bold-ritchie-xo28us-replies2. check_requests --report: no reply due; not closeable (the strategy ask waits on the owner, blocked:owner-decision).
