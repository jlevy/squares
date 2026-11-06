# search/

The research log.  Each investigation left one `UPPERCASE.md` log next to the scripts it wrote; the log names its
code, its runs (in the gitignored `runs/`, so every number is quoted in the log) and its verdict.  The logs are dated
and not curated: later logs correct earlier ones, and the corrections are recorded in place.  Nothing here is moved or
renamed, because certificate READMEs, `docs/*.html`, `RESEARCH.md` and `Completed.md` cite these paths.

For results, start at the top-level [`README.md`](../README.md) (one row per certificate bundle).  For chronology:
[`TODO.md`](../TODO.md) (open) and [`Completed.md`](../Completed.md) (done, dated, with the log of each step).
[`RESEARCH.md`](../RESEARCH.md) is the long account of the s(11)/s(12)/s(13) method.

Labels used throughout the logs: **[proved]** / **certified** (exact arithmetic or Lean), **[measured]** (float LP or
scan, reported as-is), **[heuristic]**.  A float LP value is not a bound unless the log says which way.

## Start here

| Result (bundle) | Logs that underlie it |
|---|---|
| s(12) ≥ 15680/3951, s(11) ≥ 3040/797 (point certificates in [`certificates/`](../certificates/)) | [TIGHTEN.md](TIGHTEN.md) (how 3.9686 was reached), [REPRODUCIBILITY.md](REPRODUCIBILITY.md) (`lp_search.py`), [CEILING.md](CEILING.md) and [DUAL_EXACT.md](DUAL_EXACT.md) (no pure cover works at side ≥ 3.99), [N11.md](N11.md) (s(11)), [uniform/UNIFORM.md](uniform/UNIFORM.md) (the `s12_uniform_*` files) |
| demo and branch certificates (`s12_boxclique_demo_*`, `s12_anchorclique_demo_*`, `certificates/branch/`) | [BOXCLIQUE.md](BOXCLIQUE.md), [ANCHOR.md](ANCHOR.md), [BRANCH.md](BRANCH.md) |
| s(13) = 4, case-free ([`certificates/rung2/`](../certificates/rung2/README.md)) | [ZEROMARGIN.md](ZEROMARGIN.md) (the checker), [RUNG2.md](RUNG2.md) (the cover and Theorem 1), [RUNG2_XCHECK.md](RUNG2_XCHECK.md) (`verify2/zmcheck`), [COVER4.md](COVER4.md) (`COVER^closed(4) ≥ 12.2688`) |
| s(21) = 5 ([`certificates/s21/`](../certificates/s21/README.md)) | [LINE_COVER.md](LINE_COVER.md) (the mixed cover), [ZM_MIXED.md](ZM_MIXED.md) and [ZMX2.md](ZMX2.md) (the two checkers), [ZM_MIXED_AUDIT.md](ZM_MIXED_AUDIT.md), [ZMX2_AUDIT.md](ZMX2_AUDIT.md); background [S21_COVER.md](S21_COVER.md), [S21_KILL.md](S21_KILL.md) |
| s(32) = 6 ([`certificates/s32/`](../certificates/s32/README.md)) | [S32_COVER.md](S32_COVER.md), [S32_EXACT.md](S32_EXACT.md), [S32_SHIFT.md](S32_SHIFT.md); third check in [ZMX2.md](ZMX2.md) §9, §12 |
| s(45) = 7 ([`certificates/s45/`](../certificates/s45/README.md)) | [S45_COVER.md](S45_COVER.md) §10; checkers as for s(21) |
| s(60) = s(61) = 8 ([`certificates/s60/`](../certificates/s60/README.md)) | [S60_COVER.md](S60_COVER.md), [S61_WAND125_REPLAY.md](S61_WAND125_REPLAY.md); checkers as for s(21) |
| s(k² − 3) = k ([`certificates/k2m3/`](../certificates/k2m3/README.md)) | [QUADRANT.md](QUADRANT.md) (float family LP), [QUADRANT_EXACT.md](QUADRANT_EXACT.md) (exact family, `qx2_zm.py`, Lemma Z), [ZMX2_AREA.md](ZMX2_AREA.md) (`zmx2` with area density, a second implementation); lemmas in [ZM_MIXED.md](ZM_MIXED.md) §2 |
| s(k² − 4) = k ([`certificates/k2m4/`](../certificates/k2m4/README.md)) | [K2M4_MARGIN.md](K2M4_MARGIN.md), [QUADRANT_EXACT.md](QUADRANT_EXACT.md) §3–4; Friedman's conjecture in [FRIEDMAN.md](FRIEDMAN.md) §0 |
| unavoidable sets ([`certificates/unavoid13/`](../certificates/unavoid13/README.md)) | no log in `search/`: [`notes/unavoid13.md`](../notes/unavoid13.md), [`notes/unavoid13-no.md`](../notes/unavoid13-no.md); Friedman's 14 points re-proved in [ZEROMARGIN.md](ZEROMARGIN.md) |
| packing search ([`packer/`](packer/)) | [packer/README.md](packer/README.md) (map and status), [packer/PACKER.md](packer/PACKER.md) (lab log) |
| exact forms of record packings ([`exact/`](exact/)) | [exact/README.md](exact/README.md), [exact/EXACT_FORMS.md](exact/EXACT_FORMS.md), [exact/batch/README.md](exact/batch/README.md) |

Open conjectures and proof pieces, collected: [WISHLIST.md](WISHLIST.md).

## Index of logs, by theme

One line each, from the log's own opening or verdict.  *Superseded* and *negative* are the logs' own words or
corrections.

### Pure point covers: s(12), s(11), and their ceilings

| Log | Question → outcome |
|---|---|
| [TIGHTEN.md](TIGHTEN.md) | Re-optimised weights, sparser sets, larger containers → bound moves 3.931795 → 15680/3951 = 3.968616; certificate at the old bound shrinks 788 → 224 points. |
| [REPRODUCIBILITY.md](REPRODUCIBILITY.md) | Sources of nondeterminism in `lp_search.py`, removed; two byte-identical runs demonstrated. |
| [TIGHTSET.md](TIGHTSET.md) | Near-tight pose set of the shipped 3.9686 certificate beyond its critical container (table). |
| [CEILING.md](CEILING.md) | Bracketing `ν_f(s)` → `s* ∈ [3.968616, 3.99)`: no pure cover gives s(12) ≥ 3.99. |
| [DUAL.md](DUAL.md) | Packing column generation → `L(3.99) = 12.0082 > 12`, float with margins (made exact in DUAL_EXACT). |
| [DUAL_EXACT.md](DUAL_EXACT.md) | The same bound in rational arithmetic: `L(399/100) ≥ 12`, certificate `dual_exact_3.99_support.txt`. |
| [CLOSED4.md](CLOSED4.md) | Heuristic cover LP at `[0,4]²`, closed semantics → 12.3–12.4; best explicit set costs 12.51.  Not a bound. |
| [COVER4.md](COVER4.md) | Exact floor `COVER^closed(4) ≥ 12.2688`: covers alone can never prove s(12) = 4. |
| [N11.md](N11.md) | Where the cover LP crosses 11 → s(11) ≥ 3040/797 (pure LP).  *Superseded as a bound: s(11) is now proved.* |
| [N11_ANATOMY.md](N11_ANATOMY.md) | What the mass-11 fractional packing is (four poses: the 3×3 grid, middle square counted three times); exact `ν_f(3.83375) ≥ 11`. |
| [N11_LADDER.md](N11_LADDER.md) | Every rung of the s(12) machinery run once at n = 11, for a like-for-like comparison. |
| [uniform/UNIFORM.md](uniform/UNIFORM.md) | Uniform (unweighted) certificates `(k, m, s)` for s(12), k = 1…8; the nine shipped `s12_uniform_*` files. |

### s(12) = 4 beyond pure covers: branching, cliques, anchors, leaves

| Log | Question → outcome |
|---|---|
| [BRANCH.md](BRANCH.md) | Corner-occupancy branch certificates → built and verified; does not close 3.99.  *Its k = 4 statement withdrawn (CLIQUE.md).* |
| [CLIQUE.md](CLIQUE.md) | The Helly gap: extremal packings put mass 1.3–1.5 on point-free cliques; clique cuts move the LP 0.1–0.3. |
| [CLIQUE_CEILING.md](CLIQUE_CEILING.md) | Clique-strengthened packing value vs `t` → no ceiling found; clique method not excluded at any `t ≤ 4`. |
| [BOXCLIQUE.md](BOXCLIQUE.md) | Box cliques as a verifiable certificate column (verifier, `xcheck.py`, Lean); on the demo the LP used none. |
| [CLIQUE_CONTINUUM.md](CLIQUE_CONTINUUM.md) | Is the non-Helly mass certifiable? → GO: the clique lever is real in the continuum (~14× the pure excess); not a proof. |
| [ANCHOR.md](ANCHOR.md) | Anchor cliques as a certificate object (verifier, Lean) → done and checked; worth ~10⁻⁴ on the cover side so far. |
| [RECONCILE.md](RECONCILE.md) | Packing-side vs cover-side anchor gains → both earlier numbers wrong; fixed separator gives +0.095 at 3.99. |
| [WITNESS.md](WITNESS.md) | LP rows must carry the verifier's clique credit → defect fixed; whether leaves close is not settled. |
| [T4SCREEN.md](T4SCREEN.md) | Corner branch + level-2 slots + anchor cliques at `t = 4` → undecided; pose sets starved. |
| [T4LEAF.md](T4LEAF.md) | The hardest level-2 leaf to convergence → still rising; nothing reached 12. |
| [LEAF_CEILING.md](LEAF_CEILING.md) | Exact no-go certifier for a level-2 leaf → built and validated; no no-go found. |
| [DEPTH.md](DEPTH.md) | Quadrant branching of the hardest leaf → drop per level is exactly 0 (a symmetry theorem). |
| [LINECUTS.md](LINECUTS.md) | The chord lemma on every line as packing cuts → valid, worth exactly 0 on all three instances. |
| [CLIQUELEVER.md](CLIQUELEVER.md) | QSTAB relaxation of the hardest `t = 4` leaf → cliques are the lever. |
| [CLMASTER.md](CLMASTER.md) | Restricted master + lattice pricing for `cliquelever.py` → 4–10× per iteration; stalled runs converge. |
| [RANKDIAG.md](RANKDIAG.md) | What non-clique structure carries the residual excess → a pentagon of anchors, not an odd hole of poses. |
| [LOCALITY.md](LOCALITY.md) | How much can any local family prove → "global counting unavoidable" ruled out; the obstruction is the pentagon, factor 5/4. |
| [HONEST.md](HONEST.md) | Honest cost of the best pure `t = 4` dual as a cover → 18.1 / 20.2, not 12.1–12.6: nowhere near a cover. |
| [ALLMEET.md](ALLMEET.md) | Can a sound positive-volume rule credit the fan cliques → yes, every row; it does not recover the fan mass. |
| [BENTZ.md](BENTZ.md) | Bentz's case analysis as incidence-pattern branching at `t = 4` → pinned leaf survives fractionally; integrally off by one square. |
| [RANK8.md](RANK8.md) | Margin of the rank-8 statement → exactly 0, attained on a large plateau, not only the tiling. |
| [CENSUS.md](CENSUS.md) | Integral margin of every pattern leaf → no class positive; ≥ 2,779 zero-margin leaves. |

### s(6) skeleton, chains and far field (case-free architecture; s(T² − T) = T)

| Log | Question → outcome |
|---|---|
| [S6_SKELETON.md](S6_SKELETON.md) | Separation/transversal B&B for s(6) = 3 → not closed, cannot close by refinement.  *Three numbers corrected in S6_LOCAL.* |
| [S6_LOCAL.md](S6_LOCAL.md) | The deficit off the zero set, re-measured and exact on single leaves; corrects S6_SKELETON. |
| [SOS_PROBE.md](SOS_PROBE.md) | Can exact Positivstellensatz certificates reach zero margin at s(6) = 3 → no degree reached `eps = 0` with ≥ 2 free angles. |
| [ARCH_TLEDGER.md](ARCH_TLEDGER.md) | Where does s(T² − T) = T break → `c_T = (T−2)/(2(T−1))` for T ≥ 4; never changes sign. |
| [ARCH_FARFIELD.md](ARCH_FARFIELD.md) | Does a near-axis mass cap close the far field (Lemma A3) → no: fails at the small `eps` needed (negative). |
| [FARFIELD_STRONG.md](FARFIELD_STRONG.md) | The cap in the strongest certifiable `t = 4` family → refuted at 1° and 2°; no region proved (negative). |
| [BANDCUT_SCAN.md](BANDCUT_SCAN.md) | Tilted-band family from T = 12 down → exact re-verification of s(132) < 12, s(110) < 11; budget runs out below T = 12. |
| [BANDCUT_K.md](BANDCUT_K.md) | Margin with `k` near-axis squares, with/without a chain → no chain-free configuration of margin ≥ 0 at T = 3, 4. |
| [T11_CHAINS.md](T11_CHAINS.md) | Tight wall-to-wall chains of the T = 11 packing → all run through the band. |
| [T4_CYCLES.md](T4_CYCLES.md) | Which certificates the T = 4 duals use → chain-or-cycle dichotomy false; H1 holds 727/727. |
| [BREAK_H1.md](BREAK_H1.md) | H1 under adversarial search → survives 153/153; ladder depth 2, 3, 2 at T = 3, 4, 5. |

### Zero-margin checkers and audits

| Log | Question → outcome |
|---|---|
| [ZEROMARGIN.md](ZEROMARGIN.md) | Exact checker at the container itself (`zeromargin.py`) → s(15) = 4 re-proved from Friedman's 14 points. |
| [RUNG2.md](RUNG2.md) | s(13) = 4 by a weighted closed cover of total 12.956 < 13; Theorem 1: the proof must be disjunctive. |
| [RUNG2_XCHECK.md](RUNG2_XCHECK.md) | Independent re-implementation (`verify2/zmcheck`, Rust, no symmetry) → rung-2 certificate verified. |
| [ZM_MIXED.md](ZM_MIXED.md) | Exact checker for mixed covers (points + segments + polygons), `zm_mixed.py`; lemmas §2. |
| [ZM_MIXED_AUDIT.md](ZM_MIXED_AUDIT.md) | Adversarial audit of `zm_mixed.py` and the s(21) run → no soundness defect. |
| [ZMX2.md](ZMX2.md) | `zmx2`, an independent Rust mixed-cover checker → s(21) cover verified, D4 and full. |
| [ZMX2_AUDIT.md](ZMX2_AUDIT.md) | Adversarial audit of `zmx2` → no defect touching the s(21) certificate. |
| [ZMX2_AREA.md](ZMX2_AREA.md) | `zmx2` with area densities, for the k² − 3 box cover → `Valid7` certified with `--first-order` (2026-10-01; Lemmas U/V newest, least reviewed). |
| [M4_MARGIN.md](M4_MARGIN.md) | Checker margin vs validity at m = 4 → checker factor negligible (≤ 1.0025); validity is the whole problem. |

### Mixed covers and the k² − 4 rungs: s(21), s(32), s(45), s(60), s(61)

| Log | Question → outcome |
|---|---|
| [FAMILY.md](FAMILY.md) | The m² − 4 family, first attempt (2026-08-30) → rung 2 not achieved then; m = 5 bracketed, gap not closed. |
| [S21_COVER.md](S21_COVER.md) | Cover side of s(21) = 5 with points → converged LP ≈ 20.73, room 1.3 %. |
| [S21_KILL.md](S21_KILL.md) | Kill test → `ν_f^closed(5) ≥ 20.6478` (exact); route alive, margin small. |
| [S21_LB.md](S21_LB.md) | Positive-margin point certificate → s(21) ≥ 5000/1001.  *Superseded by s(21) = 5.* |
| [S21_OVERHEAD.md](S21_OVERHEAD.md) | Where the m = 4 overhead sits.  *Corrected by M4_MARGIN; numbers citing 1.0277 superseded.* |
| [LINE_COVER.md](LINE_COVER.md) | Points + uniform grid-line densities → GO: m = 5 mixed cover of total 20.832 (became the s(21) certificate). |
| [S32_COVER.md](S32_COVER.md) | Cover side of s(32) = 6 → LP ≈ 31.22; candidate 31.7135, go for the exact checker. |
| [S32_EXACT.md](S32_EXACT.md) | Exact check of the s(32) candidate → certified; shipped as `certificates/s32/` (§§0–9 are pilots). |
| [S32_SHIFT.md](S32_SHIFT.md) | Tile-germ failures: point shifting vs the checker → second cover `s32_shift_v1` (31.698). |
| [S45_COVER.md](S45_COVER.md) | Cover side of s(45) = 7 → point covers failed (§§0–9); line-density cover 44.7735 verified (§10). |
| [S60_COVER.md](S60_COVER.md) | The m = 8 line-density cover → total 59.859 < 60, verified by both checkers. |
| [S61_WAND125_REPLAY.md](S61_WAND125_REPLAY.md) | Replay of wand125's point cover on `[0,8]²` → certified by our checkers: s(61) = 8. |

### All-k families: k² − 3, k² − 4, Friedman's conjecture, seams and corners

| Log | Question → outcome |
|---|---|
| [QUADRANT.md](QUADRANT.md) | Fixed-profile family LP for s(k² − 4), s(k² − 3) (float) → seam bound correct as stated; family viable. |
| [QUADRANT_EXACT.md](QUADRANT_EXACT.md) | Exact (R = 2, w = 2) family → s(k² − 3) = k for all k ≥ 6, certificate complete. |
| [K2M4_MARGIN.md](K2M4_MARGIN.md) | k² − 4 go/no-go and the tilt-margin ceiling → `Valid9` VERIFIED-D4 (the k2m4 certificate). |
| [QX2_PL.md](QX2_PL.md) | Hat (piecewise-linear) line densities vs uniform pieces → hats alone do not help (measured). |
| [CORNER_DEFICIT.md](CORNER_DEFICIT.md) | Can one corner module save `D > 1` per corner → the corner deficit is exactly 0 (negative). |
| [SEAM_1D.md](SEAM_1D.md) | Exact certificates for the 1D seam price (FRIEDMAN §8 (a)); data in `seam_data/`. |
| [SEAM_W1.md](SEAM_W1.md) | Seam capacity at w = 1 → `M(1) = 3/4`; what changes at w = 2. |
| [FRIEDMAN.md](FRIEDMAN.md) | Friedman's Conjecture 1 (s(n² − c) = n ⇒ s((n+1)² − c) = n+1): proof shapes, lemmas, experiments. |
| [S2_INSERTABLE.md](S2_INSERTABLE.md) | Insertable box covers at the threshold → no-go at c = 3, k = 4 and c = 4, k = 5 (measured). |

### Ceilings, s(17)–s(20), literature checks

| Log | Question → outcome |
|---|---|
| [CEILINGS_17_20.md](CEILINGS_17_20.md) | What pure closed covers can prove for n = 17–20 → several targets killed by exact ceilings; (20, 4.8856) open. |
| [S20_LB.md](S20_LB.md) | s(20) > 3 + 4√2/3 by a cover at side 4.886.  *Superseded as a bound by wand125's 1959/400; kept as confirmation.* |
| [GREEN_FIG34.md](GREEN_FIG34.md) | Green's s(17), s(18) ≥ (40√2+19)/17 → Figure 34's set is not unavoidable at its side; corrected numbers. Code in `green_fig34/`. |

### Lean and write-up

| Log | Question → outcome |
|---|---|
| [GOLF_PILOT.md](GOLF_PILOT.md) | Re-shape mixed covers before generating the Lean tree? → only by scaling the cover to ≈ 20.99; code in `golf/`. |
| [S13_WRITEUP.md](S13_WRITEUP.md) | Documentation, `verify.sh`, CI and site for s(13) = 4; no new mathematics. |

The Lean ladder itself is logged in [`lean/LADDER.md`](../lean/LADDER.md), not here.

### Speed and infrastructure

| Log | Question → outcome |
|---|---|
| [LPSPEED.md](LPSPEED.md) | LP backends for the cover cutting-plane loop → keep HiGHS IPM; shrink the master (`BRANCH_SOLVER=restricted`). |
| [LOOPSPEED.md](LOOPSPEED.md) | Float separation oracle (`floatsep.py`) replaces the exact verifier in the loop; soundness untouched. |
| [VERIFYSPEED.md](VERIFYSPEED.md) | Verifier speed on anchor-clique certificates; bit-identical output, measured speed-ups. |

### Subdirectories

| Directory | What |
|---|---|
| [packer/](packer/README.md) | Packing search engine (Rust + Python), from 2026-10-04: goals + stages ([DESIGN.md](packer/DESIGN.md)), findings in [CLAIMS.md](packer/CLAIMS.md), record submissions [SUBMITTING.md](packer/SUBMITTING.md).  Lab log to 10-24: [archive/PACKER-2026-10.md](packer/archive/PACKER-2026-10.md); literature notes moved to `../literature/packer-lit-*.md`. |
| [exact/](exact/README.md) | Exact KKT points and rational certificates `s(n) ≤ S'` for record packings; [EXACT_FORMS.md](exact/EXACT_FORMS.md) (algebraic `S*`, Lean `Packs`); [batch/](exact/batch/README.md) (all n ≤ 324 of jlevy's register). |
| [uniform/](uniform/UNIFORM.md) | Uniform s(12) certificates (see above). |
| [goebel_alt/](goebel_alt/README.md) | Alternatives to the rigid s(149) Göbel-type packing (exploratory ILP). |
| `green_fig34/` | Scripts and certificates for [GREEN_FIG34.md](GREEN_FIG34.md). |
| `golf/` | Data and scripts for [GOLF_PILOT.md](GOLF_PILOT.md). |
| `qx2_data/` | Exact family, box covers and run records for [QUADRANT_EXACT.md](QUADRANT_EXACT.md) and [K2M4_MARGIN.md](K2M4_MARGIN.md) (copied into the k2m3/k2m4 bundles). |
| `seam_data/` | Certificates for [SEAM_1D.md](SEAM_1D.md). |
| `s61_wand125/` | Cover, `MANIFEST.txt` and run records for [S61_WAND125_REPLAY.md](S61_WAND125_REPLAY.md). |
| `zmx2_audit/` | Auditor's tools for [ZMX2_AUDIT.md](ZMX2_AUDIT.md). |
| `zmx2_area/`, `zmx2_sym_logs/` | Run outputs for [ZMX2_AREA.md](ZMX2_AREA.md) and the `--sym-atoms` runs of [ZMX2.md](ZMX2.md). |
| `pack_src/` | Rust source of an earlier packer. |

## Scripts

About 190 Python and 25 shell scripts.  The ones that check shipped certificates (called from `../verify.sh` or a
bundle's `verify.sh`):

| Script | Checks |
|---|---|
| `zeromargin.py` | exact zero-margin checker for point covers (s(13), s(32), s(61)); [ZEROMARGIN.md](ZEROMARGIN.md), [RUNG2.md](RUNG2.md) |
| `zm_d4_sweep.py` | resumable per-root driver of `zeromargin.py` over the D4 region (s(32)); [S32_EXACT.md](S32_EXACT.md) §11 |
| `zm_mixed.py`, `mixed_cover.py` | exact checker and reader for mixed covers (s(21), s(45), s(60)); [ZM_MIXED.md](ZM_MIXED.md) |
| `qx2_zm.py` | exact checker for the k² − 3 / k² − 4 box covers (imports `zm_mixed.py`); [QUADRANT_EXACT.md](QUADRANT_EXACT.md) |
| `qx2_family_check.py`, `qx2_records.py`, `qx2_germscan.py` | family ↔ box cover, run records, tiny-tilt germ scan (k2m3, k2m4) |
| `s21_records.py`, `mixed_records.py` | re-summarise shipped run records and totals with their own parser (s21; s45, s60) |
| `unavoid13_check.py`, `unavoid13_exactcheck.py` | unavoidable-set checker, and the exact B&B certificate checker (`unavoid13_exactcert.py` writes them) |
| `export_points.py` | round-trips the s(11)/s(12) point certificates to JSON |

The s(11)/s(12) point certificates themselves are checked by `../verify/` and `../xcheck.py`; they are produced by
`lp_search.py` and `tighten.py` ([TIGHTEN.md](TIGHTEN.md), [REPRODUCIBILITY.md](REPRODUCIBILITY.md)).  `zmx2` and
`zmcheck` live in `../verify2/`.

Everything else is an investigation script.  Its log names it on the log's `Code:` line, so
`grep -l name.py *.md` finds it.
