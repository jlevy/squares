// Press one of the law's preset buttons, and read back the law it set and which button is
// lit. o.name is the preset.
(o) => {
  document.querySelector('#law-preset-seg button[data-law="' + o.name + '"]').click();
  const l = window.atlasTransitions.law();
  return {
    law: {rigidity: l.rigidity, repulsion: l.repulsion, attraction: l.attraction, range: l.range},
    on: Array.from(document.querySelectorAll('#law-preset-seg button'))
      .filter((b) => b.classList.contains('on')).map((b) => b.dataset.law),
  };
}
