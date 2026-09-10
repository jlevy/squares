---
type: is
id: is-01m20w2mg6aykhxw8khp0frpw9
title: "gate-budgets: the full tier's reference shape is not a CI shape, so its drift rule can never arm"
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-09-08T16:02:05.446Z
updated_at: 2026-09-08T16:02:05.446Z
---
devtools/gate-budgets.yaml declares the `full` tier's reference shape as 2 cpus at `--jobs 2 --inner-jobs 1`. No hosted runner offers that shape (ubuntu-latest reports 4 cpus), and the only CI invocation of the tier is the three-skip `validate` job at `--jobs 1 --inner-jobs 2` (1795.48s on run 34214731500), which the gate reports as "within the declared band ... not the full tier's reference, so the band was reported and not enforced". So `measured_seconds` stays null and the drift and stale rules for `full` can never arm as declared; the register's own comment warns that leaving an old reference in place "is how a band stays permanently unenforced".

Decide one of: (a) re-declare the reference to the shape CI actually runs the tier's largest piece at and record the first reading; (b) drop the reference for `full` and say plainly that only the ceiling applies, since CI never clocks the tier end to end; (c) keep the 2-cpu reference for the local full checkpoint only and add a second, CI-shaped entry for the validate job. Found by the independent audit of PR 129 (D-484); D-472 applies to whatever reading seeds it.
