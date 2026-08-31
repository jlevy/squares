---
type: is
id: is-01m12y4vwnsqpm4se8xwqmy8dm
title: render_research_tables rewrites smart quotes in a document it regenerates
kind: bug
status: open
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m12zjr144a4kg6rnv1t0pm6n
created_at: 2026-08-28T01:01:02.741Z
updated_at: 2026-08-28T01:26:23.900Z
---
Running devtools/render_research_tables.py rewrites docs/project/research/research-2026-08-22-packing-11-unit-squares.md, replacing typographic quotes with straight ASCII ones inside generated table blocks -- 7 lines changed, e.g. 'the author's official publication page' and quoted paper titles. The change is cosmetic damage rather than content, it is invisible in the check step (which passes either way), and it silently attaches itself to any commit made after running the generator. Reverted twice by hand during one session. The generator should preserve the source's typography.
