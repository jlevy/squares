---
type: is
id: is-01m2heyy9gkdtpkhwp0mng5q4k
title: "PR #160 review D58: the spike README and v2 notes are stale after the move"
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T02:39:58.255Z
updated_at: 2026-09-15T02:40:57.547Z
closed_at: 2026-09-15T02:40:57.546Z
close_reason: "Fixed on #160 at 9baad048: spike README status, sizes (stamped f3874426), commands, --out wording and file table corrected; v2 NOTES carry a dated correction of what moved."
resolution: null
duplicate_of: null
---
Review finding, PR #160 stack triage (2026-09-14), lane D-tools.

The spike README and v2 NOTES were stale after #160's move: status paragraph, "`--out` refuses to overwrite", 2.9 MB, "Eight revisions", "Two needles", the file table, and commands naming moved v2 files.

Sources: #125 F28 (README and NOTES items); #160 R23 (spike-doc items). Related: think-53dt.

Files: `packing/atlas/known-best/video/spikes/README.md:8-41`; `spikes/v2-transitions/NOTES.md:11-13`; v1 `build_candidate.py:1457`, `:1480`.
