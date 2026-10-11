---
type: is
id: is-01m3ysmq51pbqgpv0y3z8q6m4g
title: "Results tables: the record links move from under the summary to a Details column of their own, a link to a line"
kind: task
status: closed
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-02T17:12:27.040Z
updated_at: 2026-10-02T22:41:20.483Z
closed_at: 2026-10-02T22:41:20.482Z
close_reason: "Merged in jlevy/squares#310 (1fb775810): a Details column, a link to a line; the tables of results bleed from 74rem."
resolution: null
duplicate_of: null
---
Owner, 2026-10-02: 'also for cleanness let's move all the links to their own column, Details. so these: n = 11 · register · evidence 1 · evidence 2 · source · review, for example would be vertically stacked in a Details column. that keeps the Result very clean and specific and easy to read.' In both tables of results the records line under a result's summary (_records: the case link, register, evidence N, source, review N) leaves the Result cell for a Details column, one link to a line, with no separating dots. The Result cell holds the summary and its star alone. Column order: Date, Result, n, Credit, Rungs, Status, Details, ID (Details placed after Status, before the id; the owner may move it). The phone card, the widths (eight columns now: what fits at 1280, 1024 and 768), the geometry tests and paper-design.md follow. A records column existed until think-3vh9 folded it under the summary; this restores a column, stacked.

## Notes

2026-10-02: committed 1fb775810 (Details column, a link to a line; tables of results bleed from 74rem: 1200 px at 1280, fit from ~1220, scroll 195/451 px at 1024/768 with every row). 402 tests passed (overview, result columns, math faces, preview checks, ladders). PR jlevy/squares#310 opened 2026-10-02 (head 38346bf4a); close when it merges.
