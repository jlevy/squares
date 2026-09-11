// The law's force at each penetration, which is the gap read the other way round.
// o.penetrations is the list of depths.
(o) => o.penetrations.map((p) => window.atlasTransitions.lawForce(-p));
