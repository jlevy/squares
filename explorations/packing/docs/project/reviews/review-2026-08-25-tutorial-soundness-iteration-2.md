# Review: `TUTORIAL.md` Soundness, Iteration 2, on the Merged Record

**Date:** 2026-08-25

**Author:** Claude (agent), as a full soundness pass requested by the user

**Status:** Current — findings applied in place.
Unlike the [first iteration](review-2026-08-25-tutorial-pedagogy-and-accuracy.md), which
recorded findings and left the wording open, this pass edits
[`TUTORIAL.md`](../../../TUTORIAL.md) and the affected record files directly on the PR
33 branch. Each finding below names its defect entry and bead.

**Scope:** every checkable claim in the reworked tutorial — numbers, counts,
attributions, mechanisms, links, and vocabulary — checked against the primary artifacts
rather than against other prose; plus the record reconciliation the check forced.
[`SYNOPSIS.md`](../../../SYNOPSIS.md) stays authoritative for status.

**Basis:** the PR 33 branch after merging current `main` (sessions 012–014, the
research-ID reconciliation, the Rust toolchain pin, and frontier transparency).
The merge itself is part of the reviewed object: it surfaced the two branches’
conflicting dispositions of H-024, and resolving that honestly was a precondition for
checking the tutorial’s `n = 29` material at all.

## The Merge, and Two Dispositions It Forced

**H-024’s disposition changed hands twice, and the landed record now owns it**
(`think-16qn`, `think-0emo`). The tutorial branch had rewritten exp-012’s stored verdict
(`rejected` → `unresolved`) and H-024’s registered claim in place, applying the later
assurance vocabulary to a closed preregistered round.
This review’s first merge reverted that in-place re-adjudication, on the conduct rule
that *a defective artifact is corrected by dated annotation rather than rewriting* and
because the then-landed `main` said refuted.
The frontier-assurance contract
([#31](https://github.com/jlevy/thinking-scratchpad/pull/31)) then merged carrying the
demotion as a considered part of its design — its plan names the Kingbird evidence as
overstated — with exp-012 rewritten to cross-reference H-042 as the narrower numerical
successor. The second merge therefore adopts the landed disposition: H-024 unresolved
pending a formal witness, exp-012 unresolved, H-042 refuted on exp-037’s 160-digit
replay. The process concern — closed rounds edited in place rather than annotated — is
recorded here rather than as a defect entry, since the landed record has made the
rewrite its deliberate form.

**The concurrent schema fork was repaired forward twice, identically** (D-326,
`think-clin`). `main`’s exp-038 and exp-039 were authored to `Experiment/v1` after this
branch had shipped v2; this branch’s first merge migrated both (`assurance: verified`,
`method: exact-algebraic`), and #31’s own merge into `main` applied the same migration
independently. The merged record unions cleanly: 39 rounds, 933 agent-minutes, 43
hypothesis artifacts.

## What Holds

Most of the tutorial survives adversarial checking, including every place its numbers
could be traced to a primary artifact:

- The corner: one-sided slopes `0.1747`/`0.3839` at ratio `2.1973` and `0.1747`/`0.3841`
  at ratio `2.198` match the synopsis’s convergence table digit for digit, and the D-029
  story’s `+5.6440e-04` / `+4.4409e-16` pair matches its table.
- The LP: `8^C(11,2) ≈ 4.7 × 10⁴⁹` recomputes; the `1,056 = 16 × (11 + 55)` row count is
  the literal assert in `cases/trump11/independent_lp_cell.py`; the `1.28 ms` solve, the
  `4.4e-16` side agreement, and the loose-tolerance record-“beating” incident all match
  their sources, the last with the measured overlap (`9.876e-08`, pair 4–8) in
  `quench.py`’s own comment.
- The record facts: 14 of 55 pairs at exactly zero and 20 boundary corner coordinates
  (T-1); the bound gap `0.088229208023` recomputes from the exact endpoints; the
  2,001-point `[38°, 42°]` scan and the five-seeds-in-a-narrow-band claim match the
  synopsis; exp-011’s five seeds at `5.0` against Bidwell’s `4.67553009…` match the
  ledger and frontier; Bidwell’s three orientation classes (`0°`, `+39.80496°`,
  `−36.62379°`) confirm “three unknowns at `n = 17`”.
- The quench description (nested loops, cell fixed point read back, golden-section class
  bracketing, optional free-angle pass, typed unsettled stops) matches
  `sqpack/research/quench.py`.
- The §4 improvement figures are exp-007/exp-008’s medians exactly (`3.4274e-08`,
  `3.1875e-08`, `2.2204e-15`; `5.32e-03`, `4.51e-03`, `1.33e-15`).
- The cost table matches the infrastructure benchmark doc line by line (`57 ns`,
  `2,726 ns`, `215.5 µs`, `1.2 µs`, `13.49 ms`, `0.35 s`).
- The assurance and method tables match the `Witness/v1` schema enums and the semantics
  checker, including `beat_record` requiring `verified`.
- The mathematics read as stated: the Lindemann–Weierstrass transcendence of the angle
  beside its algebraic tangent, the primitive-element argument with its unbounded degree
  and non-pointwise caveats, and the Tarski–Seidenberg route to an algebraic optimal
  side.
- The strategy catalogues are really 20 entries in 4 families and 30 in 6; “terminal
  set” really is used by the synopsis without a definition; all 60 internal anchors and
  file links resolve, checked programmatically.

## Findings, All Applied

**Accuracy.**

- **SR-1** (`think-0emo`, superseded) — an interim synopsis H-024 row read “Verified
  record packings … exp-012 verifies six”, upgrading a 160-digit numerical count to the
  reserved formal term.
  The row was reworded during the first merge; #31’s landed registry row replaced it
  entirely, and no defect entry remains.
- **SR-2** (D-327, `think-mb6q`) — §5’s promotion example asserted a separation of
  `3.7e-12` that exists in no artifact (it entered with the original tutorial commit and
  survived two reviews).
  Reworded to the attested solver-floor scale.
- **SR-3** (D-328, `think-suzm`) — §8 called the `1e-11` floor “HiGHS’s own feasibility
  tolerance, pinned at the strictest value it accepts”.
  The pinned tolerance is `1e-10`; `1e-11` is the post-checked side residual it
  produces. Restated with both numbers.
- **SR-4** (D-329, `think-6z2v`) — §5 labelled `177×`/`578×` “the exact-to-float ratio”;
  the source measures compiled-over-pure-Python for the same exact multiplication.
  Reworded, and the compiled-backend table row now says *benchmarked; not integrated*,
  agreeing with §11.
- **SR-5** (D-330, `think-bqjd`) — §11 claimed every cited source is archived locally;
  no Trump 1979 or Bidwell 1998 document exists (the archive README records the failed
  Trump retrieval). The claim now names the two exceptions.
- **SR-6** (D-331, `think-ojgc`) — the synopsis registry’s Rounds column was
  hand-maintained under no reproducible rule (H-023 lagged exp-039; H-002 showed 4
  against the ledger’s 5; H-021 showed 0 against 14). Rows aligned to the ledger’s
  totals, the rule stated inline, `check_synopsis` extended to compare the column, and a
  negative control added.
- **SR-7** (D-332, `think-aihj`, recurrence of D-028) — the synopsis restated the
  no-regression-fix count by hand (“ninety-eight” against the generated 106) two
  sentences after promising the neighbouring claims cannot drift.
  The copied number is gone; #31’s landed narrative removes the aggregate restatement
  the same way.
- **SR-8** (`think-d2ah`, superseded) — the assurance-vocabulary migration had
  hand-edited the golden basin-map note out of byte agreement with its writer, which
  failed the macOS deep gate on a wrap-only diff.
  This review round-tripped the golden through the writer’s dump call; #31 then landed
  its own registration of the same phenomenon (D-320) with a semantic golden comparison
  that closes the wrap class outright, so no separate entry remains and `think-57x3`’s
  durability proposal is resolved by that landed fix.

**Precision, no defect entry.**

- §4’s improvement figures now say they are medians over the five tested seeds, with the
  worst `n = 5` seed (`6.2e-08`) named — exp-007’s range makes the unqualified form
  overstate.
- §2 now says “six, numerically, at `n = 29`” where the class count rode without its
  assurance.
- Two sourced figures disagree across documents without either being wrong in context:
  the synopsis’s `129 ms` exact verification against the benchmark doc’s `0.35 s`
  unoptimised-Python figure the tutorial cites.
  Left standing; a benchmark refresh should reconcile them.

## Tracking

Epic `think-2xex` owns this iteration.
Merge-phase findings: `think-16qn`, `think-clin`, `think-0emo`. Tutorial-pass findings:
`think-mb6q`, `think-suzm`, `think-6z2v`, `think-bqjd`, `think-ojgc`, `think-aihj`.
Post-push CI finding: `think-d2ah`; durability follow-up `think-57x3`, resolved by #31’s
semantic golden comparison.
After #31 landed with its own D-320 through D-325, this review’s surviving entries were
renumbered to D-326 through D-332; the three superseded ones (the H-024 restoration, the
H-024 row rewording, and the golden serialization) carry no entries.
Defects D-326 through D-332 are registered with these beads and are all fixed on this
branch.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
