---
type: is
id: is-01m2pgxt86adyh829125c0t4kh
title: The published page shows no link preview when shared on X
kind: bug
status: open
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels:
  - explainer
  - pages
dependencies: []
created_at: 2026-09-17T01:50:30.661Z
updated_at: 2026-09-17T02:00:30.712Z
---
Reported 2026-09-16: https://jlevy.github.io/squares/ sent in an X (Twitter) DM rendered no social card, although sharing worked previously. think-95aa (closed 2026-09-05) added the Open Graph and Twitter card set with the 1x atlas PNG as the share image, and noted X's 4096x4096 image cap. Determine whether the live head tags, the share image (URL, status, size, dimensions) or the generator regressed, find the regressing commit, fix it with a test on the generated head, and verify the deployed page with a Twitterbot fetch.

## Notes

2026-09-16 investigation (Claude sub-agent; details and scripts in .claude/worktrees/agent-a73d5c56b99cc0f5f/attic/og-regression/).
VERIFIED: the live head carries a complete, unchanged card set (og:type/site_name/title/description/url, og:image https://jlevy.github.io/squares/known-best-1-100-card.png with type/width 2400/height 1256/alt, twitter:card summary_large_image with twitter:title/description/image/image:alt, canonical). The image returns 200 image/png, 205,675 bytes, true 2400x1256. robots.txt is 404, there is no noindex, and Twitterbot gets identical HTML. The tags have not changed since 30279083 and 455f1731 (2026-09-05). The page itself grew from 1,098 KB when the card shipped (663ca37e) to 1,900 KB (e8508598, 09-08), then 2,725 KB at 171bba33 (merge of PR #135, math startup stability, 09-09), then 3,094 KB (f2e24e07, 09-13); live it is 3,172,118 bytes uncompressed and 1,066,676 gzipped. Content: 998 KB inlined woff2 (426 KB of it the same faces under two family names), ~1.35 MB math markup, 392 KB KaTeX JS. --prepare-math ships every formula once per reader font setting (+~1.18 MB).
INFERRED: X's crawler refuses responses over 2 MB ('the response is too large'), so 171bba33 is the likely regression. Unverified whether X counts the compressed bytes; if it does, size is not the cause. X caches a card for ~7 days, which fits 'it used to work'. A test: paste the URL into the X post composer, and share a known-good link in the same DM to rule out DM preview behaviour.
OPTIONS (owner decision, each trades something): de-duplicate the 426 KB of fonts (kpress change, not enough alone); serve fonts and KaTeX as separate files (~1.4 MB, breaks the self-contained offline page the tests require); stop shipping every font-setting variant of prepared math (~1.18 MB, layout shift or slower switch). A prepared guard (render_explainer.assert_card_crawlable, 2,000,000 UTF-8 bytes, plus 4 tests) sits uncommitted in that worktree; landing it fails Pages prepare until the page is under the limit, so land it with the size fix. Nit: explainer-shell.html still calls the card image portrait. Separately, the live page is stale because Pages has not deployed since 06:51Z on 09-16 (think-w7oy).
