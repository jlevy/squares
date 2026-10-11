---
type: is
id: is-01m46r3bpb5cpk6qqxm0as022h
title: "Integrity ceremony: main's n11 figure-input digest pins (n11_threshold_figures.py, paper_figures.py)"
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-10-05T19:19:25.131Z
updated_at: 2026-10-05T19:19:25.131Z
---
The merge of origin/main into claude/n17-sessions-167-168 (#347, d08d07997) brought in packing/devtools/n11_threshold_figures.py (5 sites: _pinned's sha256 comparison and four certificate/reference digest equalities) and packing/devtools/paper_figures.py (1 site: ladder_digest(records) != LADDER_DIGEST). They were written on main, where check_integrity_ceremony does not run, and are recorded in packing/devtools/integrity-ceremony.yaml's baseline as inherited. Decide per OR-16 whether each pins a real trust boundary (allowlist with its kind) or should identify inputs by Git revision and path instead, and ratchet the baseline down.
