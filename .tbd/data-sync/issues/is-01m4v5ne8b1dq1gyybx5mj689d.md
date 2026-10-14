---
type: is
id: is-01m4v5ne8b1dq1gyybx5mj689d
title: "Import Fitzharding: s(17) = L by a complete Lean 4 proof (#565)"
kind: task
status: in_progress
priority: 1
version: 15
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
child_order_hints:
  - is-01m4v5nmc9ghvpxvyvt2pc038a
  - is-01m4v5nmyq792rsjg1xyvcps9f
  - is-01m4v81zbyqd7j8x7376sx2zvq
  - is-01m4v81zv6xvy30p0a0hwsy161
  - is-01m4v820ay9e87f39mvf33zz3a
  - is-01m4v840keg820cvmfpy7s3t5j
  - is-01m4vex5amc35y6f4zqamve8q6
  - is-01m4vfsqg3sjnr9xrms9r3w7y3
  - is-01m4vhq9fgd36ctshvxs6m025x
  - is-01m4vyver4k1k50ypx40m2ga9a
  - is-01m4vyvfnafwdczzdybwgyt3pr
hold: null
hold_until: null
created_at: 2026-10-13T17:41:17.705Z
updated_at: 2026-10-14T01:01:30.154Z
started_at: 2026-10-13T17:41:23.780Z
---
Owner report of 13 October 2026 (no GitHub issue): Oscar Fitzharding's sq17-lean, https://github.com/ofitzharding/sq17-lean, and his post https://x.com/ofitzharding/status/2109798000008597616. The owner asked for a full intake crediting everything, a review of which report came first between this and Overbeck's T-153, and allowed that a formalization may be registered as its own result. Definitive name: Oscar Fitzharding (owner, 13 October).

Source facts at triage:
- Claim: `Sq17.square17_optimality (L : ℝ) : PlainPacking L ↔ EndpointGeometry.side ≤ L` in Lean 4.34.1 with Mathlib: 17 closed unit squares, independent translations and rotations, pairwise disjoint interiors, inside an axis-aligned square of side L, boundary contact allowed; existence at the endpoint included. Trust boundary: Lean kernel for geometry; 13,343 native_decide facts (Lean compiler, native evaluator, C toolchain); standard axioms propext, Classical.choice, Quot.sound; no sorryAx (verification/clean-build-receipt.json).
- Author: Oscar Fitzharding (CITATION.cff; GitHub ofitzharding; X ofitzharding). MIT licence. AI assistance: README says "substantial assistance from Claude and Codex"; the post says "Built with OpenAI Astra + Anthropic Opus 5.5" and thanks Mannaseh Ahmed (@ManassehA06) and Joshua Levy (@ojoshe) for prior work. README credits Bidwell (1998), Hämäläinen (1980), Friedman's survey, the Squares Project, Ahmed et al.'s 11SquaresFormalized, David MacIver's earlier Lean work on a 17-square lower bound, and states that Overbeck's candidate proof was published independently on 12 October 2026.
- Pins: head e6ee548090dc1dbf938ecf8590481de837a6a454 (2026-10-13T01:59:58Z); release v1.0.0 at 0a7167efa8dcae7fa73855890630fb7e2de550ed, published 2026-10-12T22:06:23Z, three certificate-source archives (1.96 GB) whose GitHub sha256 digests match manifest.json.

Chronology (UTC), from server-side timestamps where they exist:
- Overbeck: repository created 2026-10-12T13:46:05Z; release large-files-v1 published 14:24:20Z; the edition's only commit 14:40:59Z; this project's #557 opened 16:42:56Z.
- Fitzharding: first commit 20:42:00Z; repository created 20:42:08Z; release v1.0.0 published 22:06:23Z; post 2026-10-13T00:06:56Z (from the post id).
Overbeck's candidate proof is the earlier report by about six hours. Fitzharding's README names it as earlier and independent. Fitzharding's is the first complete machine-checked proof (no remaining premise, under its native_decide trust boundary); Overbeck's edition calls itself a candidate resting on 15 mathematical premises.

Planned registration (stage 3): T-153 stays the first report. A new entry, kind simplification (a second, independent proof of T-153's s(17) = L, by the epistemics.md kind rules), credited to Fitzharding, with both entries stating each other's dates. Evidence on the n = 11 precedent (E-n011-lean-formalization-report): reported, proof-assistant-checked, performed_by source-author, origin external, replay_status not-attempted, with the axioms receipt.

Stage 4 (not run without an owner budget): the full replay rebuilds 4,951 modules; the source's own command uses --jobs 40 --proof-jobs 8 and says it needs substantial CPU time and tens of GB of disk and memory.

## Notes

2026-10-13, stage 3 (Record) lane, on claude/stoic-clarke-jhfnru, local commits (not pushed):
- 3cd3b3d3c register: T-154 (simplification, V0/C1, S5 proposed), E-n017-fitzharding-lean-report, V-fitzharding-n17-lean, V-fitzharding-n17-source-manifest, coverage fitzharding-n17-lean-2026, n-017 (two priority notes, reported-lane note, prose paragraph, evidence, resource), T-153 notes and next_rung sentences, result-requests #565, bibliography note (F-1, F-2), review mapped; packet and resources README now cite #565.
- b1fe05c5d standing: a simplification that restates its case's reported value derives "second certificate, reported" (check_standing refused T-154 as superseded on a tie).
- 9b680dbd2 views; cb5251c7b site card for ofitzharding/sq17-lean (test_overview holds OTHER_PROJECTS to the coverage register); a5ab76221 re-pin DATA_REVISION to 9b680dbd.
- Check-forced changes: clock times kept out of register prose and priority-note claims (check_prose_ceremony); they are in n-017's priority_notes[].published. read_through is the issue's creation time 2026-10-12T22:23:37Z, per the schema (no comments).
- Validation: --records exit 0 (49/107); --edit exit 0 (65/107); --push exit 1 only on 4 environmental tests (2 process-reaping tests that fail at 9a8f2c4b3 too, 2 Playwright tests with no Chromium).
- Id collision to watch: PR #549's layer (regularization-policy.md on main) also plans T-154; whichever merges second renumbers.
