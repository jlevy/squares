---
type: is
id: is-01m3xgn80s0dd0t30ec7zs9k39
title: "CI: thirteen browser-backed site test files still skip on every pull request; give them a job of their own"
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-02T05:16:12.695Z
updated_at: 2026-10-02T05:16:12.695Z
---
From think-sib7 (jlevy/squares#300, D-513). The two pixel-pinned table files now run in the frontend job with a browser. The other thirteen browser-backed files (tests/test_site_glyphs.py, test_site_ladders.py, test_site_atlas_views.py and the rest of tests/test_site_*.py that launch Chromium) still sit in the behavioral shards, which install no Chromium, so they skip on every pull request and run only when main's validate job cannot reuse a PR tree. All fifteen cost 203 s serially on a Mac (90 s rendering the papers for test_site_glyphs.py) against the frontend tier's 150 s ceiling, so they need a job of their own, sized from hosted readings, with SQPACK_REQUIRE_CHROMIUM set so a missing browser fails. They also still launch with the shell's default hinting; move them to tests/site_browser.launch and expect some pins to need re-reading on Linux. OR-13: every fast check runs in CI. Also watch the frontend tier's wall with its fourth step: 93.2 s and 119.9 s read against a 104.7 s record and a 150 s ceiling.
