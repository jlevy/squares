---
type: is
id: is-01m12e2r7pke6vqym4pn8yxn7s
title: Document the three-layer work model and retire the cell terminology collision
kind: task
status: closed
priority: 2
version: 2
labels:
  - packing
dependencies: []
created_at: 2026-08-27T20:20:16.238Z
updated_at: 2026-08-27T20:23:29.773Z
closed_at: 2026-08-27T20:23:29.757Z
close_reason: Done in session 030 (commit 00927d2). BC re-glossed as 'bounded commitment' across 14 live occurrences; the 4 in terminal session records left as recorded. Work-unit map now carries the bead / commitment / phase layering with a comparison by lifetime, typing and falsifier. Four stale or misleading entries corrected. No identifier, schema pattern, test, or frozen evidence string touched. The third and fourth senses of 'cell' (instance-axis rows, experimental-design cells) are recorded in the session evidence but deliberately left as found.
resolution: null
duplicate_of: null
---
BC expanded to 'bounded cell' while 'cell' independently names the linear-programming object at the centre of the enumeration work (235 cell identifiers in source; raw, canonical, active and full cells are four distinct technical objects). The README defined both, twenty lines apart.

Measured before choosing a fix: the identifier BC-NNN appears 646 times across 49 files, is pinned by two schema patterns and by frozen evidence strings that tests assert byte-exactly, and appears in 21 terminal session records. The phrase 'bounded cell' appears 9 times, of which 4 are in terminal records.

So the identifier stays and the expansion changes: BC now reads 'bounded commitment'. Accurate to the object, which declares entry conditions, acceptable exits and a budget before work starts, and which outlives any one session.

Also repaired in the same pass: the work-unit table omitted agendas, commitments and beads entirely, so the three-layer model was undocumented; the BC-NNN gloss still described agenda-001 as the only agenda; the doc-ownership table pointed at agenda-001 as though it were the whole agenda system; and the workflow handoff column read as a rule while measuring 31 percent conformance across 171 recorded phases.
