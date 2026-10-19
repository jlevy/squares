# A275 -- THE k0 KNOWLEDGE DOCUMENT: everything the lab KNOWS about k0 as a class -- true, false, certified,
# measured, conjectured, and the dead routes -- in ONE document, for the PI's overview and as the onboarding text
# for every future theory agent.  (PI, 2026-09-23.)
Opus (a compilation with exact citations; no new mathematics; where two sources disagree, record both with dates
and say which is later / corrected).  LAUNCH-AND-EXIT.  Ops: short responses, no interim messages, write the
document in numbered pieces of <= 120 lines per Write call (docs/proofs/k0_knowledge.md, appended piece by piece,
committed after each piece with explicit pathspecs, fetch + plain merge only), never a single response over ~15k
tokens, PYTHONDONTWRITEBYTECODE=1, no heavy python (sub-minute helpers for grep/tables only).  RUNNING, never
touch: the status loop, A262/A263/A273 chains, A269/A270 loops, A274b.
Sources (read ALL, in this order; the later ones correct the earlier): docs/proofs/k0_route.md (s.13 = the current
13-link chain -- your spine), the proof docs of A218-A274 in docs/proofs/ (k0_count, wall_torque, ring_swap,
two_grains, one_flush, lemma_eps, realign, swap_leaf, local_lock, handedness, no_vv, ring_capacity, pocket_waste,
wedged_seal, cross, construct_towards, perimeter_walk, snap_down, corner_chase, type_t_chase, family250 (in
attempts/A250), ring_pocket, centre_disc, mintilt253 (attempts/A253/notes), peel, common_sense, normal_ring +
family258 (attempts/A258/notes), normal_room, locked_wall, box_meeters, no_jam, open_pairs, three_lemmas,
strip_plug, last_two, strip_enclosure, ring_domain, strip_jam, disc273 (attempts/A273/notes)), the older k0 route
docs (k0_route.md s.1-12, k0_blocked_side.md, drain_flow_k0.md, grain_flood.md, descent_grains.md, forced_corners.md,
sideband.md, corner_seal.md, slot_crowds.md s.0/s.5 for the slab structure), attempts/REGISTRY.md rows A99, A185,
A188, A189, A190, A203-A211 (the k0 tree lanes and their prices), LOG.md entries for the k0 items, the ledger's
k0_00 row, lean/AUDIT.md (which statements are theorems, which axioms), the memory of the coordinator is NOT
available to you -- everything must come from the repo.

## The document: docs/proofs/k0_knowledge.md
0. How to read it (tags [T] proved / [T-computed] certificate + verifier / [M] measured / [C] conjecture / [F] false
   with witness / [D] dead route; every entry cites file + section + Lean name where one exists + the attempt).
1. DEFINITIONS, fixed: k0; simple square; the 12 border cells and the 8m-20 general system; slots, ribbons, eps;
   family-stuck (CELLS / K0-FREE / swap_packing / teleport_of_swap); meeter / toucher / floater / poker / holder;
   sense; rows, normal cell, the potentials Phi1-Phi4 and P1-P4; corner types PAIR / THIRD / JAM / FLOAT2; the
   ring family (17 coords), the normal ring D, hybrid D^h; the JAM corner hypotheses H1-H5; the slabs G1-G4 and
   the window; the value form vs the uniqueness form.  One paragraph each, with the source.
2. THEOREMS about k0 (every [T] with its statement in one or two lines, n-general or n = 11, file, Lean name).
   Group: exchange / normalisation; counting; room; corner geometry; window exclusions; force/torque facts (A218/
   A219/A233-A240: which are theorems, which superseded).
3. CERTIFIED facts [T-computed]: what, over which domain / side range, which certificate files, which verifier,
   status (verified / running with counts as of the day you write).
4. MEASURED facts [M]: every numerical fact the chain leans on that is not yet proved (with the numbers, the
   corpus, and where the code is).
5. FALSE statements [F]: every claim that was made and refuted, with the witness file / page and WHY it failed
   (e.g. TOUCH-NORMAL as a corner lemma -> JAM; the local common-sense lemma without the slide clause; the DISC
   LEMMA; STRIP_2 as A265 stated it; my rowing rule; CENTRE-DISC's disc criteria; the count '> 3' guesses; the
   tilt-split guess; 'k5 closed at the window pad' -- that one is k5 but belongs in the pitfalls).  This section
   is as important as s.2: it is what stops agents repeating them.
6. CONJECTURES [C] still in the chain, exactly, and what would close each (theory route vs certificate route,
   priced where known).
7. DEAD ROUTES [D]: the k0 trees (A99, A185-A211 k0 lanes, A242 crowd root 1e15 CPU-h, A243 reach root, A251 box-
   valid PIERCE 5e14 CPU-h, strip266 5e3 CPU-h, the jam kernel 15-500 CPU-h) with the reason each died (product law,
   dimension, margin vs bin), so nobody re-prices them.
8. THE CURRENT CHAIN (k0_route.md s.13 copied and re-tagged as of today) and the one-paragraph plain-language
   summary of what k0 exclusion at n = 11 now rests on.
9. GENERAL n: which items are m-free, which are m = 4 only; the PEEL / onion facts; the PI's structural reading
   (ONLY-RING; retreat; the domino pinwheel as the limit; why a variational argument is needed for all n).
10. TOOLS AND CONVENTIONS for the next agent: the corpus files (A244 twelve244, A217, the ring witnesses, A262's
    JAM rings, A258's normal rings), the exact-check tools (geometry check, 12-cell family test, region search,
    PIERCE), the certificate pattern (box test + own verifier + bisect-on-disagreement + side/ADJ consistency),
    the SVG rules, the ops rules (one process, launch-and-exit, tiny-step writing), and the pitfalls list (an
    optimiser's sup is not evidence; census counts vs closed classes; soft containment; verifier bins).
Then: registry row, LOG entry, ledger s.4 note, a link from k0_route.md s.0.  Report once (<= 12 lines): the
document's size and section line counts, the number of [T]/[T-computed]/[M]/[F]/[C]/[D] entries, any
contradictions between sources you found and how you recorded them.  EXIT.
