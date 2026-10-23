---
type: is
id: is-01m5khtbaccs0tnz12bmxqdpvt
title: Audit routine CI versus paper publication and PDF diagnostics
kind: task
status: closed
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: site-followups-ui
labels: []
dependencies: []
parent_id: is-01m4ke1dkg5m43rszjm49ar77r
hold: null
hold_until: null
created_at: 2026-10-23T04:55:27.817Z
updated_at: 2026-10-23T05:01:01.201Z
started_at: 2026-10-23T04:55:36.155Z
closed_at: 2026-10-23T05:01:01.200Z
close_reason: Read-only audit complete; exact job/scope/aggregate map and accepted next-slice proposal retained in notes. No source edits or tests. Existing implementation and D-509 trackers remain open.
resolution: null
duplicate_of: null
---
Read-only audit requested by owner: PDF failures should not be part of fast checks all the time. Map Pages PDF/print/reproducibility jobs, effective path scopes and required aggregates; propose a narrow fast versus publication/on-demand split preserving functional artifact checks. Record proposal only in bead notes while PR743 is frozen; no source edits or test runs. Reuse D-509 think-6dle and existing CI optimization work instead of duplicating them.

## Notes

Read-only tier audit, 2026-10-22. Coordinator accepted this proposal for the next slice after PR743; no source changes, test runs, retries, branch-policy changes or performance claims are part of this audit.

Evidence and current graph

- Read `tbd guidelines ci-and-gates-rules`, `release-engineering-rules`, development.md Validation Loops, Pages/Packing/deep-gate workflows, pages_scope.py, producer RENDER_INPUTS and existing workflow/scope/PDF tests. The named `packing-validate --fast` is not the direct source of the current PDF exporter failure: development.md requires both packing-required and pages-required before ready/merge, and Pages owns the exporter.
- `.github/workflows/pages.yml`: every pull request starts the workflow. PR scope uses pages_scope --diff HEAD^1 HEAD. Push/main uses the long explicit union of producer input paths; once started, push and dispatch use --all, so even a site-only matching push builds every paper. Scope combines renderer RENDER_INPUTS, workflow commands and transitive imported tool/test dependencies. This conflates rendered-artifact inputs with inputs of validation verdicts.
- Exact PDF/print entry paths include `packing/devtools/render_n11_lower_bounds_explainer_pdf.py`, `prepare_n11_lower_bounds_explainer_math.py`, `check_print_layout.py`, `sans_instances.py`, `inspect_n11_lower_bounds_explainer_typography.py`, `packing/tests/test_pdf_math_browser.py`, its probes, the four paper renderers/templates, shared paper-type.css/paper-publication.css/site-math.css, vendored KPress and locked environment. Source/certificate/frontier/figure/witness inputs select the respective paper through its live declaration. Shared site_urls.py/site_assets.py imports also select all four papers today, including tutorial-only asset-name changes observed in PR743; imports are not proof those changes alter paper output.
- Pages `prepare` (line810) renders the lower-bounds HTML twice and recursively compares the trees. `pdf` (1123) depends on scope+prepare: sans coverage, --update (fresh-load normalized PDF quorum), test_pdf_math_browser with SQPACK_PDF_MATH_BROWSER=1, --check-artifact, four print font configurations; dispatch trace_pdf adds 20 draws and optional prepared-text reconstruction. `print-layout` (1307) independently checks reader-visible print geometry and an overflow mutation. `typography` (1395), screen, geometry, font-loading and browser-geometry are functional browser/font checks, not synonymous with byte reproducibility.
- `n11-optimality-review` (513), `n11-threshold-bound-review` (605), `square-packing-methods-survey` (700) each mixes --pdf with HTML/Markdown --check and site rendering checks. Those three exporters make a single settled print, unlike the lower-bounds repeated-load quorum. Methods also checks the PDF revision date.
- `overview` (979) and workbench do independent twin HTML/asset builds; this is generator reproducibility, separate from browser PDF jitter. `candidate-infographics` and startup-timing are dispatch diagnostics; the former is outside deployment, the latter is nevertheless a needs entry of pages-required.
- `publish` (2078) needs prepare,pdf,overview,workbench and the three paper jobs, assembles their exact artifacts and validates the whole site. `pages-required` (2267) needs scope,prepare,workbench,overview,the three papers,pdf,print-layout,typography,screen,geometry,font-loading,browser-geometry,startup-timing,publish. It checks valid scope booleans and prerequisite results. `deploy` (2365) needs publish+pages-required. Merely making pdf conditional without updating assembly/aggregates would strand or falsely green this graph.
- Packing PR partition aggregate is packing-required; main/dispatch/daily uses post-merge-required. Deep-gate is label/dispatch-selected scientific work, not the current PDF publication gate. Keep cheap exporter algorithm/unit tests and meaningful font/print negative controls in the functional tier; do not delete tests just because their filename contains pdf.

Failure classification

CI worker supplied Pages39902176281/pdf120246470385 at 739e283b6: three fresh loads produced three distinct normalized PDFs (882563/882565/882565 bytes); text Tm y coordinates differed by0.2188. Setup and sans coverage passed. Missing geometry output cascaded from exporter refusal. Prior 020c7f731 passed. Log: /Volumes/spud-ext2/agent-scratch/site-navigation-20261022/739e283b6-pages-pdf-failure.log. This is recurrence of D-509, think-6dle, not evidence that every PDF or geometry check is flaky. Full fresh-load byte/shape equivalence is a different obligation from readable text/math, correct fonts, no overflow, usable links and accurate publication/source metadata. Keep D-509 open; relocation is not a claimed causal repair.

Accepted next-slice design

1. Keep packing-required and pages-required as routine functional checks. Keep scoped HTML/assets/browser behavior and meaningful functional print-layout checks; measure the minimum print/font configuration before declaring it fast. Remove actual PDF production/repeated-load equality from the ordinary profile. Move the three paper jobs' --pdf/date/PDF artifact checks to separate publication jobs, leaving their HTML/Markdown and reader checks in pages-required. Keep small synthetic PDF algorithm/normalization/refusal tests fast.
2. Add an always-reporting `paper-publication-required` aggregate with a separate, explicit per-paper publication scope. Actual paper content/figures/print CSS/fonts/math preparation/exporter changes select publication; explicit dispatch can select a paper or all papers and full diagnostics. The selected paper's full PDF reproduction remains a publication requirement. Unrelated site changes must not start it. The scope needs a conservative unknown/unsupported-change fallback; changes in validator-only code select its tests without automatically declaring every PDF changed. Do not infer no-change from path names alone.
3. Exact aggregate migration: pages-required drops `pdf`, dispatch startup-timing and publication assembly from needs; it retains and explicitly requires success for every scope-selected functional producer/check. paper-publication-required needs publication-scope, each newly separated PDF producer and a validated-artifact carrier. It requires success for every selected publication and refuses selected-but-skipped, failed, cancelled, missing or malformed results. Register the new aggregate as required and update development.md together with workflow contract tests, rather than creating a period with an unprotected publication path. Preserve !cancelled() cancellation handling and measure each profile's own required graph.
4. Whole-site assembly needs functional producer artifacts plus the publication aggregate and validated PDF artifact carrier. deploy then needs pages-required, paper-publication-required and publish. For an unchanged paper, reuse only a previously validated PDF with an authenticated/source-bound manifest matching the complete current declared publication inputs, revision/date, toolchain/font contract and artifact integrity; verify these before assembly. A cache hit or filename alone is not evidence. Missing/stale/incompatible evidence fails closed and requires an explicit fresh publication. Promote the exact validated bytes; do not redraw during assembly/deployment. Site-only main pushes must use the same scopes instead of automatic --all, with this validated carry-forward path.
5. Full fresh-load quorum comparisons, 20-draw tracing, prepared-text experiments and the large print/font diagnostic matrix belong to explicit publication/on-demand profiles; a scheduled diagnostic can retain drift evidence without blocking unrelated routine edits. Preserve actual paper publication gates and independent functional negative controls. Any semantic replacement for brittle equality needs its own justified contract; do not silently add a tolerance or call unstable agreement correct.
6. Distinguish producer artifact input closure from checker/import dependencies in pages_scope and release-impact. Retain selection reasons and measured costs. A tutorial-only addition to site_urls.py must select tutorial/site validation without demanding four paper release dispositions or exports; genuinely shared publication constants still select affected papers. Independent twin HTML builds can be selected for generator/template/asset pipeline changes or explicit reproducibility runs, while ordinary content edits retain functional contracts; do not weaken collision, content integrity or source-receipt checks.

Required regression controls and admission

Extend existing tests/test_pages_scope.py, test_pages_workflow.py, test_release_impact.py and exporter tests: tutorial-only asset-name edit selects no paper publication; real individual paper prose/figure selects that paper; common print CSS/font/exporter changes select affected papers; validator-only change selects the checker rather than asserting artifact changed; shared constant change, mixed edit, rename/delete, unknown path, malformed declaration and unsupported parse stay conservative. Exercise aggregate decisions with success, selected skip, failure, cancellation and missing outputs. Artifact reuse tests must refuse stale/missing/corrupt evidence and changed source/font/toolchain/revision dates, and prove exact validated bytes reach assembly. Keep functional bad-font/missing-math/overflow controls. Record collection/setup/call/teardown costs and workflow wall after implementation; do not turn static selection counts into promised speedups.

Tracking: this completed audit is a child of live CI program think-ht59. Continue implementation through existing think-ifxx (bounded feedback/shared immutable fixtures), think-z9lx (selection reasons/costs) and D-509 think-6dle (browser PDF instability); think-dyyc supplies publication-only reuse/refusal precedent and think-6l2l supplies launch-versus-publication separation. These remain open. They are linked follow-ups, not artificial blockers on completing this read-only audit. PR743 source remains frozen; implementation starts on a later branch after it lands.
