---
type: is
id: is-01m0vd88eem4tfvmqf7z833eat
title: "PR26 R4: repair exp-012 orphaned provenance and validation claim"
kind: bug
status: closed
priority: 2
version: 4
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-frontier-assurance-and-verification.md
labels:
  - review-finding
dependencies: []
parent_id: is-01m0vd6xfaz5p8ccnq6xrnr5x5
created_at: 2026-08-25T02:51:07.085Z
updated_at: 2026-08-25T03:10:52.644Z
closed_at: 2026-08-25T03:10:52.643Z
close_reason: "Review premise rebutted with fresh-clone ancestry evidence; the real shallow-history diagnostic defect was fixed and tested on PR #26 head a9a2992."
resolution: null
duplicate_of: null
---
Source: PR #26 owner review R4. The review reported exp-012 commit 5384209 as orphaned in a fresh checkout. Reproduction on 2026-08-24 with a new single-branch clone of remote head f1d1c2b shows the commit object present and git merge-base --is-ancestor exits 0; the full 30-step gate passes, so an orphan annotation would be false and is rebutted. The actual diagnostic defect is that test.sh labeled a missing commit object in a shallow or incomplete checkout ORPHANED. Distinguish UNCHECKED history-incomplete from a known non-ancestor, keep it fatal with fetch guidance, rerun the full gate, and report the evidence in the PR disposition.

## Notes

Disposition complete on 2026-08-24: a normal fresh single-branch clone of published head f1d1c2b contains 5384209 and merge-base --is-ancestor exits 0, so the claimed exp-012 orphan was rebutted and no false annotation was added. Head a9a2992 instead fixes test.sh to distinguish missing shallow history as UNCHECKED with fetch guidance. The depth-1 failure path and the full 30-step gate both pass their expected outcomes. Evidence is posted at PR #26 issuecomment-5404553556.
