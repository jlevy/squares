---
type: is
id: is-01m5dtv8afzsphrcm2cbscsz6b
title: adopt_houses prints grid run dirs with a dot that the regularized index schema rejects (#699 B5)
kind: bug
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-10-20T23:37:48.111Z
updated_at: 2026-10-20T23:37:48.111Z
---
Review B5 of #699: adopt_houses.py:3218-3220 prints grid run directory names like -grid-0.5, which the index schema ^[a-z0-9-]+$ rejects, so each pass renames by hand. Fix the printed names (e.g. -grid-0p5) and test.
