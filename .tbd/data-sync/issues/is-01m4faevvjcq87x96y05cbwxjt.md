---
type: is
id: is-01m4faevvjcq87x96y05cbwxjt
title: "PR #449: identify and fix cold font layout shifts"
kind: bug
status: in_progress
priority: 1
version: 9
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4ekeq41zfgtf5dp8r462n05
hold: null
hold_until: null
created_at: 2026-10-09T03:14:11.939Z
updated_at: 2026-10-09T19:14:04.125Z
started_at: 2026-10-09T03:14:25.888Z
---
Exact current #449 head4963448e33c39002a48593ef79999940b153f2c0 Pages run37875117402/job113642170191 fails papers/n11-threshold-bound-review.html at390px light: CLS0.2512375662788857 exceeds the unchanged0.1 limit. The dominant native shift491.2ms reflows nav links/doc-links and hero during font loading422.1–584.2ms; all401 math nodes remain readable and task236ms passes300ms. Trace actual platform face identity and font-delivery cause with the maintained optional diagnostic, then fix production scope only after evidence and independent review. Preserve every budget, default measurement path, scientific record and source input. This is a newly observed current-head recurrence; historical think-9gu8 is closed against PR3959700cef with its own passing gates, and those receipts do not qualify this head. ROOT approves two diagnostic paths check_site_rendering.py/test_site_rendering.py and one bounded exact449 paper-only render without PDF/fullsite. Broad frontend tracker think-5jr5 remains independently open. Moderate intake_remaining_fixes owns this lane; ROOT owns publication/merges.

## Notes

2026-10-09 user-requested handoff: optional font diagnostic and isolated workflow are saved at source926ef8305300e3637bf1c742b9483109111a214e, exact accepted tree0589fc46195381bfbe5d42f0bc32c5c42a48b0b2; final normal source20-parent union d0ea1330183d343deaba0e66d66ecdcfcaaf5717/treee859c10ae6eb5e9734dfbdf91179d47491643a60 independently accepted. All four source paths committed, checkout clean, maintained DATA pin6068 unchanged. Nine default/aggregate/custody controls PASS (18.895s XML,20.07s terminal), configured types0/0/0, prior seven diagnostic controls PASS. Default gate paths and budgets unchanged. Exact4963 paper-only Mac held-font diagnostic has CLS0.0499362927 and physical .SFNS to SourceSans3 transition; this is controlled diagnostic evidence, not reproduction or qualification of Linux Pages CLS0.2512375663. Linux optional workflow has not been dispatched; no production font fix made. Keep open for future Linux physical-face attribution, narrowly reviewed production correction and actual current-head gates. Handoff receipts: review-notes/pr449-four-path-final0589-handoff-source-qualification.json and pr449-font-diagnostic-final-d0ea-handoff-composition.json. No owned experiment process remains.

2026-10-09 cloud (think-cmjh): cause identified with runner-equivalent local fontconfig (DejaVu/Liberation/Noto only, reproduces CI CLS to four digits): Source Sans 3 loses the race and DejaVu fallback is 22-35% wider (held: paper 390px 0.2506, 1280px 0.1658); frontier italic/bold PT Serif not preloaded (0.209/0.134). Production fix on #442 29a79cd10 + f020ace62 (preloads; screen-only metric-compatible local sans alias; WebKit probe fix); after: held Source Sans 0.0000 at 390px, frontier max 0.0005 in 40 runs; hosted Pages 37889299512 and Packing 37889299519 green. Not independently reviewed yet (final review round pending). Optional #468 diagnostic not dispatched: this session's token cannot dispatch workflows (403).

Round-2 senior+performance review of 29a79cd10/f020ace62 at 04767870f: no Blocker/High; root cause confirmed (parent frontier 1280 CLS 0.20859 in 1/3 samples; head 0.00001 in 6/6), new tests fail on old code, vertical overrides exact (1.024/0.93 etc.), alias draws nothing on current pages, probe skip does not weaken certification. Lows J (width approx), K (unicode-range overstated), L (64,484 B preloads on every page), M (Chromium-only proof; opaque test failure without Arial/Liberation) being addressed on #442 with N/O/P and Medium I (policy text vs Rehwaldt programs, think-efys).

Round-2 Lows addressed on #442 (head 38c3ca4f8; hosted Packing 37896427037 + Pages 37896426539 green incl. Firefox/WebKit): J comment states approximate widths with measured residuals (609fc43df); K 'draws nothing the shipped face covers' + 96 uncovered code points noted (609fc43df, 6a5ccf0e2); L preload cost and page usage documented in paper-design.md (8dd2b7cb8); M clear preflight failure without Arial/Liberation + Chromium-only note (38c3ca4f8); P _row_wiring now a setup fixture (097c80557). Follow-ups possible: retune alias widths; per-page preload list.

#468 review B (security+correctness, needs changes): B3 Medium diagnostic attribution misses text >2 levels deep yet reports complete; B2 Low diagnostic dispatch shares certificate-page concurrency group with push runs on main and blocks rerun_starved re-runs (A2's no-branch-protection reason does not cover these); B1 Low second checkout persist-credentials untested; B4 Low job comment. Security otherwise clean (contents: read, no secrets, no input interpolation, fixed SHA checkout, pinned actions). Fix agent dispatched; preferred: move diagnostic to its own workflow file.

#468 review B addressed (head 374e63b92): d181c92c9 diagnostic moved to .github/workflows/font-diagnostic.yml (workflow_dispatch only, contents: read, own concurrency group; pages.yml + test_pages_workflow.py + test_rerun_starved.py byte-identical to #466) -> fixes B2 and A2; f67a7b010 B3 per-text-node font attribution, rows with rendered text and no face fail, regression fixture with the paper's real nesting; 2b6e6bd2a B1/B5/B6 (credentials and expression pins, literal pinned input list, helper copy compare at dispatch); c57ae5dbe B4 comments; 374e63b92 test. Diagnostic dispatchable only once the file is on main; it renders the pre-fix 4963448e page by design. Keep open for one dispatch after merge.

font-diagnostic.yml is on main since d3860c97a, so it is now dispatchable; this session cannot dispatch (403). Dispatch once from main to record the pre-fix Linux faces.
