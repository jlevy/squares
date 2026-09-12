---
type: is
id: is-01m2ar91msd279bq940mkybctf
title: Return the verified-upper-bound corpus check to the fast lane
kind: bug
status: in_progress
priority: 1
version: 2
labels:
  - ci
dependencies: []
parent_id: is-01m2ad9avdatjwfznq7zwqjget
created_at: 2026-09-12T12:08:05.528Z
updated_at: 2026-09-12T13:36:48.825Z
---
The exact-head PR149 full gate measured test_a_third_of_the_corpus_certifies_a_weaker_bound_than_it_reports at 0.97s, below the repository's 1s slow-marker floor. Remove its pytest.mark.slow decorator and matching test_module_boundaries slow registry entry, add no replacement ceremony, run the focused contract and boundary tests, then rerun the required gate before publication.

## Notes

Implemented unchanged-test lane correction at 4d00ab68. Focused 23-test control, Ruff, formatting, BasedPyright, unrestricted pre-push, and all required hosted checks pass. The repeated full checkpoint is running; close only after that exact-head gate passes.
