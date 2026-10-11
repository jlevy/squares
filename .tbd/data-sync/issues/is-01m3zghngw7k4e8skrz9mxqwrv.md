---
type: is
id: is-01m3zghngw7k4e8skrz9mxqwrv
title: "Tags: consistent status colours: proved green, open yellow, reviewed blue, confirmed the C rungs' green"
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3zgh5vhwpb57pvzhtnd5ece
created_at: 2026-10-02T23:52:44.316Z
updated_at: 2026-10-03T14:38:01.296Z
closed_at: 2026-10-03T14:38:01.296Z
close_reason: Merged in jlevy/squares#312 (c831b4ee0), after a correctness and engineering review round (419a1db5d)
resolution: null
duplicate_of: null
---
Owner, 2026-10-02: 'tags like "open" and "proved" should have better consistent colors. we should make "proved" a more green color and "open" more yellow. same for "reviewed" (say blue) and "confirmed" (green similar to our confirmed hue on C1...C5)'. Give the status chips one consistent palette: a case's proved green and open yellow (Frontier table, case records, popovers), a result's reviewed blue and confirmed the green of the C rungs; recorded, incomplete and the rest keep a quiet fill. Light and dark schemes, contrast held; tests and paper-design.md (Chips, Color) follow.

## Notes

Committed cfe050c15.
