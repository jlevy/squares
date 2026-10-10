---
type: is
id: is-01m4kbxna1xdmjd8nkka3wax60
title: "Import wand125: s(122) >= 563/50 by the mixed_n122_L1126 linear certificate, raising n = 122 to 126 (no issue)"
kind: task
status: open
priority: 2
version: 1
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
created_at: 2026-10-10T16:56:43.073Z
updated_at: 2026-10-10T16:56:43.073Z
---
Found by the 2026-10-10 evening reads (think-0nkn): wand125/square-packing a9f76c3 adds problems/square-lower-bounds/certificates/mixed_n122_L1126/, a linear certificate (502 points, 1,268 segments, 3 rectangles, mass 12199999/100000) on mixed_n101_L1028's 201-direction net (core 9977/10000, step 83/40000), checked by unified_linear_verify.cpp (SHA-256 0249726a..., V-wand125-unified-linear-verify-cpp, the T-080 route). Reports s(122) >= 563/50 = 11.26, hence s(N) >= 11.26 for N >= 122: above Green's reported 11.22928087555 at 122-125 and Nagamochi's 11.24695076595 at 126, and the verified Karakus strip bounds at 122-126; 127's 11.29563 stands. Data: square-lower-bounds-v1 asset certificates__mixed_n122_L1126.tar.gz (31,784,537 B, SHA-256 6443eae03c56dc99051965246dbf97f5f3540feb9c011eac96e6d094521f5deb). The author's full replay took 7 h 41 min at 3 workers (about 23 CPU-hours): stages 1-3 only; the replay waits for an owner budget. No issue reports it.
