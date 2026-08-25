---
type: is
id: is-01m0wtztxd047fq62jd8sb2em2
title: Harden packing-validate timeout CLI edges and registry stop() nits
kind: task
status: closed
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01m0wtz4vb81vyh3665rt33xh2
created_at: 2026-08-25T16:10:25.581Z
updated_at: 2026-08-25T19:11:21.847Z
closed_at: 2026-08-25T19:11:21.846Z
close_reason: "Fixed in b450072: empty timeout options fail under the correct name, empty registries do not sleep, rejected subprocess output is drained, and focused tests cover the paths."
resolution: null
duplicate_of: null
---
Three small robustness nits in src/sqpack/cli/validate.py found during the PR 34 review: (1) an empty-string --timeout-seconds argument is falsy and silently falls back to the environment or default instead of erroring, and the error-name attribution in main() picks '--timeout-seconds' whenever the flag is not None even when the value came from the environment; (2) _ProcessRegistry.stop() sleeps the full termination grace even when no pids are registered; (3) the reject-after-stop path in _run waits on the killed process without reading or closing its stdout pipe, leaking the fd until GC. None affects the timeout guarantee; all are polish on the D-239 primitive.
