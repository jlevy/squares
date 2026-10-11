---
type: is
id: is-01m4k3mdszyfe8bpwd5yngvsnd
title: "Promote e38_point to an interval-arithmetic tool: the un-normalised Lemma 8.1-8.2 point checks of Ryu's k^{3/8} bound"
kind: task
status: open
priority: 4
version: 1
labels:
  - packing
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
created_at: 2026-10-10T14:31:51.852Z
updated_at: 2026-10-10T14:31:51.852Z
---
The #471/#486 review's e38_point.py checks the un-normalised hypotheses of Lemmas 8.1-8.2 at b = 10^16 to 10^40 in floating point (about 40 terms). Checking each term against the lemmas and moving it to intervals is about an hour; it runs in seconds. Optional: the covering replays already decide what the proof needs.
