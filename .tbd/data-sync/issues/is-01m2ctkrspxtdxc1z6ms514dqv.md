---
type: is
id: is-01m2ctkrspxtdxc1z6ms514dqv
title: packing-validate --push defaults to one xdist worker, the worst configuration, on every broad diff
kind: bug
status: open
priority: 1
version: 1
labels:
  - research-tooling
dependencies: []
created_at: 2026-09-13T07:27:22.934Z
updated_at: 2026-09-13T07:27:22.934Z
---
Hit while absorbing PR 149's base move into PR 157 on 2026-09-13.

THE DEFECT. `packing-validate --push` on a broad diff selects the whole suite and then runs it in ONE process by default, which is the slowest configuration available and cannot meet the tier's own 1800s ceiling.

It arises from two defaults composing, not from either alone:
- `src/sqpack/cli/validate.py` ~4622: `--jobs` defaults to `os.process_cpu_count()`.
- `src/sqpack/cli/validate.py` ~1197: inner workers are `max(1, cpus - jobs + 1)`.

Substituting the default jobs into the formula gives `max(1, cpus - cpus + 1) == 1` for EVERY core count. The default is therefore not merely suboptimal on a 4-cpu box; it is pathological everywhere, and it is pathological exactly in the case `development.md` singles out ("a broad diff selects the whole suite and needs `--jobs 1`").

MEASURED HERE (4 cpus, `nproc` 4):
- Plain `packing-validate --push`: `pytest -q tests -m "not exhaustive_exact"` with NO `-n` flag, loadavg 1.13 of 4, still unfinished at 16m46s (1006s) when I stopped it. I did not let it finish, so its total is unmeasured -- only that it exceeded 1006s.
- `packing-validate --push --jobs 1`: `pytest ... -n 4`. Confirmed by process inspection.

The 1800s ceiling is the part that makes this a defect rather than a preference. D-484 already records the same tests at 1020.77s serially on a four-cpu box against 1801s and a killed step on CI. A default that selects the serial configuration is a default that selects ceiling failure for any contributor who runs the documented pre-push command on a broad diff.

WHY THE DOCUMENTED REMEDY IS NOT ENOUGH. `development.md` tells the reader to pass `--jobs 1`, but `--jobs 1` reads as "use one job", i.e. less parallelism, while it is in fact the only value that grants full inner parallelism. The flag's meaning inverts at the step/worker boundary, so the remedy is counterintuitive precisely where it matters and depends on the contributor having read that one sentence.

PROPOSED FIX, for the owner to choose among rather than a decision this bead makes:
1. When the selection is the whole suite (or more generally when one step will dominate), have `--push` choose `jobs = 1` itself, so the inner budget is not eaten by outer slots that have nothing to run concurrently.
2. Or decouple: let the inner worker count derive from free cpus rather than from `cpus - jobs + 1`, so the two knobs stop fighting.
3. Or, cheapest and least satisfying, make the tier refuse to start a whole-suite selection at one worker and say which flag to pass.

Option 1 is the one that matches OR-14 (a development cycle is never artificially slow): the tool should pick the fast configuration rather than require the contributor to know an inverted flag.

RELATED. D-488 (task "pre-push tier ran the whole suite serially") fixed a step-level serial lane. This is the same observable symptom reached through the outer jobs default instead, so D-488's fix does not cover it. `think-ph9v` owns the separate question of why the lane scales at 1.42x rather than 4x; this bead is not that -- it is about getting four workers at all.

NOT CLAIMED: no completion time for either configuration on this box, since I killed the serial run rather than paying another 20+ minutes to time a configuration I already knew was wrong. One reading per configuration would be a sample and not a measurement anyway (D-472).
