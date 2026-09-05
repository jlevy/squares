---
type: is
id: is-01m1qd2c9fwd6amvrxsraz7bnz
title: "kpress: footnotes at 0.9em compound under a larger base — use a token size"
kind: task
status: open
priority: 3
version: 1
labels:
  - kpress-upstream
dependencies: []
parent_id: is-01m1q3fmvn9py28rcm0q3jadvk
created_at: 2026-09-04T23:46:38.510Z
updated_at: 2026-09-04T23:46:38.510Z
---
Found building the certificate page (PR #79). .kpress-footnotes sets font-size: 0.9em, which lands at 14.4px under an 18px base while the small token is 17.1px. A token size (font-size-small) would keep footnotes in step with the rest of the ramp.
