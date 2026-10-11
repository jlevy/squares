---
type: is
id: is-01m3tj1ahf1j0sthhhdqd9fzys
title: Include newly cited provenance files in T-060 publication checkout
kind: bug
status: closed
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01m3tf1nb0x65ybpkdj2d9y7gs
created_at: 2026-10-01T01:42:33.767Z
updated_at: 2026-10-01T01:55:08.061Z
closed_at: 2026-10-01T01:55:08.058Z
close_reason: "Fixed at 9e97024f5 in PR261: exact cited archive files declared as render inputs, sparse checkout and push paths; real sparse-checkout regression coverage. 46 Pages tests, isolated probe typing and affected browser test pass. Final hosted optimality/frontend and both required aggregate gates pass; all 26 executed checks green. No deployment."
resolution: null
duplicate_of: null
---
Draft PR261 hosted optimality job failed because source-citation admission requires the retained kingbird provenance SVG and Kleddamag README, but sparse checkout only includes the n11 proof packet. Add the two exact archive files, declare render inputs and guard article archive citations against future omission. Keep the archive sparse; rerun only affected publication/scope checks.

## Notes

Hosted job110178312979 failed source-link admission for retained kingbird SVG. Root added exact kingbird SVG and Kleddamag README sparse patterns/push paths plus ARCHIVED_CITATION_SOURCES render inputs. Sol adds article-citation coverage guard and focused Pages contract tests. No geometry/proof change.
