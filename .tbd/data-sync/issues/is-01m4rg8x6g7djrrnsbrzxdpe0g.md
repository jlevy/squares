---
type: is
id: is-01m4rg8x6g7djrrnsbrzxdpe0g
title: "Intake #557: Kleddamag's candidate proof of s(17) = L"
kind: task
status: in_progress
priority: 1
version: 5
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-12T16:48:58.063Z
updated_at: 2026-10-13T00:59:55.135Z
started_at: 2026-10-12T16:49:03.371Z
---
Lane K1 of #557 (https://github.com/jlevy/squares/issues/557): acquire Kleddamag/the-seventeenth-square-candidate at 653b9589d and release large-files-v1, run the author's check.py in an isolated venv, retain a digest-only packet (no licence for reuse), compare L with n-017's verified upper bound, and draft the register, evidence, case-record, request and acknowledgement entries for the coordinator. Issue title says n=18; the source is n = 17.

## Notes

Issue: https://github.com/jlevy/squares/issues/557 (title says n=18; the source is n = 17).
Lane K1 of the #557 intake, 2026-10-12. Branch claude/wizardly-meitner-wqn4x3-k17-intake.

Done:
- Acquired Kleddamag/the-seventeenth-square-candidate at 653b9589d0f8a152f01adc56b1d48ba53d49abc3
  and the 12 assets of release large-files-v1 (4,785,719,080 bytes) into the shared scratch
  src/; every SHA-256 equals LARGE_FILES.tsv and the release's asset digests; MANIFEST.sha256
  9ecfa0db00fc9afaf98c6df8eeee920df8cb1e4737c88521ac3c64366ec7689e and check.py
  c17240b5189821c9244b1e5568e7d6b73c3c4de0fae741ec4206f9852d86a7cb equal the release notes.
- Ran check.py (read in full first) under CPython 3.12.3 + SymPy 1.14.0, Node 22, isolated:
  CHECK RESULT: PASS (levels 0-2; 7118 files, 22013 pins, 41 checks), exit 0, 809.7 s wall,
  793 CPU-s.
- Packet packing/resources/web/kleddamag-n17-candidate-2026-10-12 (no upstream bytes; 49 files
  pinned by blob and SHA-256; release assets by SHA-256; derived facts; receipts), commit
  5043afc33, README follow-up be249242c, both pushed to claude/wizardly-meitner-wqn4x3-k17-intake;
  acquire_source --check passes; packing-validate --records exit 0; packet tests 362 passed
  (the push tier's whole-suite reachable-tests step hit its 1,800 s cap under shared load,
  the other 15 steps passed).
- Exact comparison (Python 3.14, devtools.check_n17_root_certificate and exp-237/245): the
  statement's F, G, rectangle and side map are our H-255 chart exactly; L is strictly below
  n-017's verified ceiling by 1.0358e-22 and inside the statement's enclosure.
- Prices from the author's records: capture 2,347 CPU-hours (1,273 Python + 1,074 Node),
  trees 7.4 CPU-hours (6.05 + 1.38) on the author's arm64 machine.
- Drafts in the session scratch k17/: register-draft.yaml (T-153, optimality, V0/C1 with lane K2's read as external_review, S5),
  evidence-draft.yaml, verifiers-draft.yaml, bibliography-draft.yaml,
  source-coverage-draft.yaml, case-record-draft.md, result-requests-557.yaml,
  acknowledgement-draft.md, trial-T153.diff (the whole trial on origin/main 06c425eca plus the
  packet, which passed --records).

Waiting on: the records lane's fast-path PR registering T-153; a budget for the complete
replays (C3).


The parent of this bead is:
---
type: is
id: is-01m4padgs7fh6ze3tbh57d5ar1
title: "Intake pass 2026-10-11: six new upper-bound reports, two n17 issues, four unread comments, six watched repositories"
kind: epic
status: in_progress
priority: P1
version: 62
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
child_order_hints:
  - is-01m4padhpzys6zpwepcve5pwxm
  - is-01m4padjx7fep1w6y30v4pqz9n
  - is-01m4padkz7c8b0chp1f85vmfy8
  - is-01m4padmx9cdj5hsv7snr426rb
  - is-01m4padnyzybc7ms1bryby9ax2
  - is-01m4padq3szbdty8bmp3r2bxqh
  - is-01m4padr3md3xwace5s7695t9v
  - is-01m4pads1y316jmhb4rp0fpvpg
  - is-01m4padszrtqcj8b3qyff911cd
  - is-01m4padtzpm1sj8gg4ygyrjjck
  - is-01m4pan44x8vekhh54vsb2vhan
  - is-01m4pan85d4sartjf3m3h3p1b6
  - is-01m4pcbmdj7qjggrjemdjsct5v
  - is-01m4pcbp72f9p5qad5yy2jgfmf
  - is-01m4pcbr88e5we5fgkmf7qhfgv
  - is-01m3wx2hm1ezys1w50g5pk9eet
  - is-01m4pcccsnaq8tp3nvze2wfpcs
  - is-01m4pd6dbc6j1wyjg6n62dv8ag
  - is-01m4pe36zqv5wkdyp33hpb5ahh
  - is-01m4pfeqkmdtcze4v746vtn23v
  - is-01m4pff4kjeeg11941am6tb84v
  - is-01m4pn087wev95haqgv9rffnj9
  - is-01m4pgzs74gxzc2c2srp9hg2vw
  - is-01m4ptzjgr1nmf0264k67x4ypn
  - is-01m4pv16sta8jkhsfkk7sgc46n
  - is-01m4pvgyhtqs5v7fvt63f9653r
  - is-01m4qaftjqtfy02k7kdaya84an
  - is-01m4qafvvrkvvc884100g1ch9t
  - is-01m4qdj56xc8fnfdn0yz2ddvp9
  - is-01m4qdvm05t297yghevg6nm7gz
  - is-01m4qfk7nzmgrwxdj50b3h3k5w
  - is-01m4qhcw0287k3633q1rhz4jwn
  - is-01m4qhcybbrt2fnj26vxs9595n
  - is-01m4qjdc5dyqnrex0vceagw93z
  - is-01m4qjdm5hbj0m43ymvkcjr2jm
  - is-01m4qkwr49aszyn8q68yde48q9
  - is-01m4qkww5wn1cvm898ebvwfcyx
… [35 lines omitted]

2026-10-13 (session 012JUyoHafZq55vksGxE4vPP): the owner decided to hold the remaining replays. T-153 stays at V0/C1 (reported proved on n-017, verified status open). The ten trees (~7-21 CPU-h) and the full capture recomputation (~1,273 CPU-h Python, 2,347 with Node) are not to be run until the owner says so; options priced for them: a GitHub Actions matrix fan-out (public repo, ~1 day at 15 parallel), a rented 96-192 core machine (~7-14 h), or the trees alone here. Only the second adversarial review (think-4j3n) proceeds now.
