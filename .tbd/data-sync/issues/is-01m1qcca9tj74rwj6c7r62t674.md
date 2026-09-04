---
type: is
id: is-01m1qcca9tj74rwj6c7r62t674
title: "F24: bind RETAINABLE to bytes -- hash at start, re-check after each route, print the SHA-256; retain.py verifies it before copying"
kind: task
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m1qcc9devr6mz0m6erxswxjc
created_at: 2026-09-04T23:34:35.578Z
updated_at: 2026-09-04T23:34:35.578Z
---
Their fix in decide_certificate.py; port the hash binding and the two rewrite-during-sweep regressions, not the hostile-input matrix. Add the useful half of F17: the claim string and declared total must match the reconstructed object.
