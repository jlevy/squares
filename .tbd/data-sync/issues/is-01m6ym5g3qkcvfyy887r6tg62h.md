---
type: is
id: is-01m6ym5g3qkcvfyy887r6tg62h
title: Record the test-cost cohort so suite shard 4 is not sitting at the 10% unrecorded guard
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-11-08T22:23:50.903Z
updated_at: 2026-11-08T22:23:50.903Z
---
From the senior review of PR #925 (N8). After moving test_s12_unnir_certificate.py to shard 3, shard 4 is at 21/210 = 10.0% unrecorded; the guard in devtools/suite_files.py:415 is <=, so the next unknown file hashed to shard 4 trips it. Record the cohort's costs.
