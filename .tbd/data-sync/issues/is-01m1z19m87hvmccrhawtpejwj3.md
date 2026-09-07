---
type: is
id: is-01m1z19m87hvmccrhawtpejwj3
title: Wait for a stable rotation button before the touch-check tap
kind: bug
status: in_progress
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m1z0patm2bp8vk8h8ntk3gwe
created_at: 2026-09-07T22:54:48.570Z
updated_at: 2026-09-07T22:58:09.295Z
---
The full browser checker intermittently missed the initial Figure6 tap after a preceding real canvas swipe: one unchanged run failed and the next passed. Static audit shows the handler advances from19.6 to24.6 degrees synchronously; the harness uses raw screen coordinates after only two animation frames, allowing ongoing scrolling to invalidate the target. Use the existing Playwright native-button tap actionability checks for this assertion, preserve real CDP drag/swipe tests, and rerun focused tests and the full browser check.

## Notes

Replaced only the handle tap assertion with Playwright Locator.tap(), which waits for actionability and scrolls into view; existing CDP drag/swipe coverage remains. Focused checker tests passed 27/27 in 1.35 seconds and Ruff passed. The raw-coordinate/scrolling race is a likely explanation for the intermittent failure, not an established root cause. Combined browser revalidation pending with the final box edit.
