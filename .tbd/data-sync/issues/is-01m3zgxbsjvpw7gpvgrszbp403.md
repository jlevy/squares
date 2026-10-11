---
type: is
id: is-01m3zgxbsjvpw7gpvgrszbp403
title: "Frontier: a row opens the case's own view in its popover, and the minimal row popover goes"
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3zgx0c1edkfwarjxzctvgmp
created_at: 2026-10-02T23:59:07.569Z
updated_at: 2026-10-03T14:38:05.785Z
closed_at: 2026-10-03T14:38:05.784Z
close_reason: Merged in jlevy/squares#312 (c831b4ee0), after a correctness and engineering review round (419a1db5d)
resolution: null
duplicate_of: null
---
think-t21m: pressing a frontier row opens a popover that shows the case's standard view, the same as its case page, with a way to open that page; the current minimal frontier row popover is retired. Keyboard, Escape, a click outside and the address (frontier.html#n-11) keep working; tests and paper-design.md (Frontier table, Row popovers) follow.

## Notes

Owner, 2026-10-02, later: 'the link to All cases on cases.html#cases on a current case record page is kind of broken as it's not a real navigated link to see an individual case record like n=10. we should have proper routing and urls for each case record. they should be sharable and linked off the frontier page. basically the popover for an svg on the atlas on the homepage should be the visual summary of the record and it's the core visual component of the case. then there are additional elements on that page. we should make the frontier table be the same as the svg atlas in the sense that each case is the same, with the visual summary and then the additional data below it. this is somewhat different than the results table, where it is truly details on that result plus an inclusion of a link to the case record.' A frontier row opens the visual summary and the additional data below it, the same as the case page and the atlas popover.
