---
type: is
id: is-01m7wz60j1aa28dswm7yb52gre
title: "Import #1042's comment 7022143149: de Winter's 155 lower bounds from 18 to 313 (base85 archive; 61 corner-family rows on T-180's coverage)"
kind: task
status: in_progress
priority: 2
version: 3
delegate: codex-intake-1119-01a1fb
labels: []
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
hold: null
hold_until: null
created_at: 2026-11-20T17:13:35.041Z
updated_at: 2026-11-22T23:48:22.217Z
started_at: 2026-11-22T23:26:20.297Z
---
Found in stage 1 of think-fv42 (lane c15-lower, 20 November 2026). Joost de Winter's comment 7022143149 on jlevy/squares#1042 (created 21:02:44Z on 19 November 2026, edited 02:02:32Z on 20 November) requests registration of 155 strict improvements to lower bounds on s(n), at counts 18, 20, 26-31, 37-43, 50-58, 65-75, 82-94, 101-115, 122-125, 128-138, 145-148, 152-163, 179-189, 207-218, 235-240, 242-246, 248, 267-272, 274-279, 281, 301-313 (the comment's own list; 19 was withdrawn after T-194).

The certificate is a zip embedded in the comment as one base85 block, SHA-256 2035790a40ac73479e047dc6a6a861137295468458ab6b015c4aad5ebd61c3ab (48,944 bytes; decoded and matched in think-fv42's scratch, not retained): README.md, certificate.json (155 claims, an LZMA member), replay_sources.json (the Python sources) and verify_public.py, which replays against lower_bounds_2026_11_19 at JoostdeWinter/square-packing 21d944c (packet de-winter-lower-bounds-2026-11-19, think-fv42's PR).

Methods by certificate.json: family_cut 61 (modified continuous corner families that rely on Hosono's T-180 global coverage, which the record holds as reported only), boundary 43, archived_boundary 15, mixed_gap 10, derived_boundary 10, registered_boundary 7, direct 6, native_reserve 1, corner_copy 1, periodic_boundary 1. Most compare against #1042's or #1039's claims, which it raises again; the family_cut rows compare against the unclaimed corner bounds of the 21d944c folder.

This is an import of its own (runbook stage 1, step 2): triage, report order after #1042 and its 161 follow-up, retention of the comment archive, and a validation plan (T-180 inheritance is the main question). Not started.

## Notes

23:44 UTC. Custody of the exact 48,944-byte archive and its four members verified, and its source packet and maintained walk inputs are staged in codex/intake-1042-1061-source-triage-20261122. Of 155 claims, 61 family-cut rows depend on T-180. Scoped exact triage finds 148 primary rows and seven consequences; later #1060 D strengthens all 153 common endpoints. Full historical/current-case walk and proof review remain.
