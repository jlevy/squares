---
type: is
id: is-01m495xvv5wq8p22vqds3ajqc2
title: "Import wand125/square-packing-bounds 2fad66e..f8e0178: four more check2 certificates (s(31) >= 597/100; s(19) >= 1931/400, s(28) >= 287/50 and s(29) >= 1163/200 raising T-109, T-113 and T-114)"
kind: task
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m482krnapg9vxqd91zjrg171
created_at: 2026-10-06T17:59:33.988Z
updated_at: 2026-10-06T18:59:32.475Z
closed_at: 2026-10-06T18:59:32.470Z
close_reason: duplicate of think-dc0p (same four wand125 commits past 2fad66e)
resolution: null
duplicate_of: null
---
Lane R7 (think-yrdj) stopped at its pin 2fad66e as briefed. At 2026-10-06T18:05Z the head was f8e0178, four commits past it, each a check2 bundle on a declared net: ec799b7 (08:41:42Z) mixed_n31_L597, s(31) >= 597/100 = 5.97; 953bfa4 (09:15:52Z) s(19) >= 1931/400 = 4.8275, above T-109's 193/40; 80c7ab6 (11:02:30Z) s(28) >= 287/50 = 5.74, above T-113's 1147/200; f8e0178 (11:55:11Z) s(29) >= 1163/200 = 5.815, above T-114's 581/100. 73 files changed. The R7 tooling (audit_wand125_declared_net check2 audit, bundle, compare-census, cpp-sample; the census route at sqverify-fast d97758bb) applies; UNPUBLISHED_RUN_INPUTS will need each new run log's input digest checked. Not read beyond the commit list and diffstat.
