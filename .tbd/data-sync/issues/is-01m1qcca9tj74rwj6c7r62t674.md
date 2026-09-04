---
type: is
id: is-01m1qcca9tj74rwj6c7r62t674
title: "F24: bind RETAINABLE to bytes -- hash at start, re-check after each route, print the SHA-256; retain.py verifies it before copying"
kind: task
status: open
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m1qcc9devr6mz0m6erxswxjc
created_at: 2026-09-04T23:34:35.578Z
updated_at: 2026-09-04T23:41:12.616Z
---
F17/F24, port as-is: decide_certificate requires claim and least_cell_mass and compares them against both routes, refuses Conditions 1-4 before the sweep, bounds the read, rejects duplicate keys and inexact numbers, and prints the SHA-256 of the re-read bytes on acceptance; retain.py verifies that hash before it copies. All four retained records satisfy every new requirement (verified by the code lane with --quick). The 731 test lines cost the fast tier about 13 s, 12.4 s of it one unmarked test (test_quick_mode_says_it_cannot_retain) that runs the real interval route beside its exhaustive twin -- mark it. Keep REFUSED on stdout unless the stderr split is wanted.
