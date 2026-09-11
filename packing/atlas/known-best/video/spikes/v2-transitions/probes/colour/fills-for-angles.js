// The fill each angle alone takes, with no contacts and nothing else in the array, which is
// the colouring as a pure function of the angle. o.angles is the list of angles.
(o) => o.angles.map((a) => window.atlasTransitions.fillsFor([a], [0])[0])
