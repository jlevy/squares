---
type: is
id: is-01m225nvxap6cynxrpds642e8b
title: Give the drawn contact graph an undo
kind: bug
status: open
priority: 2
version: 1
spec_path: packing/campaign/explorations/X-025-hunting-by-hand-and-the-move-set-threads.md
labels:
  - packing
dependencies: []
parent_id: is-01m225hw89vjsga1wnegrwnq5a
created_at: 2026-09-09T04:09:07.241Z
updated_at: 2026-09-09T04:09:07.241Z
---
Known defect in the v2-transitions prototype, recorded in revision 12 and deferred.

The hand-drawn contact graph has no undo. A mis-drawn edge can be toggled off, but clear is all or nothing, and a graph of thirty edges is thirty gestures to rebuild. Every other edit on the page is either a slider that can be put back or a drag that can be redone.

Why it matters beyond convenience. The drawn graph is the mechanism the next contact experiment needs, and drawing a graph is the one interaction on the page where the user's work is not recoverable from a parameter. The trajectory cache is already keyed by the graph's contents rather than by a revision counter -- three graphs are three keys, one graph reached twice is one key, and rubbing an edge out and back lands on the run it started from -- so an undo stack over the edge set costs nothing in cache identity and is the natural fit.

A related note from the same revision, worth handling in the same change or explicitly not: a graph drawn and then switched away from is still in the store and gives no sign of it beyond the clear button going live.

Prototype: packing/atlas/known-best/video/spikes/v2-transitions/. Notes: NOTES.md, revision 12, 'A contact graph drawn by hand' and 'What reads badly'.
