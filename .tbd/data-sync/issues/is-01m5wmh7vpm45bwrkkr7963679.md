---
type: is
id: is-01m5wmh7vpm45bwrkkr7963679
title: Redraw the assets and move their records with them
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m5wmghkt8vpnawbxzpbkm19e
created_at: 2026-10-26T17:36:04.982Z
updated_at: 2026-10-26T17:36:04.982Z
---
Apply the rule, redraw and re-measure.

- Redraw both poster families and every advertised export
  (`development.md`, "Release assets are drawn at their component's version bump").
- Move the retained composite descriptions in `build_known_best_atlas` with the drawing:
  they are prose a reviewer reads against it, and they name the address today.
- Re-measure the print layout. A changed line shifts baselines and ink bounds, which
  `check_print_layout` and the poster records hold.
- Take the release-impact decision for the infographic family rather than a
  no-public-change record: both families and every advertised export advance together,
  and this changes what the asset prints.
- Verify the PDFs by reading them, not by trusting the generator.

Depends on the rule bead.
