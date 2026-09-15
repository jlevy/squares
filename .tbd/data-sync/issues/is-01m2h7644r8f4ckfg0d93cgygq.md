---
type: is
id: is-01m2h7644r8f4ckfg0d93cgygq
title: One probe loader for every Python tool that drives a browser
kind: feature
status: closed
priority: 1
version: 8
labels: []
dependencies:
  - type: blocks
    target: is-01m2h764pcbfwx0btxez85zdsq
  - type: blocks
    target: is-01m2h765488h9hcy6c3zpp4abx
  - type: blocks
    target: is-01m2h765jws1b00yav58n7wzaq
  - type: blocks
    target: is-01m2h763nax0cdf5p2btjjv224
parent_id: is-01m2h76347zn3abcahzd3642ac
created_at: 2026-09-15T00:24:05.015Z
updated_at: 2026-09-15T01:17:55.952Z
closed_at: 2026-09-15T01:17:55.951Z
close_reason: "Delivered in PR #175: the shared loader, check_probes over every tree, strict type programs, and one extraction."
resolution: null
duplicate_of: null
---
One probe loader for every Python tool that drives a browser, on the model of `packages/workbench/tools/workbench_tools/probes.py`.

- Probes live as `.js` files grouped by tool, for example `packing/devtools/probes/<tool>/<name>.js` and `packing/tests/probes/...`. Each is one JavaScript expression, usually an arrow function taking a single argument object.
- Values reach a probe only as that argument, never by string formatting.
- A `probe(name)` loader reads and caches the file, and raises with the full path when it is missing.
- The probe directories are in Biome's includes with auto-formatting, and in a `tsconfig` program (with a `.d.ts` for any page API a probe calls).
- A `check_probes`-style check proves every probe parses as a function, is named by a caller, and that every name a caller uses has a file.
- Do not create a second, competing convention: either move the workbench loader into a shared module both use, or make the packing loader the same code.

## Notes

Delivered in PR #175 (branch claude/no-js-in-python-guard, stacked on #171), head 1ec9ea7b.

- Loader: packing/src/sqpack/probes.py. probe(root, name) is cached, refuses names outside root, and raises FileNotFoundError with the full path. applied(source, argument) gives add_init_script a probe called with a JSON-serialised argument.
- One copy, not two: packages/workbench already imports sqpack at runtime, so workbench_tools/probes.py is now a binding of the shared loader to packages/workbench/probes, with unchanged probe(name) semantics.
- Convention: probes/<tool>/<name>.js beside the tool (packing/devtools/probes, packing/tests/probes, a spike's own probes/).
- Check: packing/devtools/check_probes.py covers every probe tree in the repository (190 probes in 3 trees, the workbench's 186 included). Each probe must evaluate to a function (packing/devtools/node/inspect-probes.mjs, in node:vm), be named by a Python file beside its tree, and every name a loader-using file writes must have a file. It supersedes workbench_tools/check_probes.py, which no gate ran; think-xvjf deletes that file.
- Floors: strict tsconfig.packing-probes.json (reuses the workbench's atlas-transitions.d.ts) and tsconfig.devtools-node.json. Both are in Biome's includes, the ESLint promise overlay, the browser floor step and npm run typecheck.
- Proof extraction: check_published_site.py (2 sites) now uses probes and has left the allowlist. check_math_startup.py was not the smallest offender: it has 5 sites, including a ~400-line init script assembled from constants in check_math_loading and render_explainer_pdf, so it stays with think-3pox.
