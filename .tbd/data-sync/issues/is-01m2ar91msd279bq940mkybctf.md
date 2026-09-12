---
type: is
id: is-01m2ar91msd279bq940mkybctf
title: Return the verified-upper-bound corpus check to the fast lane
kind: bug
status: closed
priority: 1
version: 8
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - ci
dependencies:
  - type: blocks
    target: is-01m2ad9avdatjwfznq7zwqjget
parent_id: is-01m2ad9avdatjwfznq7zwqjget
created_at: 2026-09-12T12:08:05.528Z
updated_at: 2026-09-12T15:52:10.315Z
closed_at: 2026-09-12T15:51:57.594Z
close_reason: "PR #149 exact head 4d00ab68 passed focused, unrestricted pre-push, unrestricted full checkpoint, and all hosted checks; its body records all valid and invalid costs and the PR is mergeable over PR #148."
resolution: null
duplicate_of: null
---
The exact-head PR149 full gate measured test_a_third_of_the_corpus_certifies_a_weaker_bound_than_it_reports at 0.97s, below the repository's 1s slow-marker floor. Remove its pytest.mark.slow decorator and matching test_module_boundaries slow registry entry, add no replacement ceremony, run the focused contract and boundary tests, then rerun the required gate before publication.

## Notes

The unrestricted exact-head full merge/research checkpoint passed at `4d00ab68f26576f28c40c3a4543c7b2ca8f38000` in 3,990.24 seconds. All required checks passed; the Rust lint floor alone skipped because Cargo is unavailable. The run used the project Python 3.14 environment, a valid uv path, process access, and loopback access. It observed 10 CPUs with two outer jobs and one inner job, so the cost is reported without comparing it to the two-CPU budget band. PR #149's body now records this terminal result alongside the earlier invalid and failed attempts. The PR is open, non-draft, mergeable, stacked on PR #148, and every hosted check is green.
