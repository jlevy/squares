---
type: is
id: is-01m0vd88eem4tfvmqf7z833eat
title: "PR26 R4: repair exp-012 orphaned provenance and validation claim"
kind: bug
status: open
priority: 2
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-frontier-assurance-and-verification.md
labels:
  - review-finding
dependencies: []
parent_id: is-01m0vd6xfaz5p8ccnq6xrnr5x5
created_at: 2026-08-25T02:51:07.085Z
updated_at: 2026-08-25T03:02:29.182Z
---
Source: PR #26 owner review R4. The review reported exp-012 commit 5384209 as orphaned in a fresh checkout. Reproduction on 2026-08-24 with a new single-branch clone of remote head f1d1c2b shows the commit object present and git merge-base --is-ancestor exits 0; the full 30-step gate passes, so an orphan annotation would be false and is rebutted. The actual diagnostic defect is that test.sh labeled a missing commit object in a shallow or incomplete checkout ORPHANED. Distinguish UNCHECKED history-incomplete from a known non-ancestor, keep it fatal with fetch guidance, rerun the full gate, and report the evidence in the PR disposition.

## Notes

Disposition in progress: provenance assertion rebutted with normal fresh-clone evidence; misleading shallow-history diagnostic fixed in test.sh and conventions.md. Final commit SHA and validation to be added after push.
