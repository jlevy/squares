---
type: is
id: is-01m68ffpy9g2gmc0w2d1nk881n
title: Scale result/t-046.html so a result at one of its counts is not a page-ceiling raise
kind: task
status: open
priority: 3
version: 1
labels:
  - site
dependencies: []
created_at: 2026-10-31T07:58:45.192Z
updated_at: 2026-10-31T07:58:45.192Z
---
Review A on #851 (finding A6) accepted the raise of result/t-046.html's ceiling from 400,000 to 450,000 bytes (packing/devtools/site_urls.py, measured 401,561 with T-252 listed), but noted the growth is structural: the page lists every register result at T-046's 48 counts, about 1.5 KB each, and grew from 355,078 bytes on 7 October to 401,561 on 31 October, so 450,000 lasts weeks. Decide how the page scales, for example by collapsing superseded rows or fetching the history on demand, so the next raise is a decision rather than a reflex. Done when the page's size no longer grows with every result at those counts, or a measured reason for the growth is recorded with the next ceiling.
