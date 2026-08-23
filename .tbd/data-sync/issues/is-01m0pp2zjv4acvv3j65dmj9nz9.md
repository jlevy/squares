---
type: is
id: is-01m0pp2zjv4acvv3j65dmj9nz9
title: README restates counts that drift; remove them and check what remains
kind: bug
status: closed
priority: 1
version: 2
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels: []
dependencies: []
parent_id: is-01m0pp24qsn326dyxy9na7wc50
created_at: 2026-08-23T06:49:19.195Z
updated_at: 2026-08-23T07:01:14.471Z
closed_at: 2026-08-23T07:01:14.470Z
close_reason: Counts removed from README's defect section; the qualitative points (the dangerous defects flatter, the gate is not what finds them) are kept without numbers, and the numbers now live only in defects.md and the reconciled synopsis. Added tools/check_readme.py, wired into test.sh as step 14, covering README's links and anchors, its layout tree against the directory, and its report index against docs/project/research/. Fault-injected seven ways before wiring in.
resolution: null
duplicate_of: null
---
README's 'What has gone wrong here' repeats numbers owned by defects.yaml. It has now been wrong twice in one session: '28 defects' and '8 fixes left no regression check' against a live 29 and 7. Per common-doc-guidelines 'Avoid duplication' -- do not repeat content in higher-level docs when the details are in referenced lower-level docs. Remove the counts, keep the qualitative point, point at the generated view and the synopsis. Then extend tools/check_synopsis.py (or a sibling) to reconcile README's remaining factual claims, so the next drift fails the gate instead of being noticed by a reader.
