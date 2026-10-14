# The threshold bound s(11) > 31/8 (external, T-037) — replayed by A242

**Source.** Kleddamag, *11-squares-certified-bound*, release `v1.0.2` (tag object `59dc5626`, commit `6a733f33`),
reviewed as **T-037** in J. Levy's *n11 threshold bound review* (Part II).  Certificate
`global-certificate.json`, SHA-256 `57e9927da5c13f42dd8bcbf8f08c84363635fece626657ee63a810c61cd44458`.
Lab replay and spot-check: `attempts/A242-replay-31-8/` (pin `ext/PIN.json`, verdict `results/replay242.md`).
Lean: `Statements/Open/ThresholdBound.lean` (the bound is an axiom; the Budget lemma and the window restriction are
theorems).

**Status.** EXTERNAL certified lower bound, trust base = their exact Python sweep (replayed by us, row by row) +
their stdlib controls (rerun) + our independent spot-check (a)-(d).  It would shrink the window
**W = [3.82, s0] to W' = [31/8, s0] = [3.875, 3.877084]**.  Adoption is a coordinator decision; nothing on
CURRENT.json or any running campaign was changed (`code/adopt242.py --dry-run` lists what it would touch).

## 1. The two lemmas in our notation

Write `L = 191/50` (container), `A = 764/775` (parent side), `Γ = 0.999962528`, `M = 10.999479944`
(both in units of `10⁻⁹` in the certificate).  A *parent* is a closed square of side `A` in `[0, L]²`; parents of
a packing have pairwise disjoint interiors.

**Scaling lemma.**  `Fits(11, s)` with `s ≤ 31/8` implies that eleven parents of side `A` fit in `[0, L]²`.
*Proof.* Monotonicity puts the packing in `[0, 31/8]²`; the dilation by `A` maps unit squares to side-`A` squares and
`[0, 31/8]²` to `[0, A·31/8]² = [0, L]²`, since `(191/50)/(764/775) = 31/8` exactly.  Hence "no eleven parents in
`L`" gives `Fits(11, s) ⇒ s > 31/8` for EVERY `s` — strict without any compactness (their PROOF.md uses
attainment of the minimum; it is not needed).  [T] arithmetic in Lean: `scaling_arith`, `scaling_side`.

**Cores.**  A row `(a, b, t, B)` of the catalogue assigns to every parent with half-angle `u = tan(θ/2) ∈ [a, b]` the
CLOSED concentric square of side `B` at half-angle `t`.  Rows tile `[0, u_max]` with `u_max > √2 − 1` (all of
`θ ∈ [0, π/4]`); a parent at `θ ∈ [−π/4, 0]` uses the D4-mirror of its mirror's core (sites and charges are D4
invariant, so the charge is the same).  The core lies strictly inside the parent, so the eleven cores are
pairwise DISJOINT closed sets even when parents touch.

**Charges.**  Sites `p` with weights `w_p ≥ 0`; threshold sets `(S, k, w_S)`, `|S| = m ∈ {3, 5}`, `k ∈ {2, 3}`.
`C(Q) = Σ_{p ∈ Q} w_p + Σ_S w_S · [|S ∩ Q| ≥ k]`.

**Budget lemma** (n-general).  For pairwise disjoint sets `Q₁, …, Q_q`,
`Σᵢ C(Qᵢ) ≤ M := Σ_p w_p + Σ_S ⌊|S|/k_S⌋ w_S`.
*Proof.* A site lies in at most one `Qᵢ`.  For one threshold set, the qualifying `Qᵢ` hold disjoint subsets of
`S` of size `≥ k`, so their number `q'` obeys `q' k ≤ |S|`.  [T] Lean `budget_lemma` (`q k ≤ |S|` for disjoint
`k`-subfamilies of a finset; the point case is `k = m = 1`).

**Conclusion.**  If every assigned core has `C ≥ Γ` (the sweep) then eleven parents give `11 Γ ≤ M`; but
`11 Γ − M = 107864 · 10⁻⁹ > 0` ([T] Lean `counting`).

## 2. What the verifier checks, and what it trusts

`exact_mixed.validate` + `expand` (exact `Fraction`/`int`):
1. **catalogue coverage** — rows contiguous from `0`, `a < b`, `0 ≤ t < 1`, `0 < B < A`, and the last `b` has
   `b² + 2b > 1` (`b > √2 − 1`);
2. **angle range** — at both ends the relative angle core−parent is in `[−π/4, π/4]` (`dot > 0`, `dot ≥ |cross|`);
3. **strict core** — `A − B · max_{ends}(cos δ + |sin δ|) > 0` (the maximum over the row is at an end because
   `cos δ + |sin δ|` increases in `|δ|` on that range); minimum margin `10⁻¹²`;
4. **parent envelope** — the legal-centre square of the row is `[r, L − r]²`, `r = A·min_{ends}(c + s)/2`
   (`c + s` is concave, so the union over the row is this square), with `B(c_t + s_t)/2 ≤ r < L/2`;
5. **counting** — `11 Γ > M`, and `M` re-summed from the D4-expanded data equals `budget_units`; every charge
   orbit is a complete D4 orbit; `Σ|expanded coefficients| < 2⁵⁰` (int64 exact).

**The sweep** (`geometry` + `integer_sweep.accumulate`): in the core's frame each site's capture set is a
rectangle; a `k`-of-`m` indicator is the exact inclusion–exclusion sum of its subset rectangles
(`1[Σxᵢ ≥ k] = Σ_{j ≥ k} (−1)^{j−k} C(j−1, k−1) e_j(x)`, exhaustively checked by `verify_threshold_algebra.py`);
the rotated legal square is cut into vertical slabs at every rectangle and polygon abscissa, and a lazy segment
tree gives the minimum charge over every open cell meeting the polygon (cells are taken conservatively: floor /
ceil of the slab's polygon extent).  Each row must have minimum `≥ Γ`.  Boundary centres: the charge is a
nonnegative sum of indicators of CLOSED sets, hence upper semicontinuous, so a lower bound on generic cells
extends to every centre.

**Trusted.**  CPython integer / `Fraction` arithmetic and numpy `int64` (sums `< 2⁵⁰`); the JSON parse; the
correctness of `geometry` (rectangle construction, slab cover, `first/last` query ranges — we read it and found it
conservative); the four hand lemmas (inclusion–exclusion, upper semicontinuity, D4 folding, scaling).  Their second
checker (a JavaScript BigInt scan adapted from Guzhou's R038) was NOT run by us: it is rebuilt from an upstream file
downloaded at run time and needs node (§3).

## 3. The A242 replay (offline, pinned)

* Clone at tag `v1.0.2`, hooks / LFS / submodules off, `core.autocrlf=false` (with CRLF the certificate hash and
  the manifest fail).  `check_integrity.py`: PASS 54 pinned files (before and after the algebra rerun).
  `verify_threshold_algebra.py`: PASS (rewrites its JSON with CRLF; identical modulo CRLF; pinned bytes restored).
* Refused / not run: `verify.py`, `prepare_secondary.py`, `replay_secondary_parallel.py` — they fetch
  `raw.githubusercontent.com/Guzhou0806/…/exact_parent_side_scan.js` over the network and call node.  `pip install`
  of numba (network) not done: `ext/shim/numba.py` makes `njit` the identity, so the SAME kernel source runs
  uncompiled (int64, no overflow possible).
* `code/rows242.py` runs, per row, exactly `replay_parallel.replay()` (their `validate`, `geometry`, `accumulate`,
  `need(z ≥ Γ)`), in two resumable row shards (the lab's 2-python cap), then compares EVERY row's
  `(minimum, cells, slabs)` with both of their recorded evidence files; `independent_controls.py` is rerun as is.
* Hashes: certificate `57e9927d…`, `exact_mixed.py` `f1b9083c…`, `integer_sweep.py` `3a2bfd88…`,
  `independent_controls.py` `bee2a0cf…`, `verify.py` `aff03057…` (all in `results/integrity242.txt`, every file in
  `ext/PIN.json`).
* Verdict, runtime and the row comparison: `results/replay242.md` (written by `code/final242.py` when the
  detached run ends).

## 4. Independent spot-check (lab code, `code/spot242.py`, no import from their repository) — PASS

(a) `(191/50)/(764/775) = 31/8` exactly.  (b) own D4 expansion: 5,284 sites (496 with point weight), 2,220 threshold
sets, D4 invariance of weights and of the charge multiset; budget by family point `2.247714156`, 2-of-3
`3.188007592`, 2-of-5 `0.989672288`, 3-of-5 `4.574085908`, total `M = 10.999479944` = `budget_units`.
(c) 3,240 exact poses — 2,000 random (row, `u ∈ [a, b]`, legal centre), 1,000 on the 47 rows whose recorded minimum
is below the generic `1.000047518`, 240 corners of legal domains — each with the core strictly inside the parent
and the CLOSED capture charge evaluated logically (no inclusion–exclusion): 0 failures, minimum `1.000047518`,
never below their recorded row minimum (equality attained).  (d) `11 Γ − M = 107864 > 0`.

## 5. The consequence (if adopted): W' = [31/8, s0]

* Pads `π_i = (λ − 1)(i + 1 + 1/√2)` at `λ = s0/s`: `λ_max` drops from `s0/3.82 = 1.014943` to
  `s0/3.875 = 1.000538`; `π₀, π₁, π₂` from `0.02551, 0.04045, 0.05540` to `0.000918, 0.001456, 0.001994` (×1/27.8).
  K0-WIDEN's `w = 0.025509` becomes `0.000918`.
* A57 / A211 / A270 / A269 trees: a kill at pad `λ` certifies `[s0/λ, s0]`; on W' every pad with `λ ≥ 1.000538`
  suffices — g1 (`3.861637`), g2, g3, g4, tube, window; only the zero pad (`s0` alone) does not.  The lower slabs
  (A57 grid sides 2–4, A270's g2–g4 campaign, A269's `(3.82, 3.832084]` sub-slab and window pad) are void.
* trump5 tube: the reach needed drops from `ŝ − 3.82 = 0.0571` to `ŝ − 3.875 = 0.002084`.
* Basins (A207): the F-frame drift over `λ ∈ [1, λ₁]` shrinks by the same ×1/27.8; LP-ONLY rows are re-run
  candidates.  A185's k0 cells carry no side field (implied `[3.82, s0]` through K0-WIDEN): re-run candidates at the
  smaller pad, none dead by bookkeeping alone.
* Superseded: the fixed-side measure certificates 3.80 / 3.81 / 3.82 (Theorem 1 stays a Lean theorem).
* Counts (awk tally at launch, A211 + A270 + A269 records, last pass per node and pad): 1,795 nodes; dead on W
  1,638; dead on W' 1,737; **dead at once 99** (k5_11 68, k5_16 31, trump5 0); alive on W' 58.  The script's own
  numbers: `results/adopt242_dryrun.txt`.

## 6. Lean

`Statements/Open/ThresholdBound.lean`: `axiom threshold_bound_31_8 : ∀ s, Fits 11 s → 31/8 < s` [EXTERNAL];
[T] `budget_lemma`, `counting`, `scaling_arith`, `scaling_side`; from the axiom: `lb382_of_threshold`,
`window_restrict` (any statement on `[191/50, b]` follows from its restriction to `[31/8, b]`),
`stratum_kill_of_wnd'`, `trump_residual_of_wnd'` (the two open window axioms of `TopLevel.lean` need only `W'`).
Main's theorems do not use the new axiom.
