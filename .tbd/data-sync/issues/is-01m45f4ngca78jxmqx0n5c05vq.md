---
type: is
id: is-01m45f4ngca78jxmqx0n5c05vq
title: "PR #350 B4 (Low): gmpy2.mpq rebinding applies in every mode; fix the claim or skip it when recording"
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
labels: []
dependencies: []
parent_id: is-01m45f4dj0p0t4bsxjnxcz5whv
created_at: 2026-10-05T07:23:36.331Z
updated_at: 2026-10-05T07:23:36.331Z
---
Review B finding B4 on jlevy/squares#350 (https://github.com/jlevy/squares/pull/350#pullrequestreview-5411026984), at head 9179aab7d. packing/devtools/n17_bb_native.py:134-139 rebinds Fraction and Q to gmpy2.mpq in the pilot and cover modules for every run once the extension is installed, --save-certificate and --taylor included. No wrong output found (both exact; rational() serializes identically; the certificate-fallback test passes), but the body says those modes 'use the Python paths unchanged'. Fix (pick one): skip the rebinding when recording, or say the rational type is rebound in every mode.
