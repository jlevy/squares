---
type: is
id: is-01m121k75y3sdhhvyg3h9f1cy4
title: Session records can declare a validation_command that does not exist
kind: bug
status: open
priority: 2
version: 2
labels:
  - packing
dependencies: []
parent_id: is-01m127tej32njy532m2q642418
created_at: 2026-08-27T16:42:04.348Z
updated_at: 2026-08-27T18:30:57.859Z
---
Nothing checks that a session phase's declared validation_command is runnable. Two phase records declare 'uv run --directory explorations/packing --frozen packing-validate --list-steps', which exits 2 with 'unrecognized arguments: --list-steps'. The correct flag is --list, used correctly in two other session records.

Occurrences: session-027-balanced-research-session-b.md phase 11, and session-028-bc032-n29-promotion-inventory.md phase 1, which inherited the contract verbatim when session 028 resumed the interrupted phase.

Why it matters: validation_command is the phase's declared falsifier. A command that cannot run means the phase contract was never actually executable, and the campaign's contemporaneous-recording guarantee silently degrades. This one was only found because session 028 tried to run it.

Fix: correct both occurrences to --list. Then consider a cheap guard in devtools (or packing-ledger check) that at minimum parses declared packing-validate/packing-ledger flags against the CLIs' own argument parsers, so an unrunnable declared command fails the campaign record check rather than sitting in the archive.
