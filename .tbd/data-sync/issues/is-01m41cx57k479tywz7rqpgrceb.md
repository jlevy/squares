---
type: is
id: is-01m41cx57k479tywz7rqpgrceb
title: Adopt the record-per-line writer for every large retained JSON result (stacked PR)
kind: task
status: closed
priority: 2
version: 5
labels:
  - session-169
dependencies: []
parent_id: is-01m41cx3q2pckpmsmmwq1rsngz
created_at: 2026-10-03T17:27:35.411Z
updated_at: 2026-10-03T22:33:44.896Z
closed_at: 2026-10-03T22:33:44.895Z
close_reason: "Done in the stacked PR jlevy/squares#323 (draft): devtools.check_retained_json with its allowlist and validate step; 31 retained results re-laid once by pure transform with their writers switched (batch B 212,896 -> 10,561 lines; batch C 580,497 -> 62,295; batch A 687,068 -> 82,587), every value unchanged; the convention in development.md. 27 exemptions with reasons, none pending; session-153-native-full.json left as an owner decision. Merges #305's head again after its second merge with main."
resolution: null
duplicate_of: null
---
In a PR stacked on jlevy/squares#305: inventory every tracked JSON result over about 5,000 lines (chunk-components.json at 365,916, the agenda-033/040/031 results near 180,000, session-153-native-full.json, exp-042's paths, chunk-partitions.json, translation-escape-screen.json and the rest), find the writer of each, move each writer onto the shared record-per-line writer from think-1uwx, regenerate, and keep every --check, digest and release pin consistent. Document the layout in development.md as the convention for retained JSON, and add a check that a retained JSON result over a line threshold uses it. Files whose bytes are bound by a digest, a pinned release or an external source are listed and left alone with the reason.

## Notes

2026-10-03, lane B stage 1 (read-only inventory, session-169): 99 tracked JSON files over 5,000 lines at c73d0cc25. Plan: re-lay 27 of them with sqpack.retained_json (width 1000, fill-wrapped scalar lists) by a pure transform guarded by canonical-compact equality, switching each live writer in the same commit: batch A, 8 atlas/frontier files checked byte for byte by their generators (687,063 -> 93,558 lines; 7 under DATA_PATHS, so one re-pin; build_known_best_atlas._json_text also writes resources/web/known-best-packings/sources.json, which must keep its bytes); batch B, 4 n5 case results (209,294 -> 10,181); batch C, 15 one-shot campaign results (580,497 -> 81,117). Expected: 1,476,854 -> about 156,000-185,000 lines, 39.8 -> 21.0 MB working tree; the new blobs pack to about 1.7 MB of history once (coordinator, measured). Leave alone with reasons: 38 byte-bound files (5 pinned in code or tests, 13 with digests quoted in records, 14 certificates under packing/cases, 5 certificate-format copies, 1 frozen), 29 archive files under packing/resources (never edited; a devtools.retained_data gzip follow-up per packet is the owner's), and session-153-native-full.json (owner decision: called an immutable receipt). Convention text for development.md and a check (devtools.check_retained_json with an allowlist packing/devtools/retained-json.yaml, threshold 5,000 lines, about 1.5 s, in --edit and the pull-request surface) are drafted in the lane's report. Writer additions it found (fill-wrap, allow_nan, canonical verification, linear compaction) went to lane A.

2026-10-03, stage 2 (lane B): on branch claude/ecstatic-archimedes-62hj6a-retained-json, draft PR jlevy/squares#323 stacked on #305. Commits a02a2c795 (check_retained_json, retained-json.yaml with a `pending` reason naming this bead, 23 tests, negative control, validate step in --edit/--records/pull requests, about 1.5 s), 69ec48aa1 (batch B: 8 n5 results 212,896 -> 10,561 lines), 0dd211326 (batch C: 15 results 580,497 -> 62,295; transport_ceiling_family.py keeps its writer because replay_h157_geometry pins its blob; the n32 inventory's real writer is bentz2016/m6_model.py), 28f22ae0e (development.md section). Every file re-laid once with its value unchanged; the four commits pack to 1.74 MB. Remaining: batch A (8 atlas and frontier files plus one re-pin), after #305 merges main (think-ak5w).
