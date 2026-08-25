---
type: is
id: is-01m0w1p1t7gaen5tzf1pt94f3x
title: "[epic] W2 correctness and consistency pass over the reworked tutorial and its neighbours"
kind: epic
status: closed
priority: 1
version: 4
spec_path: explorations/packing/docs/project/reviews/review-2026-08-25-tutorial-pedagogy-and-accuracy.md
labels: []
dependencies: []
child_order_hints:
  - is-01m0w1q09whe01v1r1dntyzsq3
  - is-01m0w1qqdsy78rbz6dsw6qfcz0
created_at: 2026-08-25T08:48:10.566Z
updated_at: 2026-08-25T09:13:16.779Z
closed_at: 2026-08-25T09:13:16.779Z
close_reason: "Done in 8e203f0. conventions.md §4 already owned assurance and method as a schema-enforced registry, so the gap was only mathematical notation and terminology; conventions gains a Notation and Terminology section with the rules, SYNOPSIS keeps definitions, the tutorial keeps teaching forms. Bare 'gap' decided to mean the search gap, matching existing usage, so nothing needed rewriting. Surfaced and fixed a real error: the tutorial claimed a star marks a minimiser throughout while using s-star for the standing best, which would assert Trump's packing optimal. SYNOPSIS also had the numerically-checked misspelling. Mechanical enforcement via RETIRED_PHRASES was considered and declined with reasons recorded — a phrase scan cannot distinguish use from mention and would reject the review that documents the defect."
resolution: null
duplicate_of: null
---
The tutorial rework (think-ysoj, closed) was written under an exposition focus: it added
a notation card, a written-out linear program, a concrete quench description, precision
costs, the primitive-element answer, further reading, and a rebuilt vocabulary card.
That work has not been through an independent correctness pass, and it changed enough
vocabulary and notation that the neighbouring documents may no longer agree with it.

This epic switches focus to **Correctness**, under `W2 factual-review`.
Per the workflow contract, W2 is correctness-only and read-only by default: it may apply
an obvious bounded correction whose evidence and scope are unchanged, and it may not
invent successor theory or redesign the presentation inside the review.
Anything larger becomes a successor bead.

Enter with: `TUTORIAL.md` at its current head, `SYNOPSIS.md`, `README.md`,
`conventions.md`, the `frontier/` and `campaign/` artifacts, `src/sqpack/`, and the
review document above as the record of what the rework was trying to do.

Two children, in order. The second depends on the first, because lifting a vocabulary
into a definitive registry before it has been checked would promote any error into a
rule.
