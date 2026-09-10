---
type: is
id: is-01m20vzx7zyeaqj8ss54mzdeck
title: "Records gate: an honest terminal state for a session whose cost was not measured"
kind: feature
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-08T16:00:36.094Z
updated_at: 2026-09-08T16:00:36.094Z
---
A session record that is finished but cannot be terminalised is a time bomb: session-099 (PR 130) had to be extended twice because the records gate refuses a terminal session without a rollup, while the ledger's deadline rule fails every commit on main once an in-progress deadline passes. There is no honest way to say "this session is over and its cost was not measured".

Where the refusal lives: check_session_rollups.py ("terminal session declares no resource_rollups", no exemption above session-045) and close_session.py (about line 260, "terminal and declares no rollups"); AgentSession is `additionalProperties: false` and `resource_rollups` is a plain string array, so there is no field to carry a reason.

Design the durable fix (OR-1): either (a) an explicit unmeasured terminal state, e.g. `resource_rollups: unmeasured` plus a required reason, which the cost checks accept and the close report renders as measured: false with the reason, or (b) a waiting state (awaiting_rollup) that the deadline rule does not judge, so a record blocked on an external input is not red on the clock. Whichever is chosen, `terminal sessions name what they cost` must still fail a silent omission. Session-099 is the first consumer; its deadline is 2026-09-10T13:50Z.
