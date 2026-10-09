---
type: is
id: is-01m4fk142s062w9aj65ptbas2d
title: Add PT Serif italic/bold metric aliases to remove residual frontier CLS race
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m4fdxw81pt2v4k29y9n58rn6
created_at: 2026-10-09T05:43:58.809Z
updated_at: 2026-10-09T05:43:58.809Z
---
If both preloaded PT Serif italic and bold lose the race, frontier can still reach CLS 0.1338. Liberation/Times italic (104.5%) and bold (112%) aliases in site.css measured 0.0 in that case (scratchpad/cls). Georgia (Mac) has no italic/bold alias.
