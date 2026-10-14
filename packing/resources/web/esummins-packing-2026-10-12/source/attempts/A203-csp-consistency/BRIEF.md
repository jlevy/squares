# A203 -- H-CONSISTENCY and piece-level pair compatibility in the fast count (PI lever, 2026-09-10 18:30)

Model: Fable. Short responses, files in pieces <= 250 lines, no interim messages, commit after every shard/branch
(`git add -- <paths>; git commit -- <paths>`; fetch + plain merge only; never pull --rebase / autostash / reset; no
recursive deletes; PYTHONDONTWRITEBYTECODE=1; <= 2 processes, BLAS pinned, affinity 0xFFFF, BelowNormal; lab ceiling
12 python processes EXCLUDING command lines containing "Claude Extensions" -- check before every launch; never touch
A201's or A202's files or processes: COPY A202's stage-0 code (attempts/A202-fast30/code at the current commit) into
attempts/A203-csp-consistency/code and modify the copy). Agent messaging is broken; report ONCE at the end.

## The PI's readings (credit them by name in every note)
1. fast30_k5_16_interior_Y0839.svg (18:20): "looking at how tight the BR and TR meeter options are, it seems like
   clipping H on both of those (and settling the mutual clip) should basically kill all the options there ... Is there
   any way we bake something into the fast step to help kill these super small slots?"
2. fast30_k5_16_interior_Y0191.svg (17:40): the TL(1,0) meeter pair passes the hull tests (CN 1.056) but no pair of
   MEETING poses is disjoint (coordinator grid: 0 of 1,034 x 2,824) -- see attempts/A202-fast30/notes/PI_pair_table_pieces.md.

Coordinator grid check on Y0839 (y0839_csp_gridcheck.py, in this directory): H's hull x tilt window 53-64 deg gives
2,975 admissible H poses; the count's witness option in cell 10 (serving BL(1,0)+BR(0,1)+BR(1,0), hull
[2.192,2.226]x[0.679,0.762]) has 78 admissible meeting poses and NOT ONE of them is disjoint from ANY H pose; the
cell-23 option (BR(0,1)+TR(0,1), hull [3.353,3.377]x[2.359,2.377]) is compatible with 27 of the 2,975 H poses.
So the witness cover is impossible because H must exist: an option with no H-compatible pose is dead, and a cover
must admit a COMMON H pose compatible with every chosen option.  The pairwise hull table (A1 / CN / MK) cannot see
this: CN passes at 1.076 and 1.01 on the hull corners, in opposite corners of H's box.

## Task: make the fast count a small CSP, closed-form, on PIECES
Variables: H's pieces (sub-rect x tilt bin, as A202 builds them) and, per option, its alive pieces.  Constraints:
 (a) admissibility per piece (container, pins' stock boxes, floor/walls with the tilt bin's half-extent) -- A202 has it;
 (b) piece-piece compatibility by the separating-axis bound with the tilt bins (some direction phi in either piece's
     bin with max over the two sub-rects of |cos(phi) dx + sin(phi) dy| >= 1/2 + w(phi - theta') minimised over the
     other bin; else EXCLUDED) -- closed form, microseconds; cache per (piece, piece);
 (c) H-consistency: an option is dead if none of its pieces is compatible with any H piece; H pieces incompatible
     with every option of a slot H is forced to meet are dead (the MUTUAL clip); iterate with the option build to a
     fixed point (milliseconds);
 (d) the count carries the bitmask of H pieces compatible with every chosen option (AND) and prunes when empty, and
     requires pairwise piece-compatible chosen options (forward checking); a slot's demand-2 pair over MEETING pieces;
 (e) certificate: every exclusion with its rule and numbers; the verdict names the decisive rule; kills labelled
     [C: closed-form trace] (no verifier clause yet -- say so).  Sound direction only.
Budget: stage 0 stays <= 30 s per pad; report the CSP's own milliseconds.
Runs: Y0839 first (both pads) with the page drawn (A202's page style + a CSP panel: the H pieces surviving the mutual
clip, the dead options lettered), then Y0191, Y0044, Y0054, then every page A202 left ALIVE at stage 0
(attempts/A202-fast30/results/fast30.jsonl).  Results in results/csp203.jsonl, certs/, docs/residue_map/csp203_<nid>.svg.
notes/csp_consistency.md: the lemmas for any n (piece compatibility, H-consistency, the mutual clip), the PI credited,
the table; registry row, LOG entry, docs/residue_ledger.md section 4, docs/budget.md item, status gallery block for kills.
