---
type: is
id: is-01m263zzj8zd5ynytnyavv4k9t
title: Capture a trace to an uploadable video file
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-09-packing-strategies-as-a-shared-language.md
labels: []
dependencies: []
created_at: 2026-09-10T16:56:39.239Z
updated_at: 2026-09-10T16:56:39.239Z
---
Phase 4. Trace in, frames out at a declared size and frame rate, then an encoder, then a receipt naming the strategy documents and the record each step landed on. The end product is a file the owner can upload.

The capture cost is already measured on the v1 slideshow in the project's pinned headless browser: about 42 ms per frame at 1080p and 145 ms at 4K, with repeated captures of one instant byte-identical, which is what makes the export reproducible rather than merely repeatable. What is missing is the encode step and the receipt.

Must refuse to emit a frame from a guide phase without its label. Depends on the renderer-extraction bead.
