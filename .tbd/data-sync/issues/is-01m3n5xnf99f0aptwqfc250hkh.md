---
type: is
id: is-01m3n5xnf99f0aptwqfc250hkh
title: "n = 50: review and replay wand125's own-verifier certificates, s(50) >= 7.35 and mixed_n50_L740 at 37/5"
kind: task
status: closed
priority: 1
version: 6
labels:
  - packing
  - wand125-update
  - review
  - soundness
dependencies:
  - type: blocks
    target: is-01m3n5y05cdnsnkspf7e4vg5jp
parent_id: is-01m3n5wh72rsqd2z97m8v1vv4q
created_at: 2026-09-28T23:34:38.825Z
updated_at: 2026-10-12T23:39:29.725Z
closed_at: 2026-10-12T23:39:29.725Z
close_reason: "Completed: wand125's s(50) >= 37/5 reviewed and replayed in full; T-048 at V3/C3 in c03c6d4fb."
resolution: null
duplicate_of: null
---
Two claims beyond Tokoharu's verifier format (packing/resources/web/wand125-x-update-2026-09-28/supplied-messages.txt): 7.35, whose coverage reaches 1.0000000005 below verify.cpp's required 1.0001 margin, so it ships with its own verifier and a full replay bundle; and 7.40 (certificates/mixed_n50_L740), from bringing Green's N = k^2 + 1 approach into the search, about 0.083 above Green's 7.317426 (the register's reported bound, [Friedman DS7]). New trust boundary: review the custom verifier's soundness (outward rounding, what the margin is for, whether coverage >= 1 is decided rigorously) and the mixed certificate language before any replay counts; then replay in full. Overlaps think-pr2b (BC-394's own n = 50 and n = 82 ladders); wand125 names n = 65 (Green 8.2900) and n = 82 (Green 9.2667) as its next targets.

## Notes

Complete local replay PASSED 2026-09-29 06:54Z (ALL_ANGLES_VERIFIED_AND_REPLAYED, FULL_REPLAY_MATCHES_SHIPPED); receipts on transfer branch claude/replay-wand125-n50-l740-local. Remaining: evidence entry, n-050 verified 37/5, monotone 51-53, T-048 to V4/C3 on #243, re-pin.
