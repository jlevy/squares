---
type: is
id: is-01m27hvywbcvahg6vk2cnk9pks
title: Packings in the 300s look short of the best known on the workbench
kind: bug
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-09-packing-strategies-as-a-shared-language.md
labels: []
dependencies: []
created_at: 2026-09-11T06:18:21.962Z
updated_at: 2026-09-11T06:18:21.962Z
---
The owner, watching the workbench play, reports that many packings look as though they sit BELOW the best known — the 300s named specifically.

The readout does not agree, which is why this is worth a look rather than a fix. Scanning the settled instant of every step from n = 290 to 324 through the page's own gapBar(): 32 of 35 report the drawn side exactly equal to the record, 0 below it, and 3 above it by about 1e-6 (n = 300 side 17.824124 against record 17.824123; n = 303 and 306 differ only past the sixth decimal). So either the picture disagrees with the number the same page prints, or what the owner is reading as 'below the record' is something else in the frame.

Hypotheses, in the order they are cheap to test:

1. The container is drawn larger than the packing needs. At a step the box grows to the larger of the two sides BEFORE the squares rearrange into it, so through the move there is genuine slack against the wall. If the settle does not close it visually, every step in a long run reads as a packing that did not fill its box.
2. The record itself leaves visible gaps. A best-known packing at n in the 300s is mostly grid with a tilted core, and the grid rows can stand off a wall. That is the record being what it is, not a defect — but if so the page should not look like it is failing.
3. The gap bar's hand or its scale misreads at this end. The bar's span is a function of the record and the proved lower bound, and in the 300s those are very close, so a fixed head fraction could put the hand in a misleading place.
4. 'met' is decided against a rounded decimal. Three steps report a side a millionth above the record, which is the rounding of the printed value rather than a real excess; the tolerance should be stated rather than implicit.

To do: reproduce visually (capture the settled frame at a few n in the 300s and measure the drawn squares' bounding box against the drawn container), then say which of the four it is.
