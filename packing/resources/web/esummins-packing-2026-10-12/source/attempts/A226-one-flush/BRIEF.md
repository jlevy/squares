# A226 -- ONE-FLUSH: for the k0 exclusion to work at any n it must be something invalid about the IDEA of packing n
# into side < ceil(sqrt n): at least one corner can always be teleported to flush (PI, 2026-09-14 23:40).
Fable. LAUNCH-AND-EXIT. Ops: short responses, files <= 250 lines, no monitors or waiting turns, explicit-pathspec
commits, PYTHONDONTWRITEBYTECODE=1, <= 1 python process (the lab is at its ceiling), never touch running workers.
Pages to docs/residue_map/campaigns/A226-one-flush/.  Read first: k0_route.md s.3 (K0-FREE, teleport), ring_swap.md
(SWAP, CELLS, RAISE = the k0 obligation, why the sweep count fails), two_grains.md (FLUSH, FOUR-WALL <=> STUCK-4, the
click and why the chain formula is not monotone), wall_torque.md, k0_count.md, wall_budget.md, frame_census.md,
corner_seal.md, descent.md (Lemma CH: the corner hurt), sideband.md.

## The PI's framing
"We know from Trump that not all corners are flush, and I suspect that in the general case no non-trivial optimal
solution has 4 flush corners, but we need some way of showing that in the general case AT LEAST ONE corner can
always be teleported to flush."  I.e. Conjecture ONE-FLUSH (any n with s(n) < ceil(sqrt n)): every optimal packing
has a corner box met by <= 1 square (so K0-FREE teleports it flush); equivalently STUCK-4: no teleport-stuck packing
exists below ceil(sqrt n).  At n = 11 this IS the k0_00 obligation.

## Task
1. SURVEY first (cheap, decisive for the shape of the argument): for every n whose best-known packing beats
   ceil(sqrt n) (n = 5, 10, 11, 17, 18, 19, 26-29, 37-41, 50-54, ...; Erich Friedman's "Squares in Squares" page via
   WebFetch, and any coordinates already in the repo: Goebel n = 10, Trump, the A-series shadows), count the FLUSH
   corners and the corner boxes met by <= 1 square.  Table: n, side, flush corners, singly-met corners, source.  If
   any best-known packing has all four corner boxes doubly met, ONE-FLUSH is false as stated and the n = 11 proof is
   special -- say so.  Also the PI's second conjecture: no non-trivial optimal packing has 4 flush corners (check the
   same table).
2. MECHANISM: what a general argument needs.  Collect what is known to fail (the sweep count: mid-sweep one meeter
   blocks; the click: chain formulas rise toward alignment near 45 deg; area/waste: a doubly-met corner wastes far
   less than ceil(sqrt n)^2 - n) and look for what a 4-crowd FORCES on the whole perimeter: eight non-simple meeters,
   two per wall, each wall's chain formula (GRAIN-LP) then exceeds the flush length by a positive amount that depends
   on the meeters' tilts; the wall budget (wall_budget.md) and the frame census (frame_census.md) may already bound
   the perimeter; Lemma CH's corner hurt quantifies one corner.  Try: Theorem PERIMETER -- with all four corners
   doubly met, the four wall chains together force side >= f(n) with f(n) >= ceil(sqrt n) for the n in the survey;
   or find the exact obstruction.  State everything n-general, tag [T]/[S]/[M]/[F]/[C].
3. Deliverables: docs/proofs/one_flush.md (the conjectures, the survey table with sources, the mechanism analysis,
   the exact remaining obligation and what it would close at n = 11 and in general), Statements/Open/OneFlush.lean
   (the conjecture as a documented axiom, n-general form if the packing predicate allows, else n = 11), pages (the
   survey packings with their corner status where coordinates are available), registry row, LOG entry, ledger s.4
   note.  Report once (<= 20 lines) and EXIT.
