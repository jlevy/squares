---
type: is
id: is-01m3p5wj25knm7rbx0g4a4tpvg
title: Improve validation scheduling and test-selection efficiency
kind: task
status: in_progress
priority: 1
version: 24
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m3nzy6gqfv60whzzvww0ffa0
child_order_hints:
  - is-01m3qfvpn0dgprt6f2pb61bjza
  - is-01m3qg47fdhes208jjmx8wcb04
  - is-01m3qgvz4ka0qqjz4rrham7a3g
  - is-01m3qj2s8fb8ewx3h334rtqqjf
  - is-01m3qj6hf8hnceh702waazsnhk
  - is-01m3qk36x5q25z6sqe018s8n7c
  - is-01m3qknj2hpeb1d7tyv4kvqgh5
  - is-01m3qn7w7yphc9530wk4p70qmz
  - is-01m3qnty2dvtgva1s2tdp5m33p
  - is-01m3qqpkh2brpqnksyj08wj2gj
  - is-01m3qv1yceth454ek8yyttk0n1
  - is-01m3qygbtayj0vy2v8y2ajf8ps
  - is-01m1sx5m1p5868jhwcdzfkvada
  - is-01m4d97gn20a9nddee9p1ka2sz
hold: null
hold_until: null
created_at: 2026-09-29T08:53:16.996Z
updated_at: 2026-10-08T08:14:13.665Z
started_at: 2026-09-29T21:06:47.567Z
---
Observed during PR246 W7 quality follow-up: a narrow check_documentation.py generated-Cargo-output exclusion plus its regression and review prose selects dozens of workbench/certificate/search tests under packing-validate --push, after the previous selected suite already passed2039tests. Measure import/data fanout and preserve true callers and negative-control coverage while avoiding unrelated expensive replays. Do not weaken required test semantics or merely raise ceilings. Evidence: push-rustdoc.log in task scratch and PR246 hosted/local validation comments; full selector command retained in session tools.

## Notes

Session 163 Sol read-only diagnosis: push since4296edce selects65/386 behavioral test files, not the whole suite. Six changed Python paths select56;20 prose/record paths select62; union65. WALKER_MARKERS substring matching adds44 files that are otherwise unreachable. Confirmed false positives include __import__ in an attack string, importlib.metadata.version, tmp_path-only globs and rglob in comments; actual repo walkers must remain covered. Next safe slice: AST/context-aware exclusion of proven non-repo uses, with positive repository/dynamic-import selector controls. Rank actual gate costs before implementing; current buffered log does not attribute elapsed time. No gate weakened.

Session164 measurement: merged push against132c209 selected114 of387test files; behavioral step800.92s, pytest794.17s, whole gate818.46s (2957passed/2specificfailures). This merge is genuinely broader than the original documentation-only example. Read-only scheduler audit: _push_test_step marks only an everything selection broad; for a large proper subset the default10outer jobs gives _pytest_workers=max(1,cpus-jobs+1)=1 on this10CPU host. Remaining edit steps finish while the single pytest process stays CPU-bound. Existing --jobs1 can give pytest host workers without changing selection/semantics; a future controlled reading should compare a deliberate bounded worker allocation for large subsets, preserving test-content coverage and avoiding memory contention. No scheduling change or speedup claim made; the required repair rerun retains its declared original shape.

Session164 scheduling follow-up (read-only, no rerun): current 10-CPU --push was an actual narrow selection (114/387 files), so broad-only implicit jobs=1 did not apply. With jobs=10, _pytest_workers=max(1,10-10+1)=1; reachable_tests receives no -n and its pytest ran serially (794.17s; behavioral step 800.92s; whole gate 818.46s). Safe immediate official invocation for an unchanged intended base is packing-validate --push --since <base> --jobs 1 --inner-jobs 1: xdist gets -n 10, PACK_JOBS=1 caps nested pools, and no outer validation step competes. Speedup and ten-worker memory behavior are unmeasured; keep exact selected tests, 1800s ceiling, skips and refusal semantics. Do not call --jobs 2 / --inner-jobs 1 a no-oversubscription guarantee: although it gives nine pytest workers plus one outer slot nominally, exact verification can start nine subprocesses via _command_workers(2) in that slot. Smallest candidate implementation after a paired measurement: give the reachable test step a distinct resource allocation from the edit tier (run edit steps with normal outer pool, then reachable pytest alone with bounded xdist workers), rather than changing the selector or marking a proper subset broad. Add a scheduling contract test that on 10 CPUs the large-subset path forwards a bounded >1 xdist worker count, never overlaps a CPU-wide inner command fanout, and preserves exact file selection and non-exhaustive marker. Existing two-sided selector/runner forwarding tests should remain. Do not make a speed claim until same-head paired timings and memory are recorded.

Efficiency implementation checkpoint: Sol local scheduler gives implicit large proper subsets and broad selections an exclusive pytest phase after the parallel edit pool drains; nested PACK_JOBS=1. Independent Sol review caught and repaired a missing load marker for proper subsets. Atomic optional marker lets a narrow push retain its prior conservative allocation when another gate owns the host. Explicit resource settings remain authoritative. Effective worker allocation is visible in CLI and command receipts. 28 focused tests, Ruff, BasedPyright and diff checks passed; integrated timing still pending. Hosted fanout is think-tddk; safe selector-precision follow-up is think-6izq. Durable acceptance plan: docs/project/reviews/review-2026-09-29-validation-parallelism.md. Required packing/page/mergeability CI at5d276119c passed while implementation proceeded; deferred checkpoint still in flight.

Published pre-efficiency checkpoint5d276119c now passes deferred36630574302 as well as required CI. Candidate1afb75ca6 default broad push is running with10 pytest workers and PACK_JOBS=1; late observation has9 idle workers and1 CPU-active worker near97%. No speedup claimed; read-only audit is identifying indivisible-tail vs queue imbalance and missing per-test observability. Isolated parallel main/daily parity implementation and independent review tracked bythink-08ht. PR review progress comment5899524522.
