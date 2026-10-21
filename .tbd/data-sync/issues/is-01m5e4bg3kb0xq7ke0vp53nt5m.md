---
type: is
id: is-01m5e4bg3kb0xq7ke0vp53nt5m
title: Attribute Oct20 spud-ext1 free-space collapse to specific new writes
kind: task
status: in_progress
priority: 1
version: 4
delegate: claude-code@spud10.local
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-21T02:23:57.545Z
updated_at: 2026-10-21T03:34:03.455Z
started_at: 2026-10-21T02:25:41.628Z
---

## Notes

spud-ext1: October 20 disk-space reconciliation

The physical capacity loss is confirmed. Its complete file-by-file cause remains
unresolved. This investigation performed no deletion, migration change, or source edit.

Physical receipts (PDT, October 20; available GiB)
00:13:24   34.3614
02:14:00   26.9519
05:44:32   19.8441
07:41:30   11.0307
15:41:54    7.7129
16:12:25    1.7300
16:41:14    0.0211

The volume lost 26.9308 GiB between 02:14 and 16:41, including 8.8134 GiB between
05:44 and 07:41 and 5.9829 GiB between 15:41 and 16:12. See timeline.json for
source receipts and exact timestamps.

Visible findings
Six disjoint GTIA areas contain 9.1734 GiB in current allocated file sizes with
modification times today, across 123,399 files. Four disjoint GTIA directories born
today currently contain 8.154 GiB: closeout/W44-06 (2.721), views/2026-W44-06
(1.970), reader-inputs/W44-06 (1.921), and published-views/verified-20261020 (1.541).
These populations overlap; do not add them. Neither measures physical growth.
Full paths and provenance are in gtia-deep-known-dir-birthtimes.json and the two
files-modified-today reports. Reader inputs include about 0.566 GiB with older mtimes,
showing that modification-time queries miss some contents in newly created directories.

Most selected GTIA outputs finished before 05:44. Known retained scratch roots are
too small to explain the two large bursts. This does not rule out temporary
create/delete cycles, copying with preserved timestamps, or filesystem accounting.

Requested directory-age scan
The metadata-only full-volume fdu scan selected 114 recent directories at least
100 MiB. Its cutoff was 03:52:50 PDT, frozen at request time 19:52:50. Output arrived
after 36 minutes 14.8 seconds. See directories-modified-last16h.json.
Five inaccessible boundaries remain. A qualifying directory reports its existing
subtree size; that size is not newly written bytes. Ancestor rows overlap.

All returned large areas with latest activity before the 16:41 loss are GTIA-related.
Other large rows reflect activity after the loss, often Git or directory metadata.
For example, home-extras reports 64.324 GiB but its allocation is identical to the
earlier inventory. The 10.105 GiB next200 closeout subtree has at most 17.26 MiB
of retained regular files modified today; validation has 9.61 MiB versus 8.759 GiB
in total. A complete targeted query of the 1.175 GiB portable-seal scratch tree
found ZERO regular files modified between midnight and 16:41:14. That query took
6.70 seconds; see portable-seal-recent-files.json and .time.

These checks reject tempting false leads. They do not exclude every cause: smaller
directories are omitted, incomplete ancestors can disappear under the age filter,
and the 16-hour cutoff is later than the 02:14 baseline. No second whole-volume walk ran.

Remaining limits
macOS denies .Spotlight-V100, .DocumentRevisions-V100, .TemporaryItems and .Trashes.
A separate permission-denied test fixture is also unreadable. Their sizes and historical
changes are unknown. Current df usage minus regular-file allocation cannot be assigned
to these paths or to today: directory/filesystem metadata, shared extents and missing
historical size baselines also affect that comparison.

No APFS snapshots or currently observed deleted-open files explained the loss.
Further protected-area measurement requires an OS-authorized Terminal with sufficient
access or local authentication. The earlier user-input request remains pending.
No file-allocation baseline exists at 02:14, so exact retrospective physical attribution
may remain incomplete even after protected current sizes are available.

fdu review
See fdu-product-performance-review.txt for source citations, the existing metadata-only
recent-file tree/files/summary recipe, and prioritized improvements. fdu-observed-cost.json
and the two stack samples record this run. No document, code, word, or line analyzer ran.
The first sample shows metadata I/O waits with concurrent independently owned copy readers;
the later report sample reached a 5.2 GiB physical footprint. This is not a controlled
benchmark. The partial scan did not persist its requested cache.

The principal improvements are reusable partial query sessions, machine-readable progress,
clear activity-versus-growth labels, and durable historical baselines. Historical filesystem
events could provide changed-path leads, but cannot reconstruct byte growth without prior
metadata and explicit coverage of missing events.
