# 05 — The toolkit: geometry before LP, the leaf rules, the exact kernels, what is frozen, how to run one page

**Abstract.** Every tree node of the stratification is a PAGE: pins with certified cores, one conditioned square
H in a (centre box × tilt bin), and n − k − 1 anonymous free squares, at a fixed rational side with a pad for the
window.  The engine forces the geometry to a fixed point before any LP: closed-form rules (stage 0), a CSP on
pieces, multibox cores K′ and the clip cascade, then the leaf rules (corner cover, no-room with lane and pocket-
rooted covers, named split, role split, pocket branching, SNAP, EPS) and inheritance across runs.  Measured
speed-ups: 7.22× geometric mean on closed nodes (A215), 5.0× on no-room nodes (A221).  Pointers only; no code here.

Repository https://github.com/Esummins/packing (paths under `blob/master/`).  Your vocabulary in parentheses.
Rule of the lab (`00-README.md`): every rule is a sound NECESSARY condition on a PIECE = closed centre rectangle ×
closed tilt sub-bin of one square; the union of the surviving pieces is a superset of the true pose set.

## 1. The page and the cores

* **Page** (A57 record format, `geo178.load_record`): pins = the class's slots as upright boxes of half-width
  δ_pin with exact core a = ½ − δ_pin (A84's slack pin cores at δ_pin = 2·10⁻², A270's 9/400); H = one conditioned
  square (a level-1 cover cell of the interior zone [1.1, s0 − 1.1]² × [0°, 90°), or the whole zone at a root);
  budget = n − k − 1; pad ∈ {0, g1, g2, g3, g4 = window} (`01` §2).  Lean: `Statements/Parametrization.lean`.
* **Core** K(B) of a box of poses B = the set of points inside EVERY square of the box (your owned hull / a
  parent's core); **multibox K′** (A132/A135/A171/A172): the core computed per PIECE and unioned, exact rational
  polygons; K′/K area median 1.225 (max 1.53), excluding 22.3 % of dual-support columns.  Clips: the container,
  the mutual K′ clip (a piece of B whose square must meet K′(P) of a pin or another role is dead), the LONELY clip
  at the widened corner box c = 1 + π₀ (Theorem B of `sideband.md`, A173: a NO-family is a clip before it is a
  kill), the pin clip (A131: 132 recorded-open nodes clipped EMPTY in 4.1 s).  Invariant library with a guard
  (A171: a recorded node violating the clipping rule is convicted mechanically).
* **The exact miss test** (A161 `box_misses_cell_exact`): the separating-axis test of a parameter box against a
  cell, taken in t = tan(θ/2) with exact rationals, 8 axis/sign pairs — every miss certificate in the engine.

## 2. Stage 0 and the CSP (closed forms, ≤ 30 s a page)

* **Stage 0** (A202 `fast30`, `attempts/A202-fast30/notes/fast30.md`): the PI's readings as rules on pieces — the
  DISC rule (the alive hull of a cell is the complement of two discs: radius 1 at H's hull corner, ½ at the pin's
  corner), the CORNER rule, the COLUMN rule (a chord limit on a wall lets a column of cells hold one centre), Lemma
  A1 (two meeters' centres ≥ 1/√2 apart in ℓ∞), Lemma CN (a cell against H's hull), Theorem FC's forced cells, H
  forcing (H must be a meeter of a cell no free square can reach).  [M] 8–28 s a pad; kills 1 of 40 pages alone.
* **The CSP on pieces** (A203 `csp203`, `attempts/A203-csp-consistency/notes/`): Lemma PC (two interior-disjoint
  unit squares satisfy, for some axis φ of one of them, |(c_G − c_F)·(cos φ, sin φ)| ≥ ½ + w(t_B − φ)/2); every
  option must be compatible with some H piece, H with some option of every slot a free square must meet, and a
  cover must admit a COMMON H piece.  [M] median 23 s, 296 option rows dead, H forced on 34 of 78 pads; fuzzed
  (0 refutations of 2,872 dead pairs).  Verdicts are `[C: closed-form trace]` — the certificate is the JSON trace.

## 3. The coarse tree and the leaf rules (A211 `tree211`, the live engine)

Order at a fully named leaf: rule CC → no-room + pockets → basin clip → Rule NS → the exact cascade last.
* **Rule CC, corner cover** (A210): the hypothesised second meeter of a forced corner cell must reach the wall
  band; a role whose box cannot is dead.  [M] a LEAF rule: silent at roots (33 ms), decisive at named nodes (15
  kills over 22 certificates in 1.3 s, 4 of them whole subtrees).  Fuzzed 89,240 + 42,262 samples.
* **No-room** (A189 Lemma 1; Lean `noroom_dead`, `pocket_bound` in `Statements/NoRoom.lean`): the free centres
  must fit in the container minus the roles' reach sets; a POCKET of free area too small for its required centres
  is dead.  **Lane cover** (A161/A221: the chord-limited lane on the guard lines {½, 1, 3/2, s/2, s − 3/2, s − 1,
  s − ½}) and the **pocket-rooted cover** (A221 Lemma POCKET-DEAD: the exact clip rooted at the pocket, depth-first,
  with the sound w_min container clip; Lemma POCKET-INHERIT: a parent's pockets cover a child's free centres).
  [M] 68 non-vacuous no-room nodes: 4,685 s → 934 s (**5.0×**), 0 regressions over 314 replayed rows.
* **Named split / Rule NS** (A206): branch a role on "meets the cell / misses it" (or, after EPS, the wedge); the
  MISSES child carries an exact miss certificate.  **Role split** (Lean `role_split`): assign the anonymous
  meeters of a forced cell to named roles.  **Pocket branching** (A208/A211): at k = n − 2 the last two free
  squares are placed pocket by pocket.  **Basin clip** (A207, n = 11 only): a role box inside a certified basin
  of a local minimum (S02, S07, S33) is a (D) discharge, not a kill.
* **Rule SNAP** (A224) and **Rule EPS** (A227/A230): `02` §5.  **Count leaves** (A198/A200 Theorem COUNT; A268
  `count268`: a joint count infeasible over the option table is DEAD — the rule that closed the last live k5 node).
* **Exact-first** (A220): Lemma BUDGET — a cap is a budget, never a claim; the exact cascade runs only where the
  coarse rules leave a fully named leaf.  **Inheritance across runs** (A211 `inherit211`, A229 Lemma PAR / INHERIT):
  a DEAD branch is a theorem about a path key regardless of which run proved it, so shards started from one merged
  state and merged afterwards leave exactly the state one sequential run would — **start-node shards**
  (`run211.py page <nid> --start LABEL`) parallelise one page.

## 4. The exact kernels

* **Integer polycore** (A213): the polygon-core library on integers, bit-exact against the float path (441
  rebuilds, 2,700 vertex tests, 0 mismatches); per call rebuild ×7.0, intersect ×18, certify ×29, axis core ×25.
* **C kernel** (A214, `ckernel214.dll`, 8.7 kB, clang): the quadratic separating test at 16 ns a pair; batch
  `certify_verts` ×10 over the integer path (×321 over the library).
* **Closed-node benchmark** (A215 `results/benchmark215.md`): the live engine against the recorded walls on 11
  agreeing closed nodes — **geometric-mean speed-up 7.22×** (spread 0.16×–43.85×, median 12.03×); on the six
  like-for-like root-to-kill nodes 16.86×.  (A220's exact-first flags: ratio 0.996–1.002, no verdict regression.)
* n = 17 cost (A243): a k = 16 class dies at its root in 0.1–0.6 s; k = 15 in 556 CPU-s for 35 classes; k = 14 in
  826 CPU-s for 68 (`06` §2).

## 5. The n-general lemma files

Each rule's soundness is a prose lemma stated for every n in `docs/proofs/`: `forced_corners.md` (FC), `slot_crowds.md`
(SLOT-CROWD), `sideband.md` (A1, A2, Theorem B, B1), `noroom.md` / A189 (no-room, POCKET), `corner_seal.md` (SEAL,
WEDGE, NO-SECOND), `lemma_eps.md`, `snap_rule.md`, `boxed_windows.md` (Theorem W), `guardline_clause.md`
(Theorem G), `wedged_seal.md`, `k0_count.md` (PUSH, HOLD), `wall_torque.md` (CEIL, TWO-CONTACT, ONE-TILTED), and the
A243 note shows exactly which constants were n = 11 and how they are threaded (`attempts/A243-climb-17-19/notes/
climb243.md` §1: globals, derived pads, defaults, one hard-coded body — `tree209.noroom_at` with m = 11 − len(roles),
unsound at n > 11 and replaced).

## 6. What is frozen and verified

* **Frozen verifier v1** `attempts/A57-shadow-trees/code/verify_case.py` (sha256 521cb01fe656…): exact-core
  case-measure certificates; the chain every window row and the 3.82 bound run under.  Lean `case_verifier_kill`
  (`Statements/CaseVerifier.lean`): the Lean checker is byte-faithful to it (A70, A117: 30/30 byte-identical).
* **Measure verifier** `certs/verify_measure.py` (2a735939d67f…): s(11) ≥ 3.82 (`certs/measure_certificate_3.82.json`,
  two independent exact verifiers; Lean `lower_bound_382`).  **Parametric** `verify_param.py` (A56/A96): the 4-D
  window verifier (Lean `parametrization`).  **v4** boxed windows (Theorem W, Lean end to end); **v5** guard lines
  (Theorem G; a soundness bug found by external review and fixed, `writeup/05_status_sheet.md` §2 — the repro and
  the fix are in the record).  **v3** polygon cores rests on `PolycoreExemptSound` (a certificate clause, not Lean).
* **The coarse-tree kills are `[C: closed-form / library clip trace]`** — there is no verifier clause for a
  tree node yet; the Lean obligation `lemma_CT` (`Statements/Open/ClipTree.lean`) and the tree-file → `cover` /
  `ClosedTree` check on one complete example are the open items (`05_status_sheet.md` §3).  Where we say DEAD for a
  tree node we mean: a trace of exact rational tests, each a sound rule, replayable, not independently verified.

## 7. How to run one page (n = 11) and one census class (n = 17)

```
# one n = 11 page, both pads, 1800 s wall, resumable; certificate certs/coarsetree211_<nid>.json
python attempts/A211-coarse-tree/code/run211.py page k5_11_interior_Y0865 --wall 1800 --pads zero,g1
# shards of one page (A229): --start R.1,R.2   ...   merge = inherit211
# one n = 17 census class at the window pad, no LP (A243); row appended to results/rows243_n17.jsonl
python attempts/A243-climb-17-19/code/run243.py 17 n17_k14_0215 --wall 1800
# the whole descent / climb (two workers, resumable, commits per level)
nohup bash attempts/A243-climb-17-19/code/chain243.sh > attempts/A243-climb-17-19/logs/chain243.log 2>&1 &
```
Environment: Python 3.11+, numpy, `fractions`; `PYTHONDONTWRITEBYTECODE=1`; one process per node; flags
`A220_NOROOM_INHERIT=1 A221_LANE=1 A224_SNAP=1` (set by `run243.py`).  Each run writes a JSON certificate (every
node with its rule, its exact miss certificates and its seconds) and an SVG page under `docs/residue_map/`.

## What we ask

1. Run `06`'s descent on a larger machine (the command above; inputs in `attempts/A243-climb-17-19/results/`).
2. Review the soundness of one leaf rule end to end from its lemma file to its trace (we suggest no-room + the
   pocket-rooted cover, A189/A221), the way your review records do; tell us what a tree-node verifier clause should
   look like in your `verifiers.yaml` terms.
3. If your sqverify-fast style exact sweeps can replace the lane cover (the no-room blocker: ~98 % of a lane run is
   a float witness search, A221 §0), that is the one kernel we would import.

Sources (https://github.com/Esummins/packing/blob/master/): `attempts/{A202-fast30,A203-csp-consistency,A206-named-split,A208-noroom-leaves,A210-corner-cover,
A211-coarse-tree,A213-int-polycore,A214-c-kernel,A215-closed-node-benchmark,A220-exact-first,A221-lane-cover,
A229-start-parallel}/`; `docs/proofs/` as listed; `writeup/05_status_sheet.md`.
