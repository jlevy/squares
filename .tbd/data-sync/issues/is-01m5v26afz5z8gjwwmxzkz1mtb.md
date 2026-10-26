---
type: is
id: is-01m5v26afz5z8gjwwmxzkz1mtb
title: "Decide maximusrufus's T-154 rebuild (#565, openai-math-replays c01398b) for C3: retain its receipts if the owner accepts it"
kind: task
status: open
priority: 3
version: 1
delegate: w-records-1026
labels:
  - result-import
dependencies: []
created_at: 2026-10-26T02:56:18.430Z
updated_at: 2026-10-26T02:56:18.430Z
---
maximusrufus's comment on #565 of 2026-10-25T00:25:01Z (issuecomment-6391388887) offers a rebuild of T-154 (ofitzharding/sq17-lean v1.0.0 at 0a7167e) on a second machine as the complete build beyond the producer's that C3 asks for. Receipts: maximusrufus/openai-math-replays at c01398bf897d8688673b0eaac1284aa670607cf8, sq17-rebuild/ (BUILD.txt, Square17Optimality.log, HalfPlanePositiveControl.log, HalfPlaneBoundaryControl.log, module_log_count.txt, SHA256SUMS; the repository is dual-licensed, MIT for code, SHA256SUMS included). The comment reports exit 0 after 22,277 s, 4,951 module logs, REPRODUCTION_ACCEPTED, the final axiom log's SHA-256 5e74c4af...c241 equal to the source receipt's final_log_sha256, and both control logs equal to clean-build-receipt.json's. It shares the producer's source, toolchain, Mathlib cache and certificates; it does not check the certificates separately.

Recorded read-only in #565's requests entry by think-p7cq (PR of 26 October): read_through and a notes paragraph; no evidence entry, T-154 unchanged at V3/C1, the owner's hold unchanged.

The decision is the owner's: whether a retained third-party rebuild with byte-identical logs is the complete execution beyond the producer that C3 asks for (T-154's next_rung). If yes: retain the six receipts at c01398b under their licence (check the non-code licence for the logs), add an evidence entry naming the build, and move T-154 to C3 in a change the owner's reply to #565 then reports. The reply to #565 stays reserved to the owner (think-mxhc).
