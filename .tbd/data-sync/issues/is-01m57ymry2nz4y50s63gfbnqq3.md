---
type: is
id: is-01m57ymry2nz4y50s63gfbnqq3
title: Use actual dependent PR base for release-impact validation
kind: bug
status: in_progress
priority: 2
version: 5
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m578snhcmb9xf25bnb3atvy8
hold: null
hold_until: null
created_at: 2026-10-18T16:48:43.444Z
updated_at: 2026-10-19T06:37:44.060Z
started_at: 2026-10-18T16:48:51.049Z
---
On #676 rebased onto #661 a87de0cf7, clean2627322e1 records passes51/52 in110.18s but synopsis release impact compares main sitev0.7.25 to currentv0.7.27 and rejects correct adjacent25→26→27 history. Preserve adjacent edition validation and changelog main baseline. Select actual PR base from GITHUB_BASE_REF in hosted CI, explicit PACKING_RELEASE_BASE_REF locally, otherwise origin/main; preserve HEAD==main HEAD^1 path. Remove only redundant intake-layer n11 exemption because generated docs equal parent. Add focused own-layer pass and uncovered-input negative control plus ordinary-main selection controls before fresh records; no Stage3 registry writes before pass.
