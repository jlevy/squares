---
type: is
id: is-01m1qcy7m9dkmydk609475d33y
title: "Certificate page: inline math is 1.21× the text — size it to the faces it sits in"
kind: task
status: closed
priority: 2
version: 2
labels:
  - explainer
  - pr-79
dependencies: []
parent_id: is-01m1q0p63s2evef5mhkyn16e41
created_at: 2026-09-04T23:44:22.664Z
updated_at: 2026-09-04T23:45:37.907Z
closed_at: 2026-09-04T23:45:37.906Z
close_reason: Commit 4f504ed9.
resolution: null
duplicate_of: null
---
Review feedback on PR #79. KaTeX's stylesheet sets math at 1.21em of the surrounding text, tuned for Times-like faces; against PT Serif, and inside the small sans labels, every formula reads too large. Prose math 1.05em, sans-context math 1em, display equations 1.1em.
