---
type: is
id: is-01m4kwdbnpyegmq64y1swnqs95
title: "check_motion_lab_pages: honour the browser executable override the other site tools read"
kind: bug
status: open
priority: 3
version: 1
labels:
  - tooling
dependencies: []
created_at: 2026-10-10T21:44:54.709Z
updated_at: 2026-10-10T21:44:54.709Z
---
devtools.check_motion_lab_pages calls playwright's chromium.launch() with no executable override, so in a container whose installed Chromium build differs from the pinned Playwright's (2026-10-10 remote session: /opt/pw-browsers holds chromium_headless_shell-1194, Playwright 1.62.0 wants -1234) the fast tier's "workbench browser behaviour in Chromium" step cannot run locally. Every other browser tool reads SQUARES_BROWSER_EXECUTABLE or SQPACK_CHROMIUM (devtools/preview_site.launch_chromium).

Fix: launch through the same override (preview_site.launch_chromium or SQUARES_BROWSER_EXECUTABLE), with a test that the override is honoured. Found by lane L28 of the 2026-10-10 intake pass.
