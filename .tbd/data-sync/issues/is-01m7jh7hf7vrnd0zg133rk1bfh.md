---
type: is
id: is-01m7jh7hf7vrnd0zg133rk1bfh
title: "Import #1005, #1006 and #1007: s(292) by Özden and by de Winter, s(262) and s(295) by de Winter (T-310 to T-313), adopt and regularize in the 2026-11-17 pass"
kind: task
status: in_progress
priority: 1
version: 7
delegate: c-import-1005-1117
labels: []
dependencies:
  - type: blocks
    target: is-01m7khyh9zn4ssnwrqk014gn8r
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
hold: null
hold_until: null
created_at: 2026-11-16T15:57:20.740Z
updated_at: 2026-11-17T01:29:11.834Z
started_at: 2026-11-16T15:59:56.835Z
---

## Notes

L193 (bold-ritchie-l193), claimed 15:59:56Z: claimed=[think-qag8], skipped=[]. Worktree branch claude/bold-ritchie-xo28us-l193 from origin/main f9ddfeeef.

Pins: #1005 kenaznia-doga/s292-upper-bound dec930bdaa5f58077af6c05bc13c0fca0a58a3ed (head and only commit, 15:27:16Z; ls-remote 16:02Z). #1006 JoostdeWinter/square-packing fe13d47b02232167cdd99b6c597617daed41e007 (head, 15:37:03Z; adds n292/REGISTRATION.md and SHA256SUMS to 796ff3b, which #1006 names; certificate blobs identical; ls-remote 16:02Z).

Controls plan stated before any program decided either certificate: scratch l193/controls-plan-1005-1006.md SHA-256 ee357f3ccb714bb1f71444fa4cb1a48d19c68e4b3bf47a8b2b889b96f11f1dc9, hashed 16:05:04Z; 6 gross jobs (3 per certificate) and 22 sharp rows (11 per certificate), with the touching-wall branch (expected for #1005) and the touching-pair branch stated in advance. Only sha256sum had read the certificate bytes (both match the issues' / SHA256SUMS digests).

Adoption target: the 2026-11-16 pass; switch to 2026-11-17 if adoption + stamps + re-pin are not pushed and green by about 21:00Z (coordinator, switch point 20:30Z).

2026-11-17 coord-intake-1117: reclaimed. The bold-ritchie coordinator's last renewal was 2026-11-16T16:00Z (epic is-01m684vn); lanes L192/L193 pushed no branch (git ls-remote finds no claude/bold-ritchie-xo28us-l19x) and are silent 9.5 h. Scope widened: #1007 (262, 295) and #1009 (13 counts incl. 292, 262, 295) arrived after; #1005/#1006/#1007 go in one import PR, #1009 in its own after it. Re-parented to think-p02d.
