---
type: is
id: is-01m244b5h4c49kzk2r5ss78sjz
title: Make the retained-script closure check a devtool
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-09-09T22:24:16.932Z
updated_at: 2026-09-09T22:24:16.932Z
---
The repository now retains 39 scratch measurement scripts as `.py.txt` beside their lane
documents in
`packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/`, and two
more under `agenda-032/unrun-independent-audit/`. Two properties of that set matter and
nothing checks either:

1. **Every file parses under the project interpreter.** A truncated or mangled copy is
   otherwise invisible — the extension is `.txt`, so Ruff and BasedPyright never look at
   it and no test imports it.
2. **Every local import resolves to another retained file.** Six of lane B's ten scripts
   import a sibling `sepcore`, four of lane A3/A4's import it too, `lp383`, `flooratoms`
   and `cap_lp` are imported across lanes. Retaining a driver without its imports
   documents a measurement without leaving it runnable, which is exactly the gap the
   2026-09-09 retentions opened and then closed by hand: the A3/A4 retention left
   `sepcore` in scratch, and the follow-up retention had to find that by reading the
   files.

**What to build.** A `packing/devtools/` checker that walks the retained `.py.txt` files,
compiles each one, extracts its imports with `ast`, classifies them (stdlib,
third-party, `sqpack`/`devtools`, local) and fails when a local import has no retained
file. The name mapping the retention convention uses is: strip the `lane-<id>-` prefix,
drop `.py.txt`, turn hyphens into underscores. A working prototype that produced the
measurement above is in the session scratchpad at `retain-spike-b/check_closure.py`; it
is one-off code, which is what `OR-1` says not to leave a measurement in.

Two details it must handle: the two files under `agenda-032/unrun-independent-audit/`
carry a deliberate two-line "UNTESTED DRAFT" banner above the shebang and do not parse
as Python, so either they are exempt by that banner or the convention changes; and the
checker should be cheap enough for the fast tier (`OR-13`), since it is pure parsing.

**What done looks like.** A devtool with a CLI and tests, wired into a validation tier,
reporting today's state green: 39 files in `agenda-034` parse, every local import
(`sepcore`, `lp383`, `flooratoms`, `cap_lp`) resolves to a retained file, and the two
`agenda-032` drafts are accounted for explicitly rather than by silence.
