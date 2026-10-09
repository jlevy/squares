---
type: is
id: is-01m4fhtg9da0y5514xbzg58cr6
title: "Resolve Couzo raw-byte retention conflict between #460 and the known-best-packings policy"
kind: task
status: closed
priority: 1
version: 7
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m4fdxw81pt2v4k29y9n58rn6
hold: null
hold_until: null
created_at: 2026-10-09T05:22:53.357Z
updated_at: 2026-10-09T06:05:18.481Z
started_at: 2026-10-09T05:30:32.181Z
closed_at: 2026-10-09T05:54:33.662Z
close_reason: "Owner-approved policy amendment and record truthfulness fixes pushed at #442/#469"
resolution: null
duplicate_of: null
---
#460 retains raw Couzo certificate and decimal-pose bytes (source/*.gz, facts .xz) on a factual-data rationale; known-best-packings/README.md says Couzo packets retain no upstream byte; #466 and #469 are derived-only. Owner decision needed before merging the stack.

## Notes

Owner decision 2026-10-09 (in session): keep #460's retained factual Couzo certificate/decimal-pose files and amend the known-best-packings policy to permit retaining factual numeric data from unlicensed sources while prose stays hash-pinned. #466/#469 remain derived-only (permitted, not required).

Amended at #442 4c5085de3 (head 49d33c0c2): known-best-packings/README.md new 'Retained Factual Data' section (owner decision 2026-10-09; factual data of packing sources may be retained bound to upstream identities; prose/programs never copied; retention grants no licence; derived-only still allowed); wording aligned in upper_bound_packets.py docstring, resources/README.md:528, Couzo 09-27 and de Winter packet READMEs. No bytes, flags, data or pins changed. Inventory: #442 Ry-Xu, #448 Gupta, #460 Couzo retain factual upstream files; main Couzo/de Winter/SQUISH, #466, #469 derived-only. Follow-ups sent: Ry-Xu sources.json raw_asset_retained rows; #469 packet README wording.

Follow-ups: #442 04767870f: build_known_best_atlas._source_index marks Ry-Xu rows (path = ryxu reports fact_path) raw_asset_retained true with 'Complete factual certificate text retained losslessly; no upstream program or prose is copied.' (field describes the upstream file named by the row url, cf. UnitSquare/evand/Gupta true); sources.json regenerated via update_selected([70]); 17 rows changed, n51 stays false; no DATA_PATHS change. #469 649f76bb9: packet README and couzo_followup_reports docstring say derived-only form. Propagation: #448 conflicts in build_known_best_atlas.py retention dict; keep evand, ryxu and gupta branches; re-run build_known_best_atlas --check --sample. Old-rule rationale left in atlas/known-best/README.md:280 (DATA_PATHS), generated witness text build_known_best_atlas.py:1247, squish_second_update_house_links.py:28, resources table 643-650.
