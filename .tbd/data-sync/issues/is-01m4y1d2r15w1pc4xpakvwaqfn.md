---
type: is
id: is-01m4y1d2r15w1pc4xpakvwaqfn
title: Investigate noisy Workbench trajectory timing during concurrent frontend validation
kind: bug
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
labels: []
dependencies: []
parent_id: is-01m4xkf4v65pthd9zbd7a5a3qv
created_at: 2026-10-14T20:24:32.768Z
updated_at: 2026-10-14T20:24:32.768Z
---
PR604 ffca9c19 Packing38630350596 frontend116080088219:424site cases pass, Workbench trajectory n324 bodies412.2ms versus400ms ceiling (1,807,280bytes under4MB). Mathematical/animation source unchanged by604; previous296cohortWorkbenchpassed. Preserve failedreceipt news604-hosted-frontend-ffca.log. One failed-job-only rerun atsamehead authorized; no thresholdchange or assertionremoval. Investigate measurement isolation/avoidableallocation with sameconfiguration evidence, not assume runner noise proves no regression.
