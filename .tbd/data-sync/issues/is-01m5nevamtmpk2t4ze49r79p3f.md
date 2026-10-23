---
type: is
id: is-01m5nevamtmpk2t4ze49r79p3f
title: "Main red: test_site_ladders finds no ladder diagram on results.html (57 setup errors post-merge)"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-10-23T22:42:03.034Z
updated_at: 2026-10-23T22:42:03.034Z
---
Main's post-merge Packing validation (integration-suites) errors at setup on every test in packing/tests/test_site_ladders.py: the module fixture renders results.html and (found[width],) = results_page.evaluate(LADDERS) gets an empty list (ValueError: not enough values to unpack). Red at 7cd0a94bf and 77aba4c02 at least. Likely cause: the VERIFICATION block (overview_sections.verification_block, the one .site-ladders diagram) is now placed by devtools/templates/verification-article.md, not the results page (see 5f83d1e73), so the test should load the page that carries it. PR CI skips this browser suite. Not covered by PR #760, which fixes test_site_text_tokens and test_site_wide_blocks only. Found while verifying #762 post-merge; not worked.
