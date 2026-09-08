---
type: is
id: is-01m1tqpsewv8zcny1tkem9gv1w
title: "D3: the Markdown edition's credits run together, figure-only captions describe what it cannot show, Figure 3's preposition"
kind: bug
status: in_progress
priority: 2
version: 2
labels:
  - review-claude
dependencies: []
parent_id: is-01m1tqpgrh5ym0r6e5apbke7p8
created_at: 2026-09-06T06:50:16.411Z
updated_at: 2026-09-06T06:50:23.665Z
---
render_explainer.py's Markdown conversion looks for '<div class="credits">' while the template emits 'class="credits centred"', so the credits fall through to the paragraph flattener as one line (coordinator fixes the regex to class="credits[^"]*" and adds a lead clause to each caption whose figure the edition strips, e.g. 'On the page, Figure 6 draws ...'). Template half for the prose agent: Figure 3's 'Below 381/100 it is 0.0670835... wide' uses the wrong preposition for a gap above the bound; 'With the lower bound at 381/100 the gap is 0.0670835... wide, down from 0.0882292... at Stromquist's bound.'
