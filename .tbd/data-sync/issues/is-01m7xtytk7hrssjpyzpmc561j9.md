---
type: is
id: is-01m7xtytk7hrssjpyzpmc561j9
title: Use one reviewed status in drafts for V0/C1 restatements
kind: bug
status: open
priority: 2
version: 1
labels:
  - intake
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
created_at: 2026-11-21T01:18:59.686Z
updated_at: 2026-11-21T01:18:59.686Z
---
For a V0/C1 Option D restatement, the correction sentence in check_requests --draft derives reviewed while _plain_state emits recorded in the registered bullet. The #846 comment was reconciled in place, and #1058 records reviewed. Share the state label across both outputs and preserve restatement classification text. Cover it with the existing request-render tests.
