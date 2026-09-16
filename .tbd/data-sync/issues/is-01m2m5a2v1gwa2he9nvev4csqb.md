---
type: is
id: is-01m2m5a2v1gwa2he9nvev4csqb
title: "PR #186 review R1-R3: wall check never ran and failed open"
kind: bug
status: closed
priority: 0
version: 3
refs:
  - kind: pr
    url: https://github.com/jlevy/squares/pull/186
    at: 2026-09-16T03:50:02.690Z
labels: []
dependencies: []
parent_id: is-01m2kb4xhaqh3bv0cnnqnqvvsp
created_at: 2026-09-16T03:49:00.895Z
updated_at: 2026-09-16T03:50:02.691Z
closed_at: 2026-09-16T03:49:05.824Z
close_reason: "Fixed in ba34637b. Both jobs pin uv 0.12.8/Python 3.14.7/PyYAML 6.0.3, the tool uses the C safe loader, unmeasurable exits nonzero, and workflow/exit negative controls pass. Focused suite: 62 passed; exact standalone command starts."
resolution: null
duplicate_of: null
---
Formal review findings for PR #186. The workflow invoked a Python-3.14-only script with the mutable runner python3 and ambient PyYAML; the script violated the YAML loader boundary; and unmeasurable runs exited zero. Provision pinned uv/Python/PyYAML, make the loader fast and hermetic, and fail closed with negative controls.
