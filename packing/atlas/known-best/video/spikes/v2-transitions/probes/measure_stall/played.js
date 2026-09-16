// True once the run has reached the target pair, or has stopped playing. Takes {target}.
/** @param {{target: number}} o */
(o) => window.atlasTransitions.state().pair >= o.target || !window.atlasTransitions.state().playing;
