---
type: is
id: is-01m5jn38xtd10xgdmshtkeat2w
title: "Home page News box: discreet significance filter at top right, default S5 if enough S5 items else S4+S5"
kind: task
status: open
priority: 0
version: 4
labels:
  - process
dependencies: []
parent_id: is-01m5jn336nm6erpp0ygedhgpva
created_at: 2026-10-22T20:33:31.577Z
updated_at: 2026-10-23T01:45:52.398Z
---
c-lane-home-recent-1022, branch claude/home-recently-added (also carries the 'Recently added' section). Epic think-s38d.

## Notes

2026-10-22 21:10Z (c-lane-home-recent-1022): pushed draft PR #736 (https://github.com/jlevy/squares/pull/736), head 313c19c1e (feat e77f13dc1 + merge of origin/main 59b1ec594, #729).
- Home News box: three newest News articles at its opening levels, under news.html's own significance filter in a compact form (render_changelog.news_significance_filter shared; news_filters(compact=True)), small and right-aligned above the cards.
- Opening levels decided at render time (news_highlights.default_levels): S5 alone where News holds >= 3 S5 articles, else S4+S5. Today: S5 (13 Oct, 13 Oct, 30 Sep); with T-194's S5 item it leads with 16 Oct (tested both ways).
- Box carries the newest 3 at each level (9 cards, 42,550 bytes), hidden outside the opening levels, kept hidden without scripts; news-filters.js preview mode (data-news-limit) shows the newest 3 matching and carries a changed choice to news.html as news-s on "All news" (data-news-carry).
- news.html byte-identical apart from the site.css and news-filters.js asset hashes.
- Local: news/changelog/publication tests 87 passed; homepage browser tests 8 passed (1280/390, light/dark, keyboard, no-JS); lint/type clean on changed files. Edit tier running; hosted CI pending.

2026-10-23 00:30Z (c-lane-home-recent-1022): #736 pushed at d2a5b5ce9 (merges of main cddc5843f #724/#733 and bfc04b659 #735). Hosted red at 313c19c1e fixed: papers' release impact (no-change record edcbb6c05, re-measured d2a5b5ce9: 67/68 byte-identical, explainer's varying span only), home heading count in test_overview, check_site_rendering counting math in the box's hidden cards (probe now skips `[data-news-limit] > .site-news-day[hidden]`). With #735's T-194 item the box opens on S5 and leads with T-194 (16 Oct), then T-154, T-153. render_changelog --check: 0 owed, 0 missing. Local: 585 + 46 tests passed; edit tier running.

2026-10-23 (c-lane-home-recent-1022): review A of #736 addressed at e07648d0e (dispositions https://github.com/jlevy/squares/pull/736#issuecomment-6355393026). Box rule now (A4, coordinator decision): S5 alone only while the three newest S5 articles fall within 30 days of the build's record reference day, else S4+S5; today S5 (16, 13, 13 Oct), switches 13 Nov. Compact filter keeps a visually hidden live count (A5); scale token in site.css (A6); render_news(selected) consistent (A7); "No news yet." (A8).
