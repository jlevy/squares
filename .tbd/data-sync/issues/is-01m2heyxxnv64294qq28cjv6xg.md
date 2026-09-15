---
type: is
id: is-01m2heyxxnv64294qq28cjv6xg
title: "PR #160 review D57: declared build and selection inputs are incomplete hand lists"
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T02:39:57.876Z
updated_at: 2026-09-15T02:40:57.227Z
closed_at: 2026-09-15T02:40:57.226Z
close_reason: "Fixed on #160 at bcf0113d: render-katex.ts declared; render_explainer.py in _WORKBENCH_INPUTS; test_build_site_inputs.py derives the builder's inputs from its source and requires the declaration to cover them; selection tests for every render input and for .d.ts/.mjs/.ts/.css browser-floor inputs."
resolution: null
duplicate_of: null
---
Review finding, PR #160 stack triage (2026-09-14), lane D-tools.

Declared build and selection inputs were hand lists: the `build_site` closure was not derived (`tools/render-katex.ts` undeclared), `_WORKBENCH_INPUTS` omitted `render_explainer.py`, and `PATTERN_PROBES` had no `.d.ts` case. Missing classes, negative test and `.ts`/`.mjs`/`.cjs` patterns were fixed at f9099096.

Sources: #125 F30; #125 F36; #160 R26 (inputs item). Related: think-g0lh, think-ej1d.

Files: `packages/workbench/tools/workbench_tools/build_site.py:41-66`; `packing/src/sqpack/cli/validate.py:2847-2857`, `:2986-3008`; `packing/tests/test_change_scoped_selection.py:25-60`.
