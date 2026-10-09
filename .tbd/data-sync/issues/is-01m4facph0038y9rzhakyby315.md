---
type: is
id: is-01m4facph0038y9rzhakyby315
title: Open the hero case popover and navigate to expanded Atlas cases
kind: feature
status: in_progress
priority: 1
version: 9
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10.local
labels:
  - website
dependencies:
  - type: blocks
    target: is-01m4ex3gpzxxh9eqemc2r78p4e
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-09T03:13:00.958Z
updated_at: 2026-10-09T04:33:56.534Z
started_at: 2026-10-09T03:14:19.707Z
---
Homepage hero contains native SVG packings11,53,203 (latest counts supersede11,26,53), side by side centered with40rem wide-screen cap and text-width minus small margin on narrow screens. Exact shared caption: The best packings known for 11, 53, and 203 identical unit squares. Colors indicate angle. Darker colors mean more common shared faces. Each opens its own shared case popover and retains canonical noJS link. Keep social card case53. Popover record/Frontier-row/Atlas-tile actions follow current case; Atlas fully expands before reveal. Preserve relative URLs, keyboard, noJS and history; verify203destinations with existing11/53behavior.

## Notes

Hero now contains native SVG packings11,26,53 in threeequalcolumns, centered and capped40rem onwide screens, text-width minus1rem onnarrow screens. Onecaption: The best packings known for11,26,and53 squares. Each example has itsowncanonicalcase link/data-case/accessiblename and opensmatching sharedpopover; socialcardHERO_CASE53 unchanged. Three targeted markup/home/socialcard checks passed13.07s; Ruff/Biome/probeTS/diffclean. Live1280/390 threeequal-square drawings and centered geometry passed; pointerpopoversall3 plus keyboard11/Escape focus eachwidth passed; noJS26canonicalnavigation passed. Root inspected fresh desktop/mobile hero screenshots; Astra source review has no findings. Homepage refreshed8766. Prior popover record/Frontier-row/Atlas-tile actions, expandedtarget/history53/291/324 checks18passed and26Nodefetchfallbackchecks remain recorded. Localdraft only, no publication or merge.
