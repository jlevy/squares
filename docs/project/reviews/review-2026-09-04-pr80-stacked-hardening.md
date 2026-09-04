# Review 2026-09-04 — PR #80, the Stacked Hardening of the s(11) ≥ 381/100 Claim

A review of [PR #80](https://github.com/jlevy/squares/pull/80),
`codex/pr78-s11-adversarial-review`, head `28990b00`, as a stack on
[PR #78](https://github.com/jlevy/squares/pull/78)’s branch at its merge-base
`719c2a17`. Written by the author of the reviewed parent, at the operator’s request, as
the second reader the stack has not yet had.
The question asked was not “is the review right” but “which of its changes are clean
improvements, which are excessive, and which should be objected to” — and, because the
stack was reconciled to a parent that has since moved by twelve commits, what on it is
now out of date.

Two review lanes ran beside this document under their own briefs — one over the code and
tests, one over the records and prose — and their findings are folded in below with
attribution. Every figure here was read from the diff or the artifact, not from PR #80’s
description.

## Verdict

**Merge the substance, not the stack.** PR #80 finds one real gap in the parent’s
reusable verifier and a handful of real record errors, and it fixes them well.
It also carries a Lean project no gate builds, a second standalone verifier beside the
one already shipped, a 731-line hostile-input matrix for an internal command,
thirty-three new defects of which several are duplicates of what the parent found and
fixed on its own, and severity labels that call three parent-fixed or
non-verdict-bearing items “Blocker”.
Its suite budgets are justified by measurements the parent has since made obsolete, and
its defect numbering collides with the parent’s on three ids.

The recommended path is a short PR onto the current #78 head carrying the seven items
listed under **Adopt**, with the rest either dropped or moved out of the validated tree.
If #80 is to merge as a stack instead, the **Must update** list is what has to change
first.

| Question | Answer |
| --- | --- |
| Does anything in #80 change a retained bound or verdict? | No. All four retained certificates decide identically; #80 says so and the lanes confirmed it. |
| Is the nonnegativity finding (F1) real? | Yes, and it is the most valuable thing on the stack. The parent’s `verify()` never required `weight ≥ 0`; the counting step needs it. No retained certificate is affected — every weight is an LP output with `w ≥ 0` — but the verifier as a tool accepted a false theorem. |
| Are the six “Blocker” labels earned? | Four are (F1, F6, F7, F24) — F1 and F6 were reproduced live on the parent’s current head by the records lane. F9 is the parent’s own D-435, found and fixed there before #80 merged it. F17 concerns a path no evidence ever cited and is hardening, not soundness. |
| Is the T-018 promotion from C4 to C5 legitimate? | Yes. `epistemics.md` defines C5 as *review-ready* — C3 or C4 plus an existing `review_artifact` mapped as a non-superseded review — not as external review. The parent’s own prose (“C5 needs a review by someone outside the project”) misstates the rubric and is the parent’s to fix. |
| Is the stack current with #78? | No. It predates T-020, the integer sweep, D-442–D-444, the case-body rewrites, the attainment ratio, agenda-020, session-085 and the closeout; see **Must update**. |

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
- **A second standalone verifier.** `minimal_verify.py` (346 lines) sits beside
  `thirdparty/verify.py`, which already decides the same certificate with the standard
  library under `env -i` and was itself adversarially reviewed on this branch.
  Two self-contained checkers of one file, in one directory, each claiming to be the one
  a stranger should run, is one more than a stranger needs.
  Keep whichever the review lanes find cleaner and fold the other’s distinct checks into
  it.
- **The hostile-input matrix for the retention gate.** `decide_certificate.py` grows by
  313 lines and its tests by 731 to refuse duplicate JSON keys, decimals, overlong
  rationals, coercive integers and malformed atom rows.
  The command is an internal gate run on files the generator wrote minutes earlier; the
  binding it actually needed — the claim and the mass matched to the reconstructed
  object, and the bytes hashed across the two routes (F17’s useful half and F24) — is a
  few dozen lines. Keep those; trim the matrix to one malformed-file refusal per class.
- **Thirty-three new defects.** entry 456 of #80’s log through entry 463 of #80’s log
  are eight entries about one command’s robustness; several others record a finding the
  parent had already fixed independently before the stack merged it (see **Must
  update**). A log that grows by a quarter in one review, with entries this fine, is
  harder to read than the record it is meant to protect.
  Merge the per-command robustness entries into one, and drop the duplicates.
- **The suite budgets.** The fast suite’s cap moves from 1,800 s to 2,700 s and the
  exhaustive tier’s from 900 s to 14,400 s, each justified by a measurement — 1,789 s
  for the ordinary suite, 4,866 s for one exact decision.
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
- **One stale figure the stack introduces.** The Lean research note says “the
  90.5-million-cell C4 decision remains the expensive layer” and “do not begin by
  replaying 90.5 million raw cells” — the `19/5` rung’s cell count — while the same file
  correctly gives the current certificate’s 567,130,649. The class the parent recorded
  four times today, once more.

## Must update: where the stack is behind the parent

PR #80 was reconciled to `719c2a17`. The parent is now at `a159eb28`, twelve commits on,
and the following are not reflected in the stack.

| Parent change since `719c2a17` | What it means for #80 |
| --- | --- |
| **T-020**: `s(19), s(20), s(21) ≥ 24/5`, a fourth certificate package, `n = 19`–`21` case files rewritten, Nagamochi’s closed form now holds 58 of 65 open cases, not 60 | Every count, case body and evidence entry the stack touches for n = 17–19 has moved again; `n-019.md` in particular now carries T-020, not T-019. The frontier-corpus tripwire is 58. |
| **Defects D-442, D-443, D-444** recorded on the parent | The stack numbers its own defects D-442–entry 474 of #80’s log. Three ids collide with different content. The parent’s ids stand; the stack renumbers from entry 445 of #80’s log. |
| **D-442** (five case bodies stale against their front matter) and `devtools.check_case_prose` | The stack’s F28 / entry 467 of #80’s log is the same finding and its entry 466 of #80’s log the same possessive-mass instance; the parent’s rewrites of `n-017`–`n-019` are the ones to keep (the stack’s drop the green17 / T-001 passage and the Massaccesi provenance the parent preserves). Record concurrent discovery once and keep the parent’s detector, which reads every case body against its own front matter. |
| **`frontier/README.md` says 58 of 65** open cases rest on Nagamochi | The stack still says 60; its corpus tripwire and case bodies move with it. |
| **D-441’s consequence field corrected** on the parent | The stack’s F20 / entry 460 of #80’s log fixes the same sentence. Duplicate. |
| **The integer sweep (agenda-020, `d8733ad0`)**: `sweep.py` rewritten around an int64 grid and spans, `verify()` parallel, exact decisions 68–183× faster | The stack’s edits to `sweep.py` (F11, the witness centre) and `certificate.py` conflict textually and must be re-applied on the new code; F11’s witness fix applies to both routes now. The 14,400 s and 2,700 s budgets (F13, F30, F32; entry 451 of #80’s log, entry 470 of #80’s log, entry 471 of #80’s log) were sized for the old cost. |
| **agenda-019 cost figures corrected** (a third paired point; contention noted; 13,000 s figure retracted) | F33’s complaint about the two-point exponents is partly addressed; what remains is the two comparison factors above. |
| **The reach table gained the attainment ratio and a predicted-gain ranking** | F26’s evidence-status column has to be re-applied on the new renderer. |
| **Agenda-017 closed (W10), agenda-020, session-085, the cold-start handoff** now select `BC-191`/`think-ji0r` | The stack’s agenda-019 edits (+65/−48) predate the handoff section and the BC-190 re-basing. |
| **The certificate conditions are being renamed** on both branches from `C0`–`C4` to Condition 1–Condition 5 | Both sides must use the same table (below), or the merge will carry two vocabularies. |

The condition rename, so that the two branches align:

| Old certificate condition | New name | Meaning |
| --- | --- | --- |
| `C0` | Condition 1 | the atom multiset is closed under the container’s D4 symmetry |
| `C1` | Condition 2 | total mass strictly below n |
| `C2` | Condition 3 | the direction net reaches π/4 |
| `C3` | Condition 4 | containment, `B(1 + D) < 1` |
| `C4` | Condition 5 | every closed B-square at every net direction covers mass ≥ 1 |

`C0`–`C5` then mean only the confirmation rungs of `epistemics.md`. F1’s new
nonnegativity requirement is best written as part of Condition 2’s statement (the
weights are nonnegative and their total is below n) rather than as a sixth numbered
condition, so that the count of conditions the tutorial, the proof note and the
standalone package name stays at five.

## Lane findings

*(Filled in from the two review lanes.)*

### Code and tests

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

- **Adopt on the parent now**, as one small PR: F1 with its counterexample fixture, F6,
  F7, F24 with the hash verified at retention, F3, F4, F14’s wording, F26’s evidence
  column, F33’s two factors, the `n-011.md` body and the detector gap behind it, the
  T-017 evidence repointing, the source-key fix, the literature audit with its scoped
  novelty language, the proof note and its figure, and the C5 promotion of T-018 with
  the parent’s own C5 wording corrected.
- **Drop or move**: the Lean lake project (to a research note, and out of T-018’s
  artifact list), one of the two standalone verifiers, the bulk of the hostile-input
  matrix, the budget raises as measured (re-measure on the current head), the
  typographic edits to five dated reviews and the rewritten observation in the sixth,
  the D-439 regression, entry 469 of #80’s log, and the renumbering of the parent’s
  D-441.
- **Fix on the stack**: the tutorial’s vocabulary against the synopsis, the
  `90.5 million` figure, the T-018 proof note’s document-map registration.
- **Re-grade**: F6, F9, F17.
- **Renumber and dedupe** the defects against D-442–D-444 and the parent’s later fixes.

The concrete claim — that the retained certificate proves `s(11) ≥ 381/100` — was never
in question on either branch, and #80’s independent decisions of the same bytes are
welcome confirmation of it.
What the stack adds to the *record* is worth about a tenth of its size.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
