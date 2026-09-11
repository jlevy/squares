// Move the virtual clock to an instant of the current pair. Takes {t}, in seconds.
(o) => {
  window.atlasTransitions.seek(o.t);
};
