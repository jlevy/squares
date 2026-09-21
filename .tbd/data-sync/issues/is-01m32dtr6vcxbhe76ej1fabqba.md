---
type: is
id: is-01m32dtr6vcxbhe76ej1fabqba
title: Replay the Kleddamag n=17 certificate on this machine
kind: task
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m32dt0p76c4bvp3amxtmyt2p
created_at: 2026-09-21T16:47:17.723Z
updated_at: 2026-09-21T17:08:29.931Z
closed_at: 2026-09-21T17:08:29.930Z
close_reason: null
resolution: null
duplicate_of: null
---
Independent mechanical replay of attic/17-squares-certified-bound in its own throwaway venv (NOT the host project's, which pins Python 3.14 and must not take third-party deps).

Run check_integrity.py, verify.py, the audits/, verify_upper.py and independent_controls.py. Verify by computation, not by quotation: the certificate SHA-256 0288aaac680131aa675adb63ea6a67e3d363fcca6061d4c788301da7c5d69cec against the file it names; the exact integer counting inequality (17 x 1000020517 vs budget 16998427356, surplus claimed 1921433); the 7853 interval count; and whether both checkers run and agree on the histogram (RESULT.json asserts histograms_identical true).

Report anything that does not reproduce plainly rather than inferring it.
