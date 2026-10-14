# A202 -- fast30: the CLOSED-FORM geometric kill layer (<= 30 s per page), page drawn BEFORE anything slower
(PI directive, 2026-09-10 16:35: "I want this geometry kill chain to be running as fast as possible, and placing all
of its constraints inside of say a 30 second budget, then printing svgs so I can view where we're at, before chasing
longer steps like full branched trees and lp.")

Model: Fable. Short responses, files in pieces <= 250 lines, no interim messages, commit after every shard/branch
(`git add -- <paths>; git commit -- <paths>`; fetch + plain merge only; never pull --rebase / autostash / reset; no
recursive deletes; PYTHONDONTWRITEBYTECODE=1; <= 2 processes, BLAS pinned to 1 thread, affinity 0xFFFF, BelowNormal;
lab ceiling 12 python processes EXCLUDING command lines containing "Claude Extensions" -- check before every launch
and wait; never touch other campaigns' state (A200 and A201 are running in their own directories) or the frozen
verifiers). Agent messaging is broken: everything on disk. Report ONCE at the end.

## Why
A200's "fast phase" is normalise 4 s + the exact option table (A171 multibox REACH tests per cell x slot) 60-140 s +
union/count < 1 s.  The PI's kills are closed-form: discs and half-planes on the CELL RECTANGLES, Lemma CN / A1
between cells, chord rows, pair exclusions -- microseconds each.  Build that layer as stage 0 of the chain, draw the
page, and only then run the exact table (stage 1), the pair tests / SEAL (stage 2), branched trees and LP (stage 3).

## Stage 0 (target <= 30 s per page, every test a SOUND necessary condition; a cell dies only with a proof)
Inputs: the page record (pins, H box + tilt window, class, forced slots with their widened boxes and meeter windows
-- FP.load_page / G.forced_items), the half-grid cells (FP.make_grid), pad g1 and pad 0.
For each (slot, cell) with the cell x tilt window as the pose set:
 (a) REACH: dead if the cell rect is farther than the circumradius 1/sqrt2 (or the tilt-window's max half-extent
     along the relevant axis) from the slot's widened box, or the meeter window misses the cell;
 (b) PINS: dead if every centre of the cell is within 1/2 (inscribed disc) of some pin's stock box -- i.e. the cell
     rect lies inside the pin box dilated by 1/2 (Minkowski disc/rounded rect); for an UPRIGHT-only tilt window use
     the dilation by 1/2 in l-inf instead (bigger, still sound); same against the container walls;
 (c) H (and later every instantiated role): dead if every centre of the cell is within 1 of EVERY point of H's centre
     hull (max over cell corners x hull corners of the distance < 1); for H within phi degrees of upright, also the
     Minkowski bound: no separation along x/y possible unless |dx| >= 1/2 + w(theta) or |dy| >= ..., stated and
     proved in the notes before use;
 (d) chord rows on the pin lines and the wall lines (min chord of the cell x tilt window per line; open chords);
 (e) union caps per slot on the alive cells (CN diameter < 1 => cap 1; A1 l-inf; chord row), Theorem FC demand 2;
 (f) the assignment count (A198 Theorem COUNT) with the CELL-PAIR table: A1, CN, and the closed-form Minkowski
     rule from (c) between chosen cells (A201 is building the exact pair test as a later stage -- do NOT duplicate it;
     read attempts/A201-cell-pair-exclusion/BRIEF.md and notes/ for the rules and the Y0044 worked cases);
 (g) SEAL as closed-form inequalities (A199, docs/proofs/corner_seal.md section 4) where it applies;
 (h) H forced to a slot by the bar-H count; then H's box clipped to the poses meeting that slot (closed form: the
     dip condition), and (b)-(g) iterated to a fixed point (a few rounds, milliseconds each).
Output: a certificate (JSON, live200-compatible fields: nid, verdict, pad, steps with seconds, rounds with single /
union / caps / count / witness, roles, tests; plus `stage`: 0) and the page docs/residue_map/fast30_<nid>.svg drawn
IMMEDIATELY after stage 0 (rules: pins as pins, H's box with a hypothesis square only at an admissible pose, alive
cells grey stipple, dead cells white with the killing rule's letter, slot boxes dashed in colour, the count's witness,
every rule's count of kills and its milliseconds printed, a note saying what the panel IS: "stage 0, closed-form
tests only").  Verdicts: DEAD [C: closed-form trace] or ALIVE with the alive-cell table and the witness cover.
Then, and only then, stage 1 = A200's exact option table on the SURVIVING cells only (fewer REACH tests), page again.
Stop there: stages 2-3 are A200/A201's.

## Runs and report
1. Y0044 first (the PI's page): stage 0 kills? which rules? milliseconds per rule; the page.  Then Y0054, Y0491.
2. All 22 k5_16 pages and the 9 k5_11 pages (docs/shadows/a57v4/review_a57v4.csv alive rows), both pads, stage 0
   then stage 1; results/fast30.jsonl, certs/, pages; kills to the status gallery collector (label the verifier:
   [C: closed-form trace]); registry row, LOG entry, docs/residue_ledger.md section 4, docs/budget.md item.
3. notes/fast30.md: every rule as a lemma for any n with its proof sketch, the PI credited for the layer and for the
   disc / corner / column readings (2026-09-10), the per-page table (stage 0 ms, stage 1 s, verdicts), what stage 0
   could not do and why.
