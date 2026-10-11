---
type: is
id: is-01m41djrs4b3pdn1fk916vg1fa
title: "Deploy check: every published page carries complete link-preview metadata"
kind: task
status: closed
priority: 2
version: 9
labels: []
dependencies: []
parent_id: is-01m41d7edgm9wc99zdrkaa5ehy
created_at: 2026-10-03T17:39:23.555Z
updated_at: 2026-10-06T08:31:11.713Z
closed_at: 2026-10-06T08:31:11.713Z
close_reason: |
  Done (bead review 2026-10-06, origin/main eb43ffe9a): #319 and #334 both MERGED (2026-10-04); packing/devtools/check_published_site.py on origin/main holds every page head to the link-preview contract (render_overview.head_tags), forwarders included
resolution: null
duplicate_of: null
---
Hold every published page to the metadata contract in a test and in check_published_site, so a page added later cannot ship without a preview; forwarders state what they carry by rule.

## Notes

Merged in jlevy/squares#319 (ebe5415a7) without its review's fixes; those are in jlevy/squares#334 (forwarders from their page's record; publish checks the assembled site). Closes when #334 merges.
