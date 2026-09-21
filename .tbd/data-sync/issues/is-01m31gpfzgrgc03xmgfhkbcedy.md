---
type: is
id: is-01m31gpfzgrgc03xmgfhkbcedy
title: D-506 recorded_in points at X-040, which never mentions it
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m31gn7263sfhfbq8xfabkh3p
created_at: 2026-09-21T08:18:09.517Z
updated_at: 2026-09-21T08:18:09.517Z
---
PR 204 review finding F3 (Medium). packing/defects.yaml D-506 names X-040 as recorded_in, but grep finds only D-505 there (X-040:274); X-040 never mentions D-506, Lemma 7, or the 0.505/sqrt2 inversion. defects.md:4 promises the narrative lives in the artifact named by every row, and render_defects.py:180 makes recorded_in the row's only link, so the link lands on a document that does not discuss the defect. validate_schemas.py:238-240 checks only that the path exists. Fix: add a sentence to X-040's R3 paragraph, or repoint D-506 at the session record.
