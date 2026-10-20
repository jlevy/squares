---
type: is
id: is-01m50wds4q4nzbdkzrcy6t3ja4
title: "Audit: inventory regularization state of every count's displayed drawing (n <= 324 and beyond), list the unregularized ones, starting with n = 176"
kind: task
status: closed
priority: 1
version: 5
delegate: ecstatic-edison-reg-audit
labels:
  - regularization
dependencies:
  - type: blocks
    target: is-01m50wdwfc7a00s5yxqqq4p30r
parent_id: is-01m50wdrbfnwsq05w150az5z88
hold: null
hold_until: null
created_at: 2026-10-15T22:55:16.119Z
updated_at: 2026-10-15T23:18:04.483Z
started_at: 2026-10-15T22:55:54.217Z
closed_at: 2026-10-15T23:18:04.483Z
close_reason: "Done: audit/root cause/map recorded in notes and scratchpad regularization-audit.md (2026-10-15)"
resolution: null
duplicate_of: null
---

## Notes

AUDIT (ecstatic-edison-reg-audit, 2026-10-15, origin/main 22a67ce4a, read-only).

Method: every count's drawn picture measured with regularize_select.today (the measure default_drawings uses), single-threaded, 30.1 s for n = 1..324; the house figures at the 92 view counts match default-drawings.json exactly. Joined with regularized/index.json, default-drawings.json, witness source keys, and the layer's history over 39 index commits since c606258dd. Measures L/U/N/C/T = light-axis / uneven-axis / near-axis squares / angle classes / house total of full shared sides.

State of the 324 drawn pictures:
- 58 regularized: an Evan Daniel or grid-slack view is drawn.
- 232 regular as published: the house has U = N = 0 (175 basic grids, 52 Kingbird catalogue structures, 5 others). They need no run.
- 19 partial, pending: an axis-tool view of a re-housed witness on which the strong generators never ran: 105 129 146 153 154 156 175 204 207 211 232 237 241 264 271 272 302 303 304.
- 5 partial, generators tried and nothing better (prose evidence only): 110 123 155 179 180.
- 1 NOT regularized, severe: 176. Raw house drawn, 70/71/52/83/33.
- 9 with mild residue, raw house: 102 236 258 263 269 (Evan Daniel's own regularized lists, T-146; the axis view has no gain; 236's evand view was withdrawn in bd82e3a54), and 39 55 290 291 (decimal Kingbird witnesses; the axis tool refuses them on promotion overlap; see think-yk2h).
- Beyond the horizon (n > 324): nothing is drawn, only claims by count and source in the coverage register. The URL registry has no drawing above 324.

n = 176: the live site draws atlas/house/n-176.svg on both the homepage tile and cases/176.html (curl of jlevy.github.io/squares, 2026-10-15). The witness is Couzo's b85dee2 re-solve (T-165), with 52 squares a few thousandths of a degree off the axes. Before PR #614 the drawing was the grid-slack view of the T-151 house (run grid-slack-deg5-1013-c), 3/36/0/13/454. The axis view of the new witness is 33/73/45/76/146, which loses to the house on uneven_axis (73 vs 71), so default_drawings keeps the house.
A probe run here, regularize_grid_slack --n 176 --near-axis-degrees 5 (11.73 s on one core), gives 14/43/0/32/409, better than the house on six measures and worse on none. The exact-route selection was not run.

Pending re-run list for think-rz8c (20): 105 129 146 153 154 156 175 176 204 207 211 232 237 241 264 271 272 302 303 304. 261 was re-housed too but its house is already regular.
Risk: T-174 (PR #574, held for the owner) covers 68 counts, of which 35 now draw strong views (68 84 86 88 108 126 127 130 131 132 172 181 182 199 206 208 209 210 228 238 239 240 259 266 267 268 270 273 292 297 301 305 306 307 308). Adopting it through today's path lapses all 35.

The full per-count table and the scripts are in the session report (regularization-audit.md, delivered in the hand-back to the coordinator).
