# A221 -- the pocket cover, and pocket inheritance (n-general)

Notation as everywhere in this repo: `n` unit squares in `[0, s]^2`, a node fixes `k` boxed roles at their A171/A172
multibox fixed point, `m = n - k` squares are free.  `K'(R)` is A132/A172's certified core of role `R`: a convex
polygon contained in EVERY pose of `R`.  A pose `(c, th)` of a unit square is FREE at a node when its interior lies
in the container and misses every `K'(R)`.

## 0. What A189 does, and where its 120 s goes

A189's NO-ROOM leaf is two machines:

1. **the bisection** `bisect_free`: the free square's `(centre, tilt)` space over the whole container
   `[1/2, s-1/2]^2 x [0, 90]`, halved against the roles' obstacles with `multibox._clip_rect_obstacle` (the exact
   convex dead-set clip).  Every dropped piece is certified "every pose in this piece meets some core".
2. **the lane** `Node.lane(P_j)` on each pocket `P_j` of the residue: A141/A161's cover, which answers
   `LANE(P_j) >= #{pairwise interior-disjoint FREE squares meeting int(P_j)}`, and A189's Lemma 1 concludes
   `m <= sum_j LANE(P_j)`.

Measured (results/experiment221.md): on the four k = 10 nodes the bisection costs **3.7 - 9.3 s and EXHAUSTS** (it
stops at its own depth cap, not at the deadline), and the lane then burns **109 - 115 s of the 120 s cap and returns
`None`**.  The lane is the blocker, and it is the blocker for a structural reason:

> `chordlane.lane_out(cell, ...)` roots its cover at `polylane.centre_window(cell, s)` -- the centres of unit squares
> **meeting** `int(cell)`, i.e. the pocket grown by `1/sqrt(2)` on every side.  A pocket of `0.65 x 0.30` (area 0.20)
> becomes a root of `2.06 x 1.71` (area 3.5): **17x the pocket**, and it is exactly the grown collar -- far from the
> roles that made the pocket -- that the cover cannot discharge.

The lane is answering a harder question than the node needs.

## 1. LEMMA POCKET-DEAD  [T]

Let `P_1..P_r` be axis-aligned rectangles whose union contains the CENTRE of every free pose (A189's `pockets_of`
returns such a cover of the bisection residue).  Call `P` **dead** when every pose `(c, th)` with `c in P` and
`th in [0, 180)` meets some `K'(R)`.

> **If every `P_j` is dead, the node has no free unit square at all, hence the node is DEAD for every `m >= 1`.**

*Proof.* A free square's centre lies in some `P_j`; `P_j`'s certificate excludes its pose. []

The certificate for one pocket is the **same exact machine as the bisection, rooted at the pocket**: halve
`P x [0, 90]` (`multibox.split_piece`), drop a piece as soon as `multibox._clip_rect_obstacle` empties its rectangle
against some role's obstacle, and additionally drop by `multibox.container_clip(..., strict=False)` -- a pose whose
tilt sub-bin has `w_min = min(|cos| + |sin|)` has its centre in `[w_min/2, s - w_min/2]^2`, so that clip is sound
(it is the *non-strict* one; the strict `w_max` clip would NOT be sound here).

Cost: the pocket cover buys about `log2(area(meeting window) / area(pocket)) ~ 4` extra halvings per coordinate for
the same piece count, and it never touches the collar the lane chokes on.  It is also *monotone in the node*: a
child with larger cores can only kill more.

Relation to A189: LEMMA POCKET-DEAD is strictly stronger than `LANE(P_j) = 0` **as a node verdict for m = 1** and it
subsumes A209's Lemma CN (`cn_bound`) whenever it fires, but it is NOT a counting bound -- for `m >= 2` a surviving
pocket still needs A189's `LANE` (or A209's CN groups) to be counted.  A221 changes nothing there.

## 2. LEMMA POCKET-INHERIT  [T]

Let a child node arise from its parent by one of the branch rules the trees use:

* **Rule NS** (A206): a role's box is replaced by its meet/miss subset;
* **ROLE-SPLIT** (A211 `rsplit211`): a role's box is replaced by one half;
* **POCKET instantiation** (A209 `apply_pocket`): a NEW role is added, the existing roles untouched;
* any cascade round on top of these (A171 clipping only ever removes poses).

In every case each role of the parent has, in the child, a pose set CONTAINED in its parent pose set.  `K'` is an
intersection over the surviving poses, so shrinking a role's pose set can only **enlarge** its core:

    K'_parent(R)  subset of  K'_child(R)   for every role R of the parent.

Hence a pose excluded by the parent's cores is excluded by the child's, so

    { free poses of the child }  subset of  { free poses of the parent },

and therefore

> **the parent's pockets cover the child's free centres.**

*Consequence* (`noroom221.noroom_child`): a child may skip the container-wide bisection entirely and run the pocket
cover of LEMMA POCKET-DEAD on its **parent's** pocket list with its **own** (larger) cores.  Only when an inherited
pocket survives does it pay for a fresh global bisection.  Sound for every `m`; for `m = 1` no completeness is lost
relative to running the child's own bisection first, because a surviving pocket falls through to the full leaf.

Two cautions that the implementation respects:

* the inherited list must come from an ANCESTOR on the same path, never from a sibling (siblings are incomparable);
* a pocket list recorded *after* A189's `max_pocket_area` early-out, or after a bisection that stopped on its
  DEADLINE, is still a sound cover (the early-out is a budget decision, and a deadline-stopped bisection's open
  pieces are still a superset of the residue) -- but a list recorded when the bisection hit its PIECE CAP is too,
  for the same reason.  Every stop reason of `bisect_free` leaves a cover; only an *empty* pocket list means "no
  residue", which is already a kill.

## 2b. What the benchmark actually showed (results/bench221.md), and the honest limits

* **0 regressions** in the shipped configuration over 314 replayed rows (the one regression on record is
  `Y0738 R.1.2.3`, k = 9, under the code before Lemma CN was in this module -- see the last bullet).
* **verdict agreement on the closed pages** Y0500 g1 and Y0460 g1: 24 non-vacuous no-room nodes, 9 DEAD -> DEAD and
  15 UNDECIDED -> UNDECIDED, 1835 s -> 712 s.
* **three genuine new kills**: `Y0402 zero_page R.3.1.2.1` (12.9 s), `R.3.1.2.2` (16.9 s) and
  `Y0738 zero_page R.1.3.3.2` (12.4 s), all left UNDECIDED at the cap by the certificate -- and 3.1-4.3 s each under
  Lemma POCKET-INHERIT.  Attributed to the COVER by a control: A189's own leaf on exactly the same replayed boxes
  returns UNDECIDED at 131-133 s on all three.  (A third node, `R.3.1.1.1.2`, also comes back
  DEAD -- but the control kills it too, so that one is the replayed boxes being tighter than the ones the tree's
  `noroom_at` was handed, not A221.  A node record's `roles` is the page's LIVE dict, so a certificate can carry a
  later, tighter box than the leaf saw; every "new kill" claim needs this control.)
* **THE CAP is the real budget lever.**  Over 42 pocket covers, *every* DEAD pocket died in <= 0.1 s and *every*
  surviving pocket burned the entire 45 s: the cover either collapses at once or not at all.  So `pk_deadline`
  drops to 5 s (a 50x margin) and an UNDECIDED node costs build + bisect + 5 s a pocket.  Measured at 5 s over the
  36 no-room nodes of Y0402 / Y0500 / Y0460 / Y0738: 2550 s -> 436 s (**5.9x**), slowest node 25.3 s, verdicts
  identical.  Final numbers over all four pages, 68 non-vacuous no-room nodes: **4685 s -> 934 s (5.0x)**, slowest
  node 28.5 s; with Lemma POCKET-INHERIT on Y0402's 25 nodes: **1573 s -> 258 s (6.1x)**, slowest 25.2 s, and a
  child whose inherited pockets all die is decided in 3.0-4.6 s with no container bisection at all.
* **the cost side**: for `m >= 2` (k = 9) an UNDECIDED node is now *slower* than A189 (e.g. 6.5 s -> 15.3 s),
  because A189 with `max_pocket_area = 0` never even tries a cover there.  Lemma CN is tried FIRST (it is free), so
  a node CN can kill still costs what it did; the extra seconds buy the cover's extra kills.
* **the honest limit**: on these pages most UNDECIDED-at-cap nodes are *genuinely* undecidable by no-room -- their
  surviving pocket really holds free poses (experiment221.md s.3b: 88 % of the pocket's volume still open after 48
  halvings).  A221 cannot kill those and nothing can; what it does is stop paying 120 s to find out.

## 3. What A221 ships

* `code/noroom221.py` -- `cover_rect` (the pocket-rooted exact cover), `pocket_dead`, `pocket_pass`,
  `noroom(roles, ...)` (global bisection then the pocket cover in place of the lane) and
  `noroom_child(roles, parent_pockets, ...)` (LEMMA POCKET-INHERIT).  Wraps A189/A171; edits nothing.
* `code/tree209_integration.diff` -- the flag-gated one-liner (`A221_LANE=1`) that routes `tree209.noroom_at`
  through `noroom221`, handing it the parent node's recorded `noroom.pockets`.  To be applied after A220 lands.
* `code/bench221.py`, `results/experiment221.md`, `results/bench221.md`.

## 4. Reuse at higher n

Nothing above mentions 11.  `noroom` / `noroom_child` take `n` as an argument, and both lemmas are stated for
arbitrary `n`, `k`, `m`.  For larger `n` the pockets are what changes: more free squares means a bigger residue and
more pockets, so LEMMA POCKET-DEAD fires less often on its own and the counting bound (A189 Lemma 1, A209 Lemma CN)
carries more of the weight -- but every pocket the cover kills is one the counting bound no longer has to price,
which is a strict gain at every `n`.

## 5. Resume

Everything A221 runs is a replay of recorded certificate nodes -- no tree, no shared state, nothing to restart.  To
re-run or extend the benchmark:

```
PYTHONDONTWRITEBYTECODE=1 sh attempts/A221-lane-cover/code/run221.sh all      # or: four | closed
PYTHONDONTWRITEBYTECODE=1 python attempts/A221-lane-cover/code/bench221.py     --cert attempts/A211-coarse-tree/certs/<cert>.json --run g1_page --verdict any     --cap 120 --pk-deadline 5 --tag <tag> [--inherit] [--engine a189]     --out attempts/A221-lane-cover/results/bench221.jsonl
PYTHONDONTWRITEBYTECODE=1 python attempts/A221-lane-cover/code/table221.py    # -> results/bench221.md
```

Rows are appended with a `tag`; `table221.py` keeps the LAST row per `(tag, page, run, node)`, so a re-run of a lane
simply supersedes it.  `--engine a189` is the control (A189's own leaf on the same replayed boxes) and must be run
before any "A221 kills what A189 did not" claim.  Two BelowNormal pythons at affinity `0xFFFF` is the whole budget.

## 6. Integration (after A220 lands)

`code/tree209_integration.diff` applies cleanly to `attempts/A211-coarse-tree/code/tree209.py`
(`git apply --check`).  It is OFF unless `A221_LANE=1`.  Before turning it on, run one page both ways
(`run211.py page <page> --pads g1 --wall 1800` with an isolated cert dir) and compare verdicts node by node --
A221 is designed to be at least as strong at every node, so any verdict that gets WEAKER is a bug, and the
seconds should fall on every node whose no-room hit the cap.
