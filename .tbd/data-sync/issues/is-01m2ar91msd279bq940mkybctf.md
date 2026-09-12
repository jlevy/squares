---
type: is
id: is-01m2ar91msd279bq940mkybctf
title: Return the verified-upper-bound corpus check to the fast lane
kind: bug
status: closed
priority: 1
version: 7
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - ci
dependencies:
  - type: blocks
    target: is-01m2ad9avdatjwfznq7zwqjget
parent_id: is-01m2ad9avdatjwfznq7zwqjget
created_at: 2026-09-12T12:08:05.528Z
updated_at: 2026-09-12T15:51:57.595Z
closed_at: 2026-09-12T15:51:57.594Z
close_reason: "PR #149 exact head 4d00ab68 passed focused, unrestricted pre-push, unrestricted full checkpoint, and all hosted checks; its body records all valid and invalid costs and the PR is mergeable over PR #148."
resolution: null
duplicate_of: null
---
The exact-head PR149 full gate measured test_a_third_of_the_corpus_certifies_a_weaker_bound_than_it_reports at 0.97s, below the repository's 1s slow-marker floor. Remove its pytest.mark.slow decorator and matching test_module_boundaries slow registry entry, add no replacement ceremony, run the focused contract and boundary tests, then rerun the required gate before publication.

## Notes

Implemented the unchanged-test lane correction at 4d00ab68. Focused 23-test control, Ruff, formatting, BasedPyright, unrestricted pre-push, and all required hosted checks pass. The discovery full gate measured the intact corpus test at 0.97s below the one-second marker floor. A first repeated invocation was invalid and interrupted after 2,722s because its child PATH omitted uv. A second sandboxed replacement was interrupted after 1,146s because required process-tree and loopback controls cannot run there. The unrestricted exact-head full checkpoint is running as session 83725; close only after that gate passes.
