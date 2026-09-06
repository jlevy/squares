---
type: is
id: is-01m1w1wzkgb0rjz15kr2xm20h1
title: "PR #98 review R3: integrated-fast checkpoint tarball is half AppleDouble ._ files and has no manifest"
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m1w1w81t7vmr0gem6d91wg8b
created_at: 2026-09-06T19:07:39.504Z
updated_at: 2026-09-06T19:36:33.933Z
closed_at: 2026-09-06T19:36:33.933Z
close_reason: "Fixed: devtools.checkpoint_manifest packs deterministic archives without macOS metadata and checks SHA-256 manifests; integrated-fast archive repacked (820 -> 409 entries) with a manifest; both manifests drift-checked by test_checkpoint_manifest."
resolution: null
duplicate_of: null
---
packing/benchmarks/validation-efficiency/checkpoints/2026-09-06-integrated-fast.tar.gz: 410 of 820 entries are ._* resource forks. Fix: repack without them, add a SHA-256 manifest like the pre-main archive, keep session-088 links valid.
