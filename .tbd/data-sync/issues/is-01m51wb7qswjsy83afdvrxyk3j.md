---
type: is
id: is-01m51wb7qswjsy83afdvrxyk3j
title: "PR #641 C2: gate cannot tell a hand-dropped PENDING_ALLOWED entry from a decided one"
kind: task
status: in_progress
priority: 2
version: 2
delegate: user-eb-addr-641-650
labels:
  - regularization
dependencies: []
parent_id: is-01m50wdvvpwz9asfq2gvaxfz5w
hold: null
hold_until: null
created_at: 2026-10-16T08:13:07.193Z
updated_at: 2026-10-16T08:13:15.765Z
started_at: 2026-10-16T08:13:15.765Z
---
PR #641 Review C, finding C2 (Low): https://github.com/jlevy/squares/pull/641#pullrequestreview-5544510088

Since review B1 of #641 (c720d982b), `default_drawings.count_state` reads `PENDING_ALLOWED` (packing/devtools/default_drawings.py, the `n not in allowed` test in the regular-as-published branch), so the list is an input to the state and not only a measurement of the pending set. Two consequences the gate (`--check-state`) does not catch:

- Removing one of the 14 historical-lapse entries (105, 129, 146, 153, 156, 175, 176, 211, 237, 241, 271, 272, 302, 304) passes once the count's new house reads regular: the count reads `regular-as-published` and the runs its bead owes are dropped. The gate cannot tell that removal from a decision.
- Adding a count whose house reads regular holds it `pending`, and the gate passes; before B1 it refused that addition.

#641 documents both as reviewed decisions (the PENDING_ALLOWED comment, the module docstring, the guide's "When a Witness Changes", policy section 8's state paragraph and the runbook's "Adopt a House, Then Regularize It"), and asks such a pull request to show the bead's runs or `default_drawings --compare` output.

Fix proposed by the review (option a): hold the 14 historical lapses in code apart from the allowlist, e.g. a `HISTORICAL_LAPSES` map with each lapse's generator and adoption commit, read by `count_state` where it reads `lapsed` and only while the axis record is drawn; then drop the `n not in allowed` test so the list is measured again. A strong view, once admitted, outranks the map, so it never needs to shrink. This changes the state rule chosen in round 1 (B1 option b), the record's `lapsed` field and its tests, so it needs its own review.

Waits on: a design call (coordinator or owner) between option (a) and keeping the reviewed-removal rule. Moot, and closable, once #644 (think-la7h) and the think-kpm3/think-3zi3 batch have decided all 14 historical-lapse counts, since the hole exists only while those entries are on the list.
