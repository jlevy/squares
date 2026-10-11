---
type: is
id: is-01m32ht8jw42tvzgcfw72bya5x
title: Rigidity is reported open for n that are plainly rigid
kind: bug
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
created_at: 2026-09-21T17:56:56.025Z
updated_at: 2026-10-06T08:28:42.104Z
---
The facts panel shows 'rigidity' under OPEN with the '?' badge for many n whose packings are clearly rigid -- n = 98 in the cut video is a full grid with two loose squares and still reads 'OPEN ? rigidity'.

Whatever is deciding rigidity is either absent from the record for most n and being rendered as 'open' by default, or it is being computed wrongly. An absent fact and an open question are not the same thing, and the panel currently prints the second when it means the first.

Find where the panel's rigidity attribute comes from (the corpus record built by `workbench_tools.build_candidate`, through `src/data`), establish what is actually known, and fix the claim.

## Notes

2026-10-06 (bead review): the display half is fixed in 81e542c8f (rigidity is no longer listed under OPEN; the R badge appears only where it is established). That commit names this bead as the owner of what the record should actually say about rigidity, which is still open.
