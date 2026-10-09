---
type: is
id: is-01m1sx5m1p5868jhwcdzfkvada
title: The mutation-snapshot cap has 0.9% headroom and the record keeps growing
kind: task
status: in_progress
priority: 1
version: 16
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m3p5wj25knm7rbx0g4a4tpvg
child_order_hints:
  - is-01m3qzn1k3708fhtrsw1mqdgvk
  - is-01m45xb9xadcds46ctgqra9aw2
  - is-01m4fzyh9p9bz01rgq7wpx4vwr
hold: null
hold_until: null
created_at: 2026-09-05T23:06:30.837Z
updated_at: 2026-10-09T09:29:45.526Z
started_at: 2026-10-05T11:32:06.787Z
---
Measured 2026-09-05 after pruning packing/site/ and the link-preview card: the snapshot is 66,490,716 bytes against a 67,108,864 cap, 99.1% of it, 618,148 bytes of headroom. SNAPSHOT_MAX_BYTES' own comment says a guard with 2% headroom fires for the wrong reason; 0.9% is worse than the case it warns about, and the next committed artifact of any size trips it.

The cap has now been reached four times -- D-371 at 40 MiB, 2026-08-27 at 41,943,040 when the atlas SVG work landed, D-422 where 12 MB of the breach was bytecode the gate wrote into the tree it was measuring, and 2026-09-03 when the H-052 lane's solver state took it to 90,031,065. Each was answered by pruning or by raising, and the growth is the research record doing what it is supposed to do.

The comment names the durable fix and defers it: 'pruning what no control reads is the alternative to raising this again, and it belongs with the tier work rather than here.' The largest counted files under packing/ are chunk-components.json at 9,672,604, exp-042's result at 5,740,789, chunk-partitions.json at 5,220,955, bc-200-state-191-50.json at 2,545,923 and known-best-1-100.svg at 2,333,310 -- 25.5 MB in five files, over half the packing subtree's 48,054,972.

The composite SVG is the clearest candidate and was deliberately NOT taken here: it is named by no control (grep of controls.yaml gives zero) and is the same class as its PNG, PDF and 2x exports, all three already pruned. What stopped it is the second condition the existing entries state and check rather than assume -- 'read by nothing a control runs' -- which needs the controls that drive build_known_best_atlas --check and the deterministic SVG rendering step traced before the file is removed from a sandbox they run in. That trace is the work; the four large JSON results need the same one.

Also worth deciding rather than inheriting: the walk counts the working tree, not the git tree, which is why gitignored output could ever enter the number at all.

## Notes

2026-09-09, after the cap was raised from 128 to 160 MiB for T-026's registration.

The commit message for that raise says "nothing there is prunable". That is too strong,
and the measurement taken afterwards says so.

Excluding seven files from the snapshot -- `lane-a2-threshold-certificate-191-50-net360.json`
and the six largest lane A3 receipts, all under
`packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/` -- recovers
exactly 1,193,568 bytes and takes the tree to 133,930,591 bytes, under the OLD 128 MiB cap.

So a prune existed and was available at the moment of the breach. It was not taken, and
the reason is a real one rather than an oversight: those seven files are evidence, not
generated output. Every other prune this bead records (the composite SVG and its exports,
the bytecode of D-422, the site directory) removes something a renderer can rebuild.
These cannot be rebuilt without re-running the measurement, and removing them changes the
SOURCE SURFACE the controls exercise -- which is the second condition this bead already
insists on checking rather than assuming.

What this note buys: the next breach starts from a measured alternative instead of from
"nothing is prunable". Whoever hits it should decide explicitly between (a) raising again,
(b) pruning generated views after tracing the controls that read them, which is the work
this bead is about, and (c) pruning evidence files, which needs a policy on what the
record keeps rather than a size argument.

The 1,193,568 bytes are also the scale to keep in mind: it is under 1% of the tree, so
even taking the evidence prune buys roughly one more registration, not headroom.

2026-09-16: PR #189 measured the clean hosted mutation snapshot at 168,058,379 bytes, 286,219 bytes over the 160 MiB ceiling. This is tracked source growth, not cache drift; the Animate branch itself added only compact retained evidence plus maintained source. The ceiling was reset to 192 MiB, restoring about 32 MiB of operating headroom and bounding three portable workers at 576 MiB. The bead stays open for its durable generated-file dependency audit; the cap reset is not that audit.


2026-09-16 recovery: the 192 MiB reset above is undone on PR #188 (da2259fb). With c302b330's prune of the agenda 031-035 and exp-201/202 output roots, the merged snapshot is 144,637,123 bytes against 160 MiB. The durable generated-file dependency audit this bead owns is still outstanding; between 2026-09-09 (135,122,909 bytes) and 2026-09-16 (168,058,379 unpruned) the record grew about 33 MB, of which 23.2 MB was output roots now pruned, so the unprunable growth rate is closer to 10 MB/week and 22 MiB of headroom is a few weeks, not a standing margin.

2026-09-22, PR 218 (bead think-gatp). The composite-SVG candidate this bead nominated is
disproved, and the trace it asked for is done for that half.

Traced rather than inferred: no registered control drives `build_known_best_atlas --check`,
`render_composite_pdf --check`, or any atlas step. The two controls that name
`atlas/known-best/` reach the small contact JSONs at its top level, the `touches` glob
control matches paths without reading them, and the single full-suite control refuses at
collection before a test runs. So nothing a control runs reads either composite vector's
content.

But the prune still cannot pay, for a reason this bead did not anticipate. `README.md`
links both vectors inline -- `known-best-1-100.svg` on line 31, `known-best-1-324.svg` on
line 39 -- and the root README is one of the documents `linked_pruned_targets` scans.
`snapshot_source_bytes()` returns the identical 168,251,525 with the poster pruned, with
the n=1..100 vector pruned, and with both. The copy-back is load-bearing rather than
accounting noise: four controls run `devtools.check_readme`, which calls
`check_synopsis.check_links`, which refuses any relative link whose target does not exist.
Remove the copy-back and all four report a dead link instead of the refusal they rehearse.

Four exports already in `PRUNE` are inert for the same reason: `known-best-1-324.png`,
`known-best-1-100@2x.png`, `known-best-1-100.png` and `known-best-1-324.pdf` are all
linked from `README.md` and all copied straight back, 4,646,026 bytes that never leave a
snapshot.

So the bead narrows. Struck from its scope: the composite vectors, and any prune whose
target a checked document links inline. What remains is (a) the four large generated JSONs
-- `chunk-components.json`, `chunk-partitions.json`, `exp-042`'s result and
`translation-escape-screen.json`, 23.7 MB together -- which still need the same trace, and
(b) the structural fix this measurement newly identifies: a link scan that tolerates a
pruned target, or a placeholder for one, which is the only thing that would let the
composite vectors and the four inert exports actually leave the snapshot.

The 2026-09-22 breach itself was answered without any of that. Agenda 041's output root
joined `PRUNE` for a net 10,624,188 bytes -- the same retained-output class as agendas 031
and 033--035 -- taking the snapshot to 157,627,337 with the 160 MiB cap unchanged. Agendas
037, 038 and 040 were examined and excluded: tests and `devtools/check_class_record_claims.py`
read them from outside the record.

Do not close this bead on the strength of the above. Half its trace is done and the other
half is not.

2026-09-29 PR 246: think-r5x7 prunes only agenda-040/one-spare-inventory-n32.json (3,344,052 bytes), after consumer and independent Sol review. Other agenda-040 files remain. Two focused tests pass; snapshot measured 167,182,901 bytes against unchanged 167,772,160-byte cap, leaving 589,259 bytes. This bounded repair does not discharge structural headroom work. Inventory is retained in Git; regression forces reconsideration if it becomes a linked or registered dependency.

2026-09-29 PR246 main merge: snapshot rose above the unchanged 160 MiB cap after new records. A proposed integrated-fast.log prune was rejected because Session088 links it inline and the dependency copier correctly restores it. Reviewed replacement omits only session-152-validation/validation-timings-validate-1.zip (499,501 bytes) from temporary workers; its sole prior reference is a plain session output path. Archive and source session stay in Git; dependency copyback remains active. Three focused tests, Ruff and BasedPyright pass; snapshot 167,292,104 bytes, 480,056 bytes headroom. This narrow repair does not close the broader structural headroom issue.

Read-only Sol design audit (Session164): separate existence-only links from content inputs. A frozen worker manifest may record existing tracked regular non-Markdown files deliberately omitted under PRUNE; link checks may consult it only for those missing targets in a negative-control worker. Preserve full bytes for Markdown fragment checks, registered evidence and traced content readers. Two composite SVGs plus four linked exports could save about13MB, subject to measurement. Do not use placeholders or allow arbitrary missing paths. Required tests: real and mutated dead links still fail; pruned binary links pass; Markdown anchors read real content; registered evidence stays byte-identical; baseline README/SYNOPSIS/documentation checks pass in workers. Broader generated-output pruning needs per-command input closure/read traces, not controls.yaml mutation targets or validation touches (neither is a read set). chunk-partitions.json and translation-escape-screen.json are direct schema-check inputs; exp-042 is a replay input. Fixed cap cannot absorb unbounded genuinely required evidence forever; separately measure that growth and revise the storage budget deliberately. Design only, not implemented or benchmarked.

2026-09-30: T-060 intake reached 167,821,919 required snapshot bytes after four measured non-input prunes, exceeding 160 MiB by 49,759 bytes. Restore the established roughly 32 MiB operating headroom at 192 MiB without deleting linked proof evidence or changing copied bytes, runtime ceilings or oversized refusal. Durable dependency-aware selection remains open. Consolidated duplicate think-n2kg here; child think-9b01 fixes a separate profiled ancestry-comparison cost (focused local call 6.23s to 0.74s). Proof geometry lanes continue independently.

2026-10-05, the n=17 stack breach (PR 360, `claude/n17-fixed-witness-certificates` at e62bed3a6, hosted suite-b run 37298541719): `snapshot_source_bytes()` read 201,854,760 against the 201,326,592 cap (192 MiB), 528,168 over. Decision: option (b), pruning a generated view after tracing the controls that read it. Committed as 40aa3be3a on PR 347 (`claude/n17-sessions-167-168`), so every layer and PR 365 inherit it. The cap is unchanged. Separately, the cascade lane answered the same breach on PR 360 in 93a6839ca by pruning the Sessions 169-179 X048 exploration folders whole (net 2,122,114 bytes, an evidence-folder prune by PR 347's 167/168 precedent). The two prunes are independent; together they leave PR 360 about 9.7 MiB under the cap (201,854,760 - 2,122,114 - 8,559,777 = 191,172,869).

Per-layer measurements, taken on clean checkouts in one worktree with the harness's own walk:

- main dee22b882: 193,929,477
- PR 347 c89b841d4: 198,617,904 (+4,688,427: exp-242..248 n=17 receipts and certificates, the new n=17 devtools and tests, review docs)
- PR 354 e6cc6c715: 199,050,890 (+432,986: X048-session-169-pilots)
- PR 355 405e12a88: 199,933,289 (+882,399: X048-session-170/171/172 support packets)
- PR 356 01f003980: 200,453,499 (+520,210: X048-session-174/175/176 packets)
- PR 360 e62bed3a6: 201,854,760 (+1,401,261: X048-session-177/178/179 packets)
- PR 365 27b787a1c: 201,562,154. Its branch does not yet contain the current heads of the layers below it. Its own delta over the merge-base 451154f60 is about +261 KB, so after merging PR 360 it would sit near 202.1 MB.

Every layer's growth is X-048 receipts plus their probes and tests: evidence (c), not prunable under (b).

What made (b) possible: e4ad5cedd (2026-09-30) trimmed the root README and removed its inline links to both composite vectors and to the four exports already listed in PRUNE. The 2026-09-22 blocker recorded above (README links them, so `linked_pruned_targets` copies them back and pruning saves zero) therefore no longer holds. The remaining links are in packing/atlas/README.md, packing/atlas/known-best/README.md and FIGURE-PLAYBOOK.md. `linked_pruned_targets` does not scan those files and no control link-checks them: `check_links` runs only on the root README and SYNOPSIS, and the ledger's `dead_links` only on campaign/. Since that commit the four exports have also been effective prunes rather than inert ones.

How the trace was done (logs in the session scratchpad, snaptrace360 and snaptrace360b; runner snaptrace.py, scanner snaptracescan.py, per-file walk snapmeasure.py): all 170 registered controls were run in their own worker trees at e62bed3a6 under `strace -f -e trace=%file`, and all 170 fired. One pitfall worth knowing: on the first pass, 80 bare-`python3` controls resolved to the system interpreter and died on PEP 758 syntax, which is the AGENTS.md trap. They were re-run with the venv on PATH. Results:

- `known-best-1-100.svg` (2,350,537) and `known-best-1-324.svg` (6,209,240): opened by four controls, all of them `check_readme`. The only path is `scan_retired_workflow_identifiers`, which reads every text file in the worker's own git index looking for a retired token. A pruned file is absent from that index, so it leaves the sweep rather than turning up as missing. `check_generated_markdown` lists `atlas/known-best` but keeps only `*.md`. No other control stats, opens or lists either vector. No control drives `build_known_best_atlas --check`, `render_composite_pdf --check` or any atlas step. The full-suite control still refuses at collection without touching any tests/ file. Verdict: PRUNE.
- Checks on the prune at 40aa3be3a: all 170 controls fire (`run_negative_controls -j 3`, exit 0, snapshot source 181.3 MiB); `test_negative_controls.py` passes 32; `packing-validate --records` exits 0; Ruff and BasedPyright are clean. Unmutated `check_readme`, `sqpack.campaign.ledger check`, `validate_schemas` and `check_generated_markdown` produce byte-identical output in a worker with the vectors and in one without them.
- Saving 8,559,777 bytes: PR 360 goes to 193,294,983 (8,031,609 under the cap) and PR 347 to 190,058,127, both before the commit's own 4.5 KB.

Candidates traced and not taken:

- `composite-figure.json` (308,756), generated: opened by the 10 `validate_schemas` controls (content input), by the 4 `check_readme` controls (sweep only), and stat-ed by 2 gate-selection controls. Because `validate_schemas` reads it, it is not prunable.
- `chunk-components.json` (3,623,792), `chunk-partitions.json` (1,770,395), `translation-escape-screen.json` (1,330,667), `exp-042` (1,707,922): all inline-linked from checked documents, so a prune copies them back and saves zero. The two schema-check inputs are also read by `validate_schemas`.
- X049 `contact-shade-census.json` (1,015,137) and `family-census.json` (690,619), generator-owned with byte-for-byte `--check`: inline-linked from the X-049 exploration, so a prune copies them back and saves zero. The 30 ledger-check controls also stat them through `dead_links`.
- `measure-verifier/census/census.json` (981,349), `census-mixed/census.json` (186,847), `census-summary.json` (152,603): generated and unlinked. Only the 4 `check_readme` controls open them, through the same index sweep. They are the next (b) candidates, worth about 1.32 MB. Not taken because the vectors alone suffice, and the README-linked generated views beside them would need their own trace.
- `session-153-native-full.json` and `.rows.jsonl` (6,930,103): linked, and `test_negative_controls.py` asserts they stay.
- `t007-consumer-audit.json` (887,080): a control target.
- exp-238/exp-239 certificates (4,717,067 and 6,198,237): registered or linked evidence.

Option (c), evidence, for scale only and not taken: the X-048 session folders this stack adds total about 3.2 MB. #347 already prunes the 167/168 pilot folders whole.

Pre-existing finding, not caused by this change, and identical with or without it: in a worker, unmutated `check_readme` (layout tree names root files the snapshot does not copy), `validate_schemas` (FAIL bibliography.yaml, plus verifier paths under the pruned resources/) and `ledger check` (missing .github/PULL_REQUEST_TEMPLATE.md, and a dead directory link from exp-249 into the pruned X048-session-168-pilots/certificates/; `linked_pruned_targets` copies files, not directories) all exit 1. The controls that drive those commands are therefore scored over a red baseline, the blinding class the PRUNE comments warn about.

The worker red-baseline defect is filed as think-nns5 (P1, child of this bead). This bead stays open: durable dependency-aware selection is still the work.
