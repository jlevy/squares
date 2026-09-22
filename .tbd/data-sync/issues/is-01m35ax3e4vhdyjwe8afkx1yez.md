---
type: is
id: is-01m35ax3e4vhdyjwe8afkx1yez
title: Negative controls demand no green baseline, so a checker red in every worker blinds its controls silently
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
created_at: 2026-09-22T19:53:52.305Z
updated_at: 2026-09-22T19:53:52.305Z
---
run_one in packing/devtools/run_negative_controls.py scores a control on 'exited non-zero AND printed the expected message'. It never establishes that the command is green on the unmutated snapshot. A checker that fails in every worker before any mutation is applied therefore produces either a wrong-message failure (noisy, what happened on 2026-09-22) or, with a looser expect string, a silent pass over a checker that never ran.

Evidence, 2026-09-22 on PR 218 (bead think-gatp): commit a4bdfae4c registered packing/resources/bibliography.yaml as a validated dataset at packing/devtools/validate_schemas.py:297 while packing/resources stayed in PRUNE. 'python3 -m devtools.validate_schemas' then raised FileNotFoundError in every worker, and all ten controls driving it were scored as failing -- four on the defect log, three on the frontier, the full-cell geometry channel and two more. Fixed for that path by rescuing it into COPY_SEPARATELY, which does not close the class.

The PRUNE comment block in run_negative_controls.py already names this weakness in prose (the exp-052 checkpoint paragraph, on check_canonical and archived_n11). This bead is to make it a guard rather than a warning: run each distinct control command once per worker against the unmutated snapshot and refuse the run if it is not green, or an equivalent that costs less than 40 distinct baseline commands. Measure the added wall before adopting -- the controls step is already ~544s on CI with its own 1800s budget (OR-17).
