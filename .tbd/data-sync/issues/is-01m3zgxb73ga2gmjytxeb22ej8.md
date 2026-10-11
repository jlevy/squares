---
type: is
id: is-01m3zgxb73ga2gmjytxeb22ej8
title: "Cases: a page for each case, in place of the one page of every record (cases.html)"
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3zgx0c1edkfwarjxzctvgmp
created_at: 2026-10-02T23:59:06.977Z
updated_at: 2026-10-03T14:38:04.690Z
closed_at: 2026-10-03T14:38:04.690Z
close_reason: Merged in jlevy/squares#312 (c831b4ee0), after a correctness and engineering review round (419a1db5d)
resolution: null
duplicate_of: null
---
think-t21m: replace cases.html, which holds every case record and shows the one its fragment names, with a page per case (for example cases/n-11.html) holding the standard case view. cases.html and cases.html#n-11 keep working through the site's forwarders; every link to a case record (frontier rows, atlas tiles, result rows and popovers, prose, README, epistemics.md) is repointed; the build, the sitemap and the published-site checks follow.

## Notes

Owner, 2026-10-02, later: 'the link to All cases on cases.html#cases on a current case record page is kind of broken as it's not a real navigated link to see an individual case record like n=10. we should have proper routing and urls for each case record. they should be sharable and linked off the frontier page. basically the popover for an svg on the atlas on the homepage should be the visual summary of the record and it's the core visual component of the case. then there are additional elements on that page. we should make the frontier table be the same as the svg atlas in the sense that each case is the same, with the visual summary and then the additional data below it. this is somewhat different than the results table, where it is truly details on that result plus an inclusion of a link to the case record.' Each case gets a real, shareable address of its own (a page per case), linked from the frontier table; the 'All cases' link and cases.html#… fragments forward to it.
