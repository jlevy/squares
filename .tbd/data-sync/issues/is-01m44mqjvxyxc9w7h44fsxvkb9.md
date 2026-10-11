---
type: is
id: is-01m44mqjvxyxc9w7h44fsxvkb9
title: "Site: one hover transition token, used by every hover background and colour change"
kind: task
status: closed
priority: 2
version: 3
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m42xfwp06kzm2b390dx1cw17
hold: null
hold_until: null
created_at: 2026-10-04T23:42:04.669Z
updated_at: 2026-10-05T01:45:18.611Z
started_at: 2026-10-05T01:07:48.707Z
closed_at: 2026-10-05T01:45:18.611Z
close_reason: Merged in jlevy/squares#348
resolution: null
duplicate_of: null
---
Owner request 2026-10-04: hover background changes snap with no transition. Define one design-system variable (smooth but quick, e.g. --site-hover-transition) and use it on every :hover / :focus-visible background, colour and border change across site.css, site-nav.css, site-result.css and paper-type.css (and the papers' and workbench's shared layers where they hover), respecting prefers-reduced-motion. A contract test holds every hover rule to the token.
