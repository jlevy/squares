---
type: is
id: is-01m21npt8yyc1faakzqd5m51fb
title: Unify sans regular weight at 410 and refine support text
kind: task
status: in_progress
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels: []
dependencies: []
parent_id: is-01m20v1mq20k9d9p1wg9s5qdsq
created_at: 2026-09-08T23:30:01.117Z
updated_at: 2026-09-09T00:16:16.128Z
---
Owner requires regular sans text and sans math at 410 with one adjustable authoritative setting. Captions and end footnotes should share a slightly smaller size and more left/right inset. Keep font metrics and print instances matched to the weight; put reusable typography configuration in KPress and page-specific role sizing in Squares. Rebuild prepared geometry and verify HTML/PDF baseline, weight, size and wrapping.

## Notes

Checkpoint committed93cf54a9, pinned KPress0dd60f9 candidate (PR68).116focused tests +45/45affectedprepush checks pass165.74s. Rebuilt prepared HTML and PDF816939bytes; lightdesktop inspector finds no typography/provenance issue and13caption +11code baselines0screen/print. HostedCI/finalmergedpin/fullartifactreview/deployment remainpending; active spec has fullhandoff. KPress main thenadvanced viaPR66 changingmono.87to.82; reconcile current upstreamhead before finalpin rather than mislabel oldartifactchecks.
