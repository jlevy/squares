// Move the virtual clock to an instant of the current pair. Takes {t}, in seconds.
/** @param {{t: number}} o */ (o) => {
  window.atlasTransitions.seek(o.t);
};
