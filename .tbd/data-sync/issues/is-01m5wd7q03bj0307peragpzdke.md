---
type: is
id: is-01m5wd7q03bj0307peragpzdke
title: A tally is never in the toggles' small caps, and the toggle holds the first line
kind: task
status: closed
priority: 2
version: 4
delegate: claude-code@vm
labels: []
dependencies:
  - type: blocks
    target: is-01m5wd7re80yjz5wacnp5fqzy5
parent_id: is-01m5wd6833v6wx316fc361515a
hold: null
hold_until: null
created_at: 2026-10-26T15:28:32.771Z
updated_at: 2026-10-26T17:11:54.740Z
started_at: 2026-10-26T15:28:59.311Z
closed_at: 2026-10-26T17:11:54.740Z
close_reason: null
resolution: null
duplicate_of: null
---
The owner, 26 October 2026: a tally of results is not set in small caps the way a
toggle's label is, one style everywhere, the count bold and its noun lowercase
(`17 results`), and the toggle stays on the first line when a summary wraps.

Where it comes from: KPress's `.kpress summary` sets the shared section-label treatment
-- `font-variant-caps`, `text-transform`, `letter-spacing` and `--kpress-caps-label-size`
-- and `.site-rollup-count` inherits all of it. KPress is a vendored submodule, so the
override belongs in `devtools/overview/results.css` beside the rollup's own rules.

- `.site-rollup-count`: caps variant, transform and letter-spacing back to normal, the
  count in the sans medium weight, the noun lowercase.
- The toggle: `.kpress summary` is a flex box with `align-items: center`, so its
  `::before` chevron centres against a wrapped label. Align a rollup summary to the
  start and keep the glyph on the first line's baseline.
- `tallied_summary` marks the count so the weight has something to sit on, and
  `recent_tally`'s parts stay one shape.

`test_home_recent.py` holds the summary markup; the browser checks that lay the page out
at 1280 and 390 px are what say the wrapped summary reads right.
