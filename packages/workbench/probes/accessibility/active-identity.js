// The square identity held by keyboard focus, or the focused element's id outside the layer.
() => {
  const active = document.activeElement;
  return active?.getAttribute("data-square-index") ?? active?.id ?? null;
};
