---
type: is
id: is-01m5gh9s9h73f2y5syfmwhzjsk
title: Reconcile shared resource rendering and metadata with upstream adoption merge
kind: task
status: in_progress
priority: 2
version: 3
delegate: about_profiles_implementation
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
hold: null
hold_until: null
created_at: 2026-10-22T00:48:41.776Z
updated_at: 2026-10-22T00:54:58.997Z
started_at: 2026-10-22T00:48:51.320Z
---
Resolve only overview_sections.py, suite-file-costs.json and document-map.yaml merge conflicts, preserving the shared profile/resource implementation, exact cost and document entry unions, and incoming Couzo/Joost adoption descriptions via site_resources.py. Run focused checks after the merged release module parses. Stage only owned resolutions; do not commit or push.

## Notes

Resolved and staged the delegated upstream d7923b8d8 merge slice without committing. The overview conflict reintroduced inline resource tuples that this branch had moved to site_resources; retained the shared extraction and ported only the exact new Couzo T-223 and Joost T-196 adoption descriptions. Preserved the branch's evidenced Hosono/Manasseh identity corrections and mixed-contributor resource model. Cost manifest is the exact parent union: 753 weights, no overlapping weight changes, all25 admission records. Document-map retains every record and field from both parents; enforced schema validation and repair-check valid with no repairs.

Initial focused run:73passed,1failed,11deselected in6.13s. The failure was the expected n204 occurrence-reconciliation sequencing and cleared after the data lane froze. Ruff/format and BasedPyright zero findings; both parent unions verified structurally, and resource projection checks retain the incoming description strings exactly.

Existing snapshot --source-bytes initially measured264512602 against252MiB=264241152 (271450over). Both existing PDF custody cases passed complete PDF/index/loader checks and failed only at the cap assertion. Coordinator authorized253MiB, the smallest whole-MiB limit above the measured roster, keeping all evidence, unchanged selection, exact preclone refusal and three workers bounded at759MiB. Updated only constant, census rationale and two numeric test expectations. Final census264522594/cap265289728 leaves767134bytes.

Final targeted validation:7passed in30.62s, including both PDF custody cases, cap−1/0/+1 boundary, oversized preclone refusal and the formerly blocked shared-resource test. Ruff/format/BasedPyright and staged diff check clean. Independent Astra review found no blocker. Evidence logs: external task scratch upstream-adoption-focused-tests.log, upstream-adoption-final-focused.log, upstream-adoption-pdf-custody.log and upstream-adoption-snapshot-bytes{,-fixed}.json. No commit/push, no unrelated files edited. Coordinator owns final merge, repin and broad validation.
