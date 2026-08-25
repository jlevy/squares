---
type: is
id: is-01m0wazz9b0ffdqcxd682d8y7w
title: Avoid shell evaluation in tbd descriptions
kind: bug
status: closed
priority: 3
version: 2
spec_path: explorations/packing/campaign/agent-sessions/session-011-eight-hour-continuation.md
labels:
  - packing
  - focus-process
dependencies: []
parent_id: is-01m0w9a47h5zrn7jf16pp2kpxs
created_at: 2026-08-25T11:30:52.842Z
updated_at: 2026-08-25T11:33:50.996Z
closed_at: 2026-08-25T11:33:50.996Z
close_reason: The damaged think-sx22 description was replaced immediately with shell-inert prose and D-287 preserves the command-construction error.
resolution: null
duplicate_of: null
---
While creating think-sx22, the coordinator put a backtick-delimited word inside a double-quoted shell argument. Bash evaluated the word as a command and removed it from the created description. The command printed an error but tbd still created the bead. Correct the description immediately, record D-287, and use arguments without shell-active backticks for later tbd commands.
