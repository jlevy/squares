// Moves the clock of the pair on the stage to one instant, in seconds. Takes {seconds}.
/** @param {{seconds: number}} o */
(o) => window.atlasTransitions.seek(o.seconds);
