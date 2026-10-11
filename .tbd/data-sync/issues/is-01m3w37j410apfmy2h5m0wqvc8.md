---
type: is
id: is-01m3w37j410apfmy2h5m0wqvc8
title: Papers live under papers/ with simple slugs, in URLs and in the source
kind: task
status: closed
priority: 2
version: 7
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T16:02:18.368Z
updated_at: 2026-10-01T22:56:52.814Z
closed_at: 2026-10-01T22:56:52.808Z
close_reason: "jlevy/squares#284 merged 2026-10-01 (main eaa1a4b45): papers/n11-lower-bounds-explainer.{html,md,pdf} and papers/n11-optimality-review.{html,md,pdf}; six old pages forward with canonical links to the new addresses and four old files are kept as copies; 109 source files renamed to the slugs by repren; check_published_site checks the forwarders and has a local mode. Tutorial stays at tutorial.html (recommended)."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: 'for papers we should update the URLs to match the site: explainer.html -> papers/n11-lower-bounds.html; n11-optimality/t-060-explainer.html -> papers/n11-optimality-review.html. Papers should have those simple slug names internally and externally. Or we could make it n11-lower-bounds-explainer.html for consistency.' Slugs taken: papers/n11-lower-bounds-explainer.html and papers/n11-optimality-review.html (each slug says the case, the subject and the kind of paper). Externally: the published paths, with the Markdown and PDF beside each under the same slug, and the old URLs (explainer.html, n11-optimality/t-060-explainer.html and its index, .md, .pdf) forwarding so no inbound link breaks. Internally: the renderers, templates, stylesheets, Pages jobs, tests, the Paper records (overview_sections.PAPERS), SITE_PAGES, repo_links, check_published_site and every link in reader documents use the slug names. The tutorial's place (papers/tutorial.html?) is proposed, not assumed.

## Notes

jlevy/squares#284 opened 2026-10-01 (claude/paper-slugs). First hosted run failed 23 tests of test_native_parent_core_receipt: packing/pyproject.toml is a frozen proof input of the n = 11 native audit and the rename had edited its comments and a per-file lint entry; restored to main's bytes, with the exemption moved into the renamed test (637a7ec89).
