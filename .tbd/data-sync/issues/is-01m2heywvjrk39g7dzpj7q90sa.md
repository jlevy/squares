---
type: is
id: is-01m2heywvjrk39g7dzpj7q90sa
title: "PR #160 review D54: browser-floor contract tests pass with the floor off"
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T02:39:56.786Z
updated_at: 2026-09-15T02:40:56.314Z
closed_at: 2026-09-15T02:40:56.313Z
close_reason: "Fixed on #160 at f7a640a2: declared Biome overrides only, no relaxation outside the four-flag ratchet, trackers must be live beads read from the tbd sync store, Biome's verbose file lists must cover every tracked script and stylesheet; each with a negative control, and seven config mutations fail. tsconfig comments repointed to think-n711 in #175's wording."
resolution: null
duplicate_of: null
---
Review finding, PR #160 stack triage (2026-09-14), lane D-tools.

Browser-floor contract tests passed with the floor off: a broad Biome override passed (`"motion_lab" in text`), a child `tsconfig` could set `checkJs: false` if it named any tracker, a closed tracker was accepted, and Biome scope was checked by suffix globs only. Program-list item (d) was fixed at f9099096.

Source: #125 F19; the closed-tracker check is also #160 R24's suggestion.

Files: `packing/tests/test_browser_floor_contract.py:139-153`, `:171-183`, `:186-216` (@bb3f7c99); `tsconfig.json`, `tsconfig.probes.json`, `tsconfig.motion-lab.json` comments.
