---
type: is
id: is-01m299vbk4aq0mkrjfxf7hyx4s
title: "J2: the assets and the 180 probes reach zero"
kind: task
status: closed
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m299tcsrh44b8n8m1c6jpgcb
created_at: 2026-09-11T22:36:42.467Z
updated_at: 2026-09-11T22:53:31.875Z
closed_at: 2026-09-11T22:53:31.874Z
close_reason: Zero errors and zero warnings over 190 files, from 570 lint findings and 187 files the formatter would rewrite. The page's baseline moved once, from abb090b1 to 54cbd45f; check_workbench.py passes with output byte-identical to the pre-format run, and check_legend, check_revision7 and check_probes all pass. Landed as c8e852ca.
resolution: null
duplicate_of: null
---
Format and fix `assets/workbench.js` (5,079 lines), `assets/workbench.css` (395) and the 180 probe files to zero Biome findings. `useBlockStatements` fixes are classed unsafe, so local fixing is `biome check --write --unsafe` while CI stays verify-only.

**This re-baselines the published page.** Every check up to now has been byte-identity against sha256 abb090b1; formatting the script moves it, once, deliberately. What proves the page still works afterwards is not the hash -- it is `check_workbench.py` passing with the same output, `check_legend.py` and `check_revision7.py` passing, `check_probes.py` still reporting 180 probes that parse and are functions, and the page rendering the same. Record the new hash.

Expect the probes to need attention as a class: each file is one JavaScript *expression*, not a statement, and a formatter or linter may read a bare arrow function as an unused expression. If it does, the fix is the config saying so for that directory, not a suppression in 180 files.
