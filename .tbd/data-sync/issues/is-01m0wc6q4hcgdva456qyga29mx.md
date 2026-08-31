---
type: is
id: is-01m0wc6q4hcgdva456qyga29mx
title: Correct a false duplicate-key diagnosis from overlapping inspection output
kind: bug
status: closed
priority: 2
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
delegate: codex-root
labels: []
dependencies: []
parent_id: is-01m0w9a47h5zrn7jf16pp2kpxs
created_at: 2026-08-25T11:52:02.437Z
updated_at: 2026-08-25T11:57:21.613Z
closed_at: 2026-08-25T11:57:21.612Z
close_reason: "Completed as a correction: direct source and HEAD inspection disproved the duplicate-key claim. No clean session line was edited; D-298 records the overlapping-range inspection error."
resolution: null
duplicate_of: null
---
The coordinator concatenated sed ranges 245-430 and 430-720, so shared line 430 appeared twice in terminal output and was misread as a duplicate YAML status key. Direct numbered inspection of both the working file and HEAD proves the source was clean. Retract the source-defect claim, retain D-298 as the inspection-validity error, and make no session edit for a nonexistent duplicate.
