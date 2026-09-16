---
type: is
id: is-01m2nz2awrxeaa1pgh6e7x1vjt
title: Teach packing-validate to discover Homebrew Cairo on macOS
kind: bug
status: open
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m2m5zjmj7dsycs1x6yxwcwwt
created_at: 2026-09-16T20:38:24.407Z
updated_at: 2026-09-16T20:38:46.787Z
---
Make the developer validation entry point configure DYLD_FALLBACK_LIBRARY_PATH for child processes only on macOS, only when the caller has not set it, and only when lib/libcairo.2.dylib exists under a supported Homebrew prefix. Preserve explicit overrides, record the effective path in validation provenance, document the direct-renderer boundary, and require a passing broad pre-push run with the variable deliberately unset before closure.
