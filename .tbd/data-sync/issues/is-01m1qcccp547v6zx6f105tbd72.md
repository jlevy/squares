---
type: is
id: is-01m1qcccp547v6zx6f105tbd72
title: "F3 and F4: the self-contained package is not a third-party check, and declared minima govern acceptance"
kind: task
status: in_progress
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01m1qcc9devr6mz0m6erxswxjc
created_at: 2026-09-04T23:34:38.021Z
updated_at: 2026-09-05T00:53:23.097Z
---
F3 and F4 from PR 80. F3: 'Third-Party Check' overstates what a self-contained package written by the claiming project can be -- rename and reword. Also F3's sibling, the independence claim: README, SYNOPSIS, results.yaml, evidence.yaml, RESULTS.md and the thirdparty README say the two routes 'share no modelling assumption'; they share the Certificate object and Conditions 1-4 and differ in the Condition 5 method. Say that (the gate's docstring already does, ported with think-e6xe), and port PR 80's surface test over those six files. Found on the way: SYNOPSIS still says 'None reaches C5, because no one outside the project has reviewed any of them' -- a fourth D-446 sentence; fix it and add it to D-446's entry. F4: the n = 11 replay checked the declared total mass but not the declared least cell mass, and the standalone verifier printed a mismatch as a note and still ended VERIFIED; declared minima govern acceptance.
