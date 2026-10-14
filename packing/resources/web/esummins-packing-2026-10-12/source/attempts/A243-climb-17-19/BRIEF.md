# A243 -- the simple-square CLIMB at n = 17 and n = 19: does the k5 toolkit kill the non-record branches fast when
# the corners are pinned?  (PI, 2026-10-07: "brief it and run the climb on 17 and 19").
Opus. LAUNCH-AND-EXIT. Ops: short responses, files <= 250 lines, no monitors or waiting turns (runs detached with a
resume block and per-node commits), explicit-pathspec commits, PYTHONDONTWRITEBYTECODE=1, at most 2 python
processes of your own (BelowNormal, affinity 0xFFFF; A242's replay halves and the k5 frontier workers may still be
running -- never touch them or A211's state; use attempts/A243-climb-17-19/{certs,results,logs}), frozen verifiers
untouched, read-only libraries wrapped never edited.  Pages to docs/residue_map/campaigns/A243-climb-17-19/.
Read first: the Squares Project register for the windows (n = 17: record 4.6755300936 = Kleddamag's rational
witness T-065, lower bound 4.66044 T-043 -> window [4.66044, 4.67553]; n = 19: record 4.8856 = 3 + 4 sqrt2 / 3,
lower bound 4.80 T-020 -> window [4.80, 4.8856]; verify both from
https://raw.githubusercontent.com/jlevy/squares/main/packing/frontier/RESULTS.md and cite the T-numbers), A226's
survey226.jsonl (exact record coordinates for n = 17 and n = 19, Ellsworth; n = 17: 8 lattice-slot squares + 7
tilted; n = 19: 11 slot squares + 8 tilted, the ladder band; all four corners flush and singly met in both), the
toolkit's n-dependence: fast30.py (n=11 default), noroom189.noroom(n=11), count203 / Theorem FC (forced cells need
the one-slot extension's closure: at a NEW n there is NO scoreboard -- see task 2), tree211.py / run211.py /
stage209.stage0 (how a page becomes a root: pins + H + anonymous free squares, the A203 CSP, option table), A53
(slot lattice <-> stratum), A238's notes (the Trump-parent k4 run: EmptyBox at the root; SNAP / tube wiring),
docs/proofs/forced_corners.md (FC), noroom.md, snap_rule.md.

## The experiment (no conjecture needed to RUN it; the conjecture only licenses skipping k0)
For each n in {17, 19}: pin the FOUR corner slot squares (the class containing the record; both records have all
four corners flush) and run the geometric climb on the window: stage 0 (fast30) -> CSP (A203) -> coarse tree
(A211 with the pass flags A220_NOROOM_INHERIT=1 A221_LANE=1 A224_SNAP=1) with no LP anywhere.  Then the record's
own deeper classes: pin the record's full slot set (8 at n = 17, 11 at n = 19) and check the tree reaches a
basin / tube around the record (A212's tube leaf generalised: the contraction tube around the record's exact
pose; if the record is not rigid say so -- the n = 19 ladder band may slide).
Measure, per n: nodes, depth, seconds, rule counts (EmptyBox / FC / REACH / NOROOM / CC / SNAP / tube), how many
branches die at the root, how many survive the wall (1800 s per start node, shards via A229 if the root splits),
and what the survivors look like (pages).

## Task
1. GENERALISE the roots: a builder (root243.py) that takes n, the window [s_lo, s_hi], the container side, a
   pin set (lattice slots, corners first) and produces a page/root in the format run211 consumes: pins as pins,
   the remaining n - k squares anonymous, the stage-0 hull from the window.  Every n = 11 constant that matters
   (fast30 n=, noroom n=, count203's n, the pad formula pi_i = (lambda - 1)(i + 1 + 1/sqrt2) with lambda =
   s_hi / s, Lemma A1 / CN unchanged) threaded through; grep the toolkit for every "11" and either generalise or
   PROVE it is not reached.  Unit test: n = 11, pins = Trump's 5 slots, reproduces an A57 root.
2. FORCED CELLS WITHOUT A SCOREBOARD: Theorem FC says a cell next to a pin must be doubly met by non-pin squares
   OR the packing climbs to the k+1 class.  At n = 11 the climb terminates in a closed scoreboard row; at a new n
   there is none.  So run the climb TOP-DOWN as a tree over slot sets instead: branch "the cell at slot S is
   doubly met (two non-pin meeters)" vs "S is a simple square (pin it, go to k+1)"; the k+1 branch is the
   next class; a branch is DEAD when its tree closes; the record's class is the leaf that must survive (tube).
   This is Lemma K1 run forward.  Implement the branching rule (climb243.py) on top of tree211's leaf rules; cap
   the climb depth at the record's k; record the whole tree.
3. RUN n = 17 first (the narrowest window), then n = 19; wall 1800 s per start node, shards; detached, per-node
   commits; resume block.  If the four-corner root does not split within the wall, try the k = 2 (two adjacent
   corners) and k = 1 roots too and report which level the toolkit bites at.
4. REPORT the PI's thesis against the numbers: which fraction of non-record branches die at the root by geometry,
   the deepest alive branch, total CPU-h, and whether the record class is reached and tubed.  Pages: the n = 17 and
   n = 19 roots with their forced cells and the first kills; the record with its slot set and tilted band.
5. Deliverables: code/, results/climb243.md (+jsonl per node), notes/climb243.md (the generalisation, the climb rule,
   its soundness statement: a DEAD branch is a theorem about that slot-set hypothesis on the window), pages,
   registry row, LOG entry.  Report once (<= 15 lines: per-n table, rule counts, verdict on "relatively quickly",
   commits) and EXIT.

## Addendum 2b (coordinator, after the PI: "start at k4 and climb, or at k ~ 15 and descend?") -- BOTH, top-down first
The forward FC tree's "pin S -> k+1" branches should CITE closed k+1 classes, not re-solve them per path.  So:
an A53-style slot-set CENSUS at the window (locked skeletons inside [0, s_hi]^2, lattice from each corner,
D4-reduced) from k_max down to the record's k (8 at n = 17, 11 at n = 19); close each class by its own tree (few
free squares = the toolkit's strongest regime); the per-class verdict table is that n's window scoreboard; the
record's class must survive to the tube.  Then the climb from the four-corner root uses the table: a "pin S" branch
is DEAD at once when its slot set lies in a closed class (Lemma K1), so the climb is only the "all pin-adjacent
cells doubly met" spine.  Report both halves: classes per k, how many die at the root, CPU-h for the descent, then
the climb with the table in place.
