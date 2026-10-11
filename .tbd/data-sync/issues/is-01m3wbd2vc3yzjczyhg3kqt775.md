---
type: is
id: is-01m3wbd2vc3yzjczyhg3kqt775
title: "Social cards: clean Open Graph and Twitter metadata on every page, with the hero graphic (n = 53) as the image"
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T18:25:07.941Z
updated_at: 2026-10-01T19:31:23.307Z
closed_at: 2026-10-01T19:31:23.305Z
close_reason: "06d8f93dc, fdc0958e8 on claude/site-polish-4-social, merged into jlevy/squares#276: render_overview.head_tags writes every page's title, description, canonical, Open Graph and Twitter tags; the card is the n = 53 hero at 1200x630 (social-card.png, built not committed); check_published_site checks heads and the card (4 of 21 pages passed before, 21 of 21 after)."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: 'we should fix the opengraph and other social media card info to be clean on all the pages on the site. we should use the hero graphic (n=53) as the social graph image'. Every page (KPress pages, both papers, the workbench, document pages, forwarders): og:title, og:description, og:type, og:url (the page's canonical URL), og:site_name 'The Square Packing Project', og:image with width, height and alt, twitter:card summary_large_image with title, description and image, a canonical link, and a meta description; one definition feeds all page kinds. The image is the homepage hero (the n = 53 packing) rendered to a 1200x630 PNG at build time from the committed drawing, served from the site at an absolute URL; checked by check_published_site.

## Notes

2026-10-01, branch claude/site-polish-4-social (worktree epistemics-ladder-impl), two commits on cdf216bd1, not pushed: 06d8f93dc feat(site) and fdc0958e8 docs. One function, render_overview.head_tags(PageMeta), writes title, description, canonical link, Open Graph and Twitter tags for every page kind: the 12 kpress pages (kpress's own four tags replaced), the explainer, the optimality paper and the workbench. Title is '<Page> · The Square Packing Project' (overview: the name alone); og:site_name is the formal name; og:type article for the two papers and the tutorial. Card: devtools.social_card draws the n = 53 hero at 1200x630 (43,633 bytes locally) with the project's name under it as outlines; built with the site, not committed; served as social-card.png at the root; preview_site writes it and the Pages overview job draws it into both renders and diffs them. check_published_site gained head checks (one of each tag, canonical = og:url = served address, formal name, unique descriptions within 160 characters, card is a 1200x630 PNG, forwarders name their target in full and carry no card) and --local DIR / --inventory; the overview job and preview_site run --local. Measured on a full local build: 4 of 21 head checks passed before, 21 of 21 after. Focused tests 703 passed, 5 skipped, 1 failed (test_overview status.html KeyError, already failing at cdf216bd1). --edit: 3 steps failed, none on lines this change touches (type floor test_overview.py:245 and test_site_result_columns.py:196; embedded JS in test_render_n11_optimality_explainer.py _TYPESET_ALL; math markup in review-2026-10-01-site-documentation-records.md). Open for the owner: the card with the name under the packing is what ships, the plain variant is one flag away; not added: theme-color, apple-touch-icon, noindex on forwarders, per-paper card images.
