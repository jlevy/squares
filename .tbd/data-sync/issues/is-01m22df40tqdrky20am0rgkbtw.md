---
type: is
id: is-01m22df40tqdrky20am0rgkbtw
title: Explainer diagram expands and hides controls after window refocus
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
created_at: 2026-09-09T06:25:14.776Z
updated_at: 2026-09-09T06:28:06.647Z
closed_at: 2026-09-09T06:28:06.646Z
close_reason: "Cancelled: user clarified the window/diagram-controls request belonged to another task and asked this agent to stop."
resolution: null
duplicate_of: null
---
When the interactive square-packing explainer is left for another window and revisited, the diagram expands to fill the page and the explainer controls disappear. Reload restores the article layout and controls. Reproduce against the live explainer artifact, identify lifecycle/layout cause and add a focused regression before fixing. The first transport control must keep |< while paused and show a backward circular restart arrow while running, with accessible labels Go to start and Restart respectively.
