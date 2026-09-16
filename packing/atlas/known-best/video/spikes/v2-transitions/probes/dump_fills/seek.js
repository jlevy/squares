// Move the clock to one instant of the pair on the stage, in seconds from its start. Takes {t}.
/** @param {{t: number}} o */
(o) => window.atlasTransitions.seek(o.t);
