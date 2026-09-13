---
type: is
id: is-01m2chahf57z4w9tj5gehbs0td
title: Consolidate the workbench into a standalone package after cleanup
kind: epic
status: open
priority: 1
version: 13
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies:
  - type: blocks
    target: is-01m2b7nakccj4tf1tgs4k86nar
  - type: blocks
    target: is-01m2chakgrn8keadss1jcs401b
parent_id: is-01m28p7h39vcykq99dgjmvwv98
child_order_hints:
  - is-01m28p88qyq83eek30pja3np54
  - is-01m229an1fw0az9jgk0wcbg8c4
  - is-01m2ckzwew659djys62jdwq0fc
  - is-01m2ckzwx4cbwvs1ewec005c2k
  - is-01m2ckzxahng9d3m19w6bp5hfa
  - is-01m26vyt1neawsx8w6t295mwft
  - is-01m24pase6ebcw856v6d8mbvnk
created_at: 2026-09-13T04:45:03.321Z
updated_at: 2026-09-13T05:42:43.489Z
---
Phase 3 live-package consolidation under the governing workbench plan, after the small package shell (think-l9z0) and repair checkpoint (think-109t). Explicit children: think-nubm kernel; think-w0a1 data; think-ywj4 timeline/view/capture; think-6qxx mechanism registry; think-883t trace UI; think-tcns headless benchmark; think-g0lh final app/tool/build consumer migration. Related mode/start adapters are think-8cti and think-rdee. Parent dependencies do not gate children: each executable task has explicit prerequisites. Acceptance: standalone strict package commands, browser/Node parity, solver-free illustrations, versioned data, complete root-source discovery and deterministic Pages artifact. Deletion follows via think-cqfc; arbitrary-n Pack and final release/experimental Search have their own downstream acceptance tasks.

## Notes

All newly introduced workbench-specific files during the preceding repair phases also start in top-level packages/workbench with immediate lint/type/test discovery. Existing live files may receive narrow in-place repairs. The later package phase completes consolidation; it does not permit new scattered devtools or spike modules in the meantime.
