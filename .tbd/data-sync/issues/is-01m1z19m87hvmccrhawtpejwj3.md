---
type: is
id: is-01m1z19m87hvmccrhawtpejwj3
title: Wait for a stable rotation button before the touch-check tap
kind: bug
status: closed
priority: 2
version: 4
labels: []
dependencies: []
parent_id: is-01m1z0patm2bp8vk8h8ntk3gwe
created_at: 2026-09-07T22:54:48.570Z
updated_at: 2026-09-07T23:41:58.712Z
closed_at: 2026-09-07T23:41:58.712Z
close_reason: "Completed in PR #117 at 83a2e6f3. All required hosted checks and the paper build passed; the timing-only CI failure passed one unchanged-commit retry. Three agent reviews and root review accepted the work. HTML, Markdown and the 17-page PDF were rebuilt; the web preview and Preview PDF were opened. The latest upstream deployment also passed all 26 live-site checks. Separate selector issue think-oe1g remains open."
resolution: null
duplicate_of: null
---
The full browser checker intermittently missed the initial Figure6 tap after a preceding real canvas swipe: one unchanged run failed and the next passed. Static audit shows the handler advances from19.6 to24.6 degrees synchronously; the harness uses raw screen coordinates after only two animation frames, allowing ongoing scrolling to invalidate the target. Use the existing Playwright native-button tap actionability checks for this assertion, preserve real CDP drag/swipe tests, and rerun focused tests and the full browser check.

## Notes

The checker now uses Playwright Locator.tap() for the native rotation button, waiting for actionability and scrolling into view; existing real CDP drag/swipe coverage remains. A raw-coordinate/scrolling race is a likely explanation for the earlier intermittent miss, not an established root cause. The merged checker passed 32 focused tests, Ruff and BasedPyright; the final combined Chromium check passed for both figures and both certificates on desktop and phone layouts. Independent code review accepted the narrow change. Included in PR #117 at 83a2e6f3.
