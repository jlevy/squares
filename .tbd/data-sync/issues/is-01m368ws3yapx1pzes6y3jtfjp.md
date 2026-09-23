---
type: is
id: is-01m368ws3yapx1pzes6y3jtfjp
title: Keep every edition in the version history, dated by first publication
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
created_at: 2026-09-23T04:37:59.036Z
updated_at: 2026-09-23T04:37:59.036Z
---
The owner (2026-09-22): the explainer lost the version history for v0.3.0; the first version in the history should be the proof of s(11) >= 381/100; its date should be when it was first published; and the top of the paper should show the original date and the latest edition, linking the full history.

Cause: PUBLICATION_HISTORY was 'the two editions retained in the explainer's short public history', pinned by two tests asserting exactly two entries. Adding v0.4.1 in a4bdfae4c kept the list at two by dropping v0.3.0. The dates were 'first_labeled' -- when a version label first appeared in Git -- not publication.

Fix: the history keeps every edition, newest first, and only grows; each is dated by first publication from the GitHub Pages deployments (v0.3.0 September 5, v0.4.0 September 13, v0.4.1 September 22, each deployment and commit recorded); the top line reads 'First published <first date> · <edition> (version history)'. Two of the three old dates were wrong in opposite directions: v0.3.0 went live September 5 and was named September 8; v0.4.0 was named September 10 and went live September 13.
