---
type: is
id: is-01m4che48vje14earfhcfasx0r
title: Keep stacked import validation in each checkout’s own Python environment
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m4cb68shtz5h0braprdqj1qb
created_at: 2026-10-08T01:18:24.539Z
updated_at: 2026-10-08T01:18:24.539Z
---
A required lower3345 selected push attempt loaded sqpack/devtools from lower via PYTHONPATH but workbench_tools from upper mainvenv editable install; three workbench tests visibly failed before cancellation130. Fix uses absolute lowerpacking/.venv Python3.14.7 and ownvenvPATH from lowerpacking cwd, with allsqpack/devtools/workbench_tools/kpress file/root probes retained. Metadata97PASS remains scoped to sameexacthead; identical173selected-file behavioralcommand reruns under correctlower environment with native4worker ordinary+serialheavy and unchanged900s allowance. Upper ownenvironment modulecensus also passes. No source/assertion/cap change; sourcepush/closure only after actualaffectedbehavior completion. Preserve all originalfailed/cancelledreceipts and record resolution on bothPRs/native.
