---
type: is
id: is-01m1z19m87hvmccrhawtpejwj3
title: Wait for a stable rotation button before the touch-check tap
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m1z0patm2bp8vk8h8ntk3gwe
created_at: 2026-09-07T22:54:48.570Z
updated_at: 2026-09-07T22:54:48.570Z
---
The full browser checker intermittently missed the initial Figure6 tap after a preceding real canvas swipe: one unchanged run failed and the next passed. Static audit shows the handler advances from19.6 to24.6 degrees synchronously; the harness uses raw screen coordinates after only two animation frames, allowing ongoing scrolling to invalidate the target. Use the existing Playwright native-button tap actionability checks for this assertion, preserve real CDP drag/swipe tests, and rerun focused tests and the full browser check.
