---
type: is
id: is-01m5rt5tsxbxfb0b3n9mrtqs01
title: Decide Kim's exact configurations for T-244 at 172 and 263 on both exact routes (builder as fallback)
kind: task
status: in_progress
priority: 3
version: 12
delegate: bold-ritchie-l8
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
child_order_hints:
  - is-01m692s0e5n34n064hq32vb0fs
deferred_until: null
hold: null
hold_until: null
created_at: 2026-10-25T05:57:44.893Z
updated_at: 2026-10-31T14:52:53.234Z
started_at: 2026-10-25T11:43:46.219Z
---
Decide Hyukdong Kim's exact configurations for T-244 (issue #804) at 172 and 263 on both exact routes. T-244 registers s(172) <= S*_172 and s(263) <= S*_263 as reported (V0/C0); each S* is the root of #804's irreducible polynomial of degree 24 and 17.

The author attached them at 2026-10-25T09:06:23Z (issuecomment-6395743853): t244-exact-configurations.zip, SHA-256 16e6ad9d04f1def897478e59260880320bc7c06ae89e41fa83837c7dc29c9a2d, 96,347 bytes, with n172.minpoly.json (9230aa7a...02db) and n263.minpoly.json (de646870...4686) in evand/square-packing's verify_exact.py minpoly.json format; K = Q[t]/f of degree 24 and 17, S in K. No licence stated, so the #813 import keeps the two configurations as derived exact facts (packing/resources/web/hyukdongkim-t244-configurations-2026-10-25/facts/) with the attachment's and members' digests, and none of the zip's bytes; its checker, controls and distance script are pinned by digest and must not be run.

The work:
1. A small reader of the packet's facts (review B of #813, B2). devtools.algebraic_witness_reports derive-forms reads only declaration rows with a form, and _retained_form reads each form's upstream bytes from the acquisition record's archived_path under acquire_source's custody; this packet has no declaration and keeps no upstream byte (no licence), and each form is wrapped in issue-804-configuration-fact-v1 under `configuration`. So the reader takes each fact, holds it to the packet's sources.json (exact_forms.py configurations --check against the zip is the facts' custody), and feeds `configuration` to evand_minpoly_geometry to build the algebraic witness. About half an agent-day of tooling, with its tests.
2. Decide each witness on sqpack.witness.exact_verify over K, a positive and the duplicate-square and outside-container controls a count, and on a second route: the retained verify_exact.py (evand-exact-and-local-reports-2026-10-12 packet) run unchanged on each form rebuilt from the fact's content, with its mutated controls, as T-193's replay did.
3. Check that each S in K is T-244's side: the fact's S.poly and interval against #804's polynomial and exact-sides.json's interval.
4. Measure each configuration against T-174's witness (the author reports centres within 1.8e-12 and 3.5e-13), for the regularization items' identity.
5. Register the replay evidence on T-244, take it to C3, and owe the stage 4 review for V3.

Price: the reader, about half an agent-day of tooling; then about 2 CPU-hours for both counts on both routes, up to about 8 (field degree squared times count squared from T-193's 23 October adoption). Under the 40 CPU-hour item cap, so it runs now; no deferral.

Fallback, only if the author's configurations fail: the W7-style KKT/number-field builder here (one integer relation per coordinate in Q(S*), about 516 at 172 and 790 at 263; 10 to 100 CPU-hours at 172 without python-flint, over the cap at the top), or ask the author again.

Done when: both configurations are decided on both routes and recorded on T-244, or a failure is recorded with its disposition.

## Notes

2026-10-25, review B of #813 (issuecomment-6396781432), B2: derive-forms cannot read this packet (no declaration, no retained upstream bytes, forms wrapped under 'configuration'), so step 1 is a small reader that feeds each fact's configuration to algebraic_witness_reports.evand_minpoly_geometry, with exact_forms.py configurations --check as custody; about half an agent-day of tooling before the 2 CPU-hour (up to 8) decision.

2026-10-25 15:25Z, coord-n12-1025 (triage w-triage-1025b, read-only): HyukdongKim's #804 comments of 12:00:41Z and 12:23:57Z put both earlier bundles under CC0, so the packets can retain the files themselves (step 1's small reader may be unnecessary), and report a new exact configuration at 297 (s297-exact-configuration.zip e08b5d0a, CC0; degree-21 side 3.36e-90 below T-174, checked here with SymPy). The 297 import is opened as think-ozx8, unclaimed, to share this bead's tooling. Not taken over; findings in coord-n12-1025's scratchpad triage-1025b.md.

2026-10-25 16:05Z, coord-n12-1025: on the owner's word, think-ozx8 (297) is now claimed and worked by coord-n12-1025's worker w-n297-1025. It touches #804's requests entry (read_through, a result key for 297) and a new packet for the 297 configuration; it does not touch T-244 or the 172/263 packet. If this bead's PR also edits #804's entry, expect a mechanical merge.

2026-10-26 10:55Z, takeover by w-exact-804-1026 (coordinator's brief, issue 804's queued decisions): the delegate c-decide-4rzl-1025 is a dead session (no update since 2026-10-25T15:44Z; its run was stopped by a spend limit near 18:00Z) and left no branch or open PR (origin has only claude/intake-2026-10-25-issue804-exact-sides, merged). Taking over from origin/main acc1cfc3d on branch claude/friendly-einstein-gf9z0h-exact-804 (worktree .claude/worktrees/w-exact-804-1026). Priced on a sample first: exact_verify over K at 39.6 ms a pair at 172 (300 random pairs; 0.16 CPU-h for the 14,706-pair sweep) and 23.6 ms at 263 (0.23 CPU-h for 34,453 pairs); the fact's t_interval is already tight (no refinement). Both counts on both routes are priced at about 2.5 to 3 CPU-hours, under the 5 CPU-hour item budget. Found: json.dumps(configuration) rebuilds each certificate byte for byte (its SHA-256 is the comment's stated member digest), so route 2 runs verify_exact.py on the author's exact file; 127 and 184 squares have u = [] (zero), which evand_minpoly_geometry's 1 <= len check refuses, so the reader reads an empty list as zero, as verify_exact.py does.

2026-10-31 bold-ritchie-l8 (lane L8 of the 31 October intake), taking over from w-exact-804-1026, whose session ended on 26 October and left no branch. Draft PR https://github.com/jlevy/squares/pull/861 (branch claude/bold-ritchie-xo28us-l8):

- **Reader**: devtools.configuration_fact_replay, the small reader review B2 of #813 asked for. json.dumps(configuration) rebuilds each author file byte for byte, at the comment's digests (9230aa7a, de646870). Each side is T-244's: the same polynomial, a root in K, and one real root in the hull of both intervals (receipts/side-check.json).
- **Route 1**: sqpack exact_verify over K (degree 24 and 17). Both positives VALID with every pair decided (14,706 and 34,453); the duplicate-square and outside-container jobs were refused at both counts. 147,477 pair decisions, 5,197 CPU seconds (172: 2,162; 263: 3,034); receipts/algebraic-route1-n172.json.xz and -n263.json.xz.
- **Route 2**: the retained verify_exact.py (a0f38ca8), unchanged. VALID at both counts, with 1,026 and 1,593 touching incidences as identities in K, as the author states, and 4 mutated controls refused at each; 40 CPU seconds (receipts/route2-verify-exact.json). The files list no contacts, so the moved-square control takes an axis-aligned square whose centre coordinate is exactly 1/2.
- **u = []**: 127 squares at 172 and 184 at 263 state u as the empty list; the reader reads it as zero, as verify_exact.py does.
- **Record**: T-244 is at V3/C3 with E-hyukdongkim-804-configurations-exact-feasibility and -verify-exact, both under citation deferrals naming think-3trq. #804's configurations-172-263 result maps to T-244 with validation think-3trq.
- **172**: the house moved to T-257 on 31 October (#852), 1.053e-3 BELOW S*_172, so Kim's configuration realizes T-174's retired packing. T-244 is superseded at 172 and nothing is adopted there.
- **263**: S*_263 is 2.126e-94 below the house (T-174's rational certificate). It is adopted once a stage 4 review accepts the configurations, and select_houses/upper_bound_houses read Kim's side and field witness; both are think-3trq (new).
- **Cost**: about 1.45 CPU-hours against the bead's 2 to 8 estimate.
- **Reply**: the #804 reply draft is in think-8r92.
