---
type: is
id: is-01m225psj2z0sx407k1ma5a4sp
title: Test that the force law holds a known optimum still
kind: feature
status: open
priority: 2
version: 2
spec_path: packing/campaign/explorations/X-025-hunting-by-hand-and-the-move-set-threads.md
labels:
  - packing
dependencies:
  - type: blocks
    target: is-01m225ps2ejkzyjc45g0xj6kyh
parent_id: is-01m225hw89vjsga1wnegrwnq5a
created_at: 2026-09-09T04:09:37.601Z
updated_at: 2026-09-09T04:09:45.030Z
---
Not built. Candidate C0d of X-025, and the first test of the force law that should run.

Claim. Loaded with a retained best-known packing and run under the law with no target and no snap, the configuration does not drift: on a record with no movable square every square holds its pose exactly, and on a record with rattlers only the squares the translation-escape screen already identifies as free may move, with the container side never growing.

Why it goes first. It is a necessary condition, so it needs no discovery, no seeds and no budget argument: a law that cannot hold a known optimum still cannot find one, and every hit rate a Calibrate sweep would report is uninterpretable until this passes. It is also the cheapest test available -- 318 loads and 318 settles, no search -- and the only one for which the repository already holds the answer key.

The answer key, verified against packing/atlas/known-best/translation-escape-screen.json on 2026-09-08. Of 318 screened records (six excluded for witness shape residual: n = 68, 69, 103, 105, 110, 131), 296 have at least one square that can be translated, 5,323 squares in all, of which 2,714 can be pushed clear of everything they touch. So drift is not automatically a failure. The 22 records with no movable square are the 18 perfect squares from n = 1 to n = 324 together with n = 5, 11, 28, 40; on those, any drift at all is a defect in the law. The largest absolute container slack anywhere is 3.7e-33, so the container side is a hard ceiling on every record and a settle that grows it has overlapped something.

Instrument. A small extension. The workbench already loads a retained packing as a starting arrangement, already runs a settle with the snap and the target off, and already reports the deepest overlap and the side the arrangement would need. What is missing is the driver: load each record, settle, report per-square displacement and turn against the loaded pose, and join against the screen's own movable_squares list. Same shape as the headless measure_law.py harness the prototype carries. Depends on think-j30w for the best-known start.

Criterion, declared per record before the run. No movable square: maximum per-square displacement and turn below a stated tolerance, container side non-increasing. Movable squares present: every square that moved past tolerance appears in that n's movable_squares list, container side non-increasing. Headline is three counts -- held exactly, only listed squares moved, failed -- not a mean, because the failure is categorical and a mean would hide a total failure at one n behind 300 successes.

Two confounds to handle first. The screen's one-sidedness: a miss proves only that one square cannot be translated at that tolerance; rotation and coordinated multi-square motion are outside it, so a square that turns in place is not a screen hit and needs its own tolerance. And 23 records are recorded as not stable across the screen's tolerances (n = 132, 154-156, 179-182, 206-210, 238-241, 270, 273, 297, 301, 305, 307); report those separately rather than scoring them, because on them the answer key is itself tolerance-dependent.

Research framing: X-025, candidate C0d.
