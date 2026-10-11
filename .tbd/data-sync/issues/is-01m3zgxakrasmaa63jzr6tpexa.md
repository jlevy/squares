---
type: is
id: is-01m3zgxakrasmaa63jzr6tpexa
title: "Cases: the standard case view, the best packing drawn first and large, then the number line of the lower and upper bounds, then the record's facts"
kind: task
status: closed
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3zgx0c1edkfwarjxzctvgmp
created_at: 2026-10-02T23:59:06.359Z
updated_at: 2026-10-03T14:38:05.169Z
closed_at: 2026-10-03T14:38:05.169Z
close_reason: Merged in jlevy/squares#312 (c831b4ee0), after a correctness and engineering review round (419a1db5d)
resolution: null
duplicate_of: null
---
The one view of a case (think-t21m): its known-best packing drawn large at the top, then the number line of its verified and reported lower and upper bounds, the visual the film and the results show for some values, then the record's facts, cleaner than the case record today. One builder, used by the case page and by the frontier popover (and by results where it fits). Shots at 1280 and 390, both schemes; tests; paper-design.md (Case records).

## Notes

Owner, 2026-10-02, later: 'the link to All cases on cases.html#cases on a current case record page is kind of broken as it's not a real navigated link to see an individual case record like n=10. we should have proper routing and urls for each case record. they should be sharable and linked off the frontier page. basically the popover for an svg on the atlas on the homepage should be the visual summary of the record and it's the core visual component of the case. then there are additional elements on that page. we should make the frontier table be the same as the svg atlas in the sense that each case is the same, with the visual summary and then the additional data below it. this is somewhat different than the results table, where it is truly details on that result plus an inclusion of a link to the case record.' The standard view IS the atlas popover's visual summary, made one builder: the case page and the frontier popover take it, then the record's further data below it. Owner, later still: 'that way every part of the atlas or of the frontier are linking to the same set of case records, and each case record has a visual summary. the visual summary is similar but not the same as what goes in the video since the visual rendering should be larger and above the number line, but it's similar in visuals and content, just laid out better for page viewing.' So: the visual summary is the film frame's content (the packing, the bounds' number line, where each comes from) laid out for a page: the drawing larger and above the number line.
