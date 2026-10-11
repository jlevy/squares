---
type: is
id: is-01m3p4qcde9qgwr3dyp1b6v8fe
title: Define remaining sqsearch Rust support and CLI contracts
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m3nzy6gqfv60whzzvww0ffa0
created_at: 2026-09-29T08:32:58.797Z
updated_at: 2026-09-29T08:32:58.797Z
---
Follow-up to guideline review in PR 246. Declare supported platforms and MSRV separately from pinned Rust 1.98; add matching tests and dependency-policy audit after measuring adoption. Review existing reasoned lint exceptions and CLI error/help/version/broken-pipe behavior, retaining stable full CLI goldens where portable. Preserve independent geometry oracles and avoid platform-sensitive literal stochastic output. This is search-tool engineering debt, not a claim of proof-verifier failure.
