---
type: is
id: is-01m5wd7p93qr0922cjr4jvsnyt
title: "Recently Added: the owner's shorter introduction"
kind: task
status: in_progress
priority: 2
version: 3
delegate: claude-code@vm
labels: []
dependencies:
  - type: blocks
    target: is-01m5wd7re80yjz5wacnp5fqzy5
parent_id: is-01m5wd6833v6wx316fc361515a
hold: null
hold_until: null
created_at: 2026-10-26T15:28:32.034Z
updated_at: 2026-10-26T15:28:58.805Z
started_at: 2026-10-26T15:28:58.805Z
---
`devtools/templates/overview-article.md`, the paragraph under Recently Added, reads:

> Everything that reached this site over {{RECENT_SPAN}}, newest first: each result at
> any significance, each count whose house best packing moved, and the dated bounds
> recorded beyond $n = {{CORPUS_END}}$. [All Results](results.html#all-results) lists
> every result; [News](news.html) has the stories rated S3 and above.

The owner's wording, 26 October 2026:

> A log of all results recorded by the Squares Project since <date>. For major items
> only, see News.

So the section names the day its window opens rather than a span, which wants a
`recent_since` beside `recent_span` in `overview_sections.py` (the oldest day shown, as
`recent_span` reads it), and `render_overview.overview_page` passes it. `RECENT_SPAN`
and `CORPUS_END` lose their last readers on this page; drop whichever becomes unused.

`test_home_recent.py` and `test_overview.py` hold the current sentence.
