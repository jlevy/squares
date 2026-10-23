---
type: is
id: is-01m504m9vnya2jnvwddcsjbttp
title: Measure and remove repeated canonical fixture rendering in frontend CI
kind: task
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
labels: []
dependencies:
  - type: blocks
    target: is-01m5kcfhfdmgfb03gn3drg43rc
parent_id: is-01m4xkf4v65pthd9zbd7a5a3qv
created_at: 2026-10-15T15:59:24.021Z
updated_at: 2026-10-23T03:26:45.290Z
---
Astra diagnosis of ordinary38756777827: frontend540s, setup106s including71scheckout; layout426.51s (425pass6skip391.22s plus4serialloadcases33.91s). Existing site_renders cache is per xdist process, repeating canonical renders and full record admissions. First measure cold render cost separately from browser setup using a retained native tool. Only implement invocation-local fixture preparation if the removable cost is material. Acceptance: three alternating uncontended comparisons including preparation, at least30s AND10percent inclusive wall reduction, no extra worker/job/persistent cache/proof protocol, excessive fixture storage, new skips, changed nodes or weaker viewport/theme/mutation/load-budget assertions. Keep private mutable copies/browser contexts and fresh reads on the next invocation. Count local selector fan-out cost (six-file correction selected126files and took662.57s). Candidate is not measured or accepted; no held witnessVE017 execution.
