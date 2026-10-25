---
type: is
id: is-01m5rt5tsxbxfb0b3n9mrtqs01
title: Decide Kim's exact configurations for T-244 at 172 and 263 on both exact routes (builder as fallback)
kind: task
status: in_progress
priority: 3
version: 6
delegate: c-decide-4rzl-1025
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
deferred_until: null
hold: null
hold_until: null
created_at: 2026-10-25T05:57:44.893Z
updated_at: 2026-10-25T11:43:46.221Z
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
