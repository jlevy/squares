---
type: is
id: is-01m1qhhfny7yh6h6an8hw7qyek
title: n-012.md body and E-n012-fractional-certificate still describe superseded rungs (D-442 class)
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m1qcc9devr6mz0m6erxswxjc
created_at: 2026-09-05T01:04:47.806Z
updated_at: 2026-09-05T01:04:47.806Z
---
Found by the think-rjaj port: two live D-442-class staleness instances. E-n012-fractional-certificate's limitations in evidence.yaml still describe a 681-atom 197/50 certificate while pointing at certificate.json (99/25, 2097 atoms); n-012.md's body still says 'The verified lower bound is 77/20 = 3.85' under front matter saying 99/25. Neither is caught: check_rung_figures reads atom counts only in results' four prose fields, and check_case_prose matches its own patterns. PR 80 rewrites both (git diff HEAD 04127189 -- packing/frontier/evidence.yaml packing/frontier/n-012.md); port the rewrites with every figure re-derived, and extend one detector to read the shape that hid them.
