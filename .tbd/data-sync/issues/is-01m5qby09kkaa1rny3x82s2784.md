---
type: is
id: is-01m5qby09kkaa1rny3x82s2784
title: "Rebuild #678's Göbel receipt to its writer's families sentence (PR #793 A13)"
kind: bug
status: closed
priority: 3
version: 2
spec_path: docs/project/specs/active/plan-2026-10-24-rows-above-1024.md
labels:
  - result-import
dependencies: []
parent_id: is-01m5kjb20ed6wb6c1zbp2my2xc
created_at: 2026-10-24T16:29:33.875Z
updated_at: 2026-10-31T06:36:54.949Z
closed_at: 2026-10-31T06:36:54.949Z
close_reason: "Done in jlevy/squares#835 (merged 2026-10-31, 32ef0861b): #678's Göbel receipt rebuilt and held byte for byte by check."
resolution: null
duplicate_of: null
---
PR #793 review A, A13 (https://github.com/jlevy/squares/pull/793#issuecomment-6386210280). At main 2ec489d1e, packing/resources/web/couzo-issue678-2026-10-18/receipts/goebel-comparison.json does not rebuild byte for byte: devtools.couzo_678_replay goebel writes families 'Göbel squares, Göbel strips and corner-touching strips, with deletion', and the committed file says '... corner-touching Göbel strips ...'. The comparison itself is unchanged. Fix in a records slice: rerun 'python -m devtools.couzo_678_replay goebel' from packing/ and commit the one-line change, or change the writer's sentence to the committed one; then add the receipt to a byte-for-byte rebuild check so the drift cannot recur. Found by the W7 regression control (c-w7-1024).
