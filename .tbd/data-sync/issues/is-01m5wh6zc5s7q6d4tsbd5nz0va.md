---
type: is
id: is-01m5wh6zc5s7q6d4tsbd5nz0va
title: Decide whether house best packing keeps its name across the record
kind: task
status: in_progress
priority: 3
version: 4
delegate: null
labels: []
dependencies: []
hold: paused
hold_until: null
created_at: 2026-10-26T16:38:02.885Z
updated_at: 2026-10-26T22:04:47.439Z
started_at: 2026-10-26T21:54:39.931Z
---
Raised by the owner on 26 October 2026, while the site's generated reader strings were
changed to say *record packing* (think-196d): "house best" is a confusing term, and the
point is whether the packing is a new record.

What changed there: `overview_sections.house_entry` and `recent_tally`, which write the
Recently Added lines and their counts, and one sentence in `devtools/site_resources.py`.

What still says *house best packing*, and why it was left:

- `conventions.md` section 5 and `SYNOPSIS.md`'s terminology own the term, and the
  convention is that a project term is defined in the synopsis before other documents
  use it. Renaming starts there.
- The retained entry prose in `packing/site-changelog.yaml`, which the News page, the
  Changelog page and `CHANGELOG.md` all render, so a reader now meets both wordings on
  the same page.
- The case records, the atlas and the import runbook's house rule, plus
  `upper_bound_houses`, `adopt_houses` and `stamp_landed`, whose identifiers
  `conventions.md` says keep their names either way.

The decision the owner has to make is whether *record packing* replaces the term
everywhere a reader meets it, or whether the term stays and the synopsis entry is what
clarifies it. Either way the claim has to stay true: by the house rule the house best is
the smallest packing this record holds for a count, which is this project's record for
it, not a claim about every packing ever published.

## Notes

## Measured on the deployed page, 26 October 2026

The homepage now carries 18 occurrences of *record packing* and 2 of *house best
packing*. Both remaining occurrences are retained entry prose, and in both the term is
load-bearing rather than loose:

- Couzo's certificates of #763 at 268 and 303 "pass a clean-room review here and become
  the house best packings **there**" — the claim is about what this project then holds
  at those counts, not about every packing ever published.
- T-243 at 182: "a new arrangement relative to **the record**, it becomes **the house
  best packing** at 182" — one sentence using both terms to draw the distinction.

So the two wordings are not synonyms, and `conventions.md` section 5 already says so:
*house* is only a modifier meaning the project's own. Writing *record packing* into
either sentence would make a true statement false.

That narrows the owner's decision. The generated reader strings were the place the term
was genuinely wrong, because there the point really was whether a packing is a new
record, and think-196d changed them. What is left is not a rename but a disclosure
question: whether a reader who meets *house best packing* on the News or Changelog page
can find out what *house* means without opening `conventions.md`. The cheapest answer
that keeps every claim true is to define the term once where a reader meets it rather
than to replace it.
