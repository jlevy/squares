---
type: is
id: is-01m4r6fkp8vbvee03m5zykvkaq
title: "PR #518 A1: superseded reason names the intermediate house at 146, 153, 155, 207"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m4r6f9vstpx182qr6fmvagw8
created_at: 2026-10-12T13:57:51.944Z
updated_at: 2026-10-12T15:11:15.026Z
closed_at: 2026-10-12T15:11:15.026Z
close_reason: "Fixed on PR #518; dispositions: https://github.com/jlevy/squares/pull/518#issuecomment-6127052921 and #issuecomment-6127053342; head 43133a47d, CI green"
resolution: null
duplicate_of: null
---
Low. packing/frontier/source-coverage.yaml:5714,5720,5732,5750; packing/devtools/adopt_houses.py:815-817. coverage() re-points superseded_by but keeps the first pass's reason. Review A: https://github.com/jlevy/squares/pull/518#pullrequestreview-5490892444
