---
type: is
id: is-01m0wmfncxtt2ffk5b9pdtf504
title: Fail provenance timeout path closed on Windows
kind: bug
status: open
priority: 1
version: 1
spec_path: explorations/packing/src/sqpack/cli/validate.py
delegate: codex-root
labels:
  - packing
  - robustness
  - portability
dependencies: []
parent_id: is-01m0vpakbh6fy8p18cxsmtydgd
created_at: 2026-08-25T14:16:44.189Z
updated_at: 2026-08-25T14:16:44.189Z
---
The bounded quiet-returncode helper added for provenance Git probes initially omitted the Windows fail-closed guard used by the captured-output seam. On Windows it could launch normally but later call unsupported os.killpg on timeout/interrupt, falsely implying tree cleanup. Add the same early refusal and a focused platform control; record the draft defect.
