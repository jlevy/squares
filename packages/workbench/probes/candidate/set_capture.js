// The capture preview, which is the state a still is taken in. Takes {on}.
/** @param {{on: boolean}} o */ (o) => {
  window.atlasTransitions.setCapture(o.on);
};
