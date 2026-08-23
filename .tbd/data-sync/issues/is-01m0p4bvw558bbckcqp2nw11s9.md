---
type: is
id: is-01m0p4bvw558bbckcqp2nw11s9
title: "H-011: census the n<=10 landscape to saturation"
kind: task
status: open
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0p4bvjsw40qb2e41ycygyqr
created_at: 2026-08-23T01:39:35.941Z
updated_at: 2026-08-23T01:41:06.358Z
---
Multistart + LP quench + canonical dedup at n=5..10; ship the atlas with its discovery curves. Runs on existing Python plus the validated LP - no Rust required, which is why it can start early. Kill: no plateau by n=8 within tier S; enumeration will not scale to 11 and the fallback is coverage estimation over descriptor space (H-007).
