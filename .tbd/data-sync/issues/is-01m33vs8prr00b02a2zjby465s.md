---
type: is
id: is-01m33vs8prr00b02a2zjby465s
title: Re-cut both ascent videos at 60 fps from the reviewed page, and measure their cadence and fidelity
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-21-video-delivery-profiles.md
labels: []
dependencies:
  - type: blocks
    target: is-01m33vv5xk9qcb634kg55zsnp3
parent_id: is-01m1z68hzazv9yjs9k7cddmf82
created_at: 2026-09-22T06:10:23.564Z
updated_at: 2026-09-22T16:42:43.864Z
closed_at: 2026-09-22T16:42:43.863Z
close_reason: "Both cuts made from 17dcb3f92 at 60 fps on the external drive (/Volumes/spud-ext1/squares-video/out/2026-09-21-17dcb3f/): 1..100 under social, 9,579 frames, 159.65 s, 43.8 MB; 1..324 under archive, 33,626 frames, 560.43 s, 239.2 MB. Both conform; fidelity 47.9 to 51.4 dB PSNR, SSIM 0.998 to 0.999; clock exact to 0.7 us. Cadence measured by the new squares-workbench-check-cadence; the one-frame playback holds it found are think-dh9j. Recorded in the spec at the commit that follows 17dcb3f92."
resolution: null
duplicate_of: null
---
Phase 2 of the delivery-profile plan, from the committed page at 17dcb3f92 after the owner's review: n = 1..100 under social and n = 1..324 under archive, 1080p60, frames kept on the external drive (/Volumes/spud-ext1/squares-video). Beyond conformance, which every capture checks, measure what the owner asked for (2026-09-21): that the motion is smooth at 60 fps, with no repeated or skipped frame inside motion, and that the encode is high quality against the page's own frames (PSNR and SSIM over declared windows). Record both in the spec. No media enters the repository, and nothing is published without the owner's review.
