---
type: is
id: is-01m12w4weye59ydptxm26jtpw2
title: "Composite: badges flush to the container box on both axes"
kind: task
status: closed
priority: 3
version: 2
labels: []
dependencies: []
created_at: 2026-08-28T00:26:06.173Z
updated_at: 2026-10-06T08:30:24.682Z
closed_at: 2026-10-06T08:30:24.681Z
close_reason: |
  Done (bead review 2026-10-06, origin/main eb43ffe9a): _append_badge takes explicit box top; badges right-align from packing_x+SUMMARY_PACKING_SIZE with top at the number's cap height (aeb130bf4); origin/main build_known_best_atlas.py
resolution: null
duplicate_of: null
---
Badges right-align to the container box edge rather than the card, and their box top sits on the card number's cap height rather than its baseline, so the label row reads as one block against the packing above it. _append_badge now takes an explicit box top instead of a text baseline.
