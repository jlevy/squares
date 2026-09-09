---
type: is
id: is-01m20zztsqytk9pzr8cj930m0y
title: Replica exchange over a pressure ladder, once a pressure ladder exists
kind: feature
status: open
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m20zyy839t6mbvpqy8ay2hsn
created_at: 2026-09-08T17:10:27.892Z
updated_at: 2026-09-09T00:20:13.428Z
---
Replica exchange over a pressure ladder is the one annealing-family scheme the 2026-09-08 survey found that is currently producing packing records: Basurto, Gurin, Specht and Odriozola identified 108 novel maximal disk packings at N = 300 to 720, with Packomania's maintainer as a coauthor. Hard particles are athermal, so pressure rather than temperature is the parameter worth exchanging.

Blocked on a prerequisite the round-1 record establishes: exchanging over a ladder needs a ladder parameter that actually changes the landscape, and exp-136 measured the wall-pressure weight mu as having no detectable effect over three orders of magnitude. Do not build the exchange over mu. Build it over the inflation pressure once that arm exists, which is why this depends on the inflation bead.

Shape: R replicas advanced in lockstep, adjacent-pair swap attempts on a Metropolis criterion in the ladder parameter, one seed per replica. The repository's parked GPU measurement was of the wrong axis of parallelism: the parallelism worth having here is over replicas, which needs no arithmetic intensity per configuration.
