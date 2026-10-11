---
type: is
id: is-01m3v9912ea0g6xyne7qfnrgxy
title: "Site nav: the site name and tabs sized against the larger body text (tabs one notch below body, no more)"
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T08:28:43.467Z
updated_at: 2026-10-01T09:35:48.293Z
closed_at: 2026-10-01T09:35:48.274Z
close_reason: "eb42bc02c, merged into jlevy/squares#264: nav links and section tabs sit one step under body size through a token, the site name at the sans base; pinned by a browser test on the relation."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: make sure the header nav site name and tabs are appropriate sizes with respect to the main body text. We increased the body text, but maybe we should have increased the nav and tabs slightly. The tabs should be perhaps one notch smaller than the main text size, but not more than that. Measure the computed sizes of body text, the site name, the nav tabs and the Visualize sub-tabs at 1280, 768 and 390; set the tab size to one step below body on the type scale (a token, not a literal), and the site name in proportion; record the scale in paper-design.md; pin with a test.
