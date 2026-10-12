---
type: is
id: is-01m4r6fkp8vbvee03m5zykvkaq
title: "PR #518 A1: superseded reason names the intermediate house at 146, 153, 155, 207"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m4r6f9vstpx182qr6fmvagw8
created_at: 2026-10-12T13:57:51.944Z
updated_at: 2026-10-12T13:57:51.944Z
---
Low. packing/frontier/source-coverage.yaml:5714,5720,5732,5750; packing/devtools/adopt_houses.py:815-817. coverage() re-points superseded_by but keeps the first pass's reason. Review A: https://github.com/jlevy/squares/pull/518#pullrequestreview-5490892444
