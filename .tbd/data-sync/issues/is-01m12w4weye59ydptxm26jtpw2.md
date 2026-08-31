---
type: is
id: is-01m12w4weye59ydptxm26jtpw2
title: "Composite: badges flush to the container box on both axes"
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-08-28T00:26:06.173Z
updated_at: 2026-08-28T00:26:06.173Z
---
Badges right-align to the container box edge rather than the card, and their box top sits on the card number's cap height rather than its baseline, so the label row reads as one block against the packing above it. _append_badge now takes an explicit box top instead of a text baseline.
