---
type: is
id: is-01m5re1rjde9214mm9wbncb69g
title: "OR-1: retain the papers' no-change measurement as a maintained tool"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-25T02:25:48.621Z
updated_at: 2026-10-25T02:25:48.621Z
---
Each records lane this pass (#794's sync, #798, #797, H1) re-measured the papers' no-change record with a one-off scratch script (e.g. scratchpad/import-798/tools/papers_nochange.sh: render the four papers three times, twice from the tree and once with main's candidate inputs swapped in, and compare the 69 files byte for byte), which OR-1 forbids. Make it a devtools command beside check_release_impact (including the Playwright headless-shell dependency check), with a test, and point the release.py record's writer at it.
