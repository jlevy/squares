---
type: is
id: is-01m3txgjsa4b3pyzjc75jsns6z
title: "Rung chips: saturation rises with the level, least at V0 and most at the top"
kind: task
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T05:03:08.071Z
updated_at: 2026-10-01T07:14:56.451Z
closed_at: 2026-10-01T07:14:56.449Z
close_reason: Done in 8accdd328 on claude/overview-page-impl (jlevy/squares#255, pushed at 158820d9d); checked in the built site on 2026-10-01. Fill is oklch(base + step x level, chroma rising with level) per ladder; contrast at least 6.0:1 light and 5.3:1 dark; S stays gray and darkens (the owner may give it a hue); devtools.rung_scale and tests/test_rung_scale.py.
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: on the chips for the rung ladders, the lower values should be less saturated at the bottom, for example V0, and more saturated near the top. One scale per ladder (V blue, C green, S gray, think-7jo7): saturation and strength increase monotonically from rung 0 to the top rung, in light and dark themes, with text contrast kept at every step; applied wherever a rung chip or rubric card prints a level; documented in paper-design.md with the measured values.
