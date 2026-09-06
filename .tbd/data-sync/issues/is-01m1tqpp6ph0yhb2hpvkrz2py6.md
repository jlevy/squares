---
type: is
id: is-01m1tqpp6ph0yhb2hpvkrz2py6
title: "B4: certificate.py says the certificate proves s(n) > L; everything else says >="
kind: bug
status: in_progress
priority: 2
version: 2
labels:
  - review-claude
dependencies: []
parent_id: is-01m1tqpgrh5ym0r6e5apbke7p8
created_at: 2026-09-06T06:50:13.078Z
updated_at: 2026-09-06T06:50:21.187Z
---
sqpack/fractional/certificate.py: the module docstring opens with 'It proves s(n) >= L' and concludes 's(n) > L'; bounded_side says 'what the certificate proves is s(n) > L. Reported as >= L'. The strict form is true by compactness but is not what the claim documents prove. Make the docstrings consistent (>= L, with a one-line remark that > L follows by compactness), and add that remark to the explainer's Contradiction section as the review suggests: the claim is stated as >= because that is what the verifier's theorem proves without compactness.
