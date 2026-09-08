---
type: is
id: is-01m1zzssc6t2mn96vsjt7cn7xz
title: Exercise math rendering guards when checker files change
kind: bug
status: in_progress
priority: 2
version: 5
labels: []
dependencies:
  - type: blocks
    target: is-01m1zzjddp742vysds0fzm3fe8
parent_id: is-01m1zzjddp742vysds0fzm3fe8
created_at: 2026-09-08T07:47:55.397Z
updated_at: 2026-09-08T08:43:20.146Z
---
PR128 adds check_math_faces to pages build but omits its own path from push and PR triggers. Extend filter contract so changing browser gates invokes them. Expand first-visible-math guard beyond Main/Math families, and cover print plus dynamic rerendering.

## Notes

Added delayed-font tests plus real negative browser fixtures for early paint, dropped early inputs, and clipped no-JavaScript fallback. Final local Chromium/Firefox/WebKit checks pass. Dedicated KPress browser CI exposed integer-pixel font hinting in existing probes; shared 4096px measurement preserves strict .001em discrimination while actual layout/accents/size checks stay at normal size. Fix is in KPress PR59.
