---
type: is
id: is-01m29bhr1chn5zb60pd7jfy01b
title: blind_sweep collects two fields physics() never returns
kind: bug
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m299tcsrh44b8n8m1c6jpgcb
created_at: 2026-09-11T23:06:24.673Z
updated_at: 2026-09-11T23:06:24.673Z
---
Found by the type gate, which is the point of having one.

`probes/revision6/blind_sweep.js` pushes `squeezeDone: t.squeezeDone` and `side0: t.side0` off what `physics()` hands back, and `physics()` never copies either out of the trajectory. `simulate()` has them; the report it builds does not. Confirmed against the built page as well as the source: both are `undefined` in all 180-odd rows.

Nothing fails today, because `check_revision6.py` reads only `miss`. So they are two silently empty columns in a sweep that takes the better part of an hour to run -- see think-i15w.

Two ways to close it and they are different decisions:
- `physics()` in `assets/workbench.js` should forward `squeeze`/`squeezeDone`/`side0`, if the sweep was meant to have them. That is a change to the API's return, so the .d.ts follows.
- Or the probe loses them, if they were never meant to be there. That changes what the probe hands back, which is a checker's evidence.

The fields are declared optional in `probes/atlas-transitions.d.ts` and the probe carries a comment saying they are always undefined, so the state is at least honest until someone decides.
