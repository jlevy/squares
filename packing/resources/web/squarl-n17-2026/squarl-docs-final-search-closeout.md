# Final n=17 search closeout

The final non-learning production search started from commit 553c7a36f702ec6d91ffa619ea25a65a5bc0e827 and used the exact
published reference 4.67553009360455095163411127048315. It was launched with
`scripts/run_final_search_production.sh final-search-20260805t015208z --worker`
and ran for 32390.38 seconds (8h 59m 50.38s).

It completed 36 40-proposal blocks: 576 archive mutations, 720 separator-boundary
mutations, 144 parent-conditioned topology kicks, and no frozen-source or ML
proposals. By parent, roots 37, 50 and 62 supplied 496, 468 and 468 proposals;
the bounded pre-run audit supplied eight root-13 proposals. The run evaluated
1162 centre-LP candidates and made 143 deep attempts,
with 85 valid completions, 143 valid partials and 91 timeouts. Phase B processed
30 canonical continuation jobs and left 142.

The best strict float64 width was 4.675530095599908 (exact gap
1.99535674836588872951685e-09). The independent strict-repeat/high-precision
width was 4.675530095599910 (gap 1.99535854836588872951685e-09), deterministic
replay was 4.675530003392970 (gap -9.02115813516341112704831e-08), and the
float32-safe width was 4.675530654889137 (gap 5.61284585948365888729517e-07).
The published reference was not beaten under the strict validation rule.

The detailed report and best artifacts are under
`data/experiments/final-search/final-search-20260805t015208z/`: `final-report.md`,
`best-strict-high-precision-packing.json`, `best-float32-safe-packing.json`,
`certificate.json`, and `independent-double-replay-log.json`.

The numerical caveat is explicit: the directed upper bound is not rigorous,
minimum wall and pair margins are -1.53e-16 and -3.05e-16, and two of five
nearby strict restarts encountered singular or unbounded LPs. These do not
affect the conclusion because both strict widths are already above the reference.

The defensible project conclusion is that the published reference was not beaten under
the required strict validation rule. A replay below the reference cannot alter
that conclusion when its strict antecedent remains above it. No further run was
launched.
