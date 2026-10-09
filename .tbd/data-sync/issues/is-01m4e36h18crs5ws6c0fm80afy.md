---
type: is
id: is-01m4e36h18crs5ws6c0fm80afy
title: Review and validate the atlas site cleanups
kind: task
status: in_progress
priority: 2
version: 28
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
child_order_hints:
  - is-01m4fgak1gswjj6et81wfndgrm
  - is-01m4fgam2ghc99ka4m1nbjwt4c
  - is-01m4fgamsz4gh4nf00hbmt339k
  - is-01m4fqjt02p8hxaxbgq056z2mq
hold: null
hold_until: null
created_at: 2026-10-08T15:48:04.263Z
updated_at: 2026-10-09T09:41:33.890Z
started_at: 2026-10-08T15:49:07.449Z
---
Review source changes and exported atlas, run focused checks and the change-reachable gate, then commit/push a focused PR and confirm CI. Keep the site cleanup epic open for further requests.

## Notes

Current clean frozenhead98ccc9ad29; science/layout87b546,pind832ce8,eight exports002a8911 unchanged. Four source-clear formal drafts bind mergebase3213 and101changed/89reviewed/12bulk-excluded; focused custody fix12passed/staticgreen/independentAST and lifecycle acceptance. Full new local gate64prechecks+normal phase pass; serial/overall stillactive. Latest target main533dd42c6 audit and actual ORT compatibility tree747efe57 are clear without local integration: four overlapping source/tests merge their intended changes,106total/93fast/13deferred unchanged, no atlas producer/data/export movement. Hosted receipts must verify actual current combined tree; PR/CI/formal publication/readiness remain pending. Current PDFs/preview/records checks pass and PDF is revealed/opened. Epic remains open; no GitHub merge authorized.
