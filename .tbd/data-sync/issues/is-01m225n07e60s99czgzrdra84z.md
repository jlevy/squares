---
type: is
id: is-01m225n07e60s99czgzrdra84z
title: "Settle the mark stroke is none test needle: stale check or real regression"
kind: bug
status: open
priority: 2
version: 1
spec_path: packing/campaign/explorations/X-025-hunting-by-hand-and-the-move-set-threads.md
labels:
  - packing
dependencies: []
parent_id: is-01m225hw89vjsga1wnegrwnq5a
created_at: 2026-09-09T04:08:38.893Z
updated_at: 2026-09-09T04:08:38.893Z
---
Known defect in the v2-transitions prototype, deferred deliberately since revision 11.

test_candidate.py has failed one needle, 'mark stroke is none', since the outlines were removed: '#mark rect { stroke: none; }' in the stylesheet makes the previous square's outline invisible while the check still expects scarlet. It has been carried unfixed through revisions 11, 12 and 13, each of which recorded it as predating that revision's work.

Why it must be settled either way rather than carried further. The notes call it 'a real regression in the picture, not only in the check', so it is either a stale needle that should be flipped from presence to absence, or a real loss in what the stage shows that should be restored. Nobody has decided which, and an assertion that is expected to fail is worse than no assertion: revision 11 recorded that a sibling stale needle, 'index.html lacks scarlet marks the new square', had gated the entire browser tier off for two revisions because it fired before the 'if not failures: browser_checks(...)' line. A suite with a standing red is a suite whose next real failure is invisible.

Decide what the arriving and previous squares should look like -- the arriving square's fill still leans scarlet and settles to its own colour, which is the convention the review stills show -- then either restore the stroke or flip the needle, and record the decision in NOTES.md.

Prototype: packing/atlas/known-best/video/spikes/v2-transitions/. Notes: NOTES.md, revisions 11, 12, 13.
