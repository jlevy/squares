// The retained record's side at one size, with the open-ended run's state settled first.
// o.n is the size.
(o) => {
  window.atlasTransitions.optimizeState();
  return Number(JSON.parse(document.getElementById('atlas-data').textContent).facts[String(o.n)].side);
}
