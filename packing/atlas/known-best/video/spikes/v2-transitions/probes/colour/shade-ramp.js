// One angle's five shades, from no contacts to four. o.angle is the angle.
(o) => [0, 1, 2, 3, 4].map((k) => window.atlasTransitions.fillsFor([o.angle], [k])[0])
