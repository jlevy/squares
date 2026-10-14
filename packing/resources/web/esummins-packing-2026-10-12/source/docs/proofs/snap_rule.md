# Rule SNAP — a near-simple square teleports into its slot (A224, 2026-09-15; PI 2026-09-14)

A role whose box sits on a simple slot pose, and whose slot cell no OTHER square can meet, IS that slot square: the
teleport replaces it by the exact slot square at the same side, and the packing lands in the extension stratum. If
that stratum is closed on the window, the node is dead. Tags: [T] proved, [M] measured, [F] false as stated, [C]
obligation. Code `attempts/A224-snap-rule/code/{snap224,strata224,snapscan224,report224}.py` (flag `A224_SNAP=1`,
default OFF) wired into `attempts/A211-coarse-tree/code/{tree211,leaves211}.py`; Lean
`lean/.../Statements/SnapRule.lean` (`snap_assign`, `snap_step`, `snap_dead`, `snap_diag_two` — all theorems);
measurements `attempts/A224-snap-rule/results/{bench224.md,snapscan224.jsonl,bench224.jsonl}`, notes
`attempts/A224-snap-rule/notes/snap224.md`.

## 0. Verdict

> **[T] Rule SNAP (any n).** Let `P` be a packing at side `m` containing the pins of a class `S`, let `p` be a census
> cell not in `S` whose slot box `B_p(m)` lies in the container, and let `Q` be a NON-pin square of `P` such that
> **every other square of `P` has interior disjoint from `int B_p(m)`**. Then `(P \ {Q}) ∪ {B_p(m)}` is a packing at
> side `m` containing the pins of `T = S ∪ {p}` (Lemma SWAP with `|X| = 1` = `teleport_of_swap`). Hence if `T` is
> **dead on a window containing `m`**, no such `P` exists: the node is DEAD. Lean `snap_step` / `snap_dead`.
> **[T] SNAP-DIAG.** `k` roles at `k` pairwise interior-disjoint cells, each blocked only by the others, snap
> together (Lemma SWAP with `|X| = k`); `snap_diag_two` for `k = 2`, `swap_packing` / `cells_swap` for general `k`.
> The target is then `S ∪ {p_1 … p_k}`, and Lemma K1 (kills climb containment) lets ANY closed subset do the killing —
> which matters because A53's census names only `k ≤ 6`.
>
> **[T] The engine's certificate is exactly this hypothesis**, in three clauses: (a) one EXACT separating-axis
> certificate per other ROLE (A161 `box_misses_cell_exact`, taken in `t`, over the role's current pieces) against the
> WIDENED slot box `B_p⁺`; (b) the pins by the class's UNCLIPPED census (A178 `classes178.clipped_by_pin`), and the
> anonymous squares either vacuously (a fully named node) or by an EMPTY option-table row at `p`; (c) the target
> stratum's scoreboard row. The page→side-`m` transfer is Theorem FC Step 2 (`ForcedCorners.fc_transfer`): a side-`m`
> meeter of `int B_p(m)` dilates into `B_p⁺`, so a certified miss of `B_p⁺` certifies the side-`m` miss.
>
> **[F] The PI's expectation that this kills the k5 leaves is false as stated — measured.** Over **every** node of
> **every** A211 g1 certificate (72 pages, 294 nodes carrying a SNAP candidate, `snapscan224.jsonl`): **0 kills, 0
> hand-offs.** The near-simple role never has a clear cell. The obstruction is quantitative and always the same: the
> role's own box still has width (on Y0865's `R.2.3.1.p1…` family `F1` is `x ∈ [1.4999, 1.5769]`, `y ∈ [0.5, 0.5441]`,
> tilt `[0, 3]°` at slot `BL(1,0)`), so its certified core `K'` does NOT cover the cell's far corner, and the
> conditioned square `H` (centre `(2.17, 1.47)`, tilt `53–64°`) reaches an edge through `(2, 0.992)` — it pokes
> `0.008` into the cell at the corner point. The PI's "a second meeter only AT the corner point" is right in the limit
> and wrong at the node's resolution: at box width `0.077` the corner point is a sliver of positive area. Never `0`
> blockers; **65 of 173** candidate slots have exactly ONE blocker, **107 of them `H`**.
>
> **[C] What would make it fire** (§4): the one-blocker case is a Rule NS split on `(H, p)` whose MISSES child is an
> immediate SNAP kill — SNAP does not need a new lemma, it needs the blocker branched, or the role's box bisected
> below the sliver. Rule SNAP stays in the engine behind `A224_SNAP=1` because it is sound, cheap (nothing at all when
> no role is near a slot) and `n`-general: at lower `k` the roles' boxes are smaller and there is no `H`.

## 1. The rule

**1.1 Setting** (`forced_corners.md` §1, `slot_crowds.md` §1). A class `S` is a set of simple slots (corner-anchored
unit cells); a packing `P` at side `m ∈ W = [3.82, s0]` CONTAINS the pins of `S` when `|S|` of its squares are exactly
those slot squares. A census cell `p = (c, i, j)`, `i, j ≤ 2`, is UNCLIPPED for `S` when no pin's open square meets
`int B_p(m)`, and its EXTENSION class is `T = S ∪ {p}` (A53's `name_to_slots` up to `D4`). `B_p(m)` lies in the
container for every `m ≥ 3.82` because `i + 1 ≤ 3`.

**1.2 [T] The swap step.** *If every square of `P` other than one non-pin `Q` has interior disjoint from
`int B_p(m)`, then `P' := (P \ {Q}) ∪ {B_p(m)}` is a packing at side `m`, and it contains the pins of `T`.* **Proof.**
`B_p(m)` is a closed unit square inside `[0, m]²`, interior-disjoint from every square of `P'` other than itself:
from the untouched squares by hypothesis, and `Q` is gone. That is exactly Lemma SWAP's hypothesis with `X = {Q}`
(`ring_swap.md` §1.1, Lean `swap_packing` / `teleport_of_swap`). The pins of `S` are untouched (`Q` is non-pin) and
`p` is occupied by the new square, so the assignment `f` extended by `p ↦ Q`'s index is injective and occupying. ∎
Lean `snap_assign` (the assignment explicitly) and `snap_step`.

**1.3 [T] The closure step — by the ledger.** *If `T` is dead at side `m`, no `P` as in 1.2 exists.* **Proof.** 1.2
produces a packing at side `m` containing the pins of `T`. ∎ The engine reads deadness from the A56/A61/A114/A146
scoreboard (`attempts/A56-sparametric/results/scoreboard.json`, **52/52 FULL `[191/50, 969271/250000]`**,
`residue_ledger.md` §2), through A178's computed table: every usable cell of `k5_11`, `k5_16` and `trump5` has a FULL
`k6` extension —
`k5_11`: `BL(1,1)→k6_18`, `BR(0,1)→k6_20`, `TL(1,0)→k6_20`, `TR(0,0)→k6_23`;
`k5_16`: `BL(1,0)→k6_23`, `BR(0,1)→k6_29`, `BR(1,0)→k6_27`, `TR(0,1)→k6_30`, `TR(1,0)→k6_28`, `TL(1,0)→k6_27`;
`trump5`: `BL(0,2)→k6_07`, `BL(1,1)→k6_19`, `BR(0,1)→k6_21`, `TR(0,1)→k6_22`, `TR(1,0)→k6_24`, `TL(0,0)→k6_23`.
`k6_07 / k6_23 / k6_27` are A114's full-window closures (`k6_27` "the last whole-window k6 class"). **The only open
extension in the corpus is `k0_00`'s `k1_00`**, so a SNAP there is a HAND-OFF, not a kill — the engine records it and
stops the branch rather than claiming anything.

**1.4 [T] SNAP-DIAG.** `k` roles `Q_1 … Q_k` and `k` cells `p_1 … p_k` with pairwise interior-disjoint slot boxes,
such that every square outside `{Q_1 … Q_k}` misses every `int B_{p_a}(m)`. Then all `k` teleports at once give a
packing at side `m` containing the pins of `S ∪ {p_1 … p_k}` — Lemma SWAP with `X = {Q_1 … Q_k}`, the cells being
interior-disjoint from each other by hypothesis and from everything else by the miss certificates. The blockers may
be each other: that is the whole point of doing them at once (diagonal near-simple squares meeting only at their
common corner). Lean `snap_diag_two`; general `k` is `swap_packing` verbatim. **Closure:** the resulting pin set has
`|S| + k ≥ 7` slots and A53's census stops at `k = 6`, so the kill is read off any closed SUBSET — by Lemma K1
(`Skeleton.lean`, kills climb containment) the packing also contains the pins of `S ∪ {p_a}` for each single `a`, and
each of those is a FULL row. `strata224.target` reports which form was used (`via`).

## 2. [T] The certificate the engine emits, clause by clause

| clause | what must hold at side `m` | what the engine certifies on the page | where |
|---|---|---|---|
| (a) named roles | every other role's square misses `int B_p(m)` | every pose of the role's CURRENT pieces gives a square whose interior misses `B_p⁺` (A161 separating axes, exact rationals, taken in `t = tan(θ/2)` so the bin is never rounded inward) | `snap224.role_misses` |
| (b) pins | the pin slot squares miss `int B_p(m)` | `p` is UNCLIPPED for `S` — a combinatorial fact of the census, not a geometric test (the page's SLACK pin boxes could never pass one and do not have to) | `classes178.clipped_by_pin`, `forced_cells` |
| (b) anonymous | no un-named free square meets `int B_p(m)` | vacuous when all 11 squares are named; otherwise the FRESH option table's row `single[p]` is EMPTY (A198's reach of a free square into `B_p⁺` clipped against every role's `K'`) | `snap224.anon_ok` |
| (c) closure | `T` is dead at `m` | the scoreboard row of `T` (or of a subset, Lemma K1) starts `FULL [191/50, 969271/250000]` | `strata224.target` |
| transfer | a side-`m` meeter dilates into `B_p⁺` | Theorem FC Step 2, `π_i = (λ_max − 1)(i + 1 + 1/√2)`; the page's own `wb` | `ForcedCorners.fc_transfer` |

The candidate filter (role box centre within `A224_SNAP_EPS = 0.06` of the slot centre, every piece's tilt bin within
`A224_SNAP_DEG = 3°` of alignment) is a HEURISTIC and carries no soundness weight: SNAP is sound for any role, near or
far. It exists so that a node with no near-simple role costs one pass of floating-point comparisons.

**Where it runs.** Leaf rule (0) — before rule CC — at every fully named leaf, and once per internal node after the
coarse round. With `A224_SNAP` unset neither call does anything: the old engine is unchanged byte for byte.

## 3. [M] What it does on the k5 population

`snapscan224.py ALL --run g1_page` replays the rule on the pose set each recorded node actually had (its snapshot,
padded OUTWARD, so a superset of the node's hypothesis — sound in the same direction as the live rule).

| measure | value |
|---|---|
| A211 g1 certificates scanned | 72 |
| pages with at least one SNAP candidate | 17 |
| nodes with a SNAP candidate | 294 |
| candidate (role, slot) pairs passing clause (b) | 173 of 322 |
| pairs with **0** blockers (SNAP fires) | **0** |
| pairs with exactly 1 blocker | 65 (`H` alone: 52) |
| pairs with 2 blockers | 107 (`F3, H`: 55; `F1, F2`: 16; `F1, F4`: 12) |
| SNAP / SNAP-DIAG kills, hand-offs | **0, 0** |

The live A/B (`results/bench224.md` §2) repeats this inside the search on the brief's five pages and confirms the
verdicts are unchanged with the flag on.

**[F] The PI's Y0865 reading, exactly where it breaks.** At `R.2.3.1.p1.1.2.2.1.1.1x`, `F1` is near-simple at
`BL(1,0)` (centre within `0.038`, tilt `[0, 2.4]°` over 34 pieces) and `F2` near-simple at `BR(0,1)` (within `0.019`).
`F1`'s cell is missed by `F2, F3, F4, F5` exactly, and by no anonymous square (clause (b) vacuous: all 11 named) —
but not by `H`. All 19 of `H`'s pieces fail the miss test against the RAW cell `[1,2] × [0,1]`, not merely against the
`g1`-widened one: `H`'s square at `(2.17, 1.475, 58°)` has an edge from `(2.329, 0.786)` to `(1.481, 1.316)` crossing
`x = 2` at `y = 0.992`. That is the corner sliver the PI's reading treats as a point.

## 4. [C] Obligations and the levers

1. **[C] The one-blocker branch.** 65 candidate pairs have a single blocker `R`. Branching `R` at `p` (Rule NS,
   A206, on the pair `(R, p)` rather than on a sliver fraction) gives a MISSES child in which SNAP kills outright and
   a MEETS child in which `R` is a certified second meeter of `p` — a strictly better-informed split than the
   fractional one the tree uses now. This is the lever the measurement points at; it is not implemented here.
2. **[C] Bisect the near-simple role below the sliver.** SNAP fires as soon as the role's box is narrow enough that
   its `K'` covers the cell's far corner, which forces every other square out. Lemma ROLE-SPLIT already bisects
   roles; the missing piece is choosing the near-simple role and the direction that shrinks the sliver.
3. **[C] Lower `k`.** The rule was asked for "the lower k anyway": at `k ≤ 4` there is no conditioned square `H` and
   the free roles are smaller, so clause (a) has fewer and tighter blockers. Nothing in §1 uses `n = 11` or `k = 5`.
4. **[C] The anonymous clause at a partially named node.** 149 of 322 candidate pairs failed clause (b) — the option
   table row was non-empty or stale. A sharper anonymous test (the union cap of `quick200.union_cap`, which already
   certifies "at most one anonymous meeter") would convert some of these; with `cap = 0` it is exactly clause (b).
5. **[C] `k0_00`.** Its four corner cells extend to `k1_00`, which is OPEN, so SNAP there is a hand-off. It becomes a
   kill the moment `k1_00` closes — the same dependency `k0_route.md` §3 already carries.

Related: `ring_swap.md` (Lemma SWAP, CELLS, the sweep), `forced_corners.md` (Theorem FC, the widened box, the usable
cells), `slot_crowds.md` (Lemma SLOT-CROWD — the same teleport read backwards), `corner_cover.md` (rule CC, which
consumes the same near-simple geometry as a BAND and does not need the cell to be clear), `descent.md` (CORNER-COVER,
CC0), `coarse_tree.md` §5 (Lemma ROLE-SPLIT).
