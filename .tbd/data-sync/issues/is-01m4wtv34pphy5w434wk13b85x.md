---
type: is
id: is-01m4wtv34pphy5w434wk13b85x
title: Resolve four scheduled main test-time ceiling overruns without weakening assertions
kind: bug
status: in_progress
priority: 1
version: 32
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4vns6xeff13savsant84279
child_order_hints:
  - is-01m4wzs72rh8db5f4mp5y8w4wr
  - is-01m4x4c32d5wdje51ep66pbzmm
  - is-01m4x4c3gx5fggqnt3ha5v8gpw
  - is-01m4x5q04a41ca6rsj99gpd11d
  - is-01m4x9zbx706gftwnvmxgsnd0g
  - is-01m4xatk8zfjpdxv9kq2gv4yn1
  - is-01m4xes8ehmmxzpjctygnawq8h
  - is-01m4xjdycq4m3d047sdrdcfba9
  - is-01m4xjdytsg7x53t8pg6zja54b
  - is-01m4xjdz83t1r1pk7kcw3cvsaj
  - is-01m4xk1h2skppdp58y4zr0kvph
  - is-01m4yezgymfksx798467evpv4h
  - is-01m4yf4yff5se96qajm94jvwdy
  - is-01m4yf4ywh62ajt7cc9zfbcjcn
  - is-01m4yf4z92dxbp2k4amma0mrq3
  - is-01m4ygmjndn87kz50318csk62e
  - is-01m4zax62kbavpdkh7119vxj88
  - is-01m4zctkhz4k6pcptm7kjkw9pe
  - is-01m4zh3apr6q86jmjggvd08bhr
hold: null
hold_until: null
created_at: 2026-10-14T09:10:37.460Z
updated_at: 2026-10-15T10:26:04.830Z
started_at: 2026-10-14T10:03:10.224Z
---
Optional scheduled full integration run38536321398 at f73 passes functional tests but violates12s per-test ceiling for four nodes: site_forwarders no-script redirect13.08s; results_register full-part citations T15312.17s; overview_sections no-script canonical atlas20.10s; regularized_drawings edited-block check13.44s. Main push full gate and Pages deployment passed sameSHA. Diagnose full integration contention/cold-path cost, optimize or explicitly classify measured expensive cases while preserving assertions and meaningful CI coverage; avoid broad ceiling increases.

## Notes

Current origin/main d33de8b105f5b7a43646ad5fc2aa890894dbb50c is healthy: complete post-merge Packing run 38716865645 passed, including slow and exhaustive/regularized checks; Pages 38716865665 passed. Earlier identity defect 3e3j is closed upstream. This does not waive PR599's independently selected strict timing failure at remote e5a046b3d202551f56452b7ff5538273c0c29a45: enforced run 38665027001 exceeded all four suite walls and eight call ceilings. No timing cap, assertion or scientific obligation was relaxed. Local CI history, including rejected VE016 evidence, is preserved on codex/main-test-timing at 65aff4580.\n\nSmaller iteration delivery is prepared separately on codex/quick-push-selection, base d33, for gg64/ly7p: exact seven-file slice, 164 core tests and 44 selected CLI tests passed, Ruff/type checks clean, independent Astra senior review clear pending final pin. A new component-aware release-tool validation fix is being implemented under 8iml. Reader PR617 final e0633e233 preserves main v0.7.4/data6133 and cuts v0.7.5; all three final-head follow-up reviews clear, canonical edit 67 passed in 128.50s, focused release 103 passed/13 exhaustive deselected, combined News/date/native layout 146 passed. Current-head CI has no failures and remains pending. Do not claim full current-data local gate: earlier old-data full normal receipt had 10973 passes plus 12 geometry failures, corrected by restoring original meter width and passing all78 affected checks; old-data pool complement passed3 in838.09s. Receipts retained in primary .codex/regularization-closeout-evidence-2026-10-13/.\n\nVE016 native backend was rejected before timing for acceptance mismatches and restored; uebw contains the evidence. Remaining required-deep-selection architecture and baseline/refusal assurances nns5/7wpx remain open. After News delivery, land the narrow quick-push/fixture-colocation and component-owned cut checks without asserting the three-minute hosted target is achieved.
