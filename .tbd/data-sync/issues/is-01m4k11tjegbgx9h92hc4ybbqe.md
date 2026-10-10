---
type: is
id: is-01m4k11tjegbgx9h92hc4ybbqe
title: Move the per-author upper-bound report modules onto devtools.upper_bound_reports declarations, then retire them
kind: task
status: open
priority: 3
version: 1
labels:
  - packing
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
created_at: 2026-10-10T13:46:45.198Z
updated_at: 2026-10-10T13:46:45.198Z
---
OR-1 follow-up to think-md2i. devtools.upper_bound_reports (2026-10-10) does from a packet's acquisition/report.json what couzo_followup_reports, couzo_refinement_reports, evand_hunt_reports, gupta_refinement_reports and ryxu_arrangement_reports each do by hand. Port each retained packet's facts to a report.json declaration, show check --replay reproduces every retained receipt byte for byte (or row for row), repoint the register artifacts and controls, then retire the old modules and their tests. Relates to think-3jsj (one packet contract).
