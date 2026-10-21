# Submitting records: style guide and template (10-20)

How we write registration requests for jlevy/squares (and any other register).  The generator is `submission.py`
(draft from a `candidate.py` work dir; nothing is posted).  Posting needs Evan's explicit OK per post (CLAUDE.md).
Drafts go in `outreach/` as `draft-jlevy-n<N>-<date>.md`; after posting, rename to `posted-...-issue<K>.md` with the
`# POSTED` header line, as before.

Why this exists: jlevy's records follow our wording for credit ("credit follows what each source says", #673), and we
have not been consistent.  #664 called the same packing "a refinement of #561" and "a different local minimum", and
jlevy had to ask which we meant.  Our step lists used "Refinement:" for our own polishing step.  Our regularized views
said `"by": ["Francisco Couzo"]` (a regularizer default, fixed in candidate.py 10-20) and jlevy asked about it twice.

## Vocabulary (Evan 10-20)

Two packings are **the same packing** when one is reached from the other by **shrink-only moves**: gradient descent /
polishing, sliding along flat motions, moving rattlers, a descent that switches corner–corner contact branches without
expanding the box, and recomputing at tighter precision (an exact KKT solve, a smaller dilation).  These are the only
moves that don't explode the search space (Evan 10-20).  A packing reached with anything else (kicks, tilt swaps,
crossovers, insertion / removal, expansion, basin hopping, any non-monotone step) is a **new packing**, however close
it lands: finding it took a search.

These are one notion seen two ways (Evan 10-20): both ask whether the two packings are connected by a path along
which the box never has to grow.
* **Path view:** the moves that produced it (a lineage of shrink-only moves), or a constructed path between the two
  (`landscape/morph.py`: a feasible walk whose expansion barrier is 0).
* **Point view:** the endpoints themselves.  Each shrink-only path ends at a local minimum, so two packings joined by
  one share it: equal exact KKT sides (exactsolve, 1e-30) and the same contact graph (`pk/distinct.compare`).
  Different sides or graphs means no such path exists.
Use both.  A lineage with a non-shrink move makes a new-packing *claim*; the point comparison decides it.

Edge cases (Evan 10-20):
* **A non-shrink move can land back in the same minimum**, just solved more tightly (a kick and re-polish that returns to
  X's basin: the explorer's "return" status is exactly this).  So a non-shrink lineage is necessary, not sufficient.
  The point comparison is only exact between *tightened* packings: compare KKT points (exactsolve), not raw floats or
  dilation certificates.  candidate.py tightens ours and the prior record; tighten a credited start the same way before
  calling it a different minimum (submission.py's relation test only polishes it: good enough to flag, not to decide).
  A "tighten every incoming packing" rule would make this guaranteed; we don't have one.
* **Rattlers moved to a configuration reachable only with growth**, with the rigid core unchanged.  The side and the
  core's contact graph are the same, so the point view says "same minimum", but no shrink-only path exists (a rattler
  would have to pass through a gap narrower than itself), so the path view (morph walk) can say "different".  The
  bound is set by the core.  Convention: **the same packing, modulo rattlers** (a refinement / regularization; the
  regularizer moves rattlers anyway).  If the path test fails while the point test says "same", check the rattlers
  first (`compare`: `rattler_status_swaps`, and matched moves of rattlers, which `moved_*` counts exclude).
  Working definition (best effort; not fully rigorous): a packing's identity for record claims is its **rigid core**,
  the squares exactsolve finds load-bearing, with the core's exact side and contact graph; rattlers are ignored.
  Edge of the edge case: a square that rattles in one packing and is load-bearing in the other (`rattler_status_swaps`
  > 0) changes the core, so look closer.  (Rattler arrangements can still matter as search starts: a separate topic.)

| Term | Use it for | How we decide |
|---|---|---|
| **refinement** of X | reached from X by shrink-only moves: the same local minimum, with a tighter bound or a better solve (an exact KKT point for a float packing, a smaller dilation, a converged polish) | X polishes (fq POLISH) to our KKT point: sides equal to 1e-9 in float, then equal exact sides (exactsolve, 1e-30) and the same contact graph; or the morph walk connects them with no expansion |
| **regularization**, **regularized view** of X | the same packing at the same side, rattlers and flat-motion squares moved for display | the regularizer's level 1-2 ("traversable without expansion") |
| **new packing found from X** (also: *started from X*, *seeded with X*, *lineage from X*) | a different local minimum, or anything our search reached from X with a non-shrink move; X was a start or ancestor | different exact side, or different contact graph |
| **same design / family as X** | descriptive only: shares X's tilt groups, bands or blocks.  Combine with "new packing", never instead of it | shared load-bearing tilt angles, band structure |
| **improves the bound** | our side is below the best public side at n | always "improves the bound at n" / "below X's side", never "improves X's packing" (that reads as a refinement) |

Do not:
* call a different local minimum a refinement, or call anything both ("same design, a different local minimum" is
  fine; "a refinement of X ... a different local minimum" is a contradiction: #664);
* name our own pipeline step "Refinement" (say **Polish and certify**);
* use "continuation", "based on", "derived from" without saying which of the two relations holds.

**jlevy's measurement, and where we differ (Evan 10-20).**  Their record says "refinement" when the best one-to-one
assignment moves no square by more than 0.1 (#664 reply, 10-20), and "another arrangement of X's design" otherwise.
That is geometry; ours is minimum identity, and we keep ours.  A better local minimum that changes the band or bulb
pattern by a few squares, each by less than 0.1, is still a new packing and still real work: at large n everything is
in the same two-bulb family, and searching every pattern within 0.1 of a record is out of reach, so a search that finds
one is significant.  So:
* always give the matched-move numbers (max move, count > 0.1, count > 0.01) so they can apply their rule;
* when our call and theirs disagree (a different minimum with no square moving more than 0.1), **say so explicitly**,
  e.g. "We call this a new packing although no square moves more than 0.1 (your refinement threshold): it is a
  different local minimum (exact sides differ by 2.4e-9; contact graphs differ in 17 pairs), found by <search>";
* never let geometric closeness turn into the word "refinement" in our text.

**Lineage is not the story; the search is.**  We have been over-stating "this pattern was in our lineage", which reads
as "we tweaked X".  Often the mechanism was a hunt: the record was one start among many, it produced a dozen non-record
packings, those produced more, and a couple of generations on one was a new record.  Present it that way:
* **short lineage**: our search reached it in a few moves from X.  That is still a search, often a lucky early hit in
  a large space (271: an explorer test run over 52 counts; the hit came 90 s in, one tilt swap from #561).  Say what
  the search was and that the lineage is short; it is a new packing found from X, not a tweak of X;
* **hunt**: X was among the starts of a population search.  Lead with the search (method, generations from the
  credited start, number of intermediate non-record packings, CPU-h), then credit the starts in one sentence.  Don't
  narrate the pattern's descent from X square by square.

## Credit

* **Credit name** line: "Evan Daniel (GitHub @evand)".
* For a **new packing**: we are its finder.  Name every packing that was a start or a direct ancestor ("Please credit
  X's packing (#issue / register witness) as the start"), and any construction it keeps ("Y's two-wedge construction").
  Ancestors that were themselves found by others get named even when they are several steps back.
* For a **refinement** of someone else's packing: they are the finder; ask to be listed as an improver.
* Lineage must be traceable: cite the tool that traced it (`chain_lineage.py`, explorer logs) and make sure it is
  committed at the pin.
* The regularized view's JSON `"by"` field names the **finder of that packing** (candidate.py writes it from the
  credit line since 10-20).  It is not a credit request.

## Presentation (Evan 10-20)

We give more detail than most record reports.  That is good, but unorganised detail is how the misreadings happened
(a lineage narrative read as "tweaked X"; a step called "Refinement").  So:
* **The top of the issue says four things and nothing else:** the claim (table), the certificate (commit, files,
  hashes), the credit request in one or two sentences, and the relationship verdict in one sentence per packing
  ("a new packing (a different local minimum) found by <search> from starts including X").
* **Evidence goes below, in collapsed `<details>` sections** with plain headings: checking, local optimality, the
  comparison table and matched-move numbers, the search narrative.  Readers who want it can open it; nobody has to
  read past it to find the request.
* Point to committed files (the vs_prior JSON, logs) instead of pasting long tables where possible.
* One term per relationship, used the same way everywhere in the issue.

## Template

`submission.py` fills everything it can and marks the rest `TODO(...)`.  Sections, in order (1-4 plus a one-paragraph
**Credit and relationship** on top; 5-8 inside collapsed `<details>` blocks, per Presentation above):

1. **Title:** `s(N) ≤ X.XXXXXXXXXXXX: registration request` (side rounded *up* at 12 places).
2. **Credit name.**
3. **Claim.** One-row table: n, new upper bound, best public before it, improvement, that bound's source.
   Then the comparison scope ("the register (main @sha), open and closed issues through #K, Ellsworth's catalogue, the
   monotone envelope; checked <date>").  Run the live check (`candidate.py --live N S`) the day you post.
4. **Certificate.** Commit + path, the files (cert, exact KKT point, f64 input, solver report, regularized view), table
   of side and SHA-256.  The commit must be pushed before posting.
5. **Checking.** Our two checkers, how to run them, what they share.
6. **Local optimality.** Numerical evidence, not proofs: KKT, strict modulo k flat motions / inconclusive, contacts,
   corner-corner contacts, rattlers, tilted squares and angles; explorer restarts that found nothing lower.
7. **Relationship to earlier packings.**  One line per packing: the prior record and every credited start.  The
   verdict term from the vocabulary table, then the numbers (exact-side gap, contact-graph diff, matched moves max /
   > 0.1 / > 0.01, shared tilt angles).  Use the generated comparison table for the prior record.
8. **How it was found.**  Short lineage or hunt (above).  For a hunt: the search first (method, generations from the
   credited start(s), intermediate non-record packings, CPU-h), then "Please credit ... as start(s)" in one sentence.
   Numbered steps if useful; the last one is **Polish and certify**.
9. Optional: questions for them, or answers to their open questions on earlier issues.

## Checklist before asking Evan to post

- [ ] `candidate.py ... --stage` ran clean; files committed and pushed; the commit in the draft is that one.
- [ ] Live check the same day; the claim table's "best public" is today's.
- [ ] Relationship terms come from the table above, with the numbers; no "refinement" unless same minimum.
- [ ] If it is a new minimum but no square moves > 0.1, the draft says so explicitly.
- [ ] Lineage framed as direct or hunt; for a hunt, the search effort leads.
- [ ] Every start / ancestor named, with its source; lineage tool committed.
- [ ] Regularized view's `"by"` names the finder (check the staged `_regularized.json`).
- [ ] Open questions from jlevy on earlier issues: answered or listed (`outreach/` drafts).

## Our past submissions under this vocabulary (audit 10-20)

| Issue | What we wrote | Under this guide |
|---|---|---|
| #552 (154) | "a different local minimum from T-136"; start Couzo's 155 | consistent |
| #606 (146) | "a different local minimum from #505, not a re-polish of it"; start Xu's #432 | consistent |
| #659 (236) | "a different local minimum from #481"; "credit #481 for the construction" | consistent (jlevy read it as "based on": we are finder) |
| #664 (271) | "Same design, a different local minimum.  This is a refinement of the #561 packing" | **contradictory**; jlevy asked which (open; reply drafted in `outreach/draft-jlevy-replies-2026-10-20.md`) |
| #669 (155) | "a different local minimum.  Not a refinement of the T-149 packing" | consistent |
| #674 (229 update) | "a nearby configuration of the opening post's packing (same tilted structure)" | ambiguous: both are dilation certificates of unjammed polishes, so same-minimum was never tested (jlevy: 8 squares move > 0.1) |
| #680, #689, #694 | lineage fine; step "4. **Refinement:**" for our own polish | wording: say **Polish and certify** |
| all with regularized views | `"by": ["Francisco Couzo"]` in the view's JSON | tooling bug, fixed 10-20; explained in the replies draft |
