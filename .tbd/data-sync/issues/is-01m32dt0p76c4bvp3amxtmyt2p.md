---
type: is
id: is-01m32dt0p76c4bvp3amxtmyt2p
title: "Research block (W1): the Kleddamag n=17 certified bound 461300/99853"
kind: epic
status: open
priority: 1
version: 8
labels: []
dependencies: []
child_order_hints:
  - is-01m32dtr6vcxbhe76ej1fabqba
  - is-01m32dtrtvte19pensvfq0rtk5
  - is-01m32dtsk35safvs7ney6xv5fp
  - is-01m32dttakchrezsyqkyew4jet
  - is-01m32dz753apsmvrx2mybxqzhb
  - is-01m32e146z8pd8bjx4d7kxw2sr
  - is-01m32e153zhsye4s1xafvyvkq1
created_at: 2026-09-21T16:46:53.639Z
updated_at: 2026-09-21T16:50:47.551Z
---
External artifact published 2026-09-21 claiming s(17) > 461300/99853 = 4.6197910929..., above both the 461300/99999 = 4.613046 that PR 211 registers and the intermediate 461300/99951 = 4.614154.

Source: https://github.com/Kleddamag/17-squares-certified-bound (HEAD a499e2c7, tag v1.0.0).
Cloned read-only into the gitignored attic at attic/17-squares-certified-bound.
Announced at https://x.com/kleddamag/status/2102034741683708034 with the chain:
ojoshe 4.59 (Sep 4), Mira 4.613029 (Sep 8), Guzhou0806 4.613046 (Sep 19),
Mira/Guzhou 4.614154 (Sep 20-21), Kleddamag + Codex 4.619791 (Sep 21).

The artifact carries PROOF.md, two exact checkers (Python polygon edge projections and a
JavaScript adaptation of Guzhou's R038 clamped-extrema geometry), 7853 exact angle
intervals, separate audits over 31412 containment inequalities and 3403 boundary/event
samples, and a NOTICES/ directory crediting this repository (Joshua-Levy-MIT.txt,
Joshua-Levy-LICENSE-source.txt) alongside Mira and Guzhou.

Entry point W1 research-survey, opened at the owner's request during the session that
landed the agenda-040 overnight stack. Correctness blocks follow this one.

Not yet adjudicated. No bound moves until the proof review and the replay both report.
