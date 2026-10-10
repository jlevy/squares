---
type: is
id: is-01m4m1tcbeja5e99rytwg1bm9v
title: Publish the full triangular poster preview with immutable image identity
kind: bug
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-10T23:19:24.269Z
updated_at: 2026-10-10T23:23:01.302Z
started_at: 2026-10-10T23:19:42.021Z
---
Trace the homepage 324-PDF thumbnail against canonical and served PNG/SVG/PDF bytes. The user requests the full high-resolution triangular poster, not a crop or the separate Row comparison. Preserve the canonical dated PDF destination and avoid regeneration when current artifacts are already correct. Publish a content-identified image so an old same-name browser cache cannot retain the former rectangular poster.

## Notes

Source frozen: card_hero uses SiteAssets.image_file and existing content-hash _add publication under assets/images; intrinsic7497x5361 full324PNG/lazy decoding retained, no crop or Row comparison. Before export update, HTTP/preview/managed canonical PNG2839286B, SVG8020096B and datedPDF533954B are byte-equal; visually inspected HTTP PNG is triangular. Primary checkout differs and was read-only. Stable legacy image name may explain old browser cache; no direct cache proof claimed. Existing card+asset3PASS4.11s, Ruff/formatPASS, SiteAssets types0/0/0. Final hashed HTTP card proof and Home/Papers publication await coherent think-rxkc export freeze. Keep open pending that proof and final CI.
