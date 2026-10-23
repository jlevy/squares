---
type: is
id: is-01m5jb5xshmtmgffn3aw0t82h5
title: Bound Pages browser installation time to recover stalled apt downloads
kind: bug
status: open
priority: 2
version: 2
labels: []
dependencies:
  - type: blocks
    target: is-01m5kcfhfdmgfb03gn3drg43rc
created_at: 2026-10-22T17:40:12.719Z
updated_at: 2026-10-23T03:26:45.301Z
---
Pages Firefox font-loading job in .github/workflows/pages.yml stalled about57minutes in apt repository downloads before tests during PR727 run39815232525 attempt1. Cancellation and failed-only retry succeeded in19seconds for install, and final checks passed. Add an explicit step/job timeout and appropriate recovery policy without masking real test failures. Evidence https://github.com/jlevy/squares/actions/runs/39815232525 . Separate CI hardening follow-up; no change required for validated domain cutover.
