# Review 2026-09-04 — PR #80, the Stacked Hardening of the s(11) ≥ 381/100 Claim

A review of [PR #80](https://github.com/jlevy/squares/pull/80),
`codex/pr78-s11-adversarial-review`, head `28990b00`, as a stack on
[PR #78](https://github.com/jlevy/squares/pull/78)’s branch at its merge-base
`719c2a17`. Written by the author of the reviewed parent, at the operator’s request, as
the second reader the stack has not yet had.
The question asked was not “is the review right” but “which of its changes are clean
improvements, which are excessive, and which should be objected to” — and, because the
stack was reconciled to a parent that has since moved by twelve commits, what on it is
now out of date. The stack has since moved to `04127189`, four merge commits on and
reconciled to the parent’s `a159eb28`; where that head already answers a finding below,
the finding says so.

Two review lanes ran beside this document under their own briefs — one over the code and
tests, one over the records and prose — and their findings are folded in below with
attribution. Every figure here was read from the diff or the artifact, not from PR #80’s
description.

## Correction Added 2026-09-06

Two implementation details in the dated review body are now historical.
`t-018-proof.md` was retired; the maintained reader paths are the
[`t-018-proof-card.md`](../../../packing/cases/n11_fractional_certificate/t-018-proof-card.md)
and the
[`t-018-verifiable-claim-381-100.md`](../../../packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md).
The body’s 346-line count for `minimal_verify.py` describes the reviewed revision; after
subsequent certificate hardening, the maintained checker is 329 physical lines.
The body’s later shorthand references to “the proof note” likewise mean the retired
`t-018-proof.md`, not either maintained reader document.
The dated body remains otherwise unchanged as evidence of what the review assessed.

## Verdict

**Merge the substance, not the stack.** PR #80 finds one real gap in the parent’s
reusable verifier and a handful of real record errors, and it fixes them well.
It also carries a Lean project no gate builds, a second standalone verifier beside the
one already shipped, a 731-line hostile-input matrix for an internal command,
thirty-three new defects of which several are duplicates of what the parent found and
fixed on its own, and severity labels that call three parent-fixed or
non-verdict-bearing items “Blocker”.
Its suite budgets are justified by measurements the parent has since made obsolete, and
its defect numbering collides with the parent’s on nine ids, D-441 through D-449.

The path taken on this review: PR #78 merges first, and the valid improvements are
ported one bead at a time onto a branch off `main` (**Disposition**). If #80 were to
merge as a stack instead, the **Must update** list is what would have to change first.

| Question | Answer |
| --- | --- |
| Does anything in #80 change a retained bound or verdict? | No. All four retained certificates decide identically; #80 says so and the lanes confirmed it. |
| Is the nonnegativity finding (F1) real? | Yes, and it is the most valuable thing on the stack. The parent’s `verify()` never required `weight ≥ 0`; the counting step needs it. No retained certificate is affected — every weight is an LP output with `w ≥ 0` — but the verifier as a tool accepted a false theorem. |
| Are the six “Blocker” labels earned? | Four are (F1, F6, F7, F24) — F1 and F6 were reproduced live on the parent’s current head by the records lane. F9 is the parent’s own D-435, found and fixed there before #80 merged it. F17 concerns a path no evidence ever cited and is hardening, not soundness. |
| Is the T-018 promotion from C4 to C5 legitimate? | Yes. `epistemics.md` defines C5 as *review-ready* — C3 or C4 plus an existing `review_artifact` mapped as a non-superseded review — not as external review. The parent’s own prose (“C5 needs a review by someone outside the project”) misstates the rubric and is the parent’s to fix. |
| Is the stack current with #78? | At `28990b00`, no: it predates T-020, the integer sweep, D-442–D-444, the case-body rewrites, the attainment ratio, agenda-020, session-085 and the closeout. `04127189` has merged `a159eb28` and applies the witness fix on both sweep routes; the budgets, the rung-figure literals, the Lean project and the defect numbering stand. See **Must update**. |

## What PR #80 gets right

These are accepted as stated, and the parent should carry them whether or not the stack
merges.

1. **F1 — nonnegative weights are a condition, not an assumption.** The proof in
   `certificate.py` bounds the mass of disjoint inner squares by the total mass; that
   inequality needs every weight nonnegative, and neither `Atom` nor `verify()` checked
   it. The five-atom counterexample (n = 1, L = 11/10, B = 3/5, weight +2 at the centre
   and −1 at each corner, total −2 < 1) satisfies every stated condition and “proves”
   `s(1) ≥ 11/10`. This is a real gap in the reusable implementation.
   The fix — make nonnegativity a checked condition in the project verifier, the
   interval route, the standalone package and the Lean kernel, and retain the
   counterexample as a must-refuse fixture — is exactly right.
   Adopt.
2. **F7 — the interval route’s int64 masses could wrap** before Condition 2 rejected an
   oversized total. Scaling and summing in Python integers first, and refusing at `2^62`,
   is the same discipline the parent’s later integer sweep applies at `2^60`. Adopt.
3. **F6 — a restricted direction sample could report acceptance.** Reproduced on the
   parent’s current head: `verify_by_intervals(certificate, directions=("0",))` returns
   `accepted=True` after searching 1 of 361 directions, while the function’s own
   docstring says a sub-net is for controls, not claims.
   Nothing cited such a run as evidence, so no result is affected; but a public function
   that says “accepted” about a sample is a soundness hole in the API. An all-certified
   sample must be `undecided`. Adopt.
4. **F24 — RETAINABLE named a path, not bytes.** The gate read the file once and decided
   the object; the retention step then copied the path.
   A rewrite between the two would retain bytes nobody decided — the same class as
   D-433. Freezing the bytes, re-checking them after each route and printing the SHA-256
   in the verdict closes it cheaply.
   Adopt, and have `retain.py` verify the printed hash before it copies.
5. **F14 — the ceiling was overstated into a method-wide impossibility.** The parent
   proved that no certificate for n exists above `⌈√n⌉·B` and then wrote that the method
   “will ever settle” n = 12. That is too strong: a family of certificates with sides
   tending to 4 would establish `s(12) ≥ 4` without any member reaching it.
   The ceiling rules out one finite certificate at the grid bound; whether a limiting
   family exists is a question about the covering value.
   The parent’s wording in `SYNOPSIS.md`, `results.yaml` (T-017) and `README.md` needs
   the correction. Adopt.
6. **F26 — the reach table called run reports “measured optima”.** Of the restricted
   optima it lists, only one is recomputable from a tracked artifact and that one is a
   feasible mass, not an optimum; the rest are figures from run logs that were not
   retained. Placing the evidence status beside every value is the right fix.
   Adopt — and note the parent has since added a sixth report at 4.80 from a checkpoint
   that is likewise not in the repository.
7. **F33 — two comparison factors in T-017’s prose are wrong.** “Twenty-eight times
   tighter than every retained rung” compares against the wrong rung (the previous
   smallest margin is 0.007175, a factor of 6.9); “three times any other retained
   certificate” is 1.77 against the next largest.
   Both are the class D-439 names and both are the parent’s to fix.
   Adopt.
8. **F3 and F4 — the package’s name and its declared minimum.** “Third-Party Check”
   overstates what a self-contained package written by the claiming project on the day
   of the result can be; and the n = 11 replay checked the declared total mass but not
   the declared least cell mass, while the standalone verifier printed a mismatch as a
   note and still ended in VERIFIED. Both are small and correct.
   Adopt.
9. **The `n = 11` case body and T-017’s evidence list.** The records lane found that the
   parent’s own `n-011.md` still describes the `19/5` rung — “pinned to
   `[3.8, 3.877084]`”, 425 atoms, total `43391/4000` — under front matter that says
   `381/100`, and that `check_case_prose` passes it because the body never writes the
   `s(11) ≥ …` shape the detector matches.
   That is a live instance of D-442 on the parent and a detector gap, both the parent’s
   to fix; #80’s rewrite of the body is correct and was arithmetically verified.
   Separately, T-017 cited `E-n012-independent-verifier` as support for the `99/25`
   bytes although that verifier decided only the `77/20` file; #80 repoints the entry
   and drops it from T-017, which keeps C4 on the exact and interval pair.
   Adopt both, and the `[Burns n17]` → `[Burns–Massaccesi n17]` source-key fix with
   them.
10. **The literature audit and the scoped novelty language.** The audit under
    `packing/resources/web/s11-lower-bound-literature-audit-2026/` records eight
    repeatable queries including the reciprocal and density forms, separates the sources
    that decide the record from those that decide the method attribution, names its gaps
    (MathSciNet, zbMATH, theses, unindexed work), and refuses to turn a negative search
    into priority. The `novelty` labels do not move; the prose across README, SYNOPSIS,
    TUTORIAL and `n-011.md` is scoped to “the first *located public* improvement”.
    This is the best single document on the stack.
    Adopt, with the `novelty_basis.gaps` field and the proof-strategy lineage
    corrections.
11. **The proof note and its figure.** `t-018-proof.md` states its own limits, and the
    SVG is generated from the frozen certificate by a renderer that recomputes its
    witness and is drift-checked in the deterministic-rendering step; the records lane
    reproduced the bytes.
    Adopt — registering the note as `retained` rather than `definitive`, since it proves
    frozen bytes and owns no rule.

## What is excessive

Each of these adds weight the result does not need, or adds it in the wrong place.

- **The Lean spike, retained as a lake project inside the case package.** `Kernel.lean`
  proves the finite nonnegative counting inequality and the Condition 2 to Condition 4
  scalar arithmetic; by its own README it does not prove Condition 5, does not touch the
  1,121 atoms, and does not prove the theorem.
  No validation step builds it, no test would notice if it stopped compiling, and
  reproducing it needs a ten-gigabyte toolchain.
  As a dated research note it is useful and `docs/project/research/` already carries
  one; as a pinned toolchain, manifest and source tree under
  `packing/cases/n11_fractional_certificate/` it is unmaintained code presented beside
  the artifacts that decide the theorem.
  Move the source to the research note or a clearly labelled unvalidated spike
  directory; do not ship it in the case package.
- **A second standalone verifier, partly.** `minimal_verify.py` (346 lines) sits beside
  `thirdparty/verify.py`. The code lane found them less redundant than they look: the
  package verifier is general-purpose, runs on CPython 3.8, and ships against the `19/5`
  rung; the new one is pinned by SHA-256 to the retained `381/100` bytes, checks every
  declared field, and cross-checks the prefix-sum minimum against a direct summation at
  each direction’s witness.
  That is a legitimate second decision.
  What is excess is the eighty percent of algorithm they share, and that the file is the
  seventh copy of one SHA-256 on the stack, of which two are recomputed.
  Keep it; pin the hash in one place.
- **The retention gate’s loader, less than it looks.** `decide_certificate.py` grows by
  313 lines and its tests by 731. The code lane calls the result the strongest part of
  the stack — `claim` and `least_cell_mass` required and compared against *both* routes,
  Conditions 1–4 refused before the sweep, a bounded read, the SHA-256 of the re-read
  bytes printed on acceptance — and measured the tests at 52 in 186 s, of which 173 s is
  one correctly marked exhaustive node; the fast tier pays about 13 s, 12.4 s of it in
  one unmarked test that runs the real interval route beside its exhaustive twin.
  All four retained records already satisfy every new requirement.
  So: port it, mark that one test, and leave `REFUSED` on stdout unless the stderr split
  is wanted.
- **Thirty-three new defects.** entry 456 of #80’s log through entry 463 of #80’s log
  are eight entries about one command’s robustness; several others record a finding the
  parent had already fixed independently before the stack merged it (see **Must
  update**). A log that grows by a quarter in one review, with entries this fine, is
  harder to read than the record it is meant to protect.
  Merge the per-command robustness entries into one, and drop the duplicates.
- **The suite budgets.** The fast suite’s cap moves from 1,800 s to 2,700 s and the
  exhaustive tier’s from 900 s to 14,400 s (21,600 s at `04127189`, under a comment that
  still argues for 14,400), each justified by a measurement — 1,789 s for the ordinary
  suite, 4,866 s for one exact decision.
  Both measurements are of the Fraction sweep the parent replaced the same evening: the
  ordinary suite now runs in 1,031 s on four cores and the n = 20 exact decision in 29
  s. The 900 s cap on the pre-push whole-suite step is a real problem the parent
  recorded as a blocker, and raising it is right; the numbers should be re-measured on
  the current head rather than carried from the old one.

## What is objected to

- **Severity labels that do not match the evidence.** F9 is labelled “Blocker in the
  interval checkpoint, fixed here”; it is D-435, found and fixed on the parent in
  `5673ecac` at 10:14 UTC, an hour before the stack’s first commit, and the stack’s own
  text says “D-435 records the defect”.
  F6 (a restricted direction sample could report acceptance) and F17 (the gate did not
  compare the `claim` string) are labelled Blocker while the review concedes neither
  affected any cited evidence.
  A review that reports its findings by severity has to hold the labels to the same
  standard it holds the parent’s figures.
  Re-grade these three, and attribute parent fixes to the parent.
- **“The reviewed parent should not merge without the soundness repairs carried by this
  stacked branch.”** As a statement about the verifier as a reusable tool, F1 supports
  it. As a statement about the parent’s results it does not: every retained certificate
  has strictly positive weights, and the stack says so in its own verdict table.
  The sentence should say which of the two it means.
- **Three exhaustive decisions of one file.** The PR description’s “replaced in the
  permanent gate by the complete 87-second standalone verifier” reads as though the
  project verifier left the gate.
  It did not: `test_the_n11_certificate_is_accepted` stays, and the stack *adds* two
  exhaustive nodes in `test_n11_thirdparty_verify.py` that decide the same bytes again
  through `thirdparty/verify.py` and `minimal_verify.py`. The project decision is what
  the evidence cites and it now takes about thirty seconds; a second standalone decision
  is a useful control; a third is the redundancy noted above, in the tier that is priced
  by its widest step.
- **Edits to dated review records.** The stack touches six `review-2026-09-03-*` and
  `review-2026-09-04-*` files.
  Four of the diffs are typographic — backticks around formulas, curly quotes, an
  ellipsis — the formatter’s work rather than the author’s, and harmless.
  One is not: the third-party-package review has its references repointed from
  `../certificate.json` to `../certificate-19-5.json`, because the file the review
  examined is no longer at the path it named.
  The repointing is correct and the reason is real, but a dated review is an immutable
  determination; the fix belongs in a dated note beside it that says the top rung moved
  and what the path now means, not in the record’s own sentences.
  The records lane found the five typographic edits fall *inside block quotes of
  external sources* — Connelly–Whiteley, Donev et al., the Kingbird page, MathWorld —
  which this repository never retypes for tidiness; and that the sixth file also has an
  *observation* rewritten: the `check.py` row goes from “all three steps passed; real
  33.0 s”, which is what the reviewer ran, to “all four steps passed”, the fourth step
  being one #80 added.
  Revert the five; keep the path fix; restore the observed row and put the fourth step
  in an addendum.
- **D-439 is regressed by the merge reconciliation.** `defects.yaml` on the stack
  rewrites D-439’s `regression` to “None automated, and that is the honest state” and
  its `what` to “the detector this argues for, and which does not exist” — while the
  same stack ships `check_rung_figures.py` and `test_rung_figures.py` and records entry
  466 of #80’s log as a gap *in that detector*. The record now denies a detector it
  blames two entries later.
  Restore the parent’s D-439 text.
- **entry 469 of #80’s log duplicates the outstanding D-432**, whose `fix` field already
  prescribes the budget on the push whole-suite step that #80 implements; the stack
  ships the fix, leaves D-432 open, and records it again.
  Close D-432 and drop entry 469 of #80’s log, or make entry 469 of #80’s log its
  recurrence rather than D-438’s.
- **The stack renumbers the parent’s defect.** The parent’s D-441 (the generator decided
  a candidate before writing it) becomes entry 454 of #80’s log on the stack so that
  D-441 can name the signed-weight finding.
  The parent is the base; its ids stand.
  Since `719c2a17` the parent has also recorded D-442, D-443 and D-444, so the stack’s
  block D-442–entry 474 of #80’s log has to move up by at least four, and every count
  `check_synopsis` enforces (total, per class, flattering, gate-caught, unprotected)
  moves with it.
- **TUTORIAL adds five mathematical terms it does not own.** Atom/weight, atomic
  measure/mass, weighted fractional unavoidable-set certificate, direction net and event
  cell are added to `TUTORIAL.md`’s glossary and to none of `SYNOPSIS.md`’s terminology,
  against `conventions.md` §5; “event cell” is a third sense of “cell” where the
  conventions fix two; and the tutorial’s own sentences “two rows below are local” and
  “three words carry controlled multiple senses” are now false.
  The `μ` → `f` rename of the minimal polynomial is self-consistent but unannounced.
  Put the terms in the synopsis, or mark them local, and amend the cell rule.
- **A status change reworded away.** `pyproject.toml`’s comment excluding the
  third-party package and the independent verifier from the type floor said they were
  “retained verbatim as third-party evidence — editing either to satisfy a checker would
  void what they are”.
  The stack rewrites that to “source-distinct evidence with deliberately separate
  compatibility contracts”, in the same diff that edits those files by some four hundred
  lines. Editing them may be right; the change of status should be stated as one, not
  reworded.
- **A public default flipped with one test.** `generate_adaptive(decide=)` moves from
  `True` to `False` to enforce freeze-then-decide.
  The direction is right — it is this branch’s own rule — but a default on a public
  generator function is a behaviour change and one test guards it.
- **One stale figure the stack introduces.** The Lean research note says “the
  90.5-million-cell C4 decision remains the expensive layer” and “do not begin by
  replaying 90.5 million raw cells” — the `19/5` rung’s cell count — while the same file
  correctly gives the current certificate’s 567,130,649. The class the parent recorded
  four times today, once more.

## Must update: where the stack is behind the parent

PR #80 at `28990b00` was reconciled to `719c2a17`, with the parent at `a159eb28`, twelve
commits on. Its `04127189` head has since merged `a159eb28`; the rows below say which of
these that merge settled and which stand.

| Parent change since `719c2a17` | What it means for #80 |
| --- | --- |
| **T-020**: `s(19), s(20), s(21) ≥ 24/5`, a fourth certificate package, `n = 19`–`21` case files rewritten, Nagamochi’s closed form now holds 58 of 65 open cases, not 60 | Every count, case body and evidence entry the stack touches for n = 17–19 has moved again; `n-019.md` in particular now carries T-020, not T-019. The frontier-corpus tripwire is 58. |
| **Defects D-441–D-449** recorded on the parent | At `04127189` the stack numbers its own entries 441 through 489 of its log and moves the parent’s D-442, D-443 and D-444 to entries 475, 481 and 482 of its log. Nine ids collide with different content. The parent’s ids stand; the stack’s entries renumber from entry 450 and the parent’s return to their ids. |
| **D-442** (five case bodies stale against their front matter) and `devtools.check_case_prose` | The stack’s F28 / entry 467 of #80’s log is the same finding and its entry 466 of #80’s log the same possessive-mass instance; the parent’s rewrites of `n-017`–`n-019` are the ones to keep (the stack’s drop the green17 / T-001 passage and the Massaccesi provenance the parent preserves). Record concurrent discovery once and keep the parent’s detector, which reads every case body against its own front matter. |
| **`frontier/README.md` says 58 of 65** open cases rest on Nagamochi | The stack still says 60; its corpus tripwire and case bodies move with it. |
| **D-441’s consequence field corrected** on the parent | The stack’s F20 / entry 460 of #80’s log fixes the same sentence. Duplicate. |
| **The integer sweep (agenda-020, `d8733ad0`)**: `sweep.py` rewritten around an int64 grid and spans, `verify()` parallel, exact decisions 68–183× faster | Settled at `04127189`, and well: `verify()` stays parallel, `_cell_witness` is applied on both the integer and the Fraction routes, `minimum_covered_mass_integer` checks its own preconditions, and `reduce_to_cells` is re-implemented independently of `reduce_to_spans`, so the reference no longer shares the optimised route’s geometry. (At `28990b00` a plain merge left the witness fix in the Fraction path only.) What stands: the 2,700 s and 21,600 s budgets (F13, F30, F32; entries 451, 470 and 471 of #80’s log) were sized for a cost that is now 25–29 s, and the exhaustive constant’s comment still argues for 14,400. |
| **agenda-019 cost figures corrected** (a third paired point; contention noted; 13,000 s figure retracted) | F33’s complaint about the two-point exponents is partly addressed; what remains is the two comparison factors above. |
| **The reach table gained the attainment ratio and a predicted-gain ranking** | F26’s evidence-status column has to be re-applied on the new renderer. |
| **Agenda-017 closed (W10), agenda-020, session-085, the cold-start handoff** now select `BC-191`/`think-ji0r` | The stack’s agenda-019 edits (+65/−48) predate the handoff section and the BC-190 re-basing. |
| **The certificate conditions are being renamed** on both branches from the former letter-C condition labels to Condition 1–Condition 5 | Aligned at `04127189`: the stack’s `results.yaml` spells the obligations Condition 1–5 and keeps `C0`–`C5` for the confirmation rungs, as in the table below. |

The condition rename, so that the two branches align:

| Former certificate condition | New name | Meaning |
| --- | --- | --- |
| symmetry condition | Condition 1 | the atom multiset is closed under the container’s D4 symmetry |
| mass condition | Condition 2 | total mass strictly below n |
| direction-net condition | Condition 3 | the direction net reaches π/4 |
| containment condition | Condition 4 | containment, `B(1 + D) < 1` |
| coverage condition | Condition 5 | every closed B-square at every net direction covers mass ≥ 1 |

`C0`–`C5` then mean only the confirmation rungs of `epistemics.md`. F1’s new
nonnegativity requirement is best written as part of Condition 2’s statement (the
weights are nonnegative and their total is below n) rather than as a sixth numbered
condition, so that the count of conditions the tutorial, the proof note and the
standalone package name stays at five.

## Lane findings

*(Filled in from the two review lanes.)*

### Code and tests

Reviewed read-only against the stack’s head, with the stack’s `interval.py` run on all
four retained certificates (all accepted; every enclosure equal to the declared least
covered mass; none stalled) and the five-atom counterexample run against the parent’s
verifier at `719c2a17` (accepted, total mass −2, `bounded_side` 11/10 — the exact
reproduction). Per file:

- `model.py`, `certificate.py`: the nonnegativity helper is one exact check shared by
  every entry point, and `closed_form_conditions` lets the gate refuse Conditions 1–4
  before paying for the sweep; `float(product):.9f` in the containment detail becomes
  the exact product. `certificate.py` conflicts textually with this branch’s parallel
  `verify()` (d8733ad0) and needs a hand merge.
  Ported in substance already.
- `sweep.py` — **F11 is real and larger than the stack says.** On this branch’s head,
  158 of 181 directions at n = 11 and 159 of 181 at n = 17 report a witness centre
  outside the admissible domain: the midpoint of an event cell that the domain polygon
  only partly covers. The verdict is unaffected (the value is right; the point is not a
  witness). The stack’s `_cell_witness` fixes it.
  At `28990b00`, merged onto this branch, `sweep.py` auto-merged silently with the fix
  landing only in the Fraction reference path while the integer path that actually runs
  kept the midpoint; `04127189` has done that merge by hand, applies the helper on both
  routes, and re-implements `reduce_to_cells` independently of the spans, which is the
  better reference. The port takes that code as it stands, keeps the value-and-witness
  equality test, and exhausts all 181 directions of all four certificates on the integer
  route, which is now cheap, because the strict-inside check is a new hard-error path
  the lane could sample only.
  Recorded on this branch as D-449, outstanding, with the port as its fix.
- `interval.py`: the overflow hardening is clean and the four verdicts are unchanged;
  `directions=` no longer yields a verdict, which this branch has adopted.
  The new `BOX_BUDGET` of 100,000 boxes per direction fails safe but has 3.2× headroom
  at the n = 17 top rung (31,103 boxes measured) and its comment already names the wrong
  largest certificate (2,097; it is 2,260). Raise it or derive it from the net.
- `colgen.py`: the `decide=` default flip, above.
- `decide_certificate.py` and its tests: port, as above.
- `thirdparty/verify.py`: preconditions including nonnegativity, typed load errors,
  singleton and empty domains handled — and one policy change: a `B`-square that does
  not fit the container (`2h ≥ L`) no longer raises, so an all-vacuous Condition 5
  *accepts*. That is sound (a unit square containing such a `B`-square does not fit
  either) but it is acceptance on vacuity in a checker whose value was refusing what it
  cannot handle; port with the soundness note written down.
  At `28990b00`, `decide()` folded declaration mismatches into `failures` under a
  comment saying it keeps them separate; `04127189` keeps them in their own list.
  `falsify.py`’s oracles are hard-coded to the `19/5` file while its usage line
  advertises any certificate; a non-shipped path should be refused explicitly.
- `cli/validate.py`: the 1,800 → 2,700 s fast-tier budget rests on a 1,791 s measurement
  that d8733ad0 invalidated (the lane measured the n = 12 and n = 20 exact decisions at
  25.5 s and 28.4 s against the 4,866 s the exhaustive budget cites), and 2,700 s sits
  *above* CI’s 1,800 s, so the local gate could pass while CI times out.
  At `04127189` the exhaustive constant is 21,600 s while its comment still argues for
  14,400. Drop both numbers; port only the push-step `budget_seconds` line, at 1,800,
  which is the fix D-432 already prescribes.
- `test_rung_figures.py` (+193): the cross-record contract is right; the literals are
  not — six reach-table rows, “about 6.9 times tighter”, “about 1.77 times”, “2097 atoms
  took 4866 s”, “Eight rungs are retained”, three `exact_form == "459/100"` — every one
  hand-written in a test that already opens the artifact it could derive them from.
  As written, four new instances of D-439. Port the mechanism, derive the figures.
- `test_fractional_interval.py`: honest renames that strengthen; one assertion pins an
  implementation-defined box count (2,666,151).
- `minimal_verify.py`: above — keep, and stop being the seventh copy of the hash.
- Cost: about 13 s added to the fast tier and about 373 s to the exhaustive tier; the
  fast tier on the stack’s tree could not be timed meaningfully because that tree lacks
  the integer sweep.
- Not verified by the lane: the exact sweep under the stack’s own `sweep.py` on n = 12
  and n = 17 (hours at Fraction speed; the four verdicts were confirmed on this branch
  instead), and the devtools renderers, which the records lane covered.

### Records and prose

Reviewed under its own brief against a `git archive` of the stack’s head; no file was
modified. The lane ran the repository’s checkers on the stack’s tree — `check_results`,
`check_synopsis`, `check_rung_figures`, `check_nagamochi_bounds`, `check_documentation`,
`render_defects --check` — and all pass there; it then re-derived every quantitative
claim in the changed records (the condition slacks, the movement `+0.021146`, the
`5(381/100 − 2)² = 32761/2000 > 16` step, the margin and atom ratios, the two-point
exponents, `4/(1 + D) − 99/25 = 0.0308`) and found each correct.

Its conclusions, all folded into the sections above: F1 and F6 reproduce live on the
parent’s head; F9 is stale against the declared parent; F2 is measured at an earlier
head than the one the review names; the four structured changes to `results.yaml` are
justified and no `novelty` label moves; thirty-four defect entries (D-441–entry 474 of
#80’s log) with `count` and `defects.md` consistent on the stack’s tree; D-439
regressed, entry 469 of #80’s log duplicating D-432, entry 454 of #80’s log a renumber
of the parent’s D-441; the dated-review edits as described; the tutorial vocabulary
problem; the `90.5 million` figure; the Lean project listed among T-018’s artifacts with
nothing that would notice it failing to build; the SVG byte-reproducible from the
committed renderer and certificate; and the literature audit honest and well-scoped.
It also found the parent’s own `n-011.md` body stale and undetected, which the parent
takes as its own defect.

## Disposition

The operator’s decision, taken on this review: merge PR #78 at the next opportunity,
then port the valid improvements one at a time onto a branch off `main`, each as its own
commit. The ports are tracked as beads under the epic `think-pev1`, whose prerequisite
`think-xcuv` is the branch and a re-measurement of the suite budgets on `main`; the
first slice — the nonnegativity precondition, the sample verdict, the ceiling and factor
corrections, the `n = 11` body and its detector, the C5 wording — landed on #78 itself
as `580efe58` because two of them close soundness gaps in the verifier as a tool.

- **Landed on #78 as `580efe58`**: F1 with its counterexample fixture, F6, F14’s
  wording, F33’s two factors, the `n-011.md` body and the detector gap behind it, and
  the C5 wording, with D-445–D-448 recorded and D-449 opened for F11.
- **Port, one bead each under `think-pev1`**: F7 and F29 (`think-612b`), F17’s useful
  half and F24 with the hash verified at retention and the loader as measured
  (`think-e6xe`), F11 in a helper both routes call (`think-xyt1`), F10 (`think-nb9d`),
  F3 and F4 (`think-o2lo`), F26’s evidence column on the new renderer (`think-k581`),
  the T-017 evidence repointing (`think-rjaj`), the literature audit with its scoped
  novelty language (`think-rl03`), the proof note and its figure, registered in the
  document map (`think-rph2`), the C5 review artifact for T-018 (`think-pm1e`), the
  tutorial’s vocabulary against the synopsis (`think-fz5x`), F27 (`think-t1an`), F12
  (`think-4ax1`), `minimal_verify.py` with its hash pinned once (`think-4iej`), the
  `test_rung_figures` mechanism with its figures derived (`think-3v1e`), the third-party
  package’s policy changes with the vacuity note written down (`think-qpjx`), and the
  `decide=` default with a second guard (`think-nuhr`).
- **Drop or move**: the Lean lake project (to a research note, and out of T-018’s
  artifact list), the budget raises as measured (re-measure on `main`; `think-xcuv`),
  the typographic edits to five dated reviews and the rewritten observation in the
  sixth, the D-439 regression as written, entry 469 of #80’s log, and the renumbering of
  the parent’s D-441.
- **Fix on the stack**, whatever else happens to it: the `90.5 million` figure (the
  proof note’s document-map registration is done at `04127189`), the exhaustive budget’s
  14,400 comment against its 21,600 constant, and the `BOX_BUDGET` comment that names
  2,097 atoms as the largest retained certificate.
- **Re-grade**: F6, F9, F17.
- **Renumber and dedupe** the defects: the stack’s entries 441–489 of its log from entry
  450, against the parent’s D-441–D-449 and its later fixes.

The concrete claim — that the retained certificate proves `s(11) ≥ 381/100` — was never
in question on either branch, and #80’s independent decisions of the same bytes are
welcome confirmation of it.
What the stack adds to the *record* is worth about a tenth of its size.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
