---
type: is
id: is-01m3xhxhccxa8qwx75rsgqrqmc
title: "Correct the asymptotic record: Erdős-Graham Theorem (1) transcribed as Θ, the Roth-Vaughan 10^-100 constant's origin, and missing Kearney-Shiu/WDL citations"
kind: task
status: closed
priority: 3
version: 3
labels:
  - research
dependencies: []
parent_id: is-01m3xgkna3m3w1w50ky6gqyxyk
created_at: 2026-10-02T05:38:13.004Z
updated_at: 2026-10-02T07:07:26.226Z
closed_at: 2026-10-02T07:07:26.226Z
close_reason: Archived Karakuš 2026 (CC BY 4.0, pdf/md/raw.md), chelokot's Nagamochi note (packet at head 753079eb), five Kingbird pages and a dated reference for Daniel's explorer; corrected the Erdős–Graham transcription (O, not Θ; D-513) and the McClenagan transcription (Montgomery (3−√3)/2, Chung–Graham 2009 with plain log x; D-514, with a dated correction in the n11 research report), and recorded the Göbel origin of 10^-100, the Wang–Dong–Li constant and Kearney–Shiu's δ results in asymptotic-waste-bounds.yaml. Coordinator verified the McClenagan page and Karakuš's Corollary 6.2.
resolution: null
duplicate_of: null
---
Found by the X-049 asymptotics lane, first item verified by the coordinator on 2026-10-02 against the rendered PDF page 4 (printed page 2): packing/resources/papers/erdos-graham-1975-on-packing-squares-with-equal-squares.md line 61 transcribes Theorem (1) as 'w(α) = Θ(α^{7/11})' where the paper prints 'W(α) = O(α^{7/11})' (an upper bound; the paper says it has no nontrivial lower estimate). Correct per conventions §7 and the archive's inline-flag rule, and log in packing/defects.yaml. Also: (i) packing/frontier/asymptotic-waste-bounds.yaml says the 10^-100 constant attached to Roth-Vaughan 'appears nowhere in the paper' -- true, and its origin is Göbel 1979 p. 179-180 ('c ≈ 10^-100'); record the provenance. (ii) The register lacks Kearney-Shiu 2002 as the delta_k = s(k^2+1) - k source (archived) and Wang-Dong-Li's explicit constant 16√2+38 with no printed x_0. (iii) McClenagan 2026's history omits Wang-Dong-Li and writes √log x where WDL and Bui write log x. Verify each against its source before editing.
