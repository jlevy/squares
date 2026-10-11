---
type: is
id: is-01m3zgxcbe1bq63k5g089ng0y5
title: "Results: the standard case view gives context where a result is about one case"
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3zgx0c1edkfwarjxzctvgmp
created_at: 2026-10-02T23:59:08.142Z
updated_at: 2026-10-03T14:38:06.179Z
closed_at: 2026-10-03T14:38:06.179Z
close_reason: Merged in jlevy/squares#312 (c831b4ee0), after a correctness and engineering review round (419a1db5d)
resolution: null
duplicate_of: null
---
think-t21m: a result's page or popover that concerns a single case (or a short run of cases) shows that case's standard view, the drawing and the bounds' number line, for context, where it makes sense; where a result spans many cases it links them instead. Which surfaces take it is decided against the rows and popovers as they are, and recorded in paper-design.md.

## Notes

Owner, 2026-10-02, later: 'the link to All cases on cases.html#cases on a current case record page is kind of broken as it's not a real navigated link to see an individual case record like n=10. we should have proper routing and urls for each case record. they should be sharable and linked off the frontier page. basically the popover for an svg on the atlas on the homepage should be the visual summary of the record and it's the core visual component of the case. then there are additional elements on that page. we should make the frontier table be the same as the svg atlas in the sense that each case is the same, with the visual summary and then the additional data below it. this is somewhat different than the results table, where it is truly details on that result plus an inclusion of a link to the case record.' Results stay the result's own details plus a link to the case record; the full case view is not repeated there. Re-scope: make sure every result row and popover links its case records, and add the visual only where it plainly helps.
