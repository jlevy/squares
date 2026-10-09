---
type: is
id: is-01m4fhtg9da0y5514xbzg58cr6
title: "Resolve Couzo raw-byte retention conflict between #460 and the known-best-packings policy"
kind: task
status: closed
priority: 1
version: 6
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m4fdxw81pt2v4k29y9n58rn6
hold: null
hold_until: null
created_at: 2026-10-09T05:22:53.357Z
updated_at: 2026-10-09T05:54:33.662Z
started_at: 2026-10-09T05:30:32.181Z
closed_at: 2026-10-09T05:54:33.662Z
close_reason: "Owner-approved policy amendment and record truthfulness fixes pushed at #442/#469"
resolution: null
duplicate_of: null
---
#460 retains raw Couzo certificate and decimal-pose bytes (source/*.gz, facts .xz) on a factual-data rationale; known-best-packings/README.md says Couzo packets retain no upstream byte; #466 and #469 are derived-only. Owner decision needed before merging the stack.

## Notes

Follow-ups: #442 04767870f: build_known_best_atlas._source_index marks Ry-Xu rows (path = ryxu reports fact_path) raw_asset_retained true with 'Complete factual certificate text retained losslessly; no upstream program or prose is copied.' (field describes the upstream file named by the row url, cf. UnitSquare/evand/Gupta true); sources.json regenerated via update_selected([70]); 17 rows changed, n51 stays false; no DATA_PATHS change. #469 649f76bb9: packet README and couzo_followup_reports docstring say derived-only form. Propagation: #448 conflicts in build_known_best_atlas.py retention dict; keep evand, ryxu and gupta branches; re-run build_known_best_atlas --check --sample. Old-rule rationale left in atlas/known-best/README.md:280 (DATA_PATHS), generated witness text build_known_best_atlas.py:1247, squish_second_update_house_links.py:28, resources table 643-650.
