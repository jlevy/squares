// The law's force at each signed gap. o.gaps is the list of gaps; positive is apart.
(o) => o.gaps.map((d) => window.atlasTransitions.lawForce(d));
