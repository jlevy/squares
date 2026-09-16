---
type: is
id: is-01m2m6zqkgrbwg2j352gjpf6m6
title: "PR #180 review R3: make motion-lab identity evidence executable"
kind: bug
status: in_progress
priority: 1
version: 6
labels: []
dependencies: []
parent_id: is-01m2m6y4gw224dgrwf37bgqnhd
created_at: 2026-09-16T04:18:18.863Z
updated_at: 2026-09-16T07:18:55.859Z
closed_at: null
close_reason: null
resolution: null
duplicate_of: null
---
Store and check the deterministic 48-state motion-lab report and add a drawing-level invariant so a hidden canvas or wrong model fails. CI must invoke the report/golden path rather than relying on a one-time local sentence.

## Notes

Independent review at 7db71dd627ec4c544323f7948bd9f2e7c87e70b7 reproduced the residual failure with installed Google Chrome through the project Python 3.14 environment. Both labs' visible geometry was made fully transparent by CSS; devtools.check_motion_lab_pages still reported 'OK: exact lab drove 36 states and the general lab 12, with visible drawings matching the committed report'. Evidence points to packing/devtools/check_motion_lab_pages.py:85-90, 128-132, 189-198: inner_html is unaffected and locator.is_visible() does not reject opacity zero. Add a paint-level invariant (including ancestor opacity/display/visibility and nontransparent representative drawing marks, or an equally stable rendered-pixel check) and retain this exact mutant as the negative control.
