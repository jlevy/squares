---
type: is
id: is-01m4gavej55mf8ak2mqgqmxaxf
title: pages.yml browser-geometry (webkit) install step can hang with no timeout
kind: bug
status: in_progress
priority: 2
version: 2
delegate: codex-survey-tracker-repair
labels: []
dependencies: []
parent_id: is-01m4fdxw81pt2v4k29y9n58rn6
hold: null
hold_until: null
created_at: 2026-10-09T12:40:18.756Z
updated_at: 2026-10-09T20:39:30.169Z
started_at: 2026-10-09T20:39:30.169Z
---
Run 37924825906 (#469 head 3fde0883b): job 113801659733 'browser-geometry (webkit)' sat in 'Install the pinned browser and its system libraries' for over an hour (normally ~2 min). The job sets no timeout-minutes, so a hung install blocks the Certificate page conclusion until GitHub's 6-hour default. Add a bounded timeout-minutes on that job/step (and consider the rerun-starved listener covering it).
