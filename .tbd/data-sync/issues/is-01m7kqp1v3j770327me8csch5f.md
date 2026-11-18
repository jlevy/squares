---
type: is
id: is-01m7kqp1v3j770327me8csch5f
title: "Site agent: news.html story cards fold after first paint (layout shift about 0.4 of the screen at 390 px), filter bar appears late, and news-cards.js reads layout once per card; fix, then re-measure the budget"
kind: bug
status: open
priority: 2
version: 1
labels:
  - site
dependencies: []
created_at: 2026-11-17T03:09:22.147Z
updated_at: 2026-11-17T03:09:22.147Z
---
Owner, 17 November 2026: "Hand both to the site agent (Recommended)" (think-k8vt). Measured 24 October with devtools.measure_news_page (PR #788; review A https://github.com/jlevy/squares/pull/788#issuecomment-6381675002): CLS medians 0.399-0.410 at 390 px from news-cards.js folding the first visible card after first paint (refresh at news-cards.js:53-57, getBoundingClientRect at :95), a second shift of about 0.06 at 390 px from div.site-news consistent with news-filters.js:160 revealing the filter bar; longest task grows with visible cards (LayoutCount 31 / 81 / 105 at 319 KB / 1.0 MB / 1.3 MB); with news-cards.js removed the 1.3 MB page passes all four check_site_rendering limits. news-cards.js unchanged since. news.html is 415,223 bytes on 17 November against its 600,000 page budget (about 36 days at 5,093 bytes a day; the plan's 450,000 watch point about 7 days away). Done when: cards fold before first paint, the filter bar's space is reserved, the reads are batched, and measure_news_page load passes at today's size and at the projected sizes; then the budget raise (think-3oxz, think-lsam) resumes.
