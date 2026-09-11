---
type: is
id: is-01m28qw90aqjhrn2jbb7vb7427
title: Drop the progress scale along the bottom of the stage
kind: task
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-09-packing-strategies-as-a-shared-language.md
labels: []
dependencies: []
created_at: 2026-09-11T17:22:38.216Z
updated_at: 2026-09-11T17:22:54.133Z
---
The owner: the scale at the bottom is distracting, drop it entirely.

It is the band 1034-1080: a track with a fill, a numeral every 25 with a major tick and a minor tick every 5, and the riding n in bold with a cursor on the track (#progress, .p-track, .p-fill, .p-tick, .p-num, .p-cursor, .p-n in template.html). It was revision 7's replacement for two end labels, so it has already been through one round of being too much.

What it carries that is worth keeping somewhere quieter, if anything: where a continuous run has got to, over a range that can be the whole corpus. The transport already reports that in Animate, and a film has its own scrubber, so the honest answer may be that nothing needs to replace it.

Two things to check while removing it, both recorded because they were designed around the band:

1. buildScale, measureDigit and syncScale exist to lay it out, and digitWidth -- measured off its numerals -- is ALSO used by the gap bar's two labels. That measurement has to survive the removal or move somewhere else, or the bar's labels will collide.

2. The panel's own geometry was cut to end at 1032, clear of the band. With the band gone there are 48 px at the bottom of the stage that the panel could use or leave as margin.

The gate has checks on it -- the scale's span at both ends of the corpus, the riding n hiding the numeral it would touch, the bar being absent in Pack -- and those go with it.
