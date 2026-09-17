---
type: is
id: is-01m2nz2awrxeaa1pgh6e7x1vjt
title: Teach packing-validate to discover Homebrew Cairo on macOS
kind: bug
status: closed
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01m2m5zjmj7dsycs1x6yxwcwwt
created_at: 2026-09-16T20:38:24.407Z
updated_at: 2026-09-17T02:04:21.625Z
closed_at: 2026-09-17T02:04:21.624Z
close_reason: "Implemented in e8d1af2b on PR #188 (validate.py:134-138, 4250-4276, 5296; tests test_validation_environment_* and test_main_passes_the_discovered_cairo_path_to_validation_children). Closure evidence: the broad pre-push gate at da2259fb ran with DYLD_FALLBACK_LIBRARY_PATH unset on macOS on 2026-09-16 and passed (6,577 passed, 9 skipped, 49 of 80 steps, exit 0), including the cairosvg-importing modules."
resolution: null
duplicate_of: null
---
Make the developer validation entry point configure DYLD_FALLBACK_LIBRARY_PATH for child processes only on macOS, only when the caller has not set it, and only when lib/libcairo.2.dylib exists under a supported Homebrew prefix. Preserve explicit overrides, record the effective path in validation provenance, document the direct-renderer boundary, and require a passing broad pre-push run with the variable deliberately unset before closure.
