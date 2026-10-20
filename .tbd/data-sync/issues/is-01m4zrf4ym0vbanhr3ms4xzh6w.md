---
type: is
id: is-01m4zrf4ym0vbanhr3ms4xzh6w
title: Recover completed closure scratch space while preserving source and release evidence
kind: task
status: closed
priority: 1
version: 6
delegate: claude-code@spud10.local
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-15T12:26:52.243Z
updated_at: 2026-10-15T14:03:01.192Z
started_at: 2026-10-15T12:27:22.303Z
closed_at: 2026-10-15T14:03:01.191Z
close_reason: Immediate external scratch pressure eased to about733MiB through normal configured pytest retention; older failed pytest-2 is gone, all bounded test sessions exited, and no manual deletion command ran. Source/evidence and the Cargo cache remain intact. No permanent-deletion override is needed for this recovery. Large builds remain constrained by actual free space.
resolution: null
duplicate_of: null
---
The external spud-ext1 volume fell to about 77 MiB free after the closure pre-push run. Hold new disk-heavy work without an internal-disk fallback. The two completed generated directories considered for recovery are tutorial-closure-20261015/tmp/pytest-of-levy/pytest-2 (about 637 MiB) and tutorial-closure-20261015/cargo-target (about 70 MiB). Producing commands have finished, and lsof/ps found no users. Source, reviewed release artifacts, raw logs and unique evidence remain in the workspace. The cleanup skill requires Trash-only staging and leaving Trash unemptied; staging on the same external volume would not free space. A direct async question requests an override for permanent removal of only these two paths. No answer has arrived, so neither has been deleted. The earlier 936 MiB staged in Trash was not physical reclamation.

## Notes

Read-only follow-up at 14:00 UTC: external free space is about 733 MiB, versus about 77 MiB before. The old tutorial-closure tmp/pytest-of-levy/pytest-2 no longer exists; the retained failed pytest-3 exists and cargo-target remains. The bounded supervisor worker confirms all sessions exited (red1, green0, lint/types0), no manual deletion or background cleanup command, and pytest failed/1 retention runs synchronous numbered-directory cleanup. Removal of the older tree matches that normal configured retention. Source and unique release/research evidence remain outside scratch. No permanent manual removal of either proposed directory was performed, and the Cargo cache stays intact. The earlier destructive-cleanup approval is no longer necessary for immediate space recovery; large builds still require more headroom. Existing Trash staging was not counted as reclaimed space.
