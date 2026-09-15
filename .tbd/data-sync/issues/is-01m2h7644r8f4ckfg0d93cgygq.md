---
type: is
id: is-01m2h7644r8f4ckfg0d93cgygq
title: One probe loader for every Python tool that drives a browser
kind: feature
status: open
priority: 1
version: 6
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
updated_at: 2026-09-15T00:24:27.830Z
---
One probe loader for every Python tool that drives a browser, on the model of `packages/workbench/tools/workbench_tools/probes.py`.

- Probes live as `.js` files grouped by tool, for example `packing/devtools/probes/<tool>/<name>.js` and `packing/tests/probes/...`. Each is one JavaScript expression, usually an arrow function taking a single argument object.
- Values reach a probe only as that argument, never by string formatting.
- A `probe(name)` loader reads and caches the file, and raises with the full path when it is missing.
- The probe directories are in Biome's includes with auto-formatting, and in a `tsconfig` program (with a `.d.ts` for any page API a probe calls).
- A `check_probes`-style check proves every probe parses as a function, is named by a caller, and that every name a caller uses has a file.
- Do not create a second, competing convention: either move the workbench loader into a shared module both use, or make the packing loader the same code.
