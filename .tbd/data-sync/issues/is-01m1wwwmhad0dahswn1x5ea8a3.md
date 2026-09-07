---
type: is
id: is-01m1wwwmhad0dahswn1x5ea8a3
title: Record the replay of Burns's 4.4811 verifier as evidence and name the rung in the n = 17 provenance
kind: task
status: open
priority: 2
version: 1
labels:
  - n17
dependencies: []
parent_id: is-01m1wwrjmnkeq6xgkwcz4ha3zs
created_at: 2026-09-07T02:59:19.722Z
updated_at: 2026-09-07T02:59:19.722Z
---
The record holds E-n017-massaccesi-source-replay for Massaccesi's modified copy but no replay of Burns's own 268-atom certificate; grep finds no 10003 or 169476 anywhere outside the archive. Replayed 2026-09-07 in a scratch venv (CPython 3.13.12, NumPy, 7.4 s wall): atoms = 268, total_weight = 169476/10000 = 16.9476, angle_net_size = 181, b*(1+d) = 899635478111/900000000000 < 1, minimum_score = 10003/10000 = 1.0003 at k=0 and at every printed checkpoint, CERTIFICATE CONDITIONS VERIFIED, s(17) >= 44811/10000 -- matching the note's expected transcript line for line. Add an evidence entry (E-n017-burns-source-replay, origin replayed-here, novelty previously-published, source_key [Burns--Massaccesi n17], replay via uv run --frozen python resources/web/n17-lower-bounds-2026/burns-verify-n17-lower-bound-4_4811.py) with the same limitations as the Massaccesi entry: the three decisive checks are assert statements that vanish under python -O, the note is credited to GPT-5.6 Pro with Burns operating, not peer reviewed. Add one sentence to packing/frontier/n-017.md's provenance paragraph placing the 4.4811 rung (6 Aug 2026) between Green's sourceless 4.4452 / Brandwijk's 89/20 capsule (18 Jul 2026) and Massaccesi's 4.5058 (21 Aug 2026); note for the record that Burns's post names Green's value as the strongest published bound and does not mention Brandwijk's.
