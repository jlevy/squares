# Task 04 / C1092 — mathematical simplification and complete case assembly

**Status: DONE_MATH.** Task 03 / C1091 is untouched and remains assigned to the other agent. No Lean was written or compiled, no repository was modified, and no proof-assistant acceptance or global twelve-square optimality claim is made.

This delivery proves a new local all-angle obstruction, reconstructs the original finite entrance, and assembles the C1092 mathematical case using the included recovered continuous lemmas. The long recovered lemma library has not been freshly verified in a proof assistant. The exact checks reported here concern the finite entrance, coordinate transports and specified scalar identities/signs; they are not an automated verification of every sentence of that library.

## 1. Main new result: one actual three-square lemma replaces three terminals

The handoff's precise open MMMP target is

    for every actual original MMMP packing,
    not Q10.Inside(3,87/50).

The new proof is `proofs/TWO-FIFTHS-SLOPE-SQUEEZE.md`. In translated actual coordinates it retains the southeast square E, northeast square N and right wall square R. E and the actual wall force

    |tan(angle R)|<2/5,

while N and the same actual wall forbid the entire closed range

    |tan(angle R)|<=2/5.

Both canonical signs and every face-normal source are treated. The proof permits weak separating-support equality and closed center signs. It needs only a>1 locally, not the global normalized side cap. Its closest displayed rational slope-loss margin is 299/145000>0.

The key improvement is retaining E's coupled floor

    s A+c H>a(c+s)-1

through its actual support calculation. For the right-supplied separator, the necessary slope bound follows from

    2[.26+s(1-z)]-5z(c+s)>0,
    z=s/(1+c), 0<s/c<1/3.

The identity and derivative in the new proof certify that inequality continuously. This avoids first proving a loose right-angle bound and then running separate final contradiction chains.

The new lemma does not ask whether G8 is owned by E. The original two exhaustive G8 alternatives each have a short, different geometric entrance proving its common profile. We preserve both entrances, then use the one terminal for both. This replaces the separate negative-right, positive-right and G8-owned terminal arguments without importing an angle estimate from the wrong ownership branch.

`proofs/MMMP-ACTUAL-ENTRANCE.md` gives the full actual-owner ledger. In particular it independently retains the genuine top origin (2,3), actual bottom bar, actual right wall/center, and the same northeast square's strict point (2.47,2.12). Therefore the new local lemma proves the exact requested omission, rather than merely a theorem with unproved stronger premises. The strict far-right point (3,64/25) follows by the retained actual-wall reach theorem, and the stated MMMP upper-pair ending applies.

The same new local theorem also replaces the right-near terminals in the windmill's one-omission sector after its own correctly signed entrance. It does not identify the MMMP and MPPM families.

## 2. Original entrance: no hand-picked assignment

The literal family is

    {3,12,48,192,256,512,1024,2048,4096,8192,16384,32768}.

The case retains twelve actual congruent open squares of side 1<a<=1001/1000 in [0,4]², arbitrary orientations and disjoint interiors. The first four owners are paired corners, not the special singletons of C1089 or merged owner of C1090.

`proofs/ORIGINAL-ENTRANCE-AND-SYMMETRY.md` supplies a direct paired-corner inner-point proof, the covering-budget argument, exact original point conventions and the full sign transports. The retained foundational geometry proves the F/G non-avoidance statements. The finite checker regenerates

    824 component labels,
    55,126 complete pairwise-disjoint auxiliary assignment vectors.

Every ordered row matches the recovered original 55,126-row table. The eight small covering disjunctions used by the direct MMMP and MMMM arguments are checked as consequences of this complete entrance. This is a necessary-condition outer catalogue; the checks do not assert that its rows are realizable packings.

All eight square symmetries are checked as simultaneous marker, owner and auxiliary permutations. The four sign orbits have sizes 4,8,2,2 and cover all sixteen closed sign strings. The maps to the handoff's four canonical Boolean branches are explicit and checked. Equality at a split is retained, not discarded by a sign convention.

## 3. The four mathematical branch obligations

| Handoff branch | Mathematical result in this delivery |
|---|---|
| 0: windmill | Full original-entrance assembly through actual omission and central-sign reductions; new common terminal in the one-omission sector; all-positive final sector uses a four-wall strict cycle. |
| 1: one exceptional | New all-angle right near-point omission, independently retained top origin, strict far-right reach, and the complete actual upper-pair ending. |
| 2: adjacent pair | Reconstructed original entrance and complete MMMM continuous reduction, including all actual wall origins and the genuine northeast center before the same-face terminal. |
| 3: opposite pair | Existing mathematical branch preserved, with its retained local center theorem; no change to its formal source or contract. |

For the windmill's all-positive ordinary sector, either forward-point status yields the same strict actual wall-center inequality. The four inequalities are

    (X9-2)+(Y8-2)>0,
    (Y10-2)+(2-X9)>0,
    (2-X11)+(2-Y10)>0,
    (2-Y8)+(X11-2)>0.

Their sum is 0>0. The same central face is retained in the two local wall comparisons. Thus all sixteen forward-status patterns share one final cancellation; the four actual walls have not been deleted as in the invalid eight-square relaxation.

For MMMM, the two simultaneous inequalities retain the same northeast faces U,V. Their positive combination has a nonpositive left side and a right side greater than 4369/140000. The full entrance proving that square's strict center and required actual bars is retained, not just the small final calculation.

The detailed active joins are in `proofs/WINDMILL-AND-ADJACENT-ASSEMBLY.md`. The underlying full continuous chapters are included in `reference/recovered/`; no inaccessible repository import is used as a substitute for their mathematical text.

## 4. Verification and exact limits of the checks

Run from this C1092 directory:

    python checks/run_all.py
    python -O checks/run_all.py
    python checks/test_inputs.py

Only the symbolic identity checker needs SymPy. The finite geometry, catalogue, transforms, polygon covers and corruption-test driver use the Python standard library. The included receipts record the actual execution modes and results. Neither normal execution nor python -O relies on assert statements to enforce required checks.

The check suite regenerates all 824 component labels and 55,126 rows, verifies eight covering clauses, checks 384 marker/owner/auxiliary images under the eight simultaneous symmetries, verifies all sixteen wall-sign choices and the four canonical transports, and checks the exact four-wall cancellation. It also rechecks the retained thirteen closed-rectangle covers and six wall-polynomial intervals, plus 35 specified symbolic identities and 23 exact scalar signs. One scalar sign is intentionally nonnegative rather than positive; the written argument supplies strictness from a>1 at that endpoint.

The six deliberate input corruptions test a component, a complete row, a canonical branch map, the endpoint quartic, the proposed common slope threshold and the southeast cosine bound. They are run in normal and optimized modes. The final package audit checks the unaltered original task body and that no task-03 file or result is in this merge package.

**Not performed:** Lean compilation, source-ancestry replay, native/axiom audit, the row-576 adapter's formal verification, independent proof-assistant checking of the recovered continuous library, or integration into a global packing-constant theorem. The handoff's formal acceptance conditions remain formalization work; DONE_MATH is not a representation that those conditions were executed.

## 5. What to read and merge

Start with the new slope-squeeze proof, then its actual-entrance ledger. The windmill/adjacent assembly explains the other two open mathematical branches and the original-entrance chapter fixes all indexing and symmetry conventions. The reference manifest records exact source paths and SHA-256 hashes for the recovered text.

The archive is deliberately task-04-only. Its task is named `04_DONE_MATH_C1092.md`, with the original task body unchanged. `TASK04-STATUS.json` records this result independently of task 03. The safe merge script updates only task 04 in a copy of an existing handoff archive; it refuses to overwrite different task-04 work and preserves all task-03 entries byte for byte.
