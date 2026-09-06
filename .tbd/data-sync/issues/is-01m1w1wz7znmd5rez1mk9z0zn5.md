---
type: is
id: is-01m1w1wz7znmd5rez1mk9z0zn5
title: "PR #98 review R2: _begin_artifacts git failure is an uncaught CalledProcessError"
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m1w1w81t7vmr0gem6d91wg8b
created_at: 2026-09-06T19:07:39.135Z
updated_at: 2026-09-06T19:16:33.783Z
closed_at: 2026-09-06T19:16:33.783Z
close_reason: "Fixed: _begin_artifacts wraps git in (OSError, CalledProcessError) and raises StepFailureError('artifact provenance: git ...'); test added."
resolution: null
duplicate_of: null
---
validate.py:643-693 runs git with check=True; main() catches only UsageError/StepFailureError/ProjectLayoutError. Fix: catch (OSError, CalledProcessError) and raise StepFailureError with a diagnostic.
