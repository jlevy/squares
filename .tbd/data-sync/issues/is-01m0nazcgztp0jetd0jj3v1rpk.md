---
type: is
id: is-01m0nazcgztp0jetd0jj3v1rpk
title: Narrow .flowmarkignore to evidence-based exceptions
kind: task
status: closed
priority: 1
version: 2
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels: []
dependencies: []
parent_id: is-01m0na001wtn9wb0fkwndgwwrq
created_at: 2026-08-22T18:15:52.607Z
updated_at: 2026-08-22T18:16:23.953Z
closed_at: 2026-08-22T18:16:23.953Z
close_reason: Tested each candidate exclusion instead of assuming. flowmark breaks inline $...$ spans across lines when rewrapping (31/339 spans in Stromquist, 101/1236 in Caoduro-Sebo, 5/433 in Kingbird), which defeats grep over the archive. Exclusions stand on evidence; scope confirmed minimal -- only the archive and generated skill files, everything else formats.
---
Policy: format the whole repo; exclude only what is demonstrably better left raw. Test each candidate exclusion rather than assuming.
