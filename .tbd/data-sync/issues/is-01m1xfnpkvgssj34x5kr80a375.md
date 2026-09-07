---
type: is
id: is-01m1xfnpkvgssj34x5kr80a375
title: Reject exponent syntax before graph-reader rational conversion
kind: task
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m1xffd8w5qsyw08g2356fd17
created_at: 2026-09-07T08:27:35.418Z
updated_at: 2026-09-07T08:27:35.418Z
---
Independent review found a bounded-input admission defect: Fraction is called before canonical syntax checks, permitting short exponent strings to allocate enormous integers. Root makes a minimal lexical guard and source-free non-evaluating regression; original reviewer cap remains unchanged. Do not execute the huge exponent value.
