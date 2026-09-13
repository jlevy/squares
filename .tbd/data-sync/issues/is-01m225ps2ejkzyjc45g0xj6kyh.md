---
type: is
id: is-01m225ps2ejkzyjc45g0xj6kyh
title: "Build Calibrate: sweep the strategy over known records with a held-out split"
kind: feature
status: open
priority: 2
version: 2
spec_path: packing/campaign/explorations/X-025-hunting-by-hand-and-the-move-set-threads.md
labels:
  - packing
dependencies: []
parent_id: is-01m225hw89vjsga1wnegrwnq5a
created_at: 2026-09-09T04:09:37.101Z
updated_at: 2026-09-13T05:02:03.076Z
---
Not built. Deferred until Pack and Animate are clean, which is a sequencing decision and not a lack of interest.

What it is. The third mode of the workbench, and candidate C0b of X-025 in executable form: choose the cases whose records you are optimising against, choose which strategy parameters vary and over what ranges, run seeds per configuration, and rank by the fraction of runs landing within tolerance of the record at a declared budget.

Why it is cheap once Pack is right, and why that is the reason to wait. Mechanically Calibrate is Pack's strategy panel with a loop and a results table around it: the same single-n settle, the same parameters behind the same setters, the same gap read at the end. Nothing new has to be modelled. The corollary is that every part of Calibrate that turns out to be hard will be a part of Pack that was left approximate, and it will be discovered a thousand runs at a time -- so Pack and Animate come first.

What it must report. Two kinds of best, and both of them. Per run, the single configuration that reached the lowest container side, which is the one to look at and the one most likely to be luck. Statistically, the configuration whose distribution over seeds is best by median or by hit rate within tolerance, which is the one to believe. A mode that reports only the first is a slot machine; a mode that reports both, and shows how far apart they are, is an instrument.

The held-out split, which is the whole hazard. Tuning on cases whose answers are known is fitting to a test set, and a setting that wins on the tuning cases has established nothing about unseen n. The split must be declared before the first run and the headline must be the held-out score, not the best score found. The naming does real work here: a mode that shows the calibration set and the held-out set side by side makes the question 'which set did that number come from' structural rather than a caution in prose.

Open, and the owner's, and it must be answered before the build: is the split declared per session or per run? X-025 argues per session, because a split chosen after seeing results is not a split, and per-run declaration is a declaration in form and a search in practice. The answer decides whether the split lives in the run record or the session record, so retrofitting it means every earlier number is unscored.

Prerequisites already tracked: think-7v26 (the rigidity slider reaches settings the timestep cannot hold, and a sweep would visit them with nobody watching), think-tswc (steps per second under Node, which prices a sweep before it is committed to), and the C0d stationarity test, which is the necessary condition every hit rate here depends on.

Reuse rather than start parallel machinery: the campaign's hypothesis records, pre-declared accept rules and devtools/run_arm_sweep.py are the same shape. Research framing: X-025, candidate C0b.

## Notes

2026-09-12 plan disposition: retain held-out calibration methodology as a Search preset under think-vhgz, not a separate tab or run engine. See updated annealing and workbench plans; Search is deferred until records, metrics, shared semantics, strict floors and packages/workbench extraction pass.
