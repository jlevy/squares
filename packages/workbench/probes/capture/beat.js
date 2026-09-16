// The beat the page is on for its range: whether continuous play is on, and the range's own duration.
() => ({
  continuous: window.atlasTransitions.continuous().on,
  range: window.atlasTransitions.range(),
});
