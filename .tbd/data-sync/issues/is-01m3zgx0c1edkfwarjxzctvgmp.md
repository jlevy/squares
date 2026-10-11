---
type: is
id: is-01m3zgx0c1edkfwarjxzctvgmp
title: "Cases: one page per case, the frontier row opens the case's own view, and one standard case view (the drawing large, then the bounds' number line)"
kind: epic
status: closed
priority: 2
version: 8
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
child_order_hints:
  - is-01m3zgxakrasmaa63jzr6tpexa
  - is-01m3zgxb73ga2gmjytxeb22ej8
  - is-01m3zgxbsjvpw7gpvgrszbp403
  - is-01m3zgxcbe1bq63k5g089ng0y5
created_at: 2026-10-02T23:58:55.872Z
updated_at: 2026-10-03T14:38:06.555Z
closed_at: 2026-10-03T14:38:06.554Z
close_reason: Merged in jlevy/squares#312 (c831b4ee0), after a correctness and engineering review round (419a1db5d)
resolution: null
duplicate_of: null
---
Owner, 2026-10-02: 'we should find a way to unify the frontier and the case records. there is a lot broken there. we don't need a full page for the cases (cases.html#cases) we need a page for each case and we need a way to put each case into the popover for the frontier page when you click a row. the current popover on the frontier rows is minimal and can go away. it should instead show the case popover, which is the same as the relevant case page for that case. the cases should be cleaner too. the case record should also include the number line visual that we have in the video and in the results table for some values. finally that layout should put the visual of the square first, and large, then have the number line view of the lower and upper bounds. this is the standard view of the square and its upper/lower bounds for a specific case, and it is what should be present also for context on any result page where it makes sense'. Children: a page per case; the standard case view; the frontier popover is that view; the view on results where it fits.

## Notes

Owner, 2026-10-02, later: 'the link to All cases on cases.html#cases on a current case record page is kind of broken as it's not a real navigated link to see an individual case record like n=10. we should have proper routing and urls for each case record. they should be sharable and linked off the frontier page. basically the popover for an svg on the atlas on the homepage should be the visual summary of the record and it's the core visual component of the case. then there are additional elements on that page. we should make the frontier table be the same as the svg atlas in the sense that each case is the same, with the visual summary and then the additional data below it. this is somewhat different than the results table, where it is truly details on that result plus an inclusion of a link to the case record.' So: the visual summary is the atlas popover's view (the packing large, the bounds and where each comes from, what is open); a case page = that summary + the rest of the record; a frontier row opens the same; results keep their own details and link the case record.
