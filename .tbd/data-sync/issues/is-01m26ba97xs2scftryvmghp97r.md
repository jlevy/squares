---
type: is
id: is-01m26ba97xs2scftryvmghp97r
title: The PDF reproduction check validates a fresh pair, not the artifact it ships
kind: task
status: closed
priority: 2
version: 5
labels: []
dependencies: []
parent_id: is-01m2cge1zdgenaswpf8nmd9fmv
created_at: 2026-09-10T19:04:36.861Z
updated_at: 2026-09-13T07:07:21.751Z
closed_at: 2026-09-13T07:07:21.749Z
close_reason: Implemented and independently reviewed in PR149 8d0a3ff2, inherited unchanged by PR156 52e4ab65. Exact stored PDF bytes and source receipt are validated; visible raw TeX, queued math and render errors are refused before export; live PDF receipts bind to fetched HTML. All six real browser controls and final artifact checks pass in both final-head Pages workflows (34743959872 and 34743978490). Full affected local gates and final hosted packing checks pass. Raw mismatch evidence is uploaded with seven-day retention; download before rerunning because GitHub can discard earlier-attempt artifacts. The intermittent PDF root cause remains separate under think-ptit.
resolution: null
duplicate_of: null
---
The previous Pages workflow first wrote publication artifact A with --update, then validated unrelated fresh draws B and C using --check. Agreement of B and C did not validate A. The implemented contract is a separate --check-artifact mode requiring existing A, comparing its full normalized bytes including the current HTML receipt against a fresh draw, applying font and pagination guards to A, and uploading A unchanged. Fresh --check remains available for diagnosis. Optional diagnostics retain the actual raw pair and neutral difference report in a unique invocation directory. This closes the artifact-validation gap; it does not identify the cause of the intermittent disagreement tracked by think-ptit.
