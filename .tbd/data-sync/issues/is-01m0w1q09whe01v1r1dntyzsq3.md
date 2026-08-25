---
type: is
id: is-01m0w1q09whe01v1r1dntyzsq3
title: "W2: full factual check of the reworked TUTORIAL, and cross-document consistency"
kind: task
status: open
priority: 1
version: 2
spec_path: explorations/packing/docs/project/reviews/review-2026-08-25-tutorial-pedagogy-and-accuracy.md
labels: []
dependencies:
  - type: blocks
    target: is-01m0w1qqdsy78rbz6dsw6qfcz0
parent_id: is-01m0w1p1t7gaen5tzf1pt94f3x
created_at: 2026-08-25T08:48:41.788Z
updated_at: 2026-08-25T08:49:05.464Z
---
Correctness-only pass over `TUTORIAL.md` at its current head, then outward to the
documents it now disagrees with.

## Part 1 — every claim the rework introduced

The rework added material that has not been independently checked.
Each item below is a claim to verify against a primary source in this directory, not
against the review that proposed it.

**Newly added numbers.** The `f64` and exact-arithmetic cost table in §5 (57 ns,
2,726 ns, 215.5 µs, 1.2 µs, 13 ms, 0.35 s), the 177x and 578x ratios, the three latency
budgets, the `1.28 ms` LP solve, `2n + 1 = 23` variables, `1,056 = 16 x (11 + 55)` rows,
and `8^C(n,2)` with `4.7e49` at `n = 11`. All were lifted from
`research-2026-08-22-infrastructure-for-packing-exploration.md` and `SYNOPSIS.md` rather
than re-measured. Confirm each is still what its source says, and that the source is
still current — several predate the assurance migration.

**Newly added mathematics.** Four claims that carry real weight and were written by the
same pass that proposed them:

- The primitive element theorem argument in §5: one `alpha` always suffices, and the
  degree is unbounded. Standard, but check the statement as written.
- That the optimal side is algebraic because the feasible set is semialgebraic and the
  set of achievable sides is a projection of it. **This is the one flagged `Unverified`
  in the review** (TR-12). It is this review's argument, not the directory's. Either
  establish it against a source, or weaken the sentence to what the algorithms report
  already supports.
- That the infimum is attained, attributed to Martin 2000 in §1. Confirm the archived
  paper actually covers this case.
- The weak-separation statement in §2: interior-disjointness iff a weakly separating
  line exists, and that edge-parallel candidates suffice.

**Newly added mechanism descriptions.** The §3 quench account (two nested loops, the
cell read off the incoming pose, the cell fixed point, golden-section bracketing over
merged classes, the free pass) was written from `src/sqpack/research/quench.py`.
Re-read the module and confirm the description still matches, including that the outer
stopping conditions are stated correctly.
Same for the §2 claim that separation is one row per pair in the quench and sixteen in
the independent formulation.

**HiGHS.** Newly named in §2, §8, §11, with a feasibility-tolerance definition and a
vocabulary row. Confirm the characterization is right and that reaching it through SciPy
is still how the code calls it.

## Part 2 — cross-document consistency

The rework changed vocabulary and notation, and the neighbours have not moved with it.
Check at least:

- **`gap`.** The tutorial now splits **bound gap** from **search gap**.
  `SYNOPSIS.md` and `README.md` both define a single unqualified `gap` as
  `best_side - standing_best`. Decide whether the split should propagate, and if so
  where the unqualified word may still be used.
- **Symbols.** The tutorial now uses `k` for the perfect-square root, `mu` for the
  minimal polynomial, and reserves `alpha` for the primitive element.
  Check `SYNOPSIS.md` uses the same, and note where the research reports differ — the
  `n = 11` report uses `theta` for what the tutorial calls `a`, `u_i` for a per-square
  parameter, and `alpha` for two other things. Those are cross-document collisions the
  notation card records but does not resolve.
- **The vocabulary card.** It gained `proposer`, `refiner`, `rigidity`, `descriptor`,
  the polish/exploration failure pair, `terminal set`, and `feasibility tolerance`, and
  split `atlas` from `census`. `SYNOPSIS.md#terminology` is the declared authority;
  confirm every added row agrees with it, and that nothing in the card contradicts it.
- **The assurance vocabulary.** Confirm the tutorial's four witness method tokens plus
  the three frontier proof tokens match `witnesses/witness.schema.yaml` and the frontier
  evidence schema, and that `README.md`'s "Essential Terms" table, which still lists
  `evidence tier` with the retired `f64_screen`/`polished`/`exact` values, is updated.
- **Section numbering.** The tutorial now runs to §12; anything linking to its sections
  by number needs checking.

## Output

Claim-by-claim dispositions.
Bounded corrections applied where evidence and scope are unchanged; anything larger
recorded as a successor bead or a defect.
Do not re-open presentation decisions that the exposition pass already made and that are
not wrong.
