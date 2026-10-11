---
type: is
id: is-01m45eyft0awdxdmkn7agn71ym
title: "PR #347 B5 (Low): name the deferred OR-18 bead think-h8d8 in the body's Deferred list"
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
labels: []
dependencies: []
parent_id: is-01m45ex3dssa31jvkkz9bzpc6e
created_at: 2026-10-05T07:20:13.887Z
updated_at: 2026-10-05T07:20:13.887Z
---
Review B finding B5 on jlevy/squares#347 (https://github.com/jlevy/squares/pull/347#pullrequestreview-5411026138), at head 9d2f05582. packing/devtools/check_n17_core_stress.py:1554-1556 still reads its three inputs through main's _frozen_bytes (git show REV:path), an OR-18 violation the body defers as main's code without naming a bead. Fix: name think-h8d8 (OR-18 enforcement, which records this violation) in the body's Deferred list. This bead is only the body edit; removing the violation is think-h8d8.
