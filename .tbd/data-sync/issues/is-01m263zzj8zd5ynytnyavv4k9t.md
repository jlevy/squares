---
type: is
id: is-01m263zzj8zd5ynytnyavv4k9t
title: Capture a trace to an uploadable video file
kind: task
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-09-packing-strategies-as-a-shared-language.md
labels: []
dependencies: []
created_at: 2026-09-10T16:56:39.239Z
updated_at: 2026-09-11T05:23:01.692Z
---
Phase 4. Trace in, frames out at a declared size and frame rate, then an encoder, then a receipt naming the strategy documents and the record each step landed on. The end product is a file the owner can upload.

The capture cost is already measured on the v1 slideshow in the project's pinned headless browser: about 42 ms per frame at 1080p and 145 ms at 4K, with repeated captures of one instant byte-identical, which is what makes the export reproducible rather than merely repeatable. What is missing is the encode step and the receipt.

Must refuse to emit a frame from a guide phase without its label. Depends on the renderer-extraction bead.

## Notes

Substantially built by a different route than this bead assumed. devtools/capture_video.py drives the BUILT WORKBENCH PAGE in the pinned headless browser through its own clock (select/duration/seek), screenshots every frame at a declared size (1080p or 4K) and frame rate, encodes with ffmpeg to H.264 (yuv420p, even dimensions, so it actually plays), and writes a receipt beside the file: page digest, range, fps, size, and per step the record the step aimed at, what it reached, and whether it landed. Measured n=2..8 at 24fps: 476 frames, 19.8s, 1.2MB, 28s to capture and encode, all seven on the record.

Two parts of this bead remain, both because the workbench does not yet play a PackingStrategy document (think-883t): the receipt names records rather than strategy documents, and there is no guide-phase label guard because the workbench path has no guide phases. Close this only when 883t lands and the receipt names documents.
