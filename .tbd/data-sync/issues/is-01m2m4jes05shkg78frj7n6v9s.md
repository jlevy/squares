---
type: is
id: is-01m2m4jes05shkg78frj7n6v9s
title: "PR #175 lane L1: check_probes cannot see a missing probe behind an assembled name"
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m2m4aptpzqgmmhqxgxz3vba5
created_at: 2026-09-16T03:36:06.684Z
updated_at: 2026-09-16T03:36:06.684Z
---
probe(PROBES, f"{GROUP}/zz_absent") returns OK. check_probes.py:26-29 admits false unused reports but not the hole in the missing-name guarantee. Count and report loader calls whose argument the analysis could not read. Found by the review lane at #181's head; not in the published review.
