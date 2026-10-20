---
type: is
id: is-01m4v4tvhns5ht9adcxznerzwd
title: Result pages link only the evidence's review_artifact, not the result's reviews list (T-153's second review is unlinked)
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-10-13T17:26:46.579Z
updated_at: 2026-10-13T17:26:46.579Z
---
The live result page for T-153 (https://jlevy.github.io/squares/result/t-153.html, deployed from 5584b2283) links the first adversarial review, docs/project/reviews/review-2026-10-12-kleddamag-n17-candidate.md, but not the second, docs/project/reviews/review-2026-10-13-overbeck-n17-candidate-second.md. The second review is named in the page's next-rung prose, and the n = 17 case page links both.

Cause: `devtools/result_overview.py` builds the "Review" row from the evidence record's single `review_artifact`. A result's `reviews` list is read only by `result_status.latest_review`, to derive the status, and no renderer links its documents. #577's description said the page renders `reviews`; it does not.

Fix options: (a) render every `reviews[].path` in the result page's links (each result with more than one review gains a link, and the URL register and its checks change with it); or (b) add the second review to T-153's `artifacts`, which #577 avoided because it changes the page's registered URL identity. (a) is the general fix. Done when every review a result lists is linked from its page and `check_published_site` holds the page to that.
