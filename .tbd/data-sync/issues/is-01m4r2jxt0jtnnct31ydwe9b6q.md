---
type: is
id: is-01m4r2jxt0jtnnct31ydwe9b6q
title: "Homepage toggle_seen fixture: theme menu 'system' choice stays hidden under CI load (flake on #547)"
kind: bug
status: closed
priority: 2
version: 4
delegate: w-records-1026
labels:
  - bug
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-12T12:49:46.293Z
updated_at: 2026-10-26T10:25:24.569Z
started_at: 2026-10-26T10:18:11.093Z
closed_at: 2026-10-26T10:25:24.568Z
close_reason: "Done in #827 (e076a2c95, merged at 909ddc76e): the homepage fixture waits on the theme menu's own state (gear closed/open, focus on the checked choice, root mode set); no timeout lengthened, nothing skipped. #550 closed with its final reply (issuecomment-6413624376)."
resolution: null
duplicate_of: null
---

## Notes

GitHub issue: https://github.com/jlevy/squares/issues/550. Seen on #547 at c8c479ad9 (run 38243975797, job 114793179857): 10 setup errors from toggle_seen's _themes (test_site_homepage.py:227), Locator.click 30 s timeout on the theme menu's 'system' choice; one re-run passed; not #547's (module never loads the atlas probe). Fix: wait on the menu's own state, as #520/#547 did; never lengthen the timeout or skip.
