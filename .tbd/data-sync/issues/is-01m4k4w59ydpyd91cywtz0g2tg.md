---
type: is
id: is-01m4k4w59ydpyd91cywtz0g2tg
title: "upper_bound_reports: key declaration rows by (n, path) so a commit's other certificates at one count are compared too"
kind: task
status: open
priority: 3
version: 1
labels:
  - packing
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
created_at: 2026-10-10T14:53:33.886Z
updated_at: 2026-10-10T14:53:33.886Z
---
Found importing evand's trio126 (think-ilwc): load_declaration requires unique ascending counts, so a source commit holding several certificates at one n (n126_xu, n126_ph14, n126_ph10) can declare only one; the other two were compared by a scratch script instead. Key rows by (n, path), make the requested row explicit, and carry the others as unrequested rows of claims.json, as stage 1 requires ('list every claim the release makes'). Test on the trio126 packet.
