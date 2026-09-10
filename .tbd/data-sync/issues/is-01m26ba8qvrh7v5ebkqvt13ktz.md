---
type: is
id: is-01m26ba8qvrh7v5ebkqvt13ktz
title: The explainer page drew differently twice in CI and the cause is unknown
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
created_at: 2026-09-10T19:04:36.347Z
updated_at: 2026-09-10T19:04:36.347Z
---
On 2026-09-10, run 34453706991 (main's push run at 3a18a05a), the `build` job of the
Pages workflow failed at `render_explainer_pdf --check`: `786119 then 786117 bytes,
normalised`. 786119 is the size every other CI render of that page produced, and the
receipt `_with_receipt` adds is exactly 94 bytes on all four runs checked, so it was the
second render of the pair that came up two bytes short. The job passed on a re-run and
the same content had passed on its pull-request run (34449286960 at 0c4c41b4), so this is
a race rather than a regression in the page.

What is known:

- A clock outside the two fields `_normalised` neutralises is ruled out by the pass rate,
  not by the log: the two renders are about nine seconds apart, so an unnormalised
  timestamp would fail every run rather than once.
- Forty consecutive renders in a container agreed byte for byte, 863873 bytes each in
  1m54s, using the preinstalled headless shell. That extends the module docstring's
  ten-render claim and does not reproduce the failure. The host's fonts differ from CI's:
  863873 bytes against 786119, 19 embedded faces against 18.
- D-490 recorded the occurrence and fixed the instrument rather than the cause:
  `_difference` now names the object, its declared subtype and a window of each render, so
  the next occurrence arrives diagnosable.

Next step is to wait for the next occurrence and read what the object is, rather than to
guess. If it recurs often enough to chase, `--renders N` is the tool: raise it in a
throwaway workflow run on a CI runner, where the fonts and the machine are CI's, rather
than locally where forty renders agree.
