---
type: is
id: is-01m225kg4dcxk61r0qzysnavwf
title: Add a best-known start and a re-randomising random start with a visible seed
kind: task
status: in_progress
priority: 2
version: 3
spec_path: packing/campaign/explorations/X-025-hunting-by-hand-and-the-move-set-threads.md
labels:
  - packing
dependencies:
  - type: blocks
    target: is-01m225psj2z0sx407k1ma5a4sp
parent_id: is-01m225hw89vjsga1wnegrwnq5a
created_at: 2026-09-09T04:07:49.644Z
updated_at: 2026-09-09T04:09:44.650Z
---
In flight in the v2-transitions prototype as of 2026-09-08.

Two additions to the starting arrangements, which are the Scope-and-Strategy boundary: what the settle is handed before any physics runs.

1. A best-known start. Load the retained best-known packing for the chosen n as the starting arrangement. It is the start every diagnostic wants: it is the only start whose answer is known, it is what candidate C0d's stationarity test needs (does the law hold a known optimum still), and it is what makes a contact-graph measurement interpretable, since the record realises its own contact graph by construction. Revision 13 already added a previous-packing start, so the loader exists and this is the sibling of it.

2. A random start that actually re-randomises, with the seed shown. Today's random start is seeded and reproducible, which is right, but pressing it again should give a different arrangement and the seed in force should be on the panel. Reproducibility is served by showing the seed and letting it be set, not by silently reusing one. Without this, 'run it again and see' is not available in the one mode where a person is watching, and a distribution over seeds -- which is the number Calibrate will report and the only one worth believing -- cannot be gathered by hand at all.

Both starts must key the trajectory cache by their contents, as revision 12's drawn graph does: one arrangement, one run, and a seed reached twice keys the same string both times.

Prototype: packing/atlas/known-best/video/spikes/v2-transitions/. Notes: NOTES.md, revisions 9, 12 and 13.
