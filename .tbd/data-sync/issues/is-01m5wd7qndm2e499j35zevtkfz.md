---
type: is
id: is-01m5wd7qndm2e499j35zevtkfz
title: Reader text says record rather than house best packing
kind: task
status: in_progress
priority: 2
version: 3
delegate: claude-code@vm
labels: []
dependencies:
  - type: blocks
    target: is-01m5wd7re80yjz5wacnp5fqzy5
parent_id: is-01m5wd6833v6wx316fc361515a
hold: null
hold_until: null
created_at: 2026-10-26T15:28:33.452Z
updated_at: 2026-10-26T15:28:59.763Z
started_at: 2026-10-26T15:28:59.763Z
---
The owner, 26 October 2026: "house best" is confusing; the point is whether the packing
is a new record.

`conventions.md` section 5 and `SYNOPSIS.md`'s terminology own *house best packing* as a
project term, and `upper_bound_houses`, `adopt_houses` and the case records use it
throughout. This bead changes the reader-visible site strings only, and leaves the
glossary and the technical record as they are:

- `overview_sections.recent_tally`: `4 house best packings` becomes the record wording.
- `overview_sections.house_entry`: "<result> is now the house best packing at <counts>".
- `devtools/site_resources.py` around line 158.
- `devtools/templates/overview-article.md`, which the introduction rewrite also touches.

The claim has to stay true: by the import runbook's house rule the house best is the
smallest validated packing this project holds for a count, so it is this record's record
for that count, not a claim about every packing ever published.
