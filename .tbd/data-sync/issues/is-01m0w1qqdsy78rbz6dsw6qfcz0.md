---
type: is
id: is-01m0w1qqdsy78rbz6dsw6qfcz0
title: Lift notation and terminology into conventions.md as the definitive registry
kind: task
status: closed
priority: 2
version: 3
spec_path: explorations/packing/docs/project/reviews/review-2026-08-25-tutorial-pedagogy-and-accuracy.md
labels: []
dependencies: []
parent_id: is-01m0w1p1t7gaen5tzf1pt94f3x
created_at: 2026-08-25T08:49:05.464Z
updated_at: 2026-08-25T09:13:16.768Z
closed_at: 2026-08-25T09:13:16.768Z
close_reason: "Done in 8e203f0. conventions.md §4 already owned assurance and method as a schema-enforced registry, so the gap was only mathematical notation and terminology; conventions gains a Notation and Terminology section with the rules, SYNOPSIS keeps definitions, the tutorial keeps teaching forms. Bare 'gap' decided to mean the search gap, matching existing usage, so nothing needed rewriting. Surfaced and fixed a real error: the tutorial claimed a star marks a minimiser throughout while using s-star for the standing best, which would assert Trump's packing optimal. SYNOPSIS also had the numerically-checked misspelling. Mechanical enforcement via RETIRED_PHRASES was considered and declined with reasons recorded — a phrase scan cannot distinguish use from mention and would reject the review that documents the defect."
resolution: null
duplicate_of: null
---
Depends on think-pv5m. Checking comes first: promoting a vocabulary into a definitive
registry before it has been verified would turn any error into a rule.

## The problem

Terminology and notation are currently spread across three documents with three
different authority levels, and none of them is the definitive registry:

- `TUTORIAL.md` §9 has a vocabulary card and §10 a notation card, both written for a
  newcomer and both explicitly deferring: "`SYNOPSIS.md#terminology` is the authority".
- `SYNOPSIS.md#terminology` has the full prose definitions, and is a living status
  document revised whenever a result lands.
- `README.md` has an eight-row "Essential Terms" table, a third short form.
- `conventions.md` is the document that actually describes itself as "the definitive
  registry of every convention, id class, and naming rule, and which are machine-checked"
  — and it carries no mathematical notation or terminology at all.

So the one document whose stated job is to be definitive is the one that does not hold
this. That is why the same term drifts in three places, and it is the same shape as the
gate-count drift that `think-4b9m` closed.

## What to consider moving

Notation, which is currently only in the tutorial's §10 card and nowhere authoritative:
the subscript rule (subscript `i` is one square, a bare letter is the whole `n`-vector),
the `*`-marks-a-minimiser rule, and the symbol table itself.
Terminology: which document owns the narrow definitions, and what the other two are
allowed to restate.

## Questions to settle first, since this is an ownership change

- **Does `conventions.md` want prose definitions, or only the rules?** Its existing
  entries are rules with `[checked]` / `[convention]` markers. A symbol table is not a
  rule. One option is that conventions owns the *rules* (subscript convention, the `*`
  mark, which spelling of an enum value is canonical) while `SYNOPSIS.md` keeps the
  definitions and the tutorial keeps the teaching form.
- **What becomes machine-checked?** The value of moving this into conventions is that
  things there can be enforced. A checker could plausibly verify that the assurance and
  method tokens used in prose match the schema enums, which is exactly the drift
  `think-po3b` fixed by hand.
- **What happens to the three restatements?** If conventions becomes definitive, the
  tutorial's two cards and the README's table become derived views, and the rule against
  copied aggregates that this directory already applies to counts should apply to them
  too.

## Do not

Do not collapse the tutorial's cards into a pointer. They are pedagogical, ordered by
introduction and by dependency rather than alphabetically, and a newcomer needs them
in place. The question is which document is *authoritative*, not which one has a table.
