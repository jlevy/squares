---
type: is
id: is-01m4zdrrf3qwg7ms04am4vx8x3
title: Fix stale News browser contracts after editorial exclusion and wrapping (B1)
kind: bug
status: closed
priority: 1
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4zaazfxmv8px64xvdvdqnc7
hold: null
hold_until: null
created_at: 2026-10-15T09:19:52.802Z
updated_at: 2026-10-15T09:35:20.621Z
started_at: 2026-10-15T09:20:04.642Z
closed_at: 2026-10-15T09:35:20.620Z
close_reason: Fixed in5b66be49598785dda245de6bb394c53e4b490d96; five real Chromium regressions pass58.81s (bothwidths plus raw/encoded/malformed archive forwarding),13integration+homepageheadingcontrols pass27.30s. Independently reviewedB atd022 confirmsbothfixed. Parentreader-deliverybeads stayopen untilPRmerge/deploy.
resolution: null
duplicate_of: null
---
Dedicated correctness review B at895637 found two native News tests still count/filter all changelog history entries, including the deliberately excluded PR492, and compare topic layout borders/gaps to the single-line Home chooser. Derive expected articles/counts/low-score and About targets from news_entries. Preserve common typography/size/state contract while separately checking intentional topic group wrapping and button borders. Worker prepares patch while frozen gate runs; apply and run exact affected native browser tests before delivery.
