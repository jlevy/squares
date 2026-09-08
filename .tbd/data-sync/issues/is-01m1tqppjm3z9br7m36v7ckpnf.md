---
type: is
id: is-01m1tqppjm3z9br7m36v7ckpnf
title: "C1: the method's originators are never named on the page"
kind: bug
status: in_progress
priority: 1
version: 2
labels:
  - review-claude
dependencies: []
parent_id: is-01m1tqpgrh5ym0r6e5apbke7p8
created_at: 2026-09-06T06:50:13.459Z
updated_at: 2026-09-06T06:50:21.495Z
---
explainer-article.md names Stromquist, Friedman and Trump in footnotes and attributes the five-condition certificate to no one. The claim document says it is the weighted unavoidable-set argument Sam Burns proposed and Gustavo Massaccesi used for n = 17 in August 2026; the 2026-09-04 review traces the lineage to Goebel (1979) and Nagamochi (2005); certificate.py calls it the Burns-Massaccesi object. Fix: one sentence at the head of 'The Five Conditions' with footnotes to the two posts (URLs are on record in packing/frontier/evidence.yaml and n-017.md: sam-burns.com/posts/proposing-better-lower-bound-for-n17-square-packing/ and gus-massa.blogspot.com/2026/08/linear-programing-for-square-packing.html, plus 'another-better-lower-bound-for-n17'): 'The certificate is the weighted unavoidable-set argument Sam Burns proposed and Gustavo Massaccesi used for n = 17 in August 2026, descended from Goebel's unavoidable points (1979) and Nagamochi's weighted resources (2005); what is new here is the n = 11 instance and the generator that found it.' Check the register's wording for the lineage before writing it.
