---
type: is
id: is-01m1qcchmasjppsb50npxmkhbd
title: "Decide minimal_verify.py: fold or drop"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m1qcc9devr6mz0m6erxswxjc
created_at: 2026-09-04T23:34:43.081Z
updated_at: 2026-09-04T23:34:43.081Z
---
Two standalone verifiers of one file is one more than a stranger needs. If the code lane finds minimal_verify.py strictly cleaner than thirdparty/verify.py, keep it and fold the other's distinct checks in; otherwise drop it and port only its distinct checks.
