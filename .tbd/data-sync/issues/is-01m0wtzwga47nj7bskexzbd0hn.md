---
type: is
id: is-01m0wtzwga47nj7bskexzbd0hn
title: Define the review-doc publication path for sessions that cannot push the default branch
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m0wtz4vb81vyh3665rt33xh2
created_at: 2026-08-25T16:10:27.209Z
updated_at: 2026-08-25T16:10:27.209Z
---
The pr-review-workflows convention says an in-repo review doc is committed to the default branch, but remote review sessions are often restricted to a designated feature branch, so the doc can only land via its own stacked PR. Record the accepted variant (review doc lands on a review branch and merges to main via draft PR) in the packing agent-session or review conventions so future reviewers do not have to improvise.
