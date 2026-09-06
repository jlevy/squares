---
type: is
id: is-01m1v227t1knqqwad3n7vgk7bs
title: Correct fractional certificate proof scope and checker trust boundary
kind: bug
status: closed
priority: 0
version: 4
delegate: claude-code@spud10.local
labels:
  - proof-scope
  - launch-blocker
dependencies:
  - type: blocks
    target: is-01m1v2yhy02qmka8ez4d2f5bde
parent_id: is-01m1tvqp2v2js8437xek2xk2gz
hold: null
hold_until: null
created_at: 2026-09-06T09:51:17.312Z
updated_at: 2026-09-06T10:07:27.844Z
started_at: 2026-09-06T09:52:13.618Z
closed_at: 2026-09-06T10:00:21.861Z
close_reason: "Integrated as 7e932f1b. The certificate-local theorem now states s(n) >= L; both standalone verifier paths require 0 < T < 1 and reject duplicate JSON keys; generated claim documents were refreshed. Specialist validation: 75 fast verifier tests, Ruff, BasedPyright, claim render check, and edit gate passed. Coordinator rerun on integrated head: 54 focused tests passed with 14 exhaustive deselected, Ruff clean, claim render current, and diff check clean. Exhaustive exact decisions remain for the checkpoint gate."
resolution: null
duplicate_of: null
---
Correct certificate.py's two false strict s(n)>L docstrings to the proved s(n)>=L relation; document the pinned checker's 0<T<1 scope; audit and, if proportionate, reject duplicate JSON keys before release. Preserve T-018 and add focused controls for every changed claim.
