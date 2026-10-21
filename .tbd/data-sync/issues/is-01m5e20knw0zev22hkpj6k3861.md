---
type: is
id: is-01m5e20knw0zev22hkpj6k3861
title: Diagnose sudden spud-ext1 disk growth and largest current consumers
kind: task
status: closed
priority: 1
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-21T01:43:03.600Z
updated_at: 2026-10-21T01:56:32.771Z
started_at: 2026-10-21T01:44:13.042Z
closed_at: 2026-10-21T01:56:32.770Z
close_reason: "Measured current consumers using cache-free targeted fdu probes plus fresh migration inventory, confirmed ~42GiB physical free-space loss since Oct19, identified ~21GiB current footprint under newly created GTIA output directories, documented protected-directory/clone attribution limits and recurring inventory-only coverage failure. Review evidence: /Volumes/spud-ext2/agent-evidence/spud-ext1-growth-20261020/REVIEW.txt. No ext1 writes or cleanup mutations."
resolution: null
duplicate_of: null
---
