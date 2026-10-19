# The SWAP LEAF — proving STEP on a cell by certificate (A232, 2026-09-15)

The PI (17:30): *"can we prove STEP against the window? we only need it true ≤ ŝ for the search to ignore k0
entirely."*  This file makes the leaf exact, states what a certificate is, proves it sound from Lemma CELLS,
and reports what it does — and does not — decide on the eleven converged-alive `k0_00` cells.  Tags: [T]
proved, [M] measured, [F] false as stated, [C] obligation.  Companions: `ring_swap.md` §1 (Lemma SWAP,
Lemma STEP, Lemma CELLS, Lemma RAISE), `k0_route.md` §3 (K0-FREE, k1-a) and §4.1 (Lemma K0-WIDEN),
`realign.md` §5 (`fourcrowd_dead_of_step_kill`: at n = 11, STEP + k1-a excludes four-crowds),
`boxed_windows.md` (the cell = role boxes over the window).  Code `attempts/A232-swap-leaf/code/`, results
`results/swapleaf232.{md,jsonl}`, certificates `certs/`, pages `docs/residue_map/campaigns/A232-swap-leaf/`,
Lean `Statements/SwapLeaf.lean`.  n-general throughout; n = 11 in §3–§4.

## 0. Verdict

> **[T] The leaf is sound and it is a theorem in Lean** (`swap_leaf_dead`, standard axioms only): a cell
> carrying a swap-leaf certificate — an injection `ι` naming the exchanged roles `X`, `|X|` unit squares at
> FIXED poses inside every container of the window, pairwise interior-disjoint, one of them the corner slot,
> and one exact MISS certificate per (square, role outside `X`) — is EMPTY at every side at which no packing
> has a settled corner (k1-a).  No LP, no load, no minimality; rattler crowds are covered exactly like loaded
> ones.  `|X| = 1` is K0-FREE, `|X| = 2` is the PI's STEP, larger `|X|` is allowed.  A new stdlib verifier
> `verify_swap232.py` decides the clause exactly (`swap-leaf-certificate-v1`); the frozen `verify_case.py`
> and `verify_case_v4.py` are untouched.
> **[T] Lemma X-FORCED and Lemma SPLIT-INVARIANCE are what decide the k0 lane.**  A role with no box can be
> anywhere, so it must be in `X`: `|X| ≥ u`, the number of UNBOXED roles of the cell.  A185's split refines
> the boxed roles' pieces and never boxes a role that was unboxed, so `u` — and with it the lower bound on
> `|X|` — is invariant under any number of split rounds.  **Only CONDITIONING (the cascade's YES branches)
> lowers it.**
> **[M]/[F] On the eleven `k0_00` cells the leaf does not fire, and not because the search is weak.**  Those
> cells box ONE of the eleven squares (A115's conditioned square `H`; `budget` 10), so `u = 10` and the leaf
> asks, at every corner, for **ten** pairwise interior-disjoint unit squares in `[0, 3.82]²`, one at the
> corner slot, all missing `H`'s reach set — an object barely weaker than the theorem itself (`s(10)` =
> 3.70711, slack 0.113, against a reach set of area 1.64–1.82 sitting in the middle of the container).  The
> search places 6–9 of the 10 — ONE SHORT on several cells; one round of A185's split into 16 children
> changes nothing (Lemma SPLIT-INVARIANCE).  So **the PI's hope does not come off from the k0 ROOT cells:
> STEP on W is not certifiable cell-wise there, and k0_00's row is unchanged.**
> **[M] the machinery is not at fault**: the geometry controls (n = 5, no k1-a claim) produce and PASS
> `|X| = 1` (K0-FREE), `|X| = 2` (STEP) and `|X| = 5` certificates end to end, and seven corruption tests of
> a passing certificate are all refused.
> **[C]/price.** The leaf becomes available exactly where the cell boxes most of the squares.  At
> `k0_route.md` §4.2's crowd-conditioned root `H_B` (the four corner crowds, EIGHT boxed roles) `u = 3` and
> `|X| = 5` at a corner — the right place to fire it; reaching such nodes is the k0 cascade, priced at
> `k0_route.md` §8 (3 200–7 000 CPU-h).  The leaf does not replace that cascade; it is a LEAF for it.

## 1. [T] The leaf, exactly

**1.1 Setting.**  A window `W = [m_lo, s0]` with `3.82 ≤ m_lo < s0 ≤ ŝ`.  A CELL is a list of `n` ROLES; a
BOXED role carries pose PIECES (a centre rectangle × a tilt bin) stated at `s0` on the dilated configuration
`F = Δ_λ P` (A115/A183/A185's convention, `boxed_windows.md`), an UNBOXED role carries none.  A packing `P`
of `n` unit squares at a side `m ∈ W` BELONGS to the cell when some bijection of its squares to the roles
puts every boxed role's dilated square in one of its pieces.  The REACH SET of a boxed role is the union of
the posed unit squares over its pieces.

**Lemma PULL-BACK [T]** (Lemma K0-WIDEN, `k0_route.md` §4.1, read backwards).  Let `Q ∈ P` at side `m` carry
the role whose piece at `s0` has centre rectangle `[x0, x1] × [y0, y1]` and tilt bin `[θ0, θ1]`.  Since
`Δ_λ` is the dilation about the origin, `c_Q = c_{Δ_λ Q}/λ` with `λ = s0/m ∈ [1, λ_max]`, `λ_max = s0/m_lo`,
and the tilt is unchanged.  Hence `c_Q ∈ [x0/λ_max, x1] × [y0/λ_max, y1]` with the SAME tilt bin. ∎

**Lemma CORNER-FRAME [T].**  Let `g_c` be the D4 map of `[0, m]²` taking the corner `c` to BL (`x ↦ m − x`
and/or `y ↦ m − y`).  It is an isometry of the container, so `g_c P` is a packing at side `m` and `P` has a
settled corner `c` iff `g_c P` has a settled BL.  Over `m ∈ W` the image of a pulled-back centre range
`[X0, X1]` under a flip is contained in `[m_lo − X1, s0 − X0]`, and an odd number of flips sends the tilt bin
`[θ0, θ1]` to `[90 − θ1, 90 − θ0]`.  These supersets are m-FREE. ∎  (They cost the window's width, 0.0571, in
each flipped coordinate; that is the whole price of working at a corner other than BL.)

**1.2 Lemma SWAP-LEAF [T] (any n, any side of W).**  Fix a corner `c` and a set `X` of roles of the cell,
`|X| = k`.  Suppose there are `k` unit squares `F_0 … F_{k−1}` — FIXED poses in the BL frame of `c` — with

  (a) `F_b ⊆ [0, m_lo]²` for every `b`, hence `F_b ⊆ [0, m]²` for every side `m ∈ W`;
  (b) `F_0 = [0, 1]²`, the corner slot square;
  (c) the `F_b` pairwise interior-disjoint;
  (d) for every role `r ∉ X` and every piece of `r`, every pose of that piece (pulled back by Lemma
      PULL-BACK and flipped by Lemma CORNER-FRAME) gives a unit square whose interior misses `int F_b`, for
      every `b`.

Then every packing `P` of the cell, at its own side `m`, exchanges — at the SAME side — into a packing
containing all the `F_b`, in particular with the corner `c` settled.

*Proof.*  Put `Π := {F_0, …, F_{k−1}}` in the frame `g_c`.  `M(Π)` = the squares of `g_c P` whose interiors
meet a member of `Π`.  By (d) no square carrying a role outside `X` is in `M(Π)`, so `M(Π) ⊆ X` and
`|M(Π)| ≤ |X| = |Π|`.  By (a) every `F_b` lies in the container and by (c) they are pairwise interior-
disjoint, so **Lemma CELLS** (`ring_swap.md` §1.3, Lean `cells_swap`) applies: `g_c P` exchanges into a
packing at side `m` containing every `F_b`.  Pull back by `g_c^{-1}`. ∎

**Corollary [T] (the leaf).**  If moreover no packing at side `m` contains a corner slot square (k1-a,
`k0_route.md` §3), then the cell contains no packing at side `m`: it is DEAD.  Lean `swap_leaf_dead` /
`swap_leaf_corner`, theorems from `cells_swap`; `hboxF`, `hdisj`, `hslot`, `hcell` are (a)–(d) verbatim.

**1.3 The certificate and its verifier.**  `swap-leaf-certificate-v1` carries `m_lo`, `s0`, the corner, the
full role list WITH the s0 pieces, the set `X`, and the cells (`axis` cells by lower-left corner, or four
exact rational vertices — a tilted cell uses `(cos, sin) = ((1 − u²)/(1 + u²), 2u/(1 + u²))` at rational `u`,
so every vertex is rational).  `verify_swap232.py` (stdlib + `Fraction`) re-derives the pull-back and the
corner frame ITSELF from the s0 pieces and then checks (a)–(d) exactly: (d) by A161's full separating-axis
test over the parameter box for an axis cell, and by the polygon's own edge normals with the posed square's
support radius bounded by `|n|·√2/2` for a tilted one (sound, deliberately incomplete — a failure is
reported as *not certified*, never as *meets*).  It also refuses any certificate in which a role outside `X`
is unboxed (§2).  The k1-a citation is printed as a DEPENDENCY on every PASS and is not checked there.
**Independence:** the search proposes, the verifier decides; a run writes a DEAD row only on a PASS.

## 2. [T] What `X` must contain — and why splitting cannot help

**Lemma X-FORCED [T].**  An unboxed role constrains nothing, so clause (d) can never be certified for it:
every unboxed role must lie in `X`.  Hence `|X| ≥ u :=` the number of unboxed roles of the cell, and the
leaf demands at least `u` pairwise interior-disjoint unit squares in `[0, m_lo]²` with one at the corner
slot.  Adding the boxed roles whose reach meets the slot (which are in `X` by definition of the leaf):
`|X| = u + #{boxed roles reaching the corner slot}`.

**Lemma SPLIT-INVARIANCE [T].**  A185's split (and every refinement of the cell in the boxed-windows
family) replaces a boxed role's pieces by a cover of them.  It changes no role from unboxed to boxed.  So
`u` is invariant under any number of split rounds and so is the bound `|X| ≥ u`.  **Splitting shrinks the
obstacles, never the demand.** ∎

**Corollary [T] (where the leaf lives).**  The leaf is available at a cell with `u` unboxed roles only if
`u` unit squares, one of them a corner slot, fit in `[0, m_lo]²` avoiding the boxed roles' reach sets.  At
`n = 11`, `m_lo = 3.82`: `u = 1` is K0-FREE and always available; `u = 2` is the PI's STEP; `u = 10` (the
k0v4 cells) asks for a ten-square packing of a container with 0.113 of slack over `s(10) = 3 + 1/√2`, with a
hole in it.  **The leaf's strength is exactly the cell's boxing depth.**

## 3. [M] The eleven `k0_00` cells

`results/swapleaf232.md` (per-cell and per-corner tables), `results/swapleaf232.jsonl`, pages
`docs/residue_map/campaigns/A232-swap-leaf/swapleaf232_<cell>.svg` (four panels, one per corner, each drawn
in that corner's BL frame: the container at 3.82 solid with `s0` dashed, the role's centre box thin dashed
orange, its REACH SET grey-stippled, the slot square blue, the placed leftovers orange, and an exact
geometry check per panel).

Every one of the eleven cells is A115's `..._warm.t4/t5.lp.json` record: **one** hypothesis box (the
conditioned square `H`, tilt bin 30°–45°, centre box ≈ 0.105 × 0.105) and `budget` 10 — so `u = 10`, `H` is
the single role outside `X` at three or four corners, and `|X| = 10` at every corner of every cell.  The
reach set of `H` in the corner frame takes 1.64–1.82 of area out of the 14.59 of `[0, 3.82]²` and sits in
its middle.  The search (bottom-left lattice fill with randomised restarts, plus tilted leftovers by
clearance, every pose re-decided by the verifier) places 6–9 cells — ONE SHORT of the ten on several cells; with no obstacle at all the same search
places 9 (the axis maximum in a container of side < 4).  One round of A185's split, 16 children (2 × 2 centre × 4 tilt) at the best corner of each cell,
raises nothing — as Lemma SPLIT-INVARIANCE says it cannot.

**[F] "|X| = 2 with X = the two corner meeters is the PI's STEP" is right as a statement of the leaf and
wrong as a description of these cells.**  `X` there is not a choice: it is forced to contain all ten unboxed
roles.  A cell where `X` can be the two corner meeters is one where the other nine squares are boxed away
from the corner — a depth-9 conditioning, not a root.

**[M] controls (n = 5, so no k1-a claim; `results/swapleaf232.md` §Controls).**  `|X| = 1` (K0-FREE, a bare
teleport), `|X| = 2` (STEP: the slot square plus one leftover) and `|X| = 5` certificates are produced and
PASS the verifier.  Seven corruption tests of a passing certificate — a role dropped from `X`, a cell moved
onto a role, the slot cell moved off the corner, two cells overlapped, a cell pushed outside the container,
an unboxed role left outside `X` — are all refused.  **An `|X| = 2` control cannot be built at n = 11 inside
the window: a passing leaf there IS the theorem `s(11) ≥ ŝ`**, which is why the controls are stated at
n = 5.

## 4. What closes, and what it would take

* **[T] Nothing about k0_00 is weakened and nothing is strengthened.**  The leaf is a new, sound, load-free
  leaf type with an exact verifier and a Lean theorem; it fires at no k0v4 cell.  `k0_00`'s residue row is
  unchanged, and the obligation RAISE(0 → 1) of `ring_swap.md` §1.5 stands exactly as A222 and A231 left it.
* **[T] The geometric fact that blocks them** is Lemma X-FORCED applied to a cell that boxes one square of
  eleven: the leaf needs ten cells, and the ten cells must be a near-record 10-packing of `[0, 3.82]²` that
  also avoids `H`'s reach.  It is not a search failure and it is not repaired by a finer split (Lemma
  SPLIT-INVARIANCE), nor by a LARGER `X`: `|X| = 11` asks for an eleven-square packing of `[0, 3.82]²`,
  which is the theorem.
* **[C] Where to fire it, and the price.**  `|X|` falls only with CONDITIONING.  At `k0_route.md` §4.2's
  crowd root `H_B` — the four corner crowds, two squares each, EIGHT boxed roles, budget 3 — `u = 3` and, at
  a corner, `|X| = 3 + 2 = 5`: five cells, one at the slot, missing six reach sets.  That is the first node
  of the k0 lane at which the leaf has a chance, and it is also the first node at which the k0 cascade has
  paid its eight conditionings; `k0_route.md` §8 prices the lane at 3 200–7 000 CPU-h.  **The leaf therefore
  does not let the search ignore k0; it gives the k0 tree a cheap, LP-free, load-free leaf rule (a few
  seconds per node) to run beside its LP leaves**, and it subsumes the teleport leaf (T) at `|X| = 1`.
* **[C] A cheaper route to the same end** remains RAISE(0 → 1) as a geometric lemma (`ring_swap.md` §1.5),
  which is a statement about every k0 packing and needs no cell at all.  A232 says only that the
  cell-wise certificate route cannot deliver it from the cells the lab has.

## 5. Lean, files, resume

`lean/.../Statements/SwapLeaf.lean`: `swapCfg`, `swapCfg_eq`, `swapCfg_ne`, `swap_leaf_exchange`,
`swap_leaf_pins`, `swap_leaf_dead`, `swap_leaf_corner` — **all theorems**, standard axioms only (no new
axiom; k1-a enters as the hypothesis `kill`, exactly as in `no_packing_of_raise`).  `lake build` +
`lean/audit.py` exit 0, no sorry.
Code: `cell232.py` (cells, the corner frame, reach sets, `X`, the split, the certificate), `search232.py`
(the placement search and its exact acceptance), `verify_swap232.py` (the clause), `swapleaf232.py` (the
driver, per-cell commits), `pages232.py`, `summarise232.py`, `run232.sh`.
**Resume:** `bash attempts/A232-swap-leaf/code/run232.sh [wall_seconds_per_cell]` — rows already in
`results/swapleaf232.jsonl` are skipped, each cell is committed as it finishes.
