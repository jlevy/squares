---
type: is
id: is-01m5wh6zc5s7q6d4tsbd5nz0va
title: Decide whether house best packing keeps its name across the record
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-10-26T16:38:02.885Z
updated_at: 2026-10-26T16:38:02.885Z
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
