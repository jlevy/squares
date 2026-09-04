---
type: is
id: is-01m1qcnppk7e67rxdhn9h3ddbe
title: "colgen.generate_adaptive(decide=) default: flip deliberately, with tests"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m1qcc9devr6mz0m6erxswxjc
created_at: 2026-09-04T23:39:43.187Z
updated_at: 2026-09-04T23:39:43.187Z
---
PR 80 flips the public default from True to False to enforce freeze-then-decide, which is this branch's own rule (D-441). A default on a public generator function is a behaviour change; port it with a test on each side of the default and a note in the function's docstring, not as a side effect.
