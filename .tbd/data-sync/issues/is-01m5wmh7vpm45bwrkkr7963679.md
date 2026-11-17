---
type: is
id: is-01m5wmh7vpm45bwrkkr7963679
title: Redraw the assets and move their records with them
kind: task
status: in_progress
priority: 2
version: 5
delegate: null
labels: []
dependencies: []
parent_id: is-01m5wmghkt8vpnawbxzpbkm19e
hold: paused
hold_until: null
created_at: 2026-10-26T17:36:04.982Z
updated_at: 2026-10-26T22:04:47.889Z
started_at: 2026-10-26T21:57:17.909Z
---
Apply the rule, redraw and re-measure.

- Redraw both poster families and every advertised export
  (`development.md`, "Release assets are drawn at their component's version bump").
- Move the retained composite descriptions in `build_known_best_atlas` with the drawing:
  they are prose a reviewer reads against it, and they name the address today.
- Re-measure the print layout. A changed line shifts baselines and ink bounds, which
  `check_print_layout` and the poster records hold.
- Take the release-impact decision for the infographic family rather than a
  no-public-change record: both families and every advertised export advance together,
  and this changes what the asset prints.
- Verify the PDFs by reading them, not by trusting the generator.

Depends on the rule bead.

## Notes

## What a reader sees today, measured on the deployed assets, 26 October 2026

The two addresses now disagree inside a single published PDF, which is the clearest
statement of what this bead is for. In `papers/n11-lower-bounds-explainer.pdf` as
deployed:

- page 25, the paper's own colophon, carries the new line —
  `The Squares Project · squaremath.org · github.com/jlevy/squares`;
- page 5, the embedded *100 Best Known Square Packings* poster, still carries
  `The Squares Project · github.com/jlevy/squares`.

The paper's colophon is shared chrome and moved with #837. The poster is a drawn
release asset, so its line only changes when the infographics component is cut, and
that is the decision this bead waits on.

## Why the cut is not just this wording

`build_known_best_atlas --check-composites` reports `known-best-1-324.svg` already
trailing the record in five cards: n = 31, 182, 268, 303 and 304. A cut made to correct
an address would publish those five bound changes in the same release, so the redraw is
an editorial decision about what the poster states, not only about its credits line.
That is the owner's call, and nothing here is blocked on anything else.
